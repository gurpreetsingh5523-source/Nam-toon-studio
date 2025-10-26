# AmritCore - 20_ultimate_master_builder.py (FIXED FOR CompositeAudioClip ERROR)

# Install necessary stable libraries
!pip install moviepy gTTS pydub numpy requests

from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_audioclips, CompositeAudioClip, vfx
from gtts import gTTS
from pydub import AudioSegment
from PIL import Image
import os
import json


# --- 1. THE ULTIMATE BRAIN: STORY ANALYSIS (Integrated) ---

def get_full_story_analysis():
    # Simulating a successful complex analysis into the final structured output:
    structured_output = {
        "title": "Tootan Wala Khooh - The Journey Begins",
        "scenes": [
            {
                "scene_id": "SCENE_1_MEETING",
                "color_code": "#A4742C", 
                "dialogues": [
                    {"character": "Krishna", "emotion": "Calmness", "volume": 1.0, "text": "ਸੁਲਤਾਨਾ, ਕਦੇ ਸੋਚਿਆ ਈ, ਆਪਾਂ ਵੀ ਕਦੀ ਸ਼ਹਿਰ ਜਾਈਏ?"},
                    {"character": "Sultan", "emotion": "Doubt", "volume": 0.7, "text": "ਸ਼ਹਿਰ? ਕੀ ਹੋ ਗਿਆ? ਮੈਂ ਤਾਂ ਇੱਥੇ ਖੇਤਾਂ ਵਿੱਚ ਖੁਸ਼ ਆਂ।"},
                    {"character": "Krishna", "emotion": "Hope", "volume": 1.0, "text": "ਕੁਝ ਵੱਡਾ ਕਰਨਾ ਚਾਹੁੰਦਾ ਹਾਂ। ਮੇਰੇ ਅੰਦਰ ਬਹੁਤ ਹੌਸਲਾ ਹੈ।"},
                    {"character": "SFX_Primary", "emotion": "Ambient", "volume": 0.15, "text": "ਕੂ-ਊ-ਕੂ! (Peacock call, for SFX mixing)"} 
                ]
            }
        ]
    }
    return structured_output


# --- 2. SYNTHESIS NODE & MASTER BUILDER LOGIC ---

def master_build():
    final_video_filename = "AmritCore_V3_Launch_Demo.mp4"
    
    # A. Get Data
    story_data = get_full_story_analysis()
    scene_data = story_data['scenes'][0]
    
    # B. Generate Audio Assets
    if not os.path.exists("audio"): os.makedirs("audio")
    dialogue_clips = []
    
    for i, item in enumerate(scene_data["dialogues"]):
        tts = gTTS(item["text"], lang='pa')
        temp_filename = f"temp_dialogue_{i}.mp3"
        tts.save(temp_filename) 

        clip = AudioFileClip(temp_filename).volumex(item['volume'])
        
        # We need the AudioFileClip objects to combine them
        dialogue_clips.append(clip) 
        os.remove(temp_filename)

    final_dialogue_track = concatenate_audioclips(dialogue_clips)
    total_duration = final_dialogue_track.duration

    # C. Create Visual and Animation (ImageClip and simple movement)
    final_image_path = "final_scene_visual.png"
    Image.new('RGB', (1920, 1080), color=scene_data['color_code']).save(final_image_path)
    
    # The simple animation logic
    video_clip_base = ImageClip(final_image_path).set_duration(total_duration)
    
    # D. Final Audio Mix (Composite)
    # Background SFX Placeholder
    flute_bg_path = "flute_432hz_bg.mp3"
    AudioSegment.silent(duration=total_duration * 1000).export(flute_bg_path, format="mp3")
    background_audio = AudioFileClip(flute_bg_path).volumex(0.05) 

    final_audio_mix = CompositeAudioClip([final_dialogue_track, background_audio])

    # E. Final Assembly and Export (THE FIX IS HERE)
    
    # 1. Video and Audio are joined together using the video clip
    final_video_clip = video_clip_base.set_audio(final_audio_mix)
    
    # 2. Write the video file (This correctly uses the video clip's write_videofile method)
    final_video_clip.write_videofile(final_video_filename, fps=24, audio_codec='aac', verbose=False, logger=None)

    print("\n\n--- AMRIT CORE V3 LAUNCH COMPLETE ---")
    print(f"The ultimate demo video is ready: {final_video_filename}")

# --- EXECUTE THE MASTER BUILD ---
master_build()
