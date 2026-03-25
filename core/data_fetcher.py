import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_latest(ticker: str, period: str = '1d', interval: str = '1m') -> pd.DataFrame:
    """Fetch latest stock data from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df = df.reset_index()
    df['ticker'] = ticker
    df['fetched_at'] = datetime.now().isoformat()
    df = df.rename(columns={
        'Datetime': 'datetime',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    })
    return df[['datetime', 'open', 'high', 'low', 'close', 'volume', 'ticker', 'fetched_at']]