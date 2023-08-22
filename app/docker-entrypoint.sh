#!/usr/bin/env bash

alembic upgrade head
uvicorn app.main:appFastAPI --host 0.0.0.0 --port 8000 --reload