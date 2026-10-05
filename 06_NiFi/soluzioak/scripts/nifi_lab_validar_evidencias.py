#!/usr/bin/env python3
"""Check archived runtime evidence offline; does not claim a fresh NiFi run."""
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text())


def main():
    case = {n: next(BASE.glob(f'0{n}_*')) for n in range(1,7)}
    for file in (case[1]/'sarrera').glob('*'):
        assert file.read_bytes() == (case[1]/'evidencias/irteera'/file.name).read_bytes()
    conflicts = list((case[1]/'evidencias/irteera/gatazkak').glob('*'))
    assert len(conflicts) == 1
    assert conflicts[0].read_text() == 'LAB conflict: original output must remain unchanged\n'
    with (case[2]/'sarrera/salmentak.csv').open() as stream:
        source = list(csv.DictReader(stream, delimiter=';'))
    assert len(source) == 6
    expected = [r for r in source if r['Country'].strip() == 'France' and int(r['Units']) > 1]
    expected = sorted(tuple(sorted(r.items())) for r in expected)
    for variant, expected_files in [(1,3),(2,1),(3,1)]:
        files = list((case[2]/f'evidencias/aldaera{variant}').glob('*.csv'))
        assert len(files) == expected_files
        rows = []
        for file in files:
            with file.open() as stream:
                rows.extend(csv.DictReader(stream, delimiter=';'))
        assert sorted(tuple(sorted(r.items())) for r in rows) == expected
    assert (case[3]/'evidencias/basic_proba.txt').read_text() == 'proba'
    document = load(case[3]/'evidencias/mongo_datuak.json')[0]
    provenance = load(case[3]/'evidencias/flow_03_atributuak_linajea_aldaera2_mongodb_provenance.json')
    assert any(a['name'] == 'datuak' and a.get('value') == document['datuak']
               for event in provenance['events'] for a in event.get('attributes', []))
    assert document['datuak'] in (case[3]/'evidencias/nifi_app_extracto.log').read_text()
    document = load(case[4]/'evidencias/mongo_http.json')[0]
    assert sorted(document['mezua'].splitlines()) == [f'ERROR: lab event {i}' for i in range(1,6)]
    assert document['mota'] == 'errorea' and document['fecha']
    provenance = load(case[4]/'evidencias/flow_04_mongodb_http_provenance.json')
    assert any(e['eventType']=='JOIN' and len(e['parentUuids'])==5 for e in provenance['events'])
    with (case[5]/'sarrera/datuak.csv').open() as stream:
        source = list(csv.DictReader(stream, delimiter=';'))
    output = load(case[5]/'evidencias/datuak.json')
    assert len(source) == len(output) == 5
    for real, actual in zip(source,output):
        assert set(real) == set(actual)
        for key,value in real.items():
            assert (float(value)==actual[key] if key in ['id','adina','soldata'] else value==actual[key])
    ports = load(case[5]/'evidencias/boundary_ports_status.json')
    assert ports['inputPorts']['aggregateSnapshot']['flowFilesIn'] >= 1
    assert ports['outputPorts']['aggregateSnapshot']['flowFilesOut'] >= 1
    comparison = load(case[6]/'evidencias/comparacion_contenido_completo.json')
    counts = {'customers':12435,'orders':68883,'order_items':172198}
    for table, expected in counts.items():
        row = comparison['tables'][table]
        assert row['source_count'] == expected
        for collection in ['6kasua-classic','6kasua-record']:
            assert row[collection]['count'] == expected
            assert row[collection]['mismatching_rows'] == 0
            assert row[collection]['normalized_sha256'] == row['source_normalized_sha256']
    print('Archived evidence verified for six NiFi cases; no fresh runtime claimed')


if __name__ == '__main__':
    main()
