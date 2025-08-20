# app/utils/logger.py
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class Logger:
    def __init__(self):
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Logger configuration
        self.logger = logging.getLogger("delivery_order_service")
        self.logger.setLevel(logging.DEBUG if os.getenv("DEBUG", "False").lower() == "true" else logging.INFO)

        # Log format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # File handler (rotates daily)
        file_handler = TimedRotatingFileHandler(
            filename=log_dir / "delivery_order_service.log",
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


# Create singleton instance
logger = Logger().get_logger()
logger.info("Logger initialized for Delivery Order Service")