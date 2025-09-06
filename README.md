# 🚀 FastAPI Project

This project runs a **FastAPI** application with **PostgreSQL** using **Docker Compose**.
It includes everything you need for local development and database migrations.

---

## 📦 Requirements

* [Docker](https://docs.docker.com/get-docker/) ≥ 20.x
* [Docker Compose](https://docs.docker.com/compose/install/) ≥ 2.x
* [Make](https://www.gnu.org/software/make/) (optional, for convenience)

---

## ⚙️ Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/zaikays/FastApiTest.git
   cd FastApiTest
   ```

2. **Configure environment variables**

   Copy the example `.env` file and adjust values if needed:

   ```bash
   cp config/local/.env.example config/local/.env
   ```

   Example `.env`:

   ```env
   POSTGRES_USER=fastapi_user
   POSTGRES_PASSWORD=fastapi_pass
   POSTGRES_DB=fastapi_db
   POSTGRES_PORT=5432
   APP_ENV=local
   ```

---

## ▶️ Run the project

### Using Docker Compose directly:

```bash
docker compose -f config/local/docker-compose.yaml --env-file config/local/.env up -d --build
```

Run **Alembic migrations** after starting the containers:

```bash
docker compose -f config/local/docker-compose.yaml --env-file config/local/.env run fastapi alembic upgrade head
```

### Using Makefile commands:

```bash
make up          # Starts Docker Compose stack
make migrate     # Runs Alembic migrations
make logs        # Tail logs of all services
make stop        # Stop and remove containers
make clean       # Stop, remove containers, networks, and volumes
```

---

## 🔍 Logs

View logs of all services:

```bash
docker compose -f config/local/docker-compose.yaml --env-file config/local/.env logs -f
```

Or just the FastAPI app:

```bash
docker compose -f config/local/docker-compose.yaml --env-file config/local/.env logs -f fastapi
```

---

## 🛑 Stop the project

Stop and remove containers, networks:

```bash
docker compose -f config/local/docker-compose.yaml --env-file config/local/.env down
```

Stop and remove containers, networks, **and volumes** (⚠️ deletes DB data):

```bash
docker compose -f config/local/docker-compose.yaml --env-file config/local/.env down -v
```

---

## 🌐 Access

* FastAPI app → [http://localhost](http://localhost)
* Interactive API docs → [http://localhost/docs](http://localhost/docs)


✨ Now you’re ready to develop with **FastAPI + Docker Compose + PostgreSQL**!
