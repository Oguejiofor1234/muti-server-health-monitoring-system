# Create test_email.py
from config import EMAIL_CONFIG
import smtplib
from email.mime.text import MIMEText

msg = MIMEText('This is a test email from Health Monitoring System')
msg['Subject'] = 'Test Email'
msg['From'] = EMAIL_CONFIG['sender_email']
msg['To'] = EMAIL_CONFIG['recipient_email']

try:
    server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
    server.starttls()
    server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
    server.send_message(msg)
    server.quit()
    print("✓ Test email sent successfully!")
except Exception as e:
    print(f"✗ Email failed: {e}")