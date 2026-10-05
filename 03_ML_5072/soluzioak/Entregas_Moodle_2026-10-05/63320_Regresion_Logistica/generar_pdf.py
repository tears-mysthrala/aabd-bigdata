"""Informe académico autocontenido. Dependencia: reportlab (ver README)."""
from pathlib import Path
import csv,json
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
BASE=Path(__file__).resolve().parent
LOGISTIC='63320' in BASE.name
M=json.loads((BASE/'resultados.json').read_text())
OUT=BASE/('63320_Regresion_Logistica_Unai_Urzainqui_Perez.pdf' if LOGISTIC else '63321_KNN_Iris_Unai_Urzainqui_Perez.pdf')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleCustom',fontName='Helvetica-Bold',fontSize=23,leading=29,textColor=colors.HexColor('#153f53'),spaceAfter=13))
styles.add(ParagraphStyle(name='Sub',fontSize=12,leading=17,textColor=colors.HexColor('#497283'),spaceAfter=12))
styles['BodyText'].fontName='Helvetica';styles['BodyText'].fontSize=10.6;styles['BodyText'].leading=15;styles['BodyText'].spaceAfter=9
styles['Heading2'].fontSize=15;styles['Heading2'].leading=20;styles['Heading2'].textColor=colors.HexColor('#153f53');styles['Heading2'].spaceBefore=8;styles['Heading2'].spaceAfter=10
styles.add(ParagraphStyle(name='CaptionCustom',fontSize=8.1,leading=11,textColor=colors.HexColor('#4c5960'),spaceBefore=4,spaceAfter=10))
styles.add(ParagraphStyle(name='TableCustom',fontSize=9.2,leading=12))
story=[]
def p(s,style='BodyText'): story.append(Paragraph(s,styles[style]))
def heading(s): p(s,'Heading2')
def img(name,width=499):
 from PIL import Image as PILImage
 path=BASE/'evidencias'/name
 with PILImage.open(path) as im: w,h=im.size
 story.append(Image(str(path),width=width,height=width*h/w))
def table(rows,widths=None):
 cells=[[Paragraph(escape(str(c)),styles['TableCustom']) for c in row] for row in rows]
 t=Table(cells,colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e3edf1')),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#b8c7ce')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 story.append(t);story.append(Spacer(1,11))
def newpage(): story.append(PageBreak())
def footer(canv,doc):
 canv.setStrokeColor(colors.HexColor('#aac1cc'));canv.line(48,39,A4[0]-48,39)
 canv.setFont('Helvetica',8);canv.setFillColor(colors.HexColor('#52616b'))
 canv.drawString(48,27,'Unai Urzainqui Perez | Orange Data Mining | 05/10/2026')
 canv.drawRightString(A4[0]-48,27,str(doc.page))

p('Regresión logística' if LOGISTIC else 'Clasificación con KNN','TitleCustom')
p('Orange Data Mining - tarea '+str(M['task']),'Sub')
p('<b>Autor:</b> Unai Urzainqui Perez<br/><b>Fecha:</b> 5 de octubre de 2026')
heading('1. Objetivo y datos elegidos')
p('Aplicar un modelo de regresión logística a un conjunto de datos real, explicar su preparación y analizar sus salidas. Se utiliza WDBC porque combina una variable numérica interpretable con un objetivo binario. Se restringe el modelo a <b>texture_mean</b> para estudiar la relación entre textura y diagnóstico; las otras 29 variables del conjunto original no intervienen.' if LOGISTIC else 'Aplicar KNN a un conjunto de datos real y explicar cómo sus medidas permiten clasificar una flor. Iris permite trabajar con cuatro variables continuas, tres clases equilibradas y errores fáciles de revisar. El modelo utiliza las cuatro medidas, sin reducir la dimensión.')
p('WDBC contiene <b>569 muestras</b>: 357 B (benignas) y 212 M (malignas), sin valores ausentes. texture_mean resume la textura de los núcleos mediante la desviación de los niveles de gris. <b>diagnosis</b> es el objetivo; sample_id se conserva solo como metadato.' if LOGISTIC else 'Se utilizan <b>150 flores</b>, 50 por especie: setosa, versicolor y virginica. Las variables son longitud y anchura del sépalo y del pétalo, en centímetros. <b>iris</b> es el objetivo; no existen valores ausentes en la copia evaluada.')
img('orange_file.png')
p('Figura 1. Widget File nativo de Orange: datos cargados y papel de las columnas. Captura de la misma tabla usada en la evaluación.','CaptionCustom')
newpage()
heading('2. Configuración del modelo y evaluación')
p('<b>Modelo:</b> regresión logística con regularización Ridge (L2), C=1, intercepto y sin ponderación de clases. La textura se estandariza a media 0 y desviación 1 <b>dentro del entrenamiento de cada fold</b>, mediante Preprocess conectado al Learner. El solver es lbfgs; el widget usa max_iter=10000 y random_state=0.' if LOGISTIC else '<b>Modelo:</b> kNN con <b>k=3</b>, distancia euclídea y voto uniforme. No se aplica normalización. Los preprocesadores predeterminados de Orange gestionan variables categóricas y datos ausentes; aquí todas las entradas ya son numéricas y completas. Un cambio de escala puede cambiar qué vecinos resultan más próximos.')
# Native model widget captures are kept at the size shown; embedded proportionally.
img('orange_modelo.png',180)
p('Figura 2. Parámetros del learner en su widget nativo.','CaptionCustom')
p('<b>Evaluación:</b> validación cruzada estratificada de 10 folds, barajada y con semilla 42. Cada fila se evalúa exactamente una vez con un modelo entrenado sin esa fila. La semilla 42 es la que utiliza Test &amp; Score en Orange 3.40.0.')
img('orange_test_score.png')
p('Figura 3. Test &amp; Score ejecutado de forma nativa. Las columnas F1, precisión y recall muestran el promedio ponderado por soporte de las clases.','CaptionCustom')
newpage()
heading('3. Salidas y análisis de los errores')
p(f'La evaluación fuera de muestra obtiene <b>{int(round(M["CA"]*M["rows"]))}/{M["rows"]} aciertos</b>, exactitud <b>{M["CA"]:.4f}</b> y AUC {M["AUC_Orange_weighted"]:.4f}. La referencia de predecir siempre una clase mayoritaria alcanza {M["majority_baseline"]:.4f}.')
img('orange_confusion.png')
p('Figura 4. Confusion Matrix nativa. Filas: clase real; columnas: clase predicha. Los números corresponden a las predicciones OOF exportadas, sin mezclar el orden de los folds con el de las filas originales.','CaptionCustom')
rows=[['Clase','Precisión','Recall','F1','n']]
for cls in M['classes']:
 r=M['classification_report'][cls];rows.append([cls,f'{r["precision"]:.4f}',f'{r["recall"]:.4f}',f'{r["f1-score"]:.4f}',int(r['support'])])
r=M['classification_report']['weighted avg']; rows.append(['Ponderado',f'{r["precision"]:.4f}',f'{r["recall"]:.4f}',f'{r["f1-score"]:.4f}',M['rows']])
table(rows,[119,95,95,95,95])
p('Hay <b>120 M clasificadas como B</b> y 47 B clasificadas como M. El recall de M es 92/212 = 0,4340: la exactitud global de 0,7065 oculta un comportamiento mucho peor para esa clase. La balanced accuracy es 0,6512. Este ejemplo de una sola variable deja amplio solapamiento entre clases.' if LOGISTIC else 'Setosa se clasifica correctamente en las 50 filas. Tres versicolor se confunden con virginica y tres virginica con versicolor. Las dos clases comparten regiones de medidas próximas; estos seis errores concentran toda la pérdida de exactitud. No se han seleccionado k ni escalado después de observar el resultado.')
if LOGISTIC:
 newpage()
 heading('4. Curva del modelo y diagnósticos observados')
 img('curva_explicativa.png')
 p('Figura 5. Figura explicativa generada con el modelo ajustado sobre las 569 filas. Los puntos representan <b>diagnósticos observados</b>, B=0 y M=1, frente a la textura real. La línea representa la probabilidad calculada por el modelo; no son probabilidades observadas.','CaptionCustom')
 p('La logística transforma el score lineal z en una probabilidad: <b>p(M)=1/(1+exp(-z))</b>. Al aumentar la textura, la probabilidad ajustada aumenta, pero ambas clases siguen apareciendo en una misma zona. Dibujar p frente a logit(p) colocaría los puntos sobre la sigmoide por construcción; no demostraría concordancia con los diagnósticos.')
 img('orange_roc.png',460)
 p('Figura 6. ROC Analysis nativo con M como objetivo. La curva usa las probabilidades OOF; la sigmoide superior usa ajuste completo únicamente para explicar el modelo. AUC=0,7745 mide ordenación, no garantiza acierto ni seguridad de una decisión.','CaptionCustom')
newpage()
heading('5. Conclusiones y límites' if LOGISTIC else '4. Conclusiones y límites')
if LOGISTIC:
 p('La textura media contiene información sobre el diagnóstico: su media es 17,9148 en B y 21,6049 en M. La logística de una variable supera la referencia mayoritaria, aunque produce 167 errores. La regularización y la normalización no compensan la información descartada al excluir las demás variables.')
 p('La validación cruzada estima el comportamiento dentro de esta muestra histórica. No se ha realizado validación temporal, externa ni prospectiva. No se ha estudiado calibración o incertidumbre individual y el umbral 0,5 no ha sido optimizado. <b>El modelo y este informe son educativos; no sirven para decisiones clínicas.</b>')
else:
 with (BASE/'predicciones_oof.csv').open() as stream: errors=[r for r in csv.DictReader(stream) if r['acierto']=='0']
 table([['Fila original','Fold','Real','Predicho']]+[[r['row_id'],r['fold'],r['real'],r['predicho']] for r in errors],[100,65,167,167])
 p('KNN obtiene 0,9600 de exactitud en este protocolo fijo. El buen resultado se explica por la cercanía entre flores de la misma especie; los errores se concentran entre versicolor y virginica. KNN conserva ejemplos y decide por vecinos, de modo que sus resultados dependen de k, la distancia, la escala y la cobertura de los datos.')
 p('Los 150 casos constituyen una muestra pequeña y clásica. La CV no prueba el resultado en nuevas poblaciones, mediciones con otras unidades o flores ajenas a estas tres especies. No se ha hecho búsqueda de hiperparámetros ni comparación estadística. Una probabilidad de 1 significa unanimidad de los tres vecinos, <b>no certeza garantizada</b>.')
heading('Reproducción y trazabilidad')
p('El paquete incluye <b>Flujo_Orange.ows</b>, la tabla en <b>datos/</b>, <b>reproducir.py</b>, <b>predicciones_oof.csv</b>, <b>resultados.json</b> y las capturas nativas en <b>evidencias/</b>. El workflow utiliza una ruta relativa a sus propios datos. El README explica cómo abrirlo o repetir la evaluación.')
p('Se comprobaron la matriz, los totales por clase, una evaluación por fila, la alineación entre datos y etiquetas y las particiones de los diez folds. La salida de Test &amp; Score coincide con una segunda evaluación por la API de Orange (incluidas las probabilidades, tolerancia 1e-10). Los hashes SHA-256 permiten detectar modificaciones de los archivos.')
p(f'<b>Entorno verificado:</b> Orange {M["versions"]["Orange"]}; scikit-learn {M["versions"]["sklearn"]}; NumPy {M["versions"]["numpy"]}; Python {M["versions"]["python"]}.')
heading('Fuentes de los datos')
if LOGISTIC:
 p('Wolberg, W.; Mangasarian, O.; Street, N.; Street, W. (1993). <i>Breast Cancer Wisconsin (Diagnostic)</i>. UCI Machine Learning Repository. DOI: <link href="https://doi.org/10.24432/C5DW2B" color="#153f53">10.24432/C5DW2B</link>. CC BY 4.0. Se entrega la selección de texture_mean con las etiquetas originales.')
else:
 p('Fisher, R. A. (1936). <i>Iris</i>. UCI Machine Learning Repository. DOI: <link href="https://doi.org/10.24432/C56C76" color="#153f53">10.24432/C56C76</link>. CC BY 4.0. Se usa la copia Iris del ejercicio, contrastada con load_iris de scikit-learn.')
p('Los enlaces de procedencia se consultaron el 05/10/2026. Las métricas proceden de la ejecución local documentada; no de ejemplos de la fuente.','CaptionCustom')
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=42,bottomMargin=53,title='Regresión logística en Orange' if LOGISTIC else 'KNN Iris en Orange',author='Unai Urzainqui Perez')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT.name)
