# COMPAS: solución ejecutada y reconciliada

[Notebook ejecutado](COMPAS_reconciliado.ipynb) de la actividad de sesgo histórico, con resultados coherentes con `decile_score >= 7`. El [material original](../../materialak/Alborapenak/2.2_compas_historikoa_soluzioa.ipynb) permanece intacto. La [guía de lectura](../../materialak/Alborapenak/README.md) enlaza ambas versiones.

## Objetivo y población

Comprobar las tasas de error por grupo, reconciliar cifras y umbral, interpretar las tasas por decil y responder las preguntas de discusión sin convertir asociaciones en causas ni estadísticas en conclusiones jurídicas.

Fuente fijada: [CSV de ProPublica en commit c062fbb5fa84f6c99d82f432c46b405f3a0ca5ec](https://raw.githubusercontent.com/propublica/compas-analysis/c062fbb5fa84f6c99d82f432c46b405f3a0ca5ec/compas-scores-two-years.csv). SHA-256: `c451db85908b2f7fef1d83203bedf6b71ecda0d5af468d82ae62178f91d0cc7d`. La copia descargada coincide byte a byte con el CSV preexistente del material; ese material no se modifica ni se copia a la solución.

Hay **7.214 registros de origen**, **6.172** tras los filtros inclusivos de ventana [-30,30], `is_recid != -1`, `c_charge_degree != O`, `score_text != N/A`, y **5.278** tras seleccionar `African-American` (3.175) y `Caucasian` (2.103). Son etiquetas textuales de la fuente, no identidades inferidas. Positivo real: `two_year_recid=1`. Unidad: registro de la fuente, no una cohorte nueva. No se entrena ningún modelo.

El umbral principal es **score >=7**. El contraste **>=5** usa exactamente la misma población y se muestra separado. En esta selección, >=5 equivale a Medium + High (`score_text != Low`), comprobado en código. Los porcentajes aproximados originales (~44/23% FPR, ~28/48% FNR) no corresponden a >=7; cambiar a >=5 tampoco reproduce exactamente todas las cifras históricas de ProPublica. No se reconstruye su análisis de supervivencia ni se fuerza una coincidencia de cohortes.

## Privacidad y archivos

La fuente contiene registros individuales. El programa la descarga únicamente a `~/.cache/aabd-compas/<sha256>.csv`, con directorio 0700 y archivo 0600, **fuera del repositorio**; verifica su hash antes de cargarla. Solo lee las siete columnas necesarias. No imprime filas individuales ni guarda nombres, IDs, fechas personales o predicciones individuales. No añade un nuevo CSV identificable a Git. Los archivos de esta solución contienen únicamente código, metadatos y agregados.

- [compas_reconciliar.py](compas_reconciliar.py): carga verificada, filtros, métricas, intervalos y gráficos.
- [ejecutar_notebook.py](ejecutar_notebook.py): ejecuta con el Python invocado como kernel, sin instalar ni modificar kernels globales.
- [metricas_umbral.csv](resultados/metricas_umbral.csv): cuatro filas agregadas (dos grupos × dos umbrales), recuentos y denominadores.
- [tasas_score.csv](resultados/tasas_score.csv): veinte agregados por grupo/decil con numerador, n y Wilson 95%.
- [proveniencia.json](resultados/proveniencia.json): commit, URL, hash, filtros, tamaños, versiones y hashes de salidas.
- [Comparación por umbral](resultados/tasas_por_umbral.png) y [tasas observadas por decil](resultados/tasas_por_score.png).

## Ejecución desde la raíz del repositorio

En esta máquina se reutilizó el entorno de notebooks existente **sin cambiar sus paquetes**:

```bash
/tmp/aabd-notebooks-20261002-venv/bin/python 02_AA_Ereduak_5071/soluzioak/COMPAS/compas_reconciliar.py
/tmp/aabd-notebooks-20261002-venv/bin/python 02_AA_Ereduak_5071/soluzioak/COMPAS/ejecutar_notebook.py
```

Si ese entorno temporal ya no existe, preparar uno dedicado fuera del checkout:

```bash
uv venv /tmp/aabd-compas-venv --python 3.13
uv pip install --python /tmp/aabd-compas-venv/bin/python -r 02_AA_Ereduak_5071/soluzioak/COMPAS/requirements.txt
/tmp/aabd-compas-venv/bin/python 02_AA_Ereduak_5071/soluzioak/COMPAS/ejecutar_notebook.py
```

La primera ejecución requiere HTTPS si falta la caché privada; las siguientes usan el mismo archivo local fijado. Los agregados y gráficos se sobrescriben, y el notebook guarda sus outputs para abrirlo sin acceso a la fuente individual. Para revisar una exportación local:

```bash
/tmp/aabd-notebooks-20261002-venv/bin/python -m jupyter nbconvert --to html --output-dir /tmp/compas-qa 02_AA_Ereduak_5071/soluzioak/COMPAS/COMPAS_reconciliado.ipynb
```

Versiones verificadas: Python 3.13.13, NumPy 2.5.3, Pandas 3.0.6, Matplotlib 3.11.2, nbformat 5.11.1, nbclient 0.11.0, ipykernel 7.4.0, nbconvert 7.17.1. [requirements.txt](requirements.txt) fija estos paquetes. La nota de transporte local TCP que emite ipykernel no impidió la ejecución; el runner no abre un servicio remoto.

## Resultados y denominadores

| Umbral | Grupo | n | TN | FP | FN | TP | Base rate | FPR | FNR | TPR |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| >=7 | African-American | 3175 | 1169 | 345 | 818 | 843 | 52,31% | 22,79% | 49,25% | 50,75% |
| >=7 | Caucasian | 2103 | 1175 | 106 | 592 | 230 | 39,09% | 8,27% | 72,02% | 27,98% |
| >=5 | African-American | 3175 | 873 | 641 | 473 | 1188 | 52,31% | 42,34% | 28,48% | 71,52% |
| >=5 | Caucasian | 2103 | 999 | 282 | 408 | 414 | 39,09% | 22,01% | 49,64% | 50,36% |

FPR=FP/(FP+TN), FNR=FN/(FN+TP), TPR=TP/(TP+FN), base rate=(TP+FN)/n. El CSV añade PPV=TP/(TP+FP) y accuracy=(TN+TP)/n. Los negativos reales son 1.514/1.281 y los positivos 1.661/822; los denominadores se conservan explícitos.

Con umbral 7 el ratio descriptivo de FPR es 2,75 y la diferencia 14,51 puntos porcentuales. Esto es una diferencia de errores frente a la etiqueta histórica; no identifica un mecanismo causal ni un estándar universal de equidad.

## Validación y límites

El notebook se ejecutó de principio a fin mediante nbclient y se validó con nbformat. Recuenta las matrices con `crosstab` de forma independiente, comprueba sus denominadores y veinte agregados por decil, y verifica que bajar el umbral aumenta FPR y reduce FNR sin cambiar las tasas base. La ejecución repetida produjo los mismos hashes de CSV, figuras y metadatos. Las imágenes guardadas y la presentación HTML se inspeccionaron visualmente; tablas y outputs están presentes, sin filas individuales.

Los deciles son ordinales: `score/10` no es una probabilidad de reincidencia. El gráfico muestra **tasas observadas**, con tamaños e intervalos Wilson binomiales 95%; el parecido de curvas o solapamiento de intervalos no prueba calibración probabilística, igualdad o equivalencia estadística. Los intervalos no corrigen sesgos de selección o del proceso de registro.

No se investiga causalidad, validez de todas las etiquetas, equidad en otros grupos, utilidad judicial, reglas de decisión reales ni legalidad en la UE. Las respuestas del notebook plantean criterios de discusión y límites: no repiten como conclusiones verificadas las afirmaciones causales, multas o autorizaciones jurídicas del original. No se ha reproducido el análisis histórico completo de ProPublica ni la defensa de Northpointe. Los cambios permanecen locales, sin commit ni publicación.
