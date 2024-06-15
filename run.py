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
        NONE = "none"
        CACHED = "cached"
        MEMOIZED = "memoized"

    duration_seconds: float
    cache_status: CacheStatus
    

# def run_goal(target: str):
#     start = time.time()
#     subprocess.run(["time", "pants", "run", "target"])
#     end = time.time()
#     print(f"  {goal.value} took {end - start} seconds")

def package_target(target: str) -> PackageMetrics:
    start2 = time.time()
    subprocess.run(["time", "pants", "package", target])
    end2 = time.time()
    print(f"  Packaging {target} took {end2 - start2} seconds")

    split = target.split(":")
    target_dir = (DIST_DIR / split[0] / split[1]).with_suffix(".pex")
    file_sizes = [f.stat().st_size for f in target_dir.glob("**/*") if f.is_file()]
    return PackageMetrics(
        duration_seconds=end2 - start2, 
        output_size_mb=int(sum(file_sizes) / (1024 * 1024)), 
        output_number_of_files=len(file_sizes)
    )

def test_target(target: str):
    subprocess.run(["time", "pants", "test", target])

def run_simple() -> pd.DataFrame:
    df = pd.DataFrame(columns=mi)

    for layout in ["loose", "packed", "zipapp"]:
        for execution_mode in ["venv", "zipapp"]:
            print(f"  Packaging pex with execution_mode={execution_mode} and layout={layout}")
            target = f"simple:bin@execution_mode={execution_mode},layout={layout}"
            # df.loc[target, ] = 0

            p = package_target(target)
            df.loc[target, (Step.CLEAN, Goal.PACKAGE)] = p.duration_seconds
    #         test_target("simple:")
            
            p = package_target(target)
            df.loc[target, (Step.NOOP, Goal.PACKAGE)] = p.duration_seconds
    #         test_target("simple:")

            content = Path("./simple/main.py").read_text().splitlines()
            content[0] = f"# CACHE_BUSTING={time.time()}"
            Path("./simple/main.py").write_text("\n".join(content))

    #         results.append((target, package_target(target, Step.INCREMENTAL)))
            p = package_target(target)
            df.loc[target, (Step.INCREMENTAL, Goal.PACKAGE)] = p.duration_seconds
    #         test_target("simple:")

    return df

if __name__ == "__main__":
    pd.set_option('display.float_format', '{:.2f}'.format)

    all_steps = list(Step)
    all_goals = list(Goal)
    mi = pd.MultiIndex.from_product([all_steps, all_goals], names=["step", "goal"])
    # index = pd.Index([])
    df = pd.DataFrame(columns=mi)
    
    simple_results = run_simple()
    print("*******simple_results********")
    print(simple_results)
    print("*******simple_results********")
    print("")
    df = pd.concat([df, simple_results], axis=0)
    print(df)