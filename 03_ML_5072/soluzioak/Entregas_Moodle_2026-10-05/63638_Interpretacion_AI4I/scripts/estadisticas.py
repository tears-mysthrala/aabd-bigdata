"""Verifica CSV oficial y genera tabla Orange sin eliminar filas ni columnas."""
import csv
import hashlib
import json
import math
import statistics
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CSV = BASE / 'datos/ai4i2020.csv'
HEADER = ['UDI', 'Product ID', 'Type', 'Air temperature [K]',
          'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]',
          'Tool wear [min]', 'Machine failure', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF']


def main():
    with CSV.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == HEADER
        rows = list(reader)
    assert len(rows) == 10000
    assert all(len(r) == 14 and all(v != '' for v in r.values()) for r in rows)
    assert len({r['UDI'] for r in rows}) == 10000
    assert {r['Machine failure'] for r in rows} == {'0', '1'}
    numeric = {name: [float(r[name]) for r in rows] for name in HEADER if name not in ['Product ID', 'Type']}
    assert all(math.isfinite(v) for values in numeric.values() for v in values)
    assert sum(numeric['Machine failure']) == 339
    stats = {'csv_sha256': hashlib.sha256(CSV.read_bytes()).hexdigest(),
             'rows': len(rows), 'columns': len(HEADER), 'missing': 0,
             'failure_count': 339, 'failure_percent': 3.39,
             'pearson_speed_torque': statistics.correlation(numeric[HEADER[5]], numeric[HEADER[6]]),
             'groups': {}, 'speed_bins': []}
    for target in ['0', '1']:
        group = [r for r in rows if r['Machine failure'] == target]
        out = {'count': len(group)}
        for column in HEADER[3:8]:
            v = [float(r[column]) for r in group]
            out[column] = {'mean': statistics.mean(v), 'median': statistics.median(v),
                           'min': min(v), 'max': max(v), 'sd': statistics.stdev(v)}
        stats['groups'][target] = out
    for label, predicate in [('speed < 1400', lambda v: v < 1400),
                             ('1400 <= speed <= 1800', lambda v: 1400 <= v <= 1800),
                             ('speed > 1800', lambda v: v > 1800)]:
        group = [r for r in rows if predicate(float(r[HEADER[5]]))]
        failures = sum(int(r['Machine failure']) for r in group)
        stats['speed_bins'].append({'label': label, 'count': len(group), 'failures': failures,
                                   'failure_percent': 100 * failures / len(group)})
    # Three Orange header rows express types/roles; the 10000 data rows are unchanged.
    with (BASE / 'datos/ai4i2020_orange.tab').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(HEADER)
        writer.writerow(['continuous', 'string', 'discrete', 'continuous', 'continuous',
                         'continuous', 'continuous', 'continuous', '0 1', '0 1', '0 1', '0 1', '0 1', '0 1'])
        writer.writerow(['meta', 'meta', '', '', '', '', '', '', 'class', 'meta', 'meta', 'meta', 'meta', 'meta'])
        writer.writerows([[r[name] for name in HEADER] for r in rows])
    stats['orange_tab_sha256'] = hashlib.sha256((BASE / 'datos/ai4i2020_orange.tab').read_bytes()).hexdigest()
    (BASE / 'evidencias/estadisticas.json').write_text(json.dumps(stats, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
