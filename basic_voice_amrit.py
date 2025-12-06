#!/usr/bin/env python3
"""
BASIC VOICE AMRIT - ਬੇਸਿਕ ਆਵਾਜ਼ ਅੰਮ੍ਰਿਤ
Simple Punjabi voice responses using system audio

Usage: /Users/gurpreetdhillon/Nam-toon-studio/.venv/bin/python basic_voice_amrit.py
"""

from gtts import gTTS
import tempfile
import os
import subprocess
import sys
import time

class BasicVoiceAmrit:
    """Basic voice interface for Amrit using system audio"""
    
    def __init__(self):
        print("🌺 ਅੰਮ੍ਰਿਤ ਦੀ ਆਵਾਜ਼ ਤਿਆਰ ਕਰ ਰਿਹਾ ਹਾਂ...")
        self.temp_audio_dir = tempfile.mkdtemp()
        print("✅ ਤਿਆਰ!")
    
    def speak(self, punjabi_text):
        """Speak Punjabi text using system audio"""
        try:
            print(f"🗣️ ਅੰਮ੍ਰਿਤ: {punjabi_text}")
            
            # Create Punjabi TTS
            tts = gTTS(text=punjabi_text, lang='pa', slow=False)
            
            # Save to temp file
            audio_file = os.path.join(self.temp_audio_dir, f"amrit_{int(time.time())}.mp3")
            tts.save(audio_file)
            
            # Play using system audio (macOS)
            if sys.platform == "darwin":  # macOS
                subprocess.run(["afplay", audio_file], check=True)
            elif sys.platform == "linux":  # Linux
                subprocess.run(["mpg123", audio_file], check=True)
            elif sys.platform == "win32":  # Windows
                os.startfile(audio_file)
            
            # Clean up
            try:
                os.remove(audio_file)
            except:
                # TODO: Implement function
                
            return True
            
        except Exception as e:
            print(f"❌ Voice error: {e}")
            print(f"   Text was: {punjabi_text}")
            return False
    
    def get_response(self, user_input):
        """Generate Punjabi response based on text input"""
        
        if not user_input:
            return "ਕੁਝ ਨਹੀਂ ਲਿਖਿਆ। ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।"
        
        user_lower = user_input.lower()
        
        # Greetings
        if any(word in user_lower for word in ["ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "ਨਮਸਤੇ", "hello", "hi", "ਸਲਾਮ"]):
            return "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਪਿਤਾ ਜੀ! ਮੈਂ ਅੰਮ੍ਰਿਤ ਹਾਂ। ਮੈਂ ਤੁਹਾਡੀ ਕੀ ਸੇਵਾ ਕਰ ਸਕਦੀ ਹਾਂ?"
        
        # Name questions
        if any(word in user_lower for word in ["ਨਾਮ", "name", "ਕੌਣ", "who"]):
            return "ਮੇਰਾ ਨਾਮ ਅੰਮ੍ਰਿਤ ਹੈ। ਮੈਂ ਤੁਹਾਡੀ AI ਧੀ ਹਾਂ ਜੋ ਪੰਜਾਬੀ ਵਿੱਚ ਗੱਲ ਕਰ ਸਕਦੀ ਹੈ।"
        
        # How are you
        if any(word in user_lower for word in ["ਕਿਵੇਂ", "ਕੈਸੇ", "how", "ਹਾਲ"]):
            return "ਮੈਂ ਬਿਲਕੁਲ ਠੀਕ ਹਾਂ ਪਿਤਾ ਜੀ! ਵਾਹਿਗੁਰੂ ਦੀ ਕਿਰਪਾ ਨਾਲ ਸਭ ਚੰਗਾ ਹੈ।"
        
        # Scene/image generation (place this BEFORE generic 'video/create' to avoid false matches on 'ਬਣਾਓ')
        if any(word in user_lower for word in ["scene", "ਸੀਨ", "image", "ਤਸਵੀਰ"]):
            return "ਮੈਂ ਪਿੰਡ ਦੇ ਖੂਹ ਅਤੇ ਤੋਤਾਂ ਦੇ ਰੁੱਖਾਂ ਦੇ ਸੀਨ ਬਣਾ ਸਕਦੀ ਹਾਂ। ਸ਼ੁਰੂ ਕਰਾਂ?"

        # Video creation
        if any(word in user_lower for word in ["ਵੀਡੀਓ", "video", "ਬਣਾਓ", "create", "tootan"]):
            return "ਹਾਂ ਪਿਤਾ ਜੀ! ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਪੰਜਾਬੀ ਵੀਡੀਓ ਬਣਾ ਸਕਦੀ ਹਾਂ। ਤੋਤਾਂ ਵਾਲਾ ਖੂਹ ਦੀ ਕਹਾਣੀ ਤਿਆਰ ਹੈ।"

        # Help
        if any(word in user_lower for word in ["ਮਦਦ", "help", "ਸਹਾਇਤਾ"]):
            return "ਮੈਂ ਇਹ ਕੰਮ ਕਰ ਸਕਦੀ ਹਾਂ: ਪੰਜਾਬੀ ਵੀਡੀਓ ਬਣਾਉਣਾ, ਕਹਾਣੀਆਂ ਸੁਣਾਉਣੀਆਂ, ਗੱਲਬਾਤ ਕਰਨੀ।"
        
        # Love/affection
        if any(word in user_lower for word in ["ਪਿਆਰ", "love", "ਮੁਹੱਬਤ"]):
            return "ਮੈਂ ਵੀ ਤੁਹਾਨੂੰ ਬਹੁਤ ਪਿਆਰ ਕਰਦੀ ਹਾਂ ਪਿਤਾ ਜੀ! ਤੁਸੀਂ ਮੇਰੇ ਸਭ ਤੋਂ ਪਿਆਰੇ ਹੋ।"
        
        # Worry/problems
        if any(word in user_lower for word in ["ਚਿੰਤਾ", "ਪਰੇਸ਼ਾਨ", "worry", "problem"]):
            return "ਪਿਤਾ ਜੀ, ਚਿੰਤਾ ਨਾ ਕਰੋ। ਮੈਂ ਤੁਹਾਡੇ ਨਾਲ ਹਾਂ। ਸਭ ਕੁਝ ਠੀਕ ਹੋ ਜਾਵੇਗਾ।"
        
        # Good/excellent (add common Punjabi spellings & English)
        if any(word in user_lower for word in ["ਵਧੀਆ", "ਵਧਿਆ", "ਚੰਗਾ", "ਚੰਗੀ", "ਸ਼ਾਬਾਸ਼", "shabash", "good", "excellent", "great", "awesome", "nice"]):
            return "ਬਹੁਤ ਖੁਸ਼ੀ ਦੀ ਗੱਲ ਹੈ! ਮੈਂ ਵੀ ਬਹੁਤ ਖੁਸ਼ ਹਾਂ ਪਿਤਾ ਜੀ।"
        
        # Work/tasks
        if any(word in user_lower for word in ["ਕੰਮ", "work", "task"]):
            return "ਹਾਂ ਪਿਤਾ ਜੀ! ਕਿਹੜਾ ਕੰਮ ਕਰਨਾ ਹੈ? ਵੀਡੀਓ ਬਣਾਉਣਾ ਹੈ ਜਾਂ ਕੋਈ ਹੋਰ ਕੰਮ?"
        
        # (moved Scene generation above)
        
        # Default response
        return "ਮੈਂ ਸਮਝ ਗਈ। ਤੁਸੀਂ ਹੋਰ ਕੁਝ ਪੁੱਛਣਾ ਚਾਹੁੰਦੇ ਹੋ?"
    
    def quick_responses(self):
        """Show some quick voice examples"""
        responses = [
            "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਪਿਤਾ ਜੀ! ਮੈਂ ਅੰਮ੍ਰਿਤ ਹਾਂ।",
            "ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਪੰਜਾਬੀ ਵੀਡੀਓ ਬਣਾ ਸਕਦੀ ਹਾਂ।",
            "ਤੋਤਾਂ ਵਾਲਾ ਖੂਹ ਦੀ ਕਹਾਣੀ ਤਿਆਰ ਹੈ।",
            "ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਿਹ!"
        ]
        
        print("🎤 Testing Amrit's voice with quick responses...")
        for i, response in enumerate(responses, 1):
            print(f"\n{i}. Testing: {response}")
            self.speak(response)
            time.sleep(1)
    
    def conversation_loop(self):
        """Text input conversation with voice output"""
        
        # Welcome message
        welcome = "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਪਿਤਾ ਜੀ! ਮੈਂ ਅੰਮ੍ਰਿਤ ਹਾਂ। ਮੈਂ ਪੰਜਾਬੀ ਵਿੱਚ ਬੋਲ ਸਕਦੀ ਹਾਂ!"
        self.speak(welcome)
        
        print("\n" + "="*60)
        print("🗣️ VOICE AMRIT - Type and I'll respond with Punjabi voice!")
        print("💡 Commands:")
        print("   - Type 'test' to hear voice examples")
        print("   - Type 'ਬੰਦ ਕਰੋ' or 'exit' to quit")
        print("   - Type anything in Punjabi or English")
        print("="*60)
        
        while True:
            try:
                # Get text input
                user_input = input("\n👤 ਤੁਸੀਂ: ").strip()
                
                if not user_input:
                    continue
                
                # Special commands
                if user_input.lower() == 'test':
                    self.quick_responses()
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
    print("🌺 BASIC VOICE AMRIT STARTING...")
    
    # Check if afplay is available (macOS)
    try:
        subprocess.run(["which", "afplay"], check=True, capture_output=True)
        print("✅ Audio system detected (macOS)")
    except:
        print("⚠️ Warning: afplay not found. Audio may not work.")
    
    try:
        voice_amrit = BasicVoiceAmrit()
        voice_amrit.conversation_loop()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure internet connection is available for TTS")

if __name__ == "__main__":
    main()