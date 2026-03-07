#!/bin/bash
pip3 install -r requirements.txt
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
