# pakakumi_analyzer/app/models.py

import numpy as np
import random

# Simple placeholder model for now
# Later we can load a trained model (like scikit-learn or XGBoost)
# but this ensures no ImportError and works in production

def predict_cashout(recent_rounds):
    """
    Predicts the next cashout multiplier based on recent game rounds.
    For now, this is a stub model that returns a simulated prediction.

    Args:
        recent_rounds (list[float]): List of recent cashout multipliers.

    Returns:
        float: Predicted next cashout multiplier.
    """

    if not recent_rounds:
        # Default prediction if no data
        return round(random.uniform(1.1, 2.0), 2)

    # Basic heuristic: weighted average with randomness
    avg = np.mean(recent_rounds)
    noise = random.uniform(-0.3, 0.3)
    prediction = max(1.0, avg + noise)

    return round(prediction, 2)

