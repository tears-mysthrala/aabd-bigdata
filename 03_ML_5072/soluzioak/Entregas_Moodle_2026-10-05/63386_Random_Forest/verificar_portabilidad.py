#!/usr/bin/env python3
"""Reabre un .ows trasladado con WidgetsScheme y señales reales, sin inyectar datos."""
from pathlib import Path
import os,shutil,json,csv,time,hashlib,importlib
import numpy as np
from AnyQt.QtWidgets import QApplication
from orangecanvas.registry import WidgetRegistry
from orangewidget.workflow.discovery import widget_desc_from_module
from orangewidget.workflow.widgetsscheme import WidgetsScheme
from orangecanvas.scheme.readwrite import scheme_load
BASE=Path(__file__).resolve().parent

def main():
 c=json.loads((BASE/'config.json').read_text());m=json.loads((BASE/'salidas/metricas.json').read_text())
 moved=BASE/'verificacion/portabilidad';(moved/'datos').mkdir(parents=True,exist_ok=True)
 flow=moved/(c['stem']+'.ows');shutil.copyfile(BASE/flow.name,flow);shutil.copyfile(BASE/'datos/iris.csv',moved/'datos/iris.csv')
 app=QApplication([]);app.setQuitOnLastWindowClosed(False);assert app.platformName()=='wayland'
 registry=WidgetRegistry()
 modules=['Orange.widgets.data.owfile','Orange.widgets.data.owpythonscript','Orange.widgets.evaluate.owtestandscore','Orange.widgets.evaluate.owconfusionmatrix','Orange.widgets.evaluate.owrocanalysis']
 if c['kind']=='tree':modules.append('Orange.widgets.visualize.owtreeviewer')
 for module in modules:registry.register_widget(widget_desc_from_module(importlib.import_module(module)))
 # El cwd es distinto de la carpeta del .ows; basedir representa su ubicación.
 os.chdir(BASE/'verificacion')
 scheme=WidgetsScheme(env={'basedir':str(moved)})
 with flow.open('rb') as f:scheme_load(scheme,f,registry=registry)
 widgets=[scheme.widget_for_node(node) for node in scheme.nodes]
 file_widget=widgets[0];script_widget=widgets[1];score=widgets[2];confusion=widgets[3]
 deadline=time.monotonic()+120
 while True:
  app.processEvents();time.sleep(.03)
  slots=list(score.learners.values())
  ready=slots and all(s.results is not None and s.results.success for s in slots)
  if ready and confusion.results is not None and not scheme.signal_manager.has_pending():break
  if time.monotonic()>deadline:raise TimeoutError('No completó la propagación del workflow trasladado')
 assert file_widget.data is not None and len(file_widget.data)==150
 assert file_widget.last_path()==str(moved/'datos/iris.csv'),file_widget.last_path()
 assert score.NFolds[score.n_folds]==10 and score.cv_stratified
 result=slots[0].results.value;pred=np.empty(150,dtype=int);pred[result.row_indices]=result.predicted[0].astype(int)
 probability=np.empty((150,3));probability[result.row_indices]=result.probabilities[0]
 rows=list(csv.DictReader((BASE/'salidas/predicciones_oof.csv').open()))
 assert len(rows)==150 and sorted(result.row_indices.tolist())==list(range(150))
 for i,row in enumerate(rows):
  assert m['classes'][pred[i]]==row['predicha']
  np.testing.assert_allclose(probability[i],[float(row['p_'+x]) for x in m['classes']],atol=1e-12)
 assert float((pred==file_widget.data.Y).mean())==m['accuracy']
 assert script_widget.text.toPlainText()==(BASE/'modelo_orange.py').read_text()
 # Los widgets de salida reciben datos mediante enlaces cargados del .ows.
 assert confusion.results.predicted.shape==(1,150)
 np.testing.assert_array_equal(confusion.results.predicted,result.predicted)
 assert widgets[4].results is not None and widgets[4].target_index==1
 if c['kind']=='tree':assert widgets[5].model is not None
 evidence=dict(passed=True,method='WidgetsScheme + scheme_load, señales reales; no llamadas manuales set_data/set_learner',workflow=flow.name,relocated_directory=str(moved),cwd=str(Path.cwd()),relative_dataset_resolved=True,rows=150,gui_accuracy=m['accuracy'],all_oof_predictions_match=True,all_oof_probabilities_match=True,downstream_confusion_received=True,roc_target='versicolor',qt_platform=app.platformName(),workflow_sha256=hashlib.sha256(flow.read_bytes()).hexdigest())
 (BASE/'verificacion/portabilidad.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
 for node in list(scheme.nodes):scheme.remove_node(node)
 for w in widgets:w.close()
 app.processEvents();app.quit();print(json.dumps(evidence,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
