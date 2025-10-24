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

CREATE TABLE IF NOT EXISTS crypto_order_book (
    symbol TEXT,
    side TEXT,
    price DECIMAL,
    quantity DECIMAL,
    fetch_time TIMESTAMP,
    PRIMARY KEY (symbol, fetch_time, side, price)
) WITH CLUSTERING ORDER BY (fetch_time DESC, side ASC, price ASC);

CREATE TABLE IF NOT EXISTS crypto_recent_trades (
    symbol TEXT,
    price DECIMAL,
    qty DECIMAL,
    isbuyermaker BOOLEAN,
    fetch_time TIMESTAMP,
    PRIMARY KEY (symbol, fetch_time)
) WITH CLUSTERING ORDER BY (fetch_time DESC);

CREATE TABLE IF NOT EXISTS crypto_klines (
    symbol TEXT,
    open_time BIGINT,
    open DECIMAL,
    high DECIMAL,
    low DECIMAL,
    close DECIMAL,
    volume DECIMAL,
    num_trades INT,
    fetch_time TIMESTAMP,
    PRIMARY KEY (symbol, fetch_time, open_time)
) WITH CLUSTERING ORDER BY (fetch_time DESC, open_time DESC);
