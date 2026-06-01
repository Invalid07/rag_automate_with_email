import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")


def send_email_smtp(to: str, subject: str, message: str, cc: str = "", bcc: str = "",
                    sender_email: str = "", sender_password: str = ""):
    """Send email using Gmail SMTP - supports any domain, multiple recipients."""

    # Prefer passed-in values, fallback to .env
    sender = sender_email or os.getenv("SENDER_EMAIL")
    password = sender_password or os.getenv("SENDER_PASSWORD")

    if not sender or not password:
        return False, "SENDER_EMAIL or SENDER_PASSWORD not set"

    # Split multiple emails
    to_list  = [t.strip() for t in to.split(",")  if t.strip()]
    cc_list  = [c.strip() for c in cc.split(",")  if c.strip()]
    bcc_list = [b.strip() for b in bcc.split(",") if b.strip()]

    msg = MIMEMultipart()
    msg["From"]    = sender
    msg["To"]      = ", ".join(to_list)
    msg["Subject"] = subject

    if cc_list:
        msg["Cc"] = ", ".join(cc_list)
    if bcc_list:
        msg["Bcc"] = ", ".join(bcc_list)

    msg.attach(MIMEText(message, "plain"))

    all_recipients = to_list + cc_list + bcc_list

    # Try SSL first (port 465), fallback to TLS (port 587)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, all_recipients, msg.as_string())
        return True, f"Email sent to: {', '.join(to_list)}"

    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Check SENDER_EMAIL and SENDER_PASSWORD."

    except Exception:
        # Fallback to TLS port 587
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, all_recipients, msg.as_string())
            return True, f"Email sent to: {', '.join(to_list)}"

        except smtplib.SMTPAuthenticationError:
            return False, "Authentication failed. Check SENDER_EMAIL and SENDER_PASSWORD."
        except Exception as e:
            return False, f"Failed to send email: {e}"
