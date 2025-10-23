import os, time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import pandas as pd

db_user = os.getenv("POSTGRES_USER")
db_pass = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("POSTGRES_HOST", "postgres")
db_port = os.getenv("POSTGRES_PORT", 5432)

db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

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

def ensure_table(table_name, schema_sql):
    with engine.begin() as conn:
        conn.execute(text(schema_sql))
    print(f"Table '{table_name}' is ready.")

def insert_df(df: pd.DataFrame, table_name: str):
    if not df.empty:
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"Inserted {len(df)} rows into '{table_name}'")
        