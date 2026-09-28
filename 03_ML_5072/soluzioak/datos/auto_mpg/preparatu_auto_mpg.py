"""Download UCI Auto MPG and prepare an Orange tab file for mpg ~ weight."""

from __future__ import annotations

from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import shlex


HERE = Path(__file__).resolve().parent
UCI_ZIP = "https://archive.ics.uci.edu/static/public/9/auto+mpg.zip"
RAW_DATA = HERE / "auto-mpg.data"
RAW_NAMES = HERE / "auto-mpg.names"
ORANGE_TAB = HERE / "auto_mpg_weight.tab"


def download_source() -> None:
    if RAW_DATA.exists() and RAW_NAMES.exists():
        return
    with urlopen(UCI_ZIP, timeout=30) as response:
        archive = ZipFile(BytesIO(response.read()))
    RAW_DATA.write_bytes(archive.read("auto-mpg.data"))
    RAW_NAMES.write_bytes(archive.read("auto-mpg.names"))


def prepare() -> int:
    download_source()
    records: list[tuple[str, str, str]] = []
    for line_number, line in enumerate(RAW_DATA.read_text(encoding="ascii").splitlines(), 1):
        fields = shlex.split(line)
        if len(fields) != 9:
            raise ValueError(f"Unexpected UCI row {line_number}: {len(fields)} fields")
        mpg, _cylinders, _displacement, _horsepower, weight, *_rest, car_name = fields
        records.append((mpg, weight, car_name))
    if len(records) != 398:
        raise ValueError(f"Expected 398 rows, got {len(records)}")

    with ORANGE_TAB.open("w", encoding="utf-8", newline="") as output:
        output.write("mpg\tweight\tcar_name\n")
        output.write("continuous\tcontinuous\tstring\n")
        output.write("class\t\tmeta\n")
        for mpg, weight, car_name in records:
            output.write(f"{mpg}\t{weight}\t{car_name}\n")
    return len(records)


if __name__ == "__main__":
    print(f"Prepared {prepare()} UCI Auto MPG rows: {ORANGE_TAB}")
