from fastapi import FastAPI
from pakakumi_analyzer.app.db import get_db
import pandas as pd
from pakakumi_analyzer.app.features import build_features
from pakakumi_analyzer.app.models import load_model

app = FastAPI(title="Pakakumi Analyzer API")

@app.get("/predict")
def predict_next():
    with get_db() as conn:
        df = pd.read_sql_query("SELECT * FROM rounds ORDER BY id DESC LIMIT 50", conn)
    if len(df) < 5:
        return {"status": "error", "message": "Not enough data yet."}

    df = build_features(df)
    model = load_model()
    X = df.drop(columns=["crash_point", "timestamp", "weight"])
    pred = model.predict(X.tail(1))[0]
    return {"predicted_cashout": round(float(pred), 2)}
