import os
import configparser
from config.config import config
from utils.encryption import get_password_from_user, load_transcription_key, load_text_key, load_mm_key
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
    config.config_path = config_path  # Save config path to config for usage elsewhere
    config_parser = configparser.ConfigParser()
    config_parser.read(config_path)

    if "DEFAULT" in config_parser:
        config.save_directory = config_parser["DEFAULT"].get("WorkingDirectory", os.path.dirname(config_path))
        config.TRANSCRIPTION_BASE_URL = config_parser["DEFAULT"].get("TranscriptionBaseURL", "http://localhost:8000/v1")
        config.SELECTED_TRANSCRIPTION_MODEL = config_parser["DEFAULT"].get("SelectedTranscriptionModel", "Systran/faster-whisper-large-v3")
        config.BASE_URL = config_parser["DEFAULT"].get("TextBaseURL", "http://localhost:11434/v1")
        config.SELECTED_MODEL = config_parser["DEFAULT"].get("SelectedModel", "llama3.1:latest")
        config.multimodal_pref = config_parser["DEFAULT"].getboolean("MultimodalPref", False)
        config.multimodal_model = config_parser["DEFAULT"].get("MultimodalModel", None)
        config.audio_device = config_parser['DEFAULT'].get('AudioDevice', config.audio_device)
        config.secure_paste_shortcut = config_parser["DEFAULT"].get("SecurePasteShortcut", "ctrl+shift+v")  
    else:
        print("Warning: 'DEFAULT' section not found in settings.ini. Using default values.")
        config.save_directory = os.path.dirname(config_path)
        config.BASE_URL = "http://localhost:11434/v1"
        config.TRANSCRIPTION_BASE_URL = "http://localhost:8000/v1"

    print(f"Using save_directory: {config.save_directory}")  # Debug output
    print(f"Using Transcription Base URL: {config.TRANSCRIPTION_BASE_URL}")
    print(f"Using Text Base URL: {config.BASE_URL}")
    print(f"Using Selected Model for Transcription: {config.SELECTED_TRANSCRIPTION_MODEL}")
    print(f"Using Selected Model: {config.SELECTED_MODEL}")
    print(f"Using Multimodal Pref: {config.multimodal_pref}")
    print(f"Using Multimodal Model: {config.multimodal_model}")
    print(f"Using Secure Paste Shortcut: {config.secure_paste_shortcut}")

    # Transcription Key Handling
    salt_path = os.path.join(os.path.dirname(config.config_path), ".asr_salt")  # Changed to .asr_salt
    transcription_key_path = os.path.join(os.path.dirname(config.config_path), "transcription_key.encrypted")
    if os.path.exists(salt_path) and os.path.exists(transcription_key_path):
        password = get_password_from_user("Enter your password to unlock the Transcription Model key:", "transcription")
        if password:
            if not load_transcription_key(transcription_key_path, password):
                messagebox.showerror("Error", "Incorrect password for Transcription Model key.")
    else:
        update_status("Kindly save the Transcription key in settings.")

    # Text Key Handling
    salt_path = os.path.join(os.path.dirname(config.config_path), ".text_salt") # Corrected line
    text_key_path = os.path.join(os.path.dirname(config.config_path), "text_key.encrypted")# Corrected line
    if os.path.exists(salt_path) and os.path.exists(text_key_path):
        password = get_password_from_user("Enter your password to unlock the Text Model key:", "text")
        if password:
            if not load_text_key(text_key_path, password):
                messagebox.showerror("Error", "Incorrect password for Text Model Key.")
    else:
        update_status("Kindly save the Text Model key in settings.")

    # MM Key Handling
    salt_path = os.path.join(os.path.dirname(config.config_path), ".mm_salt")  # Corrected line
    mm_key_path = os.path.join(os.path.dirname(config.config_path), "mm_key.encrypted")# Corrected line
    if os.path.exists(salt_path) and os.path.exists(mm_key_path):
        password = get_password_from_user("Enter your password to unlock the Multimodal Model key:", "mm")
        if password:
            if not load_mm_key(mm_key_path, password):
                messagebox.showerror("Error", "Incorrect password for Multimodal Model Key.")
    else:
        pass  # No need to show a message here


def save_settings():
    """Saves settings to the config file."""
    config_parser = configparser.ConfigParser()
    config_parser["DEFAULT"] = {
        "WorkingDirectory": config.save_directory,
        'TranscriptionBaseURL': config.TRANSCRIPTION_BASE_URL,
        'SelectedTranscriptionModel': config.SELECTED_TRANSCRIPTION_MODEL,
        "TextBaseURL": config.BASE_URL,
        "SelectedModel": config.SELECTED_MODEL,
        "MultimodalPref": config.multimodal_pref,
        "MultimodalModel": str(config.multimodal_model),  # Convert to string before saving
        "AudioDevice": config.audio_device,  # Add the audio device setting
        "SecurePasteShortcut": config.secure_paste_shortcut 
    }
    with open(get_default_config_path(), "w") as configfile:
        config_parser.write(configfile)
