"""Versión autónoma del informe, calculada desde las salidas de Jupyter."""

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE = Path(__file__).resolve().parent


def main():
    results = json.loads((BASE / "resultados.json").read_text())
    assert results["logreg"]["correct"] == 123 and results["knn"]["correct"] == 128
    styles = getSampleStyleSheet()
    styles["BodyText"].leading = 15
    styles["BodyText"].spaceAfter = 10
    styles.add(
        ParagraphStyle("SmallText", parent=styles["BodyText"], fontSize=9, leading=12)
    )
    story = []

    def p(text, style="BodyText"):
        story.append(Paragraph(text, styles[style]))

    def table(rows, widths):
        rows = [
            [Paragraph(str(value), styles["SmallText"]) for value in row]
            for row in rows
        ]
        obj = Table(rows, colWidths=widths, repeatRows=1)
        obj.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#64748b")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )
        story.extend([obj, Spacer(1, 0.4 * cm)])

    p("Iris: Regresión Logística frente a KNN", "Title")
    p("Unai Urzainqui Perez | 5072 | tarea 63325 | 5 de octubre de 2026", "SmallText")
    p("1. Objetivo y datos", "Heading1")
    p(
        "Comparar las fronteras de un modelo lineal y uno basado en vecinos. Iris contiene 150 flores, 50 setosa, 50 versicolor y 50 virginica. Se utilizan las primeras dos variables: longitud y anchura del sépalo, en centímetros. Las medidas del pétalo no entran en los modelos."
    )
    p(
        "El notebook completa la plantilla docente: carga de Iris, función de fronteras, Regresión Logística con max_iter=200, KNN con k=3, gráficos lado a lado y reflexión. Los datos se cargan desde scikit-learn, sin descargar CSV."
    )
    p("2. Método y resultados", "Heading1")
    p(
        "Se entrenan los modelos con las 150 flores y se evalúan con esas mismas filas, sin escalado. Las cifras describen entrenamiento; no son resultados de test o validación cruzada."
    )
    table(
        [
            ["Modelo", "Accuracy entrenamiento", "Aciertos / 150", "Frontera"],
            [
                "Regresión Logística",
                f"{results['logreg']['accuracy']:.4f}",
                123,
                "Lineal",
            ],
            ["KNN, k=3", f"{results['knn']['accuracy']:.4f}", 128, "Local e irregular"],
        ],
        [4.8 * cm, 4.7 * cm, 3.2 * cm, 4 * cm],
    )
    p(
        f"KNN tiene {results['knn']['correct'] - results['logreg']['correct']} aciertos más en entrenamiento (128 frente a 123). Eso no demuestra mejor rendimiento en flores nuevas. Los modelos tienen distinta flexibilidad y no se ha reservado una muestra de test."
    )
    story.append(PageBreak())
    p("3. Comparación visual", "Heading1")
    im = Image(str(BASE / "erabaki_mugak.png"))
    aspect = im.imageHeight / im.imageWidth
    im.drawWidth = 17 * cm
    im.drawHeight = im.drawWidth * aspect
    story.extend([im, Spacer(1, 0.4 * cm)])
    p(
        "Figura 1. Gráfico generado al ejecutar el notebook. Los puntos son clases observadas; el fondo muestra clases predichas en una malla. Ambos paneles tienen los mismos ejes. Color y forma distinguen las especies. No es un mapa de probabilidades.",
        "SmallText",
    )
    p("Preguntas de reflexión", "Heading2")
    p(
        "<b>Setosa:</b> ambos modelos aciertan las 50 setosa de esta muestra. Esa especie ocupa una región diferenciada del plano. Versicolor y virginica se solapan con estas medidas y no se separan perfectamente; no se asegura separación en flores nuevas."
    )
    p(
        "<b>Rectas y límites locales:</b> LogReg dibuja fronteras rectas en el plano; KNN se adapta a la distribución local de vecinos. La flexibilidad de KNN permite seguir puntos aislados, pero también lo hace más sensible al ruido."
    )
    p(
        "<b>k muy pequeño o grande:</b> con k=1 se espera más sensibilidad a puntos aislados y riesgo de sobreajuste. Con k=50 las fronteras se suavizan y pueden perder estructura, aumentando el riesgo de subajuste. Esta reflexión es hipotética: la ejecución utiliza solamente k=3."
    )
    story.append(PageBreak())
    p("4. Comprobación de resultados", "Heading1")
    p(
        "Las filas de las matrices son clases observadas; las columnas son predicciones. Orden: setosa, versicolor y virginica. Cada matriz suma 150 y su diagonal reproduce los aciertos de la tabla."
    )
    for name, key in [("Regresión Logística", "logreg"), ("KNN, k=3", "knn")]:
        p(name, "Heading2")
        matrix = results[key]["confusion_matrix"]
        table(
            [["Real / predicha", "setosa", "versicolor", "virginica"]]
            + [
                [label, *row]
                for label, row in zip(["setosa", "versicolor", "virginica"], matrix)
            ],
            [5.7 * cm, 3.7 * cm, 3.7 * cm, 3.7 * cm],
        )
    p("5. Conclusiones y reproducción", "Heading1")
    p(
        "La comparación ilustra dos formas de representar los mismos datos: una separación lineal sencilla y fronteras locales más flexibles. La mayor accuracy de entrenamiento de KNN no decide qué modelo generaliza mejor. Para comprobarlo haría falta holdout o CV y aprender cualquier transformación dentro de cada entrenamiento."
    )
    p(
        "Archivos: iris_logreg_knn.ipynb (código y salidas), txostena_beteta.md (informe), erabaki_mugak.png (figura) y resultados.json (matrices y versiones). README.md explica cómo ejecutar desde un kernel limpio. El PDF acompaña al notebook y no lo sustituye.",
        "SmallText",
    )
    p(
        "Fuente docente: tarea Moodle 63325, plantillas ikaskuntza_gainbegiratua_ikaslea.ipynb y txostena_ikaslea.md. Dataset: sklearn.datasets.load_iris(), colección de tres especies de Iris.",
        "SmallText",
    )

    def footer(canvas, document):
        canvas.setFont("Helvetica", 8)
        canvas.drawString(
            1.7 * cm,
            1.05 * cm,
            "5072 | Iris | dos medidas del sépalo | evaluación de entrenamiento",
        )
        canvas.drawRightString(A4[0] - 1.7 * cm, 1.05 * cm, str(document.page))

    out = BASE / "Informe_LogReg_KNN.pdf"
    SimpleDocTemplate(
        str(out),
        pagesize=A4,
        leftMargin=1.7 * cm,
        rightMargin=1.7 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.7 * cm,
        title="Iris: Regresión Logística frente a KNN",
    ).build(story, onFirstPage=footer, onLaterPages=footer)
    print(out)


if __name__ == "__main__":
    main()
