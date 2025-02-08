import tkinter as tk
from tkinter import ttk
from config.config import config
from audio.recorder import record_audio, stop_recording, pause_audio
from config.settings import load_settings
from ui.settings_window import open_settings
from ui.utils import initialize_status_var, update_status, draw_straight_line
from audio.transcriber import mm_gemini, transcribe_audio
from utils.file_handling import resource_path
from utils.file_handling import  on_template_select, load_templates, load_guidelines
from llm.secure_paste import initialize_secure_paste
import os

# Global variables
recording = False
audio_data = None
start_time = None
recording_thread = None
template_options = []
canvas = None
record_button = None
stop_button = None
pause_button = None
template_dropdown = None
logo_label = None

def retry_transcription():
    """Retries the transcription using the last encrypted audio file and key."""
    print(config.current_encrypted_mp3_path)
    print(config.current_encryption_key)
    if config.current_encrypted_mp3_path and config.current_encryption_key:
        update_status("Reprocessing last recorded audio...")
        if config.multimodal_pref:
            config.root.after(100, lambda: mm_gemini(config.current_encrypted_mp3_path, config.current_encryption_key))
        else:
            config.root.after(100, lambda: transcribe_audio(config.current_encrypted_mp3_path, config.current_encryption_key))
    else:
        update_status("No previous recording found to retry.")


def initialize_ui():
    global canvas, record_button, stop_button, pause_button, template_dropdown, recording, logo_label

    config.root = tk.Tk()
    if os.name == "nt":
        config.root.title("VOXRAD WIN")
    else:
        config.root.title("VOXRAD MAC")
    config.root.configure(bg='#0E1118')
    config.root.geometry("250x300")
    config.root.resizable(width=False, height=False)

    # Initialize secure paste
    initialize_secure_paste() 

    # Main frame
    main_frame = tk.Frame(config.root, bg='#0E1118')
    main_frame.pack(fill=tk.BOTH, expand=True)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(2, weight=1)

    # Top frame (logo and buttons)
    top_frame = tk.Frame(main_frame, bg='#0E1118')
    top_frame.grid(row=0, column=0, sticky='ew')
    top_frame.grid_columnconfigure(1, weight=1)

    # Logo setup

    logo_path = resource_path('voxrad_mac_logo.png')
    logo_photo = tk.PhotoImage(file=logo_path)
    logo_label = tk.Label(top_frame, image=logo_photo, bg='#0E1118')
    logo_label.image = logo_photo
    logo_label.grid(column=0, row=0, sticky='nsw', padx=10)

    #     # Load and resize the logo image
    # logo_image = Image.open('voxrad_mac_logo.png')
    # logo_photo = ImageTk.PhotoImage(logo_image)
    # logo_label = tk.Label(top_frame, image=logo_photo, bg='#0E1118')
    # logo_label.image = logo_photo
    # logo_label.grid(column=0, row=0, sticky='nsw', padx=10)

    # Buttons frame
    buttons_frame = tk.Frame(top_frame, bg='#0E1118')
    buttons_frame.grid(column=1, row=0, sticky='nsew', padx=(0, 10))
    buttons_frame.grid_columnconfigure(0, weight=1)

    # Buttons with fixed height
    button_height = 1  # Fixed height in text units
    record_button = tk.Button(buttons_frame, text="Record", command=record_audio, bg="lightblue", fg="black", height=button_height)
    record_button.grid(column=0, row=0, sticky='ew', pady=(10, 0))
    pause_button = tk.Button(buttons_frame, text="Pause", command=pause_audio, bg="lightblue", fg="black", state='disabled', height=button_height)
    pause_button.grid(column=0, row=1, sticky='ew', pady=(10, 0))
    stop_button = tk.Button(buttons_frame, text="Stop", command=stop_recording, bg="lightblue", fg="black", state='disabled', height=button_height)
    stop_button.grid(column=0, row=2, sticky='ew', pady=(10, 0))

    # Initialize status variable
    initialize_status_var(main_frame)

    # Frame for waveform
    waveform_frame = tk.Frame(main_frame, bg='#0E1118')
    waveform_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)
    waveform_frame.grid_columnconfigure(0, weight=1)
    waveform_frame.grid_rowconfigure(0, weight=1)

    # Canvas for waveform
    canvas = tk.Canvas(waveform_frame, height=50, bg='#0E1118', highlightthickness=0)
    canvas.grid(row=0, column=0, sticky='nsew')
    draw_straight_line(canvas)

    # Bottom frame (fixed at the bottom)
    bottom_frame = tk.Frame(main_frame, bg='#0E1118')
    bottom_frame.grid(row=3, column=0, sticky='ew', pady=(0, 10))
    bottom_frame.grid_columnconfigure(0, weight=1)

    # Template Dropdown
    config.template_dropdown = ttk.Combobox(bottom_frame, values=template_options, state="readonly")
    config.template_dropdown.grid(row=0, column=0, sticky='ew', padx=(10, 5))
    config.template_dropdown.bind("<<ComboboxSelected>>", lambda event: on_template_select(event))

    # Retry Button

    if os.name == "nt":
        retry_button = tk.Button(bottom_frame, text="⟳", command=retry_transcription, width=3, height=1)
        retry_button.grid(row=0, column=1, padx=0)
    else:
        retry_button = tk.Button(bottom_frame, text="🔄", command=retry_transcription, width=1, height=1)
        retry_button.grid(row=0, column=1, padx=0)

    # Settings Button
    if os.name == "nt":
        settings_button = tk.Button(bottom_frame, text="⚙️", command=open_settings, width=3, height=1)
        settings_button.grid(row=0, column=2, padx=(0, 10))
    else:
        settings_button = tk.Button(bottom_frame, text="⚙️", command=open_settings, width=1, height=1)
        settings_button.grid(row=0, column=2, padx=(0, 10))


    # Load settings and keys on startup
    load_settings()  # This initializes save_directory
    
    # Load templates
    load_templates()

    # Load guidelines
    load_guidelines()


    config.root.mainloop()

if __name__ == "__main__":
    initialize_ui()
