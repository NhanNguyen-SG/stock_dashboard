import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    """
    Finds anomalies using Price, Volume, RSI, and Moving Average gap.
    """
    if len(df) < 20: # Need at least 20 rows for MA/RSI to work
        df['anomaly'] = False
        df['anomaly_score'] = 0.0
        return df

    # Create a copy so we don't mess up the original data
    analysis_df = df.copy()

    # Feature 1: Price vs Moving Average (Is the price too far from the trend?)
    analysis_df['ma_gap'] = analysis_df['close'] - analysis_df['ma_20']

    # Select the features for the AI to look at
    # We use: Close Price, Volume, RSI, and the MA Gap
    features = ['close', 'volume', 'rsi', 'ma_20']
    
    # Fill any empty NAs with 0 so the model doesn't crash
    X = analysis_df[features].fillna(0)

    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100
    )

    # -1 means Anomaly, 1 means Normal
    preds = model.fit_predict(X)
    
    df = df.copy()
    df['anomaly'] = (preds == -1)
    df['anomaly_score'] = model.score_samples(X)
    
    return df