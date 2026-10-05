"""Caso 3 docente: transformación y ejecución acotada de consumidores Kafka."""
from __future__ import annotations

import argparse
import json
import math
import os
import time
from datetime import datetime, timezone
from pathlib import Path

BRONZE = 'iabd-aemet-brontzea'
SILVER = 'iabd-aemet-zilarra'
GOLD = 'iabd-aemet-urrea'


def to_silver(raw: dict, now: datetime | None = None, city: str = 'Elche/Elx') -> dict:
    """Silver estable; Bronze conserva la respuesta completa de cada proveedor.

    Open-Meteo current representa condiciones de modelo, no una medida nueva
    por cada consulta. source_time mantiene el instante del modelo separado del
    momento de ingesta data. La ciudad procede de la configuración del endpoint.
    """
    provenance = {}
    try:
        if 'current' in raw:
            units = raw['current_units']
            if units['temperature_2m'] != '°C' or units['relative_humidity_2m'] != '%':
                raise ValueError('Open-Meteo requiere temperatura °C y humedad %')
            if raw['utc_offset_seconds'] != 0:
                raise ValueError('Consultar Open-Meteo con timezone=UTC')
            current = raw['current']
            temperature = float(current['temperature_2m'])
            humidity = float(current['relative_humidity_2m'])
            source_time = datetime.fromisoformat(current['time'])
            if source_time.tzinfo is None:
                source_time = source_time.replace(tzinfo=timezone.utc)
            interval = int(current['interval'])
            if interval <= 0:
                raise ValueError('Intervalo del modelo inválido')
            provenance = {'source_provider':'open-meteo',
                          'source_time':source_time.astimezone(timezone.utc).isoformat(),
                          'source_interval_seconds':interval}
        else:
            city = raw['municipio']['NOMBRE']
            temperature = float(raw['temperatura_actual'])
            humidity = float(raw['humedad'])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError('Payload/unidades/tiempo de meteorología inválidos') from exc
    if not isinstance(city, str) or not city.strip():
        raise ValueError('Nombre de municipio vacío')
    if not math.isfinite(temperature) or not math.isfinite(humidity) or not 0 <= humidity <= 100:
        raise ValueError('Medidas no finitas o humedad fuera de 0–100 %')
    return {'data': (now or datetime.now(timezone.utc)).isoformat(), 'hiria': city,
            'tenperatura': temperature, 'hezetasuna': humidity, **provenance}


def to_gold(measurements: list[dict]) -> dict:
    import pandas as pd
    if len(measurements) != 10 or len({row['hiria'] for row in measurements}) != 1:
        raise ValueError('Gold requiere exactamente diez medidas de la misma ciudad')
    frame = pd.DataFrame(measurements)
    result = {'hiria': measurements[0]['hiria'], 'neurketak': len(frame),
            'batez_besteko_tenperatura': float(frame.tenperatura.mean()),
            'tenperatura_min': float(frame.tenperatura.min()),
            'tenperatura_max': float(frame.tenperatura.max()),
            'batez_besteko_hezetasuna': float(frame.hezetasuna.mean())}
    if all(row.get('source_provider') == 'open-meteo' for row in measurements):
        result.update(source_provider='open-meteo',
                      unique_source_times=len({row['source_time'] for row in measurements}),
                      sampling='model snapshots; repeated times are not independent observations')
    return result


def serializer(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False).encode('utf-8')


def make_producer(bootstrap):
    from kafka import KafkaProducer
    return KafkaProducer(bootstrap_servers=bootstrap.split(','), acks='all',
                         value_serializer=serializer, key_serializer=lambda s: s.encode('utf-8'))


def parser(description):
    p = argparse.ArgumentParser(description=description)
    p.add_argument('--bootstrap', default=os.environ.get('BOOTSTRAP', '127.0.0.1:29092'))
    p.add_argument('--max', type=int, default=0, help='Mensajes a procesar; 0 = continuo')
    p.add_argument('--idle-timeout', type=float, default=60, help='Segundos sin mensajes; 0 = ilimitado')
    return p


def consume(topic, group, args, handler, batch_size=1):
    """Confirmar SOLO offsets de efectos terminados, nunca del resto del poll.

    Gold no confirma un lote incompleto. Al reiniciar se relee desde el último
    lote completo. El envío Kafka y el commit no forman una transacción: puede
    haber duplicados tras un fallo entre ambos (at-least-once).
    """
    from kafka import KafkaConsumer, TopicPartition
    from kafka.structs import OffsetAndMetadata
    if args.max < 0 or args.idle_timeout < 0:
        raise ValueError('max/idle-timeout deben ser >= 0')
    consumer = KafkaConsumer(topic, bootstrap_servers=args.bootstrap.split(','),
                             group_id=group, auto_offset_reset='earliest',
                             enable_auto_commit=False,
                             value_deserializer=lambda value: json.loads(value.decode('utf-8')))
    count, batch, offsets = 0, [], {}
    last = time.monotonic()
    try:
        while not args.max or count < args.max:
            records = consumer.poll(timeout_ms=1000, max_records=100)
            if not records:
                if args.idle_timeout and time.monotonic()-last >= args.idle_timeout:
                    raise TimeoutError(f'{group}: sin mensajes; procesados {count}, lote incompleto {len(batch)}')
                continue
            last = time.monotonic()
            for messages in records.values():
                for message in messages:
                    batch.append(message)
                    offsets[TopicPartition(message.topic, message.partition)] = OffsetAndMetadata(message.offset+1, '', -1)
                    count += 1
                    if len(batch) == batch_size:
                        handler(batch)
                        consumer.commit(offsets=offsets)
                        batch, offsets = [], {}
                    if args.max and count >= args.max:
                        if batch:
                            raise ValueError('Final acotado con lote Gold incompleto; offsets no confirmados')
                        print(json.dumps({'group': group, 'processed': count}))
                        return
    finally:
        consumer.close(autocommit=False)


def mongo_collection(uri):
    from pymongo import MongoClient
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
    return client, client.iabd.aemet_zilarra


def store_mongo(collection, message):
    # El ID del registro Kafka evita duplicarlo si se reintenta tras un fallo.
    identity = f'{message.topic}:{message.partition}:{message.offset}'
    collection.replace_one({'_id': identity}, {'_id': identity, **message.value}, upsert=True)


def silver_main():
    p = parser('Bronze → Silver + MongoDB')
    p.add_argument('--group', default='iabd-3kasua-bronze-silver')
    p.add_argument('--city', default='Elche/Elx', help='Municipio configurado para Open-Meteo')
    p.add_argument('--mongo-uri', default=os.environ.get('MONGO_URI', 'mongodb://127.0.0.1:27027'))
    # Variante de la segunda parte: MongoDB lo escribe su consumer independiente.
    p.add_argument('--without-mongo', action='store_true')
    args = p.parse_args()
    producer = make_producer(args.bootstrap)
    client, collection = (None, None) if args.without_mongo else mongo_collection(args.mongo_uri)
    def handle(messages):
        message = messages[0]
        value = to_silver(message.value, city=args.city)
        metadata = producer.send(SILVER, key=value['hiria'], value=value).get(timeout=30)
        if collection is not None:
            identity = f'{SILVER}:{metadata.partition}:{metadata.offset}'
            collection.replace_one({'_id': identity}, {'_id': identity, **value}, upsert=True)
    try:
        consume(BRONZE, args.group, args, handle)
    finally:
        producer.close(timeout=10)
        if client is not None:
            client.close()


def gold_main(default_group='iabd-3kasua-silver-gold'):
    p = parser('Silver → Gold: lotes de 10 medidas')
    p.add_argument('--group', default=default_group)
    args = p.parse_args()
    producer = make_producer(args.bootstrap)
    def handle(messages):
        value = to_gold([message.value for message in messages])
        producer.send(GOLD, key=value['hiria'], value=value).get(timeout=30)
    try:
        consume(SILVER, args.group, args, handle, batch_size=10)
    finally:
        producer.close(timeout=10)


def jsonl_main():
    p = parser('Consumer Silver → JSONL')
    p.add_argument('--group', default='iabd-3kasua-fitxategia')
    p.add_argument('--output', type=Path, default=Path('silver_datuak.jsonl'))
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('a', encoding='utf-8') as stream:
        def handle(messages):
            stream.write(json.dumps(messages[0].value, ensure_ascii=False, allow_nan=False)+'\n')
            stream.flush()
            os.fsync(stream.fileno())
        consume(SILVER, args.group, args, handle)


def mongo_main():
    p = parser('Consumer Silver → MongoDB')
    p.add_argument('--group', default='iabd-3kasua-mongo')
    p.add_argument('--mongo-uri', default=os.environ.get('MONGO_URI', 'mongodb://127.0.0.1:27027'))
    args = p.parse_args()
    client, collection = mongo_collection(args.mongo_uri)
    try:
        consume(SILVER, args.group, args, lambda messages: store_mongo(collection, messages[0]))
    finally:
        client.close()
