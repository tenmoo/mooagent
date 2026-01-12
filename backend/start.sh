#!/bin/sh
# Fly.io entry point script

# Run database migrations if needed
# python -m alembic upgrade head

# Start the FastAPI server
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
