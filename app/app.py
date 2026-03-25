import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import plotly.graph_objects as go
import time
from core.data_fetcher import fetch_latest
from core.database import init_db, save_prices, load_prices
from core.detector import detect_anomalies
from core.alerter import send_alert

st.set_page_config(page_title="Stock Anomaly Dashboard", layout="wide")
st.title("📈 Real-Time Stock Anomaly Dashboard")

init_db()

# Sidebar
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Ticker Symbol", "AAPL").upper()
refresh_rate = st.sidebar.slider("Refresh (seconds)", 30, 300, 60)
alert_enabled = st.sidebar.checkbox("Enable Email Alerts", True)

# Fetch and save
with st.spinner(f"Fetching {ticker} data..."):
    df_new = fetch_latest(ticker)
    save_prices(df_new)

# Load and detect
df = load_prices(ticker)
df = detect_anomalies(df)

anomalies = df[df['anomaly']]
latest_price = df['close'].iloc[-1]

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"${latest_price:.2f}")
col2.metric("Anomalies Detected", len(anomalies))
col3.metric("Data Points", len(df))

st.divider()

# Chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['datetime'], y=df['close'],
    mode='lines', name='Price',
    line=dict(color='royalblue', width=2)
))
fig.add_trace(go.Scatter(
    x=anomalies['datetime'], y=anomalies['close'],
    mode='markers', name='Anomaly',
    marker=dict(color='red', size=10, symbol='x')
))
fig.update_layout(
    title=f"{ticker} Price with Anomalies",
    xaxis_title="Time",
    yaxis_title="Price ($)",
    hovermode="x unified",
    height=500
)
st.plotly_chart(fig, use_container_width=True)

# Anomaly table
if not anomalies.empty:
    st.subheader("🚨 Anomalies Detected")
    st.dataframe(
        anomalies[['datetime', 'close', 'volume', 'anomaly_score']].tail(10),
        use_container_width=True
    )

    # Send alert for latest anomaly
    if alert_enabled:
        try:
            secrets = {
                'sender': st.secrets['email']['sender'],
                'password': st.secrets['email']['password'],
                'recipient': st.secrets['email']['recipient']
            }
            latest_anomaly = anomalies.iloc[-1]
            send_alert(ticker, latest_anomaly['close'], 
                      "Unusual price/volume movement detected", secrets)
            st.success("Alert email sent!")
        except Exception as e:
            st.warning(f"Alert not sent: {e}")

# Auto refresh
st.caption(f"Auto-refreshing every {refresh_rate} seconds...")
time.sleep(refresh_rate)
st.rerun()