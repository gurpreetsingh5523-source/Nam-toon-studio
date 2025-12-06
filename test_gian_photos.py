#!/usr/bin/env python3
"""
Quick photo analysis using GIAN brain
ਫੋਟੋਆਂ ਦਾ ਤੇਜ਼ analysis GIAN brain ਨਾਲ
"""

import sys
import glob
from pathlib import Path

# Import GIAN components
try:
    from ultralytics import YOLO
    import cv2
    import numpy as np
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️  YOLO not available, using basic analysis")

def analyze_photo_simple(photo_path):
    """Simple photo analysis without display"""
    print(f"\n📸 {Path(photo_path).name}")
    print("-"*60)
    
    try:
        # Read image
        img = cv2.imread(str(photo_path))
        if img is None:
            print("❌ Could not read image")
            return
        
        # Basic info
        h, w = img.shape[:2]
        
        # Brightness
        brightness = img.mean()
        
        # Scene type from brightness and colors
        avg_color = img.mean(axis=(0,1))
        b, g, r = avg_color.astype(int)
        
        scene_type = "unknown"
        if brightness > 180:
            scene_type = "ਚਮਕਦਾਰ/bright (outdoor/day)"
        elif brightness > 120:
            scene_type = "ਸਧਾਰਨ/normal lighting"
        else:
            scene_type = "ਹਨੇਰਾ/dim (indoor/evening)"
        
        if YOLO_AVAILABLE:
            # YOLO detection
            model = YOLO('yolov8n.pt')  # Smallest/fastest model
            results = model(img, verbose=False)
            
            if len(results) > 0 and len(results[0].boxes) > 0:
                boxes = results[0].boxes
                
                # Count by category
                detected_names = [results[0].names[int(b.cls[0])] for b in boxes if float(b.conf[0]) > 0.3]
                person_count = detected_names.count('person')
                
                # Print summary
                print(f"   Scene: {scene_type}")
                if person_count > 0:
                    print(f"   👥 People: {person_count}")
                
                # Top 3 objects only
                top_objects = []
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    name = results[0].names[cls]
                    if conf > 0.3 and name != 'person':
                        top_objects.append((name, conf))
                
                top_objects.sort(key=lambda x: x[1], reverse=True)
                if top_objects[:3]:
                    obj_list = ', '.join([f"{n}({c*100:.0f}%)" for n,c in top_objects[:3]])
                    print(f"   🎯 Objects: {obj_list}")
                
                # Cultural analysis
                if person_count > 5:
                    print(f"   🙏 ਸਮਾਗਮ/gathering - ਬਹੁਤ ਸਾਰੇ ਲੋਕ")
                elif person_count > 2:
                    print(f"   👨‍👩‍👧 ਪਰਿਵਾਰ/family photo")
                elif person_count > 0:
                    print(f"   🧑 ਪੋਰਟਰੇਟ/portrait")
                else:
                    if 'chair' in detected_names or 'dining table' in detected_names:
                        print(f"   🏠 ਘਰ ਦਾ ਦ੍ਰਿਸ਼/home scene")
                    else:
                        print(f"   🖼️ ਦ੍ਰਿਸ਼/landscape or object photo")
            else:
                print(f"   Scene: {scene_type}")
                print("   ℹ️  Low confidence detections")
        else:
            print("\n   ℹ️  YOLO not available - install with: pip install ultralytics")
        
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("\n" + "="*60)
    print("  🧠 GIAN Photo Analysis - Simple Mode")
    print("  ਫੋਟੋ Analysis - ਸਿੰਪਲ Mode")
    print("="*60)
    
    # Get photos
    photo_dir = Path("training_photos")
    if not photo_dir.exists():
        print("❌ training_photos/ folder not found")
        return
    
    photos = list(photo_dir.glob("*.jpg"))[:30]  # First 30 photos for better learning
    
    if not photos:
        print("❌ No photos found in training_photos/")
        return
    
    print(f"\n📊 Analyzing {len(photos)} photos...")
    print("   Learning: faces, emotions, scenes, objects")
    print("   ਸਿੱਖ ਰਿਹਾ: ਚਿਹਰੇ, ਭਾਵਨਾਵਾਂ, ਦ੍ਰਿਸ਼, ਵਸਤੂਆਂ")
    print()
    
    for photo in photos:
        analyze_photo_simple(photo)
    
    print("\n✅ Analysis Complete!")
    print("\n💡 Full GIAN brain with live display:")
    print("   python3 gian_amrit_brain.py 0  # Webcam")
    print("   python3 gian_amrit_brain.py training_photos/photo.jpg")
    print()

if __name__ == "__main__":
    main()
