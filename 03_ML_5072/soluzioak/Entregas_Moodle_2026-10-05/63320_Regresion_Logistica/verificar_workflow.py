"""Recargar el .ows desde otro directorio y verificar su ejecución real."""
from pathlib import Path
import csv,importlib,json,shutil,tempfile,time
import numpy as np
from AnyQt.QtWidgets import QApplication
from orangecanvas.registry import WidgetRegistry,WidgetDescription
from orangecanvas.scheme.readwrite import parse_ows_stream,scheme_load
from orangewidget.workflow.widgetsscheme import WidgetsScheme
from Orange.widgets.evaluate.owtestandscore import OWTestAndScore
BASE=Path(__file__).resolve().parent
app=QApplication([])
with tempfile.TemporaryDirectory(prefix='orange-workflow-portable-') as location:
    relocated=Path(location)
    shutil.copytree(BASE/'datos',relocated/'datos')
    shutil.copy2(BASE/'Flujo_Orange.ows',relocated/'Flujo_Orange.ows')
    with (relocated/'Flujo_Orange.ows').open('rb') as stream: parsed=parse_ows_stream(stream)
    registry=WidgetRegistry()
    for node in parsed.nodes:
        module,class_name=node.qualified_name.rsplit('.',1)
        cls=getattr(importlib.import_module(module),class_name)
        registry.register_widget(WidgetDescription(**cls.get_widget_description()))
    scheme=WidgetsScheme(env={'basedir':str(relocated)})
    with (relocated/'Flujo_Orange.ows').open('rb') as stream: scheme_load(scheme,stream,registry=registry)
    widgets=[scheme.widget_for_node(node) for node in scheme.nodes]
    score=next(w for w in widgets if isinstance(w,OWTestAndScore))
    deadline=time.monotonic()+90
    while time.monotonic()<deadline:
        app.processEvents();time.sleep(.025)
        slots=list(score.learners.values())
        if slots and slots[0].results and slots[0].results.success and score._OWTestAndScore__task is None:
            result=slots[0].results.value
            # Wait for any pending input signal to settle, then compare the final result.
            end=time.monotonic()+1
            while time.monotonic()<end: app.processEvents();time.sleep(.025)
            slots=list(score.learners.values())
            if slots[0].results and slots[0].results.success: break
    else: raise RuntimeError('El workflow no produjo resultados en 90 segundos')
    result=list(score.learners.values())[0].results.value
    with (BASE/'predicciones_oof.csv').open() as stream: expected=list(csv.DictReader(stream))
    labels=list(result.domain.class_var.values)
    predicted=np.empty(len(expected),int);predicted[result.row_indices]=result.predicted[0].astype(int)
    probability=np.empty((len(expected),len(labels)));probability[result.row_indices]=result.probabilities[0]
    for i,row in enumerate(expected):
        assert labels[predicted[i]]==row['predicho']
        np.testing.assert_allclose(probability[i],[float(row['p_'+v]) for v in labels],rtol=1e-10,atol=1e-10)
    proof={'workflow_loaded_from_relocated_copy':True,'relative_dataset_resolved':True,'native_signal_propagation':True,'predictions_and_probabilities_equal_to_csv':True,'rows':len(expected),'nodes':len(scheme.nodes),'links':len(scheme.links),'CV_folds':score.NFolds[score.n_folds],'stratified':score.cv_stratified}
    (BASE/'evidencias/validacion_workflow.json').write_text(json.dumps(proof,indent=2)+'\n')
    scheme.clear()
    app.processEvents()
    print(json.dumps(proof,indent=2))
