# AmritCore - 08_synthesis_node.py (Final Fix for .mpex3 Typo)

# Install necessary libraries
!pip install moviepy gTTS pydub numpy

import os
from moviepy.editor import AudioFileClip, CompositeAudioClip, vfx, concatenate_audioclips
from gtts import gTTS
from pydub import AudioSegment
import numpy as np

# --- 1. Load Data from the 'Bariki Brain' ---
def get_scene_bariki():
    """Returns the complete, detailed data structure from the Thinking Node."""
    return {
        "scene_id": "SCENE_1_THE_WELL",
        "audio_layers": {
            "music_mood": "Affectionate and melancholic flute melody",
            "sfx_1_primary": "Peacock crying in the distance",
            "sfx_2_secondary": "Rustling of dry leaves and gentle wind",
            "sfx_3_tertiary": "Sound of the well bucket dropping and rope creaking"
        },
        "dialogue_flow": [
            {"character": "Krishna", "emotion": "Calmness", "volume": 1.0, "text": "ਸੁਲਤਾਨਾ, ਕਦੇ ਸੋਚਿਆ ਈ, ਆਪਾਂ ਵੀ ਕਦੀ ਸ਼ਹਿਰ ਜਾਈਏ?"},
            {"character": "Sultan", "emotion": "Doubt", "volume": 0.8, "text": "ਸ਼ਹਿਰ? ਕੀ ਹੋ ਗਿਆ? ਮੈਂ ਤਾਂ ਇੱਥੇ ਖੇਤਾਂ ਵਿੱਚ ਖੁਸ਼ ਆਂ।"},
            {"character": "Krishna", "emotion": "Hope", "volume": 1.0, "text": "ਕੁਝ ਵੱਡਾ ਕਰਨਾ ਚਾਹੁੰਦਾ ਹਾਂ। ਮੇਰੇ ਅੰਦਰ ਬਹੁਤ ਹੌਸਲਾ ਹੈ।"},
            {"character": "Sultan", "emotion": "Affection", "volume": 0.8, "text": "ਠੀਕ ਹੈ, ਕ੍ਰਿਸ਼ਨਾ। ਆਪਣੀ ਹਿੰਮਤ ਨਾ ਹਾਰੀਂ। ਸਾਡੀ ਦੋਸਤੀ ਹਮੇਸ਼ਾ ਤੇਰੇ ਨਾਲ ਰਹੇਗੀ।"}
        ]
    }
scene_data = get_scene_bariki()
audio_dir = "assets/audio/scene_1"
if not os.path.exists(audio_dir): os.makedirs(audio_dir)


# --- 2. AUDIO GENERATION AND LAYERING ---
print("--- Synthesis Node: Generating Dialogue and SFX Assets ---")

# 2.1 Generate Dialogue (Stable gTTS)
dialogue_clips_paths = []
for i, item in enumerate(scene_data["dialogue_flow"]):
    tts = gTTS(item["text"], lang='pa')
    filename = f"{audio_dir}/dialogue_{item['character']}_{i}.mp3"
    tts.save(filename)
    dialogue_clips_paths.append(filename)
    print(f"Generated dialogue: {filename}")
        
# 2.2 Generate SFX Placeholders
sfx_duration = 20000 
AudioSegment.silent(duration=sfx_duration).export(f"{audio_dir}/peacock_fx.mp3", format="mp3")
AudioSegment.silent(duration=sfx_duration).export(f"{audio_dir}/wind_rustle_fx.mp3", format="mp3")
AudioSegment.silent(duration=15000).export(f"{audio_dir}/music_flute.mp3", format="mp3")
print("SFX placeholders created.")


# --- 3. FINAL MIX (Incorporating Volume and Layers) ---
# Load all generated clips with character-specific volume (FIXED: Using .mp3)
dialogue_clips = []
for i, item in enumerate(scene_data["dialogue_flow"]):
    # CORRECT LOADING OF MP3 FILE
    clip = AudioFileClip(f"{audio_dir}/dialogue_{item['character']}_{i}.mp3")
    dialogue_clips.append(clip.volumex(item['volume']))

final_dialogue_track = concatenate_audioclips(dialogue_clips)
total_duration = final_dialogue_track.duration

# Load SFX and BGM (Low Volume Layers)
peacock_fx = AudioFileClip(f"{audio_dir}/peacock_fx.mp3").fx(vfx.loop, duration=total_duration).volumex(0.12)
wind_rustle_fx = AudioFileClip(f"{audio_dir}/wind_rustle_fx.mp3").fx(vfx.loop, duration=total_duration).volumex(0.08)

# Composite Audio Layers: [Dialogue, Wind/Rustle, Peacock]
final_audio_mix = CompositeAudioClip([final_dialogue_track, wind_rustle_fx, peacock_fx])
final_audio_mix = final_audio_mix.set_duration(total_duration)


print("\nSynthesis Node Status: SUCCESS.")
print(f"Total audio layers mixed: 3 (Dialogue, Wind/Rustle, Peacock). Total duration: {total_duration:.2f} seconds.")
print("The ultimate sound studio is ready for the Combiner Node!")
