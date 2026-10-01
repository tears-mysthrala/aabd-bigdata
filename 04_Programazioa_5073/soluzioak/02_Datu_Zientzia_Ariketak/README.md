# Cuaderno 2: NumPy, Pandas y gráficos

Son las soluciones de los 25 ejercicios del
[cuaderno de datos](../../materialak/notebooks/5073_2_Datu_Zientzia_Ariketak.ipynb).
La [solución Jupyter](5073_2_Datu_Zientzia_Ariketak.ipynb) y su
[script comentado](5073_2_Datu_Zientzia_Ariketak.py) incluyen el enunciado,
la explicación y las comprobaciones de cada paso.

## Preparación y ejecución

Python 3 y `uv`; dependencias: NumPy, Pandas, Matplotlib y Seaborn. Desde la raíz:

```bash
cd 04_Programazioa_5073/soluzioak/02_Datu_Zientzia_Ariketak
uv venv .venv
uv pip install --python .venv/bin/python numpy pandas matplotlib seaborn
.venv/bin/python 5073_2_Datu_Zientzia_Ariketak.py
```

Estos paquetes se instalan en un entorno local; este bloque no tiene un lock
propio que fije versiones. Para leer/ejecutar el notebook usa el mismo entorno
en tu editor Jupyter. Ejecuta de arriba abajo: las máscaras reutilizan arrays
anteriores y los gráficos usan el DataFrame ya limpiado. En un terminal sin
pantalla puedes anteponer `MPLBACKEND=Agg` al comando; comprobará las celdas,
pero no abrirá ventanas con los gráficos.

## Datos y resultados

El setup **sobrescribe** `data/cnc_mock.csv` con 100 filas sintéticas y seed 42.
No representa telemetría real. Columnas: `makina_id` (M1/M2/M3),
`tenperatura`, `bibrazioa` y `errorea` (0/1). Se introducen dos NaN y dos valores
extremos: temperatura 999 y vibración −50. La limpieza posterior modifica
`df_clean` en memoria, **no guarda un CSV limpio**. Los cuatro gráficos se
muestran con `plt.show()`; el script no los exporta a PNG.

| Ejercicios | Método y razón | Resultado que debes comprobar |
|---|---|---|
| 1.1–1.5 | Arrays, ceros, máximo, multiplicación vectorial y reshape. `reshape` conserva el número de elementos. | 1–10; matriz 3×3 de ceros; máximo de 10 valores; dobles; 12 valores en 3×4. |
| 2.1–2.5 | Máscaras booleanas; combinar condiciones con `&` y paréntesis. 2.3 modifica `arr6` para los pasos siguientes. | Pares 2–10; valores 16–20; cuatro ceros; intervalo 10–15; **9 múltiplos de 3**, contando los cuatro ceros. |
| 3.1–3.5 | Cargar CSV, inspeccionar filas/columnas, distinguir valores únicos y frecuencias. | Forma 100×4; 5 primeras filas; tres máquinas; conteo de `errorea=1`. |
| 4.1–4.5 | Detectar NaN; eliminar dos filas; sustituir temperatura >150 por mediana y vibración negativa por 0; convertir etiqueta a bool. | 98 filas sin NaN, temperatura máxima <150, vibración mínima ≥0 y `errorea` booleano. |
| 5.1–5.5 | Histograma (distribución), scatter (relación), boxplot (grupos) y heatmap (correlaciones). | Cuatro objetos de ejes; inspección visual para verificar variables y sentido de cada gráfico. |

Las reglas de limpieza son decisiones de este ejemplo, no reglas universales
para una fábrica. El heatmap selecciona columnas numéricas: tras convertir
`errorea` a booleano, esa etiqueta queda fuera. Correlación no demuestra
causalidad. Los asserts sobre los ejes solo prueban que existen, no que el
gráfico esté bien interpretado.

## Para estudiar

Explica por qué `arr6` ya no tiene los valores 1–4 y por qué `0 % 3 == 0`.
Compara qué información se pierde al borrar filas frente a imputarlas.
Comprueba los ejes de cada gráfico y escribe una observación apoyada en él.
[Registro de ejecución anterior](../egiaztapena_2026-09-28.md).
