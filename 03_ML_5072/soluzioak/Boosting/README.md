# Boosting — material de Moodle del 8 de octubre

Enunciados: [PDF principal](../../materialak/5072_2_07_Boosting.pdf), diapositivas 10–11, y [explicación paso a paso](<../../materialak/Boosting Ereduak_ Adaboost, Gradient Boost eta XGBoost.pdf>). No añaden una tarea de entrega con rúbrica propia: son cuatro ejemplos Python y tres ejemplos manuales que se desarrollan aquí.

[Script](boosting.py) y [notebook ejecutado](boosting.ipynb) reproducen las entradas, semillas y parámetros docentes. El PDF original se conserva. La extensión de evaluación se identifica expresamente para no confundirla con el ejemplo literal.

## Preparar y ejecutar

Desde la raíz del repositorio:

```bash
cd 03_ML_5072/soluzioak/Boosting
uv sync --frozen
uv run --frozen python boosting.py
uv run --frozen pytest -q
uv run --frozen --group security pip-audit
```

Python 3.13, entorno propio y `uv.lock`; se instala `xgboost-cpu` para limitar tamaño y evitar paquetes CUDA innecesarios, según la [guía oficial](https://xgboost.readthedocs.io/en/stable/install.html). El módulo se importa como `xgboost`. Los datasets Iris/diabetes y generadores se incluyen en sklearn, sin descarga externa. Semillas fijas, dos hilos XGBoost; esos ajustes de recursos/reproducibilidad están añadidos respecto al constructor por defecto del PDF.

Para Jupyter, seleccionar el kernel `.venv/bin/python`, abrir el cuaderno desde esta carpeta y ejecutar todas las celdas. El script funciona también desde otro directorio; el notebook comprueba su carpeta antes de escribir. Se sobrescriben solo `resultados/emaitzak.json` y `resultados/boosting.png`. La instalación y auditoría consultan registros externos; el ejercicio no llama APIs ni abre servicios.

## Los ejemplos y su razonamiento

### AdaBoost manual

Cuatro puntos `x=1,2,3,4`, etiquetas `+1,+1,−1,+1`, pesos iniciales 1/4. El stump que separa en 2,5 comete error 1/4; alpha=ln(3)/2≈0,5493. Tras multiplicar por exp(−alpha·y·h) y normalizar, los pesos son **1/6,1/6,1/6,1/2**, no tres 0,17 exactos.

La segunda regla propuesta en el PDF tiene error 1/3; alpha=ln(2)/2≈0,3466. El voto combinado clasifica `+1,+1,−1,−1`: **P4 todavía falla**. No prometemos que dos stumps resuelvan todos los puntos ni que añadir árboles lleve siempre a error cero. Las reglas se reproducen como se han elegido en el documento; no se afirma que sean los stumps óptimos entrenados. La versión sklearn usa SAMME: sus pesos de voto no se comparan numéricamente sin ajustar la convención al cálculo binario manual.

### Gradient Boosting manual

Los precios de ejemplo son `30,32,48,50`; son valores construidos, no un dataset inmobiliario. F0=40 y residuos `−10,−8,+8,+10`. El primer stump tiene hojas ±9. Con learning_rate=0,5: F1=`35,5,35,5,44,5,44,5`. La siguiente ronda tiene hojas ±4,5: F2=`33,25,33,25,46,75,46,75`.

MSE de entrenamiento: **82 → 21,25 → 6,0625**. No es test. Ajustar residuos equivale a usar gradientes negativos para pérdida cuadrática; otras pérdidas requieren su propio gradiente. La tasa pequeña reduce cada actualización, pero no garantiza evitar sobreajuste por sí sola.

### XGBoost manual y biblioteca

Con los mismos cuatro precios, lambda=1 reduce los outputs de las hojas a ±6; eta=0,3 produce F1=`38,2,38,2,41,8,41,8`. La mejora de score del PDF es 216 para el corte 2,5 y 75 para 1,5/3,5. El árbol hist real separa con umbral 3, que representa la misma partición de estas cuatro observaciones que cortar en 2,5.

Hay que especificar **la escala de la fórmula**: la [derivación oficial](https://xgboost.readthedocs.io/en/latest/tutorials/model.html) para el objetivo con factor 1/2 da mejora 108 antes de restar gamma. El dump de la biblioteca instalada registra `gain=216`. Por eso no trasladamos una cifra de gamma entre fórmulas con factores distintos sin verificarla. La prueba ejecutada confirma directamente que gamma=100 conserva el corte y gamma=250 lo elimina en esa biblioteca; las predicciones pasan de 38,2/41,8 a cuatro 40. Lambda penaliza el peso de las hojas; gamma exige mejora para añadir una partición; eta escala su contribución.

### Cuatro ejemplos Python del PDF principal

| Ejemplo | Datos y split | Resultado observado | Interpretación |
|---|---|---|---|
| AdaBoost con stump y 50 estimadores | make_classification, 1000×20, seed 42; 800/200 | accuracy test 0,875; baseline 0,465 | Comparación en esa división sintética. |
| GradientBoostingRegressor | make_regression seed 0; 75/25 | R² test 0,4413; baseline −0,0483 | R² no es porcentaje de aciertos. MAE 83,0032 en las unidades generadas. |
| XGBClassifier | Iris, 120/30, split seed 42 sin estratificar como el PDF | accuracy test 1,0 | Son solo 30 flores; no garantiza resultado perfecto fuera de esa división. |
| XGBRegressor hist con métrica MAE | diabetes, 442 filas; eval_set también entrenamiento | MAE train 0,2335; R² train 0,99998 | Es ajuste sobre los datos vistos, sin test. No demuestra utilidad predictiva ni clínica. |

## Extensión: evaluación diabetes fuera de muestra

División 353/89 filas con seed 42. Los tres modelos usan exactamente los mismos índices. Se fijan los parámetros antes de evaluar y no se usa el test para early stopping ni búsqueda de hiperparámetros. DummyRegressor aprende la media **solo de train**.

| Modelo | MAE test | R² test |
|---|---:|---:|
| Media de train | 64,0065 | −0,0120 |
| Gradient Boosting | 44,5296 | 0,4550 |
| XGBoost | 46,0148 | 0,3768 |

En esta división Gradient Boosting mejora a XGBoost; no se fuerza una conclusión de superioridad de la biblioteca. El rendimiento casi perfecto de entrenamiento no se conserva en test. La incertidumbre de una sola división y el tamaño del dataset limitan la interpretación.

## Comparación y límites

AdaBoost cambia pesos de muestras; Gradient Boosting ajusta gradientes negativos; XGBoost usa gradientes/Hessianos, regularización y algoritmos de árboles optimizados. Los tres construyen etapas sucesivas: el paralelismo de XGBoost dentro del cálculo de árboles no convierte las etapas de boosting en entrenamiento independiente como bagging.

Los estimadores AdaBoost/GradientBoosting clásicos usados aquí requieren imputación si hay NaN; XGBoost soporta direcciones para valores faltantes. Eso no se generaliza a todo estimador que contenga “boosting” en el nombre. La robustez ante outliers y desbalance depende de la pérdida, datos y configuración: la tabla del PDF no garantiza robustez universal. En datos desbalanceados hay que justificar métricas por clase, no confiar solo en accuracy.

[Evidencia notebook](EJECUCION.json), [resultados y versiones](resultados/emaitzak.json), [gráfico](resultados/boosting.png) y [auditoría](AUDITORIA_DEPENDENCIAS.json). Script y notebook ejecutados por separado, tres pruebas conceptuales pasadas, sin vulnerabilidades conocidas detectadas por pip-audit. Los asserts verifican pesos/residuos/pruning concretos, no toda decisión posible ni una entrega Moodle.
