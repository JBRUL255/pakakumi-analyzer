# pakakumi_analyzer/app/main.py
import threading
import asyncio
import uvicorn
from fastapi import FastAPI
from pakakumi_analyzer.app.db import init_db
from pakakumi_analyzer.app.routes import router
from pakakumi_analyzer.app.collector import collect_data_continuously

app = FastAPI(title="PakaKumi Analyzer API")
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    print("🚀 Initializing database...")
    init_db()

    # Start background collector
    def run_collector():
        asyncio.run(collect_data_continuously())

    threading.Thread(target=run_collector, daemon=True).start()
    print("🛰️ Background data collector started.")

if __name__ == "__main__":
    uvicorn.run("pakakumi_analyzer.app.main:app", host="0.0.0.0", port=8000)
