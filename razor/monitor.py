import psutil
import time
from analysis import analyze_user_behavior
from utils.logger import get_logger

logger = get_logger(__name__)

def monitor_processes():
    processes = {}
    logger.info("Starting process monitoring...")
    
    while True:
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'create_time', 'cmdline']):
                if proc.info['pid'] not in processes:
                    processes[proc.info['pid']] = proc.info
                    logger.info(f"New Process Detected: {proc.info}")
                    analyze_user_behavior(proc.info)
        except Exception as e:
            logger.error(f"Error in monitoring processes: {e}")
        time.sleep(1)
