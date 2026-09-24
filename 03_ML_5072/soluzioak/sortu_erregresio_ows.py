"""Create a portable Orange Canvas workflow for UCI Auto MPG OLS."""

from __future__ import annotations

import base64
import pickle
from pathlib import Path

import xml.etree.ElementTree as ET

from orangewidget.utils.filedialogs import RecentPath
from orangecanvas.scheme.readwrite import parse_ows_stream


HERE = Path(__file__).resolve().parent
OUT = HERE / "Orange_Erregresio_Lineala.ows"
DATA_RELATIVE = "datos/auto_mpg/auto_mpg_weight.tab"


def main() -> None:
    root = ET.Element("scheme", {
        "version": "2.0",
        "title": "Orange Data Mining — Regresión lineal Auto MPG",
        "description": (
            "Creador: Unai Urzainqui Perez. Datos: UCI Auto MPG (398 vehículos). "
            "Regresión lineal simple mpg ~ weight (libras), evaluación 10-fold CV y tabla de predicciones fuera de muestra."
        ),
    })
    nodes = ET.SubElement(root, "nodes")
    node_specs = [
        ("0", "File", "Orange.widgets.data.owfile.OWFile", "Auto MPG · datos locales", "(80.0, 220.0)"),
        ("1", "Scatter Plot", "Orange.widgets.visualize.owscatterplot.OWScatterPlot", "Peso vs mpg", "(300.0, 95.0)"),
        ("2", "Linear Regression", "Orange.widgets.model.owlinearregression.OWLinearRegression", "Regresión lineal · OLS", "(300.0, 260.0)"),
        ("3", "Test & Score", "Orange.widgets.evaluate.owtestandscore.OWTestAndScore", "Validación cruzada · 10 folds", "(530.0, 255.0)"),
        ("4", "Data Table", "Orange.widgets.data.owtable.OWTable", "Predicciones CV y residuos", "(770.0, 255.0)"),
    ]
    for identifier, name, qualified_name, title, position in node_specs:
        ET.SubElement(nodes, "node", {
            "id": identifier,
            "name": name,
            "qualified_name": qualified_name,
            "project_name": "Orange3",
            "version": "",
            "title": title,
            "position": position,
        })

    links = ET.SubElement(root, "links")
    for identifier, src, dst, output, input_name, src_id, dst_id in [
        ("0", "0", "1", "Data", "Data", "data", "data"),
        ("1", "0", "2", "Data", "Data", "data", "data"),
        ("2", "0", "3", "Data", "Data", "data", "train_data"),
        ("3", "2", "3", "Learner", "Learner", "learner", "learner"),
        ("4", "3", "4", "Predictions", "Data", "predictions", "data"),
    ]:
        ET.SubElement(links, "link", {
            "id": identifier,
            "source_node_id": src,
            "sink_node_id": dst,
            "source_channel": output,
            "sink_channel": input_name,
            "enabled": "true",
            "source_channel_id": src_id,
            "sink_channel_id": dst_id,
        })

    annotations = ET.SubElement(root, "annotations")
    notes = [
        ("0", "(25.0, 20.0, 220.0, 50.0)", "Dataset UCI Auto MPG · 398 coches\nCreador: Unai Urzainqui Perez"),
        ("1", "(260.0, 10.0, 240.0, 58.0)", "En Scatter Plot, usa weight en X y mpg en Y."),
        ("2", "(75.0, 380.0, 620.0, 64.0)", "OLS: mpg (millas/galón) ~ weight (libras). Test & Score: 10-fold CV, random_state 42; predicciones fuera de muestra en Data Table."),
    ]
    for identifier, rect, text in notes:
        element = ET.SubElement(annotations, "text", {
            "id": identifier, "type": "text/plain", "rect": rect,
            "font-family": "Helvetica", "font-size": "12",
        })
        element.text = text
    ET.SubElement(root, "thumbnail")

    properties = ET.SubElement(root, "node_properties")
    file_settings = {
        "controlAreaVisible": True,
        "recent_paths": [RecentPath("", "basedir", DATA_RELATIVE)],
        "recent_urls": [],
        "savedWidgetGeometry": None,
        "sheet_names": {},
        "source": 0,
        "url": "",
        "domain_editor": {},
        "__version__": 1,
        "context_settings": [],
    }
    file_payload = base64.b64encode(pickle.dumps(file_settings, protocol=4)).decode("ascii")
    file_property = ET.SubElement(properties, "properties", {"node_id": "0", "format": "pickle"})
    file_property.text = file_payload
    ET.SubElement(properties, "properties", {"node_id": "1", "format": "literal"}).text = (
        "{'auto_commit': True, 'auto_sample': True, 'controlAreaVisible': True, "
        "'attr_x': None, 'attr_y': None, '__version__': 2}"
    )
    ET.SubElement(properties, "properties", {"node_id": "2", "format": "literal"}).text = (
        "{'auto_apply': True, 'controlAreaVisible': True, 'fit_intercept': True, "
        "'learner_name': 'Linear Regression (OLS)', 'reg_type': 0, '__version__': 2}"
    )
    ET.SubElement(properties, "properties", {"node_id": "3", "format": "literal"}).text = (
        "{'controlAreaVisible': True, 'resampling': 0, 'n_folds': 3, "
        "'cv_stratified': False, '__version__': 1}"
    )
    ET.SubElement(properties, "properties", {"node_id": "4", "format": "literal"}).text = (
        "{'auto_commit': True, 'controlAreaVisible': True, 'color_by_class': True, '__version__': 1}"
    )
    ET.SubElement(root, "session_state")

    ET.indent(root, space="\t")
    OUT.write_text("<?xml version='1.0' encoding='utf-8'?>\n" + ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")
    with OUT.open("rb") as stream:
        parsed = parse_ows_stream(stream)
    if len(parsed.nodes) != 5 or len(parsed.links) != 5:
        raise ValueError("Unexpected Orange workflow node/link count")
    print(f"Saved and parsed {OUT} ({len(parsed.nodes)} widgets, {len(parsed.links)} links)")


if __name__ == "__main__":
    main()
