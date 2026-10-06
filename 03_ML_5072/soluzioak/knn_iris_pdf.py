#!/usr/bin/env python3
"""Build the KNN report from measured JSON and plots (requires reportlab)."""
from pathlib import Path
import json
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

ROOT = Path(__file__).resolve().parent


def main():
    m = json.loads((ROOT / "datos/iris/knn_iris.json").read_text())
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Caption", fontSize=9, leading=12, textColor=colors.HexColor("#475569"), alignment=TA_CENTER, spaceAfter=10))
    styles["BodyText"].leading = 15
    styles["BodyText"].spaceAfter = 9
    story = []
    def p(text, style="BodyText"):
        story.append(Paragraph(text, styles[style]))
    p("KNN con Iris", "Title")
    p("Evaluación reproducible con Orange | 5072 | assign 63321", "Caption")
    p("Objetivo y método", "Heading2")
    p("Evaluar KNN fuera de muestra manteniendo la relación entre cada flor, sus cuatro medidas, su etiqueta real y la predicción. Iris contiene 150 muestras y tres clases equilibradas (50 por clase).")
    proto = m["protocol"]
    p(f"KNN k={m['k']}, distancia {proto['metric']}, votos uniformes y cuatro atributos sin escalado. Validación cruzada estratificada de {proto['folds']} folds con mezcla y semilla {proto['random_state']}. Cada muestra se evalúa una sola vez con un modelo entrenado en otras filas.")
    p("Los preprocesadores predeterminados de Orange se ajustan dentro de cada fold: HasClass, Continuize, RemoveNaNColumns y SklImpute. El CSV no contiene valores ausentes.")
    p("Resultados calculados", "Heading2")
    p(f"<b>CA = {m['CA']:.4f}: {m['correct']}/{m['samples']} aciertos.</b> F1 macro = {m['classification_report']['macro avg']['f1-score']:.4f}. Los seis errores confunden versicolor y virginica; setosa no presenta errores en esta partición.")
    table = Table([["Real / predicha", *m["labels"]], *[[label, *row] for label, row in zip(m["labels"], m["CM"])]], colWidths=[4.2*cm, 3.1*cm, 3.1*cm, 3.1*cm])
    table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e2e8f0")), ("GRID", (0,0), (-1,-1), .5, colors.HexColor("#94a3b8")), ("ALIGN", (1,1), (-1,-1), "CENTER"), ("BOTTOMPADDING", (0,0), (-1,-1), 9), ("TOPPADDING", (0,0), (-1,-1), 9)]))
    story.extend([table, Spacer(1, .3*cm)])
    p("Corrección del exportado", "Heading2")
    p("El CSV anterior tenía 90 etiquetas reales incompatibles con las medidas de su fila. Los resultados de Orange se agrupan por folds. El script ahora usa results.row_indices para colocar predicción, probabilidad y fold en el orden original. También comprueba results.actual frente a las etiquetas de esas filas.")
    p("Después de escribir el CSV se vuelve a leer y se verifica cada identificador, medida, etiqueta y acierto. La entrada coincide exactamente con sklearn.datasets.load_iris(). Resultado: <b>0/150 etiquetas desalineadas</b>; todos los folds se verifican con StratifiedKFold, sin cruce entre entrenamiento y evaluación de un mismo fold.")
    story.append(PageBreak())
    p("Evidencia gráfica de la ejecución", "Title")
    story.append(Image(str(ROOT / "irudiak/knn_iris_confusion.png"), width=15.4*cm, height=11*cm))
    p("Figura 1. Matriz calculada con las 150 predicciones fuera de muestra. Filas reales y columnas predichas.", "Caption")
    story.append(Image(str(ROOT / "irudiak/knn_iris_errores.png"), width=16*cm, height=10*cm))
    p("Figura 2. Etiquetas reales en dos medidas del pétalo y errores OOF marcados. Los números son row_id (posición original, 1 a 150). El modelo utiliza cuatro medidas: esta proyección no representa su frontera completa ni demuestra la causa de los errores.", "Caption")
    story.append(PageBreak())
    p("Reproducción, interpretación y límites", "Title")
    p("Ejecución desde la raíz del repositorio", "Heading2")
    p("1. Ejecutar knn_iris_reproducir.py con Python del entorno Orange instalado. 2. Ejecutar knn_iris_pdf.py con reportlab. Los comandos exactos están en Orange_KNN_Iris.md. Ambos scripts residen en 03_ML_5072/soluzioak/.")
    p("El primer script escribe datos/iris/iris_knn_predicciones.csv, datos/iris/knn_iris.json e irudiak/knn_iris_*.png. El segundo reconstruye este PDF con esos resultados. El CSV de entrada no se modifica.")
    p("Trazabilidad", "Heading2")
    versions = "; ".join(f"{key} {value}" for key,value in m["versions"].items())
    p("Ejecución local: 2 de octubre de 2026. " + versions + ".")
    p("El JSON conserva la configuración, las versiones, la matriz, el informe de clasificación y los hashes SHA-256 de entrada y predicciones. row_id identifica la fila fuente y fold la partición. Las columnas p_setosa, p_versicolor y p_virginica contienen probabilidades OOF.")
    p("Filas con error: " + ", ".join(map(str,m["error_row_ids"])) + ".")
    p("Workflow de Orange", "Heading2")
    p("Orange_KNN_Iris.ows conecta File y kNN a Test &amp; Score, y sus resultados a Confusion Matrix y Data Table. Se corrige la clase del widget a OWKNNLearner y n_folds=3 (índice de 10 folds en Orange 3.40). Si File no resuelve la ruta, escoger datos/iris/iris.csv desde soluzioak y confirmar iris como clase.")
    p("Qué se ha validado", "Heading2")
    p("Ejecución real de la API de Orange, correspondencia de datos con scikit-learn, exportado releído, cobertura de cada fila y folds, métricas calculadas y PDF renderizado. Las figuras son gráficos generados por código; <b>no son capturas de la GUI</b>. No se afirma ejecución interactiva del workflow.")
    p("Alcance de las conclusiones", "Heading2")
    p("La CA previa 0,9533 y las comparaciones de otros k quedan sustituidas por esta evaluación k=3. No se selecciona un nuevo hiperparámetro. La CV mide este protocolo y estas versiones; no acredita rendimiento en datos externos. La práctica visual Iris_LogReg_KNN usa dos atributos y accuracy de entrenamiento, por lo que sus resultados no son comparables directamente.")
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#475569"))
        canvas.drawString(2*cm, 1.2*cm, "KNN Iris | API Orange | CV estratificada | semilla 42")
        canvas.drawRightString(A4[0]-2*cm, 1.2*cm, str(doc.page))
        canvas.restoreState()
    doc = SimpleDocTemplate(str(ROOT / "Orange_KNN_Iris.pdf"), pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1.7*cm, bottomMargin=1.8*cm, title="KNN Iris: evaluación reproducible", author="AABD")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(ROOT / "Orange_KNN_Iris.pdf")


if __name__ == "__main__":
    main()
