#!/usr/bin/env python3
"""Compare every source row with both Mongo outputs; never print customer data."""
import sys,json,subprocess,hashlib,datetime,itertools
from nifi_lab_verificar import Lab, BASE
l=Lab();result={'source':'create_db.sql imported in MySQL 8.4 (not MariaDB)', 'normalization':'exclude Mongo _id; datetime to ISO seconds; currency floats rounded to two decimal places; all other fields exact','tables':{}}
for table,pk in [('customers','customer_id'),('orders','order_id'),('order_items','order_item_id')]:
 fields=subprocess.run(['docker','exec','-e','MYSQL_PWD='+l.credentials['MYSQL_PASSWORD'],'bigdata-nifi-lab-20261002-mysql','mysql','-uiabd','retail_db','-N','-e',f"SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_SCHEMA='retail_db' AND TABLE_NAME='{table}' ORDER BY ORDINAL_POSITION"],capture_output=True,text=True,check=True).stdout.splitlines()
 query='SELECT JSON_OBJECT('+','.join("'"+f+"',`"+f+'`' for f in fields)+f",'source_table','{table}') FROM `{table}` ORDER BY `{pk}`"
 def normalize(d):
  if 'order_date' in d:d['order_date']=datetime.datetime.fromisoformat(d['order_date']).isoformat(timespec='seconds')
  for field in ['order_item_subtotal','order_item_product_price']:
   if field in d:d[field]=round(float(d[field]),2)
  return json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False)
 source=subprocess.Popen(['docker','exec','-e','MYSQL_PWD='+l.credentials['MYSQL_PASSWORD'],'bigdata-nifi-lab-20261002-mysql','mysql','-uiabd','retail_db','--batch','--raw','--skip-column-names','-e',query],stdout=subprocess.PIPE,text=True)
 source_lines=[normalize(json.loads(line)) for line in source.stdout];assert source.wait()==0
 source_hash=hashlib.sha256(('\n'.join(source_lines)+'\n').encode()).hexdigest();result['tables'][table]={'source_count':len(source_lines),'source_normalized_sha256':source_hash}
 for collection in ['6kasua-classic','6kasua-record']:
  expression=f'const c=db.getSiblingDB("iabd").getCollection("{collection}"); c.find({{source_table:"{table}"}},{{_id:0}}).sort({{"{pk}":1}}).forEach(d=>print(JSON.stringify(d)));'
  target=subprocess.Popen(['docker','exec','bigdata-nifi-lab-20261002-mongo','mongosh','--quiet','--eval',expression],stdout=subprocess.PIPE,text=True)
  h=hashlib.sha256();count=0;mismatches=0
  for reference,line in itertools.zip_longest(source_lines,target.stdout):
   if line is None: mismatches+=1;continue
   normalized=normalize(json.loads(line));h.update((normalized+'\n').encode());count+=1
   mismatches+=(reference!=normalized)
  assert target.wait()==0
  result['tables'][table][collection]={'count':count,'normalized_sha256':h.hexdigest(),'mismatching_rows':mismatches}
  assert count==len(source_lines) and mismatches==0
 print(table,'source',len(source_lines),'all rows equal in both Mongo collections',flush=True)
path=BASE/'06_MariaDB_MongoDB_Laborategia_DF2.2/evidencias/comparacion_contenido_completo.json';path.write_text(json.dumps(result,indent=2)+'\n')
print('All source tables verified')
