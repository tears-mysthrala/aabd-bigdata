# 04 — data/: cnc_10M.csv (10M filas, pruebas reales)

- `generar_cnc_10M.py`: genera 10M filas deterministas (seed 42) por chunks de 1M —
  `ts,makina_id,tenperatura,bibrazioa,presioa,errorea` (~350 MB, ~30 s).
- `test_estabilidad_10M.py`: conteo exacto + agregados por chunks + SGD incremental
  (`partial_fit`, chunks 0–7), umbral calibrado en chunk 8 y holdout en chunk 9.
- El CSV **no se versiona** (`.gitignore`): se regenera con el script.

Resultado 2026-09-22 (6 GB RAM, sin cargar el CSV entero):
`conteo=10000000 err_rate=0.0118` → `SGD 10M: umbral=0.05 acc=0.9861 F1=0.2036`.

Lección (con números): lineal crudo F1=0 → `balanced` hunde accuracy (0.57) →
solo-umbral F1=0.07 → **+feature engineering (interacción temp×vib) F1=0.20**.
El 85% de fallos es ruido puro (1% aleatorio): techo de F1 limitado por los datos.
