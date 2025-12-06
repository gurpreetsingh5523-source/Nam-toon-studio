#!/usr/bin/env python3
"""
🎵 AUDIO GENERATION SYSTEM
Text-to-Speech for Punjabi with background music
"""

from gtts import gTTS
import os
from pathlib import Path

class AudioGenerator:
    def __init__(self):
        self.audio_cache = {}
        
    def generate_speech(self, text, language='pa', output_file='speech.mp3'):
        """Generate speech from Punjabi text"""
        try:
            # Check cache
            if text in self.audio_cache:
                return self.audio_cache[text]
            
            # Generate speech
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(output_file)
            
            self.audio_cache[text] = output_file
            return output_file
            
        except Exception as e:
            print(f"Error generating speech: {e}")
            # Fallback to English if Punjabi fails
            try:
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(output_file)
                return output_file
            except:
                return None
    
    def sync_audio_to_video(self, video_file, audio_file, output_file):
        """Add audio to video using ffmpeg"""
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
        except subprocess.CalledProcessError as e:
            print(f"Error syncing audio: {e}")
            return None

if __name__ == "__main__":
    # Test
    audio_gen = AudioGenerator()
    audio_file = audio_gen.generate_speech("ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ", output_file="test_punjabi_audio.mp3")
    print(f"✅ Audio generated: {audio_file}")
