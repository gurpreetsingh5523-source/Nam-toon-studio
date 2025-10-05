 # AmritCore - VISUALIZATION NODE (FINAL FIX: Installing ImageMagick)

# --- THE CRITICAL FIX: INSTALLING THE MISSING DEPENDENCY ---
!apt-get install imagemagick -y 

# Install necessary stable libraries
!pip install moviepy gTTS pydub requests

from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_audioclips, CompositeAudioClip, vfx, TextClip, CompositeVideoClip
from gtts import gTTS
from pydub import AudioSegment
from PIL import Image
import os


# --- Step 1: Audio Generation and Timing (The Core Logic) ---

# Dialogue Data
dialogues_scene1 = [
    {"character": "Krishna", "emotion": "Calmness", "text": "ਸੁਲਤਾਨਾ, ਕਦੇ ਸੋਚਿਆ ਈ, ਆਪਾਂ ਵੀ ਕਦੀ ਸ਼ਹਿਰ ਜਾਈਏ?", "volume": 1.0},
    {"character": "Sultan", "emotion": "Doubt", "text": "ਸ਼ਹਿਰ? ਕੀ ਹੋ ਗਿਆ? ਮੈਂ ਤਾਂ ਇੱਥੇ ਖੇਤਾਂ ਵਿੱਚ ਖੁਸ਼ ਆਂ।", "volume": 0.8},
    {"character": "Krishna", "emotion": "Hope", "text": "ਕੁਝ ਵੱਡਾ ਕਰਨਾ ਚਾਹੁੰਦਾ ਹਾਂ। ਮੇਰੇ ਅੰਦਰ ਬਹੁਤ ਹੌਸਲਾ ਹੈ।", "volume": 1.0}
]

# Create all necessary assets and calculate timing
if not os.path.exists("audio"): os.makedirs("audio")
if not os.path.exists("images"): os.makedirs("images")
if not os.path.exists("assets/animation"): os.makedirs("assets/animation")

# Generate dialogue audio and calculate durations
audio_clips = []
for i, dialogue in enumerate(dialogues_scene1):
    tts = gTTS(dialogue["text"], lang='pa')
    tts.save(f"audio/dialogue_{i}.mp3")
    
    audio_clip = AudioFileClip(f"audio/dialogue_{i}.mp3").volumex(dialogue['volume'])
    audio_clips.append(audio_clip)

final_dialogue_audio = concatenate_audioclips(audio_clips)
total_duration = final_dialogue_audio.duration


# --- Step 2: Visual and Text Compositing ---
final_video_filename = "AmritCore_Dialogue_Visualized.mp4"

# Create Scene Base (The background)
SCENE_COLOR = "#33404D" 
Image.new('RGB', (1920, 1080), color=SCENE_COLOR).save("images/scene_base.png")
video_clip_base = ImageClip("images/scene_base.png").set_duration(total_duration).set_fps(24)

# Create Text Overlays (The Brain's Visualization)
text_clips = []
current_start = 0.0

for dialogue_info in dialogues_scene1:
    # Find the duration of the corresponding audio clip
    clip_duration = AudioFileClip(f"audio/dialogue_{dialogues_scene1.index(dialogue_info)}.mp3").duration
    
    # Create the text overlay: [Character Name] (Emotion)
    text_content = f"[{dialogue_info['character']}] ({dialogue_info['emotion']})"
    
    # Create the TextClip (ImageMagick is needed here)
    txt_clip = TextClip(text_content, fontsize=60, color='white', bg_color='black', font='Arial-Bold')
    txt_clip = txt_clip.set_duration(clip_duration)
    txt_clip = txt_clip.set_pos(('center', 'top')).set_start(current_start)
    
    text_clips.append(txt_clip)
    current_start += clip_duration # Advance the time for the next text block


# --- Step 3: Final Assembly and Export ---
final_audio_mix = final_dialogue_audio # Using dialogue only for testing stability

# Final Compositing: Base image + Dialogue Text Overlays
final_video_clip = CompositeVideoClip([video_clip_base] + text_clips)
final_video_clip = final_video_clip.set_audio(final_audio_mix)

final_video_clip.write_videofile(final_video_filename, fps=24, audio_codec='aac', verbose=False, logger=None)

print("\n\n--- AMRIT CORE VISUALIZATION STATUS: SUCCESS ---")
print("The studio is now displaying the Brain's creative output (Dialogue and Emotion tags)!")
print(f"Find the file: {final_video_filename}")
