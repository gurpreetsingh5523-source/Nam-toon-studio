#!/usr/bin/env python3
"""
🎚️ CUSTOM AUDIO PROCESSOR - Nam-Toon Studio
Our own audio processing (no pydub dependency)
Version 1.0: Basic mixing and effects

Phase 1: Use external pydub (CURRENT)
Phase 2: Basic WAV mixing
Phase 3: Audio effects (fade, volume)
Phase 4: Professional audio processing (TARGET)
"""

import wave
import struct
import numpy as np
from pathlib import Path

class CustomAudioProcessor:
    """Custom Audio Processing Engine"""
    
    def __init__(self):
        self.sample_rate = 44100
        self.use_external = True  # For now, use pydub
    
    def load_wav(self, filename):
        """Load WAV file"""
        with wave.open(filename, 'r') as wav:
            frames = wav.readframes(wav.getnframes())
            audio_data = struct.unpack(f'{wav.getnframes()}h', frames)
            return list(audio_data), wav.getframerate()
    
    def save_wav(self, audio_data, filename, sample_rate=44100):
        """Save audio as WAV"""
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            
            for sample in audio_data:
                wav.writeframes(struct.pack('h', int(sample)))
    
    def mix_audio(self, audio1_file, audio2_file, output_file, ratio=0.5):
        """Mix two audio files"""
        print(f"🎛️ Mixing audio: {ratio*100}% / {(1-ratio)*100}%")
        
        # Load both files
        audio1, rate1 = self.load_wav(audio1_file)
        audio2, rate2 = self.load_wav(audio2_file)
        
        # Make same length
        max_len = max(len(audio1), len(audio2))
        audio1.extend([0] * (max_len - len(audio1)))
        audio2.extend([0] * (max_len - len(audio2)))
        
        # Mix
        mixed = []
        for s1, s2 in zip(audio1, audio2):
            mixed_sample = int(s1 * ratio + s2 * (1 - ratio))
            mixed.append(mixed_sample)
        
        # Save
        self.save_wav(mixed, output_file, rate1)
        print(f"✅ Mixed audio saved: {output_file}")
        return output_file
    
    def adjust_volume(self, audio_file, output_file, volume=1.0):
        """Adjust audio volume"""
        audio, rate = self.load_wav(audio_file)
        
        adjusted = [int(sample * volume) for sample in audio]
        
        # Clip to prevent distortion
        adjusted = [max(-32768, min(32767, s)) for s in adjusted]
        
        self.save_wav(adjusted, output_file, rate)
        return output_file
    
    def fade_in(self, audio_file, output_file, duration_sec=1.0):
        """Add fade-in effect"""
        audio, rate = self.load_wav(audio_file)
        
        fade_samples = int(duration_sec * rate)
        
        for i in range(min(fade_samples, len(audio))):
            factor = i / fade_samples
            audio[i] = int(audio[i] * factor)
        
        self.save_wav(audio, output_file, rate)
        return output_file
    
    def sync_with_video_custom(self, video_file, audio_file, output_file):
        """Sync audio with video using ffmpeg"""
        import subprocess
        
        cmd = [
            'ffmpeg', '-i', video_file,
            '-i', audio_file,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-shortest',
            output_file,
            '-y'
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_file
        except Exception as e:
            print(f"Sync failed: {e}")
            return None

# Test
if __name__ == "__main__":
    processor = CustomAudioProcessor()
    
    print("📊 Custom Audio Processor")
    print("   Status: Phase 1 (Basic mixing)")
    print("   Quality: 30%")
    print("   Using: pydub for now, custom for simple tasks")
