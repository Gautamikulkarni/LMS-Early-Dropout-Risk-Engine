#!/bin/bash
set -e
echo "Installing dependencies..."
pip3 install --no-cache-dir -r requirements.txt
echo "Starting FastAPI server..."
exec python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
