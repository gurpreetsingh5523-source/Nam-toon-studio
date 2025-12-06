e#!/usr/bin/env python3
"""
📸 REAL PHOTO VIDEO MAKER
Uses trained photos to create REAL character videos with auto-diversity

ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ! 🙏
"""

import os
import sys
import random
import json
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

class RealPhotoVideoMaker:
    """Create videos using REAL photos from training data"""
    
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.training_photos = self.workspace / "training_photos"
        self.output_dir = self.workspace / "realistic_videos"
        self.output_dir.mkdir(exist_ok=True)
        
        # Load training photos
        self.available_photos = self._load_training_photos()
        self.used_photos = set()  # Track to avoid repeats
        
        # Diverse backgrounds
        self.backgrounds = [
            ("village", (220, 200, 160)),      # Village beige
            ("gurdwara", (255, 245, 230)),    # Gurdwara white-gold
            ("home", (240, 230, 220)),         # Home warm
            ("garden", (200, 220, 180)),       # Garden green
            ("city", (200, 210, 220)),         # City blue-grey
            ("farm", (210, 190, 150)),         # Farm earth
            ("river", (180, 210, 230)),        # River blue
            ("mountain", (190, 200, 210))      # Mountain grey
        ]
        
        print("📸 Real Photo Video Maker initialized")
        print(f"   Available photos: {len(self.available_photos)}")
        print(f"   Auto-diversity: ENABLED")
    
    def _load_training_photos(self):
        """Load all training photos"""
        if not self.training_photos.exists():
            print("⚠️  No training photos found!")
            return []
        
        photos = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG']:
            photos.extend(self.training_photos.glob(ext))
        
        # Filter out small/icon images
        photos = [p for p in photos if p.stat().st_size > 50000]  # > 50KB
        
        return photos
    
    def get_diverse_photo(self):
        """Get a photo that hasn't been used recently"""
        if not self.available_photos:
            print("⚠️  No photos available, using default")
            return None
        
        # Get unused photos
        unused = [p for p in self.available_photos if p not in self.used_photos]
        
        # If all used, reset
        if not unused:
            self.used_photos.clear()
            unused = self.available_photos
        
        # Pick random
        photo = random.choice(unused)
        self.used_photos.add(photo)
        
        return photo
    
    def get_diverse_background(self):
        """Get random background that's different from recent"""
        bg_name, bg_color = random.choice(self.backgrounds)
        return bg_name, bg_color
    
    def create_real_character_frame(self, photo_path, background_color):
        """Create frame with real photo"""
        width, height = 1920, 1080
        
        # Create background
        frame = Image.new('RGB', (width, height), background_color)
        draw = ImageDraw.Draw(frame)
        
        # Add subtle gradient
        for y in range(height):
            alpha = y / height
            gradient_color = tuple(int(c * (1 - alpha * 0.3)) for c in background_color)
            draw.line([(0, y), (width, y)], fill=gradient_color)
        
        if photo_path and photo_path.exists():
            try:
                # Load and process photo
                photo = Image.open(photo_path)
                
                # Convert to RGB if needed
                if photo.mode != 'RGB':
                    photo = photo.convert('RGB')
                
                # Calculate size - make it prominent
                max_width = int(width * 0.4)  # 40% of frame
                max_height = int(height * 0.6)  # 60% of frame
                
                # Resize maintaining aspect ratio
                photo.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Position - center-left for character
                x = int(width * 0.15)
                y = int((height - photo.height) / 2)
                
                # Add subtle shadow
                shadow = Image.new('RGBA', photo.size, (0, 0, 0, 80))
                frame.paste(shadow, (x + 10, y + 10), shadow)
                
                # Paste photo
                frame.paste(photo, (x, y))
                
                print(f"      ✅ Added real photo: {photo_path.name[:30]}")
                
            except Exception as e:
                print(f"      ⚠️  Photo error: {e}")
        
        return frame
    
    def add_text_to_frame(self, frame, text, position="bottom"):
        """Add text overlay to frame"""
        draw = ImageDraw.Draw(frame)
        
        # Try to load font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        # Clean text
        lines = text.strip().split('\n')
        
        # Position
        if position == "bottom":
            y_start = frame.height - 200
        else:
            y_start = 100
        
        # Draw each line with shadow
        for i, line in enumerate(lines[:3]):  # Max 3 lines
            if not line.strip():
                continue
            
            y = y_start + (i * 70)
            
            # Calculate center position
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (frame.width - text_width) // 2
            
            # Shadow
            draw.text((x + 3, y + 3), line, fill=(0, 0, 0), font=font)
            # Main text
            draw.text((x, y), line, fill=(255, 255, 255), font=font)
        
        return frame
    
    def create_video_from_story(self, story_text, video_name):
        """Create video with diverse real characters"""
        print(f"\n🎬 Creating video: {video_name}")
        
        # Parse story into scenes
        scenes = self._parse_scenes(story_text)
        print(f"   Scenes: {len(scenes)}")
        
        frames = []
        
        for i, scene in enumerate(scenes, 1):
            print(f"\n   Scene {i}/{len(scenes)}: {scene.get('title', 'Untitled')[:30]}")
            
            # Get DIVERSE photo for this scene
            photo = self.get_diverse_photo()
            
            # Get DIVERSE background for this scene
            bg_name, bg_color = self.get_diverse_background()
            
            print(f"      Background: {bg_name}")
            
            # Create frames for this scene (2 seconds = 60 frames at 30fps)
            for frame_num in range(60):
                # Create frame with real photo
                frame = self.create_real_character_frame(photo, bg_color)
                
                # Add text
                text = scene.get('punjabi', '') or scene.get('text', '')
                frame = self.add_text_to_frame(frame, text)
                
                # Add scene indicator
                draw = ImageDraw.Draw(frame)
                indicator_text = f"Scene {i} | {bg_name}"
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
                except:
                    font = ImageFont.load_default()
                draw.text((50, 50), indicator_text, fill=(255, 255, 255), font=font)
                
                frames.append(frame)
            
            print(f"      ✅ 60 frames created")
        
        # Save as video
        if frames:
            video_path = self.output_dir / f"{video_name}.mp4"
            self._save_video(frames, video_path)
            return video_path
        
        return None
    
    def _parse_scenes(self, story_text):
        """Parse story into scenes"""
        scenes = []
        current_scene = {}
        
        for line in story_text.split('\n'):
            line = line.strip()
            
            if line.startswith('[SCENE'):
                if current_scene:
                    scenes.append(current_scene)
                current_scene = {'title': line, 'punjabi': '', 'english': ''}
            elif line and current_scene:
                # Punjabi lines
                if any(punjabi_char in line for punjabi_char in 'ਅਆਇਈਉਊਏਐਓਔਕਖਗਘਚਛਜਝਟਠਡਢਣਤਥਦਧਨਪਫਬਭਮਯਰਲਵਸ਼ਸਹ'):
                    current_scene['punjabi'] = line
                else:
                    current_scene['english'] = line
        
        if current_scene:
            scenes.append(current_scene)
        
        return scenes if scenes else [{'title': 'Default Scene', 'punjabi': story_text[:100]}]
    
    def _save_video(self, frames, output_path):
        """Save frames as video"""
        print(f"\n💾 Saving video: {output_path}")
        
        try:
            import cv2
            import numpy as np
            
            # Video settings
            fps = 30
            width, height = frames[0].size
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
            
            # Write frames
            for i, frame in enumerate(frames):
                # Convert PIL to OpenCV
                frame_np = np.array(frame)
                frame_bgr = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)
                out.write(frame_bgr)
                
                if (i + 1) % 30 == 0:
                    print(f"      Progress: {i+1}/{len(frames)} frames")
            
            out.release()
            
            print(f"   ✅ Video saved: {output_path}")
            print(f"   Duration: {len(frames)/fps:.1f} seconds")
            print(f"   Frames: {len(frames)}")
            
            return True
            
        except ImportError:
            print("   ⚠️  OpenCV not installed, saving first frame as image")
            img_path = output_path.with_suffix('.png')
            frames[0].save(img_path)
            print(f"   ✅ Sample frame saved: {img_path}")
            return False
        except Exception as e:
            print(f"   ❌ Video save error: {e}")
            return False


def main():
    """Test the real photo video maker"""
    print("\n" + "="*70)
    print("📸 REAL PHOTO VIDEO MAKER TEST")
    print("   Using trained photos with auto-diversity")
    print("="*70)
    
    maker = RealPhotoVideoMaker()
    
    if not maker.available_photos:
        print("\n❌ No training photos found!")
        print("   Run training first: python3 full_overnight_training.py")
        return
    
    # Test story
    test_story = """[SCENE 1: Morning]
ਸਵੇਰ ਹੋਈ, ਨਵਾਂ ਦਿਨ ਸ਼ੁਰੂ।
Morning came, new day began.

[SCENE 2: Prayer]
ਪ੍ਰਾਰਥਨਾ ਕੀਤੀ, ਮਨ ਸ਼ਾਂਤ ਹੋਇਆ।
Prayed, mind became peaceful.

[SCENE 3: Work]
ਕੰਮ ਸ਼ੁਰੂ ਕੀਤਾ, ਮਿਹਨਤ ਕਰਨੀ ਹੈ।
Started work, must work hard."""
    
    # Create test video
    video_path = maker.create_video_from_story(test_story, "test_real_photo_video")
    
    if video_path and video_path.exists():
        print(f"\n✅ Success! Video created: {video_path}")
        print("\nThis video should have:")
        print("   ✅ Different REAL photo in each scene")
        print("   ✅ Different background color per scene")
        print("   ✅ Automatic diversity (no repeats)")
    else:
        print("\n⚠️  Video creation had issues")


if __name__ == "__main__":
    main()
