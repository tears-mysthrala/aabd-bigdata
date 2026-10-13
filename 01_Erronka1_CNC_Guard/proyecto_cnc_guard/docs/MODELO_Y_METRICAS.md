# Clasificador supervisado: diseño y límites

El generador de datos cnc_10M.csv construye la etiqueta errorea en la misma
lectura (umbral de temperatura/vibración más ruido aleatorio). Esto es un
clasificador de estado sintético, NO un predictor verificado a 24 horas.
Tampoco es válido trasladar sin medición el 3,4% de prevalencia usado como
ejemplo por la rúbrica: medir la tasa real en cada muestra.

RandomForestClassifier es la opción principal de esta versión. Aplica
class_weight=balanced_subsample para la minoría. No se usa SMOTE: si se
añade, implementarlo SOLO dentro de los folds de entrenamiento (nunca
antes de separar tiempo) para evitar fuga de información.

## Variables, aprendizaje y serving

- Sensores actuales: tenperatura, bibrazioa, presioa.
- Interacciones: producto temperatura*vibración y temperatura al cuadrado.
- Historias causales: media de las tres lecturas ANTERIORES por máquina para
  temperatura/vibración, y delta contra la última temperatura anterior.
  Calcular con groupby(makina_id), shift(1), rolling(3). Nunca incluir
  información futura ni etiquetas en features.
- API: aportar history de hasta tres lecturas PREVIAS de la misma máquina.
  Si no se aporta, se usan valores actuales como cold start. La respuesta
  marca history_available=false; esto puede afectar a la calidad y debe
  medirse. La implementación NiFi debe reconstruir la ventana causal.
- Splits globales cronológicos: 60% train, 20% validation, 20% test. Validación
  ajusta umbral binario con F2, test solo estima calidad. No confundirlo con
  las bandas fijas de alertas 0.15 AVISO y 0.70 CRITICA.
- Métricas: confusion_matrix [TN FP; FN TP], precision, recall, F1, ROC-AUC,
  average_precision, prevalencia y relevancia de variables. TimeSeriesSplit
  adicional SOLO dentro de train si hay ambas clases.
- Advertencia: evitar accuracy aislada. Un recall alto con FP excesivos
  aumenta el coste operativo; justificar con curva precision-recall.

## Comandos desde la raíz de proyecto_cnc_guard

    uv sync --locked
    uv run --locked python scripts/train_supervised.py \
      --csv ../../04_Programazioa_5073/data/cnc_10M.csv \
      --max-rows 50000 \
      --out models/rf-rubrica.joblib \
      --metrics reports/rubrica-metricas.json

    CNC_MODEL_PATH=models/rf-rubrica.joblib \
    uv run --locked --with fastapi --with uvicorn \
      uvicorn cnc_guard.api:app --host 127.0.0.1 --port 18080 --workers 1

Estas rutas son de ejemplo. El script se niega a sobrescribir evidencias.
Ningún valor de accuracy/F1/recall está inventado en este documento.
El default de 50.000 muestras utiliza las PRIMERAS filas del archivo:
sirve para desarrollo local, no generalización a 10 millones ni a plantas.
Registrar muestras de validación posteriores y por máquina antes de decidir.

Los modelos joblib usan pickle: cargar solo artefactos confiables, nunca
archivos recibidos de terceros. Separar entrenamiento offline de inferencia.

## Coste del negocio

La cifra docente de 1.200 EUR/hora es una hipótesis, no ahorro medido. Un
balance cuantitativo necesita duración/coste de paradas, FP y FN, coste
de inspección y condiciones operativas. No automatizar paradas por esta API.
