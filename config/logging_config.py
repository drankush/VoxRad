import logging
import os
from pathlib import Path

def setup_logging(debug=False):
    """Configure logging for VoxRad application."""
    log_level = logging.DEBUG if debug else logging.INFO

    log_dir = Path.home() / '.voxrad' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'voxrad.log'

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING if not debug else logging.DEBUG)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    return logging.getLogger(__name__)

def get_logger(name):
    """Get a logger instance for the given module name."""
    return logging.getLogger(name)
