# Kafka 5–11 ariketak: broker isolatuko exekuzioa (2026-09-28)

**Ingurunea:** `apache/kafka:3.7.0` irudiko `codex-aabd-kafka-ej2` container
efimeroa, barneko `localhost:9092`, bolumenik eta host-porturik gabe. Ez da
`iabd-kafka` broker partekatua ukitu. Container-a amaieran gelditu eta
`--rm` bidez ezabatu da; honako hauek komandoen irteera behatuaren
transkripzioa dira. Topic izen guztiek `codex-` aurrizkia daramate.

## 5: erreplika-faktorea

Komandoa: `kafka-topics.sh --create --topic codex-replikak --partitions 2
--replication-factor 2 --bootstrap-server localhost:9092`.

```text
Error while executing topic command : Unable to replicate the partition 2 time(s):
The target replication factor of 2 cannot be reached because only 1 broker(s) are registered.
ERROR org.apache.kafka.common.errors.InvalidReplicationFactorException: Unable to replicate
the partition 2 time(s): The target replication factor of 2 cannot be reached because only
1 broker(s) are registered. (org.apache.kafka.tools.TopicCommand)
```

## 6: gakoak

Topic `codex-erosketak-key` (3 partizio). Bost mezuak `parse.key=true,
key.separator=:` erabilita bidalita. Consumer:
`--group codex-key-read --from-beginning --max-messages 5
--property print.key=true --property print.partition=true`:

```text
Partition:1	Bezero3	produktua ikusi du
Partition:0	Bezero1	Erosketa egin tu
Partition:0	Bezero2	Saioa hasi du
Partition:0	Bezero1	ordainketa egin du
Partition:0	Bezero2	erosketa egin du
```

`Bezero1` biak P0, `Bezero2` biak P0, `Bezero3` P1: gako bera → partizio bera.

## 7: consumer group

Topic `codex-eskaerak-g` (3 partizio). Bi consumer `codex-denda3` taldean
**mezuak bidali aurretik** abiarazita; gero 12 mezu gakodun bidalita:

- G1: 3 mezu (`Partition:2` x3)
- G2: 9 mezu (`Partition:0` x5, `Partition:1` x4)
- Guztira: 12/12, bikoizketarik gabe.

(Oharra: lehen saiakera batean mezuak consumer-ak abiarazi aurretik bidali
ziren eta lehen consumer-ak dena irakurri zuen — hori ere irakasgarria da:
taldea kide bakarrekin badago, hark hartzen du dena; `--describe`-ek orduan
P0+P1 kide bati eta P2 besteari esleituta erakutsi zuen rebalancearen ondoren.)

## 8: erorketa

Taldea `codex-denda4`, topic `codex-eskaerak-g`. Sekuentzia: H1 abiarazi →
3 mezu (m1–m3) → H2 abiarazi → 3 mezu (m4–m6) → **H1 hil** → 20 s
(rebalance) → 3 mezu (m7–m9) → H2 hil.

- H1 log (buffering dela eta partziala): `m2, m3 (P0), m1, m4 (P2)` = 4 lerro.
- H2 log (partziala): `m5 (P0), m6, m8 (P1)` = 3 lerro.
- Erabakigarria: **`m8` H2-k jaso zuen H1 hilda zegoela** (takeover), eta
  `--describe` finalak `CURRENT-OFFSET = LOG-END-OFFSET` (P0:8/8, P1:6/6,
  P2:7/7, **LAG 0**) erakutsi zuen: bederatzi mezuak kontsumituta, krisia
  gorabehera. H1/H2 prozesuak `kill` bidez hil zirenez eta irteera pipe
  bidez jasotzen zenez, log-lerro batzuk galdu ziren (block buffering);
  horregatik offset commit-ak dira froga, ez lerro-kopurua.

## 9: consumer soberakina

Topic `codex-eskaerak-2p` (2 partizio). Hiru consumer `codex-denda5`
taldean (`--max-messages 6 --timeout-ms 30000` bakoitza), gero 6 mezu gakodun:

- J1: 3 mezu, J2: 3 mezu, **J3: 0 mezu** (timeout bidez amaitu, hutsik).
- Guztira 6/6: partizio bakoitza consumer bakar bati; hirugarrena geldirik.

## 10: bi talde

Topic `codex-salmentak` (2 partizio), lau mezu (`salmenta-001` … `004`):

- `codex-analitika`: 4/4 (`salmenta-001` … `salmenta-004`).
- `codex-alertak`: 4/4 (berak).

## 11: offset

Topic `codex-offset-clean` (1 partizio). 10 mezu (`m01` … `m10`):

R1 (`codex-off2`, `--from-beginning --property print.offset=true`):

```text
Offset:0	m01
Offset:1	m02
Offset:2	m03
Offset:3	m04
Offset:4	m05
Offset:5	m06
Offset:6	m07
Offset:7	m08
Offset:8	m09
Offset:9	m10
```

Gero 5 berri (`m11` … `m15`). R2 **talde berean** (`codex-off2`, `--from-beginning`
berriro — baina commit-a dagoenez ez da hasieratik hasten):

```text
Offset:10	m11
Offset:11	m12
Offset:12	m13
Offset:13	m14
Offset:14	m15
```

`--describe`: `CURRENT-OFFSET 15, LOG-END-OFFSET 15, LAG 0`.
