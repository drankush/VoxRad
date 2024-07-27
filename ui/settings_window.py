import os
import configparser
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import subprocess
import webbrowser
from ui.utils import update_status
from config.config import config
from utils.file_handling import move_files, load_templates
from utils.encryption import save_groq_key, save_openai_key, delete_groq_key, delete_openai_api_key, fetch_models, get_password_from_user, load_groq_key, load_openai_key
from config.settings import save_settings, get_default_config_path


def open_settings():
    """Opens the settings dialog box with additional fields for OpenAI settings."""
    if config.settings_window is None:
        """Opens the settings dialog box with additional fields for OpenAI settings."""
        config.settings_window = tk.Toplevel()
        config.settings_window.title("Settings")

        # Create Tab Control
        tab_control = ttk.Notebook(config.settings_window)
        tab_control.pack(expand=1, fill="both")

        # --- Tab 1: General ---
        general_tab = ttk.Frame(tab_control)
        tab_control.add(general_tab, text="🛠️ General")

        dir_label = tk.Label(general_tab, text="Working Directory:")
        dir_label.grid(row=0, column=0, padx=5, pady=5)
        dir_var = tk.StringVar(general_tab, value=config.save_directory)
        dir_entry = tk.Entry(general_tab, textvariable=dir_var, width=30)
        dir_entry.grid(row=0, column=1, padx=5, pady=5)

        def browse_directory():
            print(config.template_dropdown)
            directory = filedialog.askdirectory()
            if directory:
                old_directory = config.save_directory
                config.save_directory = directory
                dir_var.set(directory)
                save_settings()  # Save settings using self
                if old_directory:
                    move_files(old_directory, config.save_directory)
                load_templates()  # Pass template_dropdown

        # browse_button = tk.Button(general_tab, text="Browse", command=browse_directory)
        browse_button = tk.Button(general_tab, text="Browse", command=lambda: browse_directory())
        browse_button.grid(row=0, column=2, padx=5, pady=5)
        
        def open_templates_folder():
            templates_path = os.path.join(config.save_directory, "templates")
            if not os.path.exists(templates_path):
                os.makedirs(templates_path)
            if os.name == 'nt':
                os.startfile(templates_path)
            elif os.name == 'posix':
                subprocess.run(['open', templates_path])
            else:
                print(f"Unsupported operating system: {os.name}")

        open_templates_button = tk.Button(general_tab, text="Open Templates Folder", command=open_templates_folder)
        open_templates_button.grid(row=1, column=1, padx=5, pady=5)

        # --- Tab 2: Transcription Model ---
        transcription_tab = ttk.Frame(tab_control)
        tab_control.add(transcription_tab, text="🎙️ Transcription Model")

        # Groq API Key Setting
        groq_key_label = tk.Label(transcription_tab, text="Groq API Key:")
        groq_key_label.grid(row=0, column=0, padx=5, pady=5)
        groq_key_var = tk.StringVar(transcription_tab)
        groq_key_entry = tk.Entry(transcription_tab, textvariable=groq_key_var, show="*", width=30, state="normal")

        # Initialize the entry field based on the existence of the encrypted key file
        groq_key_path = os.path.join(config.save_directory, "groq_key.encrypted")
        if os.path.exists(groq_key_path):
            groq_key_entry.config(state="readonly")
            groq_key_var.set("**********************************")
            save_delete_button_state = "Delete Key"
            lock_unlock_button_state = "normal"
        else:
            groq_key_entry.config(state="normal")
            groq_key_var.set("")
            save_delete_button_state = "Save Key"
            lock_unlock_button_state = "disabled"

        groq_key_entry.grid(row=0, column=1, padx=5, pady=5)

        def save_groq_key_ui():
            if groq_key_var.get().strip() == "":
                update_status("API key cannot be empty.")
                messagebox.showerror("Error", "API key cannot be empty.")
                return

            if save_groq_key(groq_key_var.get()):
                # Update UI elements directly within the function
                groq_key_entry.config(state="readonly")
                save_delete_button.config(text="Delete Key")
                lock_unlock_button.config(state="normal", text="🔒 Lock Key")  # Update button text and enable lock button
                config.settings_window.update_idletasks()  # Force UI update

        def delete_groq_key_ui():
            delete_groq_key()
            groq_key_entry.config(state="normal")
            groq_key_var.set("")
            save_delete_button.config(text="Save Key")
            lock_unlock_button.config(state="disabled", text="🔓 Unlock Key")  # Update button text and disable lock button

        def toggle_save_delete_key():
            if save_delete_button.cget("text") == "Save Key":
                if save_groq_key_ui():  # Call save_groq_key_ui and check for success
                    # Update UI elements directly within the function
                    groq_key_entry.config(state="readonly")
                    save_delete_button.config(text="Delete Key")
                    lock_unlock_button.config(state="normal", text="🔒 Lock Key")  # Update button text and enable lock button
                    config.settings_window.update_idletasks()  # Force UI update
            else:
                delete_groq_key_ui()

        save_delete_button = tk.Button(transcription_tab, text=save_delete_button_state,
                                    command=toggle_save_delete_key, width=8)
        save_delete_button.grid(row=0, column=2, padx=5, pady=5)

        def toggle_lock_unlock_groq_key():
            if config.GROQ_API_KEY is None:
                password = get_password_from_user("Enter your password to unlock the Transcription Model key:", "groq")
                if password:
                    if load_groq_key(password=password):
                        lock_unlock_button.config(text="🔒 Lock Key")  # Update button text
                        update_status("Transcription Model key unlocked.")
                    else:
                        update_status("Incorrect password for Transcription Model key.")
                        messagebox.showerror("Error", "Incorrect password for Transcription Model key.")
            else:
                config.GROQ_API_KEY = None
                lock_unlock_button.config(text="🔓 Unlock Key")  # Update button text
                update_status("Transcription Model key locked.")

        # Set initial state for lock/unlock button
        lock_unlock_button_text = "🔒 Lock Key" if config.GROQ_API_KEY else "🔓 Unlock Key"
        lock_unlock_button = tk.Button(transcription_tab, text=lock_unlock_button_text,
                                    command=toggle_lock_unlock_groq_key, width=8, state=lock_unlock_button_state)
        lock_unlock_button.grid(row=0, column=3, padx=5, pady=5)

        # --- Tab 3: Text Model ---
        text_model_tab = ttk.Frame(tab_control)
        tab_control.add(text_model_tab, text="📝 Text Model")

        # OpenAI Settings
        base_url_label = tk.Label(text_model_tab, text="Base URL:")
        base_url_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        base_url_var = tk.StringVar(text_model_tab, value=config.BASE_URL)
        base_url_entry = tk.Entry(text_model_tab, textvariable=base_url_var, width=30)
        base_url_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="w")

        api_key_label = tk.Label(text_model_tab, text="API Key:")
        api_key_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        api_key_var = tk.StringVar(text_model_tab)
        api_key_entry = tk.Entry(text_model_tab, textvariable=api_key_var, show="*", width=30, state="normal")  # Enable entry by default

        # Initialize the entry field based on the existence of the encrypted key file
        openai_key_path = os.path.join(config.save_directory, "openai_key.encrypted")
        if os.path.exists(openai_key_path):
            api_key_entry.config(state="readonly")  # Make it readonly if the file exists
            api_key_var.set("**********************************")  # Set dummy input
            save_delete_openai_button_state = "Delete Key"
            lock_unlock_openai_button_state = "normal"
        else:
            api_key_entry.config(state="normal")  # Make it editable if the file doesn't exist
            api_key_var.set("")  # Set blank
            save_delete_openai_button_state = "Save Key"
            lock_unlock_openai_button_state = "disabled"

        api_key_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        def save_openai_key_ui():
            if api_key_var.get().strip() == "":
                update_status("API key cannot be empty.")
                messagebox.showerror("Error", "API key cannot be empty.")
                return

            if save_openai_key(api_key_var.get()):
                # Update UI elements directly within the function
                api_key_entry.config(state="readonly")
                save_delete_openai_button.config(text="Delete Key")
                lock_unlock_openai_button.config(state="normal", text="🔒 Lock Key")  # Update button text and enable lock button
                config.settings_window.update_idletasks()  # Force UI update

        def delete_openai_key_ui():
            delete_openai_api_key()
            api_key_entry.config(state="normal")
            api_key_var.set("")
            save_delete_openai_button.config(text="Save Key")
            lock_unlock_openai_button.config(state="disabled", text="🔓 Unlock Key")  # Update button text and disable lock button

        def toggle_save_delete_openai_key():
            if save_delete_openai_button.cget("text") == "Save Key":
                if save_openai_key_ui():  # Call save_openai_key_ui and check for success
                    # Update UI elements directly within the function
                    api_key_entry.config(state="readonly")
                    save_delete_openai_button.config(text="Delete Key")
                    lock_unlock_openai_button.config(state="normal", text="🔒 Lock Key")  # Update button text and enable lock button
                    config.settings_window.update_idletasks()  # Force UI update
            else:
                delete_openai_key_ui()

        save_delete_openai_button = tk.Button(text_model_tab, text=save_delete_openai_button_state,
                                            command=toggle_save_delete_openai_key, width=12)
        save_delete_openai_button.grid(row=2, column=2, padx=5, pady=5)

        def toggle_lock_unlock_openai_key():
            if config.OPENAI_API_KEY is None:
                password = get_password_from_user("Enter your password to unlock the Text Model key:", "openai")
                if password:
                    if load_openai_key(password=password):
                        lock_unlock_openai_button.config(text="🔒 Lock Key")  # Update button text
                        update_status("Text Model key unlocked.")
                    else:
                        update_status("Incorrect password for Text Model key.")
                        messagebox.showerror("Error", "Incorrect password for Text Model key.")
            else:
                config.OPENAI_API_KEY = None
                lock_unlock_openai_button.config(text="🔓 Unlock Key")  # Update button text
                update_status("Text Model key locked.")

        # Set initial state for lock/unlock button
        lock_unlock_openai_button_text = "🔒 Lock Key" if config.OPENAI_API_KEY else "🔓 Unlock Key"
        lock_unlock_openai_button = tk.Button(text_model_tab, text=lock_unlock_openai_button_text, command=toggle_lock_unlock_openai_key, width=12, state=lock_unlock_openai_button_state)
        lock_unlock_openai_button.grid(row=2, column=3, padx=5, pady=5)

        fetch_models_button = tk.Button(text_model_tab, text="Fetch Models",
                                        command=lambda: fetch_models(base_url_var.get(), api_key_var.get(), model_combobox), width=12)
        fetch_models_button.grid(row=3, column=2, padx=5, pady=5)

        model_label = tk.Label(text_model_tab, text="Select Model:")
        model_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        model_combobox = ttk.Combobox(text_model_tab, width=29, state="readonly")
        model_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        def open_url(url):
            webbrowser.open_new(url)

        # OpenAI Disclaimer Label
        disclaimer_frame = tk.Frame(text_model_tab)
        disclaimer_frame.grid(row=0, column=0, columnspan=4, pady=(5, 0), sticky="w")

        disclaimer_text = "  Supports any OpenAI compatible API. Read more"
        disclaimer_label = tk.Label(disclaimer_frame, text=disclaimer_text, font=("Helvetica", 10, "italic"))
        disclaimer_label.pack(side=tk.LEFT)

        here_link = tk.Label(disclaimer_frame, text="here", font=("Helvetica", 10, "italic"), fg="blue", cursor="arrow")
        here_link.pack(side=tk.LEFT)
        here_link.bind("<Button-1>", lambda e: open_url("https://platform.openai.com/docs/api-reference"))

        def open_url(url):
            if os.name == 'nt':
                os.startfile(url)
            elif os.name == 'posix':
                subprocess.Popen(['open', url])
            else:
                print(f"Unsupported operating system: {os.name}")

        def save_all_settings():
            config_parser = configparser.ConfigParser()
            config_parser['DEFAULT'] = {
                'WorkingDirectory': dir_var.get(),
                'OpenAIBaseURL': base_url_var.get(),
                'SelectedModel': model_combobox.get()
            }
            with open(get_default_config_path(), 'w') as configfile:
                config_parser.write(configfile)
            config.save_directory = dir_var.get()
            config.BASE_URL = base_url_var.get()
            config.SELECTED_MODEL = model_combobox.get()
            update_status("Settings saved.")

        save_settings_button = tk.Button(text_model_tab, text="Save Settings", command=save_all_settings, width=12)
        save_settings_button.grid(row=3, column=3, padx=5, pady=5)

        # --- Tab 4: Help ---
        help_tab = ttk.Frame(tab_control)
        tab_control.add(help_tab, text="💡 Help")

        read_docs_button = tk.Button(help_tab, text="Read VOXRAD Docs",
                                    command=lambda: open_url("https://github.com/drankush/voxrad/"))
        read_docs_button.pack(pady=20)


        # --- Tab 5: About ---
        about_tab = ttk.Frame(tab_control)
        tab_control.add(about_tab, text="ℹ️ About")

        about_text = """
        Application Name: VOXRAD
        Version: v1.2

        Description:
        VOXRAD is a voice transcription application for radiologists leveraging 
        voice transcription models and large language models to restructure and 
        format reports as per predefined user inputs.

        Features:
        - Transcribes voice inputs accurately for radiologists.
        - Uses advanced large language models to format and restructure reports.
        - Customizable to predefined user inputs for consistent report formatting.

        Developer Information:
        Developed by: Dr. Ankush
        🌐 www.drankush.com
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
