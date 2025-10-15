#!/bin/bash
set -e

echo "🚀 Starting Pakakumi Analyzer..."

export PYTHONPATH=/app

# Start background tasks
python -m pakakumi_analyzer.app.collector &
sleep 3
python -m pakakumi_analyzer.app.trainer &
sleep 3

# Start API server
uvicorn pakakumi_analyzer.app.serve:app --host 0.0.0.0 --port 8000
