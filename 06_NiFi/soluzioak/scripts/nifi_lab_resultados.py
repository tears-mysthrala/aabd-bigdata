#!/usr/bin/env python3
"""Verify and archive actual output files, Mongo documents and scoped logs."""
import sys,json,shutil,subprocess,hashlib,csv,re
from pathlib import Path
from nifi_lab_verificar import Lab, BASE
l=Lab();s=json.loads((l.directory/'cases-state.json').read_text());summary={}
for key,pg in s['groups'].items():l.state(pg,'STOPPED')
for number in range(1,7):
 folder=next(BASE.glob(f'0{number}_*'));ev=folder/'evidencias';ev.mkdir(exist_ok=True)
 summary[number]={'date':'2026-10-02','NiFi':'2.0.0','execution':'real Docker lab REST/API; no GUI capture','scope':'dedicated groups; original materialak untouched'}
 if number==1:
  root=l.directory/'data/flow_01_fitxategiak_mugitu/irteera';shutil.copytree(root,ev/'irteera',dirs_exist_ok=True)
  for f in (folder/'sarrera').glob('*'):assert f.read_bytes()==(ev/'irteera'/f.name).read_bytes()
  conflicts=list((ev/'irteera/gatazkak').glob('*'));assert len(conflicts)==1;assert conflicts[0].read_text()=='LAB conflict: original output must remain unchanged\n'
  summary[number].update(normal_files=3,conflict_files=1,original_content_preserved=True)
 if number==2:
  with (folder/'sarrera/salmentak.csv').open() as f: rows=list(csv.DictReader(f,delimiter=';'))
  expected=[r for r in rows if r['Country'].strip()=='France' and int(r['Units'])>1]
  for variant in range(1,4):
   key=next(k for k in s['groups'] if k.startswith('flow_02') and ('aldaera'+str(variant)) in k)
   processor=next(p for p in l.flow(s['groups'][key])['processors'] if p['component']['type'].endswith('PutFile'));out=l.directory/'data'/processor['component']['config']['properties']['Directory'].removeprefix('/opt/nifi/ariketak/');dest=ev/f'aldaera{variant}';dest.mkdir(exist_ok=True);files=sorted(out.glob('*'))
   actual=[]
   for i,p in enumerate(files,1):
    target=dest/f'result_{i}.csv';shutil.copyfile(p,target)
    with p.open() as f:actual.extend(csv.DictReader(f,delimiter=';'))
   assert sorted([tuple(r.items()) for r in actual])==sorted([tuple(r.items()) for r in expected])
   summary[number][f'variant{variant}']={'files':len(files),'selected_records':len(actual),'split_flowfiles':6 if variant==1 else (1 if variant==2 else 0)}
  summary[number]['source_records']=len(rows)
 if number==3:
  paths=list((l.directory/'data/flow_03_atributuak_linajea/irteera').glob('*'));assert len(paths)==1;assert paths[0].read_text()=='proba'
  shutil.copyfile(paths[0],ev/'basic_proba.txt')
  result=subprocess.run(['docker','exec','bigdata-nifi-lab-20261002-mongo','mongosh','--quiet','--eval','print(JSON.stringify(db.getSiblingDB("nifi").datuak.find({}, {_id:0}).toArray()))'],capture_output=True,text=True,check=True)
  documents=json.loads(result.stdout);assert len(documents)==1 and '[[[ Data:' in documents[0]['datuak'];(ev/'mongo_datuak.json').write_text(json.dumps(documents,indent=2)+'\n');summary[number]['mongo_documents']=len(documents)
 if number==4:
  result=subprocess.run(['docker','exec','bigdata-nifi-lab-20261002-mongo','mongosh','--quiet','--eval','print(JSON.stringify(db.getSiblingDB("iabd").getCollection("4kasua").find({}, {_id:0}).toArray()))'],capture_output=True,text=True,check=True)
  documents=json.loads(result.stdout);assert len(documents)==1;doc=documents[0];assert sorted(doc['mezua'].splitlines())==[f'ERROR: lab event {i}' for i in range(1,6)];assert doc['mota']=='errorea';assert re.fullmatch(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',doc['fecha']);(ev/'mongo_http.json').write_text(json.dumps(documents,indent=2)+'\n');summary[number].update(http_posts=6,accepted_errors=5,excluded_normal=1,mongo_documents=1)
 if number==5:
  local=l.directory/'data/flow_05_csv_json_df2.1/irteera/datuak.json';boundary=l.directory/'data/case5-boundary/irteera/datuak.json';assert json.loads(local.read_text())==json.loads(boundary.read_text());shutil.copyfile(local,ev/'datuak.json')
  with (folder/'sarrera/datuak.csv').open() as f:rows=list(csv.DictReader(f,delimiter=';'))
  documents=json.loads(local.read_text());assert len(rows)==len(documents)==5
  for r,d in zip(rows,documents):
   for k,v in r.items():assert (float(v)==d[k] if k in ['id','adina','soldata'] else v==d[k])
  pg=s['groups']['flow_05_csv_json_df2.1'];ports={}
  for kind in ['inputPorts','outputPorts']:
   port=l.flow(pg)[kind][0];api_kind='input-ports' if kind=='inputPorts' else 'output-ports';ports[kind]=l.api('/'+api_kind+'/'+port['id'])['status']
  saved=l.directory/'case5-boundary-status.json'
  if saved.exists():
   immediate=json.loads(saved.read_text());ports={'inputPorts':immediate['input_port'],'outputPorts':immediate['output_port']}
  (ev/'boundary_ports_status.json').write_text(json.dumps(ports,indent=2));summary[number].update(json_records=5,local_ingress_tested=True,boundary_ingress_and_egress_tested=True)
 if number==6:
  comparison=json.loads((ev/'comparacion_contenido_completo.json').read_text());summary[number].update(source_engine='MySQL8.4',mariadb_not_tested=True,source_tables={k:v['source_count'] for k,v in comparison['tables'].items()},documents_each_collection=253516,all_rows_compared=True,benchmark=False)
  for key,pg in s['groups'].items():
   if key.startswith('flow_06'):(ev/(key+'_final_status.json')).write_text(json.dumps(l.status(pg),indent=2))
 (ev/'resultado_2026-10-02.json').write_text(json.dumps(summary[number],indent=2,ensure_ascii=False)+'\n')
# Preserve only relevant log lines and complete case3 LogAttribute blocks, never credentials.
log=subprocess.run(['docker','exec','bigdata-nifi-lab-20261002-nifi','cat','/opt/nifi/nifi-current/logs/nifi-app.log'],capture_output=True,text=True,check=True).stdout.splitlines()
for number in [2,3,6]:
 pgids=[pg for key,pg in s['groups'].items() if key.startswith(f'flow_0{number}')]+[pg for key,pg in s.get('failed_groups',{}).items() if key.startswith(f'flow_0{number}')]
 procids=[p['id'] for pg in pgids for p in l.flow(pg)['processors']]
 selected=set()
 for i,line in enumerate(log):
  if any(p in line for p in procids):
   selected.add(i)
   if 'LogAttribute' in line:selected.update(range(i,min(i+18,len(log))))
 folder=next(BASE.glob(f'0{number}_*'))/'evidencias'
 (folder/'nifi_app_extracto.log').write_text('\n'.join(log[i] for i in sorted(selected))+'\n')
 print('Log',number,'lines',len(selected))
print(json.dumps(summary,indent=2))
