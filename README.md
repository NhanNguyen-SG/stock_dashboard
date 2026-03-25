📈 Real-Time Stock Anomaly DashboardThis is a professional data analytics project that monitors live stock market data, detects price anomalies using Machine Learning, and sends automated email alerts.

🚀 https://stockdashboard-jg44wj4ynsqknmbv8kaxyb.streamlit.app/

🛠️ Tech Stack
- Language: Python
- Framework: Streamlit (Web Dashboard)
- Machine Learning: Scikit-Learn (Isolation Forest for Anomaly Detection)
- Database: SQLite (Local Data Storage)
- APIs: Yahoo Finance (yfinance) for real-time market data
- Alerts: Gmail SMTP (Automated Email System) 

✨ Key Features
- Live Ingestion: Fetches the latest stock prices every minute.
- AI Detection: Uses an Unsupervised ML model to identify "strange" price or volume movements.
- Visualized Data: Interactive charts showing stock trends with anomalies marked in red.Instant
- Alerts: Sends a notification to the user's email as soon as an anomaly is detected.

📁 Project StructurePlaintextstock_dashboard/
```
stock_dashboard/
├── app/
│   ├── app.py          # Main Dashboard Code
│   └── pages/          # Multi-page setup
├── core/
│   ├── data_fetcher.py # YFinance logic
│   ├── database.py     # SQLite logic
│   ├── detector.py     # ML Anomaly model
│   └── alerter.py      # Email SMTP logic
├── data/               # Local database storage
└── requirements.txt    # Library dependencies
```

🔍 Technical Deep Dive

1. Data Engineering & Ingestion
Real-Time Pipeline: The system uses yfinance to pull 1-minute interval data, ensuring the dashboard reflects the most current market conditions.
Persistent Storage: Data is stored in a local SQLite database. This allows the app to maintain historical context for the Machine Learning model even if the app restarts.

2. Machine Learning Model (Anomaly Detection)
Algorithm: The project implements Isolation Forest, an unsupervised learning algorithm perfect for detecting outliers in financial data.
Feature Engineering: The model analyzes Price Change and Volume Change percentages to find "shocks" in the market rather than just high prices.
Scoring: Each data point receives an anomaly_score. If the score falls below a specific threshold (contamination), it is flagged as a risk.

3. Automated Alert System
SMTP Integration: Using Python’s smtplib, the system connects to a Gmail SMTP server to send high-priority alerts.
Logic: An alert is only triggered when the latest data point is flagged as an anomaly, preventing "spam" and ensuring the user only sees critical movements.

4. Cloud Deployment
CI/CD: The project is integrated with GitHub, allowing for continuous deployment to Streamlit Cloud.
Security: Sensitive credentials (email/password) are managed using Streamlit Secrets, ensuring no private data is ever exposed in the public code.

📈 Business Value
Risk Mitigation: Helps traders identify "Flash Crashes" or unusual "Pump and Dump" patterns.

Scalability: The modular code structure (Fetcher -> Database -> Detector) allows for adding more stocks or different ML models easily.
