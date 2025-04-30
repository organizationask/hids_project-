import smtplib
from email.mime.text import MIMEText

def send_email_alert(subject, message, to_email):
    """Send an email alert."""
    from_email = "your_email@example.com"
    password = "your_email_password"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            print("Alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email alert: {e}")