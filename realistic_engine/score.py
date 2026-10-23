"""Original procedural score: sub drones, pulse, braams, risers. Synthesized, no samples."""
import json, wave
import numpy as np

SR = 48000


def env(n, a, d, s_lvl, r, total=None):
    total = total or n
    e = np.zeros(n, np.float32)
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    a = max(1, min(a, n)); d = min(d, max(1, n - a)); r = min(r, max(1, n - a - d))
    e[:a] = np.linspace(0, 1, a)
    e[a:a + d] = np.linspace(1, s_lvl, d)
    e[a + d:n - r] = s_lvl
    if r:
        e[n - r:] = np.linspace(s_lvl, 0, r)
    return e


def osc(f, n, kind="sine", detune=0.0, phase=0.0):
    t = np.arange(n, dtype=np.float32) / SR
    f = f * (1 + detune)
    if kind == "sine":
        return np.sin(2 * np.pi * f * t + phase)
    if kind == "saw":
        x = (f * t + phase) % 1.0
        return 2 * x - 1
    if kind == "tri":
        x = (f * t + phase) % 1.0
        return 4 * np.abs(x - 0.5) - 1
    return np.sign(np.sin(2 * np.pi * f * t + phase))


def lp(x, cutoff, sr=SR):
    """one-pole lowpass, vectorised via exponential smoothing"""
    a = np.exp(-2 * np.pi * cutoff / sr)
    b = 1 - a
    y = np.empty_like(x)
    acc = 0.0
    # chunked python loop is too slow; use lfilter-equivalent via cumulative trick
    # (approximate with repeated box smoothing — good enough for pads)
    k = max(1, int(sr / max(60.0, cutoff)))
    y = x.copy()
    for _ in range(3):
        c = np.cumsum(np.pad(y, (k, 0)), dtype=np.float32)
        y = (c[k:] - c[:-k]) / k
        y = np.pad(y, (0, len(x) - len(y)), mode="edge")[:len(x)]
    return y


def drone(dur, root, harm=(1, 1.5, 2, 3), amp=(1, .35, .28, .12), wob=0.12):
    n = int(dur * SR)
    t = np.arange(n, dtype=np.float32) / SR
    out = np.zeros(n, np.float32)
    for h, a in zip(harm, amp):
        lfo = 1 + wob * 0.004 * np.sin(2 * np.pi * (0.07 + h * 0.013) * t)
        out += a * osc(root * h, n, "sine") * lfo
        out += a * 0.35 * osc(root * h, n, "saw", detune=0.004) * lfo
    out *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.045 * t)
    return lp(out, 320)


def braam(dur, root, gain=1.0):
    """low brass-ish hit for act transitions"""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    for h, a in ((1, 1.0), (2, .55), (3, .30), (4, .18), (6, .10)):
        out += a * osc(root * h, n, "saw", detune=0.003 * h)
    out = lp(out, 900)
    out *= env(n, 0.06, 0.5, 0.45, dur * 0.55)
    return out * gain


def sub_pulse(dur, root, period, gain=1.0):
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    step = int(period * SR)
    for s in range(0, n - step, step):
        ln = min(int(period * 0.9 * SR), n - s)
        seg = osc(root, ln, "sine") * env(ln, 0.004, 0.10, 0.25, period * 0.55)
        seg += osc(root * 2, ln, "sine") * 0.25 * env(ln, 0.002, 0.05, 0.1, period * 0.3)
        out[s:s + ln] += seg
    return out * gain


def riser(dur, f0=90, f1=900, gain=1.0):
    n = int(dur * SR)
    t = np.arange(n, dtype=np.float32) / SR
    f = f0 * (f1 / f0) ** (t / max(1e-6, dur))
    ph = 2 * np.pi * np.cumsum(f) / SR
    out = np.sin(ph) * 0.5 + np.sign(np.sin(ph * 0.5)) * 0.12
    noise = np.random.default_rng(3).standard_normal(n).astype(np.float32)
    out += lp(noise, 1500) * np.linspace(0.05, 0.6, n)
    return out * np.linspace(0.05, 1.0, n) ** 2 * gain


def shimmer(dur, root, seed=1):
    """high sustained texture, the 'cold void' layer"""
    n = int(dur * SR)
    rng = np.random.default_rng(seed)
    out = np.zeros(n, np.float32)
    t = np.arange(n, dtype=np.float32) / SR
    for i, mult in enumerate((4, 6, 8, 12)):
        a = 0.08 / (i + 1)
        lfo = 0.5 + 0.5 * np.sin(2 * np.pi * (0.02 + 0.017 * i) * t + rng.random() * 6)
        out += a * osc(root * mult, n, "sine", detune=rng.uniform(-.004, .004)) * lfo
    return out


def whoosh(dur=1.6, seed=0, gain=1.0):
    n = int(dur * SR)
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n).astype(np.float32)
    x = lp(x, 2400) - lp(x, 260)
    e = np.linspace(0, 1, n) ** 3
    return x * e * np.linspace(1, 0.2, n) * gain


def reverb(x, mix=0.32, decay=2.4):
    """cheap multi-tap plate"""
    out = x.copy()
    rng = np.random.default_rng(11)
    for i in range(14):
        d = int(SR * rng.uniform(0.02, decay * 0.45))
        g = mix * (0.72 ** (i * 0.55)) * rng.uniform(0.55, 1.0)
        if d < len(x):
            out[d:] += x[:-d] * g
    return out


def build(timings, tail=7.0, lead=5.0):
    total = timings[-1]["end"] + tail + lead
    n = int(total * SR)
    mix = np.zeros(n, np.float32)

    def put(sig, at, g=1.0):
        s = int(at * SR)
        e = min(n, s + len(sig))
        if s < n:
            mix[s:e] += sig[:e - s] * g

    # --- three acts, each with its own harmonic centre
    acts = [(0.0, timings[4]["end"] + lead, 41.20, "dread"),      # the trap
            (timings[4]["end"] + lead, timings[10]["end"] + lead, 49.00, "assault"),
            (timings[10]["end"] + lead, total, 55.00, "resolve")]

    for a0, a1, root, mood in acts:
        d = a1 - a0
        put(drone(d, root), a0, 0.30 if mood == "dread" else 0.26)
        put(shimmer(d, root, seed=int(root)), a0, 0.55)
        if mood == "dread":
            put(sub_pulse(d, root * 0.5, 2.35), a0, 0.16)
        elif mood == "assault":
            put(sub_pulse(d, root * 0.5, 1.05), a0, 0.30)
            put(drone(d, root * 1.5, wob=0.4), a0, 0.10)
        else:
            put(sub_pulse(d, root * 0.5, 3.2), a0, 0.13)
            put(drone(d, root * 2, harm=(1, 2, 3), amp=(.5, .3, .15)), a0, 0.10)

    # --- hits on the beats that matter
    for idx, g in ((2, .55), (6, .80), (7, .85), (10, .70), (12, .60), (14, .75)):
        put(braam(3.2, 41.2 if idx < 8 else 49.0), timings[idx]["start"] + lead - 0.35, g)
    put(riser(4.0), timings[6]["start"] + lead - 4.0, 0.22)      # into the decloak
    put(riser(3.0, 120, 1400), timings[10]["start"] + lead - 3.0, 0.18)

    # --- transition whooshes on every cut
    for i, seg in enumerate(timings):
        put(whoosh(1.5, seed=i), seg["start"] + lead - 1.1, 0.13)

    mix = reverb(mix, 0.30, 2.6)
    mix *= 1.0 / max(1e-6, np.abs(mix).max()) * 0.62
    # gentle stereo widening
    d = int(SR * 0.011)
    L = mix.copy(); R = np.roll(mix, d) * 0.96
    st = np.stack([L, R], 1)
    return st, total


if __name__ == "__main__":
    t = json.load(open("timings.json"))
    st, total = build(t)
    with wave.open("audio/score.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())
    print(f"score {total/60:.2f} min -> audio/score.wav")
