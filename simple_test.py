"""
Simple Nam-toon Studio Test - Independent Video Generation
"""

import os
import json
from moviepy.editor import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
import tempfile

def create_simple_scene_image(text, emotion="neutral", scene_id=0):
    """Create a simple colored scene image with text"""
    
    # Different colors based on emotion
    colors = {
        "happy": [(255, 255, 150), (150, 255, 150)],  # Yellow-green
        "sad": [(150, 150, 255), (100, 100, 200)],    # Blue
        "neutral": [(200, 200, 200), (150, 150, 150)], # Gray
        "peaceful": [(150, 255, 200), (100, 200, 150)] # Light green
    }
    
    bg_colors = colors.get(emotion, colors["neutral"])
    
    # Create image
    img = Image.new('RGB', (1280, 720), bg_colors[0])
    draw = ImageDraw.Draw(img)
    
    # Add simple background gradient effect
    for y in range(720):
        ratio = y / 720
        r = int(bg_colors[0][0] * (1-ratio) + bg_colors[1][0] * ratio)
        g = int(bg_colors[0][1] * (1-ratio) + bg_colors[1][1] * ratio)
        b = int(bg_colors[0][2] * (1-ratio) + bg_colors[1][2] * ratio)
        draw.line([(0, y), (1280, y)], fill=(r, g, b))
    
    # Add text
    try:
        # Try to use a system font
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Add scene text
    scene_text = f"Scene {scene_id + 1}"
    draw.text((50, 50), scene_text, fill=(0, 0, 0), font=font)
    
    # Add story text (first 50 chars)
    story_preview = text[:50] + "..." if len(text) > 50 else text
    draw.text((50, 350), story_preview, fill=(50, 50, 50), font=font)
    
    # Save temp image
    temp_path = f"temp_scene_{scene_id}.png"
    img.save(temp_path)
    return temp_path

def create_simple_audio(text, duration=3.0):
    """Create simple audio for text"""
    # Create a simple tone based on text length
    sample_rate = 44100
    samples = int(duration * sample_rate)
    
    # Generate simple tone (frequency based on text)
    frequency = 440 + (len(text) * 10) % 200  # Vary frequency
    t = np.linspace(0, duration, samples)
    audio_data = 0.3 * np.sin(2 * np.pi * frequency * t)
    
    # Add fade in/out
    fade_samples = int(0.1 * sample_rate)
    audio_data[:fade_samples] *= np.linspace(0, 1, fade_samples)
    audio_data[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    
    return audio_data

def test_independent_studio():
    """Test Nam-toon Studio independently"""
    
    print("🎬 TESTING NAM-TOON STUDIO INDEPENDENTLY")
    print("=" * 50)
    
    # Simple test story
    story_segments = [
        {"text": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਜੀ! ਇਹ ਇੱਕ ਟੈਸਟ ਕਹਾਣੀ ਹੈ।", "emotion": "happy", "duration": 4},
        {"text": "ਇੱਕ ਮੁੰਡਾ ਆਪਣੇ ਦਾਦਾ ਜੀ ਨਾਲ ਗੱਲ ਕਰ ਰਿਹਾ ਸੀ।", "emotion": "neutral", "duration": 4},
        {"text": "ਦਾਦਾ ਜੀ ਨੇ ਸਿੱਖਿਆ ਦਿੱਤੀ ਅਤੇ ਮੁੰਡਾ ਖੁਸ਼ ਹੋ ਗਿਆ।", "emotion": "happy", "duration": 4}
    ]
    
    video_clips = []
    
    for i, segment in enumerate(story_segments):
        print(f"\n🎬 Creating scene {i+1}: {segment['text'][:30]}...")
        
        # Create scene image
        image_path = create_simple_scene_image(
            segment['text'], 
            segment['emotion'], 
            i
        )
        
        # Create video clip from image
        img_clip = ImageClip(image_path, duration=segment['duration'])
        
        # Skip zoom effect for now (compatibility issue)
        # img_clip = img_clip.resize(zoom_effect)
        
        # Create audio
        print(f"   🔊 Adding audio...")
        audio_data = create_simple_audio(segment['text'], segment['duration'])
        
        # Save audio temporarily
        temp_audio = f"temp_audio_{i}.wav"
        import scipy.io.wavfile as wav
        wav.write(temp_audio, 44100, audio_data.astype(np.float32))
        
        # Add audio to clip
        audio_clip = AudioFileClip(temp_audio)
        img_clip = img_clip.set_audio(audio_clip)
        
        video_clips.append(img_clip)
        print(f"   ✅ Scene {i+1} complete")
    
    # Combine all clips
    print(f"\n🎬 Combining {len(video_clips)} scenes...")
    final_video = concatenate_videoclips(video_clips)
    
    # Export video
    output_file = "nam_toon_studio_test.mp4"
    print(f"📹 Exporting video: {output_file}")
    
    final_video.write_videofile(
        output_file,
        fps=24,
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )
    
    # Cleanup
    for i in range(len(story_segments)):
        try:
            os.remove(f"temp_scene_{i}.png")
            os.remove(f"temp_audio_{i}.wav")
        except:
            # TODO: Implement function
    
    print(f"\n✅ NAM-TOON STUDIO TEST COMPLETE!")
    print(f"📁 Video saved: {output_file}")
    print(f"🎬 Total duration: {final_video.duration:.1f} seconds")
    print(f"🎞️ Scenes: {len(story_segments)}")
    
    return output_file

if __name__ == "__main__":
    print("🎬 Nam-toon Studio - Independent Test")
    print("ਨਾਮ-ਟੂਨ ਸਟੂਡੀਓ - ਆਜ਼ਾਦ ਟੈਸਟ")
    print("=" * 50)
    
    # Install required packages if needed
    try:
        import scipy.io.wavfile
    except ImportError:
        print("Installing scipy...")
        os.system("pip install scipy")
        import scipy.io.wavfile
    
    # Run test
    video_file = test_independent_studio()
    
    print(f"\n🎉 SUCCESS! Nam-toon Studio working independently!")
    print(f"📹 Video: {video_file}")
    print("🎬 Studio is ready for Punjabi video generation!")
