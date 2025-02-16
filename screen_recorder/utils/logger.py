import logging
import os
from datetime import datetime

class Logger:
    """Application logging functionality"""
    
    def __init__(self):
        self._setup_logger()

    def _setup_logger(self):
        """Configure logging settings"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(
            log_dir,
            f"screen_recorder_{datetime.now().strftime('%Y%m%d')}.log"
        )

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def error(message):
        logging.error(message)

    @staticmethod
    def warning(message):
        logging.warning(message) 