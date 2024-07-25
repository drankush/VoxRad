import sounddevice as sd
import threading
import time
import numpy as np
import soundfile as sf
import os
import subprocess
from config.config import config  
from audio.transcriber import transcribe_audio
from ui.utils import update_status, simulate_waveform, draw_straight_line, stop_waveform_simulation, start_waveform_simulation

# Global variables
recording = False
paused = False  # Add paused flag
audio_data = []  # Use a list to collect chunks
start_time = None
recording_thread = None
pause_event = threading.Event()

def record_audio():
    """Starts audio recording after checking for Groq API key."""
    global recording, recording_thread, audio_data
    print(f"GROQ API Key from recorder.py: {config.GROQ_API_KEY}")
    if config.GROQ_API_KEY is None:
        update_status("Please set your Transcription and Text Model API keys in settings.")
        return
    recording = True
    paused = False
    audio_data = []  # Reset audio data
    from ui.main_window import record_button, stop_button, pause_button, canvas, root  # Import additional global variables
    record_button['state'] = 'disabled'
    stop_button['state'] = 'normal'
    pause_button['state'] = 'normal'  # Enable pause button
    recording_thread = threading.Thread(target=background_recording, daemon=True)
    recording_thread.start()
    update_status("Recording 🔴")
    start_waveform_simulation(canvas, root)  # Start simulating the waveform

def pause_audio():
    global paused, pause_event
    from ui.main_window import record_button, stop_button, pause_button, canvas, root  # Import additional global variables
    if not paused:
        paused = True
        pause_event.clear()
        pause_button.config(text="Resume")
        record_button['state'] = 'disabled'
        stop_button['state'] = 'disabled'
        update_status("Paused ⏸️")
        stop_waveform_simulation(canvas)  # Stop the waveform simulation
        draw_straight_line(canvas)  # Clear the waveform when paused
    else:
        paused = False
        pause_event.set()
        pause_button.config(text="Pause")
        record_button['state'] = 'disabled'
        stop_button['state'] = 'normal'
        update_status("Recording 🔴")
        start_waveform_simulation(canvas, root)  # Resume waveform simulation

def background_recording():
    global audio_data, start_time, recording, paused, pause_event
    fs = 44100  # Sample rate
    start_time = time.time()

    try:
        # Prepare recording stream
        stream = sd.InputStream(samplerate=fs, channels=1, dtype='float32')
        stream.start()
        print("Recording started...")

        loop_counter = 0  # To count the number of iterations (chunks recorded)

        # Record as long as recording is True
        while recording:
            if paused:
                pause_event.wait()  # Wait while paused
            data, overflowed = stream.read(fs)  # Read data for 1 second
            if overflowed:
                print("Audio buffer overflowed")
            audio_data.append(data)  # Collect chunks of audio data

            # Log the size of the current chunk and the iteration count
            print(f"Chunk {loop_counter}: shape={data.shape}, overflowed={overflowed}")
            loop_counter += 1

        # Stop and close the stream
        stream.stop()
        stream.close()
        print(f"Recording stopped. Total chunks recorded: {loop_counter}")

    except Exception as e:
        print(f"An error occurred during recording: {e}")

    if not recording:
        update_status("Started Processing...⚙️")

def stop_recording():
    global recording, audio_data, start_time, recording_thread
    print("stop_recording called")
    recording = False  # Signal to stop recording
    pause_event.set()  # Ensure any waiting pause_event is released
    from ui.main_window import pause_button, canvas  # Import additional global variables
    pause_button['state'] = 'disabled'  # Disable pause button
    stop_waveform_simulation(canvas)  # Stop the waveform simulation
    
    # Schedule a check to wait for the recording to finish non-blockingly
    from ui.main_window import root  # Import global variable
    root.after(100, check_recording_finished)

def check_recording_finished():
    global recording_thread
    print("check_recording_finished called")
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
    print("Before draw_straight_line(canvas)")
    draw_straight_line(canvas)
    print("After draw_straight_line(canvas)")

    fs = 44100  # Sample rate used for recording
    if audio_data:
        wav_path = save_audio_as_wav(np.vstack(audio_data), fs)
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
