"""Informe académico a partir de métricas y capturas nativas ya verificadas."""
import json
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

BASE = Path(__file__).resolve().parents[1]
FONT = Path('/usr/share/fonts/TTF/DejaVuSans.ttf')
BOLD = Path('/usr/share/fonts/TTF/DejaVuSans-Bold.ttf')
if FONT.exists() and BOLD.exists():
    pdfmetrics.registerFont(TTFont('Report', str(FONT)))
    pdfmetrics.registerFont(TTFont('ReportBold', str(BOLD)))
    normal, bold = 'Report', 'ReportBold'
else:
    normal, bold = 'Helvetica', 'Helvetica-Bold'

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='ReportBody', fontName=normal, fontSize=10, leading=14,
                          spaceAfter=8, textColor=colors.HexColor('#203041')))
styles.add(ParagraphStyle(name='ReportTitle', fontName=bold, fontSize=21, leading=26,
                          spaceAfter=10, textColor=colors.HexColor('#173d56')))
styles.add(ParagraphStyle(name='ReportHeading', fontName=bold, fontSize=13, leading=18,
                          spaceBefore=8, spaceAfter=9, textColor=colors.HexColor('#173d56')))
styles.add(ParagraphStyle(name='Caption', fontName=normal, fontSize=8, leading=11,
                          spaceBefore=5, spaceAfter=10, textColor=colors.HexColor('#43505b')))
styles.add(ParagraphStyle(name='SmallReport', fontName=normal, fontSize=9, leading=12, spaceAfter=7))


def para(text, style='ReportBody'):
    return Paragraph(text, styles[style])


def table(data, widths=None):
    data = [[para(str(cell), 'SmallReport') for cell in row] for row in data]
    result = Table(data, colWidths=widths, hAlign='LEFT')
    result.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e6eef4')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f7f9')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, 0), 0.6, colors.HexColor('#9fb5c5')),
    ]))
    return result


def figure(name, caption):
    return [Image(str(BASE / 'capturas' / name), width=505, height=505*820/1200),
            para(caption, 'Caption')]


def fmt(number, digits=2):
    return f'{number:.{digits}f}'.replace('.', ',')


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#ccd6df'))
    canvas.line(45, 38, 550, 38)
    canvas.setFont(normal, 8)
    canvas.setFillColor(colors.HexColor('#556372'))
    canvas.drawString(45, 25, 'Unai Urzainqui Perez | Interpretación de datos con Orange | AI4I 2020')
    canvas.drawRightString(550, 25, str(doc.page))
    canvas.restoreState()


def main():
    metrics = json.loads((BASE / 'evidencias/estadisticas.json').read_text())
    gui = json.loads((BASE / 'evidencias/orange_gui.json').read_text())
    assert metrics['rows'] == gui['rows'] == gui['scatter_points'] == 10000
    assert metrics['failure_count'] == gui['failure_count'] == 339
    story = [para('Interpretación de AI4I 2020<br/>con Orange', 'ReportTitle'),
             para('<b>Trabajo individual</b> · Unai Urzainqui Perez · 5 de octubre de 2026', 'SmallReport'),
             para('1. Introducción', 'ReportHeading'),
             para('El objetivo es seleccionar un conjunto de datos, representarlo en Orange e interpretar '
                  'los gráficos con apoyo de estadísticas. Se analiza AI4I 2020, un conjunto <b>sintético</b> '
                  'de mantenimiento predictivo publicado en UCI. No son mediciones recogidas en una planta real.'),
             para('Se estudia la relación entre <b>Rotational speed [rpm]</b> (velocidad de giro), '
                  '<b>Torque [Nm]</b> (par o momento de fuerza) y <b>Machine failure</b> '
                  '(0 = sin fallo; 1 = fallo). La pregunta es en qué zonas del gráfico se observan más fallos.'),
             table([['Comprobación del archivo oficial', 'Resultado'],
                    ['Registros / columnas / valores vacíos', '10.000 / 14 / 0'],
                    ['Sin fallo / con fallo', '9.661 / 339 (3,39 %)']], [325, 180]),
             para('2. Desarrollo: carga de los datos', 'ReportHeading')]
    story += figure('01_file.png', 'Figura 1. Captura real de File en Orange 3.40.0: 10.000 instancias, '
                    '6 atributos, 1 clase y 7 metadatos; en total se conservan las 14 columnas.')
    story += [para('El archivo .tab adjunto conserva las filas y los valores del CSV oficial; añade tres '
                   'líneas de cabecera para declarar tipos y roles. Machine failure se configura como clase '
                   'categórica. UDI, Product ID y los cinco indicadores de fallo quedan como metadatos.', 'SmallReport'),
              PageBreak(), para('2. Desarrollo: velocidad y par', 'ReportHeading'),
              para('En el flujo <b>File → Scatter Plot</b>, X es Rotational speed [rpm] e Y es Torque [Nm]. '
                   'El color y la forma muestran Machine failure. Se representan las 10.000 filas, sin '
                   'desplazamiento aleatorio de los puntos ni selección de una muestra.')]
    story += figure('02_scatter_speed_torque.png', 'Figura 2. Scatter Plot real. Los círculos azules corresponden a 0 '
                    '(sin fallo) y las cruces rojas a 1 (fallo). Un mismo lugar puede contener varios registros superpuestos.')
    story += [para('La nube desciende: a mayor velocidad se observa generalmente menor par. La correlación '
                   f'lineal de Pearson es <b>r = {fmt(metrics["pearson_speed_torque"], 3)}</b>, aunque la curva '
                   'no es una recta. Las cruces aparecen sobre todo en la zona de baja velocidad y par elevado; '
                   'también existen fallos en el extremo de alta velocidad y par bajo.'),
              para('Para cuantificar la lectura visual se agrupan las filas en tres intervalos descriptivos. '
                   'La tasa es fallos / registros de cada intervalo; los límites se han elegido para resumir '
                   'el gráfico y no son umbrales de seguridad ni de un modelo predictivo.', 'SmallReport')]
    bins = metrics['speed_bins']
    story += [table([['Velocidad (rpm)', 'Registros', 'Fallos', 'Tasa de fallo'],
                     ['Menor que 1.400', str(bins[0]['count']), str(bins[0]['failures']), fmt(bins[0]['failure_percent'])+' %'],
                     ['De 1.400 a 1.800, incluidos', str(bins[1]['count']), str(bins[1]['failures']), fmt(bins[1]['failure_percent'])+' %'],
                     ['Mayor que 1.800', str(bins[2]['count']), str(bins[2]['failures']), fmt(bins[2]['failure_percent'])+' %']],
                    [260, 85, 65, 95]),
              PageBreak(), para('2. Desarrollo: distribución y comparación', 'ReportHeading'),
              para('En <b>File → Distributions</b> se selecciona Torque [Nm], se separan las barras por '
                   'Machine failure y se fija una anchura de intervalo de 5 Nm. El eje vertical muestra '
                   'frecuencias absolutas, no porcentajes ni probabilidades de fallo.')]
    story += figure('03_distributions_torque.png', 'Figura 3. Widget Distributions real. La clase 0 domina '
                    'el número de registros; la menor altura de la clase 1 también refleja el desequilibrio 9.661 frente a 339.')
    groups = metrics['groups']
    speed = 'Rotational speed [rpm]'
    torque = 'Torque [Nm]'
    wear = 'Tool wear [min]'
    rows = [['Estadística recalculada', 'Sin fallo (n = 9.661)', 'Con fallo (n = 339)']]
    for label, variable, stat in [('Velocidad media (rpm)', speed, 'mean'),
                                 ('Velocidad mediana (rpm)', speed, 'median'),
                                 ('Par medio (Nm)', torque, 'mean'),
                                 ('Par mediano (Nm)', torque, 'median'),
                                 ('Desgaste medio (min)', wear, 'mean')]:
        rows.append([label, fmt(groups['0'][variable][stat]), fmt(groups['1'][variable][stat])])
    story += [table(rows, [230, 138, 137]), Spacer(1, 8),
              para('El par medio es mayor en los registros con fallo (50,17 frente a 39,63 Nm), y la mediana '
                   'confirma ese desplazamiento. Sin embargo, los grupos se solapan: también hay fallos con par '
                   'bajo. La diferencia entre la velocidad media y mediana del grupo con fallo indica que '
                   'sus valores altos afectan al promedio.'),
              PageBreak(), para('3. Conclusiones', 'ReportHeading'),
              para('<b>Relación observada.</b> Velocidad y par presentan una asociación negativa fuerte '
                   '(r = -0,875). Las dos variables permiten reconocer zonas donde la proporción de fallo '
                   'es distinta, pero un punto rojo o azul no ofrece por sí solo una explicación completa.'),
              para('<b>Fallos y comparación.</b> El 3,39 % de los registros está etiquetado como fallo. '
                   'La tasa observada es 12,78 % por debajo de 1.400 rpm, 0,89 % entre 1.400 y 1.800 rpm '
                   'y 5,08 % por encima de 1.800 rpm. Por tanto, la menor frecuencia de barras rojas debe '
                   'interpretarse teniendo en cuenta el número de registros de cada grupo.'),
              para('<b>Límite del análisis.</b> Estos resultados describen el conjunto adjunto. El dataset '
                   'se generó de forma sintética mediante relaciones y reglas de fallo. La asociación '
                   'no demuestra que modificar una variable cause una avería ni que estos porcentajes '
                   'representen el riesgo de una máquina real.'),
              para('<b>Alcance.</b> No se ha entrenado un clasificador ni calculado su capacidad predictiva. '
                   'Las temperaturas y el desgaste podrían ampliar el análisis descriptivo. Para una '
                   'aplicación industrial harían falta datos reales y una validación adecuada.'),
              para('Cómo comprobar el trabajo', 'ReportHeading'),
              para('El paquete incluye el CSV oficial, su versión .tab para Orange, '
                   '<b>Interpretacion_AI4I.ows</b>, las tres capturas originales y scripts reproducibles. '
                   'Para repetir la visualización se abre el flujo con Orange conservando la carpeta datos '
                   'junto al archivo .ows. Las estadísticas provienen de las 10.000 filas completas; '
                   'no se han inferido a partir de los píxeles de las imágenes.'),
              para('Fuentes', 'ReportHeading'),
              para('UCI Machine Learning Repository. <i>AI4I 2020 Predictive Maintenance Dataset</i> (2020). '
                   'Datos sintéticos y documentación del conjunto. DOI: '
                   '<link href="https://doi.org/10.24432/C5HS5C" color="#175c84">10.24432/C5HS5C</link>. '
                   'Licencia CC BY 4.0. Consultado el 5 de octubre de 2026.', 'SmallReport'),
              para('<link href="https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset" '
                   'color="#175c84">Ficha oficial UCI y descarga del dataset</link>. '
                   'Orange Data Mining: <link href="https://orangedatamining.com/widget-catalog/visualize/scatterplot/" '
                   'color="#175c84">Scatter Plot</link> y '
                   '<link href="https://orangedatamining.com/widget-catalog/visualize/distributions/" '
                   'color="#175c84">Distributions</link>.', 'SmallReport'),
              para('Las figuras 1-3 son capturas de widgets nativos de Orange 3.40.0 mostrados en pantalla '
                   'el 5 de octubre de 2026. Las métricas se han recalculado desde el archivo oficial.', 'Caption')]
    target = BASE / 'AI4I_Interpretacion_Orange.pdf'
    document = SimpleDocTemplate(str(target), pagesize=A4, rightMargin=45, leftMargin=45,
                                 topMargin=35, bottomMargin=50, title='Interpretación de AI4I 2020 con Orange',
                                 author='Unai Urzainqui Perez', subject='Trabajo individual: visualización e interpretación')
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(target)


if __name__ == '__main__':
    main()
