#!/usr/bin/env python3
"""Execute cases1-6 once on the dedicated fresh lab; stop own group on exit."""
import json
import shutil
import subprocess
import time
from pathlib import Path
from nifi_lab_verificar import Lab, BASE


def boundary5(l):
    s=json.loads((l.directory/'cases-state.json').read_text());owner=s['owner'];pg=s['groups']['flow_05_csv_json_df2.1'];flow=l.flow(pg)
    base=l.directory/'data'/'case5-boundary';(base/'sarrera').mkdir(parents=True,exist_ok=True);(base/'sarrera').chmod(0o777);(base/'irteera').mkdir(exist_ok=True);(base/'irteera').chmod(0o777)
    source=l.api(f'/process-groups/{owner}/processors','POST',{'revision':{'version':0},'component':{'name':'LAB case5 boundary source','type':'org.apache.nifi.processors.standard.GetFile','bundle':{'group':'org.apache.nifi','artifact':'nifi-standard-nar','version':'2.0.0'},'position':{'x':50,'y':50},'config':{'properties':{'Input Directory':'/opt/nifi/ariketak/case5-boundary/sarrera','Keep Source File':'false'}}}})['id']
    sink=l.api(f'/process-groups/{owner}/processors','POST',{'revision':{'version':0},'component':{'name':'LAB case5 boundary sink','type':'org.apache.nifi.processors.standard.PutFile','bundle':{'group':'org.apache.nifi','artifact':'nifi-standard-nar','version':'2.0.0'},'position':{'x':900,'y':50},'config':{'properties':{'Directory':'/opt/nifi/ariketak/case5-boundary/irteera','Conflict Resolution Strategy':'replace'},'autoTerminatedRelationships':['success','failure']}}})['id']
    inputport=flow['inputPorts'][0]['id'];outputport=flow['outputPorts'][0]['id']
    for src,srcgroup,srctype,dst,dstgroup,dsttype,rel in [(source,owner,'PROCESSOR',inputport,pg,'INPUT_PORT',['success']),(outputport,pg,'OUTPUT_PORT',sink,owner,'PROCESSOR',[])]:
     l.api(f'/process-groups/{owner}/connections','POST',{'revision':{'version':0},'component':{'source':{'id':src,'groupId':srcgroup,'type':srctype},'destination':{'id':dst,'groupId':dstgroup,'type':dsttype},'selectedRelationships':rel}})
    time.sleep(1)
    l.state(pg,'RUNNING');l.processor(sink,'RUNNING');shutil.copyfile(BASE/'05_CSV_JSON_ConvertRecord_DF2.1/sarrera/datuak.csv',base/'sarrera/datuak.csv');l.processor(source,'RUNNING');time.sleep(3);l.processor(source,'STOPPED')
    l.state(pg,'STOPPED');l.processor(sink,'STOPPED')
    s['case5_boundary']={'source':source,'sink':sink,'pg':pg};(l.directory/'cases-state.json').write_text(json.dumps(s,indent=2))
    return {'outputs': [p.name for p in (base/'irteera').glob('*')], 'input_port': l.api('/input-ports/'+inputport)['status'], 'output_port': l.api('/output-ports/'+outputport)['status']}


def mongo_counts():
    expression = ('const d=db.getSiblingDB("iabd"); print(JSON.stringify({'
                  'classic:d.getCollection("6kasua-classic").countDocuments(),'
                  'record:d.getCollection("6kasua-record").countDocuments()}));')
    return json.loads(subprocess.run([
        'docker', 'exec', 'bigdata-nifi-lab-20261002-mongo', 'mongosh', '--quiet',
        '--eval', expression], capture_output=True, text=True, check=True).stdout)


def main():
    lab = Lab()
    state = json.loads((lab.directory/'cases-state.json').read_text())
    if any(mongo_counts().values()):
        raise SystemExit('Mongo output already exists: refusing to duplicate the SQL import')
    try:
        for key, pg in state['groups'].items():
            if not key.startswith(('flow_01', 'flow_02', 'flow_05')):
                continue
            source = next(BASE.glob('0[1-6]*/'+key+'.json')).parent/'sarrera'
            processors = lab.flow(pg)['processors']
            getfile = next(p for p in processors if p['component']['type'].endswith('GetFile'))
            input_path = getfile['component']['config']['properties']['Input Directory']
            host = lab.directory/'data'/input_path.removeprefix('/opt/nifi/ariketak/')
            for file in source.glob('*'):
                if file.is_file():
                    shutil.copyfile(file, host/file.name)
            for p in processors:
                if p != getfile:
                    lab.processor(p['id'], 'RUNNING')
            lab.processor(getfile['id'], 'RUNNING')
        time.sleep(7)
        # The initial writes remain in place: this second input must take failure routing.
        key = 'flow_01_fitxategiak_mugitu'
        pg = state['groups'][key]
        source = next(p for p in lab.flow(pg)['processors'] if p['component']['type'].endswith('GetFile'))
        incoming = source['component']['config']['properties']['Input Directory']
        (lab.directory/'data'/incoming.removeprefix('/opt/nifi/ariketak/')/'proba_01.txt').write_text('LAB conflict: original output must remain unchanged\n')
        lab.processor(source['id'], 'RUNNING')
        for key, pg in state['groups'].items():
            if not key.startswith(('flow_03', 'flow_06')):
                continue
            processors = lab.flow(pg)['processors']
            for p in processors:
                if not p['component']['type'].endswith(('GenerateFlowFile', 'ExecuteSQLRecord')):
                    lab.processor(p['id'], 'RUNNING')
            for p in processors:
                if p['component']['type'].endswith(('GenerateFlowFile', 'ExecuteSQLRecord')):
                    lab.processor(p['id'], 'RUN_ONCE')
        pg = state['groups']['flow_04_mongodb_http']
        lab.state(pg, 'RUNNING')
        time.sleep(1)
        for message in ['INFO: lab ordinary message'] + [f'ERROR: lab event {i}' for i in range(1,6)]:
            result = subprocess.run([
                'docker', 'exec', '-i', 'bigdata-nifi-lab-20261002-nifi', 'curl',
                '-sS', '-w', '%{http_code}', '-X', 'POST', '-H', 'Content-Type: text/plain',
                '--data-binary', '@-', 'http://localhost:8081/iabd'],
                input=message, text=True, capture_output=True, check=True)
            if result.stdout != '200':
                raise RuntimeError('HTTP ingest did not acknowledge the fixture')
        boundary = boundary5(lab)
        (lab.directory/'case5-boundary-status.json').write_text(json.dumps(boundary, indent=2))
        deadline = time.monotonic() + 600
        while time.monotonic() < deadline:
            counts = mongo_counts()
            print('SQL Mongo counts', counts, flush=True)
            if counts == {'classic':253516, 'record':253516}:
                return
            time.sleep(10)
        raise RuntimeError('SQL transfer did not reach full source counts within ten minutes')
    finally:
        lab.state(state['owner'], 'STOPPED')


if __name__ == '__main__':
    main()
