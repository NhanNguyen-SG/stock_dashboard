import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_latest(ticker: str, period: str = '5d', interval: str = '1m') -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df = df.reset_index()
    
    # 1. Create the base columns
    df['ticker'] = ticker
    df['fetched_at'] = datetime.now().isoformat()
    
    # 2. Rename columns to match our database
    df = df.rename(columns={
        'Datetime': 'datetime', 
        'Open': 'open', 
        'High': 'high', 
        'Low': 'low', 
        'Close': 'close', 
        'Volume': 'volume'
    })
    
    # 3. Calculate technical indicators
    df['ma_20'] = df['close'].rolling(window=20).mean()
    
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # 4. Explicitly select only what we need (ignores Dividends/Splits)
    final_cols = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'ticker', 'fetched_at', 'rsi', 'ma_20']
    
    return df[final_cols].fillna(0)