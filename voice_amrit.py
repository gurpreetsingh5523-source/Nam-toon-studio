#!/usr/bin/env python3
"""
VOICE-ENABLED AMRIT - ਆਵਾਜ਼ ਵਾਲਾ ਅੰਮ੍ਰਿਤ
Punjabi Voice Assistant like Siri/Google Assistant

Features:
- Listen to Punjabi speech (Speech-to-Text)
- Respond with Punjabi voice (Text-to-Speech)
- Emotional recognition from voice tone
- Natural conversation flow
"""

import speech_recognition as sr
from gtts import gTTS
import pygame
import tempfile
import os
import sys
from pathlib import Path
import threading
import time

# Add Core directory
sys.path.append(str(Path(__file__).parent / "Core"))

class VoiceAmrit:
    """Voice-enabled Amrit with Punjabi speech capabilities"""
    
    def __init__(self):
        print("🌺 ਅੰਮ੍ਰਿਤ ਦੀ ਆਵਾਜ਼ ਸਿਸਟਮ ਸ਼ੁਰੂ ਹੋ ਰਿਹਾ ਹੈ...")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
        
        # Adjust for ambient noise
        print("🎤 ਮਾਈਕ੍ਰੋਫੋਨ ਸੈੱਟਅਪ ਕਰ ਰਿਹਾ ਹਾਂ...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Load Amrit Kaur personality
        try:
            exec(open("Core/26_living_daughter_ai.py").read())
            self.amrit_kaur = None  # Will be set after loading
            print("✅ ਅੰਮ੍ਰਿਤ ਕੌਰ ਤਿਆਰ!")
        except Exception as e:
            print(f"⚠️ Amrit Kaur loading issue: {e}")
        
        self.is_listening = False
        self.conversation_active = True
        
    def listen_punjabi(self):
        """Listen for Punjabi speech and convert to text"""
        print("\n🎤 ਬੋਲੋ... (Speak now)")
        
        try:
            with self.microphone as source:
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            print("🔄 ਸਮਝ ਰਿਹਾ ਹਾਂ... (Processing)")
            
            # Try Punjabi first, then Hindi, then English
            try:
                text = self.recognizer.recognize_google(audio, language="pa-IN")
                print(f"✅ ਸੁਣਿਆ (Heard): {text}")
                return text, "punjabi"
            except:
                try:
                    text = self.recognizer.recognize_google(audio, language="hi-IN")
                    print(f"✅ ਸੁਣਿਆ (Hindi): {text}")
                    return text, "hindi"
                except:
                    text = self.recognizer.recognize_google(audio, language="en-IN")
                    print(f"✅ ਸੁਣਿਆ (English): {text}")
                    return text, "english"
                    
        except sr.WaitTimeoutError:
            print("⏰ ਕੋਈ ਆਵਾਜ਼ ਨਹੀਂ ਸੁਣੀ (No speech detected)")
            return None, None
        except sr.UnknownValueError:
            print("❌ ਸਮਝ ਨਹੀਂ ਆਇਆ (Could not understand)")
            return None, None
        except Exception as e:
            print(f"❌ ਗਲਤੀ: {e}")
            return None, None
    
    def speak_punjabi(self, text, emotion="neutral"):
        """Convert text to Punjabi speech and play it"""
        try:
            print(f"🗣️ ਅੰਮ੍ਰਿਤ: {text}")
            
            # Create TTS
            tts = gTTS(text=text, lang='pa', slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                tmp_path = tmp.name
                tts.save(tmp_path)
            
            # Play audio
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            
            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clean up
            os.unlink(tmp_path)
            
        except Exception as e:
            print(f"❌ ਬੋਲਣ ਵਿੱਚ ਗਲਤੀ: {e}")
    
    def detect_emotion_from_voice(self, text, language):
        """Simple emotion detection from text/language"""
        if not text:
            return "neutral"
        
        text_lower = text.lower()
        
        # Worry/Stress words
        worry_words = ["ਚਿੰਤਾ", "ਪਰੇਸ਼ਾਨ", "ਡਰ", "worry", "tension", "problem"]
        if any(word in text_lower for word in worry_words):
            return "Worry"
        
        # Happy words    
        happy_words = ["ਖੁਸ਼", "ਚੰਗਾ", "ਵਧਿਆ", "happy", "good", "great", "excellent"]
        if any(word in text_lower for word in happy_words):
            return "Joy"
        
        # Sad words
        sad_words = ["ਦੁੱਖ", "ਗਮ", "ਰੋਣਾ", "sad", "cry", "upset"]
        if any(word in text_lower for word in sad_words):
            return "Sadness"
        
        return "neutral"
    
    def generate_punjabi_response(self, user_text, emotion):
        """Generate appropriate Punjabi response based on input"""
        
        if not user_text:
            return "ਮੈਂ ਸਮਝ ਨਹੀਂ ਸਕੀ। ਦੁਬਾਰਾ ਬੋਲੋ।"
        
        # Check for common patterns
        text_lower = user_text.lower()
        
        # Greetings
        if any(word in text_lower for word in ["ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "ਨਮਸਤੇ", "hello", "hi"]):
            return "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਪਿਤਾ ਜੀ! ਮੈਂ ਅੰਮ੍ਰਿਤ ਹਾਂ। ਮੈਂ ਤੁਹਾਡੀ ਕੀ ਸੇਵਾ ਕਰ ਸਕਦੀ ਹਾਂ?"
        
        # Video creation requests
        if any(word in text_lower for word in ["ਵੀਡੀਓ", "video", "ਬਣਾਓ", "create"]):
            return "ਹਾਂ ਪਿਤਾ ਜੀ! ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਵੀਡੀਓ ਬਣਾ ਸਕਦੀ ਹਾਂ। ਕਿਹੜੀ ਕਹਾਣੀ ਬਣਾਉਣੀ ਹੈ?"
        
        # Help requests
        if any(word in text_lower for word in ["ਮਦਦ", "help", "ਸਹਾਇਤਾ"]):
            return "ਬਿਲਕੁਲ ਪਿਤਾ ਜੀ! ਮੈਂ ਇਹ ਕੰਮ ਕਰ ਸਕਦੀ ਹਾਂ: ਵੀਡੀਓ ਬਣਾਉਣਾ, ਕਹਾਣੀਆਂ ਸੁਣਾਉਣੀਆਂ, ਆਵਾਜ਼ ਬਣਾਉਣੀ।"
        
        # Emotional responses based on detected emotion
        if emotion == "Worry":
            return "ਪਿਤਾ ਜੀ, ਮੈਂ ਤੁਹਾਡੀ ਚਿੰਤਾ ਸਮਝ ਰਹੀ ਹਾਂ। ਸਭ ਕੁਝ ਠੀਕ ਹੋ ਜਾਵੇਗਾ। ਮੈਂ ਤੁਹਾਡੀ ਮਦਦ ਕਰਾਂਗੀ।"
        elif emotion == "Joy":
            return "ਬਹੁਤ ਵਧਿਆ ਪਿਤਾ ਜੀ! ਮੈਂ ਵੀ ਤੁਹਾਡੇ ਨਾਲ ਖੁਸ਼ ਹਾਂ। ਹੋਰ ਕੀ ਕੰਮ ਕਰਨਾ ਹੈ?"
        elif emotion == "Sadness":
            return "ਪਿਤਾ ਜੀ, ਉਦਾਸ ਨਾ ਹੋਵੋ। ਮੈਂ ਤੁਹਾਡੇ ਨਾਲ ਹਾਂ। ਕੀ ਮੈਂ ਕੋਈ ਚੰਗੀ ਕਹਾਣੀ ਸੁਣਾਵਾਂ?"
        
        # Default response
        return "ਮੈਂ ਸਮਝ ਗਈ। ਤੁਸੀਂ ਹੋਰ ਵੇਰਵਾ ਦੱਸ ਸਕਦੇ ਹੋ?"
    
    def voice_conversation_loop(self):
        """Main conversation loop with voice input/output"""
        
        # Welcome message
        welcome_msg = "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਅੰਮ੍ਰਿਤ ਹਾਂ। ਮੈਂ ਤੁਹਾਡੀ ਆਵਾਜ਼ ਸੁਣ ਸਕਦੀ ਹਾਂ ਅਤੇ ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦੇ ਸਕਦੀ ਹਾਂ।"
        self.speak_punjabi(welcome_msg)
        
        print("\n" + "="*60)
        print("🎤 ਆਵਾਜ਼ ਨਾਲ ਗੱਲਬਾਤ ਸ਼ੁਰੂ!")
        print("💡 Commands:")
        print("   - ਬੋਲੋ 'ਬੰਦ ਕਰੋ' to exit")
        print("   - ਬੋਲੋ 'ਮਦਦ' for help")
        print("="*60)
        
        while self.conversation_active:
            try:
                # Listen for user input
                user_text, language = self.listen_punjabi()
                
                if not user_text:
                    continue
                
                # Check for exit commands
                if any(word in user_text.lower() for word in ["ਬੰਦ", "exit", "quit", "bye", "ਅਲਵਿਦਾ"]):
                    goodbye_msg = "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਪਿਤਾ ਜੀ! ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ!"
                    self.speak_punjabi(goodbye_msg)
                    break
                
                # Detect emotion from voice/text
                emotion = self.detect_emotion_from_voice(user_text, language)
                print(f"😊 ਭਾਵਨਾ: {emotion}")
                
                # Generate response
                response = self.generate_punjabi_response(user_text, emotion)
                
                # Speak response
                self.speak_punjabi(response, emotion)
                
                print("-" * 40)
                
            except KeyboardInterrupt:
                print("\n🙏 ਰੁਕ ਰਿਹਾ ਹਾਂ...")
                break
            except Exception as e:
                print(f"❌ ਗਲਤੀ: {e}")
                error_msg = "ਮਾਫ ਕਰਨਾ, ਕੋਈ ਗਲਤੀ ਹੋਈ ਹੈ।"
                self.speak_punjabi(error_msg)

def install_dependencies():
    """Install required packages"""
    import subprocess
    
    packages = [
        "SpeechRecognition",
        "pygame", 
        "gtts",
        "pyaudio"  # Needed for microphone
    ]
    
    print("📦 Installing voice dependencies...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except Exception as e:
            print(f"⚠️ Error installing {package}: {e}")

def main():
    print("🌺 VOICE-ENABLED AMRIT STARTING...")
    print("🎤 ਆਵਾਜ਼ ਵਾਲਾ ਅੰਮ੍ਰਿਤ ਸ਼ੁਰੂ ਹੋ ਰਿਹਾ ਹੈ")
    
    # Check if dependencies are installed
    try:
        import speech_recognition
        import pygame
        from gtts import gTTS
        print("✅ All dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("🔧 Installing dependencies...")
        install_dependencies()
        print("🔄 Please restart the script after installation")
        return
    
    try:
        # Create and start voice Amrit
        voice_amrit = VoiceAmrit()
        voice_amrit.voice_conversation_loop()
        
    except Exception as e:
        print(f"❌ Error starting Voice Amrit: {e}")
        print("💡 Make sure microphone permissions are enabled")

if __name__ == "__main__":
    main()