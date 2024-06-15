from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import subprocess
import time
from typing import Final

import pandas as pd

DIST_DIR: Final[Path] = Path("./dist")

class Step(str, Enum):
    CLEAN = "clean"
    NOOP = "noop"
    INCREMENTAL = "incremental"

    def __str__(self) -> str:
        return self.value

class Goal(str, Enum):
    PACKAGE = "package"
    RUN = "run"
    TEST = "test"
    # TODO: Lint/Fix/Fmt/Check step? Do we learn anything from that?
    
    def __str__(self) -> str:
        return self.value

@dataclass
class StepMetrics:
    step: Step
    package: PackageMetrics
    run: RunMetrics
    test: TestMetrics

@dataclass
class PackageMetrics:
    duration_seconds: float
    output_size_mb: int
    output_number_of_files: int

@dataclass
class RunMetrics:
    duration_seconds: float
    startup_time_seconds: float

@dataclass
class TestMetrics:
    class CacheStatus(Enum):
        NA = "n/a"
        NONE = "none"
        CACHED = "cached"
        MEMOIZED = "memoized"

    duration_seconds: float
    cache_status: CacheStatus
    

def run_goal(target: str):
    start = time.time()
    subprocess.run(["time", "pants", "run", target])
    end = time.time()
    duration = end - start
    print(f"  Running took {duration} seconds")
    return RunMetrics(duration_seconds=duration, startup_time_seconds=0)

def package_target(target: str) -> PackageMetrics:
    start = time.time()
    subprocess.run(["time", "pants", "package", target])
    end = time.time()
    duration = end - start
    print(f"  Packaging {target} took {duration} seconds")

    split = target.split(":")
    target_dir = (DIST_DIR / split[0] / split[1]).with_suffix(".pex")
    file_sizes = [f.stat().st_size for f in target_dir.glob("**/*") if f.is_file()]
    return PackageMetrics(
        duration_seconds=duration, 
        output_size_mb=int(sum(file_sizes) / (1024 * 1024)), 
        output_number_of_files=len(file_sizes)
    )

def test_target(target: str):
    """TODO: This is just structural right now, the tests need to be parametrized first"""
    start = time.time()
    subprocess.run(["time", "pants", "test", "simple:"])
    end = time.time()
    duration = end - start
    print(f"  Testing took {duration} seconds")
    return TestMetrics(duration_seconds=duration, cache_status=TestMetrics.CacheStatus.NA)


def run_simple() -> pd.DataFrame:
    def _run_sequence(frame: pd.DataFrame, step: Step):
        p = package_target(target)
        frame.loc[target, (step, Goal.PACKAGE)] = p.duration_seconds
        r = run_goal(target)
        frame.loc[target, (step, Goal.RUN)] = r.duration_seconds
        t = test_target(target)
        frame.loc[target, (step, Goal.TEST)] = t.duration_seconds

    df = pd.DataFrame(columns=mi)

    for layout in ["loose", "packed", "zipapp"]:
        for execution_mode in ["venv", "zipapp"]:
            print(f"  Packaging pex with execution_mode={execution_mode} and layout={layout}")
            target = f"simple:bin@execution_mode={execution_mode},layout={layout}"
            
            _run_sequence(df, Step.CLEAN)
            _run_sequence(df, Step.NOOP)

            content = Path("./simple/main.py").read_text().splitlines()
            content[0] = f"# CACHE_BUSTING={time.time()}"
            Path("./simple/main.py").write_text("\n".join(content))

            _run_sequence(df, Step.INCREMENTAL)

    return df

if __name__ == "__main__":
    pd.set_option('display.float_format', '{:.2f}'.format)

    all_steps = list(Step)
    all_goals = list(Goal)
    mi = pd.MultiIndex.from_product([all_steps, all_goals], names=["step", "goal"])
    # index = pd.Index([])
    df = pd.DataFrame(columns=mi)
    
    simple_results = run_simple()

    df = pd.concat([df, simple_results], axis=0)
    print(df)