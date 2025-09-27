#!/usr/bin/env bash
celery -A worker.celery_app.celery worker --loglevel=info -Q transcripts