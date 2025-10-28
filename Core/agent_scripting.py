import speech_recognition as sr
import pyttsx3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - Scripting Agent - %(message)s')

class ScriptingAgent:
    """
    Handles Voice-to-Text conversion and intelligent script generation.
    It takes raw input and refines it into a structured movie scene.
    """
    
    def __init__(self, name="Scripting_Agent"):
        self.name = name
        self.recognizer = sr.Recognizer()
        self.speech_engine = pyttsx3.init()
        logging.info(f"{self.name} initialized. Ready to listen and generate scripts.")

    def text_to_speech(self, text):
        """Converts text back into speech for the user (feedback)."""
        logging.info(f"Speaking: '{text}'")
        self.speech_engine.say(text)
        self.speech_engine.runAndWait()

    def listen_for_command(self):
        """Records user's voice input from the microphone."""
        with sr.Microphone() as source:
            self.text_to_speech("Please speak your script idea now...")
            self.recognizer.adjust_for_ambient_noise(source) # Adjusting to background noise
            logging.info("Listening...")
            
            try:
                audio = self.recognizer.listen(source, timeout=5)
                # Use Google's API for reliable transcription
                raw_text = self.recognizer.recognize_google(audio)
                logging.info(f"Raw Input Received: {raw_text}")
                return raw_text
            
            except sr.WaitTimeoutError:
                logging.error("No speech detected within the time limit.")
                return "ERROR: Timeout"
            except sr.UnknownValueError:
                logging.error("Could not understand audio.")
                return "ERROR: Unknown"
            except Exception as e:
                logging.error(f"Microphone Error: {e}")
                return "ERROR: Mic Failed"

    def refine_to_script(self, raw_text):
        """
        The core intelligence logic: takes raw text and applies structure.
        This is where the agent converts an 'idea' into a structured 'scene'.
        """
        if "ERROR" in raw_text:
            return None
        
        logging.info("Refining raw input into a structured script...")
        time.sleep(1) # Simulate complex reasoning

        # Simple logic: We will expand this greatly later!
        script = {
            "title": f"Scene_001__{raw_text[:20].replace(' ', '_')}",
            "setting": "A peaceful futuristic Punjabi village.",
            "dialogue": [
                {"character": "Gurpreet Singh", "line": f"Mastermind, I said: '{raw_text}'."},
                {"character": "Amrit Kaur", "line": "Script analyzed. Generating visual plan."},
            ]
        }
        logging.info("Script structure generated successfully.")
        return script

# Test the agent (This section only runs when the file is run directly)
if __name__ == "__main__":
    script_agent = ScriptingAgent()
    
    # 1. Listen for voice command
    user_idea = script_agent.listen_for_command()
    
    # 2. Refine the idea into a script
    final_script = script_agent.refine_to_script(user_idea)
    
    if final_script:
        import json
        logging.info(f"Final Script Output:\n{json.dumps(final_script, indent=4)}")
        script_agent.text_to_speech("Script is ready for the visual team.")

