# infra/ — lo compartido vive aquí, el código en su asignatura

| Servicio | Qué es | Quién lo usa |
|---|---|---|
| `nginx` | Frontal HTTPS (`nifi.bigdata.local` → NiFi). HTTP redirige a HTTPS. | DF2.2 (NiFi). Futuro: más UIs. |
| `kafka` | Bus de eventos KRaft (texto plano, **sin auth**, solo `127.0.0.1`). | 07_Kafka y quien publique/consuma topics. |
| red `iabd-infra-net` | Red externa que los labs reutilizan (no la crean). | DF2.2 (`nifi`), futuros labs. |

Kafka **no** va detrás de nginx a propósito: nginx es proxy HTTP y Kafka habla
su protocolo binario TCP. Endurecer Kafka = SASL/TLS en el broker, no un frontal web.

## Arranque (orden)

```bash
cd infra
cp .env.example .env   # opcional
docker compose up -d
curl -k -o /dev/null -s -w "%{http_code}\n" -H 'Host: nifi.bigdata.local' https://127.0.0.1/  # 200/301/404 = nginx vivo
```

Luego cada lab (`06_NiFi/.../DF2.2`, …) con su `docker compose up -d`.
Para `nifi.bigdata.local` en navegador: `127.0.0.1 nifi.bigdata.local` en `/etc/hosts` (una vez, con sudo).

## Certs

`certs/` (CA local + `bigdata.local`, autofirmados): las `.key` **no se versionan**
(ver `/.gitignore`). Si caducan, regenerar y reimportar flujos si NiFi lo exige.
