"""Global constants for VoxRad application."""

import os

DEFAULT_BITRATE = 128
MIN_BITRATE = 32
MAX_BITRATE = 320
AUDIO_CHUNK_SIZE = 4096
MAX_AUDIO_SIZE_MB = 25
MAX_AUDIO_SIZE_BYTES = MAX_AUDIO_SIZE_MB * 1024 * 1024

ENCRYPTED_TRANSCRIPTION_KEY_FILE = "transcription_key.encrypted"
ENCRYPTED_TEXT_KEY_FILE = "text_key.encrypted"
ENCRYPTED_MM_KEY_FILE = "multimodal_key.encrypted"

ASR_SALT_FILE = ".asr_salt"
SETTINGS_FILENAME = "settings.ini"

TEMPLATE_FILE_EXTENSION = ".txt"
GUIDELINE_FILE_EXTENSION = ".md"

WHISPER_DEFAULT_LANGUAGE = "en"
WHISPER_DEFAULT_MODEL_SIZE = "base"

PLATFORM_WINDOWS = "nt"
PLATFORM_UNIX = "posix"

MAX_RETRY_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = 1

API_TIMEOUT_SECONDS = 30

FERNET_KEY_SIZE = 32

OPENAI_API_TIMEOUT = 60
GEMINI_API_TIMEOUT = 60
OLLAMA_API_TIMEOUT = 120

CONFIG_DIR_WINDOWS = os.path.expandvars("%APPDATA%\\VOXRAD")
CONFIG_DIR_UNIX = os.path.expanduser("~/.voxrad")

LOG_DIR = os.path.expanduser("~/.voxrad/logs")

SUPPORTED_AUDIO_FORMATS = [".wav", ".mp3", ".m4a", ".ogg", ".flac"]
SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".gif"]
