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


def package_target(target: str) -> PackageMetrics:
    print(f"--> {target}: Starting Package")
    start = time.time()
    subprocess.run(["time", "pants", "package", target])
    end = time.time()
    duration = end - start
    print(f"--> {target}: Package took {duration} seconds")

    split = target.split(":")
    target_dir = (DIST_DIR / split[0] / split[1]).with_suffix(".pex")
    file_sizes = [f.stat().st_size for f in target_dir.glob("**/*") if f.is_file()]
    return PackageMetrics(
        duration_seconds=duration, 
        output_size_mb=int(sum(file_sizes) / (1024 * 1024)), 
        output_number_of_files=len(file_sizes)
    )

def run_goal(target: str):
    print(f"--> {target}: Starting Run")
    start = time.time()
    subprocess.run(["time", "pants", "run", target])
    end = time.time()
    duration = end - start
    print(f"--> {target}: Run took {duration} seconds")
    return RunMetrics(duration_seconds=duration, startup_time_seconds=0)

def test_target(target: str):
    """TODO: This is just structural right now, the tests need to be parametrized first"""
    print(f"--> {target}: Starting Test")
    start = time.time()
    subprocess.run(["time", "pants", "test", "simple:"])
    end = time.time()
    duration = end - start
    print(f"--> {target}: Test took {duration} seconds")
    return TestMetrics(duration_seconds=duration, cache_status=TestMetrics.CacheStatus.NA)


def run_simple() -> pd.DataFrame:
    def _bust_cache():
        print("--> Busting sources cache")
        content = Path("./simple/main.py").read_text().splitlines()
        content[0] = f"# CACHE_BUSTING={time.time()}"
        Path("./simple/main.py").write_text("\n".join(content))

    def _run_sequence(frame: pd.DataFrame, step: Step, tgt: str):
        p = package_target(tgt)
        frame.loc[tgt, (step, Goal.PACKAGE)] = p.duration_seconds
        r = run_goal(tgt)
        frame.loc[tgt, (step, Goal.RUN)] = r.duration_seconds
        t = test_target(tgt)
        frame.loc[tgt, (step, Goal.TEST)] = t.duration_seconds

    df = pd.DataFrame(columns=mi)

    for execution_mode in ["venv", "zipapp"]:
        for layout in ["packed", "zipapp"]: # TODO: Removed `loose` as it's just painfully slow in this workflow
            target = f"simple:bin@execution_mode={execution_mode},layout={layout}"
            
            print(f"***** {target}: Starting sequence with execution_mode={execution_mode} and layout={layout} *****")
            start = time.time()
            
            print(f"==> {target}: Starting Pex sequence")
            start_pex = time.time()
            
            _run_sequence(df, Step.CLEAN, target)
            _run_sequence(df, Step.NOOP, target)
            _bust_cache()
            _run_sequence(df, Step.INCREMENTAL, target)

            end_pex = time.time()
            duration_pex = end_pex - start_pex
            print(f"==> {target}: Pex sequence took {duration_pex} seconds")

            if subprocess.run(["which", "docker"]).returncode == 0:
                print(f"==> {target}: Starting Docker sequence")
                start_docker = time.time()

                docker_target = target.replace("@", "_").replace("=", "_").replace(",", "_").replace("bin", "img")
                # TODO: Do something to actually "Clean" this
                _run_sequence(df, Step.CLEAN, docker_target)
                _run_sequence(df, Step.NOOP, docker_target)
                _bust_cache()
                _run_sequence(df, Step.INCREMENTAL, docker_target)

                end_docker = time.time()
                duration_docker = end_docker - start_docker
                print(f"==> {target}: Docker sequence took {duration_docker} seconds")

            end = time.time()
            duration = end - start
            print(f"***** {target}: Sequence took {duration} seconds *****")

    return df

if __name__ == "__main__":
    pd.set_option('display.float_format', '{:.2f}'.format)

    all_steps = list(Step)
    all_goals = list(Goal)
    mi = pd.MultiIndex.from_product([all_steps, all_goals], names=["step", "goal"])
    # index = pd.Index([])
    df = pd.DataFrame(columns=mi)
    
    start = time.time()
    simple_results = run_simple()
    end = time.time()

    df = pd.concat([df, simple_results], axis=0)
    print(f"Total script time: {end - start}")
    print(df)