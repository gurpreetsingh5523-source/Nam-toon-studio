#!/usr/bin/env python3
"""
Photo to Character Animator
ਫੋਟੋ ਤੋਂ Character Animation ਬਣਾਓ

Takes real photos from training_photos/ and creates animated characters
Uses YOLO to detect people, extracts them, and animates frame-by-frame
"""

import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import json
from datetime import datetime

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

class PhotoCharacterExtractor:
    """Extract actual characters from photos"""
    
    def __init__(self):
        if YOLO_AVAILABLE:
            self.model = YOLO('yolov8n.pt')
        else:
            self.model = None
        
        self.extracted_characters = []
    
    def extract_people_from_photo(self, photo_path: str):
        """Extract all people from a photo as separate character images"""
        print(f"\n📸 Processing: {Path(photo_path).name}")
        
        img = cv2.imread(photo_path)
        if img is None:
            print("   ❌ Could not read image")
            return []
        
        if not YOLO_AVAILABLE:
            print("   ⚠️  YOLO not available")
            return []
        
        # Detect people
        results = self.model(img, verbose=False)
        
        characters = []
        if len(results) > 0 and len(results[0].boxes) > 0:
            boxes = results[0].boxes
            
            person_count = 0
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                name = results[0].names[cls]
                
                if name == 'person' and conf > 0.5:
                    # Extract person region
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Add padding
                    padding = 20
                    x1 = max(0, x1 - padding)
                    y1 = max(0, y1 - padding)
                    x2 = min(img.shape[1], x2 + padding)
                    y2 = min(img.shape[0], y2 + padding)
                    
                    person_img = img[y1:y2, x1:x2]
                    
                    if person_img.size > 0:
                        person_count += 1
                        character = {
                            'image': person_img,
                            'bbox': [x1, y1, x2, y2],
                            'confidence': conf,
                            'source': Path(photo_path).name,
                            'id': f"{Path(photo_path).stem}_person_{person_count}"
                        }
                        characters.append(character)
            
            print(f"   ✅ Extracted {len(characters)} people")
        else:
            print("   ℹ️  No people detected")
        
        return characters
    
    def save_character(self, character, output_dir: Path):
        """Save extracted character as PNG"""
        output_dir.mkdir(exist_ok=True)
        
        char_id = character['id']
        output_path = output_dir / f"{char_id}.png"
        
        # Convert to PIL Image
        img_rgb = cv2.cvtColor(character['image'], cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        
        # Save with transparency if possible
        pil_img.save(output_path)
        
        return output_path

class FrameByFrameAnimator:
    """Create frame-by-frame animation with extracted characters"""
    
    def __init__(self):
        self.frames = []
    
    def create_animation_frames(self, character_paths, background_img, num_frames=30):
        """Create animation frames with character movement"""
        print(f"\n🎬 Creating {num_frames} animation frames...")
        
        bg = cv2.imread(str(background_img))
        if bg is None:
            print("❌ Could not load background")
            return []
        
        h, w = bg.shape[:2]
        
        # Load characters
        characters = []
        for char_path in character_paths[:3]:  # Max 3 characters
            char_img = cv2.imread(str(char_path))
            if char_img is not None:
                # Resize character to fit scene
                char_h, char_w = char_img.shape[:2]
                scale = min(h * 0.6 / char_h, w * 0.3 / char_w)
                new_w = int(char_w * scale)
                new_h = int(char_h * scale)
                char_resized = cv2.resize(char_img, (new_w, new_h))
                characters.append(char_resized)
        
        if not characters:
            print("❌ No characters loaded")
            return []
        
        # Create frames with movement
        frames = []
        for frame_num in range(num_frames):
            # Copy background
            frame = bg.copy()
            
            # Calculate movement for each character
            for i, char in enumerate(characters):
                char_h, char_w = char.shape[:2]
                
                # Movement: LEFT to RIGHT
                progress = frame_num / (num_frames - 1)
                
                # Stagger characters
                start_x = -char_w + (i * 100)
                end_x = w + (i * 100)
                x = int(start_x + (end_x - start_x) * progress)
                
                # Vertical position (bottom of frame)
                y = h - char_h - 50 - (i * 20)
                
                # Place character on frame
                if 0 <= x < w and 0 <= y < h:
                    # Calculate overlap region
                    x_start = max(0, x)
                    x_end = min(w, x + char_w)
                    y_start = max(0, y)
                    y_end = min(h, y + char_h)
                    
                    char_x_start = max(0, -x)
                    char_x_end = char_w - max(0, (x + char_w) - w)
                    char_y_start = max(0, -y)
                    char_y_end = char_h - max(0, (y + char_h) - h)
                    
                    if x_end > x_start and y_end > y_start:
                        frame[y_start:y_end, x_start:x_end] = \
                            char[char_y_start:char_y_end, char_x_start:char_x_end]
            
            frames.append(frame)
            
            if (frame_num + 1) % 10 == 0:
                print(f"   Created frame {frame_num + 1}/{num_frames}")
        
        print(f"   ✅ Generated {len(frames)} frames")
        return frames
    
    def frames_to_video(self, frames, output_path: str, fps=30):
        """Convert frames to video"""
        if not frames:
            print("❌ No frames to convert")
            return False
        
        print(f"\n💾 Creating video: {output_path}")
        
        h, w = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
        
        for frame in frames:
            out.write(frame)
        
        out.release()
        
        print(f"✅ Video created!")
        return True

def main():
    print("\n" + "="*70)
    print("🎨 PHOTO TO CHARACTER ANIMATOR")
    print("   ਫੋਟੋ ਤੋਂ Character Animation")
    print("="*70)
    print()
    
    # Setup
    photo_dir = Path("training_photos")
    char_dir = Path("extracted_characters")
    output_dir = Path("animated_videos")
    
    char_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # Step 1: Extract characters from photos
    print("📋 STEP 1: Extract Characters from Photos")
    print("-"*70)
    
    extractor = PhotoCharacterExtractor()
    
    if not YOLO_AVAILABLE:
        print("❌ YOLO not available - cannot extract characters")
        print("   Install: pip install ultralytics")
        return
    
    # Get photos with people
    photos = list(photo_dir.glob("*.jpg"))[:10]  # First 10 for demo
    
    all_characters = []
    for photo in photos:
        characters = extractor.extract_people_from_photo(str(photo))
        
        for char in characters:
            char_path = extractor.save_character(char, char_dir)
            all_characters.append(char_path)
            print(f"   💾 Saved: {char_path.name}")
    
    print(f"\n✅ Extracted {len(all_characters)} characters total")
    
    if not all_characters:
        print("❌ No characters extracted")
        return
    
    # Step 2: Create animation frames
    print("\n📋 STEP 2: Create Animation Frames")
    print("-"*70)
    
    animator = FrameByFrameAnimator()
    
    # Use a photo as background
    background = photos[0] if photos else None
    
    if background:
        frames = animator.create_animation_frames(
            all_characters,
            background,
            num_frames=60  # 2 seconds at 30fps
        )
        
        # Step 3: Create video
        print("\n📋 STEP 3: Create Final Video")
        print("-"*70)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_video = output_dir / f"photo_animated_{timestamp}.mp4"
        
        success = animator.frames_to_video(frames, str(output_video), fps=30)
        
        if success:
            print("\n" + "="*70)
            print("✅ ANIMATION COMPLETE!")
            print("="*70)
            print(f"📹 Video: {output_video}")
            print(f"👥 Characters: {len(all_characters)} from your photos")
            print(f"🎞️  Frames: {len(frames)}")
            print(f"⏱️  Duration: {len(frames)/30:.1f} seconds")
            print()
            print("🎯 Key Improvements:")
            print("   ✅ Used YOUR photos")
            print("   ✅ Extracted REAL people")
            print("   ✅ Frame-by-frame animation")
            print("   ✅ Character movement (LEFT → RIGHT)")
            print()
            print("💡 Next: Add audio, better backgrounds, more frames!")
            print("="*70)
            
            # Open video
            import subprocess
            subprocess.run(['open', str(output_video)])
    else:
        print("❌ No background image available")

if __name__ == "__main__":
    main()
