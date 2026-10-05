"""Build the Heart Disease deliverable from the recorded CV JSON and figures."""
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

BASE = Path(__file__).resolve().parent
DATA = BASE / 'datos' / 'heart_disease'


def build_pdf(filename):
    r = json.loads((DATA / 'resultados_cv.json').read_text())
    assert hashlib.sha256((DATA / 'predicciones_cv.csv').read_bytes()).hexdigest() == r['predictions_sha256']
    assert hashlib.sha256((DATA / 'heart_disease.tab').read_bytes()).hexdigest() == r['dataset']['sha256']
    manifest = json.loads((DATA / 'figuras_manifest.json').read_text())
    assert manifest['results_sha256'] == hashlib.sha256((DATA / 'resultados_cv.json').read_bytes()).hexdigest(), 'Regenerate figures from current results'
    for name, digest in manifest['figures'].items():
        assert hashlib.sha256((BASE / 'irudiak' / name).read_bytes()).hexdigest() == digest, f'Changed figure: {name}'
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('Small', parent=styles['BodyText'], fontSize=8, leading=11))
    styles['BodyText'].fontSize = 9
    styles['BodyText'].leading = 13
    story = []

    def p(text, style='BodyText'):
        story.append(Paragraph(text, styles[style]))
        story.append(Spacer(1, 7))

    def image(name, width, height):
        story.append(Image(str(BASE / 'irudiak' / name), width=width, height=height))

    def table(rows, widths):
        t = Table(rows, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A365D')),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('FONTSIZE', (0, 0), (-1, -1), 8),
                              ('GRID', (0, 0), (-1, -1), 0.4, colors.lightgrey),
                              ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#EDF2F7'), colors.white]),
                              ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
        story.append(t)
        story.append(Spacer(1, 12))

    p('ORANGE DATA MINING', 'Title')
    p('Heart Disease: CV erreproduzigarria', 'Heading1')
    p('5072 Ikasketa Automatikoa | Tokiko exekuzio egiaztatua: 2026-10-02')
    d = r['dataset']
    p('1. Helburua, datuak eta ebaluazioa', 'Heading2')
    p(f"Decision Tree eta Random Forest alderatzea da helburua, Logistic Regression eta k-NN erreferentziekin. "
      f"Orange-ren Heart Disease lagina: <b>{d['n']} erregistro, {d['predictors']} iragarle</b>; "
      f"target: <b>{escape(d['target'])}</b>. Klase 0: {d['class_counts'][0]}; klase 1: {d['class_counts'][1]}. "
      f"<b>Klase positiboa: 1</b>. Iragarleetan {d['missing_predictor_cells']} balio falta daude; erregistro guztiak mantendu dira.")
    p('Datuak Orange-ren lagin-fitxategitik kopiatuta daude; ez dira paziente berriak edo kanpo-balioztatze kohorte bat. '
      'Klase-etiketek dataseteko diameter narrowing sailkapena adierazten dute; ez dira diagnostiko kliniko berriak.')
    p(f"<b>Split:</b> {r['evaluation']['k']}-fold stratified CV, shuffle=True, random_state={r['evaluation']['random_state']}. "
      'Lau modeloek fold berberak erabiltzen dituzte. Erregistro bakoitzak bere entrenamendutik kanpoko iragarpen bakarra du modelo bakoitzeko. '
      'Inputazioa eta normalizazioa learner bakoitzaren training fold barruan doitzen dira.')
    p('Metrikak out-of-fold iragarpen guztiak elkartuta kalkulatzen dira, ez fold-metriken batezbesteko gisa. '
      'F1, Precision eta Recall bitarrak dira (klase 1). CA klase-iragarpenarekin kalkulatzen da; ROC/AUC klase 1 probabilitatearekin.')
    image('orange_workflow.png', 495, 180)
    p('1. irudia: egiaztatutako Python API prozesuaren eskema; ez da Orange GUI pantaila-argazkia.', 'Small')
    p('Exekuzio-ingurunea: ' + ', '.join(f'{escape(k)} {escape(v)}' for k, v in r['versions'].items()), 'Small')
    story.append(PageBreak())
    p('2. Ereduak eta emaitzak', 'Heading1')
    for m in r['models']:
        p(f"<b>{escape(m['name'])}</b>: {escape(json.dumps(m['settings']))}. "
          f"Aurreprozesamendua: {escape(', '.join(m['preprocessors']))}.", 'Small')
    p('TreeLearner Orange-ren zuhaitza da; ez da sklearn CART gisa aurkezten. Random Forest sklearn bidezko Orange learner da. '
      'LR eta k-NN aldagai jarraitu normalizatuekin ebaluatu dira; konfigurazioa ez dator bat aurreko PDFko balio literalekin.')
    keys = ['AUC', 'CA', 'F1', 'Precision', 'Recall']
    table([['Model'] + keys] + [[m['name']] + [f"{m['metrics'][k]:.4f}" for k in keys] for m in r['models']],
          [145, 65, 65, 65, 75, 65])
    image('metrics_comparison.png', 490, 225)
    p('2. irudia: benetako CV metrikak; F1/Precision/Recall klase 1erako.', 'Small')
    tree = next(m for m in r['models'] if m['name'] == 'Decision Tree')
    forest = next(m for m in r['models'] if m['name'] == 'Random Forest')
    p(f"<b>Decision Tree (63544):</b> CA={tree['metrics']['CA']:.4f}, AUC={tree['metrics']['AUC']:.4f}, "
      f"Recall={tree['metrics']['Recall']:.4f}. Arauak ikus daitezke, baina interpretazioa ez da kanpo-balioztatzea.")
    p(f"<b>Random Forest (63386):</b> CA={forest['metrics']['CA']:.4f}, AUC={forest['metrics']['AUC']:.4f}, "
      f"Recall={forest['metrics']['Recall']:.4f}. Exekuzio honetako AUC handiagoa du zuhaitz bakarrak baino; "
      'ez da esangura estatistikorik edo populazio berrietako nagusitasunik frogatu.')
    story.append(PageBreak())
    p('3. Nahasketa-matrizeak eta ROC', 'Heading1')
    image('confusion_matrices.png', 440, 352)
    p('3. irudia: errenkadak benetako klaseak; zutabeak iragarritako klaseak. Matrizeak 303 erregistro biltzen ditu modelo bakoitzeko.', 'Small')
    for m in [tree, forest]:
        cm = m['confusion_matrix']
        p(f"<b>{m['name']}:</b> TN={cm[0][0]}, FP={cm[0][1]}, FN={cm[1][0]}, TP={cm[1][1]}.")
    story.append(PageBreak())
    p('3.1 ROC enpirikoa', 'Heading1')
    image('roc_curves.png', 480, 360)
    p('4. irudia: held-out probabilitateetatik sortutako ROC enpirikoak. Ez dago formula analitikorik edo atari optimo asmaturik.', 'Small')
    p('AUCk sailkapen-gaitasuna laburbiltzen du atari guztietan. Ez du probabilitateen kalibrazioa edo erabaki klinikoen erabilgarritasuna neurtzen. '
      'Atari bat CV emaitza hauetan aukeratuz gero, atari horren errendimendua beste datu independenteetan egiaztatu beharko litzateke.')
    story.append(PageBreak())
    p('4. Zuhaitzaren azalpena', 'Heading1')
    p('Beheko arauak datu guztiekin entrenatutako max_depth=3 zuhaitz errealaren print_tree irteera dira. '
      'Kopuruak training laginekoak dira; CV taulako zuhaitzak max_depth=5 erabiltzen du. '
      'Nodo baten %100 training proportzioak ez du ziurtasuna edo probabilitate kliniko kalibratua esan nahi.')
    image('decision_tree_vis.png', 490, 303)
    p('5. irudia: zuhaitz errealaren adarrak eta klase 0/1 kopuruak, inputazioaren ondoren.', 'Small')
    p('5. Erreproduzigarritasuna eta mugak', 'Heading2')
    p('Sarrerak eta irteerak: datos/heart_disease/heart_disease.tab; predicciones_cv.csv (row_index, fold, model, actual, predicted, probability_1); '
      'resultados_cv.json (hashak, bertsioak, hiperparametroak, metrikak, ROC eta zuhaitza). '
      'Exekuzio-komandoak eta egiaztapenak Heart_Disease_Evaluacion.md dokumentuan daude.', 'Small')
    p('Datu-multzo bakarra eta split bakarra erabili dira; ez dago kanpo-testik, nested CVrik, kalibrazio edo justizia-ebaluaziorik. '
      'Ez da ezaugarrien garrantziaren adostasunik egiaztatu, ezta eredu baten nagusitasun estatistikorik ere. '
      'Orange_Bihotza_Ereduak.ows ez da GUI bidez exekutatu eta bere konfigurazioa ez da exekuzio honen baliokidea. '
      'Emaitzak ikasketa akademikorako dira; ez erabilera klinikorako.', 'Small')
    p('Dataset SHA-256: ' + d['sha256'], 'Small')

    def footer(c, doc):
        c.setFont('Helvetica', 8)
        c.setFillColor(colors.grey)
        c.drawString(45, 25, '5072 ML | Heart Disease | CV egiaztatua')
        c.drawRightString(550, 25, str(doc.page))

    SimpleDocTemplate(str(filename), pagesize=A4, leftMargin=45, rightMargin=45,
                      topMargin=40, bottomMargin=45).build(story, onFirstPage=footer, onLaterPages=footer)
    print(filename)


if __name__ == '__main__':
    build_pdf(BASE / 'Orange_Data_Mining_Entregagarria.pdf')
