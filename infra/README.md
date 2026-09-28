# infra/ — lo compartido vive aquí, el código en su asignatura

| Servicio | Qué es | Quién lo usa |
|---|---|---|
| `nginx` | Frontal HTTPS (`nifi.bigdata.local` → NiFi). HTTP redirige a HTTPS. | DF2.2 (NiFi). Futuro: más UIs. |
| `kafka` | Bus KRaft (texto plano, **sin auth**); host solo `127.0.0.1:${KAFKA_PORT:-9092}`, contenedores de `iabd-infra-net` en `kafka:9092`. | Servicios autorizados de la red compartida; para ejercicios destructivos usa broker aislado. |
| red `iabd-infra-net` | Red externa que los labs reutilizan (no la crean). | DF2.2 (`nifi`), futuros labs. |

Kafka **no** va detrás de nginx a propósito: nginx es proxy HTTP y Kafka habla
su protocolo binario TCP. Endurecer Kafka = SASL/TLS en el broker, no un frontal web.

## Arranque (orden)

```bash
cd infra
cp .env.example .env   # opcional
docker compose up -d
curl --cacert certs/ca.crt --resolve nifi.bigdata.local:443:127.0.0.1 -o /dev/null -s -w "%{http_code}\n" https://nifi.bigdata.local/nifi/  # 200/502 según NiFi esté arrancado
```

Luego cada lab (`06_NiFi/.../DF2.2`, …) con su `docker compose up -d`.
Para `nifi.bigdata.local` en navegador: `127.0.0.1 nifi.bigdata.local` en `/etc/hosts` (una vez, con sudo).

## Certs

`certs/` (CA local + `bigdata.local`, autofirmados): las `.key` **no se versionan**
(ver `/.gitignore`). Si caducan, regenerar y reimportar flujos si NiFi lo exige.

Límite del laboratorio: el navegador puede verificar el certificado del frontal
con la CA local, pero `nginx.conf` desactiva la comprobación del certificado autofirmado del
NiFi situado en la red Docker interna. MongoDB y Kafka tampoco autentican
clientes en sus redes de laboratorio. No conectes contenedores de terceros a
esas redes ni uses esta configuración para datos reales o una red compartida.
