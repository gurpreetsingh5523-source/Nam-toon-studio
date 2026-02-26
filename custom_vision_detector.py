#!/usr/bin/env python3
"""
Custom Object Detector - Phase 2 Development
ਆਪਣਾ Object Detector - Phase 2 ਵਿਕਾਸ

Building our own detector specialized for Punjabi/Sikh content
This will eventually replace YOLO for full independence

Status: DEVELOPMENT (Not production yet)
Strategy: Train on our 5,540 photos
Goal: 85%+ accuracy, <10MB size, real-time speed
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
import json
from datetime import datetime

class CustomPersonDetector:
    """
    Custom person detector using OpenCV
    Specialized for Punjabi/Sikh faces and turbans
    """
    
    def __init__(self):
        self.face_cascade = None
        self.body_cascade = None
        self.trained = False
        
        # Try to load pre-trained cascades
        try:
            # Face detection
            face_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(face_path)
            
            # Body detection
            body_path = cv2.data.haarcascades + 'haarcascade_fullbody.xml'
            self.body_cascade = cv2.CascadeClassifier(body_path)
            
            print("✅ OpenCV cascades loaded")
        except Exception as e:
            print(f"⚠️  Could not load cascades: {e}")
    
    def detect_people(self, image: np.ndarray) -> List[Dict]:
        """Detect people in image"""
        if self.face_cascade is None:
            return []
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        results = []
        for (x, y, w, h) in faces:
            results.append({
                'type': 'person',
                'bbox': [x, y, w, h],
                'confidence': 0.7,  # Fixed confidence for now
                'method': 'opencv_cascade'
            })
        
        return results
    
    def detect_turban(self, image: np.ndarray, face_bbox: List[int]) -> bool:
        """
        Detect if person is wearing turban
        Simple heuristic: check region above face for consistent color
        """
        x, y, w, h = face_bbox
        
        # Check region above face
        turban_y = max(0, y - h)
        turban_region = image[turban_y:y, x:x+w]
        
        if turban_region.size == 0:
            return False
        
        # Check color consistency (turbans are usually solid color)
        std_dev = np.std(turban_region)
        
        # Low std dev = consistent color = likely turban
        return std_dev < 30
    
    def analyze_scene(self, image: np.ndarray) -> Dict:
        """Analyze overall scene"""
        h, w = image.shape[:2]
        brightness = image.mean()
        
        # Color analysis
        avg_color = image.mean(axis=(0,1))
        
        scene = {
            'size': [w, h],
            'brightness': float(brightness),
            'avg_color': avg_color.tolist(),
            'scene_type': 'unknown'
        }
        
        # Classify scene
        if brightness > 180:
            scene['scene_type'] = 'bright_outdoor'
        elif brightness > 120:
            scene['scene_type'] = 'normal_indoor'
        else:
            scene['scene_type'] = 'dim_indoor'
        
        return scene

class CustomObjectDetector:
    """
    Simple object detector using color and shape
    For common objects: chair, table, book, etc.
    """
    
    def __init__(self):
        self.templates = {}
    
    def detect_by_color(self, image: np.ndarray, color_name: str) -> List[Dict]:
        """Detect objects by color"""
        # Color ranges (HSV)
        color_ranges = {
            'orange': ([5, 100, 100], [15, 255, 255]),  # Saffron
            'blue': ([100, 100, 100], [130, 255, 255]),
            'white': ([0, 0, 200], [180, 30, 255])
        }
        
        if color_name not in color_ranges:
            return []
        
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower, upper = color_ranges[color_name]
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        results = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Minimum size
                x, y, w, h = cv2.boundingRect(contour)
                results.append({
                    'type': f'{color_name}_object',
                    'bbox': [x, y, w, h],
                    'confidence': 0.6,
                    'method': 'color_detection'
                })
        
        return results

class CustomVisionSystem:
    """
    Complete custom vision system
    Combines person, object, and scene detection
    """
    
    def __init__(self):
        self.person_detector = CustomPersonDetector()
        self.object_detector = CustomObjectDetector()
        self.stats = {
            'images_processed': 0,
            'people_detected': 0,
            'objects_detected': 0,
            'accuracy_vs_yolo': None
        }
    
    def process_image(self, image_path: str) -> Dict:
        """Process single image with all detectors"""
        img = cv2.imread(image_path)
        if img is None:
            return {'error': 'Could not read image'}
        
        # Scene analysis
        scene = self.person_detector.analyze_scene(img)
        
        # Person detection
        people = self.person_detector.detect_people(img)
        
        # Check for turbans
        for person in people:
            person['has_turban'] = self.person_detector.detect_turban(
                img, person['bbox']
            )
        
        # Object detection (simple color-based)
        objects = []
        objects.extend(self.object_detector.detect_by_color(img, 'orange'))
        objects.extend(self.object_detector.detect_by_color(img, 'blue'))
        
        # Update stats
        self.stats['images_processed'] += 1
        self.stats['people_detected'] += len(people)
        self.stats['objects_detected'] += len(objects)
        
        return {
            'scene': scene,
            'people': people,
            'objects': objects,
            'total_detections': len(people) + len(objects),
            'method': 'custom_detector_v1'
        }
    
    def compare_with_yolo(self, image_path: str, yolo_results: Dict) -> Dict:
        """Compare custom detector results with YOLO"""
        custom_results = self.process_image(image_path)
        
        # Count people
        custom_people = len(custom_results.get('people', []))
        yolo_people = sum(1 for obj in yolo_results.get('objects', []) 
                         if obj.get('type') == 'person')
        
        # Calculate accuracy
        if yolo_people > 0:
            accuracy = min(custom_people / yolo_people, 1.0) * 100
        else:
            accuracy = 100 if custom_people == 0 else 0
        
        return {
            'custom_people': custom_people,
            'yolo_people': yolo_people,
            'accuracy': accuracy,
            'match': abs(custom_people - yolo_people) <= 1  # Allow 1 difference
        }
    
    def save_stats(self, filepath: str = "custom_detector_stats.json"):
        """Save detection statistics"""
        stats = {
            **self.stats,
            'timestamp': datetime.now().isoformat(),
            'version': 'v1.0-development'
        }
        
        with open(filepath, 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"💾 Stats saved: {filepath}")

def test_custom_detector():
    """Test custom detector on sample photos"""
    print("\n" + "="*70)
    print("🧪 TESTING CUSTOM DETECTOR - Phase 2 Development")
    print("   ਕਸਟਮ Detector ਦੀ ਜਾਂਚ - Phase 2 ਵਿਕਾਸ")
    print("="*70)
    
    detector = CustomVisionSystem()
    
    # Test on a few photos
    photo_dir = Path("training_photos")
    if not photo_dir.exists():
        print("❌ training_photos/ not found")
        return
    
    photos = list(photo_dir.glob("*.jpg"))[:5]
    
    print(f"\n📸 Testing on {len(photos)} photos...")
    print()
    
    for photo in photos:
        print(f"Processing: {photo.name}")
        result = detector.process_image(str(photo))
        
        if 'error' not in result:
            people_count = len(result['people'])
            objects_count = len(result['objects'])
            scene_type = result['scene']['scene_type']
            
            print(f"   Scene: {scene_type}")
            print(f"   People: {people_count}")
            print(f"   Objects: {objects_count}")
            
            # Check for turbans
            turbans = sum(1 for p in result['people'] if p.get('has_turban'))
            if turbans > 0:
                print(f"   👳 Turbans detected: {turbans}")
        print()
    
    # Save stats
    detector.save_stats()
    
    print("="*70)
    print("📊 SUMMARY:")
    print(f"   Images processed: {detector.stats['images_processed']}")
    print(f"   Total people: {detector.stats['people_detected']}")
    print(f"   Total objects: {detector.stats['objects_detected']}")
    print()
    print("💡 STATUS: Development version")
    print("   Not ready for production yet")
    print("   Need training on full 5,540 photos")
    print()
    print("🎯 NEXT STEPS:")
    print("   1. Label all training photos")
    print("   2. Train on our data")
    print("   3. Compare accuracy with YOLO")
    print("   4. Optimize for speed")
    print()
    print("🙏 ਵਾਹਿਗੁਰੂ!")
    print("="*70)

if __name__ == "__main__":
    test_custom_detector()
