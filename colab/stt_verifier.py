#!/usr/bin/env python3
"""
STT Verifier
Tries to transcribe a given audio file and compute a simple quality score against
an expected text string. Prefers `whisper` if available; otherwise returns None.

Usage: python colab/stt_verifier.py --audio path/to.wav --expected "expected text"
"""
import sys
from pathlib import Path
import json


def transcribe_with_whisper(audio_path: str, model: str = 'tiny'):
    try:
        import whisper  # type: ignore
    except Exception:
        print('whisper not installed; STT unavailable')
        return None

    try:
        model_obj = whisper.load_model(model)
        res = model_obj.transcribe(audio_path)
        return res.get('text')
    except Exception as e:
        print('whisper transcription failed:', e)
        return None


def score_transcription(expected: str, transcript: str) -> float:
    """Simple word-overlap score: common words / expected words."""
    if not expected or not transcript:
        return 0.0
    import re
    e_words = re.findall(r"\w+", expected.lower())
    t_words = re.findall(r"\w+", transcript.lower())
    if not e_words:
        return 0.0
    common = sum(1 for w in e_words if w in t_words)
    return float(common) / float(len(e_words))


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Transcribe audio and score against expected text')
    parser.add_argument('--audio', type=str, required=True)
    parser.add_argument('--expected', type=str, required=True)
    parser.add_argument('--model', type=str, default='tiny')
    args = parser.parse_args()

    transcript = transcribe_with_whisper(args.audio, model=args.model)
    if transcript is None:
        print('Transcription unavailable')
        return

    score = score_transcription(args.expected, transcript)
    out = {
        'audio': args.audio,
        'expected': args.expected,
        'transcript': transcript,
        'score': score
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
