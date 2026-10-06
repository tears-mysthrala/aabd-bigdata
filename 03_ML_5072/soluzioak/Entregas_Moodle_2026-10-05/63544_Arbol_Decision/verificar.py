#!/usr/bin/env python3
"""Verifica artefactos entregados sin volver a entrenar ni alterar resultados."""
from pathlib import Path
import json,csv,hashlib,base64,pickle,xml.etree.ElementTree as ET
from collections import Counter
import subprocess,sys
BASE=Path(__file__).resolve().parent
c=json.loads((BASE/'config.json').read_text());m=json.loads((BASE/'salidas/metricas.json').read_text())
rows=list(csv.DictReader((BASE/'salidas/predicciones_oof.csv').open()))
assert len(rows)==150 and [int(r['row_id']) for r in rows]==list(range(1,151))
raw=list(csv.reader((BASE/'datos/iris.csv').open()))[3:];assert len(raw)==150
assert Counter(r['real'] for r in rows)==dict.fromkeys(m['classes'],50)
cm=[[0]*3 for _ in range(3)]
for row,source in zip(rows,raw):
 assert [float(row[k]) for k in ['sepal_length','sepal_width','petal_length','petal_width']]==[float(x) for x in source[:4]]
 assert row['real']==source[4]
 assert abs(sum(float(row['p_'+label]) for label in m['classes'])-1)<1e-8
 assert int(row['acierto'])==int(row['real']==row['predicha'])
 cm[m['classes'].index(row['real'])][m['classes'].index(row['predicha'])]+=1
for fold in range(1,11):
 held=[r for r in rows if int(r['fold'])==fold];assert len(held)==15
 assert Counter(r['real'] for r in held)==dict.fromkeys(m['classes'],5)
assert cm==m['confusion_matrix'] and sum(cm[i][i] for i in range(3))/150==m['accuracy']
for path,expected in m['sha256'].items():assert hashlib.sha256((BASE/path).read_bytes()).hexdigest()==expected
for rec in m['capture']['files']:
 p=BASE/rec['file'];assert p.read_bytes().startswith(b'\x89PNG\r\n\x1a\n');assert hashlib.sha256(p.read_bytes()).hexdigest()==rec['sha256'] and rec['displayed']
assert m['capture']['platform']=='wayland'
if c['kind']=='svm':assert len(m['scaling_fold_audit'])==10 and all(x['training_only'] for x in m['scaling_fold_audit'])
# Se deserializan exclusivamente propiedades pickle generadas por este proyecto.
# Orange es necesario para leer RecentPath: ejecutar con el entorno de Orange.
root=ET.parse(BASE/(c['stem']+'.ows')).getroot()
props={p.attrib['node_id']:pickle.loads(base64.b64decode(p.text)) for p in root.find('node_properties')}
assert props['1']['scriptText']==(BASE/'modelo_orange.py').read_text()
assert props['2']['n_folds']==3 and props['2']['cv_stratified']
assert props['0']['recent_paths'][0].relpath=='datos/iris.csv'
pdf=BASE/(c['stem']+'.pdf');info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
pages=int(next(line.split(':')[1] for line in info.splitlines() if line.startswith('Pages:')))
assert pages==5
text=subprocess.check_output(['pdftotext',str(pdf),'-'],text=True)
assert '150' in text and 'Test' in text
result=dict(passed=True,rows=150,folds=10,rows_per_fold=15,classes_per_fold=5,confusion_sum=150,pdf_pages=pages,pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),dataset_sha256=hashlib.sha256((BASE/'datos/iris.csv').read_bytes()).hexdigest(),workflow_parameters_match=True,native_capture_count=len(m['capture']['files']),capture_hashes_match=True)
print(json.dumps(result,indent=2))
if '--record' in sys.argv:(BASE/'verificacion/verificacion.json').write_text(json.dumps(result,indent=2)+'\n')
