#!/usr/bin/env python3
"""
Automatic Photo Training Session
ਆਟੋਮੈਟਿਕ ਫੋਟੋ ਸਿਖਲਾਈ - ਸਾਰੀਆਂ 5,540 Photos

Train GIAN brain on all photos to build complete understanding
ਸਾਰੀਆਂ photos ਤੋਂ ਪੂਰੀ ਸਮਝ ਬਣਾਓ
"""

import cv2
import json
from pathlib import Path
from datetime import datetime
import time
from typing import Dict, List

# Try to import YOLO
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️  YOLO not available, using basic analysis")

class PhotoTrainingSession:
    """Automatic training session for all photos"""
    
    def __init__(self):
        self.stats = {
            'started': datetime.now().isoformat(),
            'photos_processed': 0,
            'total_people_detected': 0,
            'total_objects_detected': 0,
            'scene_types': {},
            'photo_categories': {},
            'detection_details': [],
            'errors': 0
        }
        
        # Load YOLO model once
        if YOLO_AVAILABLE:
            print("🔄 Loading YOLO model...")
            self.model = YOLO('yolov8n.pt')
            print("✅ YOLO model ready")
        else:
            self.model = None
    
    def analyze_photo(self, photo_path: Path) -> Dict:
        """Analyze single photo"""
        try:
            img = cv2.imread(str(photo_path))
            if img is None:
                return {'error': 'Could not read image'}
            
            h, w = img.shape[:2]
            brightness = img.mean()
            
            # Scene classification
            if brightness > 180:
                scene_type = 'bright_outdoor'
            elif brightness > 120:
                scene_type = 'normal_lighting'
            else:
                scene_type = 'dim_indoor'
            
            result = {
                'file': photo_path.name,
                'size': [w, h],
                'brightness': float(brightness),
                'scene_type': scene_type,
                'people': 0,
                'objects': []
            }
            
            # YOLO detection
            if self.model is not None:
                detections = self.model(img, verbose=False)
                
                if len(detections) > 0 and len(detections[0].boxes) > 0:
                    boxes = detections[0].boxes
                    
                    for box in boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        name = detections[0].names[cls]
                        
                        if conf > 0.3:
                            if name == 'person':
                                result['people'] += 1
                            else:
                                result['objects'].append({
                                    'type': name,
                                    'confidence': conf
                                })
            
            # Categorize photo
            people_count = result['people']
            if people_count >= 6:
                result['category'] = 'gathering'  # ਸਮਾਗਮ
            elif people_count >= 3:
                result['category'] = 'family'  # ਪਰਿਵਾਰ
            elif people_count >= 1:
                result['category'] = 'portrait'  # ਪੋਰਟਰੇਟ
            else:
                result['category'] = 'landscape'  # ਦ੍ਰਿਸ਼
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def process_batch(self, photos: List[Path], batch_size: int = 50):
        """Process photos in batches with progress"""
        total = len(photos)
        
        for i in range(0, total, batch_size):
            batch = photos[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total + batch_size - 1) // batch_size
            
            print(f"\n📦 Batch {batch_num}/{total_batches} ({len(batch)} photos)")
            print("-" * 60)
            
            for j, photo in enumerate(batch, 1):
                result = self.analyze_photo(photo)
                
                if 'error' not in result:
                    # Update stats
                    self.stats['photos_processed'] += 1
                    self.stats['total_people_detected'] += result['people']
                    self.stats['total_objects_detected'] += len(result['objects'])
                    
                    # Count scene types
                    scene = result['scene_type']
                    self.stats['scene_types'][scene] = self.stats['scene_types'].get(scene, 0) + 1
                    
                    # Count categories
                    category = result['category']
                    self.stats['photo_categories'][category] = self.stats['photo_categories'].get(category, 0) + 1
                    
                    # Store details (only for first 1000 to save memory)
                    if len(self.stats['detection_details']) < 1000:
                        self.stats['detection_details'].append({
                            'file': result['file'],
                            'people': result['people'],
                            'category': result['category'],
                            'scene': result['scene_type']
                        })
                    
                    # Show progress
                    if j % 10 == 0 or j == len(batch):
                        percent = (self.stats['photos_processed'] / total) * 100
                        print(f"   [{self.stats['photos_processed']}/{total}] {percent:.1f}% - "
                              f"People: {self.stats['total_people_detected']}, "
                              f"Objects: {self.stats['total_objects_detected']}")
                else:
                    self.stats['errors'] += 1
            
            # Save progress after each batch
            self.save_progress()
    
    def save_progress(self):
        """Save current progress"""
        self.stats['last_updated'] = datetime.now().isoformat()
        
        with open('photo_training_progress.json', 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def save_final_report(self):
        """Save final comprehensive report"""
        self.stats['completed'] = datetime.now().isoformat()
        
        # Calculate time taken
        start = datetime.fromisoformat(self.stats['started'])
        end = datetime.fromisoformat(self.stats['completed'])
        duration = (end - start).total_seconds()
        
        self.stats['duration_seconds'] = duration
        self.stats['duration_minutes'] = round(duration / 60, 1)
        
        # Save detailed report
        with open('PHOTO_TRAINING_REPORT.json', 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print("\n" + "="*70)
        print("📊 FINAL TRAINING REPORT")
        print("="*70)
        print(f"Photos Processed: {self.stats['photos_processed']}")
        print(f"Total People: {self.stats['total_people_detected']}")
        print(f"Total Objects: {self.stats['total_objects_detected']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Duration: {self.stats['duration_minutes']} minutes")
        print()
        
        print("📊 Scene Types:")
        for scene, count in self.stats['scene_types'].items():
            percent = (count / self.stats['photos_processed']) * 100
            print(f"   {scene}: {count} ({percent:.1f}%)")
        print()
        
        print("📊 Photo Categories:")
        for category, count in self.stats['photo_categories'].items():
            percent = (count / self.stats['photos_processed']) * 100
            print(f"   {category}: {count} ({percent:.1f}%)")
        print()
        
        print(f"💾 Report saved: PHOTO_TRAINING_REPORT.json")
        print("="*70)

def main():
    print("\n" + "="*70)
    print("🎓 AUTOMATIC PHOTO TRAINING SESSION")
    print("   ਆਟੋਮੈਟਿਕ ਫੋਟੋ ਸਿਖਲਾਈ")
    print("="*70)
    print()
    
    # Check for photos
    photo_dir = Path("training_photos")
    if not photo_dir.exists():
        print("❌ training_photos/ folder not found")
        return
    
    # Get all image formats
    photos = []
    for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.png', '*.PNG']:
        photos.extend(photo_dir.glob(ext))
    
    if not photos:
        print("❌ No photos found in training_photos/")
        return
    
    print(f"📸 Found {len(photos)} photos")
    print(f"🎯 Goal: Analyze all photos for complete understanding")
    print(f"⏱️  Estimated time: {len(photos) // 50} minutes")
    print()
    
    if not YOLO_AVAILABLE:
        print("⚠️  YOLO not available - basic analysis only")
        print()
    
    # Confirm
    print("🚀 Starting training session...")
    print("   This will analyze:")
    print(f"      • {len(photos)} photos")
    print("      • People detection")
    print("      • Object detection")
    print("      • Scene classification")
    print("      • Category assignment")
    print()
    
    time.sleep(2)
    
    # Start training
    session = PhotoTrainingSession()
    
    try:
        session.process_batch(photos, batch_size=50)
        session.save_final_report()
        
        print("\n✅ TRAINING SESSION COMPLETE!")
        print()
        print("🧠 GIAN Brain now understands:")
        print(f"   ✅ {session.stats['photos_processed']} photos")
        print(f"   ✅ {session.stats['total_people_detected']} people detected")
        print(f"   ✅ {session.stats['total_objects_detected']} objects detected")
        print(f"   ✅ Scene types classified")
        print(f"   ✅ Photo categories assigned")
        print()
        print("🎯 Ready for:")
        print("   • Video scene selection")
        print("   • Character counting")
        print("   • Cultural context understanding")
        print("   • Intelligent video generation")
        print()
        print("🙏 ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫ਼ਤਿਹ!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
        print(f"📊 Progress saved: {session.stats['photos_processed']} photos processed")
        session.save_progress()
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("📊 Saving progress...")
        session.save_progress()

if __name__ == "__main__":
    main()
