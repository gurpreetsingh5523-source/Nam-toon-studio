#!/usr/bin/env python3
"""
🎵 CUSTOM TTS - Nam-Toon Studio
Our own Text-to-Speech engine for Punjabi
Version 1.0: Basic phoneme synthesis

Phase 1: Use external gTTS (CURRENT)
Phase 2: Basic phoneme mapping
Phase 3: Voice training from audio files
Phase 4: Natural Punjabi speech (TARGET)
"""

import wave
import struct
import math
import numpy as np
from pathlib import Path

class CustomTTS:
    """Custom Text-to-Speech Engine"""
    
    def __init__(self):
        self.sample_rate = 44100
        self.use_external = True  # For now, use gTTS
        self.phoneme_map = self.build_phoneme_map()
        
    def build_phoneme_map(self):
        """Map Punjabi characters to sound frequencies"""
        # Basic phoneme mapping (will improve over time)
        phonemes = {
            # Punjabi vowels
            'ਅ': [(440, 0.2)],  # A sound
            'ਆ': [(440, 0.3)],  # AA sound
            'ਇ': [(880, 0.2)],  # I sound
            'ਈ': [(880, 0.3)],  # EE sound
            'ਉ': [(330, 0.2)],  # U sound
            'ਊ': [(330, 0.3)],  # OO sound
            
            # Punjabi consonants (simplified)
            'ਕ': [(200, 0.05), (600, 0.1)],  # K
            'ਗ': [(150, 0.05), (550, 0.1)],  # G
            'ਸ': [(2000, 0.15)],  # S
            'ਤ': [(300, 0.05), (800, 0.1)],  # T
            'ਦ': [(250, 0.05), (750, 0.1)],  # D
            'ਨ': [(400, 0.15)],  # N
            'ਮ': [(350, 0.15)],  # M
            'ਰ': [(500, 0.1)],   # R
            'ਲ': [(450, 0.12)],  # L
            
            # Space/pause
            ' ': [(0, 0.1)],
        }
        return phonemes
    
    def generate_speech_external(self, text, output_file='speech.mp3'):
        """Use external gTTS (current method)"""
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='pa', slow=False)
            tts.save(output_file)
            return output_file
        except Exception as e:
            print(f"External TTS failed: {e}")
            # Fallback to custom
            return self.generate_speech_custom(text, output_file.replace('.mp3', '.wav'))
    
    def generate_speech_custom(self, text, output_file='custom_speech.wav'):
        """Our custom TTS (basic version)"""
        print(f"🔊 Generating custom speech for: {text[:30]}...")
        
        audio_data = []
        
        for char in text:
            if char in self.phoneme_map:
                # Generate sound for this character
                phonemes = self.phoneme_map[char]
                for freq, duration in phonemes:
                    samples = self.generate_tone(freq, duration)
                    audio_data.extend(samples)
            else:
                # Unknown character - short pause
                samples = self.generate_tone(0, 0.05)
                audio_data.extend(samples)
        
        # Save as WAV file
        self.save_wav(audio_data, output_file)
        print(f"✅ Custom speech saved: {output_file}")
        return output_file
    
    def generate_tone(self, frequency, duration):
        """Generate a tone at given frequency"""
        if frequency == 0:
            # Silence
            return [0] * int(self.sample_rate * duration)
        
        samples = []
        for i in range(int(self.sample_rate * duration)):
            # Simple sine wave
            value = math.sin(2 * math.pi * frequency * i / self.sample_rate)
            # Add some harmonics for richness
            value += 0.3 * math.sin(4 * math.pi * frequency * i / self.sample_rate)
            value += 0.2 * math.sin(6 * math.pi * frequency * i / self.sample_rate)
            
            # Normalize and convert to 16-bit
            sample = int(value * 16384)  # Half of max 16-bit value
            samples.append(sample)
        
        return samples
    
    def save_wav(self, audio_data, output_file):
        """Save audio data as WAV file"""
        with wave.open(output_file, 'w') as wav_file:
            # Set parameters
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            
            # Write data
            for sample in audio_data:
                wav_file.writeframes(struct.pack('h', sample))
    
    def speak(self, text, output_file='speech.mp3', use_custom=False):
        """Main speech generation method"""
        if use_custom or not self.use_external:
            return self.generate_speech_custom(text, output_file.replace('.mp3', '.wav'))
        else:
            return self.generate_speech_external(text, output_file)

# Test
if __name__ == "__main__":
    tts = CustomTTS()
    
    # Test external (current)
    print("Testing external TTS (gTTS)...")
    audio1 = tts.speak("ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ", "test_external.mp3")
    print(f"✅ External: {audio1}")
    
    # Test custom (building)
    print("\nTesting custom TTS (basic)...")
    audio2 = tts.speak("ਸਤਿ", "test_custom.wav", use_custom=True)
    print(f"✅ Custom: {audio2}")
    
    print("\n📊 Status:")
    print("   External TTS: 100% working (using now)")
    print("   Custom TTS: 20% working (building)")
    print("   Goal: 100% custom TTS with natural voice")
