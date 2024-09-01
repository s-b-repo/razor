import os
import shutil
import psutil
from utils.logger import get_logger

logger = get_logger(__name__)
QUARANTINE_DIR = "/var/quarantine"
os.makedirs(QUARANTINE_DIR, exist_ok=True)

def quarantine_process(proc_info):
    try:
        proc = psutil.Process(proc_info['pid'])
        proc.terminate()
        logger.info(f"Terminated process: {proc_info['name']} (PID {proc_info['pid']})")

        exe_path = proc_info['cmdline'][0] if proc_info['cmdline'] else None
        if exe_path and os.path.isfile(exe_path):
            quarantine_path = os.path.join(QUARANTINE_DIR, os.path.basename(exe_path))
            shutil.move(exe_path, quarantine_path)
            logger.info(f"Moved executable {exe_path} to quarantine.")
        else:
            logger.info(f"No executable found for process {proc_info['name']} (PID {proc_info['pid']}).")
    except Exception as e:
        logger.error(f"Failed to quarantine process {proc_info['name']} (PID {proc_info['pid']}): {e}")

def quarantine_file(file_path):
    try:
        quarantine_path = os.path.join(QUARANTINE_DIR, os.path.basename(file_path))
        shutil.move(file_path, quarantine_path)
        logger.info(f"File {file_path} moved to quarantine.")
    except Exception as e:
        logger.error(f"Failed to quarantine file {file_path}: {e}")
