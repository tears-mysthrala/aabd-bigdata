#!/usr/bin/env python3
"""Save scoped statuses and bounded provenance, releasing query results only."""
import sys,json,time,collections,subprocess
from nifi_lab_verificar import Lab, BASE
l=Lab();s=json.loads((l.directory/'cases-state.json').read_text())
for key,pg in s['groups'].items():
 folder=next(BASE.glob('0[1-6]*/'+key+'.json')).parent/'evidencias';folder.mkdir(exist_ok=True)
 (folder/(key+'_status.json')).write_text(json.dumps(l.status(pg),indent=2))
 events=[]
 for p in l.flow(pg)['processors']:
  query=l.api('/provenance','POST',{'provenance':{'request':{'searchTerms':{'ProcessorID':{'value':p['id'],'inverse':False}},'maxResults':100}}})
  qid=query['provenance']['id']
  for _ in range(50):
   query=l.api('/provenance/'+qid)
   if query['provenance']['finished']:break
   time.sleep(.1)
  for event in query['provenance']['results']['provenanceEvents']:
   for field in ['childUuids', 'parentUuids']:
    if len(event.get(field, [])) > 20:
     event[field + 'TotalCount'] = len(event[field])
     event[field] = event[field][:20]
   events.append(event)
  l.api('/provenance/'+qid,'DELETE')
 summary=collections.Counter((e['componentName'],e['eventType']) for e in events)
 (folder/(key+'_provenance.json')).write_text(json.dumps({'query_limit_per_processor':100,'events':events,'counts_in_saved_sample':{' | '.join(k):v for k,v in summary.items()}},indent=2))
 print(key,len(events),dict(summary),flush=True)
