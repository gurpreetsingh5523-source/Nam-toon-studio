"""
Naam Dhun & Healing Frequencies Generator
Generates 30-second audio clips for Naam Dhun (spiritual chant) and healing frequencies.

Gurbani Teachings:
- Nimmarta (Humility): "Nanak Neech Kahai Veechar" – Har audio vich nimmarta te seva di bhavna.
- Protection: "Rakhe Rakhanhaar aap ubaariyan" – Healing frequencies te Naam Dhun vich spiritual protection.
- Loving Service (Seva): "Seva karat hoey nihkam" – Audio seva de roop vich, sab nu pyaar te shanti dena.
Har generated audio humble, protective, te loving hovega.
"""
import numpy as np
import wave
import os
from gtts import gTTS

def generate_sine_wave(freq, duration, sample_rate=44100, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave_data = amplitude * np.sin(2 * np.pi * freq * t)
    return wave_data

def save_wave(filename, wave_data, sample_rate=44100):
    wave_data = (wave_data * 32767).astype(np.int16)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(wave_data.tobytes())

def generate_naam_dhun(filename, duration=30):
    # Naam Dhun: spiritual chant (e.g., "Satnaam Waheguru")
    chant = "Satnaam Waheguru"
    # Gurbani-inspired message
    gurbani_message = (
        "Nanak Neech Kahai Veechar: Har audio vich nimmarta. "
        "Rakhe Rakhanhaar: Spiritual protection. "
        "Seva: Loving service for all listeners."
    )
    tts = gTTS(text=f"{chant}. {gurbani_message}", lang='pa')
    tts.save("_chant.mp3")
    # Overlay chant on healing frequency
    freq = 528  # Healing frequency (Hz)
    wave_data = generate_sine_wave(freq, duration)
    save_wave("_healing.wav", wave_data)
    # Combine chant and healing frequency (simple overlay)
    try:
        from pydub import AudioSegment
        chant_audio = AudioSegment.from_mp3("_chant.mp3")
        healing_audio = AudioSegment.from_wav("_healing.wav")
        chant_audio = chant_audio[:duration*1000]
        healing_audio = healing_audio[:duration*1000]
        combined = healing_audio.overlay(chant_audio)
        combined.export(filename, format="wav")
        os.remove("_chant.mp3")
        os.remove("_healing.wav")
    except ImportError:n
        print("Install pydub for audio overlay: pip install pydub")
        save_wave(filename, wave_data)

def generate_healing_frequency(filename, freq=528, duration=30):
    wave_data = generate_sine_wave(freq, duration)
    save_wave(filename, wave_data)

if __name__ == "__main__":
    generate_naam_dhun("naam_dhun_60s.wav", duration=60)
    generate_healing_frequency("healing_528hz_60s.wav", freq=528, duration=60)
    print("Generated 1-minute naam dhun and healing frequency audio files.")
