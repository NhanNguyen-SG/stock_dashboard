import yfinance as yf
import pandas as pd

def fetch_latest(ticker: str, period: str = '5d', interval: str = '1m') -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df = df.reset_index()
    
    # Calculate Simple Moving Average (MA 20)
    df['ma_20'] = df['Close'].rolling(window=20).mean()
    
    # Calculate RSI manually
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    df = df.rename(columns={
        'Datetime': 'datetime', 'Open': 'open', 'High': 'high', 
        'Low': 'low', 'Close': 'close', 'Volume': 'volume'
    })
    return df.fillna(0)