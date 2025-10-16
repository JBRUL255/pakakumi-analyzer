import asyncio
import random
from pakakumi_analyzer.app.db import save_round

async def run_collector_loop():
    print("🕸️ Starting data collection loop...")
    while True:
        try:
            # Simulated data – replace with WebSocket/API integration later
            round_id = int(asyncio.get_event_loop().time() * 1000)
            multiplier = random.uniform(1.0, 10.0)
            save_round(round_id, multiplier)
            print(f"💾 Saved round: {round_id} -> {multiplier:.2f}")
        except Exception as e:
            print(f"❌ Collector error: {e}")

        await asyncio.sleep(10)  # Collect new data every 10 seconds
