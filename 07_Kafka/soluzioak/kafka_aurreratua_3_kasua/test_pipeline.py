from datetime import datetime, timezone

import pytest

from pipeline import to_silver, to_gold


def test_silver_extracts_types_without_mutating_bronze():
    raw = {'municipio': {'NOMBRE': 'Elche/Elx'}, 'temperatura_actual': '21', 'humedad': '55', 'extra': [1]}
    silver = to_silver(raw, datetime(2026, 10, 2, tzinfo=timezone.utc))
    assert silver == {'data': '2026-10-02T00:00:00+00:00', 'hiria': 'Elche/Elx', 'tenperatura': 21.0, 'hezetasuna': 55.0}
    assert raw['temperatura_actual'] == '21' and raw['extra'] == [1]


@pytest.mark.parametrize('field,value', [('temperatura_actual', None), ('temperatura_actual', 'NaN'), ('humedad', 'inf'), ('humedad', '-1'), ('humedad', '101')])
def test_invalid_measurements_are_rejected(field, value):
    raw = {'municipio': {'NOMBRE': 'Elche/Elx'}, 'temperatura_actual': '21', 'humedad': '55'}
    raw[field] = value
    with pytest.raises(ValueError):
        to_silver(raw)


def test_exact_ten_measurement_batch_with_real_arithmetic():
    measurements = [{'hiria': 'Elche/Elx', 'tenperatura': float(i), 'hezetasuna': float(40+i)} for i in range(10)]
    assert to_gold(measurements) == {'hiria': 'Elche/Elx', 'neurketak': 10, 'batez_besteko_tenperatura': 4.5, 'tenperatura_min': 0.0, 'tenperatura_max': 9.0, 'batez_besteko_hezetasuna': 44.5}
    with pytest.raises(ValueError):
        to_gold(measurements[:9])
    measurements[-1]['hiria'] = 'Other city'
    with pytest.raises(ValueError):
        to_gold(measurements)


def test_commit_does_not_skip_unprocessed_records_from_same_poll(monkeypatch):
    from types import SimpleNamespace
    import kafka
    from pipeline import consume
    from kafka import TopicPartition

    commits = []
    processed = []
    class Consumer:
        def __init__(self, *a, **kw): pass
        def poll(self, **kw):
            return {TopicPartition('t', 0): [SimpleNamespace(topic='t', partition=0, offset=i, value=i) for i in range(3)]}
        def commit(self, offsets): commits.append(offsets)
        def close(self, **kw): pass
    monkeypatch.setattr(kafka, 'KafkaConsumer', Consumer)
    consume('t', 'g', SimpleNamespace(max=1, idle_timeout=1, bootstrap='test:9092'),
            lambda rows: processed.extend(row.value for row in rows))
    assert processed == [0]
    assert commits[0][TopicPartition('t', 0)].offset == 1


def test_partial_gold_batch_is_not_committed(monkeypatch):
    from types import SimpleNamespace
    import kafka
    from pipeline import consume
    from kafka import TopicPartition

    commits = []
    class Consumer:
        def __init__(self, *a, **kw): pass
        def poll(self, **kw):
            return {TopicPartition('t', 0): [SimpleNamespace(topic='t', partition=0, offset=i, value=i) for i in range(9)]}
        def commit(self, offsets): commits.append(offsets)
        def close(self, **kw): pass
    monkeypatch.setattr(kafka, 'KafkaConsumer', Consumer)
    with pytest.raises(ValueError, match='incompleto'):
        consume('t', 'g', SimpleNamespace(max=9, idle_timeout=1, bootstrap='test:9092'),
                lambda _: pytest.fail('No puede emitir lote parcial'), batch_size=10)
    assert commits == []


def test_open_meteo_uses_current_values_and_preserves_model_time():
    raw = {'latitude':38.25,'longitude':-0.6875,'utc_offset_seconds':0,
           'current_units':{'temperature_2m':'°C','relative_humidity_2m':'%'},
           'current':{'time':'2026-10-02T06:45','interval':900,'temperature_2m':20.8,'relative_humidity_2m':85}}
    value=to_silver(raw,datetime(2026,10,2,7,0,tzinfo=timezone.utc),city='Elche/Elx')
    assert value['data']=='2026-10-02T07:00:00+00:00'
    assert value['source_time']=='2026-10-02T06:45:00+00:00'
    assert value['source_provider']=='open-meteo' and value['source_interval_seconds']==900
    assert value['tenperatura']==20.8 and value['hezetasuna']==85.0
    assert raw['current']['time']=='2026-10-02T06:45'


def test_open_meteo_rejects_wrong_units_or_null_values():
    raw={'utc_offset_seconds':0,'current_units':{'temperature_2m':'°F','relative_humidity_2m':'%'},
         'current':{'time':'2026-10-02T06:45','interval':900,'temperature_2m':20.8,'relative_humidity_2m':85}}
    with pytest.raises(ValueError): to_silver(raw)
    raw['current_units']['temperature_2m']='°C';raw['current']['temperature_2m']=None
    with pytest.raises(ValueError): to_silver(raw)


def test_gold_reports_repeated_model_times_explicitly():
    rows=[{'hiria':'Elche/Elx','tenperatura':20.8,'hezetasuna':85.0,
           'source_provider':'open-meteo','source_time':'2026-10-02T06:45:00+00:00'} for _ in range(10)]
    result=to_gold(rows)
    assert result['neurketak']==10
    assert result['unique_source_times']==1
    assert 'not independent' in result['sampling']
