# pakakumi_analyzer/app/collector.py

import requests
from pakakumi_analyzer.app.db import insert_round
from pakakumi_analyzer.app.config import API_BASE_URL

def fetch_latest_rounds():
    try:
        res = requests.get(f"{API_BASE_URL}/latest_rounds")
        res.raise_for_status()
        data = res.json()

        for item in data.get("rounds", []):
            insert_round(item["round_number"], item["cashout"])
    except Exception as e:
        print(f"⚠️ Failed to fetch latest rounds: {e}")
