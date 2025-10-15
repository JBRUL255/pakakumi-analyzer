import numpy as np

def detect_anomalies(df, threshold=3):
    mean = np.mean(df["crash_point"])
    std = np.std(df["crash_point"])
    df["anomaly"] = np.abs(df["crash_point"] - mean) > threshold * std
    return df
