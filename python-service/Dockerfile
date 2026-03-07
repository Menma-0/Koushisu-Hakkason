# ================================
# Stage 1: 開発環境
# ================================
FROM python:3.11-slim AS dev
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]


# ================================
# Stage 2: 本番環境
# ================================
FROM python:3.11-slim AS prod
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password --no-create-home appuser
USER appuser

COPY . .

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
