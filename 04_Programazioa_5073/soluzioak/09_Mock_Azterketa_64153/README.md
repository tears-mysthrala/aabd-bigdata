# Mock de preparación del examen · Moodle 64153

[Guía original](../../materialak/Moodle_page_64153.md), preservada sin cambios.
Incluye cinco preguntas de autoevaluación y el checklist práctico. La guía
describe un examen de 30 preguntas (3 puntos) y una práctica Jupyter (7 puntos),
pero **no proporciona esas 30 preguntas ni un CSV específico**. La penalización
del test no se cuantifica: no se inventa una fórmula de nota.

Las respuestas justificadas son **C, B, B, C, B**, en el
[notebook resuelto](mock_azterketa.ipynb) y [script equivalente](mock_azterketa.py).
Incluyen por qué los distractores no corresponden y los límites de cada respuesta.

Para entrenar la práctica, empieza por el [enunciado propio](ENUNCIADO_PRACTICA.md)
y consulta después la solución. Cubre las seis habilidades: list comprehension,
limpieza Pandas, Pipeline, desbalance, interpretación de métricas y Pydantic.
Usa el [CSV ya versionado](../../data/cnc_mock.csv), un mock sintético previo,
sin modificarlo; no se presenta como dataset oficial específico del examen.

## Preparar y ejecutar

Desde la raíz del repositorio:

```bash
cd 04_Programazioa_5073/soluzioak/09_Mock_Azterketa_64153
uv sync --frozen
MPLBACKEND=Agg uv run --frozen python mock_azterketa.py
uv run --frozen pytest -q
uv run --frozen --group security pip-audit
```

Python 3.13, entorno aislado, [lock](uv.lock). En Jupyter selecciona
`.venv/bin/python`, abre el cuaderno desde esta carpeta y ejecuta todas las celdas.
La instalación/auditoría necesita acceso a registros; prepara el entorno antes
de estudiar offline. La solución no descarga datos, abre servicios, carga pickle
ni cambia fuentes. Sobrescribe solo `resultados/`: CSV limpios/descartes,
predicciones, JSON de validación y gráfico de confusión.

## Resultado e interpretación

De 100 registros, se conservan **96**: se descartan dos con NaN, uno con 999 °C
y otro con vibración −50. Hay 91 negativos y solo cinco positivos. M1/M2/M3 se
repiten: se reserva una máquina completa para no compartir máquina entre train
y test. Quedan **56 train y 40 test**, con escalado aprendido solo en train.

En la ejecución registrada: **TN=26, FP=11, FN=2, TP=1**, accuracy 0.675,
recall 1/3 y precisión 1/12. El clasificador siempre-cero alcanza accuracy 0.925,
pero recall cero. El modelo detecta un error de tres y produce once falsas
alertas: es un resultado débil y no justifica decisiones de mantenimiento.
Una prueba verde verifica cálculos y separación, no que el modelo sea útil.

[Métricas y procedencia](resultados/validacion.json),
[predicciones de test](resultados/test_predictions.csv),
[matriz](resultados/confusion.png), [ejecución](EJECUCION.json) y
[auditoría de dependencias](AUDITORIA_DEPENDENCIAS.json).

El número reducido de positivos y de máquinas impide evaluar generalización con
precisión. No cambiamos semillas, umbrales o modelo para mejorar el test. Harían
falta más datos representativos, validación por grupo/tiempo según el despliegue
y análisis de costes. La imputación/eliminación de registros puede introducir
sesgo y debe revisarse con conocimiento del sensor.

El esquema Pydantic bloquea valores imposibles para esta variante. La salida
define P(errorea=1), incluso si la clase predicha es 0. No se ha publicado una API:
la guía pide el esquema, no desplegar un servicio.

La solución es material de preparación. Para practicar las condiciones del
examen, intenta la teoría sin apuntes y la práctica con los PDF de clase, sin
Internet ni asistentes, tal como establece la guía.

Referencias: [class_weight de LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html),
[validadores Pydantic](https://docs.pydantic.dev/latest/concepts/validators/),
[carga al inicio con lifespan en FastAPI](https://fastapi.tiangolo.com/advanced/events/).
