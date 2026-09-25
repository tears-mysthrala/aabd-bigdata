# Kafka 1–5 ariketak: broker isolatuko exekuzioa (2026-09-25)

**Ingurunea:** `apache/kafka:3.7.0` irudiko `codex-aabd-kafka-ejercicios-20260925`
container efimeroa, barneko `localhost:9092`, bolumenik eta host-porturik
gabe. Ez da `iabd-kafka` broker partekatua ukitu. Topic-ak:
`codex-aabd-20260925-sensors` eta `codex-aabd-20260925-purchases`.
CLIak `/opt/kafka/bin/`-koak dira. Container-a amaieran gelditu eta `--rm`
bidez ezabatu da; honako hauek komandoen irteera behatuaren transkripzioa
dira, ez une honetan berriro kontsulta daitekeen broker-egoera.

## 1–3: topic-ak eta consumer taldeak

- `sensors` 2 partiziorekin eta `purchases` 4rekin sortu ziren; `--describe`
  lehenengoan `PartitionCount: 2` erakutsi zuen.
- Sei sentsore-mezu bidali eta lehen consumer taldeak 6 irakurri zituen.
  Consumer-a amaitu ondoren beste 3 bidali ziren; bigarren talde berri batek
  `--from-beginning` erabilita 9 irakurri zituen. Hau ez da lehengo taldearen
  commit-aren edo retention luzearen froga.
- Bost erosketa-mezu bidali ziren. Bi consumer group desberdinek 5/5 mezu
  irakurri zituzten. Irakurtzeak ez zituen mezuak ezabatu.

## 4: benetan behatutako partizioa eta offset-a

Komandoa: `kafka-console-consumer.sh --topic ...purchases --group
...purchase-1 --from-beginning --max-messages 5 --property
print.partition=true --property print.offset=true --bootstrap-server
localhost:9092`.

| Mezua | Partition | Offset |
|---|---:|---:|
| `E001;ordenagailua;899` | 3 | 0 |
| `E002;monitorea;249` | 3 | 1 |
| `E003;teklatua;59` | 3 | 2 |
| `E004;SSD;89` | 3 | 3 |
| `E005;routerra;119` | 3 | 4 |

Producer honek ez zuen key-rik erabili; bost mezuak partizio berean amaitzea
exekuzio honen emaitza da, ez Kafka-ren topic osorako ordena-bermea.

## 5: partizio kopurua handitu eta murriztea saiatu

`--describe`: `PartitionCount: 2`, partizio IDak `0,1`.
`--alter --partitions 4`: exit code 0.
Bigarren `--describe`: `PartitionCount: 4`, IDak `0,1,2,3`.
`--alter --partitions 2`: exit code 1 eta honako errorea:

```text
InvalidPartitionsException: The topic codex-aabd-20260925-sensors currently has 4 partition(s); 2 would not be an increase.
```

Azken erroreak erakusten du broker honek ez duela partizio-murrizketa onartu.
Ez da lehendik idatzitako mezuen kokapena aldatu edo beste konfiguraziorik
ukitu.
