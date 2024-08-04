import tkinter as tk
from tkinter import ttk
from tkmacosx import Button
from PIL import Image, ImageTk
from audio.recorder import record_audio, stop_recording, pause_audio  # Import the pause_audio function
from utils.file_handling import update_template_dropdown, on_template_select
from ui.settings_window import open_settings
from ui.utils import initialize_status_var, update_status, draw_straight_line, simulate_waveform
from config.config import config  # Import the config instance
from utils.file_handling import load_templates
from audio.transcriber import mm_gemini, transcribe_audio  # Import the transcription function
import os
import threading


# Global variables
recording = False
audio_data = None
start_time = None
recording_thread = None
template_options = []
root = None
canvas = None
record_button = None
stop_button = None
pause_button = None  # Add pause_button
template_dropdown = None 


def retry_transcription():
    """Retries the transcription using the recorded_audio.mp3 file."""
    recorded_audio_path = os.path.join(config.save_directory, "recorded_audio.mp3")
    if os.path.exists(recorded_audio_path):
        if config.multimodal_pref:
            threading.Thread(target=mm_gemini, args=(recorded_audio_path,), daemon=True).start()
        else:
            threading.Thread(target=transcribe_audio, args=(recorded_audio_path,), daemon=True).start()
    else:
        update_status("No recorded audio found to retry transcription.")



def initialize_ui():
    global root, canvas, record_button, stop_button, pause_button, template_dropdown, recording

    root = tk.Tk()
    root.title("VOXRAD MAC")
    root.configure(bg='#0E1118')
    root.geometry("250x300")
    root.resizable(width=False, height=False)

    # Main frame
    main_frame = tk.Frame(root, bg='#0E1118')
    main_frame.pack(fill=tk.BOTH, expand=True)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(2, weight=1)  # Make the status area expandable


    # Top frame (logo and buttons)
    top_frame = tk.Frame(main_frame, bg='#0E1118')
    top_frame.grid(row=0, column=0, sticky='ew')
    top_frame.grid_columnconfigure(1, weight=1)  # Make buttons column expandable

    # Load and resize the logo image
    logo_image = Image.open('voxrad_mac_logo.png')
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(top_frame, image=logo_photo, bg='#0E1118')
    logo_label.image = logo_photo
    logo_label.grid(column=0, row=0, sticky='nsw', padx=10)

    # Buttons frame
    buttons_frame = tk.Frame(top_frame, bg='#0E1118')
    buttons_frame.grid(column=1, row=0, sticky='nsew', padx=(0, 10))
    buttons_frame.grid_columnconfigure(0, weight=1)

    # Buttons
    button_height = logo_photo.height() // 3
    record_button = Button(buttons_frame, text="Record", command=record_audio, bg="lightblue", fg="black", height=button_height)
    record_button.grid(column=0, row=0, sticky='ew', pady=(10, 0))
    pause_button = Button(buttons_frame, text="Pause", command=pause_audio, bg="lightblue", fg="black", state='disabled', height=button_height)
    pause_button.grid(column=0, row=1, sticky='ew', pady=(10, 0))
    stop_button = Button(buttons_frame, text="Stop", command=stop_recording, bg="lightblue", fg="black", state='disabled', height=button_height)
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
    retry_button = tk.Button(bottom_frame, text="🔄", command=retry_transcription, width=1, height=1)
    retry_button.grid(row=0, column=1, padx=0)

    # Settings Button
    settings_button = tk.Button(bottom_frame, text="⚙️", command=open_settings, width=1, height=1)
    settings_button.grid(row=0, column=2, padx=(0, 10))

    # Load templates
    load_templates()

    root.mainloop()


if __name__ == "__main__":
    initialize_ui()
