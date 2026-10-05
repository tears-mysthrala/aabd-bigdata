#!/usr/bin/env python3
"""Genera un informe autónomo desde salidas calculadas y capturas Orange reales."""
from pathlib import Path
import json,csv,sys
BASE=Path(__file__).resolve().parent
if (BASE/'.pdf-deps').exists():sys.path.insert(0,str(BASE/'.pdf-deps'))
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,Preformatted
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xml.sax.saxutils import escape
pdfmetrics.registerFont(TTFont('DejaVu',str(BASE/'recursos/LiberationSans-Regular.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuBold',str(BASE/'recursos/LiberationSans-Bold.ttf')))
styles=getSampleStyleSheet();styles['Normal'].fontName='DejaVu';styles['Normal'].fontSize=10;styles['Normal'].leading=14;styles['Normal'].spaceAfter=9
for s in ['Title','Heading1','Heading2']: styles[s].fontName='DejaVuBold';styles[s].textColor=colors.HexColor('#15354b')
styles['Title'].fontSize=23;styles['Title'].leading=28;styles['Heading1'].fontSize=17;styles['Heading1'].leading=22
styles.add(ParagraphStyle('Small',parent=styles['Normal'],fontSize=8,leading=11))
m=json.loads((BASE/'salidas/metricas.json').read_text());c=json.loads((BASE/'config.json').read_text());story=[]
def p(txt,style='Normal'):story.append(Paragraph(txt,styles[style]))
def h(txt):p(txt,'Heading1')
def table(rows,widths=None):
 t=Table([[Paragraph(escape(str(v)),styles['Small']) for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eff4')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#7390a2')),('BOTTOMPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f6f8fa')])]))
 story.append(t);story.append(Spacer(1,10))
def image(name,width=500):
 im=Image(str(BASE/'capturas'/name));aspect=im.imageHeight/im.imageWidth;im.drawWidth=width;im.drawHeight=width*aspect;story.append(im)
def page():story.append(PageBreak())
def footer(canvas,doc):
 canvas.saveState();canvas.setFont('DejaVu',8);canvas.setFillColor(colors.HexColor('#5b6f7c'));canvas.drawString(45,25,'5072 · Machine Learning · Iris · ejecución 05/10/2026');canvas.drawRightString(A4[0]-45,25,str(doc.page));canvas.restoreState()
correct=round(m['accuracy']*150);kind=c['kind']
p(c['title'],'Title');p('Práctica individual con Orange Data Mining','Heading2')
p('El objetivo es predecir la especie de una flor a partir de cuatro medidas y evaluar el modelo con datos que no participaron en el ajuste de esa predicción. Iris permite relacionar las decisiones del algoritmo con características concretas y observar dónde aparecen los errores.')
h('Datos y variables')
p('Se emplea Iris (Fisher, 1936), del repositorio UCI: 150 registros, cuatro medidas en centímetros y tres especies. La copia entregada coincide exactamente con <i>sklearn.datasets.load_iris</i>; no hay valores ausentes. Cada especie tiene 50 registros.')
table([['Campo','Significado / función'],['sepal_length / sepal_width','Longitud / anchura del sépalo, en cm; predictoras'],['petal_length / petal_width','Longitud / anchura del pétalo, en cm; predictoras'],['iris','Objetivo: setosa, versicolor o virginica']], [155,350])
h('Diseño experimental')
p('Validación cruzada estratificada de 10 particiones, con barajado y semilla 42. Cada ciclo ajusta con 135 flores y evalúa otras 15: cinco por especie. Las 150 predicciones fuera de muestra (OOF) se reúnen una sola vez por fila. Los hiperparámetros se fijan antes de la evaluación y no se optimizan utilizando estos resultados.')
if kind=='svm':p('La normalización de Orange (<i>AdaptiveNormalize</i>) calcula media y desviación en las 135 filas de entrenamiento de cada ciclo y aplica esa transformación a las 15 filas retenidas. No se normaliza la tabla completa antes de dividir. La semilla 42 también fija la calibración interna de probabilidades del SVM.')
else:p('No se aplica escalado a las cuatro variables continuas. Los preprocesadores por defecto del learner se ejecutan dentro del ajuste; no se entrega al evaluador una tabla preprocesada globalmente.')
p('El modelo ajustado con las 150 flores se utiliza exclusivamente para inspección. Su comportamiento sobre esos datos no se presenta como estimación de generalización. No hay un test externo independiente.')
p('Fuente: Fisher, R. (1936). Iris [Dataset]. UCI. DOI: 10.24432/C56C76. Licencia CC BY 4.0. https://archive.ics.uci.edu/dataset/53/iris','Small')
page();h('Modelo y resultados fuera de muestra')
if kind=='tree':
 p('El árbol de Orange divide los datos mediante reglas sobre los atributos. Se limita la profundidad a 3 para facilitar la inspección. Las hojas tienen al menos dos ejemplos; no se dividen subconjuntos menores de cinco. Se permiten cortes binarios y se detiene una rama si la mayoría alcanza el 95 %. Estos límites reducen la complejidad, pero pueden dejar errores en regiones solapadas.')
elif kind=='forest':
 p('Random Forest agrega 100 árboles entrenados con remuestreo bootstrap. En cada división considera sqrt(4) = 2 atributos. Se fija la semilla 42; no se limita la profundidad y se impide dividir nodos con menos de cinco registros. No se usan pesos de clase: las tres especies tienen igual frecuencia. La votación conjunta reduce la dependencia de un único árbol, sin garantizar mayor precisión en todos los problemas.')
else:
 p('El clasificador SVC utiliza un kernel RBF: K(x,z)=exp(-0,25·||x-z||²), aplicado a las medidas normalizadas. C=1 controla la penalización por errores; gamma=0,25 determina el alcance de la similitud. La tolerancia es 0,001 y no se limita el número de iteraciones. Se calculan probabilidades para la exploración ROC. El margen opera en el espacio del kernel y no equivale a reglas simples de centímetros.')
table([['Medida','Resultado OOF'],['Accuracy (CA)',f'{correct}/150 = {m["accuracy"]:.4f}'],['F1 ponderado / macro',f'{m["f1_weighted"]:.4f} / {m["f1_macro"]:.4f}'],['AUC multicategoría Orange',f'{m["auc_weighted"]:.4f}']], [260,245])
p('Accuracy es la proporción de etiquetas acertadas. F1 combina precisión y sensibilidad; se pondera por el soporte de cada especie. Como los soportes son iguales, coincide con F1 macro. AUC resume discriminación a partir de probabilidades y no mide el porcentaje de etiquetas acertadas. La ROC mostrada más adelante corresponde a una clase contra las restantes; no representa una curva única de las tres especies.','Small')
rows=[['Especie','Precisión','Sensibilidad','F1','Soporte']]
for label in m['classes']:
 r=m['classification_report'][label];rows.append([label,*[f'{r[k]:.4f}' for k in ['precision','recall','f1-score']],int(r['support'])])
table(rows,[125,100,100,100,80])
h('Matriz de confusión')
table([['Real / Predicha',*m['classes']]]+[[label,*m['confusion_matrix'][i]] for i,label in enumerate(m['classes'])],[170,110,110,115])
p('Cada fila corresponde a la especie real y cada columna a la predicha. Las filas suman 50 y la matriz completa suma 150. Los errores se concentran entre versicolor y virginica; setosa se distingue sin errores en esta ejecución.','Small')
page();h('Ejecución nativa en Orange: Test &amp; Score')
p(f'La tabla procede de un widget Orange real sobre la copia incluida de Iris. Configuración: validación cruzada, 10 folds, estratificada. Su salida reproduce exactamente una segunda ejecución con la API de Orange: etiquetas, orden de filas y probabilidades. No se ha dibujado una interfaz simulada.')
image('orange_test_score.png',500)
p('Captura obtenida mostrando el widget en Wayland y guardando exclusivamente su ventana mediante QWidget.grab(). Las columnas CA y F1 se redondean en pantalla; metricas.json conserva los valores completos.','Small')
h('Flujo reproducible')
p('File (datos/iris.csv) → Python Script → Learner → Test &amp; Score. File también entrega los datos originales directamente al evaluador. Evaluation Results alimenta Confusion Matrix y ROC Analysis. El script incluido configura el mismo learner que ha generado todas las salidas. El archivo .ows guarda esos parámetros y una ruta relativa al conjunto de datos.')
if kind=='forest':p('El widget estándar Random Forest de esta versión usa semilla 0 al activar entrenamiento replicable. Se utiliza Python Script para fijar exactamente la semilla 42, que forma parte del experimento.','Small')
p('Artefactos: modelo_orange.py, reproducir.py, config.json, salidas/predicciones_oof.csv y salidas/metricas.json. El CSV mantiene row_id, fold, las cuatro medidas, clase real, clase predicha y probabilidades por especie.','Small')
page();h('Matriz y ROC: capturas Orange')
image('orange_confusion.png',425)
p('Matriz de confusión sobre las predicciones OOF. Permite localizar el sentido de cada equivocación; los totales verifican la cobertura de la evaluación.','Small')
image('orange_roc.png',425)
p('ROC nativa para versicolor frente al resto. Un área alta indica buena ordenación de probabilidades, pero no elimina los errores de clasificación. El trazo y el AUC dependen del protocolo y no prueban comportamiento en flores nuevas de otro origen.','Small')
page();h('Inspección e interpretación del modelo')
if kind=='tree':
 image('orange_tree_viewer.png',450)
 p('Tree Viewer muestra el árbol ajustado con las 150 flores, empleado para interpretar reglas. La regla petal_length ≤ 1,9 cm identifica setosa; después, petal_width > 1,7 cm conduce a una hoja mayoritariamente virginica. Si la anchura es ≤ 1,7 cm, petal_length ≤ 4,9 cm conduce a una hoja mayoritariamente versicolor. El árbol tiene siete nodos y cuatro hojas. Las distribuciones y frecuencias visibles pertenecen al ajuste completo, mientras que las métricas anteriores proceden de los diez modelos CV.','Small')
else:
 image('orange_modelo.png',450)
 p('Python Script nativo configura el learner de forma explícita. out_classifier se ajusta con la tabla completa solo para inspección y out_learner se evalúa mediante validación cruzada. La semilla y los parámetros visibles están incluidos en el workflow.','Small')
h('Errores y conclusión')
if m['errors']:
 first=m['errors'][0]; f=first['features']
 p(f'Se observan {len(m["errors"])} errores en 150 predicciones. Por ejemplo, la fila {first["row_id"]} (fold {first["fold"]}) es {first["real"]} y se predice como {first["predicha"]}; tiene pétalo de {f[2]:.1f} cm de longitud y {f[3]:.1f} cm de anchura. El modelo utiliza las cuatro medidas: un ejemplo aislado no establece una causa única del error. El listado completo se conserva en el CSV OOF.')
p(f'El modelo obtiene accuracy {m["accuracy"]:.4f} y F1 ponderado {m["f1_weighted"]:.4f} en el protocolo fijado. La distinción de setosa es clara en esta muestra, mientras que el solapamiento versicolor/virginica exige revisar sensibilidad y precisión por clase. El conjunto es pequeño, clásico y equilibrado; estos resultados no demuestran superioridad general del algoritmo ni garantizan el comportamiento sobre un nuevo origen de datos.')
p('Reproducibilidad: Orange '+m['versions']['Orange']+'; scikit-learn '+m['versions']['sklearn']+'; NumPy '+m['versions']['numpy']+'. Los SHA-256 del dataset, flujo, modelo y CSV se registran en salidas/metricas.json.','Small')
p('Documentación del procedimiento: https://orangedatamining.com/widget-catalog/evaluate/testandscore/ (validación cruzada, métricas y salidas de evaluación).','Small')
out=BASE/(c['stem']+'.pdf');SimpleDocTemplate(str(out),pagesize=A4,leftMargin=45,rightMargin=45,topMargin=38,bottomMargin=44,title=c['title'],author='Práctica de Machine Learning',pageCompression=1).build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
