from fastapi import FastAPI
from pakakumi_analyzer.app.models import predict_cashout
from pakakumi_analyzer.app.db import get_latest_rounds

app = FastAPI(title="PakaKumi Analyzer API")

@app.get("/")
def home():
    return {"message": "Welcome to PakaKumi Analyzer API 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/predict")
def predict_endpoint():
    # Example: fetch last few rounds and predict
    recent_rounds = get_latest_rounds(limit=50)
    cashout = predict_cashout(recent_rounds)
    return {"predicted_cashout": cashout}
