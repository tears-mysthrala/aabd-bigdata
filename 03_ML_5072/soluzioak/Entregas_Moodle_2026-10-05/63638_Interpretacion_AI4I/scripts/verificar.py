"""Verificación de artefactos con biblioteca estándar y señales de Poppler."""
import argparse
import csv
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PINNED_SOURCE = 'dc6630cd9b1f0f853922fad78a1b6436570d3f1ec863f1dd5c4340ac56bc8a8e'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--actualizar-hashes', action='store_true')
    args = parser.parse_args()
    source = BASE / 'datos/ai4i2020.csv'
    assert sha(source) == PINNED_SOURCE, 'El CSV no coincide con el oficial verificado.'
    with source.open(encoding='utf-8-sig', newline='') as stream:
        original = list(csv.reader(stream))
    with (BASE / 'datos/ai4i2020_orange.tab').open(encoding='utf-8', newline='') as stream:
        adapted = list(csv.reader(stream, delimiter='\t'))
    assert original[0] == adapted[0] and original[1:] == adapted[3:]
    assert len(original) == 10001 and all(len(row) == 14 for row in original)
    assert all(all(value != '' for value in row) for row in original[1:])
    target_index = original[0].index('Machine failure')
    assert sum(int(row[target_index]) for row in original[1:]) == 339
    gui = json.loads((BASE / 'evidencias/orange_gui.json').read_text())
    assert gui['rows'] == gui['scatter_points'] == 10000 and gui['failure_count'] == 339
    assert len(gui['captures']) == 3
    for capture in gui['captures']:
        assert capture['visible'] is True
        assert sha(BASE / capture['file']) == capture['sha256']
    root = ET.parse(BASE / 'Interpretacion_AI4I.ows').getroot()
    assert len(root.find('nodes')) == 3 and len(root.find('links')) == 2
    restored = json.loads((BASE / 'evidencias/flujo_reabierto.json').read_text())
    assert restored['status'] == 'passed' and restored['rows_in_each_widget'] == 10000
    assert restored['workflow_sha256'] == sha(BASE / 'Interpretacion_AI4I.ows')
    pdf = BASE / 'AI4I_Interpretacion_Orange.pdf'
    info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
    assert re.search(r'Pages:\s+4\b', info)
    text = subprocess.check_output(['pdftotext', str(pdf), '-'], text=True)
    for expected in ['1. Introducción', '2. Desarrollo', '3. Conclusiones', 'Unai Urzainqui Perez',
                     '3,39', '339', '-0,875', '50,17', '39,63']:
        assert expected in text, expected
    images = subprocess.check_output(['pdfimages', '-list', str(pdf)], text=True)
    embedded = [line for line in images.splitlines() if re.match(r'^\s*\d+\s+\d+\s+image\s', line)]
    assert len(embedded) == 3
    excluded = {'SHA256SUMS', 'evidencias/verificacion.json'}
    files = sorted(p for p in BASE.rglob('*') if p.is_file() and p.relative_to(BASE).as_posix() not in excluded
                   and '__pycache__' not in p.parts)
    sums = '\n'.join(f'{sha(p)}  {p.relative_to(BASE).as_posix()}' for p in files)+'\n'
    manifest = BASE / 'SHA256SUMS'
    if args.actualizar_hashes:
        manifest.write_text(sums)
    else:
        assert manifest.read_text() == sums, 'Integridad o lista de archivos modificada.'
    visual_file = BASE / 'evidencias/revision_visual.json'
    visual_current = visual_file.exists() and json.loads(visual_file.read_text()).get('pdf_sha256') == sha(pdf)
    result = {'status': 'passed', 'rows': 10000, 'columns': 14, 'failure_count': 339,
              'csv_equals_tab_values': True, 'pdf_pages': 4, 'pdf_embedded_images': 3,
              'workflow_runtime': 'passed', 'manifest_files': len(files), 'pdf_sha256': sha(pdf),
              'visual_review_matches_pdf': visual_current}
    (BASE / 'evidencias/verificacion.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
