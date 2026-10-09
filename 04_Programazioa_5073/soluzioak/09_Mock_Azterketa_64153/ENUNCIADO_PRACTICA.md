# Práctica propia basada en el checklist del examen

Fuente: [guía docente, Moodle 64153](../../materialak/Moodle_page_64153.md).
Este enunciado contextualiza sus seis habilidades con un CSV existente; **no es
un examen oficial adicional** ni anticipa el contexto que se entregará en clase.

Una persona responsable de mantenimiento quiere explorar la detección de errores
a partir de temperatura y vibración. Usa `../../data/cnc_mock.csv`, un mock previo
de 100 filas. `errorea=1` indica error; `makina_id` identifica la máquina y puede
repetirse. No descargues datos, no modifiques el original ni cargues modelos ajenos.

1. Normaliza nombres de columnas mediante una **list comprehension**. Inspecciona
   dimensiones, tipos, nulos, rangos y frecuencia de las clases antes de modelar.
2. Limpia exclusivamente con **Pandas**, sin transformers de sklearn: conserva
   registros con temperatura finita de 0–150 °C y vibración finita no negativa;
   elimina registros con características ausentes. Estas son reglas explícitas
   del ejercicio, no umbrales industriales generales. Conserva los descartes y
   explica la pérdida de datos. No imputes etiquetas ni conviertas el ID en feature.
3. Reserva una de las tres máquinas para test con semilla 42, entrenando con las
   otras dos. Comprueba que no comparten máquinas y que hay ambas clases en los
   dos conjuntos. Usa **Pipeline(StandardScaler, LogisticRegression)**: ningún
   fit de escalado debe utilizar test. Justifica este reparto por grupos frente
   a repartir filas de la misma máquina entre train y test.
4. Usa **class_weight='balanced'** y explica su fórmula. Indica por qué no
   equivale a duplicar muestras y por qué no garantiza una mejora. Conserva el
   umbral 0.5; no lo elijas mirando test.
5. Calcula **accuracy, balanced accuracy, recall y precisión** de la clase 1,
   classification_report y matriz de confusión. Explica TN/FP/FN/TP y support.
   Compara con predecir siempre 0. Justifica la importancia de recall y también
   el coste de falsas alarmas. Explica qué impide concluir un dataset tan pequeño.
6. Define un **BaseModel de Pydantic** con temperatura/vibración y
   **@field_validator** para bloquear negativos, NaN e infinitos, y temperaturas
   superiores al rango declarado. Rechaza campos extra. Prueba límites válidos
   e inválidos y predice una entrada válida usando la misma ordenación de features.
   Si devuelves probabilidad, define a qué clase corresponde.

Entrega de autoestudio: notebook narrado, código ejecutable, datos descartados,
predicciones de test, métricas y decisiones justificadas. No hay rúbrica numérica
inventada ni subida automática a Moodle. Inténtalo antes de abrir la solución.
