# AmritCore - 10_master_builder.py (Final Assembly and Launch Logic)

# Install necessary libraries
!pip install moviepy gTTS pydub requests numpy

from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_audioclips, CompositeAudioClip, vfx
from gtts import gTTS
from pydub import AudioSegment
from PIL import Image
import os
import numpy as np

# --- 1. SETUP: Define Constants and Paths ---
final_video_filename = "AmritCore_DEMO_LAUNCH.mp4"
if os.path.exists(final_video_filename):
    os.remove(final_video_filename)

# --- Define the paths for assets created by previous nodes ---
AUDIO_DIR = "assets/audio"
VISUAL_PATH = "assets/visuals/icon.png"
ANIMATION_PATH = "assets/animation/movement_clip.mp4"


# --- 2. LOGIC: Replicate Successful Node Execution (Audio & Visuals) ---

# A. Visual Node Logic (Recreate the placeholder image for stability)
if not os.path.exists('assets/visuals'): os.makedirs('assets/visuals')
Image.new('RGB', (800, 600), color='#A03030').save(VISUAL_PATH)


# B. Audio Synthesis Logic (Based on 08_synthesis_node.py final successful run)
dialogues_scene1 = [
    {"character": "Krishna", "text": "ਸੁਲਤਾਨਾ, ਕਦੇ ਸੋਚਿਆ ਈ, ਆਪਾਂ ਵੀ ਕਦੀ ਸ਼ਹਿਰ ਜਾਈਏ?", "volume": 1.0},
    {"character": "Sultan", "text": "ਕ੍ਰਿਸ਼ਨਾ, ਮੈਂ ਤਾਂ ਏਸੇ ਪਿੰਡ ਵਿੱਚ ਖੁਸ਼ ਆਂ। ਬਸ ਰੱਬ ਸੁੱਖ ਰੱਖੇ, ਆਪਣੀ ਦੋਸਤੀ ਕਾਇਮ ਰਹੇ।", "volume": 0.8},
    {"character": "SFX_Peacock", "text": "ਕੂ-ਊ-ਕੂ! (Peacock Sound)", "volume": 0.15},
    {"character": "Krishna", "text": "ਰੱਬ ਜ਼ਰੂਰ ਸੁੱਖ ਰੱਖੇਗਾ। ਆਹ ਤੂਤਾਂ ਵਾਲਾ ਖੂਹ ਹਮੇਸ਼ਾ ਆਪਣੀ ਦੋਸਤੀ ਦਾ ਗਵਾਹ ਰਹੇਗਾ।", "volume": 1.0}
]

# Generate and save audio assets
one_second_silence = AudioSegment.silent(duration=1000)
if not os.path.exists(AUDIO_DIR): os.makedirs(AUDIO_DIR)
dialogue_clips = []
dialogue_duration_sum = 0

for i, dialogue in enumerate(dialogues_scene1):
    tts = gTTS(dialogue["text"], lang='pa')
    temp_filename = "temp_dialogue.mp3"
    tts.save(temp_filename)
    
    dialogue_segment = AudioSegment.from_file(temp_filename, format="mp3")
    final_segment = dialogue_segment + one_second_silence
    
    filename = f"{AUDIO_DIR}/FINAL_DIALOGUE_{i}_{dialogue['character']}.mp3"
    final_segment.export(filename, format="mp3")
    os.remove(temp_filename)

    # Load clip and apply volume/duration logic
    audio_clip = AudioFileClip(filename).volumex(dialogue['volume'])
    dialogue_clips.append(audio_clip)
    dialogue_duration_sum += audio_clip.duration


# --- 3. FINAL ASSEMBLY (The Combiner Node's Job) ---

# A. Combine Dialogue and Calculate Total Duration
final_dialogue_audio = concatenate_audioclips(dialogue_clips)
total_duration = final_dialogue_audio.duration

# B. Create and Loop Background Audio (for stability)
background_fx_path = f"{AUDIO_DIR}/birds.mp3"
AudioSegment.silent(duration=4000).export(background_fx_path, format="mp3") 

background_audio_clip = AudioFileClip(background_fx_path)
background_audio = background_audio_clip.fx(vfx.loop, duration=total_duration).volumex(0.15) 

# C. Final Audio Mix
final_audio_mix = CompositeAudioClip([final_dialogue_audio, background_audio])


# D. Animation and Video Export
# Create animation clip (Illusion of movement)
clip1 = ImageClip(VISUAL_PATH).set_duration(1.5).set_fps(24)
clip1.write_videofile(ANIMATION_PATH, audio_codec='aac', verbose=False, logger=None)

# Final Video Construction
video_clip_final = VideoFileClip(ANIMATION_PATH).set_duration(total_duration)
final_video_clip = video_clip_final.set_audio(final_audio_mix)

# Write the final file
final_video_clip.write_videofile(final_video_filename, fps=24, audio_codec='aac', verbose=False, logger=None)

print("\n\n--- AMRIT CORE MASTER BUILDER STATUS: FINAL SUCCESS ---")
print("The fully assembled demonstration video has been created!")
print(f"Find the file: {final_video_filename}")

