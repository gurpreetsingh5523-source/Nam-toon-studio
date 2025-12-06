#!/usr/bin/env python3
"""
Quick diagnostic video to prove the pipeline works
Creates a test video with:
- Visible test pattern
- Audible beep sounds
- Text overlay
"""

from moviepy.editor import *
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np
from PIL import Image, ImageDraw, ImageFont

print("🔧 Creating diagnostic test video...")

duration = 10  # 10 second test

# Create test pattern video
def make_test_frame(t):
    # Create colorful test pattern
    w, h = 1920, 1080
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)
    
    # Animated gradient
    phase = int((t / duration) * 255)
    for y in range(h):
        color_val = int((y / h) * 255)
        color = ((color_val + phase) % 256, (255 - color_val), (phase * 2) % 256)
        draw.rectangle([(0, y), (w, y+1)], fill=color)
    
    # Draw big text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
    except:
        font = None
    
    text = f"TEST VIDEO - {t:.1f}s"
    draw.text((w//2 - 400, h//2 - 100), text, fill=(255, 255, 255), font=font)
    
    # Draw character "portrait" - a big circle
    circle_x = w//2
    circle_y = h//2 + 200
    circle_r = 150
    draw.ellipse([circle_x-circle_r, circle_y-circle_r, 
                  circle_x+circle_r, circle_y+circle_r], 
                 fill=(255, 200, 100), outline=(0, 0, 0), width=5)
    draw.ellipse([circle_x-40, circle_y-40, circle_x-10, circle_y-10], fill=(0,0,0))  # eye
    draw.ellipse([circle_x+10, circle_y-40, circle_x+40, circle_y-10], fill=(0,0,0))  # eye
    draw.arc([circle_x-60, circle_y, circle_x+60, circle_y+80], 0, 180, fill=(0,0,0), width=5)  # smile
    
    return np.array(img)

video_clip = VideoClip(make_test_frame, duration=duration).set_fps(24)

# Create test audio - beeps and sine wave
def make_test_audio(t):
    freq = 440  # A note
    beep_freq = 880  # Higher beep every second
    
    # Handle both scalar and array inputs
    t_arr = np.atleast_1d(t)
    
    # Base tone
    base = 0.3 * np.sin(2 * np.pi * freq * t_arr)
    
    # Add beeps every second
    beep_mask = (t_arr % 1.0) < 0.1
    base = base + 0.5 * beep_mask * np.sin(2 * np.pi * beep_freq * t_arr)
    
    # Return stereo
    if base.shape[0] == 1:
        return np.array([base[0], base[0]])
    else:
        return np.column_stack([base, base])

audio_clip = AudioClip(make_test_audio, duration=duration, fps=44100)

# Combine
final_video = video_clip.set_audio(audio_clip)

# Verify before writing
assert final_video.audio is not None, "Audio not attached!"

print("✅ Writing test video...")
final_video.write_videofile(
    'DIAGNOSTIC_TEST.mp4',
    fps=24,
    codec='libx264',
    audio_codec='aac',
    verbose=False,
    logger=None
)

print("\n" + "="*60)
print("✅ DIAGNOSTIC VIDEO CREATED: DIAGNOSTIC_TEST.mp4")
print("="*60)
print("\nThis video has:")
print("  ✅ Colorful animated gradient background")
print("  ✅ White text showing timestamp")
print("  ✅ Yellow smiley face (character)")
print("  ✅ Musical tone (440 Hz) continuously")
print("  ✅ Beep sound every 1 second")
print("\nIf you can see/hear this video, the pipeline works!")
print("If you cannot, there's a playback/codec issue.")
print("\nTo play: open DIAGNOSTIC_TEST.mp4")
print("="*60)
