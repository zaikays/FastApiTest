FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local

COPY --from=builder /app /app

EXPOSE 8000

CMD ["uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "8888", "--loop", "uvloop"]