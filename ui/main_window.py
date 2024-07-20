import tkinter as tk
from tkinter import ttk
from tkmacosx import Button
from PIL import Image, ImageTk
from audio.recorder import record_audio, stop_recording
from utils.file_handling import update_template_dropdown, on_template_select
from ui.settings_window import open_settings
from ui.utils import initialize_status_var, update_status, simulate_waveform, draw_straight_line
from config.config import config  # Import the config instance
from utils.file_handling import load_templates

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
template_dropdown = None 

def initialize_ui():
    global root, canvas, record_button, stop_button, template_dropdown, recording

    root = tk.Tk()
    root.title("VOXRAD MAC")
    root.configure(bg='#0E1118')
    root.geometry("250x300")
    root.resizable(width=False, height=False)

    initialize_status_var(root)  # Initialize the status variable

    # Load and resize the logo image
    logo_image = Image.open('voxrad_mac_logo.png')
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(root, image=logo_photo, bg='#0E1118')
    logo_label.image = logo_photo  # Keep a reference to the image
    logo_label.grid(column=0, row=0, sticky='ns', padx=10)

    # Frame for buttons
    buttons_frame = tk.Frame(root, bg='#0E1118')
    buttons_frame.grid(column=1, row=0, sticky='nsew', padx=(0, 10))

    # Configure row heights to align with logo
    logo_height = logo_photo.height()
    button_height = logo_height // 2  # Half the height of the logo for each button
    buttons_frame.rowconfigure([0, 1], minsize=button_height)

    # Buttons
    record_button = Button(buttons_frame, text="Record", command=record_audio, bg="lightblue", fg="black", height=button_height)
    record_button.grid(column=0, row=0, sticky='ew', pady=(10, 0))  # Align with top of logo

    stop_button = Button(buttons_frame, text="Stop", command=stop_recording, bg="lightblue", fg="black", state='disabled', height=button_height)
    stop_button.grid(column=0, row=1, sticky='ew', pady=(10, 0))  # Align with bottom of logo

    # Canvas for the waveform adjusted to fill the width
    canvas = tk.Canvas(root, width=root.winfo_width(), height=100, bg='#0E1118', highlightthickness=0)
    canvas.grid(column=0, row=3, columnspan=2, sticky='ew', padx=25, pady=(5, 10))
    draw_straight_line(canvas)

    # Ensure the widgets do not cover each other and canvas fills the width
    root.columnconfigure(0, weight=1)
    root.rowconfigure(3, weight=1)

    # Create a frame to hold the combobox and settings button
    bottom_frame = tk.Frame(root, bg='#0E1118')
    bottom_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=(0, 10))

    # Center the bottom frame
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(4, weight=1)

    # --- Template Dropdown ---
    global template_dropdown  # Declare as global to modify in functions
    template_dropdown = ttk.Combobox(bottom_frame, values=template_options, state="readonly", width=20)
    template_dropdown.grid(row=0, column=0, padx=(0, 5))
    # template_dropdown.bind("<<ComboboxSelected>>", on_template_select)
    template_dropdown.bind("<<ComboboxSelected>>", lambda event: on_template_select(event, template_dropdown))
    # --- End of Template Dropdown ---

    # Settings Button
    settings_button = tk.Button(bottom_frame, text="⚙️", command=open_settings, width=2, height=1)
    settings_button.grid(row=0, column=1)

    # Center the contents of the bottom frame
    bottom_frame.grid_columnconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(1, weight=1)

    # Load templates and update dropdown after creating template_dropdown
    load_templates(template_dropdown)

    root.mainloop()