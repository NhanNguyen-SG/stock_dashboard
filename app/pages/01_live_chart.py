import streamlit as st
import plotly.graph_objects as go
from core.database import load_prices

st.set_page_config(page_title="Live Analytics", layout="wide")

st.title("📊 Detailed Market Analytics")

ticker = st.sidebar.selectbox("Select Ticker", ["AAPL", "TSLA", "NVDA", "BTC-USD"])
df = load_prices(ticker)

if not df.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['close'], name='Price', line=dict(color='#00ff41')))
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['ma_20'], name='Trend', line=dict(color='#ff0055', dash='dot')))
    
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data found. Please run the main Dashboard first.")