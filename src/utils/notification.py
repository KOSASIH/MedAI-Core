# utils/notification.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class NotificationService:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, to_email: str, subject: str, message: str):
        """Send an email notification."""
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.username, self.password)
                server.send_message(msg)
            print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")

# Example usage:
if __name__ == "__main__":
    notification_service = NotificationService(
        smtp_server='smtp.gmail.com',
        smtp_port=587,
        username='your_email@gmail.com',
        password='your_password'
    )
    
    notification_service.send_email(
        to_email='recipient@example.com',
        subject='Anomaly Detected in Vital Signs',
        message='An anomaly has been detected in your vital signs. Please consult a doctor.'
    )
