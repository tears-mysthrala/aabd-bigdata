# PDF base is 7.7.1. Compose selects 7.8.0 after the reproduced standalone
# deadlock (upstream KAFKA-16051, fixed in Kafka 3.8.0).
ARG CONNECT_VERSION=7.7.1
FROM confluentinc/cp-kafka-connect:${CONNECT_VERSION}

USER root
# Same plugins as PDF p. 59; versions pinned instead of mutable "latest".
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:10.8.9 \
    && confluent-hub install --no-prompt mongodb/kafka-connect-mongodb:1.13.0 \
    && curl --fail --location --retry 3 \
       --output /usr/share/confluent-hub-components/confluentinc-kafka-connect-jdbc/lib/mysql-connector-j-8.4.0.jar \
       https://repo.maven.apache.org/maven2/com/mysql/mysql-connector-j/8.4.0/mysql-connector-j-8.4.0.jar \
    && mkdir -p /var/lib/kafka-connect \
    && chown appuser:appuser /var/lib/kafka-connect
USER appuser
