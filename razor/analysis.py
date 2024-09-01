from collections import defaultdict
from quarantine import quarantine_process
from alert import send_alert
from utils.logger import get_logger

logger = get_logger(__name__)

command_threshold = 10  # Example threshold
user_command_count = defaultdict(int)

def analyze_user_behavior(process_info):
    user_command_count[process_info['username']] += 1
    logger.info(f"User {process_info['username']} executed command. Count: {user_command_count[process_info['username']]}")
    
    if user_command_count[process_info['username']] > command_threshold:
        logger.warning(f"Potential Threat Detected: User {process_info['username']} exceeded command threshold.")
        send_alert(process_info['username'], user_command_count[process_info['username']])
        quarantine_process(process_info)
