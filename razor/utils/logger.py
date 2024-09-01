import logging
import os

LOG_DIR = "/var/log/edr_system"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "edr.log"),
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_logger(name):
    return logging.getLogger(name)
