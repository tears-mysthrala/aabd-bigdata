"""Build the reviewed Auto MPG linear-regression assignment PDF."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)


AUTHOR = "Unai Urzainqui Perez"
HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "datos" / "auto_mpg"
PDF_PATH = HERE / "Orange_Erregresio_Lineala_Entregagarria.pdf"
METRICS = json.loads((DATA_DIR / "auto_mpg_cv_metrics.json").read_text(encoding="utf-8"))
with (DATA_DIR / "auto_mpg_weight.tab").open(encoding="utf-8") as tab:
    next(tab)
    next(tab)
    next(tab)
    DATA_ROWS = [line.rstrip("\n").split("\t") for line in tab]
WEIGHTS = [float(row[1]) for row in DATA_ROWS]
MPG_VALUES = [float(row[0]) for row in DATA_ROWS]
ROWS = list(csv.DictReader((DATA_DIR / "auto_mpg_cv_iragarpenak.csv").open(encoding="utf-8")))

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2878B5")
ORANGE = colors.HexColor("#E1812C")
PALE = colors.HexColor("#EFF4F7")
INK = colors.HexColor("#263746")
MUTED = colors.HexColor("#52616B")


def build_pdf() -> None:
    doc = SimpleDocTemplate(
        str(PDF_PATH), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm, title="Regresión lineal con UCI Auto MPG",
        author=AUTHOR, subject="Orange Data Mining: regresión lineal simple mpg ~ weight",
    )
    doc.author = AUTHOR
    doc.creator = "Orange Data Mining 3.40 · ReportLab"
    doc.keywords = "UCI Auto MPG, Orange Data Mining, regresión lineal, Unai Urzainqui Perez"

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=21,
        leading=25, textColor=NAVY, alignment=TA_CENTER, spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        name="SubTitle", parent=styles["Normal"], fontName="Helvetica", fontSize=10,
        leading=14, textColor=MUTED, alignment=TA_CENTER, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=14,
        leading=17, textColor=NAVY, spaceBefore=5, spaceAfter=6, keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name="SubSection", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=10.5,
        leading=13, textColor=BLUE, spaceBefore=6, spaceAfter=4, keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name="Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5,
        leading=13.3, textColor=INK, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="Small", parent=styles["BodyText"], fontName="Helvetica", fontSize=8,
        leading=10.5, textColor=MUTED, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="Cell", parent=styles["BodyText"], fontName="Helvetica", fontSize=8,
        leading=10, textColor=INK,
    ))
    styles.add(ParagraphStyle(
        name="CellHeader", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8,
        leading=10, textColor=colors.white,
    ))

    body = styles["Body"]
    small = styles["Small"]
    story = [
        Spacer(1, 8 * mm),
        Paragraph("Orange Data Mining: regresión lineal", styles["ReportTitle"]),
        Paragraph("UCI Auto MPG · peso del vehículo y consumo urbano", styles["SubTitle"]),
        Paragraph(f"<b>Creador:</b> {AUTHOR} &nbsp;&nbsp; <b>Software:</b> Orange Data Mining 3.40", styles["SubTitle"]),
        Spacer(1, 3 * mm),
        Paragraph("1. Datos elegidos", styles["Section"]),
        Paragraph(
            "Uso Auto MPG, conjunto publicado por UCI para tareas de regresión. Contiene 398 coches "
            "de los años modelo 1970-1982; el objetivo original es el consumo urbano en millas por galón. "
            "Para este ejercicio selecciono <b>weight</b> (peso, libras) como predictor y <b>mpg</b> "
            "como objetivo. Así estudio una relación concreta y puedo interpretar la pendiente con unidades.", body,
        ),
        Paragraph(
            "Conservo las 398 filas. Los seis valores ausentes de horsepower no afectan porque esa variable "
            "no entra en este modelo. Excluyo car_name porque identifica el coche y no es una medida numérica "
            "adecuada para esta regresión. La tabla de Orange y el CSV de predicciones mantienen la trazabilidad.", body,
        ),
        _summary_table(styles),
        Spacer(1, 4 * mm),
        Paragraph("Flujo de trabajo aplicado en Orange", styles["SubSection"]),
        Image(str(HERE / "irudiak" / "reg_workflow.png"), width=174 * mm, height=54 * mm),
        Paragraph(
            "La fuente de datos es el archivo relativo <font name='Courier'>datos/auto_mpg/auto_mpg_weight.tab</font>; "
            "el flujo se puede abrir sin depender de una ruta privada del equipo creador.", small,
        ),
        PageBreak(),
        Paragraph("2. Modelo y evaluación", styles["Section"]),
        Paragraph(
            "Aplico <b>regresión lineal simple por mínimos cuadrados ordinarios (OLS)</b>: "
            "<font name='Courier'>mpg = b + w × weight</font>. Orange evalúa el modelo con validación cruzada "
            "de 10 particiones y semilla 42. Las métricas principales se calculan con predicciones fuera de "
            "muestra (cada coche se predice desde un modelo ajustado sin ese coche). La ecuación descriptiva "
            "se ajusta una vez sobre las 398 filas completas; no se usan sus errores de entrenamiento como "
            "métrica de generalización.", body,
        ),
        _metrics_table(styles),
        Paragraph(
            f"La recta ajustada a todos los datos es <b>mpg = {METRICS['full_data_intercept_mpg']:.2f} "
            f"- {abs(METRICS['full_data_slope_mpg_per_pound']):.5f} × weight</b>. "
            f"La correlación de Pearson es r = {METRICS['pearson_r_weight_mpg']:.3f}. "
            f"En esta muestra, 1.000 libras más se asocian con aproximadamente "
            f"{abs(METRICS['full_data_slope_mpg_per_pound'])*1000:.2f} mpg menos, en promedio lineal.", body,
        ),
        Image(str(HERE / "irudiak" / "reg_scatter_ols.png"), width=166 * mm, height=101 * mm),
        Paragraph("La recta resume una tendencia media; la dispersión de los puntos muestra que el peso no explica por sí solo todo el consumo.", small),
        PageBreak(),
        Paragraph("3. Salidas y análisis", styles["Section"]),
        Paragraph(
            "El fichero <font name='Courier'>auto_mpg_cv_iragarpenak.csv</font> contiene una fila por coche: "
            "identificador, peso, consumo observado, predicción fuera de muestra y residuo (observado - predicho). "
            "El JSON complementario conserva las métricas completas. En validación cruzada, el error absoluto "
            f"medio es {METRICS['cv_mae']:.2f} mpg y el RMSE {METRICS['cv_rmse']:.2f} mpg. El percentil 95 del "
            f"error absoluto es {METRICS['cv_residual_95th_percentile_abs_mpg']:.2f} mpg, por lo que hay coches "
            "para los que la recta se equivoca bastante más que el promedio.", body,
        ),
        Image(str(HERE / "irudiak" / "reg_residuals.png"), width=174 * mm, height=80 * mm),
        Paragraph("Predicciones fuera de muestra (izquierda) y residuos CV según el peso (derecha). La línea ideal y el cero indican referencia, no ajuste adicional.", small),
        Paragraph("Ejemplos con mayor error absoluto", styles["SubSection"]),
        _largest_errors_table(styles),
        Paragraph("4. Conclusiones y límites", styles["Section"]),
        Paragraph(
            "<b>Conclusión:</b> en estos coches históricos, los vehículos más pesados tienden a registrar "
            "menos millas por galón. El modelo lineal con peso explica alrededor del "
            f"{METRICS['cv_r2']*100:.1f}% de la variación según validación cruzada. Su MAE de "
            f"{METRICS['cv_mae']:.2f} mpg lo hace útil para ilustrar una tendencia, pero los residuos y errores "
            "grandes muestran que no basta para describir bien cada vehículo.", body,
        ),
        Paragraph(
            "<b>Límites:</b> son datos urbanos antiguos de 1970-1982, no una muestra de coches actuales ni "
            "de todos los mercados. La asociación no demuestra que el peso por sí solo cause el cambio de consumo; "
            "motor, tecnología y año también pueden influir. El resultado es un ejercicio didáctico, no una "
            "herramienta para estimar vehículos actuales.", body,
        ),
        Paragraph(
            "<b>Procedencia:</b> R. Quinlan (1993), <a href='https://archive.ics.uci.edu/dataset/9/auto' color='#2878B5'>"
            "UCI Auto MPG</a>, DOI <a href='https://doi.org/10.24432/C5859H' color='#2878B5'>10.24432/C5859H</a>. "
            "Licencia CC BY 4.0 según UCI. Datos originales, transformación, workflow Orange, salida CSV y métricas "
            "JSON incluidos junto al entregable.", small,
        ),
        Paragraph(f"<b>Creador:</b> {AUTHOR}", small),
    ]

    def decorate(canvas, document) -> None:
        canvas.saveState()
        width, height = A4
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(18 * mm, 10 * mm, f"{AUTHOR} · UCI Auto MPG · Orange Data Mining")
        canvas.drawRightString(width - 18 * mm, 10 * mm, f"Página {document.page}")
        canvas.setStrokeColor(colors.HexColor("#D9E2E8"))
        canvas.line(18 * mm, 14 * mm, width - 18 * mm, 14 * mm)
        canvas.restoreState()

    doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
    print(f"Created {PDF_PATH}")


def _cell(text: str, styles):
    return Paragraph(text, styles["Cell"])


def _header(text: str, styles):
    return Paragraph(text, styles["CellHeader"])


def _summary_table(styles):
    data = [
        ["Observaciones", "Predictor", "Objetivo", "Peso", "Consumo"],
        ["398 coches", "weight", "mpg", f"{min(WEIGHTS):.0f}-{max(WEIGHTS):.0f} lb", f"{min(MPG_VALUES):.1f}-{max(MPG_VALUES):.1f} mpg"],
    ]
    return Table(
        [[_header(str(value), styles) if row_index == 0 else _cell(str(value), styles)
          for value in row] for row_index, row in enumerate(data)],
        colWidths=[34 * mm, 27 * mm, 27 * mm, 34 * mm, 39 * mm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, 1), PALE),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]),
    )


def _metrics_table(styles):
    rows = [
        ["Métrica (10-fold CV)", "Resultado", "Interpretación"],
        ["R²", f"{METRICS['cv_r2']:.3f}", "Variación explicada en predicción fuera de muestra"],
        ["RMSE", f"{METRICS['cv_rmse']:.2f} mpg", "Penaliza más los errores grandes"],
        ["MAE", f"{METRICS['cv_mae']:.2f} mpg", "Error absoluto medio"],
        ["MSE", f"{METRICS['cv_mse']:.2f} mpg²", "Error cuadrático medio"],
    ]
    return Table(
        [[_header(str(value), styles) if row_index == 0 else _cell(str(value), styles)
          for value in row] for row_index, row in enumerate(rows)],
        colWidths=[44 * mm, 32 * mm, 85 * mm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("BACKGROUND", (0, 1), (-1, -1), PALE),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]),
    )


def _largest_errors_table(styles):
    largest = sorted(ROWS, key=lambda row: abs(float(row["cv_residual"])), reverse=True)[:5]
    data = [["Coche", "Peso (lb)", "Observado mpg", "Predicho mpg", "Residuo mpg"]]
    for row in largest:
        data.append([
            row["car_name"], row["weight_lb"], row["mpg_observed"],
            row["mpg_cv_predicted"], row["cv_residual"],
        ])
    table = Table(
        [[_header(value, styles) if row_index == 0 else _cell(value, styles)
          for value in row] for row_index, row in enumerate(data)],
        colWidths=[60 * mm, 24 * mm, 29 * mm, 29 * mm, 26 * mm],
        repeatRows=1,
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, -1), PALE),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


if __name__ == "__main__":
    build_pdf()
