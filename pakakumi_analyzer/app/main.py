from fastapi import FastAPI
import asyncio
import threading
from pakakumi_analyzer.app.db import init_db
from pakakumi_analyzer.app.models import predict_cashout
from pakakumi_analyzer.app.collector import run_collector_loop

app = FastAPI(title="PakaKumi Analyzer")

@app.on_event("startup")
async def startup_event():
    print("🗄️ Initializing database...")
    init_db()
    print("✅ Database ready.")

    def background_collector():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_collector_loop())

    thread = threading.Thread(target=background_collector, daemon=True)
    thread.start()
    print("🕸️ Collector thread started.")

    # Optional: keep Render awake by pinging itself
    async def keep_alive():
        while True:
            try:
                import httpx
                async with httpx.AsyncClient() as client:
                    await client.get("https://pakakumi-analyzer.onrender.com/")
                print("🔁 Keep-alive ping sent.")
            except Exception as e:
                print(f"⚠️ Keep-alive failed: {e}")
            await asyncio.sleep(300)  # every 5 min

    asyncio.create_task(keep_alive())

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/predict")
def predict():
    try:
        result = predict_cashout()
        return {"cashout_point": round(result, 2)}
    except Exception as e:
        return {"error": str(e)}
