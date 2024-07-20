from groq import Groq
import re
import pyperclip
from config.config import config
from ui.utils import update_status
from utils.file_handling import strip_markdown
from llm.format import format_text

def transcribe_audio(mp3_path):
    """Transcribes the audio using Groq's API, extracting spellings from the global template."""
    client = Groq(api_key=config.GROQ_API_KEY)
    
    # Ensure global_md_text_content is initialized
    if hasattr(config, 'global_md_text_content') and config.global_md_text_content:
        content = config.global_md_text_content
    else:
        content = " "

    # print(f"Using global_md_text_content: {config.global_md_text_content}")  # Debug
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
            # print(transcription) # for debugging
            update_status("Performing AI analysis.🤖")
            formatted_text = format_text(transcription)
            stripped_text = strip_markdown(formatted_text)
            pyperclip.copy(stripped_text)
            update_status("Your report is ready.✨")
        except Exception as e:
            update_status(f"Error during transcription or restructuring/formatting the report: {e}")
            print(f"Error details: {e}")