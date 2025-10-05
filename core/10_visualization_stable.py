# AmritCore - MASTER BUILDER (Final Assembly and Export - TYPO FIXED)

# Install necessary libraries
!pip install moviepy gTTS pydub requests

from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_audioclips, CompositeAudioClip, vfx
from gtts import gTTS
from pydub import AudioSegment
from PIL import Image
import os

# --- Step 1: Setup and Data ---
final_video_filename = "AmritCore_FULL_LAUNCH_FINAL.mp4"

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


# B. Audio Node: Generate Dialogue & Effects
for i, dialogue in enumerate(dialogues_scene1):
    tts = gTTS(dialogue["text"], lang='pa')
    tts.save(f"audio/dialogue_{i}.mp3") # File is created as .mp3

background_fx_path = "audio/birds.mp3"
AudioSegment.silent(duration=4000).export(background_fx_path, format="mp3") # SFX Placeholder


# --- Step 2: Animation & Final Assembly ---
movement_clip_path = "assets/animation/movement_clip.mp4"
clip1 = ImageClip(AI_IMAGE_PATH).set_duration(1.5).set_fps(24)
clip1.fx(vfx.fadein, 0.5).write_videofile(movement_clip_path, audio_codec='aac', verbose=False, logger=None)

# Load Dialogue (FIX APPLIED HERE: using .mp3)
dialogue_clips = [
    AudioFileClip(f"audio/dialogue_0.mp3").volumex(1.0),
    AudioFileClip(f"audio/dialogue_1.mp3").volumex(0.8), 
    AudioFileClip(f"audio/dialogue_2.mp3").volumex(1.0)
]

final_dialogue_audio = concatenate_audioclips(dialogue_clips)
total_duration = final_dialogue_audio.duration

# Final Audio Mix
background_audio_clip = AudioFileClip(background_fx_path)
background_audio = background_audio_clip.fx(vfx.loop, duration=total_duration).volumex(0.15) 
final_audio_mix = CompositeAudioClip([final_dialogue_audio, background_audio])

# Final Video Output
video_clip_final = VideoFileClip(movement_clip_path).set_duration(total_duration)
final_video_clip = video_clip_final.set_audio(final_audio_mix)

final_video_clip.write_videofile(final_video_filename, fps=24, audio_codec='aac', verbose=False, logger=None)

print("\n\n--- AMRIT CORE MASTER BUILDER STATUS: SUCCESS ---")
print("The final, fully assembled demonstration video has been created!")
print(f"Find the file: {final_video_filename}")

