#!/usr/bin/env python3
"""CV Orange real, widgets nativos Wayland y flujo autocontenido. Ejecutar bajo flock."""
from pathlib import Path
import csv,json,hashlib,platform,time,base64,pickle,xml.etree.ElementTree as ET
import numpy as np
import Orange,sklearn
from Orange.data import Table
from Orange.evaluation import CrossValidation,CA,F1,AUC
from sklearn.datasets import load_iris
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.model_selection import StratifiedKFold
from AnyQt.QtWidgets import QApplication
from AnyQt.QtGui import QFont
from Orange.widgets.data.owpythonscript import OWPythonScript
from Orange.widgets.evaluate.owtestandscore import OWTestAndScore
from Orange.widgets.evaluate.owconfusionmatrix import OWConfusionMatrix
from Orange.widgets.evaluate.owrocanalysis import OWROCAnalysis
from Orange.widgets.visualize.owtreeviewer import OWTreeGraph
from orangewidget.utils.filedialogs import RecentPath
from orangecanvas.scheme.readwrite import parse_ows_stream
BASE=Path(__file__).resolve().parent

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    config=json.loads((BASE/'config.json').read_text())
    app=QApplication([]); app.setQuitOnLastWindowClosed(False); app.setFont(QFont('DejaVu Sans',12))
    data=Table(str(BASE/'datos/iris.csv')); ref=load_iris(); labels=list(data.domain.class_var.values)
    np.testing.assert_array_equal(data.X,ref.data); np.testing.assert_array_equal(data.Y,ref.target)
    assert labels==list(ref.target_names) and data.X.shape==(150,4) and np.isfinite(data.X).all()
    script=(BASE/'modelo_orange.py').read_text()
    native=OWPythonScript(); native.text.setPlainText(script); native.insert_data(0,data); native.commit()
    learner=native.console.locals['out_learner']; model=native.console.locals['out_classifier']
    assert learner is not None and model is not None
    score=OWTestAndScore(); score.n_folds=3; score.resampling=0; score.cv_stratified=True
    score.set_train_data(data); score.insert_learner(0,learner); score.handleNewSignals()
    deadline=time.monotonic()+120
    while not all(s.results is not None for s in score.learners.values()):
        app.processEvents(); time.sleep(.03)
        if time.monotonic()>deadline: raise TimeoutError('Orange GUI CV')
    slot=next(iter(score.learners.values())); assert slot.results.success,slot.results
    results=slot.results.value
    assert results.predicted.shape==(1,150)
    # Independent API run must reproduce the widget, including probabilities.
    independent=CrossValidation(k=10,stratified=True,random_state=42,store_data=True,store_models=True)(data,[learner])
    np.testing.assert_array_equal(results.row_indices,independent.row_indices)
    np.testing.assert_array_equal(results.predicted,independent.predicted)
    np.testing.assert_allclose(results.probabilities,independent.probabilities,atol=1e-12)
    idx=results.row_indices; assert sorted(idx.tolist())==list(range(150))
    np.testing.assert_array_equal(results.actual,data.Y[idx])
    pred=np.empty(150,dtype=int); pred[idx]=results.predicted[0].astype(int)
    prob=np.empty((150,3));prob[idx]=results.probabilities[0]
    fold_ids=np.empty(150,dtype=int)
    for fold,positions in enumerate(results.folds,1): fold_ids[idx[positions]]=fold
    scaling_audit=[]
    for fold,(train,test) in enumerate(StratifiedKFold(10,shuffle=True,random_state=42).split(data.X,data.Y),1):
        np.testing.assert_array_equal(np.flatnonzero(fold_ids==fold),test)
        assert len(test)==15 and not set(train)&set(test)
        assert np.bincount(data.Y[test].astype(int)).tolist()==[5,5,5]
        if config['kind']=='svm':
            folded=independent.models[fold-1,0]
            offsets=np.array([v.compute_value.offset for v in folded.domain.attributes])
            factors=np.array([v.compute_value.factor for v in folded.domain.attributes])
            np.testing.assert_allclose(offsets,data.X[train].mean(axis=0),atol=1e-10)
            np.testing.assert_allclose(factors,1/data.X[train].std(axis=0),atol=1e-10)
            assert not np.allclose(offsets,data.X.mean(axis=0),atol=1e-10)
            scaling_audit.append(dict(fold=fold,train_rows=len(train),means=offsets.tolist(),factors=factors.tolist(),training_only=True))
    with (BASE/'salidas/predicciones_oof.csv').open('w',newline='') as f:
        writer=csv.writer(f); writer.writerow(['row_id','fold',*[v.name for v in data.domain.attributes],'real','predicha','acierto',*['p_'+s for s in labels]])
        for i in range(150): writer.writerow([i+1,fold_ids[i],*data.X[i],labels[int(data.Y[i])],labels[pred[i]],int(pred[i]==data.Y[i]),*prob[i]])
    exported=list(csv.DictReader((BASE/'salidas/predicciones_oof.csv').open())); assert len(exported)==150
    for i,row in enumerate(exported):
        assert int(row['row_id'])==i+1 and int(row['fold'])==fold_ids[i]
        assert row['real']==labels[int(data.Y[i])] and row['predicha']==labels[pred[i]]
        np.testing.assert_array_equal([float(row[v.name]) for v in data.domain.attributes],data.X[i])
    cm=confusion_matrix(data.Y,pred,labels=range(3)); assert cm.sum()==150 and cm.sum(axis=1).tolist()==[50]*3
    errors=[dict(row_id=int(i+1),real=labels[int(data.Y[i])],predicha=labels[pred[i]],fold=int(fold_ids[i]),features=data.X[i].tolist()) for i in np.flatnonzero(pred!=data.Y)]
    report=classification_report(data.Y,pred,target_names=labels,output_dict=True)
    metrics=dict(title=config['title'],dataset='Iris: UCI / Fisher (1936), copia local verificada contra sklearn.load_iris',rows=150,features=4,classes=labels,class_counts=[50]*3,
      accuracy=float(CA(results)[0]),f1_weighted=float(F1(results,average="weighted")[0]),f1_macro=report['macro avg']['f1-score'],auc_weighted=float(AUC(results)[0]),confusion_matrix=cm.tolist(),classification_report=report,errors=errors,
      protocol=dict(folds=10,stratified=True,shuffle=True,random_state=42,fold_test_rows=15,fold_train_rows=135,each_row_evaluated_once=True,external_test=False),
      model=config['parameters'],preprocessors=[type(p).__name__ for p in learner.preprocessors],versions=dict(Orange=Orange.__version__,sklearn=sklearn.__version__,numpy=np.__version__,python=platform.python_version()),
      validation=dict(source_equals_sklearn=True,oof_file_reread=True,fold_ids_verified=True,gui_equals_independent_api=True,probability_gui_equals_api=True),
      capture=dict(platform=app.platformName(),method='Widgets nativos Orange mostrados en Wayland; QWidget.grab(); sin recreación de interfaz',files=[]))
    metrics['scaling_fold_audit']=scaling_audit
    assert metrics['capture']['platform']=='wayland'
    confusion=OWConfusionMatrix();confusion.set_results(results);confusion.handleNewSignals()
    roc=OWROCAnalysis();roc.set_results(results);roc.handleNewSignals();roc.target_index=1;roc._on_target_changed()
    widgets=[('orange_modelo.png',native),('orange_test_score.png',score),('orange_confusion.png',confusion),('orange_roc.png',roc)]
    viewer=None
    if config['kind']=='tree':
        viewer=OWTreeGraph();viewer.ctree(model);widgets.append(('orange_tree_viewer.png',viewer))
        (BASE/'salidas/arbol.txt').write_text(model.print_tree() if hasattr(model,'print_tree') else str(model))
    # Capture only own widgets and close them immediately.
    for filename,widget in widgets:
        widget.setFixedSize(1100,800);widget.show()
        until=time.monotonic()+1.2
        while time.monotonic()<until:app.processEvents();time.sleep(.02)
        assert widget.isVisible() and widget.windowHandle().isVisible()
        assert widget.grab().save(str(BASE/'capturas'/filename))
        metrics['capture']['files'].append(dict(file='capturas/'+filename,sha256=digest(BASE/'capturas'/filename),widget=type(widget).__name__,displayed=True))
        widget.hide()
    root=ET.Element('scheme',version='2.0',title=config['title'],description='Iris 150; CV estratificada 10 folds semilla 42; learner del script incluido')
    nodes=ET.SubElement(root,'nodes')
    entries=[('0','File','Orange.widgets.data.owfile.OWFile',(80,200),None),('1','Python Script','Orange.widgets.data.owpythonscript.OWPythonScript',(330,280),native),('2','Test and Score','Orange.widgets.evaluate.owtestandscore.OWTestAndScore',(600,160),score),('3','Confusion Matrix','Orange.widgets.evaluate.owconfusionmatrix.OWConfusionMatrix',(860,100),confusion),('4','ROC Analysis','Orange.widgets.evaluate.owrocanalysis.OWROCAnalysis',(860,250),roc)]
    if viewer: entries.append(('5','Tree Viewer','Orange.widgets.visualize.owtreeviewer.OWTreeGraph',(600,420),viewer))
    for identifier,name,qualified,pos,w in entries:ET.SubElement(nodes,'node',id=identifier,name=name,qualified_name=qualified,project_name='Orange3',version='',title=name,position=str(tuple(float(x) for x in pos)))
    links=ET.SubElement(root,'links');connections=[('0','1','Data','Data','data','data'),('0','2','Data','Data','data','train_data'),('1','2','Learner','Learner','learner','learner'),('2','3','Evaluation Results','Evaluation Results','evaluations_results','evaluation_results'),('2','4','Evaluation Results','Evaluation Results','evaluations_results','evaluation_results')]
    if viewer:connections.append(('1','5','Classifier','Tree','classifier','tree'))
    for i,(s,t,sc,tc,si,ti) in enumerate(connections):ET.SubElement(links,'link',id=str(i),source_node_id=s,sink_node_id=t,source_channel=sc,sink_channel=tc,source_channel_id=si,sink_channel_id=ti,enabled='true')
    ET.SubElement(root,'annotations');ET.SubElement(root,'thumbnail');properties=ET.SubElement(root,'node_properties')
    for identifier,name,qualified,pos,w in entries:
        settings=w.settingsHandler.pack_data(w) if w else dict(recent_paths=[RecentPath('','basedir','datos/iris.csv')],recent_urls=[],source=0,url='',sheet_names={},domain_editor={},context_settings=[],__version__=1)
        if identifier=='1':settings.update(scriptText=script,scriptLibrary=[dict(name=config['title'],script=script,filename=None)],currentScriptIndex=0)
        prop=ET.SubElement(properties,'properties',node_id=identifier,format='pickle');prop.text=base64.b64encode(pickle.dumps(settings,protocol=4)).decode()
    ET.indent(root);workflow=BASE/(config['stem']+'.ows');ET.ElementTree(root).write(workflow,encoding='utf-8',xml_declaration=True)
    with workflow.open('rb') as f:parse_ows_stream(f)
    metrics['workflow']=dict(file=workflow.name,relative_dataset='datos/iris.csv',script_equals_model_file=True,test_score_settings=dict(n_folds_index=3,NFolds_value=10,cv_stratified=True,random_state_implementation=42))
    metrics['sha256']={p.relative_to(BASE).as_posix():digest(p) for p in [BASE/'datos/iris.csv',BASE/'modelo_orange.py',BASE/'salidas/predicciones_oof.csv',workflow]}
    (BASE/'salidas/metricas.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
    for _,w in widgets:w.close();w.onDeleteWidget()
    app.quit();print(json.dumps({k:metrics[k] for k in ['title','accuracy','f1_weighted','f1_macro','confusion_matrix','validation']},indent=2))
if __name__=='__main__':main()
