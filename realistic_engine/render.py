"""Render one continuous 2.4:1 frame stream (with dissolves) straight into ffmpeg.

Each shot uses its motion clip (clips/<name>.mp4 from i2v.py) when one exists, else
the 2.5D depth camera on the still. Motion is an optional per-shot upgrade.
"""
import json, os, subprocess, sys, time
import numpy as np
from PIL import Image
import mlx.core as mx
from camera import FW, FH
from camera_mlx import Shot
from clip_shot import ClipShot
import titles

OW, OH = 1920, 1080                  # delivery frame; image is letterboxed inside
BAR = (OH - FH) // 2

FPS = 24
LEAD, TAIL = 5.0, 7.0        # title card / end card
DISSOLVE = 0.9
UPSCALE = 1.15               # headroom so pans never sample past the edge

MOVE = {
    "title_card": "slow_push", "void_hunter": "drift_left", "graveyard": "push_left",
    "arrival": "push", "deathworld": "crane_down", "hud_signal": "push",
    "turn_toward": "drift_right", "decloak": "pull", "corridor": "push",
    "core": "crane_up", "broadcast": "pull", "swarm": "drift_left",
    "buried": "push", "admiral": "push", "promise": "slow_push",
    "finale": "pull", "end_card": "slow_push",
}


def load(name, seed):
    clip = f"clips/{name}.mp4"
    if os.path.exists(clip):                              # motion upgrade for this shot
        return ClipShot(clip, seed=seed)
    rgb = Image.open(f"shots/{name}.png").convert("RGB")
    w, h = int(rgb.width * UPSCALE) // 2 * 2, int(rgb.height * UPSCALE) // 2 * 2
    rgb = rgb.resize((w, h), Image.LANCZOS)
    d = Image.open(f"depth/{name}.png").convert("L").resize((w, h), Image.BILINEAR)
    return Shot(np.asarray(rgb), np.asarray(d), MOVE[name], seed=seed)


def main(out="out/video_raw.mp4"):
    T = json.load(open("timings.json"))
    ev = [("title_card", 0.0, LEAD)]
    for s in T:
        ev.append((s["scene"], LEAD + s["start"], LEAD + s["end"]))
    ev.append(("end_card", LEAD + T[-1]["end"], LEAD + T[-1]["end"] + TAIL))
    total = ev[-1][2]
    nframes = int(total * FPS)
    print(f"{len(ev)} shots, {total:.1f}s, {nframes} frames @ {FPS}fps", flush=True)

    layers = titles.build(LEAD, TAIL)
    print(f"{len(layers)} text layers", flush=True)

    p = subprocess.Popen([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
        "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
        "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)

    canvas = np.zeros((OH, OW, 3), np.float32)
    cache, t0 = {}, time.time()
    for f in range(nframes):
        T_ = f / FPS
        i = min(len(ev) - 1, max(0, next((k for k, e in enumerate(ev) if T_ < e[2]), len(ev) - 1)))
        name, s0, s1 = ev[i]
        if name not in cache:
            cache = {name: load(name, seed=i * 17 + 3)}       # keep memory flat
        cur = cache[name]
        img = cur.frame(np.clip((T_ - s0) / max(1e-6, s1 - s0), 0, 1))

        if i > 0 and T_ < s0 + DISSOLVE:                      # dissolve from previous shot
            pn, ps0, ps1 = ev[i - 1]
            if pn not in cache:
                cache[pn] = load(pn, seed=(i - 1) * 17 + 3)
            pt = np.clip((T_ - ps0) / max(1e-6, ps1 - ps0), 0, 1.12)
            a = (T_ - s0) / DISSOLVE
            a = a * a * (3 - 2 * a)
            img = cache[pn].frame(pt) * (1 - a) + img * a

        canvas[BAR:BAR + FH] = np.array(img)             # letterbox
        frame = titles.composite(canvas, layers, T_)
        p.stdin.write((frame * 255).astype(np.uint8).tobytes())
        if f % 120 == 0:
            el = time.time() - t0
            eta = (nframes - f) * el / max(1, f) / 60
            print(f"  {f:5d}/{nframes}  {name:12s}  eta {eta:5.1f}m", flush=True)

    p.stdin.close(); p.wait()
    print(f"-> {out}  ({(time.time()-t0)/60:.1f} min)")


if __name__ == "__main__":
    main(*sys.argv[1:])
