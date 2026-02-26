"""
ਆਤਮ ਨਿਰਭਰ Character Generator
Uses only PIL - no Stable Diffusion needed for basic avatars
"""

from PIL import Image, ImageDraw, ImageFont
import random
from pathlib import Path


def generate_character(name, emotion="neutral", size=512):
    """Generate a character avatar without AI"""
    
    # Color schemes based on emotion
    emotions = {
        "neutral": [(100, 150, 255), (80, 120, 200)],
        "happy": [(255, 200, 100), (255, 180, 80)],
        "sad": [(150, 150, 180), (120, 120, 160)],
        "angry": [(255, 100, 100), (220, 80, 80)],
    }
    
    colors = emotions.get(emotion, emotions["neutral"])
    
    # Create gradient background
    img = Image.new('RGB', (size, size))
    draw = ImageDraw.Draw(img)
    
    # Gradient
    for y in range(size):
        t = y / size
        r = int(colors[0][0] * (1-t) + colors[1][0] * t)
        g = int(colors[0][1] * (1-t) + colors[1][1] * t)
        b = int(colors[0][2] * (1-t) + colors[1][2] * t)
        draw.line([(0, y), (size, y)], fill=(r, g, b))
    
    # Draw face circle
    margin = size // 4
    draw.ellipse([margin, margin, size-margin, size-margin],
                 fill=(255, 230, 200), outline=(200, 150, 100), width=5)
    
    # Draw eyes
    eye_y = size // 2 - size // 8
    eye_size = size // 20
    left_eye = size // 2 - size // 6
    right_eye = size // 2 + size // 6
    
    draw.ellipse([left_eye-eye_size, eye_y-eye_size,
                  left_eye+eye_size, eye_y+eye_size], fill=(50, 50, 50))
    draw.ellipse([right_eye-eye_size, eye_y-eye_size,
                  right_eye+eye_size, eye_y+eye_size], fill=(50, 50, 50))
    
    # Draw smile/mouth based on emotion
    mouth_y = size // 2 + size // 6
    if emotion == "happy":
        draw.arc([size//3, mouth_y-20, 2*size//3, mouth_y+40],
                 0, 180, fill=(50, 50, 50), width=5)
    elif emotion == "sad":
        draw.arc([size//3, mouth_y-40, 2*size//3, mouth_y+20],
                 180, 360, fill=(50, 50, 50), width=5)
    else:
        draw.line([size//3, mouth_y, 2*size//3, mouth_y],
                  fill=(50, 50, 50), width=5)
    
    # Add name
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size//12)
    except:
        font = ImageFont.load_default()
    
    draw.text((size//2, size-size//8), name,
              fill=(255, 255, 255), font=font, anchor="mm")
    
    return img


if __name__ == "__main__":
    # Test
    img = generate_character("Test", "happy")
    img.save("test_character.png")
    print("✅ Character generator works!")
