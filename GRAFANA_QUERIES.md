# Grafana Query Guide for Crypto Pipeline

## Timestamp Format
The `fetch_time` column is stored as **BIGINT** containing milliseconds since Unix epoch.

## Query Examples

### For Time Series Panels

#### Basic Query
```sql
SELECT symbol, price, fetch_time
FROM crypto_prices
WHERE symbol = 'BTCUSDT'
ALLOW FILTERING
```

**Transformation Required:**
1. Add transformation: "Convert field type"
2. Field: `fetch_time`
3. As: `Time`
4. Input format: `Unix timestamp (milliseconds)`

#### With Time Range Filter
```sql
SELECT symbol, price, fetch_time
FROM crypto_prices
WHERE symbol = 'BTCUSDT' 
  AND fetch_time >= ${__from:raw}
  AND fetch_time <= ${__to:raw}
ALLOW FILTERING
```

### For Latest Update Panel

**Recommended Query (easiest):**
```sql
SELECT toUnixTimestamp(MAX(fetch_time)) as latest_update
FROM crypto_prices
ALLOW FILTERING
```

**Transformation:**
1. Add transformation: "Convert field type"
2. Field: `latest_update`
3. As: `Time`
4. Input format: `Unix timestamp (milliseconds)`

**Alternative (if above doesn't work):**
```sql
SELECT MAX(fetch_time) as latest_update
FROM crypto_prices
ALLOW FILTERING
```

**Transformation for alternative:**
1. Add transformation: "Convert field type"
2. Field: `latest_update`
3. As: `Time`
4. Input format: `Time` (it's already a timestamp type)

### For "Last Value" Panels

**Query:**
```sql
SELECT symbol, price, fetch_time
FROM crypto_prices
WHERE symbol = 'BTCUSDT'
ORDER BY fetch_time DESC
LIMIT 1
ALLOW FILTERING
```

**Transformation:**
- Convert `fetch_time` to Time (milliseconds format)

## Panel Configuration Tips

1. **Time as Value Panel:**
   - Use transformation to convert to Time
   - Format as "Date & Time"

2. **Time Series Panel:**
   - X-Axis: Use `fetch_time` converted to Time
   - Y-Axis: Use your value field (price, volume, etc.)

3. **Table Panel:**
   - Show timestamps as readable date/time
   - Add transformation: "Convert field type" → Time (milliseconds)

## Quick Fix for "No Data" Issues

If you see "no data" in Grafana:

1. **Check if data exists:**
   ```sql
   SELECT COUNT(*) FROM crypto_prices ALLOW FILTERING
   ```

2. **Verify timestamp format:**
   ```sql
   SELECT fetch_time, typeof(fetch_time) FROM crypto_prices LIMIT 1 ALLOW FILTERING
   ```

3. **Add transformation:**
   - Always convert `fetch_time` from `number` to `Time`
   - Use input format: `Unix timestamp (milliseconds)`

## Time Range Variables

Use Grafana's built-in time range in queries:
```
WHERE fetch_time >= ${__from:raw}
  AND fetch_time <= ${__to:raw}
```

This automatically converts Grafana's time range to milliseconds.
