# pakakumi_analyzer/app/serve.py

from fastapi import FastAPI
from pakakumi_analyzer.app.db import get_latest_rounds, get_all_rounds, init_db
from pakakumi_analyzer.app.models import predict_cashout, train_model
import traceback

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print("🗄️ Initializing database...")
    init_db()
    print("✅ Database ready.")

    try:
        rounds = get_all_rounds()
        if rounds:
            print("⚙️ Training model...")
            train_model(rounds)
            print("✅ Model trained successfully.")
        else:
            print("⚠️ No rounds yet — waiting for collector.")
    except Exception as e:
        print("❌ Startup error:", e)
        print(traceback.format_exc())


@app.get("/")
def root():
    return {"message": "Paka Kumi Analyzer Live ✅"}


@app.get("/predict")
def predict():
    try:
        rounds = get_latest_rounds(limit=50)
        if not rounds:
            return {"error": "No data found in database yet."}

        prediction = predict_cashout(rounds)
        return {"predicted_cashout": round(prediction, 2)}

    except Exception as e:
        print("❌ Prediction error:", e)
        print(traceback.format_exc())
        return {"error": str(e)}
