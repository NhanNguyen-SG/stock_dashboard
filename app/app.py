import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time
from core.data_fetcher import fetch_latest
from core.database import init_db, save_prices, load_prices
from core.detector import detect_anomalies

# 1. Cinematic Neon Setup
st.set_page_config(page_title="UCF Terminal", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    [data-testid="stMetricValue"] { 
        color: #00ff41; 
        text-shadow: 0 0 10px #00ff41; 
        font-family: 'Courier New', monospace; 
    }
    .stExpander { border: 1px solid #30363d !important; background-color: #0d1117 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 AI Predictive Terminal")
init_db()

# 2. Multi-Stock Sidebar
st.sidebar.header("🕹️ Control Center")
tickers = st.sidebar.multiselect("Select Assets", 
                                 ["AAPL", "TSLA", "NVDA", "BTC-USD", "GOOGL"], 
                                 default=["AAPL"])

refresh_rate = st.sidebar.slider("Refresh Interval (s)", 30, 300, 60)

# 3. Main Display Loop
for ticker in tickers:
    with st.expander(f"🛰️ LIVE FEED: {ticker}", expanded=True):
        # Fetch and store
        df_new = fetch_latest(ticker)
        save_prices(df_new)
        
        # Load and detect
        df = load_prices(ticker)
        df = detect_anomalies(df)
        anomalies = df[df['anomaly']]
        latest = df.iloc[-1]

        # Metric Header
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Price", f"${latest['close']:.2f}")
        c2.metric("RSI (14)", f"{latest['rsi']:.1f}")
        c3.metric("MA (20)", f"${latest['ma_20']:.2f}")
        c4.metric("Status", "⚠️ ANOMALY" if latest['anomaly'] else "✅ STABLE")

        # High-Contrast Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['close'], name='Price', line=dict(color='#00ff41', width=2)))
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['ma_20'], name='Trend (MA)', line=dict(color='#ff0055', width=1, dash='dot')))
        fig.add_trace(go.Scatter(x=anomalies['datetime'], y=anomalies['close'], mode='markers', name='Alert', marker=dict(color='yellow', size=8)))
        
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=20,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, key=f"chart_{ticker}")

# Auto-refresh
time.sleep(refresh_rate)
st.rerun()