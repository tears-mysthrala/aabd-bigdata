# Simulacro A — 5073 — Programación para IA

Elaboración propia, 9 de octubre de 2026. Basado en la materia local disponible;
no es un examen oficial ni una predicción de preguntas del profesorado.
Duración propuesta: **150 minutos**. Nota máxima: **10 puntos**.
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

- [Moodle_page_64153.md](../Moodle_page_64153.md)
- [5073_1_Lengoaiak.pdf](../5073_1_Lengoaiak.pdf)
- [5073_2_Datu_Zientzia.pdf](../5073_2_Datu_Zientzia.pdf)
- [5073_3_Programazioa.pdf](../5073_3_Programazioa.pdf)
- [1_Ariketa_koadernoa_URLa.ipynb](../1_Ariketa_koadernoa_URLa.ipynb)
- [2_Ariketa_Koadernoa_URLa.ipynb](../2_Ariketa_Koadernoa_URLa.ipynb)
- [3_Ariketa_koadernoa_URLa.ipynb](../3_Ariketa_koadernoa_URLa.ipynb)

## Parte teórica (3 puntos; 35 min)

30 preguntas, una respuesta correcta, cuatro opciones. Sin apuntes ni ordenador.
La guía especifica penalización, pero no fija aquí su cuantía: para este simulacro
se propone **T = max(0, 0.1 × (aciertos − errores/3))**; blanco=0.
No atribuyas esta fórmula al profesorado. Marca respuestas en una hoja 1–30.

**1. ¿Qué combinación describe mejor el uso de Python y Java en la materia?**

- A) Python: ecosistema de datos/ML; Java: sistemas robustos y parte del ecosistema Big Data.
- B) Ambos lenguajes obligan a usar GPU en toda inferencia.
- C) Java sustituye a Pandas sin librerías; Python exige navegador.
- D) Python: solo frontend; Java: exclusivamente estadística.

**2. ¿Qué hace MCP en un sistema de agentes?**

- A) Entrena automáticamente el clasificador con nuevos pesos.
- B) Sustituye al protocolo de transporte de Kafka.
- C) Garantiza que toda herramienta tenga autorización de escritura.
- D) Estandariza la conexión con herramientas y fuentes de contexto.

**3. ¿Cuál es el resultado de [x*x for x in [1,2,3] if x>1]?**

- A) [1, 2, 3]
- B) [1, 4, 9]
- C) [4, 9]
- D) [2, 3]

**4. Para convertir una cadena JSON en un diccionario Python se usa:**

- A) dict.dump(cadena)
- B) pickle.dump(cadena)
- C) json.loads(cadena)
- D) json.dumps(cadena)

**5. ¿Qué conviene hacer con un pickle de origen desconocido?**

- A) Cargarlo porque la extensión garantiza datos puros.
- B) Quitar espacios al nombre para convertirlo en seguro.
- C) Evitar deserializarlo: puede ejecutar código.
- D) Renombrarlo a JSON y luego cargarlo con pickle.

**6. ¿Qué distingue una rama de Git de un entorno virtual?**

- A) Ambos almacenan únicamente librerías Python.
- B) La rama fija automáticamente las versiones del lockfile.
- C) Un venv sustituye los commits y la historia.
- D) La rama organiza historia de código; el entorno aísla dependencias.

**7. ¿Qué flujo respeta los entornos de este repositorio?**

- A) Usar un solo entorno global para todas las prácticas.
- B) Gestionar con uv y el lock local, manteniendo aislamiento por ejercicio.
- C) Instalar con sudo pip para compartir todas las dependencias.
- D) Copiar .venv entre sistemas como sustituto del lock.

**8. Un array de 12 elementos puede hacerse matriz 3×4 con:**

- A) arr.reshape(4, 4)
- B) arr.reshape(12, 12)
- C) arr.reshape(3, 5)
- D) arr.reshape(3, 4)

**9. ¿Qué selecciona arr[arr > 5]?**

- A) Todos los elementos desde la posición 5.
- B) Una copia con valores <=5 reemplazados por cero.
- C) Los elementos que cumplen una máscara booleana.
- D) Los índices siempre, aunque arr contenga float.

**10. Para dos condiciones sobre columnas Pandas se emplea normalmente:**

- A) (df.a > 0) && (df.b < 10)
- B) df.a > 0 and df.b < 10
- C) (df.a > 0) & (df.b < 10)
- D) (df.a > 0) + (df.b < 10) como filtro equivalente

**11. ¿Qué hace dropna() con sus valores por defecto sobre un DataFrame?**

- A) Elimina solo filas completamente nulas.
- B) Elimina filas que contienen al menos un valor ausente.
- C) Elimina duplicados sin revisar los nulos.
- D) Imputa todos los nulos con la media.

**12. ¿Qué instrucción modifica valores por una condición de forma explícita?**

- A) df['x'].median() = 0
- B) df.iloc['x'] = 0
- C) df[df['x'] < 0]['x'] = 0 como forma siempre fiable
- D) df.loc[df['x'] < 0, 'x'] = 0

**13. ¿Qué son Figure y Axes en Matplotlib?**

- A) Figure y Axes son siempre el mismo objeto.
- B) Figure es una serie; Axes es una base de datos.
- C) Axes es solo el título de la ventana.
- D) Figure es el contenedor general; Axes representa un gráfico con sus ejes.

**14. Para comparar temperatura por cámara, ¿qué gráfico ayuda?**

- A) Matriz de confusión sin etiquetas de clase.
- B) Boxplot de temperatura agrupada por cámara.
- C) Pie chart con una porción por lectura continua.
- D) Histograma solo de IDs sin temperatura.

**15. ¿Dónde se ajusta StandardScaler para evaluar un holdout?**

- A) Se ajusta por separado en test para hacer comparables métricas.
- B) Sobre train y test juntos para tener media global.
- C) Solo sobre test antes de entrenar.
- D) Solo en train; se transforma test con ese ajuste.

**16. ¿Qué código separa correctamente el target?**

- A) X = y = df[['averia']]
- B) X = df; y = df['averia']
- C) X = df[['averia']]; y = df['temperatura']
- D) X = df.drop(columns=['averia']); y = df['averia']

**17. Una categoría nominal sin orden se suele codificar con:**

- A) OrdinalEncoder porque todo texto tiene jerarquía.
- B) La columna target como sustituto de la categoría.
- C) OneHotEncoder.
- D) StandardScaler sin convertir el texto.

**18. ¿Para qué sirve Pipeline en sklearn?**

- A) Permite usar el test para ajustar todo sin sesgo.
- B) Encadena transformaciones y modelo, ajustando preprocesado dentro de fit/CV.
- C) Hace que todos los modelos usen los mismos hiperparámetros.
- D) Evita automáticamente cualquier fuga temporal o por grupos.

**19. ¿Cuál es una imputación razonable de stock con outliers?**

- A) Valor máximo de test para cada nulo de train.
- B) Mediana ajustada solo en train, con justificación del contexto.
- C) Etiqueta de fallo como valor sustituto de stock.
- D) Media calculada en train+test obligatoriamente.

**20. ¿Qué significa class_weight="balanced"?**

- A) Duplica físicamente cada muestra minoritaria.
- B) Pondera clases inversamente a su frecuencia en entrenamiento.
- C) Garantiza precisión y recall superiores.
- D) Equilibra siempre las probabilidades predichas a 50/50.

**21. ¿Dónde debe aplicarse SMOTE durante selección con CV?**

- A) Solo a entrenamiento de cada fold, sin sintetizar validación/test.
- B) Solo al test para facilitar recall.
- C) Después de calcular métricas para corregirlas.
- D) A todo el dataset antes del split.

**22. Recall de la clase positiva es:**

- A) (TP+TN)/N.
- B) TN/(TN+FP).
- C) TP/(TP+FP).
- D) TP/(TP+FN).

**23. Precision de la clase positiva es:**

- A) TP/(TP+FP).
- B) FP/(FP+TN).
- C) (TP+TN)/N.
- D) TP/(TP+FN).

**24. Si fallo tiene prevalencia 1%, predecir siempre no fallo produce:**

- A) Detección útil de todos los fallos.
- B) Recall 99% y accuracy 0%.
- C) F1 de fallo 99%.
- D) Accuracy 99%, pero recall de fallo 0%.

**25. En confusion_matrix con labels=[0,1], ¿qué representa [1,0]?**

- A) FP: real 0, predicho 1.
- B) TN: real 0, predicho 0.
- C) TP: real 1, predicho 1.
- D) FN: real 1, predicho 0.

**26. Para elegir un umbral se debe usar:**

- A) El target de cada fila test para decidir su umbral.
- B) La accuracy de entrenamiento como única garantía.
- C) Validación o predicciones CV de train; test queda final.
- D) El test repetidamente hasta lograr la mejor cifra.

**27. GridSearchCV debe recibir:**

- A) Todos los datos con transformaciones aprendidas globalmente.
- B) Test como entrenamiento para evitar sobreajuste.
- C) Solo las predicciones finales sin X ni y.
- D) Train y un esquema CV/scoring coherente con el objetivo.

**28. Al publicar una API de inferencia, el modelo suele cargarse:**

- A) Solo al apagar el servicio.
- B) Una vez durante arranque de cada proceso de la API.
- C) Después de enviar la respuesta al cliente.
- D) Desde disco en cada predicción como requisito general.

**29. BaseModel y field_validator se usan para:**

- A) Definir esquema de entrada y validar restricciones adicionales.
- B) Conceder acceso automático a cualquier endpoint.
- C) Entrenar los coeficientes del clasificador.
- D) Convertir toda entrada inválida en una predicción válida.

**30. Una entrada de inferencia válida debe:**

- A) Ordenar features alfabéticamente aunque train usara otro orden.
- B) Escalarse con un scaler nuevo ajustado a una sola solicitud.
- C) Incluir el target verdadero para la predicción.
- D) Respetar esquema, rangos y mismo orden de features que train.

## Parte práctica — cámaras frigoríficas (7 puntos; 115 min)

[CSV sintético](../../data/mock_exams_2026_10/refrigeracion.csv).
Cada registro es una lectura independiente del generador: no es serie temporal.
`Averia=1` significa anomalía etiquetada en esa lectura, no fallo futuro.
Cuatro cámaras C01–C04. Temperatura °C y potencia W; IDs no son features.
El dataset no prueba capacidad de mantenimiento predictivo ni eficacia real.
Bibliotecas necesarias preinstaladas: Pandas, NumPy, sklearn, Matplotlib y Pydantic 2.
Se permite documentación PDF local. No instales ni descargues durante el simulacro.

### P1. Inspección y limpieza (1.5 puntos; 25 min)

Normaliza nombres con **list comprehension** (strip, lower, espacios a `_`) y
muestra dimensiones/tipos/nulos/clases (0.5). Con **Pandas**, sin transformers
sklearn para limpieza, elimina duplicados exactos; luego rechaza temperatura
no finita/fuera de [-30,15], potencia no finita/fuera de [0,6000] y etiqueta
fuera de {0,1}. No imputes target. Exporta descartes con motivo y resumen,
conservando originales (0.75). Explica efecto de reglas y pérdida de datos (0.25).
Estos rangos son del ejercicio, no límites industriales universales.

### P2. Split y pipeline (2 puntos; 30 min)

Reserva **C04 completo para test**, el resto para train. Comprueba separación,
ambas clases y conteos (0.5). Features en orden ['temperatura_c','potencia_w'];
Pipeline(StandardScaler, LogisticRegression(max_iter=1000,
class_weight='balanced', random_state=42)), entrenado solo en train (1).
Explica pesos y por qué no equivalen a duplicación ni garantizan mejora (0.5).
No selecciones umbral en test: conserva 0.5.

### P3. Métricas y explicación (2 puntos; 30 min)

Predicciones en test, accuracy, balanced_accuracy, recall, precision, F1,
classification_report y matriz con labels=[0,1] (1). Compara con siempre 0 y
explica FN/FP, support y coste de cada error (0.75). Escribe limitación de evaluar
una sola cámara sintética y evita adjudicar generalización real (0.25).

### P4. Contrato de inferencia (1.5 puntos; 30 min)

BaseModel con temperatura_c/potencia_w, extra='forbid' y **field_validator**:
finito y rangos de P1 (0.75). Prueba extremos válidos y al menos negativo fuera
de rango, NaN, infinito y campo extra; temperatura negativa dentro del rango es
válida (0.5). Predice una solicitud válida con el pipeline y orden correcto;
define probabilidad de averia=1 (0.25). No hace falta desplegar una API.

Entrega notebook con explicaciones/salidas, CSV de descartes y predicciones de
test, y métricas. Guarda salidas en carpeta nueva; no sobrescribas el CSV de entrada.
