from pakakumi_analyzer.app.utils import clean_data, add_lag_features, rolling_mean_feature, apply_time_decay

def build_features(df):
    df = clean_data(df)
    df = add_lag_features(df)
    df = rolling_mean_feature(df)
    df = apply_time_decay(df)
    df = df.dropna()
    return df
