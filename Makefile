# Makefile - backend only (FastAPI + Celery + Postgres + Redis)
# Note: This Makefile assumes you activate the Python virtualenv BEFORE running `make api` or `make worker` on Windows.
# Example PowerShell:
#   .\.venv\Scripts\Activate.ps1
#   make start-infra
#   make worker
#   make api

PYTHON ?= python
VENV_DIR := .venv
PIP := $(VENV_DIR)/Scripts/pip.exe

.DEFAULT_GOAL := help

help:
	@echo "Usage:"
	@echo "  make venv          # create virtualenv and install base deps"
	@echo "  make deps          # install python deps into venv"
	@echo "  make start-infra   # start postgres & redis via docker-compose"
	@echo "  make stop-infra    # stop postgres & redis"
	@echo "  make up            # docker compose up (full stack)"
	@echo "  make down          # docker compose down"
	@echo "  make api           # run FastAPI locally (expects venv activated)"
	@echo "  make worker        # run Celery worker locally (expects venv activated)"
	@echo "  make test-model    # run scripts/test_model.py (in venv)"
	@echo "  make logs          # tail docker logs (api,worker,redis,postgres)"
	@echo ""

venv:
	$(PYTHON) -m venv $(VENV_DIR)
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

deps: venv

start-infra:
	docker compose up -d postgres redis

stop-infra:
	docker compose stop postgres redis

up:
	docker compose up -d

down:
	docker compose down

# IMPORTANT: on Windows, run these targets from a shell where the virtualenv is activated
# Example (PowerShell):
#   .\.venv\Scripts\Activate.ps1
#   make worker
#   make api

api:
	@echo "Starting FastAPI on http://localhost:8000"
	@REM Set env vars for this shell then run uvicorn. Assumes uvicorn is available in activated venv.
	@set DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/transcriptdb && \
	set REDIS_URL=redis://localhost:6379/0 && \
	uvicorn app.main:app --reload --port 8000

worker:
	@echo "Starting Celery worker..."
	@REM Set env vars and run celery. Assumes celery is available in activated venv.
	@set DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/transcriptdb && \
	set REDIS_URL=redis://localhost:6379/0 && \
	celery -A worker.celery_app.celery worker --loglevel=info -Q transcripts --concurrency=1 --pool=solo --prefetch-multiplier=1

test-model:
	$(PYTHON) scripts/test_model.py

logs:
	docker compose logs -f api worker redis postgres

.PHONY: help venv deps start-infra stop-infra up down api worker test-model logs
