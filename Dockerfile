# ---------- Base Image ----------
FROM python:3.11-slim

# ---------- Environment Setup ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# ---------- Install dependencies ----------
# Copy requirement file first to leverage Docker cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy project files ----------
COPY scripts/ ./scripts/
COPY .env ./  

# ---------- Set entrypoint ----------
CMD ["python", "scripts/binance_ingestor.py"]
