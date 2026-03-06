#!/bin/bash
set -e
pip install --no-cache-dir -r requirements.txt
exec uvicorn app:app --host 0.0.0.0 --port 8000
