import time
from datetime import datetime
from db_utils import wait_for_db, ensure_table, insert_df
from binance_api import (
    fetch_binance_prices, fetch_24h_stats,
    fetch_order_book, fetch_recent_trades, fetch_klines
)
from schemas import schemas

def main():
    print("Starting Binance Data Ingestor...")
    wait_for_db()

    for table, schema in schemas.items():
        ensure_table(table, schema)

        while True:
            try:
                insert_df(fetch_binance_prices(), "crypto_prices")
                insert_df(fetch_24h_stats(), "crypto_24h_stats")
                insert_df(fetch_order_book(), "crypto_order_book")
                insert_df(fetch_recent_trades(), "crypto_recent_trades")
                insert_df(fetch_klines(), "crypto_klines")

                print(f"[{datetime.utcnow()}] Successfully ingested all endpoints.\n")
                time.sleep(600)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(10)

if __name__ == "__main__":
    main()