from groq import Groq
import re
import pyperclip
from config.config import config
from ui.utils import update_status
from utils.file_handling import strip_markdown
from llm.format import format_text
import os
from datetime import datetime

def transcribe_audio(mp3_path):
    """Transcribes the audio using Groq's API, extracting spellings from the global template."""
    client = Groq(api_key=config.GROQ_API_KEY)
    
    # Ensure global_md_text_content is initialized
    if hasattr(config, 'global_md_text_content') and config.global_md_text_content:
        content = config.global_md_text_content
    else:
        content = " "

    # Extract spellings from the global template content
    spellings_match = re.search(r'\[correct spellings\](.*?)\[correct spellings\]', content)
    prompt_spellings = spellings_match.group(1).strip() if spellings_match else " "
    
    with open(mp3_path, "rb") as file:
        try:
            update_status("Transcribing...📝")
            transcription_result = client.audio.transcriptions.create(
                file=(mp3_path, file.read()),
                model="whisper-large-v3",
                prompt=prompt_spellings, 
                language="en",
                temperature=0.0
            )
            transcription = transcription_result.text
            update_status("Performing AI analysis.🤖")
            formatted_text = format_text(transcription)
            stripped_text = strip_markdown(formatted_text)
            pyperclip.copy(stripped_text)
            save_report(stripped_text)  # Save the report to a file
            update_status("Your report is ready.✨")
        except Exception as e:
            update_status("Some error occurred. Please check both API keys are saved and/or network connection.")
            print(f"Error details: {e}")

def save_report(report_text):
    """Saves the transcribed report to a file in the reports directory."""
    reports_dir = os.path.join(config.save_directory, "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)  # Create the reports directory if it doesn't exist
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"report_{timestamp}.txt"
    report_filepath = os.path.join(reports_dir, report_filename)
    
    with open(report_filepath, "w") as report_file:
        report_file.write(report_text)
    
    print(f"Report saved to {report_filepath}")
