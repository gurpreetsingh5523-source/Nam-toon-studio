# AmritCore - 20_ultimate_master_builder.py (Final Fix: Importing numpy)

# Install necessary stable libraries
!pip install moviepy gTTS pydub requests numpy imageio[ffmpeg]

from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_audioclips, CompositeAudioClip, vfx
from gtts import gTTS
from pydub import AudioSegment
from PIL import Image
import os
import json
import imageio
import numpy as np # <--- THE FIX IS HERE: Importing numpy as np


# --- 1. DATA AND SETUP ---
final_video_filename = "AmritCore_V4_FINAL_LAUNCH.mp4"
if os.path.exists(final_video_filename): os.remove(final_video_filename)

if not os.path.exists("audio"): os.makedirs("audio")
if not os.path.exists("images"): os.makedirs("images")
if not os.path.exists("assets/animation"): os.makedirs("assets/animation")

# Dialogue Data (for audio consistency)
MASTER_DATA = {
    "color_code": "#A4742C", 
    "dialogues": [
        {"character": "Krishna", "text": "ਸੁਲਤਾਨਾ, ਕਦੇ ਸੋਚਿਆ ਈ, ਆਪਾਂ ਵੀ ਕਦੀ ਸ਼ਹਿਰ ਜਾਈਏ?", "volume": 1.0},
        {"character": "Sultan", "text": "ਕ੍ਰਿਸ਼ਨਾ, ਮੈਂ ਤਾਂ ਏਸੇ ਪਿੰਡ ਵਿੱਚ ਖੁਸ਼ ਆਂ। ਬਸ ਰੱਬ ਸੁੱਖ ਰੱਖੇ, ਆਪਣੀ ਦੋਸਤੀ ਕਾਇਮ ਰਹੇ।", "volume": 0.8},
        {"character": "Krishna", "text": "ਰੱਬ ਜ਼ਰੂਰ ਸੁੱਖ ਰੱਖੇਗਾ। ਆਹ ਤੂਤਾਂ ਵਾਲਾ ਖੂਹ ਹਮੇਸ਼ਾ ਆਪਣੀ ਦੋਸਤੀ ਦਾ ਗਵਾਹ ਰਹੇਗਾ।", "volume": 1.0}
    ]
}


# --- HELPER: Create a temporary GIF to simulate Animation Logic ---
def create_animated_asset(path):
    """Creates a basic color-changing GIF to represent complex animation logic."""
    if os.path.exists(path): return path
    
    frames = []
    colors = ['#A4742C', '#70542C', '#A4742C'] # Simulating movement colors
    for color in colors:
        img = Image.new('RGB', (1920, 1080), color=color)
        frames.append(np.array(img)) # np.array is now defined
    
    imageio.mimsave(path, frames, fps=1) # Save as low-frame GIF
    return path


# --- Step 2: Audio Synthesis and Final Assembly ---

# A. Audio Generation (Dialogue & Mixing)
dialogue_clips = []
one_second_silence = AudioSegment.silent(duration=1000)

for i, dialogue in enumerate(MASTER_DATA['dialogues']):
    tts = gTTS(dialogue["text"], lang='pa')
    temp_filename = "temp_dialogue.mp3"
    tts.save(temp_filename)
    
    dialogue_segment = AudioSegment.from_file(temp_filename, format="mp3")
    final_segment = dialogue_segment + one_second_silence
    
    final_segment_path = f"audio/dialogue_{i}.mp3"
    final_segment.export(final_segment_path, format="mp3")
    os.remove(temp_filename)
    
    clip = AudioFileClip(final_segment_path).volumex(dialogue['volume'])
    dialogue_clips.append(clip)

final_dialogue_audio = concatenate_audioclips(dialogue_clips)
total_duration = final_dialogue_audio.duration

# Background SFX
background_fx_path = "audio/birds.mp3"
AudioSegment.silent(duration=4000).export(background_fx_path, format="mp3") 
background_audio_clip = AudioFileClip(background_fx_path)
background_audio = background_audio_clip.fx(vfx.loop, duration=total_duration).volumex(0.15) 

final_audio_mix = CompositeAudioClip([final_dialogue_audio, background_audio])


# --- 3. MASTER BUILDER: FINAL ASSEMBLY ---

# A. Create and load the animated asset
animated_gif_path = "assets/animation/animated_scene.gif"
create_animated_asset(animated_gif_path) # Now successfully creates the asset

# B. Video Assembly
video_clip_final = VideoFileClip(animated_gif_path).set_duration(total_duration)
final_video_clip = video_clip_final.set_audio(final_audio_mix)


# C. Final Export
final_video_clip.write_videofile(final_video_filename, fps=24, audio_codec='aac', verbose=False, logger=None)

print("\n\n--- AMRIT CORE V4 FINAL LAUNCH STATUS: SUCCESS ---")
print("The final, fully assembled demonstration video has been created!")
print(f"Find the file: {final_video_filename}")
