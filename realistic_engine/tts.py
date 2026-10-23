"""Narration: Piper TTS, one voice per host, one wav per sentence + exact timings."""
import json, os, re, wave
import numpy as np
from piper import PiperVoice, SynthesisConfig
from script import SEGMENTS

SR = 22050
VOICES = {1: "voices/en_US-ryan-high.onnx", 2: "voices/en_US-lessac-high.onnx"}
# host 1 = measured, ominous;  host 2 = slightly brighter, urgent
CFG = {1: SynthesisConfig(length_scale=1.10, noise_scale=0.63, noise_w_scale=0.78, volume=1.0),
       2: SynthesisConfig(length_scale=1.05, noise_scale=0.65, noise_w_scale=0.80, volume=1.0)}

GAP_SENT = 0.30      # pause between sentences inside a segment
GAP_SEG = 0.85       # pause between hosts


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    out = []
    for p in parts:                                  # split very long lines on commas too
        if len(p) > 165:
            chunks, cur = [], ""
            for piece in re.split(r"(?<=,)\s+", p):
                if len(cur) + len(piece) > 140 and cur:
                    chunks.append(cur.strip()); cur = piece
                else:
                    cur += " " + piece
            if cur.strip():
                chunks.append(cur.strip())
            out += chunks
        else:
            out.append(p)
    return [s for s in out if s.strip()]


def synth(voice, cfg, text):
    chunks = [c.audio_float_array for c in voice.synthesize(text, syn_config=cfg)]
    return np.concatenate(chunks).astype(np.float32)


def main():
    os.makedirs("audio", exist_ok=True)
    loaded = {h: PiperVoice.load(p) for h, p in VOICES.items()}
    track, timings, t = [], [], 0.0

    for si, (host, scene, text) in enumerate(SEGMENTS):
        seg_start, caps = t, []
        for sent in sentences(text):
            a = synth(loaded[host], CFG[host], sent)
            dur = len(a) / SR
            caps.append({"text": sent, "start": round(t, 3), "end": round(t + dur, 3)})
            track.append(a)
            track.append(np.zeros(int(SR * GAP_SENT), np.float32))
            t += dur + GAP_SENT
        t = t - GAP_SENT + GAP_SEG
        track[-1] = np.zeros(int(SR * GAP_SEG), np.float32)
        timings.append({"i": si, "host": host, "scene": scene,
                        "start": round(seg_start, 3), "end": round(t, 3),
                        "dur": round(t - seg_start, 3), "captions": caps})
        print(f"{si:02d} {scene:12s} host{host}  {t-seg_start:6.2f}s", flush=True)

    audio = np.concatenate(track)
    audio = audio / max(1e-6, np.abs(audio).max()) * 0.85
    with wave.open("audio/narration.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())

    json.dump(timings, open("timings.json", "w"), indent=1)
    print(f"\ntotal narration {len(audio)/SR/60:.2f} min -> audio/narration.wav")


if __name__ == "__main__":
    main()
