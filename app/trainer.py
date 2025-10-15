import pandas as pd
import time
from pakakumi_analyzer.app.db import get_db
from pakakumi_analyzer.app.features import build_features
from pakakumi_analyzer.app.models import train_model
from pakakumi_analyzer.app.config import RETRAIN_INTERVAL_HOURS

def retrain_loop():
    while True:
        with get_db() as conn:
            df = pd.read_sql_query("SELECT * FROM rounds ORDER BY id DESC LIMIT 50000", conn)
        if not df.empty:
            df = build_features(df)
            train_model(df)
            print("🧠 Model retrained successfully.")
        else:
            print("⚠️ No data yet, waiting...")
        time.sleep(RETRAIN_INTERVAL_HOURS * 3600)

if __name__ == "__main__":
    retrain_loop()
