"""Capturas nativas Orange/Qt. Ejecutar con reproducir.sh para respetar flock."""
import base64
import hashlib
import json
import os
import pickle
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

if os.environ.get('AI4I_ORANGE_LOCK_HELD') != '1':
    raise SystemExit('Use reproducir.sh: toda ejecución Orange requiere flock.')

import Orange
import numpy as np
from AnyQt.QtCore import QTimer
from AnyQt.QtGui import QFont
from AnyQt.QtWidgets import QApplication
from Orange.widgets.data.owfile import OWFile
from Orange.widgets.visualize.owscatterplot import OWScatterPlot
from Orange.widgets.visualize.owdistributions import OWDistributions
from orangewidget.utils.filedialogs import RecentPath
from orangecanvas.scheme.readwrite import parse_ows_stream

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'datos/ai4i2020_orange.tab'


def workflow(widgets):
    root = ET.Element('scheme', version='2.0', title='AI4I: interpretación de velocidad y par',
                      description='Tarea 63638. Descripción de 10000 registros sintéticos, sin entrenamiento.')
    nodes = ET.SubElement(root, 'nodes')
    definitions = [('0', 'File', 'Orange.widgets.data.owfile.OWFile', '(100.0, 200.0)'),
                   ('1', 'Scatter Plot', 'Orange.widgets.visualize.owscatterplot.OWScatterPlot', '(400.0, 100.0)'),
                   ('2', 'Distributions', 'Orange.widgets.visualize.owdistributions.OWDistributions', '(400.0, 300.0)')]
    for identifier, name, qualified, position in definitions:
        ET.SubElement(nodes, 'node', id=identifier, name=name, qualified_name=qualified,
                      project_name='Orange3', version='', title=name, position=position)
    links = ET.SubElement(root, 'links')
    for destination in ['1', '2']:
        ET.SubElement(links, 'link', id=destination, source_node_id='0', sink_node_id=destination,
                      source_channel='Data', sink_channel='Data', source_channel_id='data',
                      sink_channel_id='data', enabled='true')
    ET.SubElement(root, 'annotations')
    ET.SubElement(root, 'thumbnail')
    properties = ET.SubElement(root, 'node_properties')
    settings = {'recent_paths': [RecentPath('', 'basedir', 'datos/ai4i2020_orange.tab')],
                'recent_urls': [], 'source': 0, 'url': '', 'sheet_names': {},
                'domain_editor': {}, 'context_settings': [], '__version__': 1}
    for identifier, widget in zip(['0', '1', '2'], widgets):
        packed = settings if identifier == '0' else widget.settingsHandler.pack_data(widget)
        prop = ET.SubElement(properties, 'properties', node_id=identifier, format='pickle')
        prop.text = base64.b64encode(pickle.dumps(packed, protocol=4)).decode('ascii')
    ET.indent(root)
    target = BASE / 'Interpretacion_AI4I.ows'
    ET.ElementTree(root).write(target, encoding='utf-8', xml_declaration=True)
    with target.open('rb') as stream:
        parsed = parse_ows_stream(stream)
    assert len(parsed.nodes) == 3 and len(parsed.links) == 2


def main():
    app = QApplication([])
    app.setFont(QFont('DejaVu Sans', 14))
    file_widget = OWFile()
    file_widget.recent_paths = [RecentPath(str(SOURCE), '', '')]
    file_widget.source = 0
    file_widget.load_data()
    app.processEvents()
    table = file_widget.data
    assert table is not None and len(table) == 10000
    assert len(table.domain.attributes) == 6 and len(table.domain.metas) == 7
    assert table.domain.class_var.name == 'Machine failure'
    assert table.domain.class_var.values == ('0', '1')
    assert int((table.Y == 1).sum()) == 339
    assert np.isfinite(table.X).all() and np.isfinite(table.Y).all()
    scatter = OWScatterPlot()
    scatter.set_data(table)
    scatter.handleNewSignals()
    scatter.attr_x = table.domain['Rotational speed [rpm]']
    scatter.attr_y = table.domain['Torque [Nm]']
    scatter.attr_color = table.domain.class_var
    scatter.attr_shape = table.domain.class_var
    scatter.attr_size = None
    scatter.graph.point_width = 6
    scatter.graph.alpha_value = 140
    scatter.graph.jitter_size = 0
    scatter.setup_plot()
    distributions = OWDistributions()
    distributions.set_data(table)
    distributions.var = table.domain['Torque [Nm]']
    distributions.cvar = table.domain.class_var
    distributions._on_var_changed()
    distributions._on_cvar_changed()
    distributions.number_of_bins = min(range(len(distributions.binnings)),
        key=lambda i: abs(float(distributions.binnings[i].width or 0) - 5))
    distributions._on_bins_changed()
    assert distributions.ploti.getAxis('bottom').labelText == 'Torque [Nm]'
    captures = [('01_file.png', file_widget), ('02_scatter_speed_torque.png', scatter),
                ('03_distributions_torque.png', distributions)]
    capture_records = []
    failures = []

    def capture(index=0):
        try:
            if index == len(captures):
                workflow([file_widget, scatter, distributions])
                app.quit()
                return
            name, widget = captures[index]
            widget.setFixedSize(1200, 820)
            widget.show()
            def save():
                try:
                    app.processEvents()
                    # Hide only the introductory tip attached to this widget.
                    # Runtime data/error messages remain visible.
                    tip = getattr(widget, '_OWBaseWidget__msgwidget', None)
                    if tip is not None:
                        tip.hide()
                    if widget is file_widget:
                        for column, width in enumerate([365, 155, 130, 480]):
                            widget.domain_editor.setColumnWidth(column, width)
                    app.processEvents()
                    assert widget.isVisible()
                    target = BASE / 'capturas' / name
                    pixmap = widget.grab()
                    assert pixmap.save(str(target))
                    capture_records.append({'file': f'capturas/{name}', 'widget': type(widget).__name__,
                        'visible': True, 'width': pixmap.width(), 'height': pixmap.height(),
                        'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
                    widget.close()
                    capture(index + 1)
                except Exception as exc:
                    failures.append(repr(exc)); app.quit()
            QTimer.singleShot(1400, save)
        except Exception as exc:
            failures.append(repr(exc)); app.quit()
    QTimer.singleShot(0, capture)
    app.exec()
    scatter_points = len(scatter.data)
    for widget in [file_widget, scatter, distributions]:
        widget.close()
        widget.onDeleteWidget()
    if failures:
        raise RuntimeError(failures)
    evidence = {'captured_utc': datetime.now(timezone.utc).isoformat(), 'orange_version': Orange.__version__,
        'python_version': sys.version.split()[0], 'platform': os.environ.get('QT_QPA_PLATFORM'),
        'method': 'Visible native Qt Orange widgets; QWidget.grab(); no screenshot reconstruction',
        'rows': len(table), 'features': 6, 'target': 'Machine failure', 'metas': 7,
        'failure_count': int((table.Y == 1).sum()), 'scatter_points': scatter_points,
        'jitter': 0, 'sampled_rows': False, 'captures': capture_records,
        'workflow_parse': {'nodes': 3, 'links': 2}, 'dataset': 'datos/ai4i2020_orange.tab'}
    (BASE / 'evidencias/orange_gui.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(evidence, indent=2))


if __name__ == '__main__':
    main()
