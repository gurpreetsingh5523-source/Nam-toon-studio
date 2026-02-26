"""
ਆਤਮ ਨਿਰਭਰ Audio Mixer
Uses pydub (free) - no premium tools needed
"""

from pydub import AudioSegment
import numpy as np


def mix_audio(dialogue_path, background_path, output_path,
              dialogue_volume=1.0, background_volume=0.15):
    """Mix dialogue with background music"""
    
    dialogue = AudioSegment.from_file(dialogue_path)
    background = AudioSegment.from_file(background_path)
    
    # Adjust volumes
    dialogue = dialogue + (20 * np.log10(dialogue_volume))
    background = background + (20 * np.log10(background_volume))
    
    # Loop background to match dialogue
    if len(background) < len(dialogue):
        repeats = int(np.ceil(len(dialogue) / len(background)))
        background = background * repeats
    
    background = background[:len(dialogue)]
    
    # Mix
    mixed = dialogue.overlay(background)
    mixed.export(output_path, format="mp3")
    
    return output_path


def normalize_audio(audio_path, target_dB=-20.0):
    """Normalize audio to target dB"""
    audio = AudioSegment.from_file(audio_path)
    change_in_dB = target_dB - audio.dBFS
    normalized = audio.apply_gain(change_in_dB)
    normalized.export(audio_path, format="mp3")
    return audio_path
