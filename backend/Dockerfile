FROM python:3.10-slim

WORKDIR /app

# Install dependencies needed for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

# Start script makes sure DB is seeded and then runs the server
CMD ["sh", "-c", "python seed.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
