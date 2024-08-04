class Config:
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
    multimodal_pref = False  # Add this line
    multimodal_model = None  # Add this line
    MM_API_KEY = None  # Add this line

config = Config()
