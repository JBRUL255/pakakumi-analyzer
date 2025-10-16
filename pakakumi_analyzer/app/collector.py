# pakakumi_analyzer/app/collector.py

# pakakumi_analyzer/app/collector.py
import time
import random
import requests
from pakakumi_analyzer.app.db import save_round

def fetch_real_data():
    # Replace this with real scraping from the API or websocket
    # For now we simulate random multipliers
    return {
        "round_id": int(time.time()),
        "multiplier": round(random.uniform(1.0, 10.0), 2)
    }

def collect_data_continuously():
    print("🕸️ Starting data collection loop...")
    while True:
        try:
            data = fetch_real_data()
            save_round(data["round_id"], data["multiplier"])
            print(f"Saved round: {data}")
        except Exception as e:
            print(f"Collector error: {e}")
        time.sleep(5)  # every 5s
