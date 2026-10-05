"""API del enunciado → Bronze; fixture explícita para pruebas sin API."""
import json
import time
from pathlib import Path

from pipeline import BRONZE, make_producer, parser

API_URL = 'https://www.el-tiempo.net/api/json/v2/provincias/03/municipios/03065'


def main():
    p = parser('Producer Bronze: API cada 10 segundos')
    p.add_argument('--provider', choices=['el-tiempo','open-meteo'], default='el-tiempo')
    p.add_argument('--url', default=None, help='Override explícito del endpoint del proveedor')
    p.add_argument('--latitude', type=float, default=38.26218)
    p.add_argument('--longitude', type=float, default=-0.70107)
    p.add_argument('--city', default='Elche/Elx')
    p.add_argument('--interval', type=float, default=None, help='Por defecto 10s el-tiempo, 900s Open-Meteo')
    p.add_argument('--fixture', type=Path, help='JSONL de prueba; no consulta API')
    args = p.parse_args()
    if args.interval is None:
        args.interval = 900 if args.provider == 'open-meteo' else 10
    args.url = args.url or ('https://api.open-meteo.com/v1/forecast' if args.provider == 'open-meteo' else API_URL)
    if not -90 <= args.latitude <= 90 or not -180 <= args.longitude <= 180:
        p.error('Coordenadas fuera de rango')
    if args.interval < 0 or args.max < 0:
        p.error('interval/max deben ser >= 0')
    fixtures = None
    if args.fixture:
        fixtures = [json.loads(line) for line in args.fixture.read_text().splitlines() if line.strip()]
        if not fixtures:
            p.error('fixture vacía')
        if args.max == 0:
            args.max = len(fixtures)
        if args.max > len(fixtures):
            p.error('max excede las filas fixture')
    producer = make_producer(args.bootstrap)
    count = 0
    try:
        while not args.max or count < args.max:
            if fixtures is None:
                import requests
                params = {'latitude':args.latitude,'longitude':args.longitude, 'current':'temperature_2m,relative_humidity_2m','temperature_unit':'celsius','timezone':'UTC'} if args.provider == 'open-meteo' else None
                response = requests.get(args.url, params=params, timeout=20)
                response.raise_for_status()  # No publicar HTML de errores como datos.
                value = response.json()
            else:
                value = fixtures[count]
            # Bronze conserva el JSON completo; el municipio es la clave de partición.
            producer.send(BRONZE, key=args.city if args.provider == 'open-meteo' else value.get('municipio', {}).get('NOMBRE', 'unknown'), value=value).get(timeout=30)
            count += 1
            if not args.max or count < args.max:
                time.sleep(args.interval)
        print(json.dumps({'topic': BRONZE, 'sent': count, 'source': 'fixture' if fixtures is not None else args.provider, 'url':args.url if fixtures is None else None}))
    finally:
        producer.close(timeout=10)


if __name__ == '__main__':
    main()
