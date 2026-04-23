import os
import logging
from base64 import urlsafe_b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import simpledialog, messagebox
from config.config import config
from config.logging_config import get_logger
from ui.utils import update_status
import openai
from openai import OpenAI

logger = get_logger(__name__)
password_dialog_open = False  # Global flag to track if a password dialog is open


def ensure_salt_exists(salt_filename=".asr_salt"):
    """Ensure that a salt exists and is stored securely."""
    salt_path = os.path.join(os.path.dirname(config.config_path), salt_filename)  # Corrected line
    if not os.path.exists(salt_path):
        salt = os.urandom(16)  # Generate a new 16-byte salt
        with open(salt_path, "wb") as f:
            f.write(salt)
        os.chmod(salt_path, 0o400)  # Make the file read-only
    else:
        with open(salt_path, "rb") as f:
            salt = f.read()
    return salt

def get_encryption_key(password, salt_filename=".asr_salt"):
    """Generate a deterministic encryption key based on the provided password and salt."""
    salt = ensure_salt_exists(salt_filename)
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    key = urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def get_password_from_user(prompt, flag):
    """Prompt the user to enter their password securely with error handling for incorrect entries."""
    global password_dialog_open
    if password_dialog_open:
        messagebox.showerror("Error", "Another password dialog is already open.")
        return None

    password_dialog_open = True  # Set the flag to True

    class PasswordDialog(simpledialog.Dialog):
        def body(self, master):
            tk.Label(master, text=prompt).grid(row=0)
            self.password_entry = tk.Entry(master, show='*', width=25)
            self.password_entry.grid(row=1, padx=5, pady=5)
            return self.password_entry  # initial focus on the password entry

        def apply(self):
            self.result = self.password_entry.get()  # get the password from the entry widget

    root = tk.Tk()
    root.withdraw()  # Hide the main window

    while True:
        dialog = PasswordDialog(root, "Password")
        password = dialog.result
        if password is None:
            root.destroy()
            password_dialog_open = False  # Reset the flag if the dialog is canceled
            return None  # User cancelled the dialog

        if is_password_correct(password, flag):
            root.destroy()
            password_dialog_open = False  # Reset the flag after successful validation
            return password  # Correct password entered

        messagebox.showerror("Error", "Incorrect password, please try again.")
        # The loop will continue, prompting the user again


def get_save_password_from_user(prompt):
    """Prompt the user to enter their password securely."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    password = simpledialog.askstring("Password", prompt, show='*')
    root.destroy()
    return password

def is_password_correct(password, flag):
    """Function to check if the provided password is correct by attempting to decrypt the encrypted key file."""
    if flag == "transcription":
        return load_transcription_key(password=password)
    elif flag == "text":
        return load_text_key(password=password)
    elif flag == "mm":
        return load_mm_key(password=password)
    else:
        return False  # Invalid flag


def _load_generic_key(key_type, key_file, salt_file, config_attr, password="default_password"):
    """Generic function to load and decrypt any API key. Returns True if decryption is successful."""
    key_path = os.path.join(os.path.dirname(config.config_path), key_file)
    if os.path.exists(key_path):
        try:
            with open(key_path, "rb") as f:
                encrypted_key = f.read()
            key = get_encryption_key(password, salt_file)
            cipher = Fernet(key)
            decrypted_key = cipher.decrypt(encrypted_key).decode()
            setattr(config, config_attr, decrypted_key)
            logger.info(f"Successfully loaded {key_type} key")
            return True
        except Exception as e:
            logger.error(f"Error loading {key_type} key: {e}")
            return False
    logger.warning(f"{key_type} key file not found")
    return False


def _save_generic_key(key_type, api_key, key_file, salt_file, config_attr, status_message):
    """Generic function to encrypt and save any API key."""
    key_path = os.path.join(os.path.dirname(config.config_path), key_file)
    password = get_save_password_from_user("Set a new password for the key:")
    if not password:
        update_status("No password provided. Key not saved.")
        return False

    try:
        key = get_encryption_key(password, salt_file)
        cipher = Fernet(key)
        encrypted_key = cipher.encrypt(api_key.encode())
        with open(key_path, "wb") as f:
            f.write(encrypted_key)
        setattr(config, config_attr, api_key)
        logger.info(f"Successfully saved {key_type} key")
        update_status(status_message)
        return True
    except Exception as e:
        logger.error(f"Error saving {key_type} key: {e}")
        update_status("Error saving API key.")
        return False


def _delete_generic_key(key_type, key_file, config_attr, status_message):
    """Generic function to delete any API key file."""
    key_path = os.path.join(os.path.dirname(config.config_path), key_file)
    if os.path.exists(key_path):
        try:
            os.remove(key_path)
            setattr(config, config_attr, None)
            logger.info(f"Successfully deleted {key_type} key")
            update_status(status_message)
        except Exception as e:
            logger.error(f"Error deleting {key_type} key: {e}")
            update_status(f"Error deleting {key_type} key.")
    else:
        logger.warning(f"{key_type} key file not found")
        update_status(f"{key_type} key not found.")


def load_transcription_key(key_file="transcription_key.encrypted", password="default_password"):
    """Loads and decrypts the Transcription API key from the encrypted file. Returns True if decryption is successful."""
    return _load_generic_key("Transcription", key_file, ".asr_salt", "TRANSCRIPTION_API_KEY", password)


def save_transcription_key(api_key, key_file="transcription_key.encrypted"):
    """Encrypts and saves the Transcription API key to a file after getting a new password."""
    return _save_generic_key("Transcription", api_key, key_file, ".asr_salt", "TRANSCRIPTION_API_KEY", "Transcription API key saved.")

def delete_transcription_key():
    """Deletes the Transcription API key."""
    _delete_generic_key("Transcription", "transcription_key.encrypted", "TRANSCRIPTION_API_KEY", "Transcription API key deleted.")

def load_text_key(key_file="text_key.encrypted", password="default_password"):
    """Loads and decrypts the Text API key from the encrypted file. Returns True if decryption is successful."""
    return _load_generic_key("Text", key_file, ".text_salt", "TEXT_API_KEY", password)


def save_text_key(api_key, key_file="text_key.encrypted"):
    """Encrypts and saves the Text API key to a file after getting a new password."""
    return _save_generic_key("Text", api_key, key_file, ".text_salt", "TEXT_API_KEY", "Text API key saved.")

def delete_text_api_key():
    """Deletes the Text API key."""
    _delete_generic_key("Text", "text_key.encrypted", "TEXT_API_KEY", "Text API key deleted.")


def fetch_models(base_url, api_key, model_combobox):
    """Fetches available models and updates the model combobox."""
    try:
        text_key_path = os.path.join(os.path.dirname(config.config_path), "text_key.encrypted")# Corrected line

        # Check if the text key file exists
        if os.path.exists(text_key_path):
            # Check if API key is loaded; if not, attempt to load it
            if not config.TEXT_API_KEY:
                password = get_password_from_user("Enter your password to unlock the Text key:", "text")
                if password:
                    if not load_text_key(password=password):
                        raise ValueError("Incorrect password for Text Key.")

            logger.debug("Initializing OpenAI client")
            client = openai.OpenAI(api_key=config.TEXT_API_KEY, base_url=base_url)
            logger.debug("Client initialized, fetching models")
            models = client.models.list()
            logger.debug("Models fetched successfully")

            # Filter out models starting with certain prefixes
            excluded_prefixes = ("whisper", "dall", "sdxl")
            model_ids = [model.id for model in models.data if not any(prefix in model.id for prefix in excluded_prefixes)]
            logger.debug(f"Available models: {model_ids}")

            model_combobox['values'] = model_ids
            if model_ids:
                model_combobox.current(0)  # Set default selection
        else:
            messagebox.showerror("Error", "Text API key not found. Please save the key first.")

    except Exception as e:
        logger.error(f"Failed to fetch models: {str(e)}")
        messagebox.showerror("Error", f"Failed to fetch models: {str(e)}")


def fetch_transcription_models(base_url, api_key, model_combobox):
    """Fetches available transcription models and updates the model combobox."""
    try:
        transcription_key_path = os.path.join(os.path.dirname(config.config_path), "transcription_key.encrypted") # Corrected line

        # Check if the key file exists
        if os.path.exists(transcription_key_path):
            # Check if API key is loaded; if not, attempt to load it
            if not config.TRANSCRIPTION_API_KEY:
                password = get_password_from_user("Enter your password to unlock the Transcription key:", "transcription")
                if password:
                    if not load_transcription_key(password=password):
                        raise ValueError("Incorrect password for Transcription Key.")

            logger.debug("Initializing OpenAI client")
            client = openai.OpenAI(api_key=config.TRANSCRIPTION_API_KEY, base_url=base_url)
            logger.debug("Client initialized, fetching models")
            models = client.models.list()
            logger.debug("Models fetched successfully")
            # Filter out models other than those with whisper
            included_prefix = "whisper"
            model_ids = [model.id for model in models.data if included_prefix in model.id]
            logger.debug(f"Available models: {model_ids}")

            model_combobox['values'] = model_ids
            if model_ids:
                model_combobox.current(0)  # Set default selection
        else:
            messagebox.showerror("Error", "Transcription API key not found. Please save the key first.")

    except Exception as e:
        logger.error(f"Failed to fetch models: {str(e)}")
        messagebox.showerror("Error", f"Failed to fetch models: {str(e)}")



###---------------- Multimodal Support ----------------####



def save_mm_key(api_key, key_file="mm_key.encrypted"):
    """Encrypts and saves the Multimodal Model API key to a file after getting a new password."""
    return _save_generic_key("Multimodal", api_key, key_file, ".mm_salt", "MM_API_KEY", "Multimodal Model API key saved.")

def delete_mm_key():
    """Deletes the Multimodal Model API key."""
    _delete_generic_key("Multimodal", "mm_key.encrypted", "MM_API_KEY", "Multimodal Model API key deleted.")

def load_mm_key(key_file="mm_key.encrypted", password="default_password"):
    """Loads and decrypts the Multimodal Model API key from the encrypted file. Returns True if decryption is successful."""
    return _load_generic_key("Multimodal", key_file, ".mm_salt", "MM_API_KEY", password)
