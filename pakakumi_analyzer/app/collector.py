# pakakumi_analyzer/app/collector.py

from pakakumi_analyzer.app.db import init_db
init_db()
import asyncio
import socketio
from pakakumi_analyzer.app.db import insert_round, init_db
import traceback

WS_URL = "https://api.pakakumi.com"
API_VERSION = 112

sio = socketio.AsyncClient(
    reconnection=True,
    reconnection_attempts=5,
    reconnection_delay=5,
    logger=True,
    engineio_logger=True,
)

async def connect_to_pakakumi():
    print("🔌 Connecting to PakaKumi WebSocket...")
    try:
        await sio.connect(f"{WS_URL}", transports=["websocket"], query={"v": str(API_VERSION)})
        print("✅ Connected to PakaKumi WebSocket")
    except Exception as e:
        print("❌ Connection failed:", e)
        traceback.print_exc()

@sio.event
async def connect():
    print("🟢 WebSocket connection established!")

@sio.event
async def disconnect():
    print("🔴 Disconnected from WebSocket. Reconnecting...")

@sio.on("game:crash")
async def on_crash(data):
    """
    Triggered when a round ends.
    Example data = {'crash_point': 2.37, ...}
    """
    try:
        if isinstance(data, dict) and "crash_point" in data:
            cashout = float(data["crash_point"])
            insert_round(cashout)
            print(f"💾 Saved crash point: {cashout}")
    except Exception as e:
        print("⚠️ Error processing crash event:", e)
        traceback.print_exc()

async def run_collector():
    init_db()
    await connect_to_pakakumi()
    await sio.wait()  # Keep connection alive
