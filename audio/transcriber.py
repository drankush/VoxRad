from openai import OpenAI
from faster_whisper import WhisperModel
import re
from config.config import config
from ui.utils import update_status
from utils.file_handling import strip_markdown
from llm.format import format_text
import os
from datetime import datetime
import google.generativeai as genai
from cryptography.fernet import Fernet
import tempfile

def transcribe_audio(encrypted_mp3_path, decryption_key):
    """Transcribes the audio from an encrypted MP3 file using OpenAI's API."""
    if not encrypted_mp3_path or not decryption_key:
        print("Error: Encrypted MP3 path or decryption key missing.")
        update_status("Error: Could not process audio.")
        return

    if getattr(config, 'ASR_BACKEND', 'api') == "local":
        return transcribe_audio_local(encrypted_mp3_path, decryption_key)

    cipher_suite = Fernet(decryption_key)
    decrypted_mp3_path = None
    try:
        with open(encrypted_mp3_path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_decrypted_file:
            tmp_decrypted_file.write(decrypted_data)
            decrypted_mp3_path = tmp_decrypted_file.name

        client = OpenAI(api_key=config.TRANSCRIPTION_API_KEY, base_url=config.TRANSCRIPTION_BASE_URL)

        if hasattr(config, 'global_md_text_content') and config.global_md_text_content:
            content = config.global_md_text_content
        else:
            content = " "

        spellings_match = re.search(r'\[correct spellings\](.*?)\[correct spellings\]', content)
        prompt_spellings = spellings_match.group(1).strip() if spellings_match else " "

        with open(decrypted_mp3_path, "rb") as decrypted_file:
            update_status("Transcribing...📝")
            transcription_result = client.audio.transcriptions.create(
                file=(decrypted_mp3_path, decrypted_file.read()),
                model=config.SELECTED_TRANSCRIPTION_MODEL,
                prompt=prompt_spellings,
                language="en",
                temperature=0.0
            )
            transcription = transcription_result.text
            update_status("Performing AI analysis.🤖")
            formatted_text = format_text(transcription)
            stripped_text = strip_markdown(formatted_text)

            # Encrypt the report and store it in config
            report_key = Fernet.generate_key()
            report_cipher = Fernet(report_key)
            encrypted_report = report_cipher.encrypt(stripped_text.encode()).decode()
            config.current_encrypted_report = encrypted_report
            config.current_report_encryption_key = report_key.decode()

            if os.name == "nt":
                update_status(f"Report generated. Use {config.secure_paste_shortcut} to securely paste.✨")
            else:
                update_status(f"Report generated. Use {config.secure_paste_shortcut} to securely paste.✨")

    except Exception as e:
        update_status(f"Error decrypting or transcribing audio: {e}")
        print(f"Error details: {e}")
    finally:
        if decrypted_mp3_path and os.path.exists(decrypted_mp3_path):
            os.remove(decrypted_mp3_path)

def transcribe_audio_local(encrypted_mp3_path, decryption_key):
    """Transcribes the audio locally using faster-whisper."""
    cipher_suite = Fernet(decryption_key)
    decrypted_mp3_path = None
    try:
        with open(encrypted_mp3_path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_decrypted_file:
            tmp_decrypted_file.write(decrypted_data)
            decrypted_mp3_path = tmp_decrypted_file.name

        update_status(f"Loading local model ({config.WHISPER_MODEL_SIZE})... ⏳")
        # Initialize model
        # Using GPU if available, else CPU
        device = "cuda" if os.getenv("CUDA_VISIBLE_DEVICES") != "" else "cpu"
        # Force cpu if no nvidia-smi found previously? No, I checked and it's there.
        # But to be safe, we can use "auto".
        model = WhisperModel(
            config.WHISPER_MODEL_SIZE, 
            device="auto", 
            compute_type=config.WHISPER_QUANTIZATION
        )

        update_status("Transcribing locally...📝")
        segments, info = model.transcribe(
            decrypted_mp3_path, 
            beam_size=5, 
            language=config.WHISPER_LANGUAGE
        )
        
        transcription = "".join([segment.text for segment in segments])
        
        update_status("Performing AI analysis.🤖")
        formatted_text = format_text(transcription)
        stripped_text = strip_markdown(formatted_text)

        # Encrypt the report and store it in config
        report_key = Fernet.generate_key()
        report_cipher = Fernet(report_key)
        encrypted_report = report_cipher.encrypt(stripped_text.encode()).decode()
        config.current_encrypted_report = encrypted_report
        config.current_report_encryption_key = report_key.decode()

        update_status(f"Report generated. Use {config.secure_paste_shortcut} to securely paste.✨")
        return stripped_text

    except Exception as e:
        update_status(f"Error in local transcription: {e}")
        print(f"Error details: {e}")
    finally:
        if decrypted_mp3_path and os.path.exists(decrypted_mp3_path):
            os.remove(decrypted_mp3_path)

def mm_gemini(encrypted_mp3_path, decryption_key):
    """Generates text from an encrypted audio file using the multimodal Gemini model."""
    if not encrypted_mp3_path or not decryption_key:
        print("Error: Encrypted MP3 path or decryption key missing.")
        update_status("Error: Could not process audio.")
        return

    cipher_suite = Fernet(decryption_key)
    decrypted_mp3_path = None
    try:
        with open(encrypted_mp3_path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_decrypted_file:
            tmp_decrypted_file.write(decrypted_data)
            decrypted_mp3_path = tmp_decrypted_file.name

        update_status("Performing AI analysis.🤖")
        genai.configure(api_key=config.MM_API_KEY)
        audio_file = genai.upload_file(path=decrypted_mp3_path)
        model = genai.GenerativeModel(model_name=config.multimodal_model)
        prompt = f"""
The provided audio is as dictated by a radiologist regarding a report of radiological study. Format is according to a standard radiological report.
This is the report template format as chosen by the user:
{config.global_md_text_content}
"""
        response = model.generate_content([prompt, audio_file])
        if response.text:
            stripped_text = strip_markdown(response.text)

            # Encrypt the report and store it in config
            report_key = Fernet.generate_key()
            report_cipher = Fernet(report_key)
            encrypted_report = report_cipher.encrypt(stripped_text.encode()).decode()
            config.current_encrypted_report = encrypted_report
            config.current_report_encryption_key = report_key.decode()

            if os.name == "nt":
                update_status(f"Report generated. Use {config.secure_paste_shortcut} to securely paste.✨")
            else:
                update_status(f"Report generated. Use {config.secure_paste_shortcut} to securely paste.✨")
            return stripped_text
        else:
            update_status("No text returned by the multimodal model.")
            return None
    except Exception as e:
        update_status(f"Failed to generate summary. Error: {str(e)}")
        print(f"Error details: {e}")
        return None
    finally:
        if decrypted_mp3_path and os.path.exists(decrypted_mp3_path):
            os.remove(decrypted_mp3_path)

def save_report(report_text):
    """Saves the transcribed report to a file in the reports directory."""
    reports_dir = os.path.join(config.save_directory, "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"report_{timestamp}.txt"
    report_filepath = os.path.join(reports_dir, report_filename)

    with open(report_filepath, "w") as report_file:
        report_file.write(report_text)

    print(f"Report saved to {report_filepath}")

