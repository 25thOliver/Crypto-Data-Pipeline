# --- Base Image ---
FROM python:3.11-slim

# --- Working Directory ---
WORKDIR /app

# --- Install Dependencies ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy Scripts ---
COPY scripts/ ./scripts

# --- Set Environment Variables ---
ENV PYTHONUNBUFFERED=1

# --- Default Command ---
CMD ["python", "scripts/binance_ingestor.py"]
