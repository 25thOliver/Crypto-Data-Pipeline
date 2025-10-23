import os
import time
import requests
from datetime import datetime
from sqlalchemy import create_engine, text
import pandas as pd
from sqlalchemy.exec import OperationalError

# Configuration
binance_api = os.getenv("BINANCE_API_BASE", "https://api.binance.com")
ticker_endpoint = "/api/v3/ticker/price"

db_user = os.getenv("POSTGRES_USER")
db_pass = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("POSTGRES_HOST", "postgres")
db_port = os.getenv("POSTGRES_PORT", 5432)

db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

table_name = "crypto_prices"

def wait_for_db(max_retries=10, delay=5):
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connection established.")
            return
        except OperationalError:
            print(f"Waiting for database... ({attempt + 1}/{max_retries})")
            time.sleep(delay)
    raise Exception("Could not connect to database after several attempts.")

# Ensure table exists else auto-create
def ensure_table():
    with engine.begin() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                symbol VARCHAR(20) NOT NULL,
                price NUMERIC(18,8) NOT NULL,
                fetch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.execute(text(f"CREATE INDEX IF NOT EXISTS idx_symbol_time ON {table_name} (symbol, fetch_time);"))
    print(f"Table '{table_name}' is ready.")

# Fetch data from Binance
def fetch_binance_prices():
    url = f"{binance_api}{ticker_endpoint}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    df["price"] = df["price"].astype(float)
    df["fetch_time"] = datetime.utcnow()
    return df

# Insert using pandas to_sql
def insert_prices(df):
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"Inserted {len(df)} rows into '{table_name}'")

# Main loop
def main():
    print("Starting Binance Data Ingestor...")
    wait_for_db()
    ensure_table()
    while True:
        try:
            df = fetch_binance_prices()
            insert_prices(df)
            print(f"[{datetime.utcnow()}] Successfully ingested {len(df)} records")
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()