from groq import Groq
from openai import OpenAI
import re
import pyperclip
from config.config import config
from ui.utils import update_status
from utils.file_handling import strip_markdown
from llm.format import format_text
import os
from datetime import datetime
import google.generativeai as genai

def transcribe_audio(mp3_path):
    """Transcribes the audio using OpenAI's API, extracting spellings from the global template."""
    client = OpenAI(api_key=config.TRANSCRIPTION_API_KEY, base_url=config.TRANSCRIPTION_BASE_URL)
    
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
                model=config.SELECTED_TRANSCRIPTION_MODEL,
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
            if os.name == "nt":
                update_status(f"Report saved to {config.save_directory}/reports/ and Clipboard. Ctrl+V to paste the saved report into your application.✨")
            else:
                update_status(f"Report saved to {config.save_directory}/reports/ and Clipboard. Cmd+V to paste the saved report into your application.✨")
        except Exception as e:
            update_status("Some error occurred. Please check both API keys are saved and/or network connection.")
            print(f"Error details: {e}")


def mm_gemini(mp3_path):
    """Generates text from audio using the multimodal Gemini model."""
    try:
        update_status("Performing AI analysis.🤖")
        # print(f"MM_API_KEY: {config.MM_API_KEY}")  # Print MM_API_KEY
        # print(f"Audio Path: {mp3_path}")  # Print the audio path
        genai.configure(api_key=config.MM_API_KEY)
        audio_file = genai.upload_file(path=mp3_path)
        model = genai.GenerativeModel(model_name=config.multimodal_model)
        # print(f"Multimodal Model: {config.multimodal_model}")  # Print the selected model
        prompt = f"""
The provided audio is as dictated by a radiologist regarding a report of radiological study. Format is according to a standard radiological report.         
This is the report template format as chosen by the user:
{config.global_md_text_content}

                            """
        # print(f"Prompt: {prompt}")  # Print the prompt
        response = model.generate_content([prompt, audio_file])
        # print(response.text)
        # Extract the text from the response
        if response.text:
            stripped_text = strip_markdown(response.text)  # Strip markdown
            pyperclip.copy(stripped_text)  # Copy to clipboard
            save_report(stripped_text)  # Save the report
            if os.name == "nt":
                update_status(f"Report saved to {config.save_directory}/reports/ and Clipboard. Ctrl+V to paste the saved report into your application.✨")
            else:
                update_status(f"Report saved to {config.save_directory}/reports/ and Clipboard. Cmd+V to paste the saved report into your application.✨")
            return stripped_text  # Return the processed text
        else:
            update_status("No text returned by the multimodal model.")
            return None
    except Exception as e:
        update_status(f"Failed to to generate summary. Error: {str(e)}")
    return None


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
