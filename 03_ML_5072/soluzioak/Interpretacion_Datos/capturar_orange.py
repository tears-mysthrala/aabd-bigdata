"""Capturar widgets Orange reales, mostrando cada ventana Qt en Wayland.

No recrea gráficos ni captura contenido ajeno del escritorio. QWidget.grab()
obtiene exclusivamente la ventana Orange que procesa la tabla de Iris.
"""
import hashlib
import json
import base64
import pickle
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from AnyQt.QtCore import QTimer
from AnyQt.QtWidgets import QApplication
from AnyQt.QtGui import QFont
from Orange.data import Table
from Orange.widgets.visualize.owscatterplot import OWScatterPlot
from Orange.widgets.visualize.owdistributions import OWDistributions

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent/'datos/iris/iris.csv'


def main():
    app = QApplication([])
    app.setFont(QFont("DejaVu Sans", 13))
    table = Table(str(SOURCE))
    assert table.X.shape == (150,4) and np.isfinite(table.X).all()
    scatter = OWScatterPlot()
    scatter.set_data(table)
    scatter.handleNewSignals()
    scatter.attr_x = table.domain['petal_length']
    scatter.attr_y = table.domain['petal_width']
    scatter.attr_color = table.domain.class_var
    scatter.attr_shape = table.domain.class_var
    scatter.attr_size = None
    scatter.setup_plot()
    distributions = OWDistributions()
    distributions.set_data(table)
    distributions.var = table.domain['petal_length']
    distributions.cvar = table.domain.class_var
    distributions._on_var_changed()
    distributions._on_cvar_changed()
    distributions.number_of_bins = min(range(len(distributions.binnings)), key=lambda i: abs(float(distributions.binnings[i].width or 0)-0.5))
    distributions._on_bins_changed()
    assert distributions.ploti.getAxis('bottom').labelText == 'petal_length'
    widgets = [('orange_scatter.png', scatter),('orange_distribucion.png', distributions)]
    def capture(index=0):
        if index == len(widgets):
            app.quit(); return
        name,widget = widgets[index]
        widget.setFixedSize(1100,800)
        widget.show()
        def save():
            app.processEvents()
            assert widget.grab().save(str(BASE/name))
            widget.close()
            capture(index+1)
        QTimer.singleShot(1200,save)
    QTimer.singleShot(0,capture)
    app.exec()
    means={name: {'n':int((table.Y==index).sum()),'petal_length_mean_cm':float(table.X[table.Y==index,2].mean()),
                 'petal_width_mean_cm':float(table.X[table.Y==index,3].mean())}
           for index,name in enumerate(table.domain.class_var.values)}
    metrics={'source':'../datos/iris/iris.csv','sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
             'rows':len(table),'features':4,'missing':int(np.isnan(table.X).sum()),'classes':means,
             'pearson_petal_length_width':float(np.corrcoef(table.X[:,2],table.X[:,3])[0,1]),
             'capture':'Native Orange 3.40 widgets displayed on Wayland; QWidget.grab(), no recreated screenshots'}
    (BASE/'resumen.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
    from orangewidget.utils.filedialogs import RecentPath
    from orangecanvas.scheme.readwrite import parse_ows_stream
    root = ET.Element('scheme', version='2.0', title='Interpretación Iris: pétalos', description='Tarea 63638; 150 flores; análisis descriptivo')
    nodes = ET.SubElement(root, 'nodes')
    for identifier, name, qualified, position in [
        ('0','File','Orange.widgets.data.owfile.OWFile','(100.0, 200.0)'),
        ('1','Scatter Plot','Orange.widgets.visualize.owscatterplot.OWScatterPlot','(350.0, 100.0)'),
        ('2','Distributions','Orange.widgets.visualize.owdistributions.OWDistributions','(350.0, 300.0)')]:
        ET.SubElement(nodes,'node',id=identifier,name=name,qualified_name=qualified,project_name='Orange3',version='',title=name,position=position)
    links = ET.SubElement(root,'links')
    for destination in ['1','2']:
        ET.SubElement(links,'link',id=destination,source_node_id='0',sink_node_id=destination,source_channel='Data',sink_channel='Data',source_channel_id='data',sink_channel_id='data',enabled='true')
    ET.SubElement(root,'annotations')
    ET.SubElement(root,'thumbnail')
    properties = ET.SubElement(root,'node_properties')
    file_settings = {'recent_paths':[RecentPath('', 'basedir', '../datos/iris/iris.csv')], 'recent_urls':[], 'source':0,'url':'','sheet_names':{},'domain_editor':{},'context_settings':[], '__version__':1}
    for identifier, settings in [('0',file_settings),('1',scatter.settingsHandler.pack_data(scatter)),('2',distributions.settingsHandler.pack_data(distributions))]:
        prop = ET.SubElement(properties,'properties',node_id=identifier,format='pickle')
        prop.text = base64.b64encode(pickle.dumps(settings,protocol=4)).decode('ascii')
    workflow = BASE/'Interpretacion_Iris.ows'
    ET.indent(root)
    ET.ElementTree(root).write(workflow,encoding='utf-8',xml_declaration=True)
    with workflow.open('rb') as stream:
        parse_ows_stream(stream)
    print(json.dumps(metrics,indent=2))


if __name__=='__main__':
    main()
