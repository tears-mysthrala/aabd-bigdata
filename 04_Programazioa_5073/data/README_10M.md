# 04 — data/: cnc_10M.csv (10M filas, pruebas reales)

- `generar_cnc_10M.py`: genera 10M filas sintéticas deterministas (seed 42)
  por chunks de 1M y escribe cada línea sin construir una lista de 1M
  cadenas en memoria. Columnas: `ts,makina_id,tenperatura,bibrazioa,presioa,errorea`.
  Mantener `--chunk=1000000` al reproducir métricas históricas: cambiar el
  tamaño de chunk altera el orden de llamadas al generador aleatorio, aunque
  la seed siga siendo 42.
- `test_estabilidad_10M.py`: conteo exacto + agregados por chunks + SGD incremental
  (`partial_fit`, chunks 0–7), umbral calibrado en chunk 8 y holdout en chunk 9.
- El CSV **no se versiona** (`.gitignore`): se regenera con el script.

Resultado 2026-09-22 (6 GB RAM, sin cargar el CSV entero):
`conteo=10000000 err_rate=0.0118` → `SGD 10M: umbral=0.05 acc=0.9861 F1=0.2036`.

Lección (con números): lineal crudo F1=0 → `balanced` hunde accuracy (0.57) →
solo-umbral F1=0.07 → **+feature engineering (interacción temp×vib) F1=0.20**.
El generador añade una condición de error aleatoria del 1 % a la regla
física; por ello hay falsos negativos inevitables para un modelo que solo
observa las variables de esta tabla. El porcentaje exacto y el F1 dependen
de la muestra y del umbral; este experimento no prueba capacidad predictiva
sobre maquinaria industrial.
