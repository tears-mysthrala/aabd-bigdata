"""Fetch UCI WDBC and make a one-predictor Orange table for logistic regression."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
import csv

HERE = Path(__file__).resolve().parent
URL = "https://archive.ics.uci.edu/static/public/17/breast+cancer+wisconsin+diagnostic.zip"
RAW = HERE / "wdbc.data"
NAMES = HERE / "wdbc.names"
TAB = HERE / "wdbc_texture_mean.tab"

FEATURES = [
    "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
    "compactness_mean", "concavity_mean", "concave_points_mean", "symmetry_mean", "fractal_dimension_mean",
    "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se",
    "compactness_se", "concavity_se", "concave_points_se", "symmetry_se", "fractal_dimension_se",
    "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
    "compactness_worst", "concavity_worst", "concave_points_worst", "symmetry_worst", "fractal_dimension_worst",
]


def fetch_source() -> None:
    if RAW.exists() and NAMES.exists():
        return
    with urlopen(URL, timeout=60) as response:
        archive = ZipFile(BytesIO(response.read()))
    RAW.write_bytes(archive.read("wdbc.data"))
    NAMES.write_bytes(archive.read("wdbc.names"))


def main() -> None:
    fetch_source()
    rows = []
    with RAW.open(encoding="utf-8", newline="") as stream:
        for record in csv.reader(stream):
            if len(record) != 32:
                raise ValueError(f"Unexpected UCI row with {len(record)} columns")
            sample_id, diagnosis, *features = record
            rows.append((sample_id, diagnosis, features))
    if len(rows) != 569 or sum(row[1] == "M" for row in rows) != 212 or sum(row[1] == "B" for row in rows) != 357:
        raise ValueError("Unexpected UCI WDBC row or class counts")

    with TAB.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["sample_id", "texture_mean", "diagnosis"])
        writer.writerow(["string", "continuous", "discrete"])
        writer.writerow(["meta", "", "class"])
        for sample_id, diagnosis, features in rows:
            writer.writerow([sample_id, features[1], diagnosis])
    print(f"Prepared {TAB}: 569 samples; benign=357, malignant=212; predictor=texture_mean")
    print(f"Original source files: {RAW}, {NAMES}")


if __name__ == "__main__":
    main()
