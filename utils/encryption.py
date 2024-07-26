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
            return None  # User cancelled the dialog

        if is_password_correct(password, flag):
            root.destroy()
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
    if flag == "groq":
        return load_groq_key(password=password)
    else:
        return load_openai_key(password=password)

def load_groq_key(key_file="groq_key.encrypted", password="default_password"):
    """Loads and decrypts the Groq API key from the encrypted file. Returns True if decryption is successful."""
    key_path = os.path.join(config.save_directory, key_file)
    if os.path.exists(key_path):
        try:
            with open(key_path, "rb") as f:
                encrypted_key = f.read()
            key = get_encryption_key(password)
            f = Fernet(key)
            config.GROQ_API_KEY = f.decrypt(encrypted_key).decode()
            return True  # Decryption was successful
        except Exception as e:
            print(f"Error loading Groq API key: {e}")
            return False  # Decryption failed
    return False  # File does not exist

def save_groq_key(api_key, key_file="groq_key.encrypted"):
    """Encrypts and saves the Groq API key to a file after getting a new password."""
    key_path = os.path.join(config.save_directory, key_file)
    password = get_save_password_from_user("Set a new password for the key:")
    if not password:
        update_status("No password provided. Key not saved.")
        return

    try:
        key = get_encryption_key(password)
        f = Fernet(key)
        encrypted_key = f.encrypt(api_key.encode())
        with open(key_path, "wb") as f:
            f.write(encrypted_key)
        config.GROQ_API_KEY = api_key
        update_status("Groq API key saved.")
    except Exception as e:
        print(f"Error saving Groq API key: {e}")
        update_status("Error saving API key.")

def delete_groq_key():
    """Deletes the Groq API key."""
    key_path = os.path.join(config.save_directory, "groq_key.encrypted")
    if os.path.exists(key_path):
        try:
            os.remove(key_path)
            config.GROQ_API_KEY = None
            update_status("Groq API key deleted.")
        except Exception as e:
            print(f"Error deleting Groq API key: {e}")
            update_status("Error deleting API key.")
    else:
        update_status("API key not found.")

def load_openai_key(key_file="openai_key.encrypted", password="default_password"):
    """Loads and decrypts the Openai API key from the encrypted file. Returns True if decryption is successful."""
    key_path = os.path.join(config.save_directory, key_file)
    if os.path.exists(key_path):
        try:
            with open(key_path, "rb") as f:
                encrypted_key = f.read()
            key = get_encryption_key(password, ".openai_salt")
            f = Fernet(key)
            config.OPENAI_API_KEY = f.decrypt(encrypted_key).decode()
            return True  # Decryption was successful
        except Exception as e:
            print(f"Error loading Openai API key: {e}")
            return False  # Decryption failed
    return False  # File does not exist

def save_openai_key(api_key, key_file="openai_key.encrypted"):
    """Encrypts and saves the Openai API key to a file after getting a new password."""
    key_path = os.path.join(config.save_directory, key_file)
    password = get_save_password_from_user("Set a new password for the key:")
    if not password:
        update_status("No password provided. Key not saved.")
        return

    try:
        key = get_encryption_key(password, ".openai_salt")
        f = Fernet(key)
        encrypted_key = f.encrypt(api_key.encode())
        with open(key_path, "wb") as f:
            f.write(encrypted_key)
        config.OPENAI_API_KEY = api_key
        update_status("Openai API key saved.")
    except Exception as e:
        print(f"Error saving Openai API key: {e}")
        update_status("Error saving API key.")

def delete_openai_api_key():
    """Deletes the OpenAI API key."""
    key_path = os.path.join(config.save_directory, "openai_key.encrypted")
    if os.path.exists(key_path):
        try:
            os.remove(key_path)
            config.OPENAI_API_KEY = None
            update_status("OpenAI API key deleted.")
        except Exception as e:
            print(f"Error deleting OpenAI API key: {e}")
            update_status("Error deleting OpenAI API key.")
    else:
        update_status("OpenAI API key not found.")

def fetch_models(base_url, api_key, model_combobox):
    """Fetches available models from OpenAI and updates the model combobox."""
    try:
        # Check if API key is loaded; if not, attempt to load it
        if not config.OPENAI_API_KEY:
            password = get_password_from_user("Enter your password to unlock the OpenAI key:", "openai")
            if password:
                if not load_openai_key(password=password):
                    raise ValueError("Incorrect password for OpenAI Key.")
        
        print("Initializing OpenAI client")
        client = openai.OpenAI(api_key=config.OPENAI_API_KEY, base_url=base_url)
        print("Client initialized, fetching models")
        models = client.models.list()
        print("Models fetched")

        # Filter out models starting with certain prefixes
        excluded_prefixes = ("whisper", "dall", "sdxl")
        model_ids = [model.id for model in models.data if not model.id.startswith(excluded_prefixes)]
        print(f"Model IDs: {model_ids}")

        model_combobox['values'] = model_ids
        if model_ids:
            model_combobox.current(0)  # Set default selection
    except Exception as e:
        print(f"Failed to fetch models: {str(e)}")
        messagebox.showerror("Error", f"Failed to fetch models: {str(e)}")
