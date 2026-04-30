# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from pathlib import Path
# from dotenv import load_dotenv

# load_dotenv(dotenv_path=Path(__file__).parent / ".env")


# def send_email_smtp(to: str, subject: str, message: str, cc: str = "", bcc: str = ""):
#     """Send email using Gmail SMTP with optional CC and BCC."""
#     sender = os.getenv("SENDER_EMAIL")
#     password = os.getenv("SENDER_PASSWORD")

#     if not sender or not password:
#         print("❌ SENDER_EMAIL or SENDER_PASSWORD not set in .env")
#         return

#     msg = MIMEMultipart()
#     msg["From"] = sender
#     msg["To"] = to
#     msg["Subject"] = subject

#     if cc:
#         msg["Cc"] = cc

#     if bcc:
#         msg["Bcc"] = bcc

#     msg.attach(MIMEText(message, "plain"))

#     # Combine all recipients
#     recipients = [to]
#     if cc:
#         recipients += [c.strip() for c in cc.split(",")]
#     if bcc:
#         recipients += [b.strip() for b in bcc.split(",")]

#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(sender, password)
#             server.sendmail(sender, recipients, msg.as_string())
#         print(f"📨 Email sent to {to}")
#         if cc:
#             print(f"📋 CC: {cc}")
#         if bcc:
#             print(f"🔒 BCC: {bcc}")
#     except smtplib.SMTPAuthenticationError:
#         print("❌ Authentication failed. Check SENDER_EMAIL and SENDER_PASSWORD in .env")
#     except Exception as e:
#         print(f"❌ Failed to send email: {e}")

# --------------------------------------------------------------------------
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")


def send_email_smtp(to: str, subject: str, message: str, cc: str = "", bcc: str = ""):
    """Send email using Gmail SMTP - supports any domain, multiple recipients."""
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_PASSWORD")

    if not sender or not password:
        print("❌ SENDER_EMAIL or SENDER_PASSWORD not set in .env")
        return

    # Split multiple emails
    to_list  = [t.strip() for t in to.split(",") if t.strip()]
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

    # All recipients combined
    all_recipients = to_list + cc_list + bcc_list

    # Try SSL first (port 465), fallback to TLS (port 587)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, all_recipients, msg.as_string())
        print(f"📨 Email sent to: {', '.join(to_list)}")
        if cc_list:
            print(f"📋 CC: {', '.join(cc_list)}")
        if bcc_list:
            print(f"🔒 BCC: {', '.join(bcc_list)}")

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Check SENDER_EMAIL and SENDER_PASSWORD in .env")

    except Exception:
        # Fallback to TLS port 587
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, all_recipients, msg.as_string())
            print(f"📨 Email sent to: {', '.join(to_list)}")
            if cc_list:
                print(f"📋 CC: {', '.join(cc_list)}")
            if bcc_list:
                print(f"🔒 BCC: {', '.join(bcc_list)}")

        except smtplib.SMTPAuthenticationError:
            print("❌ Authentication failed. Check SENDER_EMAIL and SENDER_PASSWORD in .env")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")