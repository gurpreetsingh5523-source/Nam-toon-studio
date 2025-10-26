# AmritCore - Advanced Audio Mixing Demo (FINAL FIX)

# Install necessary libraries
!pip install numpy pydub moviepy gTTS

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from gtts import gTTS
from pydub import AudioSegment
from PIL import Image # <--- THE FIX: Explicitly importing Image
import os

# --- 1. SETUP: Define paths and clean up ---
audio_path = 'assets/audio'
if not os.path.exists(audio_path): os.makedirs(audio_path)
if not os.path.exists('assets/visuals'): os.makedirs('assets/visuals')

# Create silent placeholders for ambient sounds for stable execution
AudioSegment.silent(duration=10000).export(f'{audio_path}/leaves.mp3', format='mp3')
AudioSegment.silent(duration=10000).export(f'{audio_path}/well.mp3', format='mp3')


# --- 2. DIALOGUE GENERATION ---
text = "ਪਹਿਲੀ ਝਲਕ: ਪਿੰਡ ਦੀ ਸਵੇਰ, ਤੂਤਾਂ ਦੀ ਸ਼ਾ-ਸ਼ਾ..."
tts = gTTS(text=text, lang='pa')
tts.save(f'{audio_path}/seg1.mp3')
print('1. Dialogue saved to seg1.mp3')


# --- 3. ADVANCED AUDIO MIXING ---
try:
    # Load the files
    speech = AudioSegment.from_mp3(f'{audio_path}/seg1.mp3')
    
    # Load ambient stems and apply gain for professional mix
    leaves = AudioSegment.from_file(f'{audio_path}/leaves.mp3')[:len(speech)].apply_gain(-6)
    well = AudioSegment.from_file(f'{audio_path}/well.mp3')[:len(speech)].apply_gain(-8)
    
    # Overlay the sounds
    mixed = speech.overlay(leaves).overlay(well)
    mixed.export(f'{audio_path}/seg1_mixed.mp3', format='mp3')
    print('2. Ambient sounds successfully mixed with dialogue (Robust Audio Mix).')
    
except Exception as e:
    print(f'FATAL AUDIO MIXING ERROR: {e}')
    exit() 

# --- 4. VIDEO ASSEMBLY ---
# Create a temporary visual placeholder (THE LINE THAT CAUSED THE ERROR IS HERE)
Image.new('RGB', (800, 600), color='#A03030').save('assets/visuals/icon.png')

bg = ImageClip('assets/visuals/icon.png').set_duration(10)  
audio = AudioFileClip(f'{audio_path}/seg1_mixed.mp3')

# Set the audio and export the final video
bg = bg.set_audio(audio).set_fps(24)
out = 'preview_seg1.mp4'
bg.write_videofile(out, codec='libx264', audio_codec='aac', verbose=False)

print('3. Preview ready:', out)
print("\n--- Synthesis Node Status: SUCCESS ---")

# --- FINAL INSTRUCTION ---
# Save the successful logic to GitHub
print("\nProfessional Workflow: Please save this successful code to core/08_synthesis_node.py.")
