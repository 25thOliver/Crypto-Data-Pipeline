schemas = {
    "crypto_prices": """
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(20),
            price NUMERIC(18,8),
            fetch_time TIMESTAMP
        );
    """,
    "crypto_24h_stats": """
        CREATE TABLE IF NOT EXISTS crypto_24h_stats (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(20),
            priceChange NUMERIC(18,8),
            priceChangePercent NUMERIC(18,8),
            weightedAvgPrice NUMERIC(18,8),
            prevClosePrice NUMERIC(18,8),
            lastPrice NUMERIC(18,8),
            volume NUMERIC(18,8),
            fetch_time TIMESTAMP
        );
    """,
    "crypto_order_book": """
        CREATE TABLE IF NOT EXISTS crypto_order_book (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(20),
            side VARCHAR(4),
            price NUMERIC(18,8),
            quantity NUMERIC(18,8),
            fetch_time TIMESTAMP
        );
    """,
    "crypto_recent_trades": """
        CREATE TABLE IF NOT EXISTS crypto_recent_trades (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(20),
            price NUMERIC(18,8),
            qty NUMERIC(18,8),
            isBuyerMaker BOOLEAN,
            fetch_time TIMESTAMP
        );
    """,
    "crypto_klines": """
        CREATE TABLE IF NOT EXISTS crypto_klines (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(20),
            open_time BIGINT,
            open NUMERIC(18,8),
            high NUMERIC(18,8),
            low NUMERIC(18,8),
            close NUMERIC(18,8),
            volume NUMERIC(18,8),
            num_trades INT,
            fetch_time TIMESTAMP
        );
    """,
}
