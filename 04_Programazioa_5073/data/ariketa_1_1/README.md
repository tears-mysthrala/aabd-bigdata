# Ariketa 1.1

Python-en `range` baten batura eskuzko `for` begiztarekin eta NumPy-ren
`np.sum` erabiliz neurtzen da, `N = 1_000_000`, `10_000_000` eta `50_000_000`
balioetarako.

## Exekuzioa

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install numpy
python benchmark.py
```

Emaitzak `emaitzak.csv` fitxategian ere gordetzen dira.

## Emaitzak

| N | Python (s) | NumPy (s) | NumPy-ren abiadura |
|---:|---:|---:|---:|
| 1.000.000 | 0,042304 | 0,000653 | 64,75x |
| 10.000.000 | 0,424848 | 0,005899 | 72,02x |
| 50.000.000 | 2,138076 | 0,025327 | 84,42x |

`speedup` kalkulua hau da: `Python denbora / NumPy denbora`. Beraz, hiru
kasuetan NumPy nabarmen azkarragoa da. NumPy-ren eragiketa C-n konpilatutako
kode bektorialean egiten da; Python-eko bertsioak, aldiz, elementu bakoitzeko
begizta eta Python objektuen kudeaketa ditu. `N` handitzean, Python-en begizta
horren kostu lineala gehiago pilatzen da, eta NumPy-k memoria jarraituan eta
barneko optimizazio bektorialetan duen abantaila agerikoagoa bihurtzen da.

Neurketa baturaren eragiketari dagokio: `np.arange` bidezko array-aren sorrera
ez da `numpy_s` denboran sartu.