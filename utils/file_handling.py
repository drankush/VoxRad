import os
import sys
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
from config.config import config

# Global variables
template_options = []


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



def load_templates():
    """Loads templates from the 'templates' directory and updates dropdown."""
    global template_options
    template_dir = os.path.join(config.save_directory, "templates")
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)  # Create the templates directory if it doesn't exist
    
    # List of template files to copy. Can be expanded in future for templates to be packaged.
    template_files_to_copy = ["HRCT_Thorax.txt"]
    
    # Copy specified template files from resource path to the working directory
    for template_file in template_files_to_copy:
        source_file = resource_path(os.path.join("templates", template_file))
        destination_file = os.path.join(template_dir, template_file)
        if os.path.exists(source_file) and not os.path.exists(destination_file):
            shutil.copy2(source_file, destination_file)
            print(f"Copied {template_file} to {destination_file}")
    
    template_files = [f for f in os.listdir(template_dir) if f.endswith((".txt", ".md"))]
    template_files.sort()  # Sort the list of template files alphabetically
    template_options = [os.path.splitext(f)[0].replace("_", " ") for f in template_files]
    update_template_dropdown()


def update_template_dropdown():
    """Updates the options in the template dropdown menu."""
    global template_options
    if config.template_dropdown:  # Ensure template_dropdown is not None
        config.template_dropdown["values"] = template_options
        print(f"Combobox values updated: {config.template_dropdown['values']}")  # Debug: Print the updated combobox values
        if template_options:  # Check if template_options is not empty
            config.template_dropdown.set("")  # Set an empty selection to force user to choose

def on_template_select(event=None):
    """Handles template selection from the dropdown menu."""
    if config.template_dropdown:
        selected_index = config.template_dropdown.current()
        if selected_index != -1:
            selected_template = template_options[selected_index]
            template_file_txt = os.path.join(config.save_directory, "templates", selected_template.replace(" ", "_") + ".txt")
            template_file_md = os.path.join(config.save_directory, "templates", selected_template.replace(" ", "_") + ".md")
            
            # Try to read .txt file first, if it fails, try .md file
            try:
                if os.path.exists(template_file_txt):
                    with open(template_file_txt, "r") as f:
                        config.global_md_text_content = f.read()
                        print(f"Loaded content from {template_file_txt}")
                elif os.path.exists(template_file_md):
                    with open(template_file_md, "r") as f:
                        config.global_md_text_content = f.read()
                        print(f"Loaded content from {template_file_md}")
                else:
                    raise FileNotFoundError(f"Template file not found: {selected_template}")
                print(f"global_md_text_content set to: {config.global_md_text_content}")  # Debug
            except Exception as e:
                print(f"Error loading template: {e}")
                config.global_md_text_content = ""


def move_files(old_dir, new_dir):
    """Moves the templates folder from the old to the new directory."""
    folder_name = "templates"
    old_path = os.path.join(old_dir, folder_name)
    new_path = os.path.join(new_dir, folder_name)

    if os.path.exists(old_path):
        if os.path.exists(new_path):
            if messagebox.askyesno("Confirm Overwrite", f"'{folder_name}' folder already exists in the new directory. Overwrite?"):
                try:
                    shutil.rmtree(new_path)
                    shutil.move(old_path, new_path)
                    print(f"Moved '{folder_name}' folder from '{old_path}' to '{new_path}'")
                except Exception as e:
                    print(f"Error moving '{folder_name}' folder: {e}")
        else:
            try:
                shutil.move(old_path, new_path)
                print(f"Moved '{folder_name}' folder from '{old_path}' to '{new_path}'")
            except Exception as e:
                print(f"Error moving '{folder_name}' folder: {e}")

def strip_markdown(text):
    """Strips markdown formatting from a given text."""
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    return text
