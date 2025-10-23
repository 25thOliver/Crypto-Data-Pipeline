CREATE KEYSPACE IF NOT EXISTS crypto_keyspace
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE crypto_keyspace;

CREATE TABLE IF NOT EXISTS crypto_prices (
    symbol TEXT,
    price DECIMAL,
    fetch_time TIMESTAMP,
    PRIMARY KEY (symbol, fetch_time)
) WITH CLUSTERING ORDER BY (fetch_time DESC);

CREATE TABLE IF NOT EXISTS crypto_24h_stats (
    symbol TEXT,
    price DECIMAL,
    price_change_percent DECIMAL,
    fetch_time TIMESTAMP,
    PRIMARY KEY (symbol, fetch_time)
) WITH CLUSTERING ORDER BY (fetch_time DESC);