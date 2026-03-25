import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    """
    Run Isolation Forest on price/volume data.
    Returns df with 'anomaly' column: True = anomaly detected.
    """
    if len(df) < 10:
        df['anomaly'] = False
        df['anomaly_score'] = 0.0
        return df

    features = df[['close', 'volume']].copy()
    features['price_change'] = features['close'].pct_change().fillna(0)
    features['volume_change'] = features['volume'].pct_change().fillna(0)

    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100
    )
    preds = model.fit_predict(features[['price_change', 'volume_change']])
    df = df.copy()
    df['anomaly'] = preds == -1
    df['anomaly_score'] = model.score_samples(features[['price_change', 'volume_change']])
    return df