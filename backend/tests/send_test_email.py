import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Load env vars
MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
MAIL_PORT = int(os.getenv('MAIL_PORT', 1025))
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@example.com')

def send_test_email():
    msg = EmailMessage()
    msg['Subject'] = 'Test Email from Command Line'
    msg['From'] = MAIL_DEFAULT_SENDER
    msg['To'] = 'test@localhost'
    msg.set_content('Hello from your local environment! This is a test email sent via MailHog.')

    try:
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            server.set_debuglevel(1)  # Show SMTP debug output
            if os.getenv('MAIL_USE_TLS', 'False') == 'True':
                server.starttls()
            if MAIL_USERNAME and MAIL_PASSWORD:
                server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(msg)
            print("✅ Test email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)

if __name__ == "__main__":
    send_test_email()
