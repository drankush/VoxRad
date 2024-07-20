import tkinter as tk
import random

status_var = None

def initialize_status_var(root):
    global status_var
    status_var = tk.StringVar()
    status_label = tk.Label(
        root,
        textvariable=status_var,
        fg='white',
        bg='#0E1118',
        font=('Helvetica', 13),
        wraplength=200
    )
    status_label.grid(column=0, row=1, columnspan=2, sticky='ew', padx=10, pady=(5, 5))
    status_var.set("Press record to start recording.✨")

def update_status(message):
    global status_var
    if status_var is not None:
        status_var.set(message)
    else:
        print(f"Status update: {message}")  # Fallback if status_var is not initialized

def simulate_waveform(canvas, root):
    canvas.delete("waveform")  # Clear existing waveform
    start_y = 50
    for i in range(1, 101):
        x = i * 2
        y = start_y + random.randint(-10, 10)  # Simulate waveform variation
        canvas.create_line(x, start_y, x + 2, y, fill="yellow", tags="waveform")
    from audio.recorder import recording  # Import recording flag
    if recording:
        root.after(100, simulate_waveform, canvas, root)  # Continue simulating waveform

def draw_straight_line(canvas):
    canvas.delete("waveform")  # Clear any existing waveform
    canvas.create_line(0, 50, 200, 50, fill="black", tags="waveform")