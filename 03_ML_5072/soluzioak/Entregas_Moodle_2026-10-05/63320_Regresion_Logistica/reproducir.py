"""Ejecución nativa Orange y exportación auditada. Ejecutar bajo flock (ver README)."""
from pathlib import Path
import base64, csv, hashlib, json, pickle, platform, time, warnings
import xml.etree.ElementTree as ET
import numpy as np
import Orange, sklearn
from AnyQt.QtWidgets import QApplication
from AnyQt.QtGui import QFont
from Orange.data import Table
from Orange.widgets.data.owfile import OWFile
from Orange.widgets.data.owpreprocess import OWPreprocess
from Orange.widgets.model.owlogisticregression import OWLogisticRegression
from Orange.widgets.model.owknn import OWKNNLearner
from Orange.widgets.evaluate.owtestandscore import OWTestAndScore
from Orange.widgets.evaluate.owconfusionmatrix import OWConfusionMatrix
from Orange.widgets.evaluate.owrocanalysis import OWROCAnalysis
from Orange.evaluation import CrossValidation, CA, AUC, F1, Precision, Recall
from Orange.preprocess import Continuize, Normalize, RemoveNaNColumns, SklImpute
from Orange.classification import LogisticRegressionLearner, KNNLearner
from sklearn.metrics import confusion_matrix, classification_report, balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from orangewidget.utils.filedialogs import RecentPath
from orangecanvas.scheme.readwrite import parse_ows_stream

BASE=Path(__file__).resolve().parent
LOGISTIC='63320' in BASE.name
SOURCE=BASE/'datos'/('wdbc_texture_mean.tab' if LOGISTIC else 'iris.csv')
EVIDENCE=BASE/'evidencias'
EVIDENCE.mkdir(exist_ok=True)
warnings.filterwarnings('ignore',message="'penalty' was deprecated.*",category=FutureWarning)
warnings.filterwarnings('ignore',message="'n_jobs' has no effect.*",category=FutureWarning)

def hashfile(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def wait(app, seconds):
    start=time.monotonic()
    while time.monotonic()-start<seconds:
        app.processEvents(); time.sleep(.02)

def make_widget(cls, settings):
    widget=cls.__new__(cls, stored_settings=settings)
    cls.__init__(widget)
    return widget

def main():
    app=QApplication([])
    app.setFont(QFont('DejaVu Sans',12))
    data=Table(str(SOURCE))
    assert data.X.shape == ((569,1) if LOGISTIC else (150,4))
    assert np.isfinite(data.X).all() and np.isfinite(data.Y).all()
    labels=list(data.domain.class_var.values)
    file=make_widget(OWFile, {'recent_paths':[RecentPath(str(SOURCE), None, None)], 'source':0, 'context_settings':[]})
    file.load_data()
    if LOGISTIC:
        pre=make_widget(OWPreprocess, {'storedsettings':{'name':'','preprocessors':[('orange.preprocess.scale',{'method':2})]},'autocommit':True})
        pre.set_data(data)
        pre.apply()
        modelwidget=make_widget(OWLogisticRegression, {'C_index':61,'penalty_type':1,'class_weight':False,'auto_apply':True,'learner_name':'Logistic Regression'})
        modelwidget.set_preprocessor(pre.buildpreproc())
        modelwidget.handleNewSignals()
        learner=modelwidget.create_learner()
        learner.name='Logistic Regression'
        reference=LogisticRegressionLearner(penalty='l2',C=1,class_weight=None,random_state=42,max_iter=1000,preprocessors=[Continuize(),Normalize(),RemoveNaNColumns(),SklImpute()])
    else:
        pre=None
        modelwidget=make_widget(OWKNNLearner, {'n_neighbors':3,'metric_index':0,'weight_index':0,'auto_apply':True,'learner_name':'kNN'})
        learner=modelwidget.create_learner()
        learner.name='kNN'
        reference=KNNLearner(n_neighbors=3,metric='euclidean',weights='uniform')
    score=make_widget(OWTestAndScore, {'resampling':0,'n_folds':3,'cv_stratified':True})
    score.set_train_data(data)
    score.insert_learner(0,learner)
    score.handleNewSignals()
    deadline=time.monotonic()+120
    while score._OWTestAndScore__task is not None:
        if time.monotonic()>deadline: raise TimeoutError('Test & Score')
        wait(app,.1)
    slot=next(iter(score.learners.values()))
    assert slot.results and slot.results.success, slot.results
    result=slot.results.value
    assert not any(result.failed)
    independent=CrossValidation(k=10,stratified=True,random_state=42,store_data=True)(data,[reference])
    np.testing.assert_array_equal(result.row_indices,independent.row_indices)
    np.testing.assert_array_equal(result.predicted,independent.predicted)
    np.testing.assert_allclose(result.probabilities,independent.probabilities,rtol=1e-10,atol=1e-10)
    ix=np.asarray(result.row_indices,int)
    assert sorted(ix.tolist())==list(range(len(data)))
    np.testing.assert_array_equal(result.actual,data.Y[ix])
    prediction=np.empty(len(data),int); prediction[ix]=result.predicted[0].astype(int)
    probs=np.empty((len(data),len(labels))); probs[ix]=result.probabilities[0]
    folds=np.empty(len(data),int)
    for f, sl in enumerate(result.folds,1): folds[ix[sl]]=f
    for f,(train,test) in enumerate(StratifiedKFold(10,shuffle=True,random_state=42).split(data.X,data.Y),1):
        np.testing.assert_array_equal(np.flatnonzero(folds==f),test)
        assert not set(train)&set(test)
    out=BASE/'predicciones_oof.csv'
    with out.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.writer(stream,lineterminator='\n')
        writer.writerow(['row_id','fold',*[v.name for v in data.domain.attributes],'real','predicho','acierto',*['p_'+v for v in labels]])
        for i in range(len(data)): writer.writerow([i+1,folds[i],*data.X[i],labels[int(data.Y[i])],labels[prediction[i]],int(prediction[i]==data.Y[i]),*probs[i]])
    with out.open() as stream: rows=list(csv.DictReader(stream))
    for i,row in enumerate(rows):
        assert int(row['row_id'])==i+1 and row['real']==labels[int(data.Y[i])]
        np.testing.assert_array_equal([float(row[v.name]) for v in data.domain.attributes],data.X[i])
        assert int(row['acierto'])==int(row['real']==row['predicho'])
    cm=confusion_matrix(data.Y.astype(int),prediction,labels=range(len(labels)))
    assert int(cm.sum())==len(data) and np.trace(cm)/len(data)==float(CA(result)[0])
    confusion=make_widget(OWConfusionMatrix, {'selected_learner':[0],'quantity':0})
    confusion.set_results(result)
    widgets=[('orange_file.png',file),('orange_modelo.png',modelwidget)]
    if pre: widgets.append(('orange_preprocess.png',pre))
    widgets.extend([('orange_test_score.png',score),('orange_confusion.png',confusion)])
    roc=None
    if LOGISTIC:
        roc=OWROCAnalysis()
        roc.set_results(result)
        roc.target_index=labels.index('M')
        roc._on_target_changed()
        widgets.append(('orange_roc.png',roc))
    for name,widget in widgets:
        widget.setFixedSize(1100,700)
        widget.show(); wait(app,1.0)
        assert widget.grab().save(str(EVIDENCE/name))
        widget.hide()
    report=classification_report(data.Y.astype(int),prediction,target_names=labels,output_dict=True,zero_division=0)
    metrics={'author':'Unai Urzainqui Perez','task':63320 if LOGISTIC else 63321,'rows':len(data),'features':[v.name for v in data.domain.attributes],'classes':labels,'class_counts':{v:int((data.Y==i).sum()) for i,v in enumerate(labels)},'missing':0,'CA':float(CA(result)[0]),'AUC_Orange_weighted':float(AUC(result)[0]),'F1_weighted':float(report['weighted avg']['f1-score']),'precision_weighted':float(report['weighted avg']['precision']),'recall_weighted':float(report['weighted avg']['recall']),'balanced_accuracy':float(balanced_accuracy_score(data.Y,prediction)),'confusion_matrix':cm.tolist(),'classification_report':report,'error_row_ids':(np.flatnonzero(prediction!=data.Y)+1).tolist(),'protocol':{'folds':10,'stratified':True,'shuffle':True,'seed':42,'preprocessing_inside_training_fold':True,'scaling':bool(LOGISTIC)},'learner_params':{k:v for k,v in (learner.params if LOGISTIC else learner.get_params('classification')).items() if isinstance(v,(str,int,float,bool,type(None)))},'versions':{'Orange':Orange.__version__,'sklearn':sklearn.__version__,'numpy':np.__version__,'python':platform.python_version()},'source_sha256':hashfile(SOURCE),'oof_sha256':hashfile(out),'verification':{'native_Test_and_Score_run':True,'API_reference_probabilities_equal':True,'each_row_once':True,'source_row_label_alignment':True,'folds_match_StratifiedKFold':True},'capture_method':'Native Orange widgets shown on Wayland; QWidget.grab(); no reconstructed screenshot'}
    if LOGISTIC:
        positive=labels.index('M')
        metrics['AUC_M']=float(roc_auc_score(data.Y==positive,probs[:,positive]))
        metrics['texture_means']={v:float(data.X[data.Y==i,0].mean()) for i,v in enumerate(labels)}
        metrics['majority_baseline']=357/569
    else: metrics['majority_baseline']=1/3
    (BASE/'resultados.json').write_text(json.dumps(metrics,indent=2,ensure_ascii=False)+'\n')
    root=ET.Element('scheme',version='2.0',title=('Regresión Logística WDBC' if LOGISTIC else 'KNN Iris'),description='Unai Urzainqui Perez. CV estratificada 10 folds, semilla 42; resultados OOF.')
    nodes=ET.SubElement(root,'nodes')
    objects={'0':file,'1':modelwidget,'2':score,'3':confusion}
    if pre: objects['4']=pre
    if roc: objects['5']=roc
    for i,w in objects.items(): ET.SubElement(nodes,'node',id=i,name=w.name,qualified_name=type(w).__module__+'.'+type(w).__name__,project_name='Orange3',version='',title=w.name,position=str((100+int(i)*190,150 if int(i)%2==0 else 330)))
    links=ET.SubElement(root,'links')
    specs=[('0','2','Data','Data','data','train_data'),('1','2','Learner','Learner','learner','learner'),('2','3','Evaluation Results','Evaluation Results','evaluations_results','evaluation_results')]
    if pre: specs.extend([('0','4','Data','Data','data','data'),('4','1','Preprocessor','Preprocessor','preprocessor','preprocessor')])
    if roc: specs.append(('2','5','Evaluation Results','Evaluation Results','evaluations_results','evaluation_results'))
    for i,(s,t,sc,tc,si,ti) in enumerate(specs): ET.SubElement(links,'link',id=str(i),source_node_id=s,sink_node_id=t,source_channel=sc,sink_channel=tc,source_channel_id=si,sink_channel_id=ti,enabled='true')
    ET.SubElement(root,'annotations'); ET.SubElement(root,'thumbnail')
    properties=ET.SubElement(root,'node_properties')
    settings_evidence={}
    for i,w in objects.items():
        packed=w.settingsHandler.pack_data(w)
        if i=='0': packed.update(recent_paths=[RecentPath('','basedir',str(SOURCE.relative_to(BASE)))],context_settings=[])
        settings_evidence[i]={'widget':w.name,'n_folds':packed.get('n_folds'),'cv_stratified':packed.get('cv_stratified'),'C_index':packed.get('C_index'),'penalty_type':packed.get('penalty_type'),'n_neighbors':packed.get('n_neighbors'),'metric_index':packed.get('metric_index'),'weight_index':packed.get('weight_index'),'preprocessors':packed.get('storedsettings',{}).get('preprocessors')}
        ET.SubElement(properties,'properties',node_id=i,format='pickle').text=base64.b64encode(pickle.dumps(packed,protocol=4)).decode('ascii')
    ET.indent(root)
    workflow=BASE/'Flujo_Orange.ows'
    ET.ElementTree(root).write(workflow,encoding='utf-8',xml_declaration=True)
    with workflow.open('rb') as stream:
        parsed=parse_ows_stream(stream)
        assert len(parsed.nodes)==len(objects) and len(parsed.links)==len(specs)
    (EVIDENCE/'settings_gui.json').write_text(json.dumps(settings_evidence,indent=2,ensure_ascii=False)+'\n')
    for w in objects.values(): w.close(); w.onDeleteWidget()
    app.processEvents()
    print(json.dumps(metrics,indent=2,ensure_ascii=False))

if __name__=='__main__': main()
