-- Fix timestamps in crypto_keyspace by converting from microseconds to milliseconds
-- This will divide all fetch_time values by 1000

-- Note: CQL doesn't support UPDATE with arithmetic operations on timestamps
-- We need to use a client script for this

-- Alternative: Truncate tables and let the sink re-populate with correct timestamps
-- from Kafka (which contains microseconds in the messages)

-- For now, the best approach is to:
-- 1. Let new data flow in with the current microseconds
-- 2. Fix the timestamps in Grafana by dividing by 1000 in the queries
-- OR
-- 3. Fix timestamps in the application layer (Python script or at insertion time)

USE crypto_keyspace;

-- Truncate all tables to start fresh
TRUNCATE crypto_prices;
TRUNCATE crypto_24h_stats;
TRUNCATE crypto_order_book;
TRUNCATE crypto_recent_trades;
TRUNCATE crypto_klines;
