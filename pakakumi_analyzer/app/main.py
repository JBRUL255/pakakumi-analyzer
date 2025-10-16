from fastapi import FastAPI
from pakakumi_analyzer.app.db import init_db
from pakakumi_analyzer.app.models import predict_cashout
import asyncio
import threading
from pakakumi_analyzer.app.collector import run_collector_loop

app = FastAPI(title="PakaKumi Analyzer")

@app.on_event("startup")
async def startup_event():
    # Initialize DB
    print("🗄️ Initializing database...")
    init_db()
    print("✅ Database ready.")

    # Start collector in background
    def start_collector():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_collector_loop())

    threading.Thread(target=start_collector, daemon=True).start()
    print("🕸️ Collector started in background.")


@app.get("/")
def home():
    return {"message": "Welcome to PakaKumi Analyzer!"}


@app.get("/predict")
def predict():
    try:
        prediction = predict_cashout()
        return {"cashout_point": round(prediction, 2)}
    except Exception as e:
        return {"error": str(e)}
