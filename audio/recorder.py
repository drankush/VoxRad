import sounddevice as sd
import threading
import time
import numpy as np
import soundfile as sf
import os
import subprocess
from config.config import config  
from audio.transcriber import transcribe_audio
from ui.utils import update_status, simulate_waveform, draw_straight_line

# Global variables
recording = False
audio_data = None
start_time = None
recording_thread = None

def record_audio():
    """Starts audio recording after checking for Groq API key."""
    global recording, recording_thread
    print(f"GROQ API Key from recorder.py: {config.GROQ_API_KEY}")
    if config.GROQ_API_KEY is None:
        update_status("Please set your Transcription Model API key in settings.")
        return
    recording = True
    from ui.main_window import record_button, stop_button, canvas, root  # Import additional global variables
    record_button['state'] = 'disabled'
    stop_button['state'] = 'normal'
    recording_thread = threading.Thread(target=background_recording, daemon=True)
    recording_thread.start()
    update_status("Recording 🔴")
    simulate_waveform(canvas, root)  # Start simulating the waveform

def background_recording():
    global audio_data, start_time, recording
    fs = 44100  # Sample rate
    start_time = time.time()

    audio_data = np.array([], dtype='float32')  # Initialize audio_data to prevent NameError

    try:
        # Prepare recording stream
        stream = sd.InputStream(samplerate=fs, channels=1, dtype='float32')
        stream.start()
        chunks = []
        print("Recording started...")

        loop_counter = 0  # To count the number of iterations (chunks recorded)

        # Record as long as recording is True
        while recording:
            data, overflowed = stream.read(fs)  # Read data for 1 second
            if overflowed:
                print("Audio buffer overflowed")
            chunks.append(data)

            # Log the size of the current chunk and the iteration count
            print(f"Chunk {loop_counter}: shape={data.shape}, overflowed={overflowed}")
            loop_counter += 1

        # Stop and close the stream
        stream.stop()
        stream.close()
        print(f"Recording stopped. Total chunks recorded: {loop_counter}")

        # Combine chunks into one array
        audio_data = np.vstack(chunks)
        print(f"Total recording duration (approx.): {audio_data.shape[0]/fs} seconds")

    except Exception as e:
        print(f"An error occurred during recording: {e}")

    if not recording:
        update_status("Started Processing...⚙️")

def stop_recording():
    global recording, audio_data, start_time, recording_thread
    # print("stop_recording called") #Debug
    recording = False  # Signal to stop recording
    
    # Schedule a check to wait for the recording to finish non-blockingly
    from ui.main_window import root  # Import global variable
    root.after(100, check_recording_finished)

def check_recording_finished():
    global recording_thread
    # print("check_recording_finished called") #Debug
    from ui.main_window import root  # Import global variable
    if recording_thread.is_alive():
        # Check again after some time if the recording thread is still alive
        root.after(100, check_recording_finished)
    else:
        # Now that the recording thread has finished, proceed with saving and other tasks
        complete_stop_recording()

def complete_stop_recording():
    global audio_data, start_time, recording
    print("complete_stop_recording called")
    # This function now contains the code to save the recording and any other tasks
    # that should only be executed after the recording has completely stopped.
    sd.stop()
    from ui.main_window import record_button, stop_button, canvas  # Import additional global variables
    record_button['state'] = 'normal'
    stop_button['state'] = 'disabled'
    # print("Before draw_straight_line(canvas)")
    draw_straight_line(canvas)
    # print("After draw_straight_line(canvas)") #Debug

    fs = 44100  # Sample rate used for recording
    if hasattr(audio_data, 'size') and audio_data.size > 0:
        wav_path = save_audio_as_wav(audio_data, fs)
        mp3_path = convert_wav_to_mp3(wav_path)
        threading.Thread(target=transcribe_audio, args=(mp3_path,), daemon=True).start()
    else:
        print("No audio data to save.")

def save_audio_as_wav(audio_data, fs):
    """Saves the recorded audio to a WAV file."""
    file_path = os.path.join(config.save_directory, "recorded_audio.wav")
    sf.write(file_path, audio_data, fs)
    return file_path

def convert_wav_to_mp3(wav_path):
    """Converts a WAV file to MP3 format using ffmpeg, targeting a maximum file size."""
    mp3_path = wav_path.replace(".wav", ".mp3")
    target_size_bytes = 25 * 1024 * 1024  # 25MB in bytes
    bitrate = 128  # Initial bitrate (kbps)

    while True:
        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(wav_path),
            "-vn",  # Disable video recording
            "-ar",
            "44100",  # Set audio sample rate
            "-ac",
            "1",  # Set number of audio channels
            "-b:a",
            f"{bitrate}k",  # Set audio bitrate
            "-f",
            "mp3",
            str(mp3_path),
        ]
        print(f"Executing command: {' '.join(command)}")

        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            file_size = os.path.getsize(mp3_path)
            print(f"Conversion successful. File size: {file_size / (1024 * 1024):.2f} MB")

            if file_size <= target_size_bytes:
                return mp3_path  # File size is within the limit
            else:
                bitrate -= 10  # Reduce bitrate and try again
                if bitrate < 64: 
                    print("Warning: Unable to reduce file size below 25MB with acceptable quality.")
                    return mp3_path 
                os.remove(mp3_path)  # Remove the large file before trying again

        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")
            return None  # Return None to indicate an error