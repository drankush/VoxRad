import os
import subprocess
import sys
import configparser

def get_config_path():
    if os.name == "nt":
        config_dir = os.path.join(os.environ["APPDATA"], "VOXRAD")
    else:
        config_dir = os.path.join(os.path.expanduser("~"), ".voxrad")
    return os.path.join(config_dir, "settings.ini")

def configure_defaults():
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        
    config_parser = configparser.ConfigParser()
    if os.path.exists(config_path):
        config_parser.read(config_path)
    
    if "DEFAULT" not in config_parser:
        config_parser["DEFAULT"] = {}
        
    # Set requested defaults for local operation
    config_parser["DEFAULT"]["ASRBackend"] = "local"
    config_parser["DEFAULT"]["WhisperModelSize"] = "small"
    config_parser["DEFAULT"]["WhisperQuantization"] = "int8"
    config_parser["DEFAULT"]["WhisperLanguage"] = "pt"
    config_parser["DEFAULT"]["TextBaseURL"] = "http://localhost:11434/v1"
    config_parser["DEFAULT"]["SelectedModel"] = "llama3.1:latest"
    
    with open(config_path, "w") as f:
        config_parser.write(f)
    print(f"Configured defaults in {config_path}")

if __name__ == "__main__":
    print("Setting up local environment for VoxRad...")
    
    # 1. Update settings.ini with local defaults
    configure_defaults()
    
    # 2. Check for Ollama
    print("\nChecking for Ollama...")
    try:
        # Simple check if ollama command exists
        subprocess.run(["ollama", "--version"], check=True, capture_output=True)
        print("Ollama is installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("WARNING: Ollama not found in PATH. Please install it from https://ollama.com/")
        
    print("\nLocal environment setup complete.")
    print("To start VoxRad, use: .\\.venv\\Scripts\\python VoxRad.py")
