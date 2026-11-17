FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client make git \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "psycopg[binary]==3.2.*" "Faker==30.*"
WORKDIR /app
ENV PYTHONPATH=/app/src
