# pakakumi_analyzer/app/models.py

import numpy as np
import random
import pickle
import os

MODEL_PATH = os.getenv("MODEL_PATH", "pakakumi_model.pkl")


def train_model(round_data):
    """
    Trains a very simple predictive model based on recent rounds.
    In production, you could replace this with scikit-learn, XGBoost, etc.
    
    Args:
        round_data (list[float]): List of past cashout multipliers.
    
    Returns:
        dict: Model metadata (e.g. average multiplier, etc.)
    """

    if not round_data:
        round_data = [1.5, 1.7, 2.1, 1.3, 1.9]

    model = {
        "mean": float(np.mean(round_data)),
        "std": float(np.std(round_data)),
    }

    # Save model locally (Render keeps /app directory writable during runtime)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    return model


def load_model():
    """Loads the model from disk or returns default model."""
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    return {"mean": 1.8, "std": 0.3}


def predict_cashout(recent_rounds):
    """
    Predict the next cashout multiplier based on the trained model.

    Args:
        recent_rounds (list[float]): List of recent cashout multipliers.

    Returns:
        float: Predicted next cashout multiplier.
    """

    model = load_model()

    if not recent_rounds:
        return round(model["mean"], 2)

    # Simple weighted average + random noise
    recent_avg = np.mean(recent_rounds[-10:])
    noise = random.uniform(-model["std"], model["std"])
    prediction = max(1.0, recent_avg + noise)

    return round(prediction, 2)
