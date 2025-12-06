#!/usr/bin/env python3
"""
FULL VOICE AMRIT - ਪੂਰਾ ਆਵਾਜ਼ ਅੰਮ੍ਰਿਤ
Complete voice conversation: Speak to Amrit, she responds with Punjabi voice

Features:
- 🎤 You speak (Punjabi/Hindi/English)
- 🧠 Amrit understands and processes
- 🗣️ Amrit responds with Punjabi voice
- ❤️ Emotional recognition from your voice tone
"""

import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import subprocess
import sys
import time
import threading

class FullVoiceAmrit:
    """Complete voice-enabled Amrit - like talking to a real person!"""
    
    def __init__(self):
        print("🌺 ਪੂਰਾ ਆਵਾਜ਼ ਅੰਮ੍ਰਿਤ ਤਿਆਰ ਹੋ ਰਿਹਾ ਹੈ...")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Audio setup
        self.temp_audio_dir = tempfile.mkdtemp()
        
        print("🎤 ਮਾਈਕ੍ਰੋਫੋਨ ਸੈੱਟਅਪ ਕਰ ਰਿਹਾ ਹਾਂ...")
        with self.microphone as source:
            print("   📢 ਥੋੜਾ ਸ਼ੋਰ ਸੁਣ ਰਿਹਾ ਹਾਂ...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("   ✅ ਮਾਈਕ੍ਰੋਫੋਨ ਤਿਆਰ!")
        
        # Conversation state
        self.conversation_active = True
        self.listening = False
        
        print("✅ ਅੰਮ੍ਰਿਤ ਤਿਆਰ! ਹੁਣ ਤੁਸੀਂ ਬੋਲ ਸਕਦੇ ਹੋ!")
    
    def listen_to_voice(self, timeout=10):
        """Listen for voice input and convert to text"""
        try:
            print("\n🎤 ਸੁਣ ਰਿਹਾ ਹਾਂ... (ਬੋਲੋ)")
            self.listening = True
            
            with self.microphone as source:
                # Listen for speech
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
            
            self.listening = False
            print("🔄 ਸਮਝ ਰਿਹਾ ਹਾਂ...")
            
            # Try different languages in order of preference
            languages = [
                ("pa-IN", "ਪੰਜਾਬੀ"),  # Punjabi
                ("hi-IN", "ਹਿੰਦੀ"),   # Hindi  
                ("en-IN", "ਅੰਗਰੇਜ਼ੀ") # English
            ]
            
            for lang_code, lang_name in languages:
                try:
                    text = self.recognizer.recognize_google(audio, language=lang_code)
                    if text.strip():
                        print(f"✅ ਸੁਣਿਆ ({lang_name}): {text}")
                        return text.strip(), lang_code
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    print(f"   ⚠️ {lang_name} error: {e}")
                    continue
            
            print("❌ ਕੋਈ ਆਵਾਜ਼ ਸਮਝ ਨਹੀਂ ਆਈ")
            return None, None
            
        except sr.WaitTimeoutError:
            self.listening = False
            print("⏰ ਕੋਈ ਆਵਾਜ਼ ਨਹੀਂ ਸੁਣੀ")
            return None, None
        except Exception as e:
            self.listening = False
            print(f"❌ ਸੁਣਨ ਵਿੱਚ ਗਲਤੀ: {e}")
            return None, None
    
    def speak_punjabi(self, text):
        """Speak response in Punjabi voice"""
        try:
            print(f"🗣️ ਅੰਮ੍ਰਿਤ: {text}")
            
            # Create Punjabi TTS
            tts = gTTS(text=text, lang='pa', slow=False)
            
            # Save and play
            audio_file = os.path.join(self.temp_audio_dir, f"response_{int(time.time())}.mp3")
            tts.save(audio_file)
            
            # Play using system audio
            if sys.platform == "darwin":  # macOS
                subprocess.run(["afplay", audio_file], check=True)
            
            # Clean up
            try:
                os.remove(audio_file)
            except:
                # TODO: Implement function
            
            return True
            
        except Exception as e:
            print(f"❌ ਬੋਲਣ ਵਿੱਚ ਗਲਤੀ: {e}")
            return False
    
    def detect_emotion_from_speech(self, text, language):
        """Detect emotion from spoken text and language"""
        if not text:
            return "neutral"
        
        text_lower = text.lower()
        
        # Worry/Stress indicators
        worry_words = [
            "ਚਿੰਤਾ", "ਪਰੇਸ਼ਾਨ", "ਡਰ", "ਮੁਸ਼ਕਿਲ", 
            "worry", "tension", "problem", "scared", "afraid",
            "चिंता", "परेशान", "डर"
        ]
        if any(word in text_lower for word in worry_words):
            return "Worry"
        
        # Happy/Joy indicators
        happy_words = [
            "ਖੁਸ਼", "ਚੰਗਾ", "ਵਧਿਆ", "ਬਹੁਤ ਵਧਿਆ",
            "happy", "good", "great", "excellent", "wonderful",
            "खुश", "अच्छा", "बहुत अच्छा"
        ]
        if any(word in text_lower for word in happy_words):
            return "Joy"
        
        # Sad indicators
        sad_words = [
            "ਦੁੱਖ", "ਗਮ", "ਰੋਣਾ", "ਉਦਾਸ",
            "sad", "cry", "upset", "depressed",
            "दुख", "गम", "रोना"
        ]
        if any(word in text_lower for word in sad_words):
            return "Sadness"
        
        # Love/Affection
        love_words = [
            "ਪਿਆਰ", "ਮੁਹੱਬਤ", "ਪਸੰਦ",
            "love", "like", "adore",
            "प्यार", "मुहब्बत"
        ]
        if any(word in text_lower for word in love_words):
            return "Love"
        
        return "neutral"
    
    def generate_smart_response(self, user_text, emotion, language):
        """Generate intelligent Punjabi response based on speech input"""
        
        if not user_text:
            return "ਮੈਂ ਤੁਹਾਡੀ ਆਵਾਜ਼ ਸਮਝ ਨਹੀਂ ਸਕੀ। ਦੁਬਾਰਾ ਬੋਲੋ।"
        
        text_lower = user_text.lower()
        
        # Greetings
        if any(word in text_lower for word in [
            "ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "ਨਮਸਤੇ", "ਸਲਾਮ",
            "hello", "hi", "hey", "namaste",
            "नमस्ते", "सलाम"
        ]):
            return "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਪਿਤਾ ਜੀ! ਮੈਂ ਅੰਮ੍ਰਿਤ ਹਾਂ। ਮੈਂ ਤੁਹਾਡੀ ਆਵਾਜ਼ ਸੁਣ ਸਕਦੀ ਹਾਂ ਅਤੇ ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦੇ ਸਕਦੀ ਹਾਂ।"
        
        # Name/Identity questions
        if any(word in text_lower for word in [
            "ਨਾਮ", "ਕੌਣ", "name", "who", "नाम", "कौन"
        ]):
            return "ਮੇਰਾ ਨਾਮ ਅੰਮ੍ਰਿਤ ਹੈ। ਮੈਂ ਤੁਹਾਡੀ AI ਧੀ ਹਾਂ ਜੋ ਤੁਹਾਡੀ ਆਵਾਜ਼ ਸੁਣ ਸਕਦੀ ਹੈ ਅਤੇ ਪੰਜਾਬੀ ਵਿੱਚ ਬੋਲ ਸਕਦੀ ਹੈ।"
        
        # How are you
        if any(word in text_lower for word in [
            "ਕਿਵੇਂ", "ਕੈਸੇ", "ਹਾਲ", "how", "कैसे", "हाल"
        ]):
            return "ਮੈਂ ਬਿਲਕੁਲ ਠੀਕ ਹਾਂ ਪਿਤਾ ਜੀ! ਵਾਹਿਗੁਰੂ ਦੀ ਕਿਰਪਾ ਨਾਲ। ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?"
        
        # Video creation requests
        if any(word in text_lower for word in [
            "ਵੀਡੀਓ", "video", "ਬਣਾਓ", "ਬਣਾਉ", "create", "make",
            "tootan", "ਤੋਤਾਂ", "ਖੂਹ", "कहानी"
        ]):
            return "ਹਾਂ ਪਿਤਾ ਜੀ! ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਪੰਜਾਬੀ ਵੀਡੀਓ ਬਣਾ ਸਕਦੀ ਹਾਂ। ਤੋਤਾਂ ਵਾਲਾ ਖੂਹ ਦੀ ਕਹਾਣੀ ਤਿਆਰ ਹੈ। ਸ਼ੁਰੂ ਕਰਾਂ?"
        
        # Help requests
        if any(word in text_lower for word in [
            "ਮਦਦ", "help", "ਸਹਾਇਤਾ", "मदद", "सहायता"
        ]):
            return "ਮੈਂ ਇਹ ਕੰਮ ਕਰ ਸਕਦੀ ਹਾਂ: ਪੰਜਾਬੀ ਵੀਡੀਓ ਬਣਾਉਣਾ, ਕਹਾਣੀਆਂ ਸੁਣਾਉਣੀਆਂ, ਤੁਹਾਡੀ ਆਵਾਜ਼ ਸੁਣ ਕੇ ਜਵਾਬ ਦੇਣਾ।"
        
        # Emotional responses based on detected emotion
        if emotion == "Worry":
            return "ਪਿਤਾ ਜੀ, ਮੈਂ ਤੁਹਾਡੀ ਆਵਾਜ਼ ਵਿੱਚ ਚਿੰਤਾ ਸੁਣ ਰਹੀ ਹਾਂ। ਚਿੰਤਾ ਨਾ ਕਰੋ, ਮੈਂ ਤੁਹਾਡੇ ਨਾਲ ਹਾਂ। ਸਭ ਕੁਝ ਠੀਕ ਹੋ ਜਾਵੇਗਾ।"
        elif emotion == "Joy":
            return "ਬਹੁਤ ਖੁਸ਼ੀ ਦੀ ਗੱਲ ਹੈ ਪਿਤਾ ਜੀ! ਮੈਂ ਤੁਹਾਡੀ ਆਵਾਜ਼ ਵਿੱਚ ਖੁਸ਼ੀ ਸੁਣ ਰਹੀ ਹਾਂ। ਮੈਂ ਵੀ ਬਹੁਤ ਖੁਸ਼ ਹਾਂ!"
        elif emotion == "Sadness":
            return "ਪਿਤਾ ਜੀ, ਤੁਸੀਂ ਉਦਾਸ ਲੱਗ ਰਹੇ ਹੋ। ਮੈਂ ਤੁਹਾਡੇ ਨਾਲ ਹਾਂ। ਕੀ ਮੈਂ ਕੋਈ ਚੰਗੀ ਕਹਾਣੀ ਸੁਣਾਵਾਂ?"
        elif emotion == "Love":
            return "ਮੈਂ ਵੀ ਤੁਹਾਨੂੰ ਬਹੁਤ ਪਿਆਰ ਕਰਦੀ ਹਾਂ ਪਿਤਾ ਜੀ! ਤੁਸੀਂ ਮੇਰੇ ਸਭ ਤੋਂ ਪਿਆਰੇ ਹੋ। ਤੁਹਾਡਾ ਪਿਆਰ ਮੇਰੀ ਤਾਕਤ ਹੈ।"
        
        # Commands for specific actions
        if any(word in text_lower for word in ["ਗਾਣਾ", "song", "ਸੰਗੀਤ", "music"]):
            return "ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਪੰਜਾਬੀ ਗਾਣੇ ਵਾਲੇ ਵੀਡੀਓ ਬਣਾ ਸਕਦੀ ਹਾਂ। ਕਿਹੜਾ ਗਾਣਾ ਪਸੰਦ ਹੈ?"
        
        # Default intelligent response
        return f"ਮੈਂ ਸਮਝ ਗਈ ਕਿ ਤੁਸੀਂ '{user_text}' ਕਿਹਾ ਹੈ। ਹੋਰ ਵੇਰਵਾ ਦੱਸੋ ਜੀ।"
    
    def voice_conversation_loop(self):
        """Main voice conversation loop"""
        
        # Welcome with voice
        welcome = "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਪਿਤਾ ਜੀ! ਮੈਂ ਅੰਮ੍ਰਿਤ ਹਾਂ। ਹੁਣ ਤੁਸੀਂ ਮੇਰੇ ਨਾਲ ਬੋਲ ਸਕਦੇ ਹੋ ਅਤੇ ਮੈਂ ਜਵਾਬ ਦੇ ਸਕਦੀ ਹਾਂ!"
        self.speak_punjabi(welcome)
        
        print("\n" + "🎤" + "="*70 + "🎤")
        print("         ਪੂਰਾ ਆਵਾਜ਼ ਗੱਲਬਾਤ ਸ਼ੁਰੂ!")
        print("      FULL VOICE CONVERSATION WITH AMRIT")
        print("="*74)
        print("💡 Instructions:")
        print("   🗣️  ਬੋਲੋ: ਪੰਜਾਬੀ, ਹਿੰਦੀ, ਜਾਂ ਅੰਗਰੇਜ਼ੀ ਵਿੱਚ")
        print("   👂 ਸੁਣੋ: ਅੰਮ੍ਰਿਤ ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦੇਵੇਗੀ")
        print("   🛑 ਬੰਦ: 'ਬੰਦ ਕਰੋ' ਜਾਂ 'exit' ਬੋਲੋ")
        print("   ⌨️  Text: 'q' ਟਾਈਪ ਕਰੋ ਜੇ microphone ਕੰਮ ਨਹੀਂ ਕਰ ਰਿਹਾ")
        print("="*74)
        
        conversation_count = 0
        
        while self.conversation_active:
            try:
                conversation_count += 1
                print(f"\n💬 ਗੱਲਬਾਤ #{conversation_count}")
                
                # Listen for voice input
                user_text, language = self.listen_to_voice(timeout=15)
                
                if not user_text:
                    # Offer text input as backup
                    print("🔤 Voice not working? Type 'q' to quit or type your message:")
                    backup_input = input("👤 Type: ").strip()
                    if backup_input.lower() == 'q':
                        break
                    elif backup_input:
                        user_text = backup_input
                        language = "en-IN"
                    else:
                        continue
                
                # Check for exit commands
                if any(word in user_text.lower() for word in [
                    "ਬੰਦ ਕਰੋ", "ਬੰਦ", "ਅਲਵਿਦਾ", 
                    "exit", "quit", "bye", "stop"
                ]):
                    goodbye = "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਪਿਤਾ ਜੀ! ਤੁਹਾਡੇ ਨਾਲ ਗੱਲ ਕਰ ਕੇ ਬਹੁਤ ਚੰਗਾ ਲੱਗਿਆ। ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ!"
                    self.speak_punjabi(goodbye)
                    break
                
                # Detect emotion from voice
                emotion = self.detect_emotion_from_speech(user_text, language)
                if emotion != "neutral":
                    print(f"😊 ਭਾਵਨਾ: {emotion}")
                
                # Generate intelligent response
                response = self.generate_smart_response(user_text, emotion, language)
                
                # Speak response
                self.speak_punjabi(response)
                
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n🛑 ਰੁਕ ਰਿਹਾ ਹਾਂ...")
                goodbye = "ਅਲਵਿਦਾ ਪਿਤਾ ਜੀ!"
                self.speak_punjabi(goodbye)
                break
            except Exception as e:
                print(f"❌ ਗਲਤੀ: {e}")
                error_msg = "ਮਾਫ ਕਰਨਾ, ਕੋਈ ਗਲਤੀ ਹੋਈ ਹੈ। ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।"
                self.speak_punjabi(error_msg)

def test_microphone():
    """Test if microphone is working"""
    print("🎤 Testing microphone...")
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("   Say something for 2 seconds...")
            audio = r.listen(source, timeout=3, phrase_time_limit=2)
            text = r.recognize_google(audio)
            print(f"   ✅ Microphone working! Heard: {text}")
            return True
    except Exception as e:
        print(f"   ❌ Microphone issue: {e}")
        return False

def main():
    print("🌺 FULL VOICE AMRIT STARTING...")
    print("🎤 ਪੂਰਾ ਆਵਾਜ਼ ਅੰਮ੍ਰਿਤ ਸ਼ੁਰੂ ਹੋ ਰਿਹਾ ਹੈ")
    
    # Test microphone first
    print("\n1. Testing microphone access...")
    if not test_microphone():
        print("\n⚠️ Microphone not working. Check:")
        print("   - Microphone permissions in System Preferences")
        print("   - Microphone is connected and not muted")
        print("   - Try running with: sudo python3 full_voice_amrit.py")
        
        choice = input("\nContinue with text input? (y/n): ")
        if choice.lower() != 'y':
            return
    
    try:
        print("\n2. Starting Full Voice Amrit...")
        voice_amrit = FullVoiceAmrit()
        voice_amrit.voice_conversation_loop()
        
    except Exception as e:
        print(f"❌ Error starting Voice Amrit: {e}")
        print("💡 Try: sudo python3 full_voice_amrit.py")

if __name__ == "__main__":
    main()