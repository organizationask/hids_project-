import smtplib
from email.mime.text import MIMEText

def send_email_alert(subject, body, recipient_email):
    """Send an email alert."""
    sender_email = "your_email@example.com"
    sender_password = "your_password"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        print(f"Failed to send email alert: {e}")