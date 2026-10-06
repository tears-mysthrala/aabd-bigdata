"""Reabre el .ows con el motor real de Orange y verifica datos/configuración."""
import hashlib
import json
import os
from pathlib import Path

if os.environ.get('AI4I_ORANGE_LOCK_HELD') != '1':
    raise SystemExit('Ejecutar bajo el flock documentado en README.')

from AnyQt.QtCore import QTimer
from AnyQt.QtWidgets import QApplication
from Orange.widgets.data.owfile import OWFile
from Orange.widgets.visualize.owscatterplot import OWScatterPlot
from Orange.widgets.visualize.owdistributions import OWDistributions
from orangecanvas.registry import WidgetRegistry, WidgetDescription
from orangewidget.workflow.widgetsscheme import WidgetsScheme

BASE = Path(__file__).resolve().parents[1]


def main():
    app = QApplication([])
    registry = WidgetRegistry()
    for cls in [OWFile, OWScatterPlot, OWDistributions]:
        registry.register_widget(WidgetDescription(**cls.get_widget_description()))
    scheme = WidgetsScheme(env={'basedir': str(BASE)})
    scheme.load_from(str(BASE / 'Interpretacion_AI4I.ows'), registry=registry)
    widgets = {type(scheme.widget_for_node(node)).__name__: scheme.widget_for_node(node) for node in scheme.nodes}
    result = {}
    errors = []

    def inspect():
        try:
            file = widgets['OWFile']
            scatter = widgets['OWScatterPlot']
            distributions = widgets['OWDistributions']
            if file.data is None or scatter.data is None or distributions.data is None:
                QTimer.singleShot(200, inspect)
                return
            assert len(file.data) == len(scatter.data) == len(distributions.data) == 10000
            assert scatter.attr_x.name == 'Rotational speed [rpm]'
            assert scatter.attr_y.name == 'Torque [Nm]'
            assert scatter.attr_color.name == 'Machine failure'
            assert distributions.var.name == 'Torque [Nm]'
            assert distributions.cvar.name == 'Machine failure'
            width = float(distributions.binnings[distributions.number_of_bins].width)
            assert width == 5
            assert int((file.data.Y == 1).sum()) == 339
            result.update({'status': 'passed', 'engine': 'orangewidget.workflow.WidgetsScheme',
                'workflow_sha256': hashlib.sha256((BASE / 'Interpretacion_AI4I.ows').read_bytes()).hexdigest(),
                'nodes': len(scheme.nodes), 'links': len(scheme.links),
                'relative_file_resolution': True, 'rows_in_each_widget': 10000,
                'failure_count': 339, 'scatter_x': scatter.attr_x.name, 'scatter_y': scatter.attr_y.name,
                'scatter_color': scatter.attr_color.name, 'distribution_variable': distributions.var.name,
                'distribution_split': distributions.cvar.name, 'bin_width_Nm': width})
            app.quit()
        except Exception as exc:
            errors.append(repr(exc)); app.quit()

    def timeout():
        if not result:
            errors.append('Workflow did not finish loading within 20 seconds')
            app.quit()

    QTimer.singleShot(300, inspect)
    QTimer.singleShot(20000, timeout)
    app.exec()
    scheme.clear()
    for widget in widgets.values():
        widget.close()
    if errors:
        raise RuntimeError(errors)
    (BASE / 'evidencias/flujo_reabierto.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
