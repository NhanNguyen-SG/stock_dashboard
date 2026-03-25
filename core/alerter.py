import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert(ticker: str, price: float, reason: str, secrets: dict):
    """Send email alert via Gmail SMTP."""
    sender = secrets['sender']
    password = secrets['password']
    recipient = secrets['recipient']

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = f'🚨 Stock Alert: {ticker} Anomaly Detected'

    body = f"""
    Stock Alert Notification
    ========================
    Ticker:  {ticker}
    Price:   ${price:.2f}
    Reason:  {reason}
    
    Log in to your dashboard to view details.
    """
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
    
    print(f"Alert sent for {ticker} at ${price:.2f}")