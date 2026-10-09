# Soluciones y rúbrica — 5073 — Programación para IA, simulacro A

[Volver al examen](../../materialak/Mock_Exams_2026-10/EXAMEN_A.md).
Corrección propuesta, no baremo docente. Se admiten alternativas coherentes con
los requisitos. Concede crédito parcial por razonamiento correcto aunque haya
un error aritmético posterior; no cuentes dos veces el mismo mérito.
Los valores calculados son respuestas de casos sintéticos, no resultados de planta.

## Test — máximo 3 puntos

| Nº | Respuesta | Motivo |
|---|---|---|
| 1 | A | La elección depende de ecosistema, integración y requisitos. |
| 2 | D | Conectar una herramienta no concede permiso para toda acción. |
| 3 | C | El filtro se aplica antes de construir cada elemento. |
| 4 | C | loads lee texto JSON; dumps serializa hacia texto. |
| 5 | C | La confianza en el origen importa en pickle/joblib. |
| 6 | D | Son aislamientos diferentes. |
| 7 | B | uv reutiliza caché sin mezclar estado lógico de ejercicios. |
| 8 | D | reshape conserva número de elementos. |
| 9 | C | Indexación por máscara filtra valores. |
| 10 | C | Usar operadores vectorizados y paréntesis. |
| 11 | B | subset/how pueden cambiar la regla; no es imputación. |
| 12 | D | loc evita asignación encadenada ambigua. |
| 13 | D | Una Figure puede contener varios Axes. |
| 14 | B | Boxplot muestra distribución, mediana y dispersión por grupo. |
| 15 | D | El test no debe informar los parámetros del escalado. |
| 16 | D | La etiqueta no puede permanecer como predictor de sí misma. |
| 17 | C | Ordinal requiere un orden justificable. |
| 18 | B | Pipeline ayuda, pero no corrige un split inadecuado. |
| 19 | B | La mediana resiste outliers mejor que la media. |
| 20 | B | Pesos n/(K*n_c); no equivale a oversampling. |
| 21 | A | Remuestrear antes del split puede contaminar evaluación. |
| 22 | D | Mide cobertura de positivos reales. |
| 23 | A | Mide acierto de positivos predichos. |
| 24 | D | Accuracy aislada engaña con desbalance. |
| 25 | D | Filas reales, columnas predichas. |
| 26 | C | Optimizar con test lo convierte en parte de selección. |
| 27 | D | La selección necesita respetar frontera de validación. |
| 28 | B | Evitar carga repetida; cada worker tiene su proceso. |
| 29 | A | Validación de datos no sustituye autenticación ni modelo. |
| 30 | D | Usar el pipeline entrenado y su contrato de entrada. |

Aplicar T=max(0,0.1×(A−E/3)); A+E+blancos=30. Si A=24,E=3,blancos=3,
T=2.3. Esta penalización es una propuesta de entrenamiento.

## Práctica — máximo 7 puntos

Resultados estructurales del CSV generado: **322 filas**, **2 duplicados exactos**,
**12 inválidas restantes**, **308 válidas**. Tras limpiar: 32 positivas y 276
negativas. Train C01–C03: **231 filas, 24 positivas**; test C04: **77 filas,
8 positivas**. Los IDs se excluyen del modelo. Estos conteos no prescriben
métricas del clasificador: deben salir de la ejecución.

Código de referencia. Desde la raíz del repositorio, pegarlo en un notebook o
script nuevo; crea/sobrescribe únicamente `resultados_mock_programacion/`.
Conserva una copia de esa salida antes de repetir si interesa comparar.
Selecciona un entorno local con las dependencias declaradas; para preparar uno
fuera del tiempo de examen usa uv, no pip global.

```python
from pathlib import Path
import math
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, recall_score, precision_score,
    f1_score, classification_report, confusion_matrix,
)
from pydantic import BaseModel, ConfigDict, field_validator, ValidationError

source = Path('04_Programazioa_5073/data/mock_exams_2026_10/refrigeracion.csv')
out = Path('resultados_mock_programacion')
out.mkdir(exist_ok=True)
df = pd.read_csv(source)
df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
print(df.shape, df.dtypes, df.isna().sum(), df['averia'].value_counts())
duplicate = df.duplicated()
unique = df.loc[~duplicate].copy()
temp_ok = np.isfinite(unique['temperatura_c']) & unique['temperatura_c'].between(-30, 15)
power_ok = np.isfinite(unique['potencia_w']) & unique['potencia_w'].between(0, 6000)
label_ok = unique['averia'].isin([0, 1])
ok = temp_ok & power_ok & label_ok
bad = unique.loc[~ok].copy()
bad['motivo'] = [
    ';'.join(reason for reason, valid in [
        ('temperatura', temp_ok.loc[i]), ('potencia', power_ok.loc[i]),
        ('etiqueta', label_ok.loc[i]),
    ] if not valid) for i in bad.index
]
dup = df.loc[duplicate].copy()
dup['motivo'] = 'duplicado_exacto'
pd.concat([dup, bad]).to_csv(out / 'descartes.csv', index=False)
clean = unique.loc[ok].copy()
assert len(df) == 322 and duplicate.sum() == 2 and len(bad) == 12
assert len(clean) == 308
train = clean.loc[clean.camara_id != 'C04']
test = clean.loc[clean.camara_id == 'C04']
assert set(train.camara_id).isdisjoint(set(test.camara_id))
assert set(train.averia) == set(test.averia) == {0, 1}
assert len(train) == 231 and len(test) == 77
features = ['temperatura_c', 'potencia_w']
model = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(
        max_iter=1000, class_weight='balanced', random_state=42
    )),
])
model.fit(train[features], train.averia)
pred = model.predict(test[features])
def evaluate(y, p):
    return dict(
        accuracy=accuracy_score(y, p), balanced_accuracy=balanced_accuracy_score(y, p),
        recall=recall_score(y, p, zero_division=0),
        precision=precision_score(y, p, zero_division=0),
        f1=f1_score(y, p, zero_division=0),
    )
metrics = evaluate(test.averia, pred)
baseline = evaluate(test.averia, np.zeros(len(test), dtype=int))
print(metrics, baseline)
print(classification_report(test.averia, pred, labels=[0, 1], zero_division=0))
print(confusion_matrix(test.averia, pred, labels=[0, 1]))
pd.DataFrame([metrics, baseline], index=['modelo', 'siempre_0']).to_csv(out / 'metricas.csv')
predictions = test[['registro_id', 'averia']].copy()
predictions['prediccion'] = pred
predictions.to_csv(out / 'predicciones.csv', index=False)

class Solicitud(BaseModel):
    model_config = ConfigDict(extra='forbid')
    temperatura_c: float
    potencia_w: float

    @field_validator('temperatura_c', 'potencia_w')
    @classmethod
    def validate_value(cls, value, info):
        lo, hi = (-30, 15) if info.field_name == 'temperatura_c' else (0, 6000)
        if not math.isfinite(value) or not lo <= value <= hi:
            raise ValueError('fuera de rango o no finito')
        return value

for t, p in [(-30, 0), (15, 6000), (-18, 2500)]:
    Solicitud(temperatura_c=t, potencia_w=p)
invalid = [
    dict(temperatura_c=-31, potencia_w=100),
    dict(temperatura_c=-18, potencia_w=-1),
    dict(temperatura_c=float('nan'), potencia_w=100),
    dict(temperatura_c=-18, potencia_w=float('inf')),
    dict(temperatura_c=-18, potencia_w=100, extra=1),
]
for entry in invalid:
    try:
        Solicitud(**entry)
    except ValidationError:
        pass
    else:
        raise AssertionError('entrada inválida aceptada')
request = Solicitud(temperatura_c=-10, potencia_w=3500)
row = pd.DataFrame([[request.temperatura_c, request.potencia_w]], columns=features)
class_idx = list(model.classes_).index(1)
print('Predicción:', int(model.predict(row)[0]))
print('Probabilidad averia=1:', float(model.predict_proba(row)[0, class_idx]))
```

### P1 — 1.5 puntos

Inspección y comprehension 0.5; deduplicación/validación/descartes con motivo
0.75; interpretación 0.25. Descartar no es imputar. Son reglas fijas del caso,
no parámetros aprendidos de test. Los duplicados se retiran antes del split.
Se eliminan 14/322 filas; invalidar temperatura negativa sin mirar rango es error:
una cámara frigorífica puede tener temperatura válida negativa.

### P2 — 2 puntos

Split/comprobaciones 0.5; pipeline y fit solo train 1; explicación 0.5.
Pesos n/(K*n_c): clase 1 =231/48=**4.8125**; clase 0=231/414≈**0.5580**.
Cambian contribución a la pérdida; no generan registros, no cambian prevalencia
real y no garantizan mejora. El test C04 simula cámara nueva, no futuro temporal.

### P3 — 2 puntos

Métricas/matriz/reporte 1; baseline/interpretación 0.75; límite 0.25.
Baseline accuracy=69/77≈**0.8961**, balanced accuracy=**0.5**, recall/F1=0.
Precision con cero predicciones positivas es indefinida, se usa zero_division=0.
Filas reales/columnas predichas, matriz [[TN,FP],[FN,TP]], support número real de
cada clase. FN omite avería; FP moviliza revisión innecesaria. Test pequeño y
sintético no valida planta ni calibración; cambiar umbral mirando test invalida
su papel final. Explicar métricas obtenidas, sin asegurar que balanced mejora.

### P4 — 1.5 puntos

Esquema/validator 0.75; pruebas explícitas 0.5; inferencia/orden/clase 0.25.
La probabilidad procede de columna asociada a clase 1; no se interpreta como
certeza ni como probabilidad calibrada demostrada. No desplegar API evita añadir
trabajo fuera del checklist.
