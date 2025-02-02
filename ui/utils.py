import tkinter as tk
import random
from config.config import config


status_var = None
status_label = None # Added global status label
waveform_timer = None

def initialize_status_var(main_frame):
    global status_var, status_label
    status_var = tk.StringVar()
    status_label = tk.Label(
        main_frame,
        textvariable=status_var,
        fg='white',
        bg='#0E1118',
        font=('Helvetica', 13),
        wraplength=200,
        justify='center'
    )
    status_label.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
    main_frame.grid_rowconfigure(1, weight=1)  # Allow the status label to expand vertically
    status_var.set("Press record to start recording.✨")

def update_status(message):
    """Updates the status bar with the given message."""
    global status_var, status_label
    if status_var is None or not isinstance(status_var, tk.StringVar):
        print("Re-initializing status_var.")  # Debugging message
        if config.root: # Added condition if config.root is initialized, then do the below
            if config.root.winfo_exists(): # Verify the root exists
                initialize_status_var(config.main_frame) # Pass main_frame as argument
            else:
                print("Error: config.root is not active. Unable to update status.")
                return
        else:
            print("Error: config.root is not initialized. Unable to update status.")
            return # Exit if config.root is not initialized

    if status_var is not None:
        status_var.set(message)
    else:
        print(f"Status update: {message}")  # Fallback if status_var is not initialized
    
    if config.root:
        if config.root.winfo_exists():
            config.root.update() # Force GUI to update immediately


def simulate_waveform(canvas):
    canvas.delete("waveform")  # Clear existing waveform
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    if canvas_width > 1:  # Ensure the canvas has been drawn
        # Calculate the start and end points for the waveform
        start_x = canvas_width / 8
        end_x = canvas_width * 7 / 8
        waveform_width = end_x - start_x
        
        # Calculate the number of points to draw
        num_points = int(waveform_width / 2)  # Adjust this for desired density
        
        # Calculate the center y-coordinate
        center_y = canvas_height / 2
        
        # Draw the waveform
        for i in range(num_points):
            x1 = start_x + (i * waveform_width / num_points)
            x2 = start_x + ((i + 1) * waveform_width / num_points)
            y1 = center_y + random.randint(-10, 10)
            y2 = center_y + random.randint(-10, 10)
            canvas.create_line(x1, y1, x2, y2, fill="yellow", width=1, tags="waveform")
    else:
        # If the canvas hasn't been drawn yet, schedule the drawing for later
        canvas.after(100, lambda: simulate_waveform(canvas))

def draw_straight_line(canvas):
    canvas.delete("waveform")  # Clear any existing waveform
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    if canvas_width > 1:  # Ensure the canvas has been drawn
        # Calculate the center of the canvas
        center_x = canvas_width / 2
        # Draw a line from 1/4 of the width to 3/4 of the width
        start_x = center_x - (canvas_width / 4)
        end_x = center_x + (canvas_width / 4)
        canvas.create_line(start_x, canvas_height/2, end_x, canvas_height/2, fill="yellow", width=1, tags="waveform")
    else:
        # If the canvas hasn't been drawn yet, schedule the drawing for later
        canvas.after(100, lambda: draw_straight_line(canvas))

def start_waveform_simulation(canvas, root):
    global waveform_timer
    simulate_waveform(canvas)
    waveform_timer = root.after(100, start_waveform_simulation, canvas, root)  # Continuously update the waveform

def stop_waveform_simulation(canvas):
    global waveform_timer
    if waveform_timer is not None:
        canvas.after_cancel(waveform_timer)
        waveform_timer = None
