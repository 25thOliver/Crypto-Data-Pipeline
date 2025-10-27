# API fetchers
import requests
import pandas as pd
from datetime import datetime
import time

binance_api = "https://api.binance.com"

def fetch_binance_prices():
    data = requests.get(f"{binance_api}/api/v3/ticker/price", timeout=10).json()
    df = pd.DataFrame(data)
    df["price"] = df["price"].astype(float)
    # Use milliseconds since epoch for compatibility with Cassandra
    df["fetch_time"] = int(time.time() * 1000)
    return df

def fetch_24h_stats():
    data = requests.get(f"{binance_api}/api/v3/ticker/24hr", timeout=10).json()
    df = pd.DataFrame(data)
    df["fetch_time"] = int(time.time() * 1000)
    return df

def fetch_order_book(symbol="BTCUSDT", limit=5):
    data = requests.get(f"{binance_api}/api/v3/depth?symbol={symbol}&limit={limit}", timeout=10).json()
    bids = pd.DataFrame(data["bids"], columns=["price", "quantity"])
    asks = pd.DataFrame(data["asks"], columns=["price", "quantity"])
    bids["side"], asks["side"] = "bid", "ask"
    df = pd.concat([bids, asks])
    df["symbol"], df["fetch_time"] = symbol, int(time.time() * 1000)
    df["price"], df["quantity"] = df["price"].astype(float), df["quantity"].astype(float)
    return df

def fetch_recent_trades(symbol="BTCUSDT", limit=10):
    data = requests.get(f"{binance_api}/api/v3/trades?symbol={symbol}&limit={limit}", timeout=10).json()
    df = pd.DataFrame(data)
    df["symbol"], df["fetch_time"] = symbol, int(time.time() * 1000)
    return df

def fetch_klines(symbol="BTCUSDT", interval="1m", limit=5):
    data = requests.get(f"{binance_api}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}", timeout=10).json()
    df = pd.DataFrame(data, columns=[
        "open_time","open","high","low","close","volume","close_time","quote_asset_volume",
        "num_trades","taker_buy_base","taker_buy_quote","ignore"
    ])
    df["symbol"], df["fetch_time"] = symbol, int(time.time() * 1000)
    return df[["symbol","open_time","open","high","low","close","volume","num_trades","fetch_time"]]