# AmritCore - 18_mix_ambience.py (Advanced Multi-Layer Mixer)

from pydub import AudioSegment
import os, sys, json

def mix_for_segment(seg_wav_path, ambience_folder, out_wav_path):
    """
    Mixes dialogue with ambient layers using volume gain control.
    """
    if not os.path.exists(seg_wav_path):
        print(f"Error: Dialogue file not found at {seg_wav_path}")
        return

    # Base dialogue track (slightly reduced volume to make room for SFX)
    base = AudioSegment.from_wav(seg_wav_path).apply_gain(-3)
    
    # Load and process ambient stems
    try:
        # Ensure the ambient tracks are looped to match the dialogue length
        leaves = AudioSegment.from_wav(os.path.join(ambience_folder,"leaves.wav")).loop()[:len(base)]
        engine = AudioSegment.from_wav(os.path.join(ambience_folder,"engine.wav")).loop()[:len(base)].apply_gain(-12) # Very low for engine drone
        well = AudioSegment.from_wav(os.path.join(ambience_folder,"well.wav")).loop()[:len(base)].apply_gain(-8) # Low ambient well sound
        
        # Overlay all layers: Dialogue is the primary track
        mixed = base.overlay(leaves).overlay(engine).overlay(well)
        
        mixed.export(out_wav_path, format="wav")
        print(f"Exported Final Mix: {out_wav_path}")

    except Exception as e:
        print(f"Mixing Error: Could not process ambient file. {e}")
        # Fallback: export dialogue only
        base.export(out_wav_path, format="wav")
        print("Exported Dialogue Only (Mix Failed).")


if __name__ == "__main__":
    # This script is designed to be called by the Master Builder with paths.
    # We will assume successful execution.
    print("Advanced Audio Mixer Node Loaded. Ready for Master Builder execution.")
