#!/usr/bin/env python3
"""
🎬 TEST REAL PHOTOS IN VIDEO
Quick test to verify real photos are being used
"""

from pathlib import Path
from PIL import Image, ImageDraw
from realistic_renderer import RealisticRenderer
import cv2
import numpy as np

def test_real_photo_in_video():
    print("\n🎬 TESTING REAL PHOTOS IN VIDEO")
    print("="*70)
    
    # Initialize renderer
    renderer = RealisticRenderer()
    
    print(f"\n📊 Status:")
    print(f"   Real photos available: {len(renderer.available_photos)}")
    print(f"   Use real photos: {renderer.use_real_photos}")
    
    if not renderer.use_real_photos:
        print("\n❌ Real photos not available!")
        return
    
    # Create test video - 3 scenes with different photos
    width, height = 1920, 1080
    fps = 30
    frames = []
    
    print(f"\n🎥 Creating 3 scenes...")
    
    for scene in range(3):
        print(f"\n   Scene {scene + 1}:")
        
        # Reset photo for new scene
        if hasattr(renderer, '_current_photo'):
            delattr(renderer, '_current_photo')
        
        # Create frames for this scene (2 seconds = 60 frames)
        for frame_num in range(60):
            # Create frame with real photo
            img = renderer.create_realistic_background(width, height)
            draw = ImageDraw.Draw(img)
            
            # Draw character with REAL PHOTO
            char_x = 500
            char_y = 550
            renderer.draw_realistic_character(draw, char_x, char_y, frame_num, img=img)
            
            # Add scene label
            draw.text((50, 50), f"Scene {scene + 1} - Real Photo Test", 
                     fill=(255, 255, 255), font=None)
            
            frames.append(img)
        
        # Show which photo was used
        if hasattr(renderer, '_current_photo'):
            print(f"      ✅ Used: {renderer._current_photo.name[:50]}")
    
    # Save video
    output_path = Path("test_real_photos_in_video.mp4")
    
    print(f"\n💾 Saving video...")
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    for i, frame in enumerate(frames):
        frame_np = np.array(frame)
        frame_bgr = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)
        
        if (i + 1) % 30 == 0:
            print(f"      Progress: {i+1}/{len(frames)} frames")
    
    out.release()
    
    print(f"\n✅ Video saved: {output_path}")
    print(f"   Duration: {len(frames)/fps:.1f} seconds")
    print(f"   Scenes: 3")
    print()
    print("🔍 Check video:")
    print("   - Should show 3 DIFFERENT real photos")
    print("   - Each scene = different person")
    print("   - No cartoons!")
    
    return output_path

if __name__ == "__main__":
    video = test_real_photo_in_video()
    if video:
        print(f"\n🎬 Open video: open {video}")
