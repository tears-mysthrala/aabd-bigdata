"""Prueba E2E real en el Compose DEDICADO del caso 3.

Precondición: topics nuevos y colección vacía. No borra datos ni levanta otros
servicios. Usa fixture sintética o API Open-Meteo explícita, API admin, seis
scripts CLI, lectura independiente y MongoDB.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from kafka import KafkaConsumer, TopicPartition
from kafka.admin import KafkaAdminClient, NewTopic
from pymongo import MongoClient

from pipeline import BRONZE, SILVER, GOLD, to_gold

BASE = Path(__file__).resolve().parent


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', choices=['synthetic','open-meteo'], default='synthetic')
    p.add_argument('--bootstrap', default='127.0.0.1:29092')
    p.add_argument('--mongo-uri', default='mongodb://127.0.0.1:27027')
    p.add_argument('--output', type=Path, default=BASE/'evidencias')
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    admin = KafkaAdminClient(bootstrap_servers=args.bootstrap)
    present = admin.list_topics()
    assert not set([BRONZE, SILVER, GOLD]).intersection(present), 'Usar laboratorio nuevo, sin topics previos'
    admin.create_topics([NewTopic(topic, num_partitions=1, replication_factor=2) for topic in [BRONZE, SILVER, GOLD]])
    topics = admin.describe_topics([BRONZE, SILVER, GOLD])
    admin.close()
    fixture = [dict(municipio={'NOMBRE': 'Elche/Elx'}, temperatura_actual=str(10+i), humedad=str(40+i),
                    fixture=True, measurement=i, extra={'preserved': True}) for i in range(20)]
    fixture_path = args.output/'bronze_fixture.jsonl'
    if args.source=='synthetic':
        fixture_path.write_text(''.join(json.dumps(row)+'\n' for row in fixture))
    client = MongoClient(args.mongo_uri)
    collection = client.iabd.aemet_zilarra
    assert collection.count_documents({}) == 0, 'Usar MongoDB dedicado y vacío'
    logs = {}
    children = []
    common = ['--bootstrap', args.bootstrap, '--max', '20', '--idle-timeout', '90']
    def start(name, extra=()):
        process = subprocess.Popen([sys.executable, str(BASE/name), *common, *extra], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        children.append(process)
        return process
    try:
        # Primera parte: Silver escribe también MongoDB; Gold se suscribe antes del producer.
        gold = start('prozesatu_urrea.py')
        silver = start('prozesatu_zilarra.py', ['--mongo-uri', args.mongo_uri])
        producer_args = ['--fixture', str(fixture_path), '--interval', '0'] if args.source=='synthetic' else ['--provider','open-meteo','--interval','0.5']
        producer = start('producer_brontzea.py', producer_args)
        for name, process in [('bronze',producer),('silver',silver),('gold',gold)]:
            out, err = process.communicate(timeout=120)
            assert process.returncode == 0, (name, out, err)
            logs[name] = out
        assert collection.count_documents({}) == 20
        # Segunda parte: tres grupos distintos consumen los mismos veinte Silver.
        output = args.output/'silver_datuak.jsonl'
        assert not output.exists(), 'Salida ya existe; usar carpeta nueva'
        file_consumer = start('kontsumitzaileZilarraFitxategia.py', ['--output', str(output)])
        mongo_consumer = start('kontsumitzaileZilarraMongoDB.py', ['--mongo-uri', args.mongo_uri])
        independent_gold = start('kontsumitzaileZilarra_EkoizleaUrrea.py')
        for name, process in [('jsonl',file_consumer),('mongo',mongo_consumer),('independent_gold',independent_gold)]:
            out, err = process.communicate(timeout=120)
            assert process.returncode == 0, (name,out,err)
            logs[name] = out
        assert collection.count_documents({}) == 20  # Upsert por identidad Silver; no duplicar al releer.
        def read(topic):
            consumer = KafkaConsumer(bootstrap_servers=args.bootstrap, enable_auto_commit=False, group_id=None,
                                     value_deserializer=lambda s: json.loads(s.decode()))
            tp = TopicPartition(topic, 0)
            consumer.assign([tp]); consumer.seek_to_beginning(tp)
            end = consumer.end_offsets([tp])[tp]
            values = []
            while consumer.position(tp) < end:
                for messages in consumer.poll(timeout_ms=5000).values():
                    values.extend(message.value for message in messages)
            consumer.close()
            return values
        bronze_rows, silver_rows, gold_rows = read(BRONZE), read(SILVER), read(GOLD)
        if args.source=='synthetic':
            assert bronze_rows == fixture
        else:
            from pipeline import to_silver
            assert len(bronze_rows)==20
            for raw,value in zip(bronze_rows,silver_rows):
                expected=to_silver(raw,datetime.fromisoformat(value['data']))
                assert value==expected
            (args.output/'bronze_live.jsonl').write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in bronze_rows))
        assert len(silver_rows) == 20 and len(gold_rows) == 4
        file_rows = [json.loads(line) for line in output.read_text().splitlines()]
        assert file_rows == silver_rows
        mongo_rows = [{k:v for k,v in row.items() if k!='_id'} for row in collection.find({})]
        assert sorted(mongo_rows,key=lambda row:row['tenperatura']) == sorted(silver_rows,key=lambda row:row['tenperatura'])
        expected_gold = [to_gold(silver_rows[:10]), to_gold(silver_rows[10:])]
        assert gold_rows == expected_gold * 2
        # Reanudación: offsets confirmados de los tres grupos quedan al final.
        groups = {}
        for group in ['iabd-3kasua-fitxategia','iabd-3kasua-mongo','iabd-3kasua-gold']:
            consumer = KafkaConsumer(bootstrap_servers=args.bootstrap,group_id=group,enable_auto_commit=False)
            groups[group] = consumer.committed(TopicPartition(SILVER,0))
            consumer.close()
            assert groups[group] == 20
        client.close()
        result = {'verified_at':datetime.now(timezone.utc).isoformat(), 'source':args.source, 'distinct_model_times': len({row.get('source_time') for row in silver_rows}) if args.source=='open-meteo' else None, 'sampling_note':'20 HTTP polls of model current; repeated timestamps are not independent observations' if args.source=='open-meteo' else 'synthetic fixture',
                  'brokers':3,'replication_factor':2,'bronze':20,'silver':20,'mongo':20,'jsonl':20,
                  'gold_integrated':2,'gold_independent':2,'gold_values':expected_gold,'group_offsets':groups,'scripts':logs,
                  'python':sys.version.split()[0]}
        (args.output/'resultado.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
        print(json.dumps(result,indent=2,ensure_ascii=False))
    finally:
        for process in children:
            if process.poll() is None:
                process.terminate()
                try: process.communicate(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill(); process.communicate()
        client.close()


if __name__ == '__main__':
    main()
