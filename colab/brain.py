"""Simple on-disk 'brain' for Nam-toon-studio.

This module provides a lightweight Brain class that can ingest audio/images
and compute basic features (RMS, spectral centroid via FFT, color histogram).
It stores a small JSON store of feature summaries at `colab/brain_store.json`.

Purpose: allow the studio to "watch and learn" locally and suggest improved
mixing/animation parameters (duck strength, bg gain, pan width, dream strength).

This is intentionally lightweight and does not require heavy ML libraries.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import wave
import numpy as np
from PIL import Image
from moviepy.editor import VideoFileClip, AudioFileClip

STORE_PATH = Path(__file__).parent / "brain_store.json"


class Brain:
    def __init__(self, store_path: Path = STORE_PATH):
        self.store_path = Path(store_path)
        self.data = self._load_store()

    def _load_store(self):
        if self.store_path.exists():
            try:
                return json.loads(self.store_path.read_text())
            except Exception:
                return {"audios": {}, "images": {}, "videos": {}, "meta": {}}
        return {"audios": {}, "images": {}, "videos": {}, "meta": {}}

    def _save_store(self):
        self.store_path.write_text(json.dumps(self.data, indent=2))

    # ---------- Audio feature extraction ----------
    def ingest_audio(self, path: str):
        path = str(path)
        key = os.path.basename(path)
        try:
            with wave.open(path, 'rb') as wf:
                sr = wf.getframerate()
                n = wf.getnframes()
                frames = wf.readframes(n)
                sw = wf.getsampwidth()
                arr = np.frombuffer(frames, dtype=np.int16 if sw == 2 else np.int8).astype(np.float32)
                if wf.getnchannels() > 1:
                    arr = arr.reshape(-1, wf.getnchannels()).mean(axis=1)
                arr = arr / (32768.0 if sw == 2 else 128.0)
                # features
                rms = float(np.sqrt(np.mean(arr**2)))
                # spectral centroid (approx)
                S = np.abs(np.fft.rfft(arr))
                freqs = np.fft.rfftfreq(len(arr), 1.0 / sr)
                if S.sum() > 0:
                    centroid = float((S * freqs).sum() / S.sum())
                else:
                    centroid = 0.0
                duration = float(n / sr)

            self.data.setdefault("audios", {})[key] = {
                "path": path,
                "rms": rms,
                "centroid": centroid,
                "duration": duration,
            }
            self._save_store()
            return self.data["audios"][key]
        except Exception as e:
            raise RuntimeError(f"Failed to ingest audio {path}: {e}")

    # ---------- Image feature extraction ----------
    def ingest_image(self, path: str):
        path = str(path)
        key = os.path.basename(path)
        try:
            im = Image.open(path).convert('RGB')
            # small color histogram (64 bins per channel -> 192 total)
            h = np.array(im).astype(np.float32)
            # downsample for speed
            if h.size > 1920*1080*3:
                im = im.resize((640, 360))
                h = np.array(im).astype(np.float32)
            hist_r, _ = np.histogram(h[:,:,0], bins=64, range=(0,255))
            hist_g, _ = np.histogram(h[:,:,1], bins=64, range=(0,255))
            hist_b, _ = np.histogram(h[:,:,2], bins=64, range=(0,255))
            hist = np.concatenate([hist_r, hist_g, hist_b]).tolist()
            avg_brightness = float(h.mean())

            self.data.setdefault("images", {})[key] = {
                "path": path,
                "histogram": hist,
                "avg_brightness": avg_brightness,
            }
            self._save_store()
            return self.data["images"][key]
        except Exception as e:
            raise RuntimeError(f"Failed to ingest image {path}: {e}")

    # ---------- Video ingestion (extract first frame + audio summary) ----------
    def ingest_video(self, path: str):
        path = str(path)
        key = os.path.basename(path)
        try:
            clip = VideoFileClip(path)
            # sample first frame to image features
            frame = clip.get_frame(0.1) if clip.duration > 0.2 else clip.get_frame(0.0)
            tmp = Path("/tmp") / f"brain_frame_{key}.png"
            Image.fromarray(frame).save(tmp)
            img_feat = self.ingest_image(str(tmp))
            # sample audio as temporary wav and ingest
            if clip.audio:
                tmp_audio = Path(Path(path).parent) / f"brain_tmp_audio_{key}.wav"
                try:
                    clip.audio.write_audiofile(str(tmp_audio), verbose=False, logger=None)
                    aud_feat = self.ingest_audio(str(tmp_audio))
                except Exception:
                    aud_feat = {}
            else:
                aud_feat = {}

            self.data.setdefault("videos", {})[key] = {"path": path, "image": img_feat, "audio": aud_feat}
            self._save_store()
            return self.data["videos"][key]
        except Exception as e:
            raise RuntimeError(f"Failed to ingest video {path}: {e}")

    # ---------- Bulk ingest helpers ----------
    def ingest_directory(self, audio_dir="audio", image_dir="images", video_dir=None):
        results = {"audios": {}, "images": {}, "videos": {}}
        if os.path.exists(audio_dir):
            for f in os.listdir(audio_dir):
                if f.lower().endswith(('.wav', '.mp3')):
                    p = os.path.join(audio_dir, f)
                    try:
                        results['audios'][f] = self.ingest_audio(p)
                    except Exception as e:
                        results['audios'][f] = {"error": str(e)}
        if os.path.exists(image_dir):
            for f in os.listdir(image_dir):
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    p = os.path.join(image_dir, f)
                    try:
                        results['images'][f] = self.ingest_image(p)
                    except Exception as e:
                        results['images'][f] = {"error": str(e)}
        if video_dir and os.path.exists(video_dir):
            for f in os.listdir(video_dir):
                if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                    p = os.path.join(video_dir, f)
                    try:
                        results['videos'][f] = self.ingest_video(p)
                    except Exception as e:
                        results['videos'][f] = {"error": str(e)}
        return results

    # ---------- Simple suggestion engine ----------
    def suggest_parameters(self):
        """Return suggested parameters for master_builder based on learned assets.

        Output example: {"bg_gain": 0.12, "duck_factor": 0.3, "pan_width": 0.4, "dream": True}
        """
        aud = list(self.data.get('audios', {}).values())
        imgs = list(self.data.get('images', {}).values())
        # defaults
        suggestion = {"bg_gain": 0.15, "duck_factor": 0.25, "pan_width": 0.0, "dream": False}
        if len(aud) > 0:
            avg_rms = float(np.mean([a.get('rms', 0.0) for a in aud]))
            # quieter audio -> lower bg gain, louder -> higher
            suggestion['bg_gain'] = float(max(0.05, min(0.4, 0.2 - (avg_rms - 0.05))))
            # if centroid is low (bass heavy), duck a little more
            avg_cent = float(np.mean([a.get('centroid', 0.0) for a in aud]))
            if avg_cent < 500:
                suggestion['duck_factor'] = 0.2
            else:
                suggestion['duck_factor'] = 0.3
            suggestion['pan_width'] = float(min(0.7, 0.1 + avg_cent / 5000.0))
        if len(imgs) > 0:
            avg_b = float(np.mean([i.get('avg_brightness', 0.0) for i in imgs]))
            # dark images -> more dreamy processing
            suggestion['dream'] = avg_b < 100
        # store suggestions in meta
        self.data.setdefault('meta', {})['last_suggestion'] = suggestion
        self._save_store()
        return suggestion


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--scan', action='store_true', help='Scan audio/images directories and update brain store')
    parser.add_argument('--suggest', action='store_true', help='Print parameter suggestions')
    args = parser.parse_args()
    b = Brain()
    if args.scan:
        print('Scanning audio/ and images/ ...')
        res = b.ingest_directory()
        print('Scan result:', {k: len(v) for k, v in res.items()})
    if args.suggest:
        s = b.suggest_parameters()
        print('Suggestion:', s)
