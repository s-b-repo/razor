import numpy as np
from quarantine import quarantine_process
from alert import send_alert
from utils.logger import get_logger
from utils.model import load_model

logger = get_logger(__name__)
model = load_model("model/threat_detection_model.pkl")

command_threshold = 10
user_command_count = defaultdict(int)

def extract_features(process_info):
    # Example feature extraction
    features = [
        len(process_info['cmdline']),              # Length of command line
        process_info['create_time'],               # Process creation time
        user_command_count[process_info['username']], # Number of commands executed by the user
        1 if process_info['username'] == 'root' else 0,  # Is the user root?
        len(process_info['cmdline'][0]) if process_info['cmdline'] else 0,  # Length of executable name
    ]
    return np.array(features).reshape(1, -1)

def analyze_user_behavior(process_info):
    features = extract_features(process_info)
    prediction = model.predict(features)
    
    logger.info(f"Predicted {prediction[0]} for process {process_info['name']} (PID {process_info['pid']}).")
    
    if prediction[0] == 1:  # Assuming 1 means 'malicious'
        logger.warning(f"Malicious behavior detected: {process_info['name']} (PID {process_info['pid']})")
        send_alert(process_info['username'], user_command_count[process_info['username']])
        quarantine_process(process_info)
