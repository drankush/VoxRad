import sounddevice as sd
import threading
import time
import numpy as np
import soundfile as sf
import os
import sys
import subprocess
import tempfile
from cryptography.fernet import Fernet
import wave
from config.config import config
from audio.transcriber import transcribe_audio, mm_gemini
from ui.utils import update_status, draw_straight_line, stop_waveform_simulation, start_waveform_simulation

# Global variables
recording = False
paused = False
audio_data = []
start_time = None
recording_thread = None
pause_event = threading.Event()


def record_audio():
    """Starts audio recording with encryption."""
    global recording, recording_thread, audio_data

    # Check for API keys
    if config.multimodal_pref and config.MM_API_KEY is None:
        update_status("Please Save/Unlock your Multimodal Model API key in Settings.")
        return
    if not config.multimodal_pref and (config.TRANSCRIPTION_API_KEY is None or config.TEXT_API_KEY is None):
        update_status("Please Save/Unlock your Transcription and Text Model API keys in Settings.")
        return

    recording = True
    paused = False
    audio_data = []
    config.current_encryption_key = None  # Reset in config
    config.current_encrypted_mp3_path = None  # Reset in config

    from ui.main_window import record_button, stop_button, pause_button, canvas
    record_button['state'] = 'disabled'
    stop_button['state'] = 'normal'
    pause_button['state'] = 'normal'

    if config.audio_device is None:
        update_status("Please select an audio device in settings.")
        return

    device_index = next((i for i, device in enumerate(sd.query_devices()) if device['name'] == config.audio_device), None)
    if device_index is None:
        update_status("Selected audio device not found. Please check settings.")
        return

    recording_thread = threading.Thread(target=background_recording, args=(device_index,), daemon=True)
    recording_thread.start()
    update_status("Recording 🔴")
        # Initialize secure paste
    start_waveform_simulation(canvas, config.root)

def pause_audio():
    global paused, pause_event
    from ui.main_window import record_button, stop_button, pause_button, canvas
    if not paused:
        paused = True
        pause_event.clear()
        pause_button.config(text="Resume")
        record_button['state'] = 'disabled'
        stop_button['state'] = 'disabled'
        update_status("Paused ⏸️")
        stop_waveform_simulation(canvas)
        draw_straight_line(canvas)
    else:
        paused = False
        pause_event.set()
        pause_button.config(text="Pause")
        record_button['state'] = 'disabled'
        stop_button['state'] = 'normal'
        update_status("Recording 🔴")
        start_waveform_simulation(canvas, config.root)

def background_recording(device_index=None):
    global audio_data, start_time, recording, paused, pause_event
    fs = 44100
    start_time = time.time()

    try:
        device_config = {'samplerate': fs, 'channels': 1, 'dtype': 'float32', 'device': device_index} if device_index is not None else {'samplerate': fs, 'channels': 1, 'dtype': 'float32'}
        with sd.InputStream(**device_config) as stream:
            print("Recording started...")
            loop_counter = 0
            while recording:
                if paused:
                    pause_event.wait()
                data, overflowed = stream.read(fs)
                if overflowed:
                    print("Audio buffer overflowed")
                audio_data.append(data)
                print(f"Chunk {loop_counter}: shape={data.shape}, overflowed={overflowed}")
                loop_counter += 1
            print(f"Recording stopped. Total chunks recorded: {loop_counter}")
    except Exception as e:
        print(f"An error occurred during recording: {e}")
    finally:
        if not recording:
            update_status("Started Processing...⚙️")

def stop_recording():
    global recording, audio_data, start_time, recording_thread
    print("stop_recording called")
    recording = False
    pause_event.set()
    from ui.main_window import pause_button, canvas
    pause_button['state'] = 'disabled'
    stop_waveform_simulation(canvas)
    config.root.after(100, check_recording_finished)

def check_recording_finished():
    global recording_thread
    print("check_recording_finished called")
    if recording_thread.is_alive():
        config.root.after(100, check_recording_finished)
    else:
        complete_stop_recording()

def complete_stop_recording():
    global audio_data, start_time, recording
    print("complete_stop_recording called")
    sd.stop()
    from ui.main_window import record_button, stop_button, canvas
    record_button['state'] = 'normal'
    stop_button['state'] = 'disabled'
    print("Before draw_straight_line(canvas)")
    draw_straight_line(canvas)
    print("After draw_straight_line(canvas)")

    fs = 44100
    if audio_data:
        wav_data = np.concatenate(audio_data, axis=0)
        # Assign to local variables first
        encrypted_mp3_path, encryption_key = convert_wav_to_encrypted_mp3(wav_data, fs)

        # Then explicitly update the config object
        config.current_encrypted_mp3_path = encrypted_mp3_path
        config.current_encryption_key = encryption_key

        print(config.current_encrypted_mp3_path)  # Now these should print correctly
        print(config.current_encryption_key)

        if config.current_encrypted_mp3_path:
            if config.multimodal_pref:
                config.root.after(100, lambda: mm_gemini(config.current_encrypted_mp3_path, config.current_encryption_key))
            else:
                config.root.after(100, lambda: transcribe_audio(config.current_encrypted_mp3_path, config.current_encryption_key))
        else:
            update_status("Error converting audio.")
    else:
        print("No audio data to process.")

def get_ffmpeg_path():
    """Return the path to the bundled ffmpeg executable, platform-aware."""
    if getattr(sys, 'frozen', False):
        base_dir_bundled = sys._MEIPASS
        ffmpeg_exec = 'ffmpeg.exe' if sys.platform == "win32" else 'ffmpeg'
        ffmpeg_path = os.path.join(base_dir_bundled, 'bin', 'ffmpeg', ffmpeg_exec)
    else:
        base_dir_dev = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ffmpeg_exec = 'ffmpeg.exe' if sys.platform == "win32" else 'ffmpeg'
        ffmpeg_path = os.path.join(base_dir_dev, 'bin', 'ffmpeg', ffmpeg_exec)

    if not os.path.exists(ffmpeg_path):
        print(f"FFmpeg not found at: {ffmpeg_path}")
        return None
    print(f"FFmpeg found at: {ffmpeg_path}")
    return ffmpeg_path

def convert_wav_to_encrypted_mp3(wav_data, fs):
    """Converts in-memory WAV data to an encrypted MP3 file."""
    ffmpeg_path = get_ffmpeg_path()
    if not ffmpeg_path:
        print("Error: FFmpeg not found.")
        return None, None

    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    temp_wav_path = None
    temp_enc_mp3_path = None

    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav_file:
            with wave.open(tmp_wav_file.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(fs)
                wf.writeframes((wav_data * 32767).astype(np.int16).tobytes())
            temp_wav_path = tmp_wav_file.name

        with tempfile.NamedTemporaryFile(suffix=".mp3.enc", delete=False) as tmp_enc_mp3_file:
            temp_enc_mp3_path = tmp_enc_mp3_file.name

        command = [
            ffmpeg_path,
            "-y",
            "-i", temp_wav_path,
            "-vn",
            "-ar", str(fs),
            "-ac", "1",
            "-b:a", "128k",
            "-f", "mp3",
            "-"  # Output to stdout
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        mp3_data, stderr = process.communicate()
        if process.returncode == 0:
            encrypted_mp3_data = cipher_suite.encrypt(mp3_data)
            with open(temp_enc_mp3_path, 'wb') as f:
                f.write(encrypted_mp3_data)
            print(f"Encrypted MP3 saved to {temp_enc_mp3_path}")
            return temp_enc_mp3_path, key
        else:
            print(f"FFmpeg conversion error: {stderr.decode()}")
            return None, None
    except Exception as e:
        print(f"Error during conversion or encryption: {e}")
        return None, None
    finally:
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)



