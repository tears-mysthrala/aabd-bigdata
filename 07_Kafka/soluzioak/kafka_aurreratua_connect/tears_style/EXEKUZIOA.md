# Acta de ejecución tears_style: 2026-10-06 — PASS 3/3

**Resultado:** pipeline completo verificado de principio a fin:
generador → `tears-raw` → MySQL landing (hash por fila) → procesador →
`tears-curated` + `tears-dlq` → Connect MongoSink → MongoDB, con lectura
extra final Mongo-vs-manifiesto. Ningún contenedor con OOMKill.

## Entorno ejecutado

- Broker `confluentinc/cp-kafka:7.7.1` KRaft, worker `7.8.0-ccs`
  (REST declara `7.8.0-ccs`), plugin MongoDB **1.13.0**.
- MySQL **8.4**, MongoDB **8**, proyecto `aabd-kafka-tears-style`.
- Puertos loopback 19095/13308/12719/18084; límites 512/512/512/384 MiB.
- Credenciales efímeras en `.env`/`private/` (ignorados); volúmenes
  efímeros (`down -v` al cerrar, como caso5).

## Etapas (evidencias en `evidencias/`)

| Etapa | raw | MySQL | curated | DLQ | Mongo | checks |
|---|---|---|---|---|---|---|
| `aterrizaje.json` | 15 | 14 (hash OK, dup id=3 frenado por PK) | 0 | 0 | 0 docs | 9/9 PASS |
| `curado.json` | 15 | 14 | 13 (linaje OK) | 1 (veneno 99) | 13 (vs manifiesto) | 9/9 PASS |
| `reinicio.json` | 15 | 14 | 26 (replay) | 2 (replay) | 13 estables | 9/9 PASS |

## Lecciones tears_style (casos que solo aparecen al ejecutar)

1. **Commit por fila en el aterrizaje**: con un commit único al final, el
   `ROLLBACK` tras el duplicado anulaba todo el lote (la tabla quedó con
   solo el veneno). El duplicado debe frenar una sentencia, no el lote.
2. **BSON int64 vs JSON**: el sink guarda enteros como Long y cada
   `mongosh` los serializa distinto (`{high,low}` aquí); el verificador
   los normaliza (`ejson`) o los ids no comparan aunque sean iguales.
3. **Replay duplica topics, no Mongo**: reprocesar genera 13+13 curated y
   1+1 DLQ; el sink lo absorbe con upsert por `_id={id:…}` y Mongo queda
   en 13 estables. Por eso el verificador afirma CONJUNTOS, no conteos,
   en curated/DLQ.
4. **El veneno debe discrepar**: el check de hash exige que id=99 NO
   coincida (corrupción detectada) mientras las 13 válidas sí.

## Cierre

`docker compose -p aabd-kafka-tears-style down -v` tras capturar las tres
evidencias. Re-ejecutable con el runbook de `README.md` (semilla 7,
manifiesto determinista `manifest.json`).
