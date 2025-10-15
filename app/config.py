import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.pakakumi.com")
WS_URL = os.getenv("WS_URL", "wss://api.pakakumi.com/socket.io/?v=112&EIO=4&transport=websocket")

DB_PATH = os.getenv("DB_PATH", "data/pakakumi.db")
MODEL_PATH = os.getenv("MODEL_PATH", "models/latest_model.pkl")
RETRAIN_INTERVAL_HOURS = int(os.getenv("RETRAIN_INTERVAL_HOURS", 6))
TIME_DECAY_FACTOR = float(os.getenv("TIME_DECAY_FACTOR", 0.97))
MAX_DATA_POINTS = int(os.getenv("MAX_DATA_POINTS", 50000))
ENABLE_LIVE_METRICS = os.getenv("ENABLE_LIVE_METRICS", "true").lower() == "true"
