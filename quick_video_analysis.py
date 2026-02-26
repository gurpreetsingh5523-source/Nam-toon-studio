#!/usr/bin/env python3
"""
⚡ QUICK VIDEO ANALYZER
Fast analysis for screen recording
"""

import cv2
import numpy as np
import json
import subprocess
from pathlib import Path
from datetime import datetime

def quick_analyze(video_path):
    """Quick video analysis"""
    print("⚡ QUICK VIDEO ANALYSIS")
    print("="*70)
    
    # 1. Basic video info
    cap = cv2.VideoCapture(video_path)
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / fps if fps > 0 else 0
    
    print(f"\n📹 VIDEO INFO:")
    print(f"   Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps:.2f}")
    print(f"   Total Frames: {total_frames}")
    print(f"   File Size: {Path(video_path).stat().st_size / (1024*1024):.2f} MB")
    
    # Aspect ratio
    aspect_ratio = width / height if height > 0 else 0
    print(f"   Aspect Ratio: {aspect_ratio:.2f}")
    
    # 2. Check if screen recording
    is_screen_rec = height > width or aspect_ratio < 1 or aspect_ratio > 2.5
    print(f"   Likely Screen Recording: {'✅ YES' if is_screen_rec else '❌ NO'}")
    
    # 3. Sample frames analysis (every 1 second)
    print(f"\n🖼️  FRAME SAMPLING (every 1 second):")
    
    sample_interval = int(fps) if fps > 0 else 30
    frame_samples = []
    
    frame_num = 0
    sample_count = 0
    
    while frame_num < total_frames and sample_count < 20:  # Max 20 samples
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            frame_samples.append({
                'frame': frame_num,
                'time': frame_num / fps,
                'brightness': float(brightness),
                'sharpness': float(sharpness)
            })
            
            sample_count += 1
            print(f"   Frame {frame_num} ({frame_num/fps:.1f}s): Brightness={brightness:.1f}, Sharpness={sharpness:.1f}")
        
        frame_num += sample_interval
    
    cap.release()
    
    # 4. Audio check
    print(f"\n🎵 AUDIO ANALYSIS:")
    audio_temp = "temp_audio_quick.wav"
    
    cmd = [
        'ffmpeg', '-i', video_path,
        '-vn', '-acodec', 'pcm_s16le',
        '-ar', '44100', '-ac', '2',
        '-t', '10',  # First 10 seconds only
        audio_temp, '-y'
    ]
    result = subprocess.run(cmd, capture_output=True)
    
    if Path(audio_temp).exists():
        audio_size = Path(audio_temp).stat().st_size
        print(f"   ✅ Audio exists")
        print(f"   Sample size (10s): {audio_size / 1024:.1f} KB")
        
        # Check if silence
        if audio_size < 10000:  # Less than 10KB = likely silence
            print(f"   Audio Content: Likely SILENT")
        else:
            print(f"   Audio Content: Has SOUND/SPEECH")
        
        Path(audio_temp).unlink()
    else:
        print(f"   ❌ No audio track")
    
    # 5. Motion detection (first 5 seconds)
    print(f"\n🎬 MOTION DETECTION (first 5 seconds):")
    
    cap = cv2.VideoCapture(video_path)
    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    
    motion_count = 0
    motion_intensity = []
    max_frames = int(fps * 5)  # 5 seconds
    
    for i in range(1, max_frames):
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        motion = np.mean(diff)
        
        if motion > 5:
            motion_count += 1
            motion_intensity.append(motion)
        
        prev_gray = gray
    
    cap.release()
    
    if motion_intensity:
        avg_motion = np.mean(motion_intensity)
        print(f"   Motion Frames: {motion_count}/{max_frames}")
        print(f"   Average Intensity: {avg_motion:.2f}")
        
        if avg_motion < 10:
            print(f"   Motion Type: LOW (UI/static content)")
        elif avg_motion < 30:
            print(f"   Motion Type: MODERATE (mixed/scrolling)")
        else:
            print(f"   Motion Type: HIGH (user interaction/animation)")
    else:
        print(f"   Motion: STATIC (no movement detected)")
    
    # 6. AI Pattern Detection
    print(f"\n🤖 AI PATTERN DETECTION:")
    
    # Screen recording indicators
    if is_screen_rec:
        print(f"   ✅ Unusual aspect ratio ({aspect_ratio:.2f}) - Screen Recording")
    
    # Check for consistent properties
    if frame_samples:
        brightness_values = [f['brightness'] for f in frame_samples]
        brightness_std = np.std(brightness_values)
        
        if brightness_std < 10:
            print(f"   ✅ Very consistent brightness - Likely UI/synthetic")
        elif brightness_std < 30:
            print(f"   ⚠️  Moderate brightness variation - Mixed content")
        else:
            print(f"   ❌ High brightness variation - Natural/camera content")
    
    # Save summary
    summary = {
        'video_path': str(video_path),
        'analysis_time': datetime.now().isoformat(),
        'video_info': {
            'duration_seconds': duration,
            'resolution': f"{width}x{height}",
            'fps': fps,
            'total_frames': total_frames,
            'aspect_ratio': aspect_ratio,
            'is_screen_recording': is_screen_rec
        },
        'frame_samples': frame_samples,
        'motion': {
            'frames_with_motion': motion_count,
            'avg_intensity': float(np.mean(motion_intensity)) if motion_intensity else 0
        }
    }
    
    output_file = f"video_analysis_quick_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Analysis saved to: {output_file}")
    print("="*70)
    
    return summary

if __name__ == "__main__":
    video_path = "training_screen_recording.mov"
    
    if not Path(video_path).exists():
        print(f"❌ Video not found: {video_path}")
    else:
        quick_analyze(video_path)
