"""Informe específico de la tarea 63638, desde resumen y capturas Orange."""
from pathlib import Path
import json

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

BASE=Path(__file__).resolve().parent


def main():
    m=json.loads((BASE/'resumen.json').read_text())
    styles=getSampleStyleSheet()
    styles['BodyText'].leading=15
    styles['BodyText'].spaceAfter=9
    story=[]
    def p(text,style='BodyText'): story.append(Paragraph(text,styles[style]))
    def image(name,width):
        img=Image(str(BASE/name))
        img.drawHeight=width*img.imageHeight/img.imageWidth
        img.drawWidth=width
        story.append(img)
    p('Interpretación de datos con Orange','Title')
    p('5072 · Tarea Moodle 63638 · Iris · 2 de octubre de 2026')
    p('1. Introducción','Heading1')
    p('Objetivo: interpretar medidas de flores de tres especies de Iris y comprobar qué patrones permite observar Orange. Se usa el dataset Iris disponible en el repositorio, con 150 registros, cuatro medidas en centímetros y la especie como etiqueta: 50 setosa, 50 versicolor y 50 virginica. No contiene valores ausentes.')
    p('Pregunta: ¿cómo se relacionan la longitud y la anchura del pétalo, y permiten distinguir visualmente las especies? El análisis es descriptivo; no entrena ni evalúa un clasificador.')
    p('Fuente y procedimiento','Heading2')
    p('Entrada: datos/iris/iris.csv, junto a las soluciones de ML. Se carga con Orange.data.Table y se envía a los widgets reales Scatter Plot y Distributions de Orange 3.40. Las ventanas se muestran en Wayland y se capturan mediante QWidget.grab(): las imágenes siguientes contienen la interfaz Orange y sus datos, no recreaciones gráficas.')
    p('En Scatter Plot: X=petal_length, Y=petal_width, color=iris. En Distributions: variable=petal_length y split by=iris. Las magnitudes originales están en cm; no se aplica normalización.')
    rows=[['Especie','Muestras','Longitud media (cm)','Anchura media (cm)']]
    for name,v in m['classes'].items(): rows.append([name,str(v['n']),f"{v['petal_length_mean_cm']:.3f}",f"{v['petal_width_mean_cm']:.3f}"])
    table=Table(rows,colWidths=[3.4*cm,2.2*cm,5.1*cm,5.1*cm])
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e2e8f0')),('GRID',(0,0),(-1,-1),0.4,colors.grey),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    story.extend([Spacer(1,.3*cm),table])
    p('Las medias se calculan directamente sobre las 50 observaciones de cada especie; no son predicciones. El resumen JSON conserva el tamaño de muestra y el hash de la fuente.')
    story.append(PageBreak())
    p('2. Desarrollo: dispersión de pétalos','Heading1')
    image('orange_scatter.png',16.2*cm)
    p('Figura 1. Captura del widget Scatter Plot real con las 150 muestras. Las dos variables son longitud y anchura del pétalo, en centímetros.')
    p('Setosa forma un grupo con pétalos pequeños, claramente separado en esta proyección. Versicolor y virginica ocupan valores mayores y presentan solapamiento: una separación visual no permite asegurar que una regla clasifique correctamente todas las flores.')
    p(f"La correlación de Pearson global es r={m['pearson_petal_length_width']:.3f}. Describe una asociación positiva en estas 150 flores. La mezcla de especies contribuye al patrón; el valor global no establece causalidad ni garantiza la misma relación dentro de cada especie.")
    story.append(PageBreak())
    p('2. Desarrollo: distribución por especie','Heading1')
    image('orange_distribucion.png',16.2*cm)
    p('Figura 2. Widget Distributions real, longitud del pétalo agrupada por especie. Las barras dependen del ancho de los intervalos; no representan por sí solas probabilidades de clasificación.')
    p('La distribución confirma los pétalos más pequeños de setosa y el solapamiento de versicolor con virginica. La media de longitud aumenta de 1,462 a 4,260 y 5,552 cm, respectivamente; resume cada grupo pero no sustituye su distribución.')
    p('3. Conclusiones','Heading1')
    p('Orange permite contrastar la tabla numérica con dos vistas complementarias. Las medidas del pétalo resultan informativas para distinguir especies en este dataset, especialmente setosa. Para versicolor y virginica persiste solapamiento; una práctica predictiva necesitaría un modelo y evaluación fuera de muestra.')
    p('Este ejercicio responde a una pregunta descriptiva con datos identificados y capturas verificables. No acredita generalización a otras poblaciones, ni resultados causales. No se ha enviado ninguna entrega a Moodle.')
    p('Reproducción y trazabilidad','Heading2')
    p('Ejecutar capturar_orange.py en el entorno Orange y sortu_pdf.py con ReportLab desde esta carpeta o la raíz. README.md incluye comandos, workflow y referencia a la tarea. Hash SHA-256 de entrada: '+m['sha256']+'.')
    def footer(canvas,doc):
        canvas.setFont('Helvetica',8)
        canvas.drawString(1.7*cm,1.1*cm,'Iris | 150 muestras | análisis descriptivo | capturas Orange')
        canvas.drawRightString(A4[0]-1.7*cm,1.1*cm,str(doc.page))
    SimpleDocTemplate(str(BASE/'Interpretacion_Datos_Orange.pdf'),pagesize=A4,leftMargin=1.7*cm,rightMargin=1.7*cm,topMargin=1.7*cm,bottomMargin=1.7*cm,title='Interpretación de datos: Iris en Orange').build(story,onFirstPage=footer,onLaterPages=footer)
    print(BASE/'Interpretacion_Datos_Orange.pdf')


if __name__=='__main__': main()
