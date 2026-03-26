import streamlit as st
from core.database import load_prices
from core.detector import detect_anomalies

st.set_page_config(page_title="Alert History", layout="wide")

st.title("🚨 Anomaly Log")

ticker = st.sidebar.selectbox("Filter by Ticker", ["AAPL", "TSLA", "NVDA", "BTC-USD"])
df = load_prices(ticker)

if not df.empty:
    df = detect_anomalies(df)
    anomalies = df[df['anomaly']].sort_values('datetime', ascending=False)
    
    if not anomalies.empty:
        st.write(f"Found {len(anomalies)} anomalies for {ticker}:")
        st.dataframe(anomalies[['datetime', 'close', 'rsi', 'anomaly_score']], use_container_width=True)
    else:
        st.success("No anomalies detected yet!")
else:
    st.info("Start the main app to begin logging alerts.")