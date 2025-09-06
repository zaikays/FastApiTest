# Makefile for FastAPI Project

COMPOSE=docker compose -f config/local/docker-compose.yaml --env-file config/local/.env

.PHONY: up down logs fastapi-logs migrate build prune

# Start all services
up:
	$(COMPOSE) up -d --build

# Stop and remove containers, networks
down:
	$(COMPOSE) down

# Stop and remove containers, networks, and volumes (⚠️ deletes DB data)
down-v:
	$(COMPOSE) down -v

# View logs of all services
logs:
	$(COMPOSE) logs -f

# View logs of the FastAPI app
fastapi-logs:
	$(COMPOSE) logs -f fastapi

# Run Alembic migrations
migrate:
	$(COMPOSE) run fastapi alembic upgrade head

# Rebuild containers without using cache
build:
	$(COMPOSE) build --no-cache

# Remove all unused Docker resources (⚠️ be careful)
prune:
	docker system prune -af
