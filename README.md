# Crypto Data Pipeline

Lightweight Binance -> Postgres -> Kafka -> Cassandra data pipeline with Grafana dashboards.

This repository contains a demo pipeline that ingests market data from Binance, writes to PostgreSQL, streams changes via Kafka/Connect, and sinks into Cassandra for fast reads from Grafana.

## Components
- `binance_ingestor` (Python): polls Binance REST endpoints and writes tables to Postgres. Entry: `scripts/binance_ingestor.py`.
- PostgreSQL: stores ingested tables defined in `scripts/schemas.py` and `init_postgres.sql`.
- Kafka + Zookeeper: message bus used by Connect.
- Kafka Connect (Debezium image): runs connectors and sink to Cassandra.
- Cassandra: final storage for dashboards. Grafana reads Cassandra via the included Cassandra datasource.

Key files:
- `docker-compose.yml` - orchestration for all services
- `Dockerfile` - builds the ingestor image
- `requirements.txt` - Python dependencies
- `scripts/` - ingestion code, DB helpers and schema DDL
- `connectors/` - Kafka Connect connector configs (the Cassandra sink is here)
- `connect-plugins/` - local Connect plugins (Cassandra sink plugin)

## Quick start (development)
Prerequisites: Docker and Docker Compose installed on the host.

1. Create a `.env` with Postgres credentials used by compose. Example:

```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=crypto
```

2. Start the stack (builds the Python image and starts all services):

```bash
docker compose up --build -d
```

3. Check services:

```bash
docker ps
curl -sS http://localhost:8083/connectors   # Kafka Connect REST
```

4. Grafana is available at `http://localhost:3000` (default admin/admin). The provided dashboard JSON expects the included Cassandra datasource (`Cassandra-Crypto`).

## Timestamp issue (important)

While testing we discovered existing `fetch_time` values stored in Cassandra use microseconds (very large integers) rather than standard milliseconds/ISO timestamps. That causes Grafana panels that rely on time functions (for example "Latest Update Time") to show no usable data.

What we did so far:
- Created a new keyspace `crypto_keyspace_v2` and the same table schemas to hold corrected future rows.
- Attempted to add a Kafka Connect SMT (TimestampConverter) to convert `fetch_time` from MICROSECONDS -> Timestamp, but Connect rejected the first config during validation. Work is paused per request.

Recommended next steps (you can pick):
- Short-term UI fix: add a Grafana transformation per panel dividing `fetch_time` by 1000 (micro -> milli) so graphs render immediately.
- Long-term fix: add a TimestampConverter SMT to the sink connector (or adjust Debezium/source config) so future rows are written with correct timestamps. This is the preferred solution.

If you choose the long-term fix, the safe sequence is:
1. Add the SMT to the sink connector to convert `fetch_time` from MICROSECONDS -> Timestamp.
2. Point the connector at `crypto_keyspace_v2` (or create a new connector that writes to v2) so new rows are correct.
3. After verifying new data looks correct in Grafana, drop the old keyspace `crypto_keyspace` if you want to discard historical rows.

Note: In this repository we created `crypto_keyspace_v2` inside the running Cassandra container, but the connector deployment (cassandra-sink-v2) was not finalized due to validation errors. See the "Troubleshooting" section below for commands and logs to continue the SMT deployment.

## How connectors are registered
The `connect` service in `docker-compose.yml` automatically PUTs each JSON file in the `connectors/` folder to the Connect REST API on startup. You can also manage connectors directly:

```bash
# list connectors
curl -sS http://localhost:8083/connectors | jq

# get config
curl -sS http://localhost:8083/connectors/<name>/config | jq

# update config
curl -sS -X PUT -H 'Content-Type: application/json' --data @config.json http://localhost:8083/connectors/<name>/config

# create connector
curl -sS -X POST -H 'Content-Type: application/json' --data @payload.json http://localhost:8083/connectors

# delete connector
curl -sS -X DELETE http://localhost:8083/connectors/<name>
```

## Troubleshooting commands
- View Connect logs:

```bash
docker logs debezium-connect --follow
```

- Describe keyspace/tables in Cassandra:

```bash
docker exec -it cassandra cqlsh -e "DESCRIBE KEYSPACE crypto_keyspace_v2;"
```

- Check connector status:

```bash
curl -sS http://localhost:8083/connectors/cassandra-sink/status | jq
```

## Notes and caveats
- `scripts/db_utils.insert_df` originally used `if_exists='replace'` which would drop previous rows; ensure it is `append` if you want to accumulate rows (this was corrected during review).
- Connector validation errors can be opaque; the Connect worker logs are the best source of truth.

## Contact / next steps
If you want, I can:
- finish adding the TimestampConverter SMT to the sink (I previously hit a validation error and can iterate further),
- or patch the Grafana dashboard JSON to apply panel transformations (divide timestamps by 1000) for an immediate fix.

Pick which you prefer and I will proceed.

---
Generated by the repo maintenance script — adjust as you like.
