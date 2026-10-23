"""Same virtual camera as camera.py, but the hot path runs on the M-series GPU via MLX."""
import mlx.core as mx
import numpy as np
from camera import MOVES, FW, FH, ease


def _edge_pad(a, r, axis):
    """replicate-pad `a` by (r+1, r) along `axis`"""
    lo = mx.take(a, mx.zeros(r + 1, dtype=mx.int32), axis=axis)
    hi = mx.take(a, mx.full(r, a.shape[axis] - 1, dtype=mx.int32), axis=axis)
    return mx.concatenate([lo, a, hi], axis=axis)


def _box(a, r, axis):
    n = a.shape[axis]
    r = min(int(r), n - 1)
    if r < 1:
        return a
    c = mx.cumsum(_edge_pad(a, r, axis), axis=axis)
    hi = mx.take(c, mx.arange(2 * r + 1, 2 * r + 1 + n), axis=axis)
    lo = mx.take(c, mx.arange(0, n), axis=axis)
    return (hi - lo) / (2 * r + 1)


def blur(a, rx, ry=None, passes=2):
    ry = rx if ry is None else ry
    for _ in range(passes):
        a = _box(_box(a, ry, 0), rx, 1)
    return a


class Shot:
    def __init__(self, rgb, depth, move="push", seed=0, grain=1.0):
        h, w = rgb.shape[:2]
        self.h, self.w = h, w
        self.src = mx.array(rgb.astype(np.float32) / 255.0).reshape(h * w, 3)

        d = depth.astype(np.float32)
        d = (d - d.min()) / max(1e-6, float(np.ptp(d)))
        d = np.asarray(blur(mx.array(d).reshape(h, w, 1), 9))
        self.depth = mx.array(d).reshape(h * w, 1)

        self.m = MOVES[move]
        self.grain = grain
        self.key = mx.random.key(seed)
        self.step = 0

        yy, xx = np.mgrid[0:FH, 0:FW].astype(np.float32)
        self.xx = mx.array(xx.ravel())
        self.yy = mx.array(yy.ravel())
        r = np.sqrt(((xx / FW - .5) * 2) ** 2 + ((yy / FH - .5) * 2) ** 2)
        self.r = mx.array(r.ravel())
        self.vig = mx.array((1 - 0.34 * np.clip(r / 1.35, 0, 1) ** 2.1)
                            .astype(np.float32)).reshape(FH, FW, 1)

        rng = np.random.default_rng(seed)
        n = 4096
        w1 = np.cumsum(rng.standard_normal(n)); w2 = np.cumsum(rng.standard_normal(n))
        self.weave = (w1 / np.abs(w1).max(), w2 / np.abs(w2).max())

    def _sample(self, flat, sx, sy, w=None, h=None):
        """flat: (w*h, C) row-major. sx/sy are flat pixel coords in that image."""
        w = self.w if w is None else w
        h = self.h if h is None else h
        sx = mx.clip(sx, 0, w - 1.001)
        sy = mx.clip(sy, 0, h - 1.001)
        x0 = sx.astype(mx.int32); y0 = sy.astype(mx.int32)
        x1 = x0 + 1; y1 = y0 + 1
        fx = (sx - x0).reshape(-1, 1); fy = (sy - y0).reshape(-1, 1)
        i00 = y0 * w + x0; i01 = y0 * w + x1
        i10 = y1 * w + x0; i11 = y1 * w + x1
        top = flat[i00] * (1 - fx) + flat[i01] * fx
        bot = flat[i10] * (1 - fx) + flat[i11] * fx
        return top * (1 - fy) + bot * fy

    def frame(self, t):
        z0, z1, px, py, par = self.m
        e = ease(t)
        z = z0 + (z1 - z0) * e
        ox = px * e * self.w
        oy = py * e * self.h
        k = int(min(max(t, 0.0), 1.0) * 4000)
        wx = float(self.weave[0][k]) * 2.2
        wy = float(self.weave[1][k]) * 1.6

        sx = (self.xx - FW / 2) / z + self.w / 2 + ox + wx
        sy = (self.yy - FH / 2) / z + self.h / 2 + oy + wy

        dz = self._sample(self.depth, sx, sy).reshape(-1)
        amp = par * (12.0 + 26.0 * e)
        sgn = 1.0 if px >= 0 else -1.0
        sx = sx + (dz - 0.45) * (amp * sgn * (1.0 if px else 0.35))
        if py:
            sy = sy + (dz - 0.45) * (amp * 0.35 * (1.0 if py > 0 else -1.0))

        img = self._sample(self.src, sx, sy).reshape(FH, FW, 3)
        return self.post(img, sx, sy)

    def post(self, img, sx, sy):
        # anamorphic bloom
        hi = mx.maximum(mx.max(img, axis=2, keepdims=True) - 0.72, 0)
        img = img + blur(hi, 130, 5) * mx.array([0.55, 0.70, 1.00]) * 0.85
        img = img + blur(hi, 22, 22) * 0.35

        # chromatic aberration: pull the red channel in slightly toward centre
        s = 1.0 + 0.0016 * self.r
        cx = (self.xx - FW / 2) / s + FW / 2
        cy = (self.yy - FH / 2) / s + FH / 2
        flat = img.reshape(FH * FW, 3)
        red = self._sample(flat[:, :1], cx, cy, w=FW, h=FH).reshape(FH, FW, 1)
        img = mx.concatenate([red, img[:, :, 1:]], axis=2)

        img = img * self.vig

        img = mx.clip(img, 0, 4)
        img = img / (1 + img * 0.30)
        l = mx.mean(img, axis=2, keepdims=True)
        img = img + (mx.array([-0.012, 0.004, 0.020]) * (1 - l)
                     + mx.array([0.020, 0.006, -0.014]) * l)
        img = (img - 0.5) * 1.06 + 0.5

        self.step += 1
        g = mx.random.normal((FH, FW, 1), key=mx.random.split(self.key, self.step + 1)[-1])
        img = img + blur(g, 1, 1, passes=1) * (0.022 * self.grain) * (1.25 - l)
        return mx.clip(img, 0, 1)
