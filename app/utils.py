import pandas as pd
import numpy as np

def clean_data(df):
    df = df.dropna(subset=["crash_point"])
    df = df[df["crash_point"] > 1.0]
    return df

def add_lag_features(df, lags=[1, 2, 3]):
    for lag in lags:
        df[f"lag_{lag}"] = df["crash_point"].shift(lag)
    return df.dropna()

def apply_time_decay(df, decay_factor=0.995):
    weights = np.power(decay_factor, np.arange(len(df))[::-1])
    df["weight"] = weights
    return df

def rolling_mean_feature(df, window=10):
    df["rolling_mean"] = df["crash_point"].rolling(window).mean()
    return df
