#!/bin/bash
set -e

echo "🚀 Starting Pakakumi Analyzer..."
python -m pakakumi_analyzer.app.collector &
python -m pakakumi_analyzer.app.trainer &
uvicorn pakakumi_analyzer.app.serve:app --host 0.0.0.0 --port 8000
