from ui.main_window import initialize_ui
from config.settings import load_settings
from utils.encryption import load_groq_key, load_openai_key

if __name__ == "__main__":
    # Load settings and keys on startup
    load_settings()  # This initializes save_directory

    # Initialize the main UI
    initialize_ui()
