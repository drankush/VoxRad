import os
import configparser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import webbrowser
import sounddevice as sd
from ui.utils import update_status
from config.config import config
from utils.file_handling import move_files, load_templates, load_guidelines
from utils.encryption import save_transcription_key, save_text_key, delete_transcription_key, delete_text_api_key, fetch_models, fetch_transcription_models, get_password_from_user, load_transcription_key, load_text_key
from utils.encryption import save_mm_key, delete_mm_key, load_mm_key
from config.settings import save_settings, get_default_config_path
import shutil
from utils.file_handling import resource_path

def get_config_dir():
    """Helper function to get ONLY the config directory, without settings.ini"""
    if os.name == "nt":  # Windows
        config_dir = os.path.join(os.environ["APPDATA"], "VOXRAD")
    else:  # Assuming macOS or Linux
        config_dir = os.path.join(os.path.expanduser("~"), ".voxrad")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return config_dir

def open_settings():
    """Opens the settings dialog box with additional fields for settings."""
    if config.settings_window is None:
        """Opens the settings dialog box with additional fields for settings."""
        config.settings_window = tk.Toplevel()
        config.settings_window.title("Settings")


        # Create Tab Control
        tab_control = ttk.Notebook(config.settings_window)
        tab_control.pack(expand=1, fill="both")


        # --- Tab 1: General ---
        general_tab = ttk.Frame(tab_control)
        tab_control.add(general_tab, text="🛠 General")


        dir_label = tk.Label(general_tab, text="Working Directory:")
        dir_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        dir_var = tk.StringVar(general_tab, value=config.save_directory)
        dir_entry = tk.Entry(general_tab, textvariable=dir_var, width=30)
        dir_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")


        def browse_directory():
            print(config.template_dropdown)
            directory = filedialog.askdirectory()
            if directory:
                old_directory = config.save_directory
                config.save_directory = directory
                dir_var.set(directory)
                save_settings()  # Save settings
                if old_directory:
                    move_files(old_directory, config.save_directory)
                load_templates()  # Reload templates
                load_guidelines() # Reload guidelines


        # browse_button = tk.Button(general_tab, text="Browse", command=browse_directory)
        browse_button = tk.Button(general_tab, text="Browse", command=lambda: browse_directory(), width=12)
        browse_button.grid(row=0, column=2, padx=5, pady=5)


        def open_working_directory():
            """Opens the working directory in the file explorer."""
            # templates_path = os.path.join(config.save_directory, "templates")
            working_directory = config.save_directory


            # Template files to copy
            template_files_to_copy = ["HRCT_Thorax.txt", "CECT_Abdomen.txt", "CT_Head.txt"]
            templates_path = os.path.join(working_directory, "templates")
            if not os.path.exists(templates_path):
                os.makedirs(templates_path)
            
            # Copy specified template files from resource path to the templates directory
            for template_file in template_files_to_copy:
                source_file = resource_path(os.path.join("templates", template_file))
                destination_file = os.path.join(templates_path, template_file)
                if os.path.exists(source_file) and not os.path.exists(destination_file):
                    shutil.copy2(source_file, destination_file)
                    print(f"Copied {template_file} to {destination_file}")


            # Guideline files to copy
            guideline_files_to_copy = ["BIRADS_MAMMOGRAPHY.md", "BIRADS_USG.md", "Fleischner_Society_2017_guidelines.md", "LIRADS_(Liver).md", "PIRADS.md", "TIRADS.md"]
            guidelines_path = os.path.join(working_directory, "guidelines")
            if not os.path.exists(guidelines_path):
                os.makedirs(guidelines_path)


            # Copy specified guideline files from resource path to the guidelines directory
            for guideline_file in guideline_files_to_copy:
                source_file = resource_path(os.path.join("guidelines", guideline_file))
                destination_file = os.path.join(guidelines_path, guideline_file)
                if os.path.exists(source_file) and not os.path.exists(destination_file):
                    shutil.copy2(source_file, destination_file)
                    print(f"Copied {guideline_file} to {destination_file}")


            if os.name == 'nt':
                os.startfile(working_directory)
            elif os.name == 'posix':
                subprocess.run(['open', working_directory])
            else:
                print(f"Unsupported operating system: {os.name}")


        open_templates_button = tk.Button(general_tab, text="Open", command=open_working_directory, width=12)
        open_templates_button.grid(row=0, column=3, padx=5, pady=5, sticky="w")


        audio_device_label = tk.Label(general_tab, text="Audio Input Device:")
        audio_device_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")


        audio_device_var = tk.StringVar(general_tab, value=config.audio_device)  # Initialize with the current setting
        audio_device_dropdown = ttk.Combobox(general_tab, textvariable=audio_device_var, state="readonly", width=25)
        audio_device_dropdown['values'] = [device['name'] for device in sd.query_devices() if device['max_input_channels'] > 0]
        audio_device_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")


        # Secure Paste Shortcut
        secure_paste_label = tk.Label(general_tab, text="Secure Paste Shortcut:")
        secure_paste_label.grid(row=3, column=0, padx=5, pady=5,  sticky="w")
        secure_paste_var = tk.StringVar(general_tab, value=config.secure_paste_shortcut)
        secure_paste_entry = tk.Entry(general_tab, textvariable=secure_paste_var, width=30)
        secure_paste_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")


        # Create the "💡" button
        def open_input_help_url():
            webbrowser.open_new("https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key")


        docs_button = tk.Button(general_tab, text="💡", command=open_input_help_url, width=1, height=1, font=("Arial", 12))
        docs_button.grid(row=3, column=2, padx=5, pady=(0, 0), sticky="w")  # Position above the save button

        def save_general_settings():
            config_parser = configparser.ConfigParser()
            config_parser.read(get_default_config_path())
            if 'DEFAULT' not in config_parser:
                config_parser['DEFAULT'] = {}
            config_parser['DEFAULT']['WorkingDirectory'] = str(dir_var.get())  # Convert to string
            config_parser['DEFAULT']['AudioDevice'] = str(audio_device_var.get())  # Convert to string
            config_parser['DEFAULT']['SecurePasteShortcut'] = str(secure_paste_var.get())  # Convert to string
            with open(get_default_config_path(), 'w') as configfile:
                config_parser.write(configfile)
            config.save_directory = dir_var.get()
            config.audio_device = audio_device_var.get()
            config.secure_paste_shortcut = secure_paste_var.get()
            update_status("General settings saved.")

        save_general_button = tk.Button(general_tab, text="Save Settings", command=save_general_settings, width=12)
        save_general_button.grid(row=4, column=1, padx=5, pady=5, sticky="w")



        # --- Tab 2: Transcription Model ---
        transcription_tab = ttk.Frame(tab_control)
        tab_control.add(transcription_tab, text="🎤 Transcription Model")

        # BaseURL Settings
        transcription_base_url_label = tk.Label(transcription_tab, text="Base URL:")
        transcription_base_url_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        transcription_base_url_var = tk.StringVar(transcription_tab, value=config.TRANSCRIPTION_BASE_URL)
        transcription_base_url_entry = tk.Entry(transcription_tab, textvariable=transcription_base_url_var, width=30)
        transcription_base_url_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="w")

        # Transcription API Key Setting
        transcription_key_label = tk.Label(transcription_tab, text="API Key:")
        transcription_key_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        transcription_key_var = tk.StringVar(transcription_tab)
        transcription_key_entry = tk.Entry(transcription_tab, textvariable=transcription_key_var, show="*", width=30)
        transcription_key_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        # Initialize button states and entry field
        # Corrected path: Use get_config_dir()
        transcription_key_path = os.path.join(get_config_dir(), "transcription_key.encrypted")
        print(f"[DEBUG] Transcription key path: {transcription_key_path}")  # Debug: Print the path
        transcription_key_file_exists = os.path.exists(transcription_key_path)

        # Initialize in one place, then set based on conditions
        save_delete_button = tk.Button(transcription_tab, width=12)
        lock_unlock_button = tk.Button(transcription_tab, width=12)

        def update_transcription_ui():
            nonlocal transcription_key_file_exists
            transcription_key_file_exists = os.path.exists(transcription_key_path)
            print(f"[DEBUG] Transcription key file exists: {transcription_key_file_exists}")

            if transcription_key_file_exists:
                transcription_key_entry.config(state="readonly")
                transcription_key_var.set("**********************************")
                save_delete_button.config(text="Delete Key")
                print(f"[DEBUG] Encrypted file exists - Setting entry to readonly, dummy input, and button to 'Delete Key'")
                if config.TRANSCRIPTION_API_KEY:
                    lock_unlock_button.config(text="🔒 Lock Key", state="normal")
                    print(f"[DEBUG] API key loaded - Setting Lock/Unlock button to 'Lock Key' and enabled")
                else:
                    lock_unlock_button.config(text="🔓 Unlock Key", state="normal")
                    print(f"[DEBUG] API key NOT loaded - Setting Lock/Unlock button to 'Unlock Key' and enabled")
            else:
                transcription_key_entry.config(state="normal")
                transcription_key_var.set("")
                save_delete_button.config(text="Save Key")
                lock_unlock_button.config(text="🔓 Unlock Key", state="disabled")
                print(f"[DEBUG] No encrypted file - Setting entry to normal and empty, Save/Delete button to 'Save Key', Lock/Unlock to disabled")

            #Ensures no change to the button state, if the key is deleted but not cleared from config.TRANSCRIPTION_API_KEY.
            if config.TRANSCRIPTION_API_KEY is None and transcription_key_file_exists:
                 lock_unlock_button.config(state="normal")
                 print(f"[DEBUG] API key is None and file exists - Lock/Unlock button state set to normal")

        def save_transcription_key_ui():
            if transcription_key_var.get().strip() == "":
                update_status("API key cannot be empty.")
                messagebox.showerror("Error", "API key cannot be empty.")
                return False

            if save_transcription_key(transcription_key_var.get()):
                print(f"[DEBUG] Transcription key saved successfully")
                update_transcription_ui()
                return True
            print(f"[DEBUG] Transcription key save failed")
            return False

        def delete_transcription_key_ui():
            delete_transcription_key()
            config.TRANSCRIPTION_API_KEY = None  # Clear the key on delete
            print(f"[DEBUG] Transcription key deleted and config.TRANSCRIPTION_API_KEY set to None")
            update_transcription_ui()


        def toggle_save_delete_key():
            if save_delete_button.cget("text") == "Save Key":
                print(f"[DEBUG] Save/Delete button clicked: Save Key")
                save_transcription_key_ui()
            else:
                print(f"[DEBUG] Save/Delete button clicked: Delete Key")
                delete_transcription_key_ui()

        save_delete_button.config(command=toggle_save_delete_key)
        save_delete_button.grid(row=2, column=2, padx=5, pady=5)

        def toggle_lock_unlock_transcription_key():
            if config.TRANSCRIPTION_API_KEY is None:
                print(f"[DEBUG] Lock/Unlock button clicked: Unlock Key")
                password = get_password_from_user("Enter your password to unlock the Transcription Model key:", "transcription")
                if password:
                    if load_transcription_key(password=password):
                        lock_unlock_button.config(text="🔒 Lock Key")  # Update button text
                        update_status("Transcription Model key unlocked.")
                        print(f"[DEBUG] Transcription key unlocked - Setting Lock/Unlock to 'Lock Key'")
                    else:
                        update_status("Incorrect password for Transcription Model key.")
                        messagebox.showerror("Error", "Incorrect password for Transcription Model key.")
                        print(f"[DEBUG] Incorrect password for transcription key")
            else:
                print(f"[DEBUG] Lock/Unlock button clicked: Lock Key")
                config.TRANSCRIPTION_API_KEY = None
                lock_unlock_button.config(text="🔓 Unlock Key")  # Update button text
                update_status("Transcription Model key locked.")
                print(f"[DEBUG] Transcription key locked - Setting Lock/Unlock to 'Unlock Key'")

        lock_unlock_button.config(command=toggle_lock_unlock_transcription_key)
        lock_unlock_button.grid(row=2, column=3, padx=5, pady=5)

        print(f"[DEBUG] Initial state - Encrypted file exists: {transcription_key_file_exists}, API key loaded: {config.TRANSCRIPTION_API_KEY is not None}")
        update_transcription_ui()  # Call once to initialize UI



        transcription_fetch_models_button = tk.Button(transcription_tab, text="Fetch Models",
                                        command=lambda: fetch_transcription_models(transcription_base_url_var.get(), transcription_key_var.get(), transcription_model_combobox), width=12)
        # transcription_fetch_models_button.grid(row=3, column=2, padx=5, pady=5, columnspan=2)
        transcription_fetch_models_button.grid(row=3, column=2, padx=5, pady=5)


        transcription_model_label = tk.Label(transcription_tab, text="Select Model:")
        transcription_model_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        transcription_model_combobox = ttk.Combobox(transcription_tab, width=25, state="readonly")
        transcription_model_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        def open_url(url):
            webbrowser.open_new(url)

        # Create the "💡" button
        def open_docs_url():
            webbrowser.open_new("https://voxrad.gitbook.io/voxrad/fundamentals/getting-set-up/managing-keys")

        docs_button = tk.Button(transcription_tab, text="💡", command=open_docs_url, width=1, height=1, font=("Arial", 12))
        docs_button.grid(row=1, column=2, padx=5, pady=(0, 0), sticky="w")  # Position above the save button

        def save_all_transcription_settings():
            """Saves all transcription settings to the config file."""
            config_parser = configparser.ConfigParser()
            config_parser.read(get_default_config_path())  # Read existing settings

            # Append new settings to existing settings
            config_parser['DEFAULT'].update({
                'WorkingDirectory': dir_var.get(),
                'TranscriptionBaseURL': transcription_base_url_var.get(),
                'SelectedTranscriptionModel': transcription_model_combobox.get()
            })

            with open(get_default_config_path(), 'w') as configfile:
                config_parser.write(configfile)  # Write updated settings
            config.save_directory = dir_var.get()
            config.TRANSCRIPTION_BASE_URL = transcription_base_url_var.get()
            config.SELECTED_TRANSCRIPTION_MODEL = transcription_model_combobox.get()
            update_status("Settings saved.")


        save_transcription_settings_button = tk.Button(transcription_tab, text="Save Settings", command=save_all_transcription_settings, width=12)
        save_transcription_settings_button.grid(row=4, column=3, padx=5, pady=(160,0))






        # --- Tab 3: Text Model ---
        text_model_tab = ttk.Frame(tab_control)
        tab_control.add(text_model_tab, text="📝 Text Model")

        # Text Settings
        base_url_label = tk.Label(text_model_tab, text="Base URL:")
        base_url_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        base_url_var = tk.StringVar(text_model_tab, value=config.BASE_URL)
        base_url_entry = tk.Entry(text_model_tab, textvariable=base_url_var, width=30)
        base_url_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="w")

        api_key_label = tk.Label(text_model_tab, text="API Key:")
        api_key_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        api_key_var = tk.StringVar(text_model_tab)
        api_key_entry = tk.Entry(text_model_tab, textvariable=api_key_var, show="*", width=30)
        api_key_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")


        # Initialize button states
        # Corrected path: Use get_config_dir()
        text_key_path = os.path.join(get_config_dir(), "text_key.encrypted")
        print(f"[DEBUG] Text key path: {text_key_path}")  # Debug
        text_key_file_exists = os.path.exists(text_key_path)


        # Initialize in one place, and set the attributes
        save_delete_text_button = tk.Button(text_model_tab, width=12)
        lock_unlock_text_button = tk.Button(text_model_tab, width=12)


        def update_text_ui():
            nonlocal text_key_file_exists
            text_key_file_exists = os.path.exists(text_key_path)
            print(f"[DEBUG] Text key file exists: {text_key_file_exists}")

            if text_key_file_exists:
                api_key_entry.config(state="readonly")
                api_key_var.set("**********************************")
                save_delete_text_button.config(text="Delete Key")
                print(f"[DEBUG] Encrypted file exists - Setting entry to readonly, dummy input, and button to 'Delete Key'")
                if config.TEXT_API_KEY:
                    lock_unlock_text_button.config(text="🔒 Lock Key", state="normal")
                    print(f"[DEBUG] API key loaded - Setting Lock/Unlock button to 'Lock Key' and enabled")
                else:
                    lock_unlock_text_button.config(text="🔓 Unlock Key", state="normal")
                    print(f"[DEBUG] API key NOT loaded - Setting Lock/Unlock button to 'Unlock Key' and enabled")
            else:
                api_key_entry.config(state="normal")
                api_key_var.set("")
                save_delete_text_button.config(text="Save Key")
                lock_unlock_text_button.config(text="🔓 Unlock Key", state="disabled")
                print(f"[DEBUG] No encrypted file - Setting entry to normal and empty, Save/Delete button to 'Save Key', Lock/Unlock to disabled")

            #Ensures no change to the button state, if the key is deleted but not cleared from config.TEXT_API_KEY.
            if config.TEXT_API_KEY is None and text_key_file_exists:
                lock_unlock_text_button.config(state="normal")
                print(f"[DEBUG] API key is None and file exists - Lock/Unlock button state set to normal")


        def save_text_key_ui():
            if api_key_var.get().strip() == "":
                update_status("API key cannot be empty.")
                messagebox.showerror("Error", "API key cannot be empty.")
                return False  # Indicate failure

            if save_text_key(api_key_var.get()):
                print(f"[DEBUG] Text key saved successfully")
                update_text_ui()
                return True  # Indicate success
            print(f"[DEBUG] Text key save failed")
            return False

        def delete_text_key_ui():
            delete_text_api_key()
            config.TEXT_API_KEY = None  # Clear the key on delete.
            print(f"[DEBUG] Text key deleted and config.TEXT_API_KEY set to None")
            update_text_ui()

        def toggle_save_delete_text_key():
            if save_delete_text_button.cget("text") == "Save Key":
                print(f"[DEBUG] Save/Delete button clicked: Save Key")
                save_text_key_ui()
            else:
                print(f"[DEBUG] Save/Delete button clicked: Delete Key")
                delete_text_key_ui()

        #Create the button
        save_delete_text_button.config(command=toggle_save_delete_text_key)
        save_delete_text_button.grid(row=2, column=2, padx=5, pady=5)

        def toggle_lock_unlock_text_key():
            if config.TEXT_API_KEY is None:
                print(f"[DEBUG] Lock/Unlock button clicked: Unlock Key")
                password = get_password_from_user("Enter your password to unlock the Text Model key:", "text")
                if password:
                    if load_text_key(password=password):
                        lock_unlock_text_button.config(text="🔒 Lock Key")
                        update_status("Text Model key unlocked.")
                        print(f"[DEBUG] Text key unlocked - Setting Lock/Unlock to 'Lock Key'")
                    else:
                        update_status("Incorrect password for Text Model key.")
                        messagebox.showerror("Error", "Incorrect password for Text Model key.")
                        print(f"[DEBUG] Incorrect password for text key")
            else:
                print(f"[DEBUG] Lock/Unlock button clicked: Lock Key")
                config.TEXT_API_KEY = None
                lock_unlock_text_button.config(text="🔓 Unlock Key")
                update_status("Text Model key locked.")
                print(f"[DEBUG] Text key locked - Setting Lock/Unlock to 'Unlock Key'")


        lock_unlock_text_button.config(command=toggle_lock_unlock_text_key)
        lock_unlock_text_button.grid(row=2, column=3, padx=5, pady=5)

        print(f"[DEBUG] Initial state - Encrypted file exists: {text_key_file_exists}, API key loaded: {config.TEXT_API_KEY is not None}")
        update_text_ui() # Call once to initialize UI


        fetch_models_button = tk.Button(text_model_tab, text="Fetch Models",
                                        command=lambda: fetch_models(base_url_var.get(), api_key_var.get(), model_combobox), width=12)
        # fetch_models_button.grid(row=3, column=2, padx=5, pady=5, columnspan=2)
        fetch_models_button.grid(row=3, column=2, padx=5, pady=5)

        model_label = tk.Label(text_model_tab, text="Select Model:")
        model_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        model_combobox = ttk.Combobox(text_model_tab, width=25, state="readonly")
        model_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        def open_url(url):
            webbrowser.open_new(url)

            
        # Create the "💡" button
        def open_docs_url():
            webbrowser.open_new("https://voxrad.gitbook.io/voxrad/fundamentals/getting-set-up/managing-keys")

        docs_button = tk.Button(text_model_tab, text="💡", command=open_docs_url, width=1, height=1, font=("Arial", 12))
        docs_button.grid(row=1, column=2, padx=5, pady=(0, 0), sticky="w")  # Position above the save button


        def save_all_settings():
            """Saves all settings to the config file."""
            config_parser = configparser.ConfigParser()
            config_parser.read(get_default_config_path())  # Read existing settings

            # Append new settings to existing settings
            config_parser['DEFAULT'].update({
                'WorkingDirectory': dir_var.get(),
                'TextBaseURL': base_url_var.get(),
                'SelectedModel': model_combobox.get()
            })

            with open(get_default_config_path(), 'w') as configfile:
                config_parser.write(configfile)  # Write updated settings
            config.save_directory = dir_var.get()
            config.BASE_URL = base_url_var.get()
            config.SELECTED_MODEL = model_combobox.get()
            update_status("Settings saved.")



        save_settings_button = tk.Button(text_model_tab, text="Save Settings", command=save_all_settings, width=12)
        save_settings_button.grid(row=4, column=3, padx=5, pady=(160,0))


        # --- Tab 4: Multimodal Model ---
        multimodal_tab = ttk.Frame(tab_control)
        tab_control.add(multimodal_tab, text="🤖 Multimodal Model")

        # Multimodal Model Settings
        use_multimodal_var = tk.BooleanVar(value=config.multimodal_pref)
        use_multimodal_checkbox = tk.Checkbutton(multimodal_tab, text="Use multimodal model", variable=use_multimodal_var)
        use_multimodal_checkbox.grid(row=0, column=0, columnspan=2, sticky="w")

        model_label = tk.Label(multimodal_tab, text="Select Model:")
        model_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        multimodal_model_combobox = ttk.Combobox(multimodal_tab, values=['gemini-1.5-pro', 'gemini-1.5-flash'], width=20)
        multimodal_model_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")


        def save_multimodal_model(multimodal_model_combobox):
            """Saves the selected multimodal model to the settings.ini file."""
            config.multimodal_model = multimodal_model_combobox.get()
            #Corrected:  Save to the config *file*, not just the object
            config_parser = configparser.ConfigParser()
            config_parser.read(get_default_config_path())
            config_parser['DEFAULT']['multimodalmodel'] = config.multimodal_model  # Use lowercase
            with open(get_default_config_path(), 'w') as configfile:
                config_parser.write(configfile)

            save_settings()

        # Bind the combobox selection event to save
        multimodal_model_combobox.bind("<<ComboboxSelected>>", lambda event: save_multimodal_model(multimodal_model_combobox))


        # MM API Key Setting
        mm_api_key_label = tk.Label(multimodal_tab, text="Multimodal API Key:")
        mm_api_key_label.grid(row=2, column=0, padx=5, pady=5)
        mm_api_key_var = tk.StringVar(multimodal_tab)
        mm_api_key_entry = tk.Entry(multimodal_tab, textvariable=mm_api_key_var, show="*", width=30)
        mm_api_key_entry.grid(row=2, column=1, padx=5, pady=5)

        # Use get_config_dir() for the correct path
        mm_key_path = os.path.join(get_config_dir(), "mm_key.encrypted")
        print(f"[DEBUG] Multimodal key path: {mm_key_path}")
        mm_key_file_exists = os.path.exists(mm_key_path)


        # Initialize buttons (create them first)
        save_delete_mm_button = tk.Button(multimodal_tab, width=12)
        lock_unlock_mm_button = tk.Button(multimodal_tab, width=12)

        def update_mm_ui():
            nonlocal mm_key_file_exists
            mm_key_file_exists = os.path.exists(mm_key_path)
            print(f"[DEBUG] MM key file exists: {mm_key_file_exists}")

            #Update combobox
            if use_multimodal_var.get() == True:
                multimodal_model_combobox.config(state="readonly")
            else:
                multimodal_model_combobox.config(state="disabled")


            if mm_key_file_exists:
                mm_api_key_entry.config(state="readonly")
                mm_api_key_var.set("**********************************")
                save_delete_mm_button.config(text="Delete Key")
                print(f"[DEBUG] Encrypted file exists - Setting entry to readonly, dummy input, and button to 'Delete Key'")

                if config.MM_API_KEY:
                    lock_unlock_mm_button.config(text="🔒 Lock Key", state="normal")
                    print(f"[DEBUG] MM API key loaded - Setting Lock/Unlock button to 'Lock Key' and enabled")

                else:
                    lock_unlock_mm_button.config(text="🔓 Unlock Key", state="normal")
                    print(f"[DEBUG] MM API key NOT loaded - Setting Lock/Unlock button to 'Unlock Key' and enabled")
            else:
                #mm_api_key_entry.config(state="normal") #Removed
                if use_multimodal_var.get() == True: #Added
                    mm_api_key_entry.config(state="normal")
                else:
                    mm_api_key_entry.config(state="disabled")
                mm_api_key_var.set("")
                save_delete_mm_button.config(text="Save Key")
                lock_unlock_mm_button.config(text="🔓 Unlock Key", state="disabled")
                print(f"[DEBUG] No encrypted file - Setting entry based on checkbox, Save/Delete button to 'Save Key', Lock/Unlock to disabled")

            if config.MM_API_KEY is None and mm_key_file_exists:
                 lock_unlock_mm_button.config(state="normal")
                 print(f"[DEBUG] API key is None and file exists - Lock/Unlock button state set to normal")

        def toggle_multimodal_model(var, combobox, entry):
            """Toggles the state of the multimodal model combobox and entry."""
            if var.get():  # Checkbox is checked
                combobox.config(state="readonly")
                if not os.path.exists(mm_key_path):  # Only enable if no key exists
                    entry.config(state="normal")
                update_status("Multimodal model enabled.")
                print("[DEBUG] Multimodal model enabled")
            else:  # Checkbox is unchecked
                combobox.config(state="disabled")
                entry.config(state="disabled") #keep disabled
                update_status("Multimodal model disabled.")
                print("[DEBUG] Multimodal model disabled")

            # Update the config.multimodal_pref variable
            config.multimodal_pref = var.get()
            # Write to config file
            config_parser = configparser.ConfigParser()
            config_parser.read(get_default_config_path())
            config_parser['DEFAULT']['multimodal_pref'] = str(config.multimodal_pref).lower()  # Convert to lowercase string
            with open(get_default_config_path(), 'w') as configfile:
                config_parser.write(configfile)
            update_mm_ui() #Added for updating the UI


        use_multimodal_checkbox.config(command=lambda: toggle_multimodal_model(use_multimodal_var, multimodal_model_combobox, mm_api_key_entry))

        def save_mm_key_ui():
            if mm_api_key_var.get().strip() == "":
                update_status("API key cannot be empty.")
                messagebox.showerror("Error", "API key cannot be empty.")
                return False

            if save_mm_key(mm_api_key_var.get()):
                print(f"[DEBUG] MM key saved successfully")
                update_mm_ui()
                return True
            print(f"[DEBUG] MM key save failed")
            return False

        def delete_mm_key_ui():
            delete_mm_key()
            config.MM_API_KEY = None
            print(f"[DEBUG] MM key deleted and config.MM_API_KEY set to None")
            update_mm_ui()


        def toggle_save_delete_mm_key():
            if save_delete_mm_button.cget("text") == "Save Key":
                print(f"[DEBUG] Save/Delete MM button clicked: Save Key")
                save_mm_key_ui()
            else:
                print(f"[DEBUG] Save/Delete MM button clicked: Delete Key")
                delete_mm_key_ui()

        save_delete_mm_button.config(command=toggle_save_delete_mm_key)
        save_delete_mm_button.grid(row=2, column=2, padx=5, pady=5)


        def toggle_lock_unlock_mm_key():
            if config.MM_API_KEY is None:
                print(f"[DEBUG] Lock/Unlock MM button clicked: Unlock Key")
                password = get_password_from_user("Enter your password to unlock the Multimodal Model key:", "mm")
                if password:
                    if load_mm_key(password=password):
                        lock_unlock_mm_button.config(text="🔒 Lock Key")
                        update_status("Multimodal Model key unlocked.")
                        print(f"[DEBUG] MM key unlocked - Setting Lock/Unlock to 'Lock Key'")
                    else:
                        update_status("Incorrect password for Multimodal Model key.")
                        messagebox.showerror("Error", "Incorrect password for Multimodal Model key.")
                        print(f"[DEBUG] Incorrect password for MM key")
            else:
                print(f"[DEBUG] Lock/Unlock MM button clicked: Lock Key")
                config.MM_API_KEY = None
                lock_unlock_mm_button.config(text="🔓 Unlock Key")
                update_status("Multimodal Model key locked.")
                print(f"[DEBUG] MM key locked - Setting Lock/Unlock to 'Unlock Key'")

        lock_unlock_mm_button.config(command=toggle_lock_unlock_mm_key)
        lock_unlock_mm_button.grid(row=2, column=3, padx=5, pady=5)
        print(f"[DEBUG] Initial state - Encrypted file exists: {mm_key_file_exists}, API key loaded: {config.MM_API_KEY is not None}, Multimodal Checkbox: {use_multimodal_var.get()}")
        update_mm_ui() #Initialise UI
        # Set initial value for combobox
        if (config.multimodal_model != "None" and config.multimodal_model):
            #multimodal_model_combobox.config(state="readonly") #moved to update
            if config.multimodal_model == "gemini-1.5-pro":
                multimodal_model_combobox.current(0)
            else:
                multimodal_model_combobox.current(1)


        # --- Tab 5: Help ---
        help_tab = ttk.Frame(tab_control)
        tab_control.add(help_tab, text="💡 Help")

        read_docs_button = tk.Button(help_tab, text="Read VOXRAD Docs",
                                    command=lambda: open_url("https://voxrad.gitbook.io/voxrad"))
        read_docs_button.pack(pady=20)


        # --- Tab 6: About ---
        about_tab = ttk.Frame(tab_control)
        tab_control.add(about_tab, text="ℹ️ About")

        about_text = """
        Application Name: VOXRAD
        Version: v0.4.0

        Description:
        VOXRAD is a voice transcription application for radiologists leveraging 
        voice transcription models and large language models to restructure and 
        format reports as per predefined user instruction templates.

        Features:
        - Transcribes voice inputs accurately for radiologists.
        - Uses advanced large language models to format and restructure reports.
        - Customizable to predefined user inputs for consistent report formatting.

        Developer Information:
        Developed by: Dr. Ankush
        🌐 https://github.com/drankush/voxrad
        ✉️ voxrad@drankush.com

        License:
        GPLv3

        """
        about_label = tk.Label(about_tab, text=about_text, justify="left")
        about_label.pack(pady=10, padx=10)

        # Bind the window's close event to a function that sets settings_window to None
        config.settings_window.protocol("WM_DELETE_WINDOW", lambda: close_settings_window())

    else:
        # Check if the window still exists before deiconifying
        if config.settings_window.winfo_exists():
            config.settings_window.deiconify()
            config.settings_window.lift()

def close_settings_window():
    """Sets the settings_window reference to None when the window is closed."""
    global settings_window
    config.settings_window.destroy()  # Destroy the window first
    config.settings_window = None  # Then set the reference to None


def toggle_multimodal_model(use_multimodal_var, multimodal_model_combobox, mm_api_key_entry):
    """Toggles the multimodal model settings."""
    mm_key_path = os.path.join(get_default_config_path(), "mm_key.encrypted")  # Changed path
    if use_multimodal_var.get():
        # Enable the combobox and mm api key entry
        multimodal_model_combobox.config(state="readonly")
        if os.path.exists(mm_key_path):
            mm_api_key_entry.config(state="readonly")
        else:
            mm_api_key_entry.config(state="normal")
        config.multimodal_pref = True
        config.multimodal_model = multimodal_model_combobox.get()
        update_status("Multimodal model enabled.")
    else:
        # Disable the combobox and mm api key entry
        multimodal_model_combobox.config(state="disabled")
        mm_api_key_entry.config(state="disabled")
        config.multimodal_pref = False
        config.multimodal_model = None
        update_status("Multimodal model disabled.")

    save_settings()
