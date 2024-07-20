import os
import configparser
from config.config import config
from utils.encryption import get_password_from_user, load_groq_key, load_openai_key
from ui.utils import update_status
from tkinter import messagebox

def get_default_config_path():
    """Returns the platform-specific default config file path."""
    if os.name == "nt":  # Windows
        config_dir = os.path.join(os.environ["APPDATA"], "VOXRAD")
    else:  # Assuming macOS or Linux
        config_dir = os.path.join(os.path.expanduser("~"), ".voxrad")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return os.path.join(config_dir, "settings.ini")

def load_settings():
    """Loads settings from the config file, checks for key existence,
       and prompts for password if needed.
    """
    config_path = get_default_config_path()
    config_parser = configparser.ConfigParser()
    config_parser.read(config_path)

    if "DEFAULT" in config_parser:
        config.save_directory = config_parser["DEFAULT"].get("WorkingDirectory", os.path.dirname(config_path))
        config.BASE_URL = config_parser["DEFAULT"].get("OpenAIBaseURL", "https://api.openai.com/v1")
        config.SELECTED_MODEL = config_parser["DEFAULT"].get("SelectedModel", "llama3-70b-8192")
    else:
        print("Warning: 'DEFAULT' section not found in settings.ini. Using default values.")
        config.save_directory = os.path.dirname(config_path)
        config.BASE_URL = "https://api.openai.com/v1"

    print(f"Using save_directory: {config.save_directory}")  # Debug output
    print(f"Using OpenAI Base URL: {config.BASE_URL}")
    print(f"Using Selected Model: {config.SELECTED_MODEL}")

    # Groq Key Handling
    salt_path = os.path.join(config.save_directory, ".myapp_salt")
    groq_key_path = os.path.join(config.save_directory, "groq_key.encrypted")

    if os.path.exists(salt_path) and os.path.exists(groq_key_path):
        password = get_password_from_user("Enter your password to unlock the Transcription Model key:")
        if password:
            if not load_groq_key(groq_key_path, password):
                messagebox.showerror("Error", "Incorrect password for Transcription Model key.")
    else:
        update_status("Kindly save the Groq key in settings.")

    # OpenAI Key Handling
    salt_path = os.path.join(config.save_directory, ".openai_salt") # Update salt file name
    openai_key_path = os.path.join(config.save_directory, "openai_key.encrypted")
    if os.path.exists(salt_path) and os.path.exists(openai_key_path):
        password = get_password_from_user("Enter your password to unlock the Text Model key:")
        if password:
            if not load_openai_key(openai_key_path, password):
                messagebox.showerror("Error", "Incorrect password for Text Model Key.")
    else:
        update_status("Kindly save the keys in settings.")

    
        # Debug output to verify initialization
    print(f"config.save_directory: {config.save_directory}")
    print(f"config.BASE_URL: {config.BASE_URL}")
    print(f"config.SELECTED_MODEL: {config.SELECTED_MODEL}")
    # print(f"config.GROQ_API_KEY: {config.GROQ_API_KEY}")  # Debug to check if GROQ_API_KEY is set

def save_settings():
    """Saves settings to the config file."""
    config_parser = configparser.ConfigParser()
    config_parser["DEFAULT"] = {"WorkingDirectory": config.save_directory}
    with open(get_default_config_path(), "w") as configfile:
        config_parser.write(configfile)