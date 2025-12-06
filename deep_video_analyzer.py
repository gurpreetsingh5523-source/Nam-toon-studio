#!/usr/bin/env python3
"""
🔬 DEEP VIDEO ANALYZER
AI ne banayi video da poora logic samajh
"""

import cv2
import numpy as np
import json
from pathlib import Path
import subprocess
import wave
import librosa
import soundfile as sf
from datetime import datetime

class DeepVideoAnalyzer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.analysis = {
            'video_info': {},
            'audio_analysis': {},
            'frame_analysis': {},
            'motion_analysis': {},
            'color_analysis': {},
            'text_detection': {},
            'ai_patterns': {}
        }
    
    def analyze_video_metadata(self):
        """Video di complete metadata nikalo"""
        print("📊 Analyzing video metadata...")
        
        cap = cv2.VideoCapture(self.video_path)
        
        self.analysis['video_info'] = {
            'total_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'duration_seconds': int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)),
            'codec': int(cap.get(cv2.CAP_PROP_FOURCC))
        }
        
        cap.release()
        
        # FFprobe se detailed info
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_format', '-show_streams',
            '-of', 'json',
            self.video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            ffprobe_data = json.loads(result.stdout)
            self.analysis['video_info']['ffprobe'] = ffprobe_data
        
        print(f"   ✅ Duration: {self.analysis['video_info']['duration_seconds']}s")
        print(f"   ✅ Resolution: {self.analysis['video_info']['width']}x{self.analysis['video_info']['height']}")
        print(f"   ✅ FPS: {self.analysis['video_info']['fps']}")
        print(f"   ✅ Total Frames: {self.analysis['video_info']['total_frames']}")
    
    def extract_and_analyze_audio(self):
        """Audio nikalo te analyze karo"""
        print("\n🎵 Extracting and analyzing audio...")
        
        audio_path = "temp_audio.wav"
        
        # Audio extract karo
        cmd = [
            'ffmpeg', '-i', self.video_path,
            '-vn', '-acodec', 'pcm_s16le',
            '-ar', '44100', '-ac', '2',
            audio_path, '-y'
        ]
        subprocess.run(cmd, capture_output=True)
        
        if Path(audio_path).exists():
            # Librosa naal analyze karo
            y, sr = librosa.load(audio_path, sr=None)
            
            # Audio features (simplified - no beat tracking)
            try:
                spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
                mfcc = librosa.feature.mfcc(y=y, sr=sr)
                zero_crossings = librosa.zero_crossings(y, pad=False)
                
                self.analysis['audio_analysis'] = {
                    'duration': len(y) / sr,
                    'sample_rate': sr,
                    'spectral_centroid_mean': float(np.mean(spectral_centroids)),
                    'mfcc_shape': mfcc.shape,
                    'zero_crossing_rate': float(np.sum(zero_crossings) / len(zero_crossings)),
                    'rms_energy': float(np.sqrt(np.mean(y**2))),
                    'audio_path': audio_path,
                    'has_speech': float(np.sqrt(np.mean(y**2))) > 0.01  # Simple speech detection
                }
                
                print(f"   ✅ Audio duration: {self.analysis['audio_analysis']['duration']:.2f}s")
                print(f"   ✅ RMS Energy: {self.analysis['audio_analysis']['rms_energy']:.4f}")
                print(f"   ✅ Has Speech/Sound: {self.analysis['audio_analysis']['has_speech']}")
            except Exception as e:
                print(f"   ⚠️  Audio analysis partial: {e}")
                self.analysis['audio_analysis'] = {
                    'duration': len(y) / sr,
                    'sample_rate': sr,
                    'audio_path': audio_path
                }
    
    def analyze_frames(self, sample_rate=30):
        """Frames analyze karo - har nth frame"""
        print(f"\n🖼️  Analyzing frames (sampling every {sample_rate} frames)...")
        
        cap = cv2.VideoCapture(self.video_path)
        frame_count = 0
        sampled_frames = []
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % sample_rate == 0:
                # Frame analysis
                frame_analysis = {
                    'frame_number': frame_count,
                    'timestamp': frame_count / cap.get(cv2.CAP_PROP_FPS),
                    'mean_brightness': float(np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))),
                    'color_histogram': {
                        'blue': np.histogram(frame[:,:,0], bins=16)[0].tolist(),
                        'green': np.histogram(frame[:,:,1], bins=16)[0].tolist(),
                        'red': np.histogram(frame[:,:,2], bins=16)[0].tolist()
                    },
                    'dominant_color': self.get_dominant_color(frame),
                    'sharpness': float(cv2.Laplacian(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())
                }
                sampled_frames.append(frame_analysis)
                
                if len(sampled_frames) % 10 == 0:
                    print(f"   📊 Analyzed {len(sampled_frames)} frames ({frame_count}/{total_frames})")
            
            frame_count += 1
        
        cap.release()
        
        self.analysis['frame_analysis'] = {
            'sampled_frames': sampled_frames,
            'total_sampled': len(sampled_frames),
            'sample_rate': sample_rate
        }
        
        print(f"   ✅ Analyzed {len(sampled_frames)} frames")
    
    def get_dominant_color(self, frame):
        """Frame da dominant color nikalo"""
        # Resize kar ke processing fast karo
        small_frame = cv2.resize(frame, (100, 100))
        pixels = small_frame.reshape(-1, 3)
        pixels = np.float32(pixels)
        
        # K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k = 3
        _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Sabse zyada frequent color
        dominant_color = centers[np.argmax(np.bincount(labels.flatten()))]
        
        return {
            'bgr': dominant_color.tolist(),
            'rgb': [int(dominant_color[2]), int(dominant_color[1]), int(dominant_color[0])]
        }
    
    def detect_motion_patterns(self):
        """Motion patterns detect karo - AI kithey movement use kar raha"""
        print("\n🎬 Detecting motion patterns...")
        
        cap = cv2.VideoCapture(self.video_path)
        ret, prev_frame = cap.read()
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        
        motion_data = []
        frame_count = 1
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Frame difference
            frame_diff = cv2.absdiff(prev_gray, gray)
            motion_amount = np.mean(frame_diff)
            
            if motion_amount > 5:  # Threshold for significant motion
                motion_data.append({
                    'frame': frame_count,
                    'timestamp': frame_count / cap.get(cv2.CAP_PROP_FPS),
                    'motion_intensity': float(motion_amount)
                })
            
            prev_gray = gray
            frame_count += 1
            
            if frame_count % 100 == 0:
                print(f"   📊 Processing frame {frame_count}...")
        
        cap.release()
        
        self.analysis['motion_analysis'] = {
            'motion_events': motion_data,
            'total_motion_events': len(motion_data),
            'avg_motion_intensity': float(np.mean([m['motion_intensity'] for m in motion_data])) if motion_data else 0
        }
        
        print(f"   ✅ Detected {len(motion_data)} motion events")
    
    def detect_ai_patterns(self):
        """AI patterns detect karo - screen recording vich ki ho raha"""
        print("\n🤖 Detecting AI patterns...")
        
        # Check for common AI video patterns
        patterns = {
            'has_audio': self.analysis['audio_analysis'].get('duration', 0) > 0,
            'consistent_fps': self.analysis['video_info']['fps'] > 0,
            'resolution_type': self.classify_resolution(),
            'likely_screen_recording': self.is_screen_recording(),
            'motion_consistency': self.check_motion_consistency(),
            'color_palette_analysis': self.analyze_color_palette()
        }
        
        self.analysis['ai_patterns'] = patterns
        
        print(f"   ✅ Resolution: {patterns['resolution_type']}")
        print(f"   ✅ Screen Recording: {patterns['likely_screen_recording']}")
        print(f"   ✅ Motion Consistency: {patterns['motion_consistency']}")
    
    def classify_resolution(self):
        """Resolution classify karo"""
        w = self.analysis['video_info']['width']
        h = self.analysis['video_info']['height']
        
        if w == 1920 and h == 1080:
            return "1080p (Full HD)"
        elif w == 1280 and h == 720:
            return "720p (HD)"
        elif w == 3840 and h == 2160:
            return "4K (Ultra HD)"
        else:
            return f"Custom ({w}x{h})"
    
    def is_screen_recording(self):
        """Check if likely screen recording"""
        w = self.analysis['video_info']['width']
        h = self.analysis['video_info']['height']
        
        # Screen recordings often have unusual aspect ratios
        aspect_ratio = w / h
        
        # Common screen recording indicators
        if aspect_ratio < 1 or aspect_ratio > 2.5:
            return True
        
        # Check resolution - screen recordings often have exact screen dimensions
        common_screen_widths = [1314, 1440, 1366, 1920, 2560, 3840]
        if w in common_screen_widths or h > w:
            return True
        
        return False
    
    def check_motion_consistency(self):
        """Check if motion is consistent (AI-generated vs natural)"""
        if not self.analysis.get('motion_analysis'):
            return "Unknown"
        
        motion_events = self.analysis['motion_analysis']['motion_events']
        if len(motion_events) < 10:
            return "Low motion (likely static/UI)"
        
        intensities = [m['motion_intensity'] for m in motion_events]
        std_dev = np.std(intensities)
        
        if std_dev < 5:
            return "Very consistent (likely AI/synthetic)"
        elif std_dev < 15:
            return "Moderate variation (mixed content)"
        else:
            return "High variation (natural/user interaction)"
    
    def analyze_color_palette(self):
        """Color palette analyze karo"""
        if not self.analysis.get('frame_analysis'):
            return "Unknown"
        
        sampled_frames = self.analysis['frame_analysis']['sampled_frames']
        
        # Dominant colors nikalo
        dominant_colors = [f['dominant_color']['rgb'] for f in sampled_frames]
        
        # Color diversity check
        unique_colors = len(set(tuple(c) for c in dominant_colors))
        
        if unique_colors < 5:
            return "Limited palette (UI/animated)"
        elif unique_colors < 20:
            return "Moderate palette (mixed)"
        else:
            return "Rich palette (natural/photo)"
    
    def save_analysis(self):
        """Analysis save karo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"video_analysis_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Analysis saved to: {output_file}")
        
        return output_file
    
    def print_summary(self):
        """Summary print karo"""
        print("\n" + "="*70)
        print("📊 VIDEO ANALYSIS SUMMARY")
        print("="*70)
        
        print("\n🎥 VIDEO INFO:")
        print(f"   Duration: {self.analysis['video_info']['duration_seconds']}s")
        print(f"   Resolution: {self.analysis['video_info']['width']}x{self.analysis['video_info']['height']}")
        print(f"   FPS: {self.analysis['video_info']['fps']}")
        print(f"   Total Frames: {self.analysis['video_info']['total_frames']}")
        
        if self.analysis.get('audio_analysis'):
            print("\n🎵 AUDIO INFO:")
            print(f"   Duration: {self.analysis['audio_analysis']['duration']:.2f}s")
            if 'rms_energy' in self.analysis['audio_analysis']:
                print(f"   Energy: {self.analysis['audio_analysis']['rms_energy']:.4f}")
            if 'has_speech' in self.analysis['audio_analysis']:
                print(f"   Has Speech: {self.analysis['audio_analysis']['has_speech']}")
        
        if self.analysis.get('frame_analysis'):
            print("\n🖼️  FRAME ANALYSIS:")
            print(f"   Sampled Frames: {self.analysis['frame_analysis']['total_sampled']}")
            avg_brightness = np.mean([f['mean_brightness'] for f in self.analysis['frame_analysis']['sampled_frames']])
            print(f"   Average Brightness: {avg_brightness:.2f}")
        
        if self.analysis.get('motion_analysis'):
            print("\n🎬 MOTION ANALYSIS:")
            print(f"   Motion Events: {self.analysis['motion_analysis']['total_motion_events']}")
            print(f"   Avg Intensity: {self.analysis['motion_analysis']['avg_motion_intensity']:.2f}")
        
        if self.analysis.get('ai_patterns'):
            print("\n🤖 AI PATTERNS:")
            for key, value in self.analysis['ai_patterns'].items():
                print(f"   {key}: {value}")
        
        print("\n" + "="*70)

def main():
    video_path = "training_screen_recording.mov"
    
    if not Path(video_path).exists():
        print(f"❌ Video not found: {video_path}")
        return
    
    print("🔬 DEEP VIDEO ANALYSIS")
    print("="*70)
    print(f"📹 Video: {video_path}")
    print(f"📊 Size: {Path(video_path).stat().st_size / (1024*1024):.2f} MB")
    print("="*70 + "\n")
    
    analyzer = DeepVideoAnalyzer(video_path)
    
    # Step by step analysis
    analyzer.analyze_video_metadata()
    analyzer.extract_and_analyze_audio()
    analyzer.analyze_frames(sample_rate=30)  # Sample every 30th frame
    analyzer.detect_motion_patterns()
    analyzer.detect_ai_patterns()
    
    # Save and print
    output_file = analyzer.save_analysis()
    analyzer.print_summary()
    
    print(f"\n✅ Complete analysis saved to: {output_file}")
    print("\n🎯 Next Steps:")
    print("   1. Review the JSON file for detailed data")
    print("   2. Check temp_audio.wav for audio analysis")
    print("   3. Use insights to understand AI video generation logic")

if __name__ == "__main__":
    main()
