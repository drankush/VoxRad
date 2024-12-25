
class Config:
    root = None
    save_directory = None
    TEXT_API_KEY = None
    BASE_URL = None
    TRANSCRIPTION_BASE_URL = None
    TRANSCRIPTION_API_KEY = None
    SELECTED_TRANSCRIPTION_MODEL = None
    SELECTED_MODEL = None
    global_md_text_content = ""
    template_dropdown = None
    settings_window = None
    multimodal_pref = False
    multimodal_model = None
    MM_API_KEY = None
    audio_device = None 
    current_encryption_key = None  # To store the key for the encrypted mp3
    current_encrypted_mp3_path = None # To store the encrypted mp3
    secure_paste_shortcut = "ctrl+shift+v"  # Default shortcut
    current_encrypted_report = None  # To store the encrypted report
    current_report_encryption_key = None # To store the key for the encrypted report 

config = Config()

