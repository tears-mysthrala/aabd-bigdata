"""Create a portable Orange workflow for the WDBC sigmoid exercise."""
from __future__ import annotations

import base64
import pickle
from pathlib import Path
import xml.etree.ElementTree as ET

from orangewidget.utils.filedialogs import RecentPath
from orangecanvas.scheme.readwrite import parse_ows_stream

HERE = Path(__file__).resolve().parent
OUT = HERE / "Orange_Regresion_Logistica.ows"
DATA_RELATIVE = "datos/breast_cancer_wisconsin/wdbc_texture_mean.tab"


def main() -> None:
    root = ET.Element("scheme", {
        "version": "2.0",
        "title": "Orange Data Mining - Logística de diagnóstico WDBC",
        "description": (
            "Creador: Unai Urzainqui Perez. UCI WDBC: clasificación benigna/maligna. "
            "Modelo univariable texture_mean -> diagnosis, L2 C=1; 10-fold CV estratificada. "
            "El informe PDF incluye el scatter con sigmoide y el ajuste completo."
        ),
    })
    nodes = ET.SubElement(root, "nodes")
    specs = [
        ("0", "File", "Orange.widgets.data.owfile.OWFile", "WDBC · textura media", "(70.0, 210.0)"),
        ("1", "Preprocess", "Orange.widgets.data.owpreprocess.OWPreprocess", "Normalizar dentro del fold", "(280.0, 80.0)"),
        ("2", "Logistic Regression", "Orange.widgets.model.owlogisticregression.OWLogisticRegression", "Logistic Regression · L2", "(500.0, 150.0)"),
        ("3", "Test & Score", "Orange.widgets.evaluate.owtestandscore.OWTestAndScore", "CV estratificada · 10 folds", "(720.0, 235.0)"),
        ("4", "Confusion Matrix", "Orange.widgets.evaluate.owconfusionmatrix.OWConfusionMatrix", "Matriz de confusión", "(950.0, 155.0)"),
        ("5", "ROC Analysis", "Orange.widgets.evaluate.owrocanalysis.OWROCAnalysis", "ROC Analysis", "(950.0, 325.0)"),
        ("6", "Data Table", "Orange.widgets.data.owtable.OWTable", "Predicciones out-of-fold", "(1180.0, 235.0)"),
    ]
    for identifier, name, qualified_name, title, position in specs:
        ET.SubElement(nodes, "node", {
            "id": identifier, "name": name, "qualified_name": qualified_name,
            "project_name": "Orange3", "version": "", "title": title, "position": position,
        })
    links = ET.SubElement(root, "links")
    linkspecs = [
        ("0", "0", "1", "Data", "Data", "data", "data"),
        ("1", "1", "2", "Preprocessor", "Preprocessor", "preprocessor", "preprocessor"),
        ("2", "0", "3", "Data", "Data", "data", "train_data"),
        ("3", "2", "3", "Learner", "Learner", "learner", "learner"),
        ("4", "3", "4", "Evaluation Results", "Evaluation Results", "evaluations_results", "evaluation_results"),
        ("5", "3", "5", "Evaluation Results", "Evaluation Results", "evaluations_results", "evaluation_results"),
        ("6", "3", "6", "Predictions", "Data", "predictions", "data"),
    ]
    for ident, src, dst, outname, inname, outid, inid in linkspecs:
        ET.SubElement(links, "link", {
            "id": ident, "source_node_id": src, "sink_node_id": dst,
            "source_channel": outname, "sink_channel": inname, "enabled": "true",
            "source_channel_id": outid, "sink_channel_id": inid,
        })
    annotations = ET.SubElement(root, "annotations")
    for ident, rect, text in [
        ("0", "(25.0, 15.0, 240.0, 55.0)", "UCI WDBC · 569 muestras\nCreador: Unai Urzainqui Perez"),
        ("1", "(245.0, 12.0, 310.0, 58.0)", "Predictor: texture_mean\nTarget: diagnosis B/M\nNormalización dentro de cada fold"),
        ("2", "(650.0, 30.0, 360.0, 66.0)", "CV estratificada, 10 folds, semilla 42.\nEl PDF muestra los puntos, las fracciones por decil y la sigmoide."),
        ("3", "(55.0, 375.0, 800.0, 65.0)", "El ajuste de una variable facilita interpretar el scatter. Es un ejemplo educativo, no una herramienta clínica."),
    ]:
        e = ET.SubElement(annotations, "text", {"id": ident, "type": "text/plain", "rect": rect, "font-family": "Helvetica", "font-size": "12"})
        e.text = text
    ET.SubElement(root, "thumbnail")
    props = ET.SubElement(root, "node_properties")
    file_settings = {
        "controlAreaVisible": True,
        "recent_paths": [RecentPath("", "basedir", DATA_RELATIVE)],
        "recent_urls": [], "savedWidgetGeometry": None, "sheet_names": {},
        "source": 0, "url": "", "domain_editor": {}, "__version__": 1,
        "context_settings": [],
    }
    payload = base64.b64encode(pickle.dumps(file_settings, protocol=4)).decode("ascii")
    ET.SubElement(props, "properties", {"node_id": "0", "format": "pickle"}).text = payload
    ET.SubElement(props, "properties", {"node_id": "1", "format": "literal"}).text = (
        "{'storedsettings': {'name': '', 'preprocessors': "
        "[('orange.preprocess.scale', {'method': 2})]}, 'autocommit': True, '__version__': 2}"
    )
    ET.SubElement(props, "properties", {"node_id": "2", "format": "literal"}).text = (
        "{'C_index': 61, 'auto_apply': True, 'class_weight': False, 'controlAreaVisible': True, "
        "'learner_name': 'Logistic Regression', 'penalty_type': 1, '__version__': 2}"
    )
    ET.SubElement(props, "properties", {"node_id": "3", "format": "literal"}).text = (
        "{'controlAreaVisible': True, 'resampling': 0, 'n_folds': 3, 'cv_stratified': True, '__version__': 1}"
    )
    ET.SubElement(props, "properties", {"node_id": "4", "format": "literal"}).text = (
        "{'auto_commit': True, 'controlAreaVisible': True, 'show_class_distributions': True, '__version__': 1}"
    )
    ET.SubElement(props, "properties", {"node_id": "5", "format": "literal"}).text = (
        "{'controlAreaVisible': True, 'display_convex_hull': False, '__version__': 1}"
    )
    ET.SubElement(props, "properties", {"node_id": "6", "format": "literal"}).text = (
        "{'auto_commit': True, 'controlAreaVisible': True, 'color_by_class': True, '__version__': 1}"
    )
    ET.SubElement(root, "session_state")
    ET.indent(root, space="\t")
    OUT.write_text("<?xml version='1.0' encoding='utf-8'?>\n" + ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")
    with OUT.open("rb") as stream:
        parsed = parse_ows_stream(stream)
    if len(parsed.nodes) != len(specs) or len(parsed.links) != len(linkspecs):
        raise ValueError("Unexpected workflow structure")
    print(f"Saved and parsed {OUT} ({len(parsed.nodes)} widgets, {len(parsed.links)} links)")


if __name__ == "__main__":
    main()
