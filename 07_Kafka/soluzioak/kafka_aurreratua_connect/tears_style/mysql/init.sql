-- Landing zone: raw sensor records. PRIMARY KEY on id is the
-- idempotency mechanism: Kafka delivers at-least-once, so replays of an
-- already-landed id fail on duplicate key instead of duplicating rows.
-- Applied once, when the MySQL volume is empty.
USE tears_db;
CREATE TABLE raw (
  id INT PRIMARY KEY,
  ts VARCHAR(32) NOT NULL,
  schema_v INT NOT NULL,
  payload JSON NOT NULL,
  sha256 CHAR(64) NOT NULL
);
