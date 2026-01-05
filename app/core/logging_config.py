import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.config import settings

def setup_logging():
    """
    Configures the logging system for the application.
    """
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Basic Config
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Root Logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Console Handler (Stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (Rotating)
    file_handler = RotatingFileHandler(
        log_dir / "app.log", maxBytes=10*1024*1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Silence noisy libraries
    logging.getLogger("uvicorn.access").handlers = [] # We might want to keep this or redirect
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logger.info("Logging configured successfully.")

def get_logger(name: str):
    return logging.getLogger(name)
