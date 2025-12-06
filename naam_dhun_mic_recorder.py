"""
Naam Dhun Microphone Recorder & Nano Compressor
Records 1-minute Naam Dhun from microphone, compresses to nano MP3, and explains how to use as tanpura base for all ragas.
"""
import sounddevice as sd
import numpy as np
import wave
from pydub import AudioSegment
import os

def record_microphone(filename, duration=60, sample_rate=44100):
    print(f"Recording microphone for {duration} seconds...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    audio = (audio * 32767).astype(np.int16)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    print(f"Saved raw WAV: {filename}")

def compress_to_nano_mp3(wav_file, mp3_file, bitrate="64k"):
    audio = AudioSegment.from_wav(wav_file)
    audio.export(mp3_file, format="mp3", bitrate=bitrate)
    print(f"Compressed to nano MP3: {mp3_file}")

def explain_usage():
    print("""
How to use your Naam Dhun nano clip as tanpura base for all ragas:
1. Play your nano MP3 in any tanpura app or audio player.
2. Set the pitch (Sa) in the app to match your raga.
3. Loop the clip for continuous drone.
4. Sing or play any raga over the Naam Dhun base.
5. For best results, tune your recording to the raga's tonic using Audacity or a tanpura app.
""")

if __name__ == "__main__":
    wav_file = "naam_dhun_mic_60s.wav"
    mp3_file = "naam_dhun_mic_nano.mp3"
    record_microphone(wav_file, duration=60)
    compress_to_nano_mp3(wav_file, mp3_file, bitrate="64k")
    explain_usage()
    print("All done! Your nano Naam Dhun is ready for all ragas.")
