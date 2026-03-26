# 📟 AI Predictive Trading Terminal
> **Live Demo:** [https://stockdashboard-jg44wj4ynsqknmbv8kaxyb.streamlit.app/](https://stockdashboard-jg44wj4ynsqknmbv8kaxyb.streamlit.app/)

A real-time financial analytics platform built with **Python** and **Unsupervised Machine Learning**. This terminal uses a high-contrast cinematic aesthetic to visualize market volatility and detect price anomalies in real-time.

## 🚀 Key Features (v2.0)
* **Multi-Stock Monitoring:** Track up to 5 assets simultaneously (Stocks, Crypto, Forex).
* **Technical Indicator Engine:** Manual implementation of **RSI (14)** and **SMA (20)** to bypass library dependencies and show raw data logic.
* **AI Anomaly Detection:** Uses an **Isolation Forest** model to identify "shocks" in price and volume.
* **Cinematic UI:** Custom CSS implementation for a high-contrast "Wong Kar-wai" inspired dark mode.
* **Automated Alerting:** Integrated with **Gmail SMTP** to send instant notifications when the AI flags a risk.

## 🛠️ Tech Stack
* **Language:** Python 3.9
* **ML Model:** Scikit-Learn (Isolation Forest)
* **Data:** yfinance API
* **Database:** SQLite3 (Local persistence)
* **UI/UX:** Streamlit & Plotly (Custom CSS)

## 📂 Project Structure
```text
stock_dashboard/
├── app/
│   ├── app.py              # Main Dashboard (Cinematic UI)
│   └── pages/              # 01_Live_Chart & 02_Alert_Logs
├── core/
│   ├── data_fetcher.py     # Manual RSI & SMA Math
│   ├── database.py         # SQLite Schema Management
│   ├── detector.py         # ML Anomaly Model
│   └── alerter.py          # SMTP Email logic
└── requirements.txt        # Dependencies
