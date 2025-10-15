import pickle
from lightgbm import LGBMRegressor
from pakakumi_analyzer.app.config import MODEL_PATH

def train_model(df):
    X = df.drop(columns=["crash_point", "timestamp", "weight"])
    y = df["crash_point"]
    weights = df["weight"]

    model = LGBMRegressor(n_estimators=200, learning_rate=0.05)
    model.fit(X, y, sample_weight=weights)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    return model

def load_model():
    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return LGBMRegressor()
