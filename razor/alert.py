import smtplib
from email.mime.text import MIMEText
from utils.logger import get_logger

logger = get_logger(__name__)

def send_alert(user, command_count):
    msg = MIMEText(f"Alert: User {user} has executed {command_count} commands in a short period.")
    msg['Subject'] = 'EDR Threat Alert'
    msg['From'] = 'edr-system@example.com'
    msg['To'] = 'admin@example.com'

    try:
        with smtplib.SMTP('localhost') as server:
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
        logger.info(f"Sent alert email for user {user}.")
    except Exception as e:
        logger.error(f"Failed to send alert email: {e}")
