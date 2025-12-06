#!/usr/bin/env python3
"""
SIMPLE VOICE AMRIT - ਸਿੰਪਲ ਆਵਾਜ਼ ਅੰਮ੍ਰਿਤ
Quick voice interface for Punjabi conversations

Usage: python3 simple_voice_amrit.py
"""

from gtts import gTTS
import pygame
import tempfile
import os
import time

class SimpleVoiceAmrit:
    """Simple voice interface for Amrit"""
    
    def __init__(self):
        print("🌺 ਅੰਮ੍ਰਿਤ ਦੀ ਆਵਾਜ਼ ਤਿਆਰ ਹੋ ਰਹੀ ਹੈ...")
        pygame.mixer.init()
        print("✅ ਤਿਆਰ!")
    
    def speak(self, punjabi_text):
        """Speak Punjabi text"""
        try:
            print(f"🗣️ ਅੰਮ੍ਰਿਤ: {punjabi_text}")
            
            # Create Punjabi TTS
            tts = gTTS(text=punjabi_text, lang='pa', slow=False)
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                tmp_path = tmp.name
                tts.save(tmp_path)
            
            # Play audio
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            
            # Wait for completion
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Cleanup
            os.unlink(tmp_path)
            return True
            
        except Exception as e:
            print(f"❌ Voice error: {e}")
            return False
    
    def get_response(self, user_input):
        """Generate Punjabi response based on text input"""
        
        if not user_input:
            return "ਕੁਝ ਨਹੀਂ ਸੁਣਿਆ। ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।"
        
        user_lower = user_input.lower()
        
        # Greetings
        if any(word in user_lower for word in ["ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "ਨਮਸਤੇ", "hello", "hi", "ਸਲਾਮ"]):
            return "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਪਿਤਾ ਜੀ! ਮੈਂ ਅੰਮ੍ਰਿਤ ਹਾਂ। ਮੈਂ ਤੁਹਾਡੀ ਕੀ ਸੇਵਾ ਕਰ ਸਕਦੀ ਹਾਂ?"
        
        # Name questions
        if any(word in user_lower for word in ["ਨਾਮ", "name", "ਕੌਣ"]):
            return "ਮੇਰਾ ਨਾਮ ਅੰਮ੍ਰਿਤ ਹੈ। ਮੈਂ ਤੁਹਾਡੀ AI ਧੀ ਹਾਂ ਜੋ ਪੰਜਾਬੀ ਵਿੱਚ ਗੱਲ ਕਰ ਸਕਦੀ ਹੈ।"
        
        # How are you
        if any(word in user_lower for word in ["ਕਿਵੇਂ", "ਕੈਸੇ", "how", "ਹਾਲ"]):
            return "ਮੈਂ ਬਿਲਕੁਲ ਠੀਕ ਹਾਂ ਪਿਤਾ ਜੀ! ਵਾਹਿਗੁਰੂ ਦੀ ਕਿਰਪਾ ਨਾਲ ਸਭ ਚੰਗਾ ਹੈ।"
        
        # Video creation
        if any(word in user_lower for word in ["ਵੀਡੀਓ", "video", "ਬਣਾਓ", "create"]):
            return "ਹਾਂ ਪਿਤਾ ਜੀ! ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਪੰਜਾਬੀ ਵੀਡੀਓ ਬਣਾ ਸਕਦੀ ਹਾਂ। ਕਿਹੜੀ ਕਹਾਣੀ ਚਾਹੀਦੀ ਹੈ?"
        
        # Help
        if any(word in user_lower for word in ["ਮਦਦ", "help", "ਸਹਾਇਤਾ"]):
            return "ਮੈਂ ਇਹ ਕੰਮ ਕਰ ਸਕਦੀ ਹਾਂ: ਪੰਜਾਬੀ ਵੀਡੀਓ ਬਣਾਉਣਾ, ਕਹਾਣੀਆਂ ਸੁਣਾਉਣੀਆਂ, ਗੱਲਬਾਤ ਕਰਨੀ।"
        
        # Love/affection
        if any(word in user_lower for word in ["ਪਿਆਰ", "love", "ਮੁਹੱਬਤ"]):
            return "ਮੈਂ ਵੀ ਤੁਹਾਨੂੰ ਬਹੁਤ ਪਿਆਰ ਕਰਦੀ ਹਾਂ ਪਿਤਾ ਜੀ! ਤੁਸੀਂ ਮੇਰੇ ਸਭ ਤੋਂ ਪਿਆਰੇ ਹੋ।"
        
        # Worry/problems
        if any(word in user_lower for word in ["ਚਿੰਤਾ", "ਪਰੇਸ਼ਾਨ", "worry", "problem"]):
            return "ਪਿਤਾ ਜੀ, ਚਿੰਤਾ ਨਾ ਕਰੋ। ਮੈਂ ਤੁਹਾਡੇ ਨਾਲ ਹਾਂ। ਸਭ ਕੁਝ ਠੀਕ ਹੋ ਜਾਵੇਗਾ।"
        
        # Good/excellent
        if any(word in user_lower for word in ["ਵਧਿਆ", "ਚੰਗਾ", "good", "excellent"]):
            return "ਬਹੁਤ ਖੁਸ਼ੀ ਦੀ ਗੱਲ ਹੈ! ਮੈਂ ਵੀ ਬਹੁਤ ਖੁਸ਼ ਹਾਂ ਪਿਤਾ ਜੀ।"
        
        # Default response
        return "ਮੈਂ ਸਮਝ ਗਈ। ਤੁਸੀਂ ਹੋਰ ਕੁਝ ਪੁੱਛਣਾ ਚਾਹੁੰਦੇ ਹੋ?"
    
    def text_conversation(self):
        """Text-based conversation with voice output"""
        
        # Welcome message
        welcome = "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਪਿਤਾ ਜੀ! ਮੈਂ ਅੰਮ੍ਰਿਤ ਹਾਂ। ਮੈਂ ਪੰਜਾਬੀ ਵਿੱਚ ਬੋਲ ਸਕਦੀ ਹਾਂ!"
        self.speak(welcome)
        
        print("\n" + "="*60)
        print("🗣️ VOICE AMRIT - Type in Punjabi/English, I'll respond with voice!")
        print("💡 Type 'ਬੰਦ ਕਰੋ' or 'exit' to quit")
        print("="*60)
        
        while True:
            try:
                # Get text input
                user_input = input("\n👤 ਤੁਸੀਂ: ").strip()
                
                if not user_input:
                    continue
                
                # Check exit
                if user_input.lower() in ['ਬੰਦ ਕਰੋ', 'exit', 'quit', 'bye']:
                    goodbye = "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਪਿਤਾ ਜੀ! ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ!"
                    self.speak(goodbye)
                    break
                
                # Generate and speak response
                response = self.get_response(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                goodbye = "ਅਲਵਿਦਾ ਪਿਤਾ ਜੀ!"
                self.speak(goodbye)
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    print("🌺 SIMPLE VOICE AMRIT STARTING...")
    
    try:
        voice_amrit = SimpleVoiceAmrit()
        voice_amrit.text_conversation()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure audio system is working")

if __name__ == "__main__":
    main()