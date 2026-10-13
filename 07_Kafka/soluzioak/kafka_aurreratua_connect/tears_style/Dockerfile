# Worker for the MongoDB sink only. The raw landing (Kafka -> MySQL) is
# written by aterrizaje.py on purpose: landing needs per-row hash
# verification and duplicate accounting, which is application logic, not
# connector configuration. A pure sink (curated topic -> MongoDB) is the
# ideal connector use case. See README.md ("Por qué así").
ARG CONNECT_VERSION=7.8.0
FROM confluentinc/cp-kafka-connect:${CONNECT_VERSION}

USER root
RUN confluent-hub install --no-prompt mongodb/kafka-connect-mongodb:1.13.0 \
    && mkdir -p /var/lib/kafka-connect \
    && chown appuser:appuser /var/lib/kafka-connect
USER appuser
