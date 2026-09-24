import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#7F8C8D"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(45, 805, "5072 Ikasketa Automatikoa — Orange Data Mining Txosten Entregagarria")
            self.setStrokeColor(colors.HexColor("#BDC3C7"))
            self.setLineWidth(0.5)
            self.line(45, 798, 550, 798)

        # Footer
        page_text = f"Orrialdea {self._pageNumber} / {page_count}"
        self.drawRightString(550, 30, page_text)
        self.drawString(45, 30, "CIFP / Lanbide Heziketa — Big Data & AA (2025/2026)")
        self.setStrokeColor(colors.HexColor("#BDC3C7"))
        self.setLineWidth(0.5)
        self.line(45, 42, 550, 42)
        
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=55,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1A365D")
    secondary_color = colors.HexColor("#2B6CB0")
    text_color = colors.HexColor("#2D3748")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=text_color,
        leftIndent=15,
        spaceAfter=3
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=text_color
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    caption_style = ParagraphStyle(
        'FigCaption',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#718096"),
        alignment=1, # Center
        spaceBefore=4,
        spaceAfter=10
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("ORANGE DATA MINING: IKERKETA ETA TXOSTEN ENTREGAGARRIA", title_style))
    story.append(Paragraph("<b>Modulua:</b> 5072 Ikasketa Automatikoa &nbsp;|&nbsp; <b>Tresna:</b> Orange Data Mining v3.40+ &nbsp;|&nbsp; <b>Data:</b> 2026-09-24", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=secondary_color, spaceBefore=0, spaceAfter=12))

    # 1. ATALA
    story.append(Paragraph("1. Datuen Hautaketa eta Deskribapena (Dataset)", h1_style))
    story.append(Paragraph(
        "Ariketa praktiko honetarako <b>Heart Disease (Bihotzeko Gaixotasunak)</b> datu-multzoa aukeratu da (Cleveland Clinic Foundation erreferentziazko UCI datu-multzoa, Orange-n natiboki integratua). "
        "Datu-multzoak <b>303 paziente</b> ($n=303$) eta <b>13 ezaugarri iragarle</b> biltzen ditu, bihotzeko gaixotasun koronarioa detektatzeko.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Helburu-aldagaia (Target):</b> <code>diameter narrowing</code> da. Sailkapen bitarra da: "
        "<b>0</b> (osasuntsua / estutze larriegirik gabe, %54.1, 164 paziente) eta <b>1</b> (gaixotasun koronarioa baieztatua, %45.9, 139 paziente). Klaseen banaketa orekatua da.",
        body_style
    ))

    # Feature table
    feat_data = [
        [Paragraph("Ezaugarria", table_header), Paragraph("Mota", table_header), Paragraph("Deskribapena", table_header), Paragraph("Balioak / Tartea", table_header)],
        [Paragraph("age", table_cell), Paragraph("Zenbakizkoa", table_cell), Paragraph("Pazientearen adina urtetan", table_cell), Paragraph("29 - 77 urte", table_cell)],
        [Paragraph("gender", table_cell), Paragraph("Kategorikoa", table_cell), Paragraph("Pazientearen sexua", table_cell), Paragraph("female, male", table_cell)],
        [Paragraph("chest pain", table_cell), Paragraph("Kategorikoa", table_cell), Paragraph("Bularreko min mota", table_cell), Paragraph("typical, atypical, non-anginal, asympt.", table_cell)],
        [Paragraph("rest SBP", table_cell), Paragraph("Zenbakizkoa", table_cell), Paragraph("Atsedeneko odol-presio sistolikoa", table_cell), Paragraph("94 - 200 mm Hg", table_cell)],
        [Paragraph("cholesterol", table_cell), Paragraph("Zenbakizkoa", table_cell), Paragraph("Seroko kolesterol maila", table_cell), Paragraph("126 - 564 mg/dl", table_cell)],
        [Paragraph("fast blood sugar", table_cell), Paragraph("Kategorikoa", table_cell), Paragraph("Baraualdiko glukosa > 120 mg/dl", table_cell), Paragraph("true, false", table_cell)],
        [Paragraph("rest ECG", table_cell), Paragraph("Kategorikoa", table_cell), Paragraph("Atsedeneko elektrokardiograma", table_cell), Paragraph("normal, ST-T abn, left ventr hyp", table_cell)],
        [Paragraph("max HR", table_cell), Paragraph("Zenbakizkoa", table_cell), Paragraph("Gehienezko bihotz-maiztasuna", table_cell), Paragraph("71 - 202 bpm", table_cell)],
        [Paragraph("exerc ind ang", table_cell), Paragraph("Kategorikoa", table_cell), Paragraph("Ariketak eragindako bularreko angina", table_cell), Paragraph("no, yes", table_cell)],
        [Paragraph("ST by exercise", table_cell), Paragraph("Zenbakizkoa", table_cell), Paragraph("Ariketako ST segmentuaren depresioa", table_cell), Paragraph("0.0 - 6.2", table_cell)],
        [Paragraph("slope peak ST", table_cell), Paragraph("Ordinala", table_cell), Paragraph("ST segmentuaren malda ariketan", table_cell), Paragraph("upsloping, flat, downsloping", table_cell)],
        [Paragraph("major vessels", table_cell), Paragraph("Diskretua", table_cell), Paragraph("Ontzi nagusi tindatuak (fluoroskopia)", table_cell), Paragraph("0 - 3 (4 balio falta / missing)", table_cell)],
        [Paragraph("thal", table_cell), Paragraph("Kategorikoa", table_cell), Paragraph("Talasemia probaren emaitza", table_cell), Paragraph("normal, fixed, reversable (2 missing)", table_cell)]
    ]
    t_feat = Table(feat_data, colWidths=[80, 65, 185, 175])
    t_feat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_feat)
    story.append(Spacer(1, 10))

    # 2. ATALA
    story.append(Paragraph("2. Ereduen Aplikazioa (Orange Lan-fluxua)", h1_style))
    story.append(Paragraph(
        "Orange Data Mining-en gainbegiratutako ikasketa automatikoko lan-fluxu oso bat eraiki da. "
        "Fluxuak datuen karga, aurreprozesamendua (balio falten inputazioa eta normalizazioa), lau eredu osagarriren entrenamendua eta <b>10-Fold Stratified Cross-Validation</b> ebaluazioa gauzatzen ditu.",
        body_style
    ))

    story.append(Image("/home/tears/bigdata/03_ML_5072/soluzioak/irudiak/orange_workflow.png", width=500, height=270))
    story.append(Paragraph("1. Irudia: Orange Data Mining lan-fluxu osoa (File, Preprocess, Ereduak, Test & Score eta Ebaluazioa).", caption_style))

    story.append(Paragraph("Lan-fluxuko widget nagusiak:", h2_style))
    story.append(Paragraph("• <b>File:</b> <code>heart_disease.tab</code> kargatzen du; <code>diameter narrowing</code> target gisa definituz.", bullet_style))
    story.append(Paragraph("• <b>Preprocess:</b> Missing values inputazioa (batez bestekoa jarraietan, moda kategorikoetan) eta aldagai jarraituen estandarizazioa.", bullet_style))
    story.append(Paragraph("• <b>Learners:</b> <i>Logistic Regression</i> (L2 regularizazioa), <i>Random Forest</i> (100 zuhaitz), <i>Decision Tree</i> (CART, max_depth=5) eta <i>k-NN</i> (k=5, euklidearra).", bullet_style))
    story.append(Paragraph("• <b>Test & Score:</b> 10-Fold Cross-Validation exekutatzen du, partizio orotan ereduak objektiboki neurtuz.", bullet_style))

    story.append(PageBreak())

    # 3. ATALA
    story.append(Paragraph("3. Irteera Datuak eta Emaitzen Azterketa", h1_style))
    story.append(Paragraph(
        "10-Fold Cross-Validation bidez lortutako emaitza esperimentalak honako taula eta grafikoetan laburbiltzen dira:",
        body_style
    ))

    # Metrics table
    metrics_table_data = [
        [Paragraph("Eredua (Model)", table_header), Paragraph("AUC", table_header), Paragraph("CA (Accuracy)", table_header), Paragraph("F1-Score", table_header), Paragraph("Precision", table_header), Paragraph("Recall", table_header)],
        [Paragraph("<b>Logistic Regression</b>", table_cell), Paragraph("<b>0.910</b>", table_cell), Paragraph("<b>0.838</b>", table_cell), Paragraph("<b>0.819</b>", table_cell), Paragraph("<b>0.841</b>", table_cell), Paragraph("<b>0.799</b>", table_cell)],
        [Paragraph("Random Forest", table_cell), Paragraph("0.904", table_cell), Paragraph("0.825", table_cell), Paragraph("0.806", table_cell), Paragraph("0.821", table_cell), Paragraph("0.791", table_cell)],
        [Paragraph("Decision Tree", table_cell), Paragraph("0.796", table_cell), Paragraph("0.772", table_cell), Paragraph("0.745", table_cell), Paragraph("0.765", table_cell), Paragraph("0.727", table_cell)],
        [Paragraph("k-NN (k=5)", table_cell), Paragraph("0.683", table_cell), Paragraph("0.650", table_cell), Paragraph("0.604", table_cell), Paragraph("0.628", table_cell), Paragraph("0.583", table_cell)]
    ]
    t_metrics = Table(metrics_table_data, colWidths=[130, 75, 85, 70, 70, 75])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#EDF2F7"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 10))

    story.append(Image("/home/tears/bigdata/03_ML_5072/soluzioak/irudiak/metrics_comparison.png", width=490, height=260))
    story.append(Paragraph("2. Irudia: Modeloen ebaluazio-metriken konparaketa (AUC, CA, F1, Precision, Recall).", caption_style))

    story.append(Paragraph("Nahasketa-Matrizeen Azterketa (Confusion Matrix)", h2_style))
    story.append(Paragraph(
        "Medikuntzan, <b>Faltsu Negatiboak (FN)</b> minimizatzea da helburu nagusia; hau da, bihotzeko gaitza duen pertsona bati akatsez 'osasuntsu' dagoela esatea saihestea. "
        "Erregresio Logistikoak 28 FN soilik izan ditu (Recall = %79.9), eta Decision Tree-k 38 FN.",
        body_style
    ))

    story.append(Image("/home/tears/bigdata/03_ML_5072/soluzioak/irudiak/confusion_matrices.png", width=490, height=210))
    story.append(Paragraph("3. Irudia: Nahasketa-matrizeak: Logistic Regression (ezkerrean) eta Decision Tree (eskuinean).", caption_style))

    story.append(PageBreak())

    story.append(Paragraph("ROC Kurben Analisia (ROC Analysis)", h2_style))
    story.append(Paragraph(
        "ROC kurbak egiazko positiboen tasaren (TPR / Recall) eta faltsu positiboen tasaren (FPR / 1-Specificity) arteko erlazioa erakusten du ebaketa-atari desberdinetan. "
        "<b>Erregresio Logistikoak</b> ($AUC=0.910$) eta <b>Random Forest</b>-ek ($AUC=0.904$) diskriminazio-ahalmen bikaina dute.",
        body_style
    ))

    story.append(Image("/home/tears/bigdata/03_ML_5072/soluzioak/irudiak/roc_curves.png", width=420, height=310))
    story.append(Paragraph("4. Irudia: 4 modeloen ROC kurbak eta ebaketa-puntu optimoaren hautaketa.", caption_style))

    story.append(Paragraph("Erabaki-Zuhaitzaren Arau Klinikoak (Tree Viewer)", h2_style))
    story.append(Paragraph(
        "Erabaki-zuhaitzaren errendimendua zertxobait apalagoa izan arren ($CA=\\%77.2$), bere abantaila paregabea <b>interpretagarritasuna</b> da. "
        "Mediku batek zuzenean jarrai ditzake zuhaitzak sortutako baldintzak:",
        body_style
    ))

    story.append(Image("/home/tears/bigdata/03_ML_5072/soluzioak/irudiak/decision_tree_vis.png", width=500, height=250))
    story.append(Paragraph("5. Irudia: Erabaki-zuhaitzaren hierarkia: erro-nodoa (thal), bularreko mina eta ST depresioa.", caption_style))

    story.append(PageBreak())

    # 4. ATALA
    story.append(Paragraph("4. Datu eta Modeloen Inguruko Ondorioak", h1_style))
    
    story.append(Paragraph("<b>1. Eredu Irabazlea: Erregresio Logistikoa ($AUC = 0.910, CA = 83.8\%$)</b>", h2_style))
    story.append(Paragraph(
        "Erregresio Logistikoa izan da eredurik orekatuena eta fidagarriena. "
        "Probabilitateak kalibratzeko duen gaitasunak eta L2 zigorrak gaindoitzea ekiditen dute. "
        "Gainera, koefizienteen zeinuak arrisku-faktore kardiologikoekin bat datoz (tentsio arterial, adin eta ST altuek gaixotasun probabilitatea handitzen dute).",
        body_style
    ))

    story.append(Paragraph("<b>2. Interpretagarritasuna vs Errendimendua (Trade-off Klinikoa)</b>", h2_style))
    story.append(Paragraph(
        "Random Forest-ek zehaztasun handia eskaintzen du ($AUC = 0.904$), baina 'kutxa beltza' denez, ez du azalpen sinplerik ematen. "
        "Aitzitik, <b>Decision Tree</b> ereduak (%77.2 asmatze-tasarekin) arau kliniko gardenak eskaintzen ditu: "
        "<i>'Pazienteak talasemia itzulgarria badu (thal=reversable defect) eta bularreko mina asintomatikoa izanda ST depresioa > 0.5 bada, gaixotasun koronarioaren probabilitatea %100ekoa da.'</i> "
        "Diagnostiko medikoan, gardentasun horrek balio etiko eta legal handia du.",
        body_style
    ))

    story.append(Paragraph("<b>3. Ezaugarrien Garrantzia (Feature Importance)</b>", h2_style))
    story.append(Paragraph(
        "Eredu guztiek bat egiten dute: <b>proba kardiologiko espezifikoak</b> (talasemia <code>thal</code>, ontzi fluoroskopikoak <code>major vessels</code>, bularreko min mota <code>chest pain</code> eta ariketako ST jaitsiera) dira gaixotasuna aurreikusteko faktore nagusiak. "
        "Adina edo kolesterola hutsak ez dira diskriminatzaileak isolatuta aztertuta.",
        body_style
    ))

    story.append(Paragraph("<b>4. k-NN Ereduaren Ahultasuna ($CA = 65.0\%$)</b>", h2_style))
    story.append(Paragraph(
        "k-NN algoritmoak emaitza apalak lortu ditu. 13 ezaugarridun dimentsio-espazioan, aldagai nominalen eta jarraituen arteko distantzia euklidearrak ez ditu patroi kardiologikoak ondo banatzen, "
        "arauetan edo hiperplano probabilistikoetan oinarritutako algoritmoek egiten duten bezala.",
        body_style
    ))

    story.append(Paragraph("<b>5. Orange Data Mining Tresnaren Balorazioa</b>", h2_style))
    story.append(Paragraph(
        "Orange Data Mining-ek frogatu du ikasketa automatikoko proiektuen bizi-zikloa (EDA, garbiketa, modelo-entrenamendua, balioztatze gurutzatua eta bistaratze aurreratua) "
        "koderik idatzi gabe baina zorroztasun zientifiko osoz egiteko tresna paregabea dela Lanbide Heziketan eta datu-zientzian.",
        body_style
    ))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceBefore=10, spaceAfter=10))
    story.append(Paragraph("<b>Entregagarriaren fitxategi elkartuak:</b>", body_style))
    story.append(Paragraph("• <b>PDF Txostena:</b> <code>03_ML_5072/soluzioak/Orange_Data_Mining_Entregagarria.pdf</code>", bullet_style))
    story.append(Paragraph("• <b>Python Script Erreproduzigarria:</b> <code>03_ML_5072/soluzioak/orange_bihotza_ereduak.py</code>", bullet_style))
    story.append(Paragraph("• <b>Irudi Bilduma (300 DPI):</b> <code>03_ML_5072/soluzioak/irudiak/</code> (5 irudi bektorial/raster)", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {filename}")

if __name__ == "__main__":
    out_pdf = "/home/tears/bigdata/03_ML_5072/soluzioak/Orange_Data_Mining_Entregagarria.pdf"
    build_pdf(out_pdf)
