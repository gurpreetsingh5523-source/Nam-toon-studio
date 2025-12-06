#!/usr/bin/env python3
"""
🎤 VOICE SYSTEM UNIFIED - ਸਾਰੇ Voice modules ਇੱਕ ਥਾਂ

Consolidated from multiple voice files:
- simple_voice_amrit.py (143 lines)
- basic_voice_amrit.py (188 lines)
- full_voice_amrit.py (fragments)
- talk_to_amrit.py (157 lines)
- advanced_ai_voice_tutor.py (179 lines)

All voice capabilities unified with shared audio engine
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import tempfile

logging.basicConfig(level=logging.INFO, format='🎤 [VOICE] %(message)s')
log = logging.getLogger(__name__)

# Try imports
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    log.warning("gTTS not available - install with: pip install gtts")

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    log.warning("SpeechRecognition not available - install with: pip install SpeechRecognition")

try:
    from pydub import AudioSegment
    from pydub.playback import play
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


class SharedAudioEngine:
    """Shared audio processing engine - ਸਾਂਝਾ audio engine"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "amrit_voice"
        self.temp_dir.mkdir(exist_ok=True)
        
        self.supported_languages = {
            'punjabi': 'pa',
            'english': 'en',
            'hindi': 'hi'
        }
        
        log.info("✅ Shared Audio Engine initialized")
    
    def text_to_speech(self, text: str, language: str = 'pa', slow: bool = False) -> Optional[Path]:
        """Convert text to speech"""
        if not GTTS_AVAILABLE:
            log.error("gTTS not available")
            return None
        
        try:
            tts = gTTS(text=text, lang=language, slow=slow)
            output_path = self.temp_dir / f"speech_{hash(text)}.mp3"
            tts.save(str(output_path))
            log.info(f"🎵 Generated speech: {output_path.name}")
            return output_path
        except Exception as e:
            log.error(f"TTS failed: {e}")
            return None
    
    def speech_to_text(self, audio_file: Optional[Path] = None) -> Optional[str]:
        """Convert speech to text (from mic or file)"""
        if not SR_AVAILABLE:
            log.error("SpeechRecognition not available")
            return None
        
        recognizer = sr.Recognizer()
        
        try:
            if audio_file:
                # From file
                with sr.AudioFile(str(audio_file)) as source:
                    audio = recognizer.record(source)
            else:
                # From microphone
                with sr.Microphone() as source:
                    log.info("🎤 Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5)
            
            # Recognize
            text = recognizer.recognize_google(audio, language='pa-IN')
            log.info(f"🎧 Heard: {text}")
            return text
        
        except sr.UnknownValueError:
            log.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            log.error(f"Recognition service error: {e}")
            return None
        except Exception as e:
            log.error(f"STT failed: {e}")
            return None
    
    def play_audio(self, audio_path: Path):
        """Play audio file"""
        if not PYDUB_AVAILABLE:
            log.error("pydub not available")
            return
        
        try:
            audio = AudioSegment.from_file(str(audio_path))
            play(audio)
        except Exception as e:
            log.error(f"Playback failed: {e}")


class SimpleVoiceAmrit:
    """Simple voice interaction - ਸਧਾਰਨ voice"""
    
    def __init__(self, audio_engine: SharedAudioEngine):
        self.audio = audio_engine
        log.info("✅ Simple Voice initialized")
    
    def speak(self, text: str, language: str = 'pa'):
        """Speak text"""
        audio_path = self.audio.text_to_speech(text, language)
        if audio_path:
            self.audio.play_audio(audio_path)
    
    def listen(self) -> Optional[str]:
        """Listen and return text"""
        return self.audio.speech_to_text()


class BasicVoiceAmrit:
    """Basic voice with conversation - ਬੁਨਿਆਦੀ voice + ਗੱਲਬਾਤ"""
    
    def __init__(self, audio_engine: SharedAudioEngine):
        self.audio = audio_engine
        self.conversation_history = []
        log.info("✅ Basic Voice initialized")
    
    def speak(self, text: str, language: str = 'pa'):
        """Speak and log"""
        self.conversation_history.append({'type': 'speak', 'text': text})
        audio_path = self.audio.text_to_speech(text, language)
        if audio_path:
            self.audio.play_audio(audio_path)
    
    def listen_and_respond(self, response_callback) -> Optional[str]:
        """Listen, respond, and track conversation"""
        user_input = self.audio.speech_to_text()
        if user_input:
            self.conversation_history.append({'type': 'user', 'text': user_input})
            
            # Get response from callback
            response = response_callback(user_input)
            self.speak(response)
            
            return user_input
        return None
    
    def get_conversation_history(self):
        """Get full conversation"""
        return self.conversation_history


class AdvancedVoiceTutor:
    """Advanced voice tutor - ਉੱਨਤ voice ਟਿਊਟਰ"""
    
    def __init__(self, audio_engine: SharedAudioEngine, brain_system=None):
        self.audio = audio_engine
        self.brain_system = brain_system
        self.lessons = []
        self.student_progress = {}
        log.info("✅ Advanced Voice Tutor initialized")
    
    def teach_lesson(self, topic: str, language: str = 'pa'):
        """Teach a lesson"""
        lesson = {
            'topic': topic,
            'content': f"ਆਓ {topic} ਬਾਰੇ ਸਿੱਖੀਏ...",
            'language': language
        }
        
        self.lessons.append(lesson)
        self.audio.text_to_speech(lesson['content'], language)
        log.info(f"📚 Teaching: {topic}")
    
    def quiz_student(self, question: str) -> Optional[str]:
        """Ask question and get answer"""
        # Speak question
        self.audio.text_to_speech(question, 'pa')
        
        # Listen for answer
        answer = self.audio.speech_to_text()
        
        if answer:
            self.student_progress[question] = answer
            log.info(f"✅ Student answered: {answer}")
        
        return answer
    
    def provide_feedback(self, is_correct: bool):
        """Give feedback"""
        if is_correct:
            feedback = "ਬਹੁਤ ਵਧੀਆ! ਸਹੀ ਜਵਾਬ!"
        else:
            feedback = "ਕੋਈ ਗੱਲ ਨਹੀਂ, ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ"
        
        self.audio.text_to_speech(feedback, 'pa')


class TalkToAmrit:
    """Full conversation system - ਪੂਰੀ ਗੱਲਬਾਤ"""
    
    def __init__(self, audio_engine: SharedAudioEngine, brain_system=None):
        self.audio = audio_engine
        self.brain_system = brain_system
        self.active = False
        log.info("✅ Talk To Amrit initialized")
    
    def start_conversation(self):
        """Start interactive conversation"""
        self.active = True
        
        greeting = "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਅੰਮ੍ਰਿਤ ਹਾਂ। ਤੁਸੀਂ ਕੀ ਪੁੱਛਣਾ ਚਾਹੁੰਦੇ ਹੋ?"
        self.audio.text_to_speech(greeting, 'pa')
        
        log.info("💬 Conversation started")
        
        while self.active:
            user_input = self.audio.speech_to_text()
            
            if not user_input:
                continue
            
            # Check for exit
            if any(word in user_input.lower() for word in ['ਬੰਦ', 'ਖਤਮ', 'exit', 'quit']):
                farewell = "ਫਿਰ ਮਿਲਾਂਗੇ! ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ!"
                self.audio.text_to_speech(farewell, 'pa')
                self.active = False
                break
            
            # Get response
            response = self.process_query(user_input)
            self.audio.text_to_speech(response, 'pa')
    
    def process_query(self, query: str) -> str:
        """Process user query and generate response"""
        if self.brain_system:
            # Use brain system
            return self.brain_system.query(query)
        else:
            # Simple response
            return f"ਤੁਸੀਂ ਪੁੱਛਿਆ: {query}. ਮੈਂ ਇਸ ਬਾਰੇ ਸੋਚ ਰਿਹਾ ਹਾਂ..."


class VoiceSystemUnified:
    """Unified Voice System - ਇਕਜੁੱਟ Voice System"""
    
    def __init__(self, brain_system=None):
        log.info("="*70)
        log.info("🎤 VOICE SYSTEM UNIFIED")
        log.info("   All voice modules interconnected")
        log.info("="*70)
        
        # Shared audio engine for all modules
        self.audio_engine = SharedAudioEngine()
        
        # Initialize all voice modules
        self.simple_voice = SimpleVoiceAmrit(self.audio_engine)
        self.basic_voice = BasicVoiceAmrit(self.audio_engine)
        self.tutor = AdvancedVoiceTutor(self.audio_engine, brain_system)
        self.conversation = TalkToAmrit(self.audio_engine, brain_system)
        
        self.brain_system = brain_system
        
        log.info("\n✅ ALL VOICE MODULES LOADED")
        log.info("   Sharing single audio engine for efficiency")
    
    def speak_simple(self, text: str, language: str = 'pa'):
        """Simple speech"""
        self.simple_voice.speak(text, language)
    
    def have_conversation(self):
        """Start full conversation"""
        self.conversation.start_conversation()
    
    def teach_lesson(self, topic: str):
        """Teach using voice tutor"""
        self.tutor.teach_lesson(topic)
    
    def demonstrate_capabilities(self):
        """Demonstrate all voice capabilities"""
        log.info("\n" + "="*70)
        log.info("🎙️ DEMONSTRATING VOICE CAPABILITIES")
        log.info("="*70)
        
        # 1. Simple speech
        log.info("\n📢 1. Simple Speech:")
        self.simple_voice.speak("ਇਹ ਸਧਾਰਨ ਬੋਲੀ ਹੈ", 'pa')
        
        # 2. Basic conversation
        log.info("\n💬 2. Basic Conversation:")
        self.basic_voice.speak("ਮੈਂ ਗੱਲਬਾਤ ਕਰ ਸਕਦਾ ਹਾਂ", 'pa')
        
        # 3. Teaching
        log.info("\n📚 3. Teaching Mode:")
        self.tutor.teach_lesson("ਪੰਜਾਬੀ ਭਾਸ਼ਾ")
        
        # 4. Full conversation (demo mode)
        log.info("\n🎤 4. Full Conversation:")
        log.info("   (Start with: have_conversation())")
        
        log.info("\n✅ All capabilities demonstrated!")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get voice system status"""
        return {
            'audio_engine': {
                'temp_dir': str(self.audio_engine.temp_dir),
                'languages': list(self.audio_engine.supported_languages.keys()),
                'gtts_available': GTTS_AVAILABLE,
                'speech_recognition': SR_AVAILABLE,
                'pydub_available': PYDUB_AVAILABLE
            },
            'modules': {
                'simple_voice': 'active',
                'basic_voice': 'active',
                'voice_tutor': 'active',
                'conversation': 'active'
            },
            'conversation_history': len(self.basic_voice.conversation_history),
            'lessons_taught': len(self.tutor.lessons)
        }


def main():
    """Main entry point"""
    
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           🎤 VOICE SYSTEM UNIFIED                                 ║
║           ਸਾਰੇ Voice Modules ਇੱਕ ਥਾਂ                             ║
║                                                                   ║
║   Previously 5 voice files (143-188 lines each)                   ║
║   Now 1 unified system with shared audio engine                   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Create unified voice system
    voice = VoiceSystemUnified()
    
    # Demonstrate capabilities
    voice.demonstrate_capabilities()
    
    # Show system status
    log.info("\n" + "="*70)
    log.info("📊 VOICE SYSTEM STATUS")
    log.info("="*70)
    status = voice.get_system_status()
    for module, info in status.items():
        log.info(f"\n{module}:")
        if isinstance(info, dict):
            for key, value in info.items():
                log.info(f"   {key}: {value}")
        else:
            log.info(f"   {info}")
    
    log.info("\n" + "="*70)
    log.info("✅ VOICE SYSTEM UNIFIED READY!")
    log.info("   Use: voice.have_conversation() to start talking")
    log.info("="*70)


if __name__ == "__main__":
    main()
