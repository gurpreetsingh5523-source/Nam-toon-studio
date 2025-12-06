#!/usr/bin/env python3
"""
AMRIT CAPABILITY CHECK - ਪੰਜਾਬੀ ਸਮਰੱਥਾ ਰਿਪੋਰਟ
Runs a quick, non-interactive sweep of Amrit's current text→response skills.
Optionally speaks a couple of lines to verify audio.

Usage:
  /Users/gurpreetdhillon/Nam-toon-studio/.venv/bin/python amrit_capability_check.py [--voice]
"""
import sys
import argparse
from basic_voice_amrit import BasicVoiceAmrit


def main():
    parser = argparse.ArgumentParser(description="Amrit capability check (Punjabi)")
    parser.add_argument("--voice", action="store_true", help="Speak a couple of sample lines")
    args = parser.parse_args()

    amrit = BasicVoiceAmrit()

    # Test matrix: input prompts across known intent buckets
    tests = [
        ("Greeting", "ਸਤ ਸ੍ਰੀ ਅਕਾਲ"),
        ("Name/Identity", "ਤੁਹਾਡਾ ਨਾਮ ਕੀ ਹੈ?"),
        ("How are you", "ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?"),
        ("Help", "ਮੈਨੂੰ ਮਦਦ ਚਾਹੀਦੀ ਹੈ"),
        ("Love/Affection", "ਮੈਂ ਤੁਹਾਨੂੰ ਪਿਆਰ ਕਰਦਾ ਹਾਂ"),
        ("Worry/Problem", "ਮੈਨੂੰ ਚਿੰਤਾ ਹੈ"),
        ("Good/Excellent", "ਬਹੁਤ ਵਧੀਆ"),
        ("Work/Task", "ਕੋਈ ਕੰਮ ਕਰ ਸਕਦੇ ਹੋ?"),
        ("Video", "ਵੀਡੀਓ ਬਣਾ ਦਿਓ"),
        ("Scene/Image", "ਇੱਕ ਤਸਵੀਰ ਦਾ ਸੀਨ ਬਣਾਓ"),
        ("Default/Other", "ਚੱਲੋ ਅੱਜ ਦੀ ਯੋਜਨਾ ਬਣਾਈਏ"),
        ("Empty", ""),
    ]

    print("\n========== AMRIT CAPABILITY CHECK (ਪੰਜਾਬੀ) ==========")
    speak_samples = []
    count = 0

    for label, user in tests:
        count += 1
        try:
            res = amrit.get_response(user)
        except Exception as e:
            res = f"[Error generating response: {e}]"
        print(f"\n{count}. [{label}]\n👤 ਇਨਪੁੱਟ: {user!r}\n🧠 ਜਵਾਬ:  {res}")
        # Collect a couple of responses to speak if requested
        if args.voice and len(speak_samples) < 2 and res and "Error" not in res:
            speak_samples.append(res)

    if args.voice and speak_samples:
        print("\n🔊 Speaking a couple of samples...")
        for i, line in enumerate(speak_samples, 1):
            print(f"\n[{i}] 🗣️ {line}")
            try:
                amrit.speak(line)
            except Exception as e:
                print(f"❌ Voice play error: {e}")

    print("\n✅ Capability check complete.")


if __name__ == "__main__":
    main()
