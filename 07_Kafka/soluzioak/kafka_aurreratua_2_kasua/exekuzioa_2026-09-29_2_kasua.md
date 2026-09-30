# 2. kasua: exekuzio-erregistroa (2026-09-29)

**Ingurunea:** `apache/kafka:3.7.0`, ZK + 3 broker (`codex-kafkan-1..3`,
`codex-zk`), container efimeroak (`--rm`), bolumenik gabe. Host portuak
`127.0.0.1:19092/19093/19094`. Amaieran gelditu eta ezabatu dira.
NiFi: `iabd-nifi` partekatua (flow efimeroa API bidez sortu, gero ezabatuta).

## Topic describe (2. atala)

```text
Topic: codex-personas  TopicId: r0TpZq7NRuOfYz83Qsj_8Q  PartitionCount: 4  ReplicationFactor: 2
Topic: codex-personas  Partition: 0  Leader: 3  Replicas: 2,3  Isr: 2,3
Topic: codex-personas  Partition: 1  Leader: 1  Replicas: 3,1  Isr: 1,3
Topic: codex-personas  Partition: 2  Leader: 1  Replicas: 1,2  Isr: 1,2
Topic: codex-personas  Partition: 3  Leader: 1  Replicas: 2,1  Isr: 1,2
```

## Producer (3. atala, seed 42)

```text
P:0 O:0 K:bonetdominga@example.com V:{"izena": "Albano Llopis Hierro", "adina": 32, "hiria": "Valencia", "emaila": "bonetdominga@example.com"}
P:2 O:0 K:liliarivas@example.org V:{"izena": "Albino Bueno Gil", "adina": 32, "hiria": "Navarra", "emaila": "liliarivas@example.org"}
P:1 O:0 K:rnieto@example.org V:{"izena": "Marita Lobo Agudo", "adina": 66, "hiria": "Tarragona", "emaila": "rnieto@example.org"}
P:1 O:1 K:palomarrebeca@example.com V:{"izena": "Rico Navarro", "adina": 24, "hiria": "Jaén", "emaila": "palomarrebeca@example.com"}
P:3 O:0 K:marcospaula@example.net V:{"izena": "Dulce Roxana Aroca Segovia", "adina": 52, "hiria": "Jaén", "emaila": "marcospaula@example.net"}
P:1 O:2 K:maria-teresamancebo@example.org V:{"izena": "Vicenta Tere Pardo Fernandez", "adina": 63, "hiria": "Alicante", "emaila": "maria-teresamancebo@example.org"}
P:2 O:1 K:fermin55@example.org V:{"izena": "Toribio de Pinto", "adina": 35, "hiria": "Santa Cruz de Tenerife", "emaila": "fermin55@example.org"}
P:0 O:1 K:rpino@example.net V:{"izena": "Pascual Bellido-Donoso", "adina": 52, "hiria": "Cáceres", "emaila": "rpino@example.net"}
P:2 O:2 K:salvador41@example.org V:{"izena": "Constanza del Barba", "adina": 32, "hiria": "Zaragoza", "emaila": "salvador41@example.org"}
P:2 O:3 K:qclavero@example.org V:{"izena": "Valentina Miranda-Garcia", "adina": 59, "hiria": "La Coruña", "emaila": "qclavero@example.org"}
Bidaliak: 10/10
```

## Python consumer (4. atala, GROUP=codex-personas-py2)

10/10, P|O|K|V berdinak (goiko email multzoa).

## NiFi consumer (5. atala, GROUP=codex-personas-nifi)

`/tmp/nifi-personas/` (NiFi containerrean), filename=emaila:

```text
bonetdominga@example.com  fermin55@example.org  liliarivas@example.org
marcospaula@example.net   maria-teresamancebo@example.org
palomarrebeca@example.com qclavero@example.org  rnieto@example.org
rpino@example.net         salvador41@example.org
```

## Konparaketa (6. atala)

`diff` Python-keyak vs NiFi-fitxategiak: **berdinak 10/10** → MEZU BERDINAK.

## Gorabeherak (ikasgarriak)

- Hosteko Tailscale DNSak (`ndots:0`) Docker DNSa apurtzen du: IP literalak
  erabili ziren lab efimeroan (compose-an zerbitzu-izenak ondo).
- KRaft saiakera lehenik: JVMak abioan trabatu ziren (memoria + quorum);
  ZK modura pivotatu da (RF=2rako baliokidea).
- Broker berrasiera: `.lock` blokeoa (shutdown geldoa) eta zonbi-prozesuak
  (`sleep` PID1-ak ez ditu biltzen) — dena hilda + belaunaldi garbia.
- `advertised.listeners`eko PLAINTEXT NiFi-tik iristekoa izan behar da;
  bestela stale metadata → socket timeoutak (consumerra STOP/RUNNING).
- NiFi 2.0: `ConsumeKafka` record-motakoa da (connection service + reader/
  writer); konexioetan `groupId`; CSak `run-status`etik desgaitzen dira.
