"""Genera cnc_10M.csv: 10M filas CNC sintéticas, deterministas (seed 42), por chunks.

Columnas: ts, makina_id, tenperatura, bibrazioa, presioa, errorea.
NO se versiona (ver .gitignore): se regenera con este script en ~3-5 min.
Uso (venv del proyecto CNC, con numpy):
  ../../01_Erronka1_CNC_Guard/proyecto_cnc_guard/.venv/bin/python generar_cnc_10M.py [--n 10000000]
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT_DEFAULT = HERE / "cnc_10M.csv"
HEADER = "ts,makina_id,tenperatura,bibrazioa,presioa,errorea\n"
MAKINAK = np.array(["M1", "M2", "M3", "M4", "M5"])
OFFSET = np.array([0.0, 1.5, -1.0, 2.5, -2.0])  # deriva por máquina


def chunk_to_lines(rng: np.random.Generator, n: int, t0: int) -> list[str]:
    midx = rng.integers(0, 5, size=n)
    drift = rng.normal(0, 0.4, size=n)
    temp = 65.0 + OFFSET[midx] + drift + rng.normal(0, 4.0, size=n)
    vib = 3.0 + 0.06 * (temp - 65.0) + rng.normal(0, 0.8, size=n)
    pres = 1012.0 - 0.05 * (temp - 65.0) + rng.normal(0, 1.5, size=n)
    # Fallo ~5%: umbral físico + 1% aleatorio (desgaste)
    err = ((temp > 76.0) & (vib > 4.2)) | (rng.random(n) < 0.01)
    ts = t0 + np.arange(n) * 30  # 30 s entre medidas
    out = []
    for i in range(n):
        out.append(
            f"{ts[i]},{MAKINAK[midx[i]]},{temp[i]:.2f},{vib[i]:.2f},{pres[i]:.2f},{int(err[i])}\n"
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10_000_000)
    ap.add_argument("--chunk", type=int, default=1_000_000)
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    args = ap.parse_args()
    rng = np.random.default_rng(42)
    out = Path(args.out)
    t0 = 1700000000
    total = 0
    t_start = time.time()
    with out.open("w", encoding="utf-8") as fh:
        fh.write(HEADER)
        while total < args.n:
            n = min(args.chunk, args.n - total)
            for line in chunk_to_lines(rng, n, t0 + total * 30):
                fh.write(line)
            total += n
            dt = time.time() - t_start
            print(f"  {total}/{args.n} filas ({total / dt:,.0f} filas/s)", flush=True)
    dt = time.time() - t_start
    mb = out.stat().st_size / 1e6
    print(f"OK: {out} total={total} ({mb:.0f} MB en {dt:.0f}s)")


if __name__ == "__main__":
    sys.exit(main())
