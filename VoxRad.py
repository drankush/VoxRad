from ui.main_window import initialize_ui
from config.logging_config import setup_logging
import logging

if __name__ == "__main__":
    setup_logging(debug=False)
    logger = logging.getLogger(__name__)
    logger.info("Starting VoxRad application")
    initialize_ui()

