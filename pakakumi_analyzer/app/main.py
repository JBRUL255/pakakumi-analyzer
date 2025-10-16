import asyncio
import threading
from fastapi import FastAPI
from pakakumi_analyzer.app.db import init_db
from pakakumi_analyzer.app.models import predict_cashout
from pakakumi_analyzer.app.collector import run_collector_loop

app = FastAPI(title="PakaKumi Analyzer")

@app.on_event("startup")
async def startup_event():
    print("🗄️ Initializing database...")
    init_db()
    print("✅ Database ready.")

    # Start collector in background thread
    def start_collector():
        print("🕸️ Collector thread starting...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_collector_loop())

    thread = threading.Thread(target=start_collector, daemon=True)
    thread.start()
    print("🕸️ Collector started successfully.")

@app.get("/")
def home():
    return {"status": "running", "message": "Analyzer active and collecting data."}

@app.get("/predict")
def predict():
    try:
        result = predict_cashout()
        return {"predicted_cashout": round(result, 2)}
    except Exception as e:
        return {"error": str(e)}
