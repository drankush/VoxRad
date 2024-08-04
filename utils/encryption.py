import os
from base64 import urlsafe_b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import simpledialog, messagebox
from config.config import config
from ui.utils import update_status
import openai
from openai import OpenAI

password_dialog_open = False  # Global flag to track if a password dialog is open


def ensure_salt_exists(salt_filename=".myapp_salt"):
    """Ensure that a salt exists and is stored securely."""
    salt_path = os.path.join(config.save_directory, salt_filename)
    if not os.path.exists(salt_path):
        salt = os.urandom(16)  # Generate a new 16-byte salt
        with open(salt_path, "wb") as f:
            f.write(salt)
        os.chmod(salt_path, 0o400)  # Make the file read-only
    else:
        with open(salt_path, "rb") as f:
            salt = f.read()
    return salt

def get_encryption_key(password, salt_filename=".myapp_salt"):
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
    

def load_transcription_key(key_file="transcription_key.encrypted", password="default_password"):
    """Loads and decrypts the Transcription API key from the encrypted file. Returns True if decryption is successful."""
    key_path = os.path.join(config.save_directory, key_file)
    if os.path.exists(key_path):
        try:
            with open(key_path, "rb") as f:
                encrypted_key = f.read()
            key = get_encryption_key(password)
            f = Fernet(key)
            config.TRANSCRIPTION_API_KEY = f.decrypt(encrypted_key).decode()
            return True  # Decryption was successful
        except Exception as e:
            print(f"Error loading Transcription API key: {e}")
            return False  # Decryption failed
    return False  # File does not exist


def save_transcription_key(api_key, key_file="transcription_key.encrypted"):
    """Encrypts and saves the Transcription API key to a file after getting a new password."""
    key_path = os.path.join(config.save_directory, key_file)
    password = get_save_password_from_user("Set a new password for the key:")
    if not password:
        update_status("No password provided. Key not saved.")
        return False  # Return False if no password is provided

    try:
        key = get_encryption_key(password)
        f = Fernet(key)
        encrypted_key = f.encrypt(api_key.encode())
        with open(key_path, "wb") as f:
            f.write(encrypted_key)
        config.TRANSCRIPTION_API_KEY = api_key
        update_status("Transcription API key saved.")
        return True  # Return True if the key is saved successfully
    except Exception as e:
        print(f"Error saving Transcription API key: {e}")
        update_status("Error saving API key.")
        return False  # Return False if an error occurs

def delete_transcription_key():
    """Deletes the Transcription API key."""
    key_path = os.path.join(config.save_directory, "transcription_key.encrypted")
    if os.path.exists(key_path):
        try:
            os.remove(key_path)
            config.TRANSCRIPTION_API_KEY = None
            update_status("Transcription API key deleted.")
        except Exception as e:
            print(f"Error deleting Transcription API key: {e}")
            update_status("Error deleting API key.")
    else:
        update_status("API key not found.")

def load_text_key(key_file="text_key.encrypted", password="default_password"):
    """Loads and decrypts the Text API key from the encrypted file. Returns True if decryption is successful."""
    key_path = os.path.join(config.save_directory, key_file)
    if os.path.exists(key_path):
        try:
            with open(key_path, "rb") as f:
                encrypted_key = f.read()
            key = get_encryption_key(password, ".text_salt")
            f = Fernet(key)
            config.TEXT_API_KEY = f.decrypt(encrypted_key).decode()
            return True  # Decryption was successful
        except Exception as e:
            print(f"Error loading Text API key: {e}")
            return False  # Decryption failed
    return False  # File does not exist


def save_text_key(api_key, key_file="text_key.encrypted"):
    """Encrypts and saves the Text API key to a file after getting a new password."""
    key_path = os.path.join(config.save_directory, key_file)
    password = get_save_password_from_user("Set a new password for the key:")
    if not password:
        update_status("No password provided. Key not saved.")
        return False  # Return False if no password is provided

    try:
        key = get_encryption_key(password, ".text_salt")
        f = Fernet(key)
        encrypted_key = f.encrypt(api_key.encode())
        with open(key_path, "wb") as f:
            f.write(encrypted_key)
        config.TEXT_API_KEY = api_key
        update_status("Text API key saved.")
        return True  # Return True if the key is saved successfully
    except Exception as e:
        print(f"Error saving Text API key: {e}")
        update_status("Error saving API key.")
        return False  # Return False if an error occurs

def delete_text_api_key():
    """Deletes the Text API key."""
    key_path = os.path.join(config.save_directory, "text_key.encrypted")
    if os.path.exists(key_path):
        try:
            os.remove(key_path)
            config.TEXT_API_KEY = None
            update_status("Text API key deleted.")
        except Exception as e:
            print(f"Error deleting Text API key: {e}")
            update_status("Error deleting Text API key.")
    else:
        update_status("Text API key not found.")


def fetch_models(base_url, api_key, model_combobox):
    """Fetches available models and updates the model combobox."""
    try:
        text_key_path = os.path.join(config.save_directory, "text_key.encrypted")

        # Check if the text key file exists
        if os.path.exists(text_key_path):
            # Check if API key is loaded; if not, attempt to load it
            if not config.TEXT_API_KEY:
                password = get_password_from_user("Enter your password to unlock the Text key:", "text")
                if password:
                    if not load_text_key(password=password):
                        raise ValueError("Incorrect password for Text Key.")

            print("Initializing Client")
            client = openai.OpenAI(api_key=config.TEXT_API_KEY, base_url=base_url)
            print("Client initialized, fetching models")
            models = client.models.list()
            print("Models fetched")

            # Filter out models starting with certain prefixes
            excluded_prefixes = ("whisper", "dall", "sdxl")
            model_ids = [model.id for model in models.data if not any(prefix in model.id for prefix in excluded_prefixes)]
            print(f"Model IDs: {model_ids}")

            model_combobox['values'] = model_ids
            if model_ids:
                model_combobox.current(0)  # Set default selection
        else:
            messagebox.showerror("Error", "Text API key not found. Please save the key first.")

    except Exception as e:
        print(f"Failed to fetch models: {str(e)}")
        messagebox.showerror("Error", f"Failed to fetch models: {str(e)}")


def fetch_transcription_models(base_url, api_key, model_combobox):
    """Fetches available transcription models and updates the model combobox."""
    try:
        transcription_key_path = os.path.join(config.save_directory, "transcription_key.encrypted")

        # Check if the key file exists
        if os.path.exists(transcription_key_path):
            # Check if API key is loaded; if not, attempt to load it
            if not config.TRANSCRIPTION_API_KEY:
                password = get_password_from_user("Enter your password to unlock the Transcription key:", "transcription")
                if password:
                    if not load_transcription_key(password=password):
                        raise ValueError("Incorrect password for Transcription Key.")

            print("Initializing Client")
            client = openai.OpenAI(api_key=config.TRANSCRIPTION_API_KEY, base_url=base_url)
            print("Client initialized, fetching models")
            models = client.models.list()
            print("Models fetched")
            # Filter out models other than those with whisper
            included_prefix = "whisper"
            model_ids = [model.id for model in models.data if included_prefix in model.id]
            print(f"Model IDs: {model_ids}")

            model_combobox['values'] = model_ids
            if model_ids:
                model_combobox.current(0)  # Set default selection
        else:
            messagebox.showerror("Error", "Transcription API key not found. Please save the key first.")

    except Exception as e:
        print(f"Failed to fetch models: {str(e)}")
        messagebox.showerror("Error", f"Failed to fetch models: {str(e)}")



###---------------- Multimodal Support ----------------####



def save_mm_key(api_key, key_file="mm_key.encrypted"):
    """Encrypts and saves the Multimodal Model API key to a file after getting a new password."""
    key_path = os.path.join(config.save_directory, key_file)
    password = get_save_password_from_user("Set a new password for the key:")
    if not password:
        update_status("No password provided. Key not saved.")
        return False  # Return False if no password is provided

    try:
        key = get_encryption_key(password, ".mm_salt")  # Use ".mm_salt" for the salt file
        f = Fernet(key)
        encrypted_key = f.encrypt(api_key.encode())
        with open(key_path, "wb") as f:
            f.write(encrypted_key)
        config.MM_API_KEY = api_key
        update_status("Multimodal Model API key saved.")
        return True  # Return True if the key is saved successfully
    except Exception as e:
        print(f"Error saving Multimodal Model API key: {e}")
        update_status("Error saving API key.")
        return False  # Return False if an error occurs

def delete_mm_key():
    """Deletes the Multimodal Model API key."""
    key_path = os.path.join(config.save_directory, "mm_key.encrypted")
    if os.path.exists(key_path):
        try:
            os.remove(key_path)
            config.MM_API_KEY = None
            update_status("Multimodal Model API key deleted.")
        except Exception as e:
            print(f"Error deleting Multimodal Model API key: {e}")
            update_status("Error deleting API key.")
    else:
        update_status("API key not found.")

def load_mm_key(key_file="mm_key.encrypted", password="default_password"):
    """Loads and decrypts the Multimodal Model API key from the encrypted file. Returns True if decryption is successful."""
    key_path = os.path.join(config.save_directory, key_file)
    if os.path.exists(key_path):
        try:
            with open(key_path, "rb") as f:
                encrypted_key = f.read()
            key = get_encryption_key(password, ".mm_salt")  # Use ".mm_salt" for the salt file
            f = Fernet(key)
            config.MM_API_KEY = f.decrypt(encrypted_key).decode()
            return True  # Decryption was successful
        except Exception as e:
            print(f"Error loading Multimodal Model API key: {e}")
            return False  # Decryption failed
    return False  # File does not exist

