import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")


def send_email_smtp(to: str, subject: str, message: str, cc: str = "", bcc: str = ""):
    """Send email using Gmail SMTP with optional CC and BCC."""
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_PASSWORD")

    if not sender or not password:
        print("❌ SENDER_EMAIL or SENDER_PASSWORD not set in .env")
        return

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject

    if cc:
        msg["Cc"] = cc

    if bcc:
        msg["Bcc"] = bcc

    msg.attach(MIMEText(message, "plain"))

    # Combine all recipients
    recipients = [to]
    if cc:
        recipients += [c.strip() for c in cc.split(",")]
    if bcc:
        recipients += [b.strip() for b in bcc.split(",")]

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipients, msg.as_string())
        print(f"📨 Email sent to {to}")
        if cc:
            print(f"📋 CC: {cc}")
        if bcc:
            print(f"🔒 BCC: {bcc}")
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Check SENDER_EMAIL and SENDER_PASSWORD in .env")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")