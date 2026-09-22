# 03_ML_5072 — soluzioak ✅

- `5072_ML_praktika.py` / `.ipynb` (7 gelaxka): EDA + aurreprozesamendua + erregresioa + sailkapena, `cnc_mock.csv`-rekin.
- Exekuzioa: `01_Erronka1_CNC_Guard/proyecto_cnc_guard/.venv/bin/python 5072_ML_praktika.py`
  (edo `uv run --project ../../../01_Erronka1_CNC_Guard/proyecto_cnc_guard` + sklearn).

Datu errealen aurkikuntzak (ez simulatuak):
- 1 NaN `tenperatura`/`bibrazioa`-n → inputazioa beharrezkoa.
- `bibrazioa`↔`tenperatura` korrelazioa ≈ 0.03 → erregresio linealak ez du seinale linealik (MSE sentikorra outlierrekiko: teoria 2.1).
- `errorea` 95/5 desorekatua → F1=0 `balanced` gabe, 0.118 `class_weight='balanced'`-rekin (teoria 1.x klase-desoreka).
