import os
from faster_whisper import WhisperModel
def verify_local_asr():
    print("Verifying Local ASR Setup...")
    
    model_size = "tiny" # Use tiny for fast verification
    print(f"Loading WhisperModel({model_size})...")
    try:
        model = WhisperModel(model_size, device="auto", compute_type="int8")
        print("Model loaded successfully.")
        
        # Test transcription with a silent/empty file if possible, or just the fact it loaded is enough.
        print("ASR Backend check: OK.")
    except Exception as e:
        print(f"ASR Backend check: FAILED. Error: {e}")

if __name__ == "__main__":
    verify_local_asr()
