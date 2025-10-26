# AmritCore - MASTER BUILDER (Final Assembly and Export - LIST INITIALIZATION FIX)

# Install necessary libraries
#!pip install moviepy==1.0.3 gTTS requests pillow numpy

from moviepy.editor import *  # Using the simpler import style
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.fadein import fadein
from gtts import gTTS
from PIL import Image
import wave
import numpy as np
import os

# --- Step 1: Setup and Data ---
final_video_filename = "AmritCore_FINAL_STUDIO_LAUNCH.mp4"

# Create necessary folders (ensures stability)
if not os.path.exists("audio"): os.makedirs("audio")
if not os.path.exists("images"): os.makedirs("images")
if not os.path.exists("assets/animation"): os.makedirs("assets/animation")

# Dialogue Data (for audio consistency)
dialogues_scene1 = [
    {"character": "Krishna", "text": "ਸੁਲਤਾਨਾ, ਕਦੇ ਸੋਚਿਆ ਈ, ਆਪਾਂ ਵੀ ਕਦੀ ਸ਼ਹਿਰ ਜਾਈਏ?", "volume": 1.0},
    {"character": "Sultan", "text": "ਕ੍ਰਿਸ਼ਨਾ, ਮੈਂ ਤਾਂ ਏਸੇ ਪਿੰਡ ਵਿੱਚ ਖੁਸ਼ ਆਂ। ਬਸ ਰੱਬ ਸੁੱਖ ਰੱਖੇ, ਆਪਣੀ ਦੋਸਤੀ ਕਾਇਮ ਰਹੇ।", "volume": 0.8},
    {"character": "Krishna", "text": "ਰੱਬ ਜ਼ਰੂਰ ਸੁੱਖ ਰੱਖੇਗਾ। ਆਹ ਤੂਤਾਂ ਵਾਲਾ ਖੂਹ ਹਮੇਸ਼ਾ ਆਪਣੀ ਦੋਸਤੀ ਦਾ ਗਵਾਹ ਰਹੇਗਾ।", "volume": 1.0}
]

# A. Visual Node: Create Scene Base Image
SCENE_COLOR = "#434657" 
AI_IMAGE_PATH = "images/scene_base.png"
Image.new('RGB', (1920, 1080), color=SCENE_COLOR).save(AI_IMAGE_PATH)


# --- Step 2: Audio Generation and Combining (The FINAL FIX is in the loop) ---
# Create empty list to store audio clips (THE FIX)
audio_clips = []

for i, dialogue in enumerate(dialogues_scene1):
    tts = gTTS(dialogue["text"], lang='pa')
    tts.save(f"audio/dialogue_{i}.mp3") # Save the file
    
    # Load the clip and add volume
    clip = AudioFileClip(f"audio/dialogue_{i}.mp3")
    clip = volumex(clip, dialogue['volume'])  # Use the volumex effect
    audio_clips.append(clip) # Now audio_clips is defined!

final_dialogue_audio = concatenate_audioclips(audio_clips)
total_duration = final_dialogue_audio.duration

# Create SFX (for background)
background_fx_path = "audio/birds.mp3"
# Create silent audio using numpy
sample_rate = 44100
duration = 4.0  # 4 seconds
samples = np.zeros(int(duration * sample_rate))

# Save as WAV file
with wave.open(background_fx_path, 'wb') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sample_rate)
    f.writeframes((samples * 32767).astype(np.int16).tobytes())

background_audio_clip = AudioFileClip(background_fx_path)

# --- Step 3: Final Assembly ---
movement_clip_path = "assets/animation/movement_clip.mp4"
clip1 = ImageClip(AI_IMAGE_PATH).set_duration(1.5).set_fps(24)
clip1 = fadein(clip1, 0.5)  # Use the fadein effect directly
clip1.write_videofile(movement_clip_path, audio_codec='aac', verbose=False, logger=None)

background_audio = volumex(audio_loop(background_audio_clip, duration=total_duration), 0.15)  # Use audio_loop and volumex
final_audio_mix = CompositeAudioClip([final_dialogue_audio, background_audio])

video_clip_final = VideoFileClip(movement_clip_path).set_duration(total_duration)
final_video_clip = video_clip_final.set_audio(final_audio_mix)

final_video_clip.write_videofile(final_video_filename, fps=24, audio_codec='aac', verbose=False, logger=None)

print("\n\n--- AMRIT CORE MASTER BUILDER STATUS: LAUNCH SUCCESS ---")
print("The final, fully assembled demonstration video has been created!")
print(f"Find the file: {final_video_filename}")
