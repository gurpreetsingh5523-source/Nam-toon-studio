from moviepy.editor import AudioFileClip, concatenate_audioclips, CompositeAudioClip
from gtts import gTTS
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - Audio Agent - %(message)s')

# --- 1. Story Data and Tone (Your Input Logic) ---
def get_narration_script():
    """Returns the provided story text."""
    # We are using the gentle, loving tone script provided by you.
    return [
        "ਇੱਕ ਛੋਟੇ ਪਿੰਡ ਵਿੱਚ… ਜਿੱਥੇ ਤੂਤਾਂ ਦੇ ਦਰੱਖ਼ਤ ਹਵਾ ਨਾਲ ਗੁੰਗੁਨਾਉਂਦੇ, ਅਤੇ ਪੰਛੀ ਸਵੇਰ ਦਾ ਸੁਰ ਮੇਲਦੇ,",
        "ਉੱਥੇ ਬੱਚਿਆਂ ਦੀਆਂ ਹਾਸੀਆਂ ਹੀ ਸਭ ਤੋਂ ਵੱਡੀ ਰੌਣਕ ਸੀ।",
        "ਪਿੰਡ ਦੇ ਵਿਚਕਾਰ ਇੱਕ ਪੁਰਾਣਾ ਖੂਹ ਸੀ।",
        "ਖੂਹ ਦੇ ਨੇੜੇ… ਬੱਚੇ ਹੱਥ ਫੜ ਕੇ ਖੇਡਦੇ, ਕਦੇ ਕੰਗਣ ਦੀਆਂ ਛਣਕਾਂ, ਕਦੇ ਪੈਰਾਂ ਦੀਆਂ ਝੰਕਾਰਾਂ — ਜੀਵਨ ਦੀ ਧੁਨ ਵਾਂਗ ਗੂੰਜਦੀਆਂ ਸਨ।",
        "ਅੱਜ ਦੀ ਕਹਾਣੀ ਉਸੇ ਖੂਹ ਨਾਲ ਜੁੜੀ ਹੈ… ਜਿੱਥੇ ਪਾਣੀ ਸਿਰਫ ਤ੍ਰਿਸ਼ਨਾ ਨਹੀਂ ਮਿਟਾਉਂਦਾ, ਸਗੋਂ ਦਿਲਾਂ ਨੂੰ ਵੀ ਜੋੜਦਾ ਹੈ।"
    ]

# --- 2. THE AUDIO SYNTHESIS & MIXING CORE (03_audio_node logic) ---
def synthesize_and_mix_narration():
    narration_script = get_narration_script()
    
    if not os.path.exists("temp_audio"): os.makedirs("temp_audio")
    
    all_audio_clips = []
    
    # Generate Narrator Voice Clips
    logging.info("Starting G-TTS synthesis for Narration voice (Sweet Tone)...")
    
    for i, line in enumerate(narration_script):
        # Using Punjabi ('pa') language
        tts = gTTS(line, lang='pa')
        temp_path = f"temp_audio/narration_{i}.mp3"
        tts.save(temp_path)
        
        # Load the clip and reduce the volume slightly for a 'gentle, loving voice'
        clip = AudioFileClip(temp_path).volumex(0.9) 
        all_audio_clips.append(clip)
        logging.info(f"Generated Clip {i}: {len(line)} chars.")

    # 3. Create Final Narration Track
    narration_track = concatenate_audioclips(all_audio_clips)
    total_duration = narration_track.duration
    
    # 4. Background Sound Logic (The Tambura and Birds Logic)
    # We will simulate the perfect 198Hz Tanpura/Bird sound file creation here
    
    # NOTE: You need to manually provide a 'tanpura_bg.mp3' file in the 'temp_audio' folder 
    # for a real output. For now, we simulate.
    try:
        # Assuming tanpura_bg.mp3 is available and looped to match total_duration
        bg_track = AudioFileClip("temp_audio/tanpura_bg.mp3").set_duration(total_duration).volumex(0.15)
        
        # 5. Final Composite Mix (Combining the tracks)
        final_audio_mix = CompositeAudioClip([narration_track, bg_track])
    
    except Exception as e:
        logging.warning(f"Background Audio Mix Error: {e}. Exporting Narrator Only.")
        final_audio_mix = narration_track
        
    # 6. Export the Final Voice Clip
    final_output_path = "NaamToon_First_Story_Narrator.mp3"
    final_audio_mix.write_audiofile(final_output_path, fps=44100, logger=None)

    logging.info("==============================================")
    logging.info(f"SUCCESS: Final Narration Audio is ready: {final_output_path}")
    logging.info(f"Total Duration: {round(total_duration, 2)} seconds.")
    logging.info("==============================================")


# --- EXECUTE THE AUDIO AGENT ---
if __name__ == "__main__":
    synthesize_and_mix_narration()
