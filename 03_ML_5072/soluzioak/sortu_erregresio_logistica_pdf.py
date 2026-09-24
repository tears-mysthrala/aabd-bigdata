"""Build the WDBC one-feature logistic-regression assignment report."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

AUTHOR = "Unai Urzainqui Perez"
HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "datos" / "breast_cancer_wisconsin"
IMAGE_DIR = HERE / "irudiak"
PDF_PATH = HERE / "Orange_Regresion_Logistica_Entregable.pdf"
METRICS = json.loads((DATA_DIR / "wdbc_cv_metricas.json").read_text(encoding="utf-8"))
with (DATA_DIR / "wdbc_cv_predicciones.csv").open(encoding="utf-8", newline="") as f:
    PREDICTIONS = list(csv.DictReader(f))

NAVY=colors.HexColor("#17324D"); BLUE=colors.HexColor("#2878B5"); PALE=colors.HexColor("#EFF4F7")
INK=colors.HexColor("#263746"); MUTED=colors.HexColor("#52616B")


def build_pdf() -> None:
    doc=SimpleDocTemplate(str(PDF_PATH),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=16*mm,bottomMargin=17*mm,title="Regresión logística univariable - UCI Wisconsin Breast Cancer Diagnostic",author=AUTHOR,subject="Orange Data Mining: maligno o benigno usando texture_mean")
    doc.creator="Orange Data Mining 3.40 · ReportLab"
    doc.keywords="UCI WDBC, Wisconsin Breast Cancer Diagnostic, regresión logística, Unai Urzainqui Perez"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="RTitle",parent=styles["Title"],fontName="Helvetica-Bold",fontSize=20,leading=23,textColor=NAVY,alignment=TA_CENTER,spaceAfter=6))
    styles.add(ParagraphStyle(name="Sub",parent=styles["Normal"],fontSize=9,leading=12,textColor=MUTED,alignment=TA_CENTER,spaceAfter=5))
    styles.add(ParagraphStyle(name="Sect",parent=styles["Heading2"],fontName="Helvetica-Bold",fontSize=13,leading=15,textColor=NAVY,spaceBefore=5,spaceAfter=5,keepWithNext=True))
    styles.add(ParagraphStyle(name="SubSect",parent=styles["Heading3"],fontName="Helvetica-Bold",fontSize=10,leading=12,textColor=BLUE,spaceBefore=4,spaceAfter=3,keepWithNext=True))
    styles.add(ParagraphStyle(name="Body9",parent=styles["BodyText"],fontName="Helvetica",fontSize=8.6,leading=11.2,textColor=INK,spaceAfter=4))
    styles.add(ParagraphStyle(name="Small8",parent=styles["BodyText"],fontName="Helvetica",fontSize=7.4,leading=9,textColor=MUTED,spaceAfter=3))
    styles.add(ParagraphStyle(name="Cell",parent=styles["BodyText"],fontName="Helvetica",fontSize=7.6,leading=9,textColor=INK))
    styles.add(ParagraphStyle(name="CellHead",parent=styles["BodyText"],fontName="Helvetica-Bold",fontSize=7.5,leading=9,textColor=colors.white))
    body,small=styles["Body9"],styles["Small8"]
    story=[
        Spacer(1,3*mm),Paragraph("Orange Data Mining: regresión logística",styles["RTitle"]),
        Paragraph("Wisconsin Breast Cancer Diagnostic - benigno o maligno",styles["Sub"]),
        Paragraph(f"<b>Creador:</b> {AUTHOR} &nbsp;&nbsp; <b>Herramienta:</b> Orange Data Mining 3.40",styles["Sub"]),
        Paragraph("1. Datos elegidos",styles["Sect"]),
        Paragraph(
            "Uso el conjunto <b>Breast Cancer Wisconsin (Diagnostic)</b> de UCI. Cada registro contiene medidas "
            "calculadas desde una imagen digital de una aspiración con aguja fina (FNA) de una masa mamaria. La etiqueta "
            "<b>B</b> significa benigno y <b>M</b> maligno. Hay 569 muestras: 357 benignas y 212 malignas, sin valores ausentes.",body),
        Paragraph(
            "Para que el ejemplo muestre mayor solapamiento entre clases, el modelo usa solo <b>texture_mean</b>: la media "
            "de la desviación estándar de los niveles de gris en la imagen del núcleo celular. Este predictor separa menos "
            "las clases que otras variables de WDBC. Las otras 29 características originales "
            "no entran en este modelo univariable.",body),
        Image(str(IMAGE_DIR/"logistica_clases.png"),width=145*mm,height=51*mm),
        Paragraph("Distribución de las etiquetas del conjunto UCI.",small),
        Paragraph("Workflow reproducible en Orange",styles["SubSect"]),
        Image(str(IMAGE_DIR/"logistica_workflow.png"),width=174*mm,height=38*mm),
        Paragraph("El archivo Orange conserva el identificador de muestra como meta, texture_mean como predictor y diagnosis como objetivo.",small),
        PageBreak(),
        Paragraph("2. Aplicación y evaluación del modelo",styles["Sect"]),
        Paragraph(
            "Ajusto una <b>regresión logística binaria</b> con regularización L2 (C=1). La probabilidad de malignidad "
            "se calcula como P(M|x) = 1 / (1 + exp(-(b0 + b1 x))), donde x es texture_mean. Orange estandariza el predictor "
            "dentro del aprendiz en cada partición y evalúa con validación cruzada estratificada de 10 folds, semilla 42. "
            "Las cifras siguientes usan predicciones fuera de muestra; la exactitud de entrenamiento no se usa como evaluación.",body),
        _metrics_table(styles),
        Paragraph(
            f"El AUC ROC de {METRICS['roc_auc']:.3f} indica que texture_mean ofrece una separación moderada entre las dos clases en esta "
            f"muestra. Con el corte 0,5, el recall de malignos es {METRICS['recall_malignant']:.1%}: algunos casos M no se "
            "detectan. La matriz de confusión y la curva de la página siguiente ayudan a ver ese intercambio.",body),
        Image(str(IMAGE_DIR/"logistica_curvas.png"),width=145*mm,height=94*mm),
        Paragraph("Curva ROC calculada con las probabilidades de validación cruzada, no con las del ajuste completo.",small),
        PageBreak(),
        Paragraph("3. Confianza asignada a cada muestra",styles["Sect"]),
        Paragraph(
            "Cada punto es una muestra real: X es su puntuación z=b0+b1·texture_mean calculada por el ajuste descriptivo "
            "y Y es su diagnóstico observado, exactamente B=0 o M=1. La curva azul muestra la probabilidad estimada "
            "P(M)=σ(z), siempre entre 0 y 1. Si z>0 (P(M)>0,5) el modelo predice M; si z<0 predice B. Las regiones "
            "coloreadas muestran esas dos decisiones y sus límites z=0, P(M)=0,5.",body),
        Image(str(IMAGE_DIR/"logistica_sigmoide_clasificacion.png"),width=174*mm,height=96*mm),
        Paragraph(
            "Los puntos son diagnósticos observados, no probabilidades predichas; por eso solo ocupan y=0 o y=1 y no "
            "siguen necesariamente la curva. No se añade jitter. La sigmoide representa el ajuste completo solo para "
            "explicar la función; el rendimiento se mide aparte mediante validación cruzada out-of-fold. El corte 0,5 "
            "es didáctico, no un umbral clínico.",body),
        Paragraph("texture_mean por sí sola deja muchos casos ambiguos y no es un buen clasificador diagnóstico.",small),
        PageBreak(),
        Paragraph("4. Salidas, análisis y conclusiones",styles["Sect"]),
        Paragraph("El CSV contiene sample_id, texture_mean, scores z y probabilidades del ajuste completo y out-of-fold, diagnóstico observado y clase predicha por validación cruzada. La matriz siguiente resume las predicciones CV:",body),
        Image(str(IMAGE_DIR/"logistica_confusion.png"),width=139*mm,height=102*mm),
        Paragraph("Cada celda indica el número de muestras y, debajo, el porcentaje dentro de su clase observada.",small),
        _confusion_table(styles),
        Paragraph(
            f"De {METRICS['class_counts']['M (malignant)']} muestras malignas, el modelo deja {METRICS['confusion_matrix']['fn_malignant_as_benign']} "
            f"como benignas; además, {METRICS['confusion_matrix']['fp_benign_as_malignant']} benignas se clasifican como malignas. "
            "El predictor único permite explicar el mecanismo de la regresión logística, pero tiene señal limitada y pierde información que "
            "está en las otras características.",body),
        Paragraph("Conclusiones y límites",styles["SubSect"]),
        Paragraph(
            "La relación entre texture_mean y la etiqueta B/M ofrece un ejemplo visual de clasificación logística con solapamiento entre clases. "
            "El conjunto contiene mediciones históricas de una colección concreta, no una muestra clínica universal. "
            "El modelo es exclusivamente educativo: no sirve para diagnosticar, descartar cáncer ni orientar decisiones "
            "de pacientes. Una aplicación real exigiría datos clínicos adecuados, validación externa, análisis de sesgos "
            "y supervisión profesional.",body),
        Paragraph(
            "Fuente: Wolberg, Mangasarian, Street y Street (1993), <a href='https://archive.ics.uci.edu/dataset/17/breast%2Bcancer' color='#2878B5'>"
            "UCI Breast Cancer Wisconsin (Diagnostic)</a>, DOI <a href='https://doi.org/10.24432/C5DW2B' color='#2878B5'>10.24432/C5DW2B</a>, "
            "licencia CC BY 4.0. Los datos originales, tabla Orange, scripts, predicciones y métricas acompañan al entregable.",small),
    ]
    def decorate(canvas,document):
        canvas.saveState(); width,_=A4; canvas.setFillColor(MUTED); canvas.setFont("Helvetica",7.5)
        canvas.drawString(18*mm,10*mm,f"{AUTHOR} · UCI WDBC · Orange Data Mining")
        canvas.drawRightString(width-18*mm,10*mm,f"Página {document.page}")
        canvas.setStrokeColor(colors.HexColor("#D9E2E8")); canvas.line(18*mm,14*mm,width-18*mm,14*mm); canvas.restoreState()
    doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
    print(f"Created {PDF_PATH}")


def _table(data,col_widths,styles):
    cells=[[Paragraph(str(v),styles["CellHead"] if r==0 else styles["Cell"]) for v in row] for r,row in enumerate(data)]
    return Table(cells,colWidths=col_widths,repeatRows=1,style=TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("BACKGROUND",(0,1),(-1,-1),PALE),
        ("GRID",(0,0),(-1,-1),.4,colors.HexColor("#CBD5E0")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))


def _metrics_table(styles):
    rows=[
        ["Métrica (CV 10-fold)","Resultado","Lectura"],
        ["Accuracy",f"{METRICS['accuracy']:.1%}","Fracción total correcta"],
        ["Balanced accuracy",f"{METRICS['balanced_accuracy']:.1%}","Media del recall de B y M"],
        ["AUC ROC",f"{METRICS['roc_auc']:.3f}","Ordenación B/M fuera de muestra"],
        ["Precision maligno",f"{METRICS['precision_malignant']:.1%}","Predicciones M que son M"],
        ["Recall maligno",f"{METRICS['recall_malignant']:.1%}","Muestras M detectadas"],
        ["F1 maligno",f"{METRICS['f1_malignant']:.3f}","Media armónica precision/recall"],
    ]
    return _table(rows,[40*mm,30*mm,95*mm],styles)


def _confusion_table(styles):
    cm=METRICS["confusion_matrix"]
    rows=[["","Predicho B","Predicho M"],["Real B",f"TN {cm['tn_benign']}",f"FP {cm['fp_benign_as_malignant']}"],["Real M",f"FN {cm['fn_malignant_as_benign']}",f"TP {cm['tp_malignant']}"]]
    return _table(rows,[38*mm,52*mm,52*mm],styles)


if __name__=="__main__":
    build_pdf()
