# AmritCore - 17_tts_generate.py (Stable Dialogue Generator - FINAL FIX)

# --- THE FIX: Installing the missing dependency ---
!pip install pyttsx3 numpy

import json
import os
import pyttsx3 # The stable, local Text-to-Speech library

def gen_wavs(segments_json_path, outdir="tts_out"):
    """Generates WAV files for dialogue segments using local TTS engine."""
    os.makedirs(outdir, exist_ok=True)
    engine = pyttsx3.init()
    
    # Setting the rate for Surti Pacing (as requested in previous logic)
    engine.setProperty('rate', 150) 
    
    try:
        with open(segments_json_path, "r", encoding="utf-8") as f:
            segs = json.load(f)
    except Exception as e:
        print(f"Error loading segment data: {e}")
        return

    for s in segs:
        # Assuming the JSON format has 'text' and 'id' fields
        fname = os.path.join(outdir, f"seg_{s['id']:03d}.wav")
        
        # Note: pyttsx3's functionality relies on your local OS, but the structure is correct.
        engine.save_to_file(s['text'], fname)
        engine.runAndWait()  # Blocking call to ensure file is saved
        print(f"Generated Dialogue: {fname}")

if __name__ == "__main__":
    # Example usage (This script needs to be called by the Master Builder)
    print("Dialogue Generator Node Loaded. Ready for Master Builder execution.")
