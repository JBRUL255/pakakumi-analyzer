import asyncio
import json
import websockets
from pakakumi_analyzer.app.config import WS_URL
from pakakumi_analyzer.app.db import get_db
import datetime

async def collect_live_data():
    async with websockets.connect(WS_URL) as ws:
        print("✅ Connected to PakaKumi WebSocket...")
        while True:
            try:
                msg = await ws.recv()
                data = json.loads(msg)
                if "crash_point" in data:
                    with get_db() as conn:
                        conn.execute(
                            "INSERT OR IGNORE INTO rounds (round_id, crash_point, timestamp) VALUES (?,?,?)",
                            (data.get("round_id"), data["crash_point"], datetime.datetime.now())
                        )
                        conn.commit()
                    print(f"Round {data.get('round_id')} → Crash @ {data['crash_point']}")
            except Exception as e:
                print("⚠️ Collector Error:", e)

if __name__ == "__main__":
    asyncio.run(collect_live_data())
