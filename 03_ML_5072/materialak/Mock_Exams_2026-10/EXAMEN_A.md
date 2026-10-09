# Simulacro A — 5072 — Machine Learning

Elaboración propia, 9 de octubre de 2026. Basado en la materia local disponible;
no es un examen oficial ni una predicción de preguntas del profesorado.
Duración propuesta: **120 minutos**. Nota máxima: **10 puntos**.
Los tiempos, reparto de puntos y condiciones son de autoestudio, salvo el formato
3 + 7 de Programación documentado en su guía docente.

## Condiciones y entrega

Resuelve primero sin abrir la [solución y rúbrica](../../soluzioak/Mock_Exams_2026-10/SOLUCIONES_A.md).
Teoría sin apuntes; práctica con copias locales de los apuntes, sin Internet ni IA.
Calculadora básica permitida en cálculos. Entrega respuestas razonadas y, donde
se pida código, notebook o script con salidas y explicación. No basta nombrar una
herramienta: justifica su elección. Los casos y números nuevos son sintéticos.
No necesitas levantar servicios para los apartados de diseño o traza.

## Materia de referencia

- [5072_1_Datua_eta_Aurreprozesamenua.pdf](<../5072_1_Datua_eta_Aurreprozesamenua.pdf>)
- [5072_2_02_Erregresio_Logistikoa.pdf](<../5072_2_02_Erregresio_Logistikoa.pdf>)
- [5072_2_03_KNN.pdf](<../5072_2_03_KNN.pdf>)
- [5072_2_05_SVM.pdf](<../5072_2_05_SVM.pdf>)
- [5072_2_06_Random_Forest.pdf](<../5072_2_06_Random_Forest.pdf>)
- [5072_2_07_Boosting.pdf](<../5072_2_07_Boosting.pdf>)
- [5072_2_Ikasketa_Gainbegiratua.pdf](<../5072_2_Ikasketa_Gainbegiratua.pdf>)
- [5072_3_Balidazio_Metodologia.pdf](<../5072_3_Balidazio_Metodologia.pdf>)
- [5073_3_Programazioa.pdf](<../../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>)

Correspondencia de cada apartado con páginas y ejercicios docentes:
[matriz de cobertura](../../../00_Transversal/MOCK_EXAMS_2026-10/COBERTURA.md#ml).

## 1. Datos y validación (2 puntos; 20 min)

Se predice fallo a partir de temperatura, vibración, tipo de máquina y registros
repetidos por máquina. «fecha_reparación» se conoce después del fallo.
Propón tratamiento de nulos y categorías, distinguiendo nominal/ordinal (0.5),
features y fuga de información (0.5), split para máquinas nuevas frente a
futuro de las mismas máquinas (0.5) y ubicación de imputación/escalado/selección
de hiperparámetros dentro de la validación (0.5).

## 2. Regresión y modelos (2 puntos; 25 min)

(a) Para y=[2,4,6], pred=[3,3,6], calcula MAE, MSE y R² usando la media de y
como referencia (0.75). (b) Compara regresión lineal y logística: salida,
objetivo y regularización Ridge/Lasso (0.5). (c) Explica efecto de k pequeño en
KNN, de C grande en SVM y de max_depth sin límite en árbol (0.75).

## 3. Clasificación y decisión (2 puntos; 20 min)

En test: TN=180, FP=10, FN=6, TP=4. Calcula accuracy, precisión, recall y F1
para fallo=1 (1). Compara con predecir siempre 0 y justifica métrica relevante
(0.5). Explica ROC-AUC frente a F1 y dónde elegir umbral; distingue macro y
weighted en un problema multiclase (0.5).

## 4. Ensambles y lectura crítica (1.5 puntos; 15 min)

Compara bagging/Random Forest con boosting (0.5); distingue AdaBoost,
Gradient Boosting y XGBoost al nivel conceptual del material (0.5). CV ficticia:
árbol train=1.00/val=0.70; forest 0.98/0.86; boosting 0.97/0.85. Diagnostica el
árbol y elige candidato sin afirmar significación de una diferencia de 0.01 (0.5).

## 5. Práctica reproducible — Iris (2.5 puntos; 40 min)

Usa Iris incluido en sklearn, sin descargar. Objetivo: clasificación con las
cuatro features; visualización adicional con las dos primeras, claramente separada.
Con semilla 42, test_size=0.30 y stratify=y, compara dos pipelines:
StandardScaler+LogisticRegression(max_iter=1000) y StandardScaler+KNN.
Selecciona k∈{3,5,7} mediante CV estratificada de 5 folds solo en train,
scoring='accuracy'. Entrega: (a) carga/split y comprobación de tamaños (0.5),
(b) pipelines y selección sin test (0.75), (c) confusion matrix y accuracy de
ambos en test, indicando orden de clases (0.5), (d) gráfico de límites 2D con
modelos ajustados solo en train y explicación lineal/local (0.5), (e) conclusión
sin inventar una accuracy esperada ni confundir gráfico con prueba de generalización (0.25).
