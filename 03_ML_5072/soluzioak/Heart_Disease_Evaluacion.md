# Heart Disease: Árbol de Decisión y Random Forest

Esta resolución común cubre la comparación de **Árbol de Decisión (63544)** y **Random Forest (63386)** con Logistic Regression y k-NN como referencias. Las introducciones Moodle estaban vacías: no se les atribuyen requisitos adicionales. El resultado ejecutado es el script Python, no una ejecución de la interfaz Orange.

## Datos y método

Se conserva una copia exacta del dataset integrado en Orange, [heart_disease.tab](datos/heart_disease/heart_disease.tab), para que su instalación o una descarga futura no cambie la entrada. Tiene 303 registros, 13 predictores, 164 casos de clase `0`, 139 de clase `1` y seis celdas predictoras ausentes. La variable objetivo es `diameter narrowing`; la clase positiva es `1`. No se elimina ningún registro. SHA-256 de entrada: `954e44e3d93a97682b5466c7ea166e16f376f8dd93deef5855f511734e4d6224`.

Se ejecuta **CV estratificada de diez folds**, con `shuffle=True` y semilla `42`. Todos los modelos usan las mismas particiones. Cada registro aporta exactamente una predicción fuera de su entrenamiento por modelo. **La imputación se ajusta dentro de cada training fold**, por los preprocesadores del learner. Continuize codifica las categorías para LR/RF/k-NN; Normalize estandariza las variables continuas para LR/k-NN, también dentro de cada fold. El árbol conserva variables categóricas.

Las métricas se calculan sobre todas las predicciones fuera de fold agrupadas, no promediando métricas por fold. Precision, Recall y F1 son binarios para la clase `1`. CA usa la decisión de clase del modelo; AUC y ROC usan la probabilidad de clase `1`.

- **Decision Tree:** Orange `TreeLearner`, profundidad máxima 5, mínimo 1 caso por hoja, mínimo 2 casos para dividir, `sufficient_majority=0.95`. No se presenta como el algoritmo CART de sklearn.
- **Random Forest:** Orange `RandomForestLearner`, 100 árboles, `max_features='sqrt'`, sin límite de profundidad, `random_state=42`.
- **Logistic Regression:** L2, C=1, máximo 1000 iteraciones, `random_state=42`.
- **k-NN:** k=5, distancia euclídea, pesos uniformes.

El JSON registra hiperparámetros, preprocesadores, versiones y hash del CSV. El archivo `figuras_manifest.json` vincula las cinco imágenes al hash del JSON. El generador PDF rechaza una entrada o figura cuyo hash no coincide, para evitar informes con resultados obsoletos.

## Ejecución desde la raíz del repositorio

Se utilizó el entorno Orange ya existente, sin instalar ni actualizar sus paquetes. ReportLab se carga con `uv run` en un entorno temporal independiente.

```bash
/home/tears/.local/share/uv/tools/orange3/bin/python 03_ML_5072/soluzioak/orange_bihotza_ereduak.py
/home/tears/.local/share/uv/tools/orange3/bin/python 03_ML_5072/soluzioak/irudiak/sortu_irudiak.py
uv run --with reportlab==5.0.1 python 03_ML_5072/soluzioak/sortu_pdf_txostena.py
```

Versiones de la comparación verificada el 2026-10-02: Python 3.13.13, Orange 3.40.0, scikit-learn 1.9.1, NumPy 2.3.5. En otra máquina se necesita un entorno Orange con esas versiones para reproducir los mismos números; los archivos se resuelven respecto al script, independientemente del directorio de ejecución. La ejecución puede emitir avisos de deprecación de `penalty` y `n_jobs` en la integración Orange/sklearn; no hubo fallos de modelos.

## Salidas y resultados verificados

- [Predicciones CV](datos/heart_disease/predicciones_cv.csv): 1212 filas = 303 registros × cuatro modelos, con índice original (desde cero), fold (desde uno), etiqueta real, decisión y probabilidad de clase `1`.
- [Resultados y metadatos](datos/heart_disease/resultados_cv.json): métricas, matrices, coordenadas ROC, versiones, reglas del árbol ilustrativo y hashes.
- [Manifest de figuras](datos/heart_disease/figuras_manifest.json) y cinco PNG en [irudiak](irudiak/): flujo, comparación, matrices de los cuatro modelos, ROC empíricas y árbol real.
- [Informe PDF](Orange_Data_Mining_Entregagarria.pdf): cinco páginas, regenerado desde esos artefactos.

| Modelo | AUC | CA | F1 | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.9055 | 0.8317 | 0.8104 | 0.8385 | 0.7842 |
| Random Forest | 0.9009 | 0.8119 | 0.7897 | 0.8106 | 0.7698 |
| Decision Tree | 0.7993 | 0.7822 | 0.7574 | 0.7744 | 0.7410 |
| k-NN (k=5) | 0.8629 | 0.8185 | 0.8000 | 0.8088 | 0.7914 |

**Árbol de Decisión:** matriz `[[134,30],[36,103]]` (filas reales, columnas predichas): 36 FN y 30 FP. Sus reglas son interpretables, pero no se demuestra calibración ni utilidad clínica.

**Random Forest:** matriz `[[139,25],[32,107]]`: 32 FN y 25 FP. En esta ejecución mejora el AUC del árbol, pero la diferencia no prueba significación estadística ni superioridad en pacientes nuevos.

Las anteriores métricas literales, ROC analíticas y reglas dibujadas a mano se han sustituido. Las ROC actuales son escalones calculados con `roc_curve` a partir del CSV, sin selección de un umbral supuestamente óptimo. El árbol mostrado es un modelo real de profundidad 3 entrenado sobre todos los datos, claramente separado de la evaluación CV del árbol de profundidad 5. Sus recuentos son de entrenamiento, no resultados CV ni probabilidades clínicas.

## Verificación y límites

Se ejecutó dos veces la comparación: tanto el CSV como el JSON tuvieron SHA-256 idénticos. Una comprobación independiente recalculó las cinco métricas y matrices desde el CSV, comprobó sus 1212 filas, cada índice y etiqueta contra el dataset, cobertura de los diez folds y asignación compartida por los cuatro modelos. El generador de figuras vuelve a comprobar las matrices y el AUC del CSV. Se renderizaron e inspeccionaron visualmente las cinco páginas del PDF y sus cinco figuras.

[Orange_Bihotza_Ereduak.ows](Orange_Bihotza_Ereduak.ows) se conserva como material GUI **no ejecutado en esta validación**. Tiene parámetros diferentes (RF/Tree y ajustes de Test & Score): no se afirma que sus resultados coincidan con el script. La evidencia de cierre de la comparación Python es el CSV/JSON/PDF producido.

No hay cohorte externa de test, nested CV, selección de hiperparámetros, intervalos de incertidumbre, comparación estadística, calibración ni evaluación de equidad. Tampoco se han calculado importancias de características comunes a los modelos. Es una práctica académica sobre el dataset de Orange, no una herramienta de diagnóstico clínico. Los cambios permanecen locales, sin commit ni publicación.
