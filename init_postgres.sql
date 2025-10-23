CREATE TABLE IF NOT EXISTS crypo_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    price NUMERIC(18,8) NOT NULL,
    fetch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_symbol_time ON crypo_prices (symbol, fetch_time);