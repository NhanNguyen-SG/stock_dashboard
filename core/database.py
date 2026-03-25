import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path('data/stocks.db')

def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            ticker TEXT,
            fetched_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_prices(df: pd.DataFrame):
    conn = sqlite3.connect(DB_PATH)
    df['datetime'] = df['datetime'].astype(str)
    df.to_sql('prices', conn, if_exists='append', index=False)
    conn.close()

def load_prices(ticker: str, limit: int = 500) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(
        'SELECT * FROM prices WHERE ticker=? ORDER BY datetime DESC LIMIT ?',
        conn, params=(ticker, limit)
    )
    conn.close()
    return df.sort_values('datetime').reset_index(drop=True)