from monitor import monitor_processes
from utils.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("EDR System starting...")
    try:
        monitor_processes()
    except KeyboardInterrupt:
        logger.info("EDR System stopped by user.")
    except Exception as e:
        logger.error(f"Unexpected error in EDR System: {e}")
