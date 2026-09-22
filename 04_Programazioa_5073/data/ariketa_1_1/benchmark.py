from __future__ import annotations

import csv
import time
from pathlib import Path
from typing import Any, Callable

import numpy as np


N_VALUES = (1_000_000, 10_000_000, 50_000_000)
OUTPUT = Path(__file__).with_name("emaitzak.csv")


def python_sum(values: range) -> int:
    total = 0
    for value in values:
        total += value
    return total


def measure(function: Callable[[Any], Any], argument: Any) -> tuple[float, int]:
    start = time.perf_counter()
    result = function(argument)
    return time.perf_counter() - start, int(result)


def benchmark(n: int) -> dict[str, float | int]:
    python_seconds, python_result = measure(python_sum, range(n))
    values = np.arange(n, dtype=np.int64)
    numpy_seconds, numpy_result = measure(np.sum, values)

    if python_result != numpy_result:
        raise RuntimeError("Python eta NumPy emaitzak ez datoz bat")

    return {
        "N": n,
        "python_s": python_seconds,
        "numpy_s": numpy_seconds,
        "speedup": python_seconds / numpy_seconds,
        "result": python_result,
    }


def main() -> None:
    results = [benchmark(n) for n in N_VALUES]
    with OUTPUT.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("N\tPython (s)\tNumPy (s)\tNumPy-ren abiadura")
    for row in results:
        print(
            f"{row['N']:,}\t{row['python_s']:.6f}\t"
            f"{row['numpy_s']:.6f}\t{row['speedup']:.2f}x"
        )


if __name__ == "__main__":
    main()