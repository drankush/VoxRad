import pyautogui
import subprocess
from cryptography.fernet import Fernet
from config.config import config
from ui.utils import update_status
from pynput import keyboard
from pynput.keyboard import Controller
import time
import os

# Global variables
pressed_keys = set()
shortcut_active = False
last_execution_time = 0
DEBOUNCE_DELAY = 0.3  # Prevent repeated triggers within 300ms


# Global keyboard controller
keyboard_controller = Controller()

def check_secure_paste_shortcut():
    """Checks if the currently pressed keys match the secure paste shortcut."""
    required_keys = config.secure_paste_shortcut.lower().split('+')
    return all(req in pressed_keys for req in required_keys)


def thread_safe_update_status(message):
    """Update status in a thread-safe manner."""
    config.root.after(0, update_status, message)


def initialize_secure_paste():
    """Starts the hotkey listener."""
    listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    listener.start()
    print("Secure paste initialized")


def on_key_press(key):
    """Handles key press events."""
    global shortcut_active, last_execution_time

    try:
        # Add pressed key to the set
        key_name = key.char if hasattr(key, 'char') else key.name
        pressed_keys.add(key_name)
        print(f"Pressed: {pressed_keys}")

        # Check if shortcut is pressed and debounce
        if check_secure_paste_shortcut() and not shortcut_active:
            current_time = time.time()
            if current_time - last_execution_time > DEBOUNCE_DELAY:
                secure_paste_report()
                shortcut_active = True
                last_execution_time = current_time

    except Exception as e:
        print(f"Error in on_key_press: {e}")


def on_key_release(key):
    """Handles key release events."""
    global shortcut_active

    try:
        # Remove released key from the set
        key_name = key.char if hasattr(key, 'char') else key.name
        pressed_keys.discard(key_name)
        print(f"Released: {pressed_keys}")

        # Reset shortcut_active when all keys are released
        if not pressed_keys:
            shortcut_active = False

    except Exception as e:
        print(f"Error in on_key_release: {e}")

def secure_paste_report():
    """Securely pastes the generated report."""
    print("Secure paste report started")
    try:
        # Decrypt report
        if config.current_encrypted_report and config.current_report_encryption_key:
            cipher_suite = Fernet(config.current_report_encryption_key.encode())
            decrypted_report = cipher_suite.decrypt(config.current_encrypted_report.encode()).decode()

            # Inject text based on OS
            if os.name == "nt":  # Windows
                inject_text_windows(decrypted_report)
            else:  # macOS (or other systems)
                inject_text_with_applescript(decrypted_report)

            thread_safe_update_status("Report securely pasted.")
        else:
            thread_safe_update_status("No report available for secure paste.")
    except Exception as e:
        thread_safe_update_status(f"Error during secure paste: {e}")


def inject_text_with_applescript(text):
    """Injects multiline text directly into the active window using AppleScript."""
    applescript_lines = []
    for line in text.splitlines():
        escaped_line = line.replace('"', '\\"')
        applescript_lines.append(f'keystroke "{escaped_line}"')
        applescript_lines.append('key code 36')  # Key code 36 is the Return key

    applescript = '''
    tell application "System Events"
        {}
    end tell
    '''.format('\n        '.join(applescript_lines))

    subprocess.run(["osascript", "-e", applescript], check=True)


def inject_text_windows(text):
    """Injects text directly into the active window on Windows."""
    # Break text into lines for better control
    for line in text.splitlines():
        pyautogui.typewrite(line)
        pyautogui.press("enter")  # Simulate pressing Enter after each line
