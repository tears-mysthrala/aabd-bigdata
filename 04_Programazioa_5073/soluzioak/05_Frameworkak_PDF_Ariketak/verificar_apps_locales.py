"""Comprobación local: HTTP Uvicorn real y widgets Streamlit (sin Gemini).

Usa solo un servidor nuevo loopback y datos ficticios; lo detiene al finalizar.
AppTest ejecuta los scripts de Streamlit, no sustituye una revisión del navegador.
"""
import argparse
import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import requests
from streamlit.testing.v1 import AppTest

BASE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=18033)
    parser.add_argument('--output', type=Path, default=BASE/'evidencias_apps_locales.json')
    args = parser.parse_args()
    os.environ['MPLBACKEND'] = 'Agg'
    # Abortar antes de probar si el puerto pertenece a otro servidor local.
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', args.port))
    server = subprocess.Popen(
        [sys.executable, '-m', 'uvicorn', 'api_ariketak:app_3_2',
         '--host', '127.0.0.1', '--port', str(args.port)], cwd=BASE,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = f'http://127.0.0.1:{args.port}'
    try:
        for _ in range(100):
            if server.poll() is not None:
                raise RuntimeError('Uvicorn no pudo arrancar; elegir un puerto libre')
            try:
                if requests.get(url+'/openapi.json', timeout=1).status_code == 200:
                    break
            except requests.RequestException:
                pass
            time.sleep(.1)
        else:
            raise TimeoutError('Uvicorn no respondió')
        book = dict(id=170, title='Adibide sintetikoa', author='Egile fikziozkoa', year=2026)
        cases = [('GET','/liburuak/170',None,404), ('POST','/liburuak',book,201),
                 ('POST','/liburuak',book,409), ('GET','/liburuak/170',None,200),
                 ('POST','/liburuak',dict(book,id=0),422),
                 ('DELETE','/liburuak/170',None,204), ('GET','/liburuak/170',None,404)]
        statuses = []
        for method, path, payload, expected in cases:
            response = requests.request(method, url+path, json=payload, timeout=5)
            assert response.status_code == expected, (method,path,response.status_code)
            if expected == 200:
                assert response.json() == book
            if expected == 201:
                assert requests.get(url+'/liburuak',timeout=5).json() == [book]
            if expected == 204:
                assert not response.content
            statuses.append(dict(method=method,path=path,status=response.status_code))
        assert requests.get(url+'/liburuak',timeout=5).json() == []
        assert requests.get(url+'/docs',timeout=5).status_code == 200
        a = AppTest.from_file(str(BASE/'streamlit_4_1.py'),default_timeout=30).run()
        assert not a.exception and len(a.dataframe[0].value) == 5
        employees = {x.label:x.value for x in a.metric}
        assert list(employees.values()) == ['5','32.0','42,000 €']
        b = AppTest.from_file(str(BASE/'streamlit_4_2.py'),default_timeout=30).run()
        b.text_input[0].set_value('Ikasle fikziozkoa')
        b.number_input[0].set_value(24)
        b.multiselect[0].set_value(['Python','Kafka'])
        b.sidebar.selectbox[0].set_value('Castellano')
        b.sidebar.radio[0].set_value('Iluna')
        b.button[0].click().run()
        form = json.loads(b.json[0].value)
        assert form == dict(izena='Ikasle fikziozkoa',adina=24,interesak=['Python','Kafka'],
                            hizkuntza='Castellano',gaia='Iluna')
        b.button[1].click().run()
        assert not b.exception and b.session_state['clicks'] == 1
        c = AppTest.from_file(str(BASE/'streamlit_4_4.py'),default_timeout=30).run()
        c.button[0].click().run()
        assert not c.exception and c.markdown[0].value == 'Salmenta altua: `False`'
        c.sidebar.radio[0].set_value('Ebaluazioa').run()
        assert not c.exception
        metrics = {x.label:x.value for x in c.metric}
        assert list(metrics.values()) == ['0.75','0.60','0.50']
        result = dict(verified_at=datetime.now(timezone.utc).isoformat(),
                      scope='localhost Uvicorn HTTP + Streamlit AppTest; synthetic data; no Gemini',
                      http=statuses, employees=employees, form=form,counter=1,
                      prediction_default=False, synthetic_holdout_metrics=metrics,
                      versions={m:version(m) for m in ['streamlit','fastapi','uvicorn','scikit-learn','pandas']})
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print('Local HTTP and Streamlit checks passed; synthetic evidence saved.')
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill(); server.wait()


if __name__ == '__main__':
    main()
