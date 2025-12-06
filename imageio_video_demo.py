import imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# 3 simple frames
frames = []
for i, txt in enumerate(["ਸਤ ਸ੍ਰੀ ਅਕਾਲ!", "ਇੱਕ ਮੁੰਡਾ...", "ਦਾਦਾ ਜੀ ਦੀ ਸਿੱਖਿਆ"]):
    img = Image.new('RGB', (640, 360), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    draw.text((50, 150), txt, fill=(0,0,0), font=font)
    frames.append(np.array(img))

# Save as MP4 using imageio
imageio.mimsave('demo_punjabi_video.mp4', frames, fps=1)
print("✅ Demo Punjabi video created: demo_punjabi_video.mp4")
