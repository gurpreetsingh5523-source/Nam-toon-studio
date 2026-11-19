"""2.5D virtual camera: depth-parallax warp + anamorphic bloom, grain, gate weave."""
import numpy as np

FW, FH = 1920, 800          # anamorphic frame (2.4:1)


# ------------------------------------------------------------------ sampling
def bilinear(img, sx, sy):
    h, w = img.shape[:2]
    sx = np.clip(sx, 0, w - 1.001)
    sy = np.clip(sy, 0, h - 1.001)
    x0 = sx.astype(np.int32); y0 = sy.astype(np.int32)
    x1 = x0 + 1; y1 = y0 + 1
    fx = (sx - x0)[..., None]; fy = (sy - y0)[..., None]
    return ((img[y0, x0] * (1 - fx) + img[y0, x1] * fx) * (1 - fy) +
            (img[y1, x0] * (1 - fx) + img[y1, x1] * fx) * fy)


def _box(a, r, axis):
    n = a.shape[axis]
    r = min(int(r), n - 1)
    if r < 1:
        return a
    pad = [(0, 0)] * a.ndim
    pad[axis] = (r + 1, r)
    c = np.cumsum(np.pad(a, pad, mode="edge"), axis=axis, dtype=np.float32)
    hi = [slice(None)] * a.ndim; lo = [slice(None)] * a.ndim
    hi[axis] = slice(2 * r + 1, None); lo[axis] = slice(0, n)
    return (c[tuple(hi)] - c[tuple(lo)]) / (2 * r + 1)


def blur(a, rx, ry=None):
    ry = rx if ry is None else ry
    for _ in range(2):
        a = _box(_box(a, ry, 0), rx, 1)
    return a


# ------------------------------------------------------------------ moves
# (zoom_start, zoom_end, pan_x, pan_y, parallax) — pans in fractions of frame
MOVES = {
    "push":        (1.00, 1.075, 0.000, 0.000, 1.00),
    "pull":        (1.085, 1.00, 0.000, 0.000, 1.00),
    "drift_left":  (1.045, 1.045, 0.028, 0.000, 1.45),
    "drift_right": (1.045, 1.045, -0.028, 0.000, 1.45),
    "push_left":   (1.00, 1.070, 0.018, 0.000, 1.30),
    "crane_down":  (1.050, 1.050, 0.000, -0.022, 1.20),
    "crane_up":    (1.050, 1.050, 0.000, 0.022, 1.20),
    "slow_push":   (1.00, 1.045, 0.006, 0.004, 0.85),
}


def ease(t):
    return t * t * (3 - 2 * t)


class Shot:
    """Renders frames for one still with a moving virtual camera."""

    def __init__(self, rgb, depth, move="push", seed=0, grain=1.0):
        self.src = rgb.astype(np.float32) / 255.0
        h, w = self.src.shape[:2]
        d = depth.astype(np.float32)
        d = (d - d.min()) / max(1e-6, float(np.ptp(d)))
        # soften depth so edges don't tear, then bias toward mid-ground
        self.depth = blur(d, 9)[..., None]
        self.h, self.w = h, w
        self.m = MOVES[move]
        self.rng = np.random.default_rng(seed)
        self.grain = grain
        yy, xx = np.mgrid[0:FH, 0:FW].astype(np.float32)
        self.xx, self.yy = xx, yy
        # gate weave: slow correlated handheld drift
        n = 4096
        w1 = np.cumsum(self.rng.standard_normal(n)); w2 = np.cumsum(self.rng.standard_normal(n))
        self.weave = (w1 / np.abs(w1).max(), w2 / np.abs(w2).max())

    def frame(self, t):
        """t in [0,1] across the shot."""
        z0, z1, px, py, par = self.m
        e = ease(t)
        z = z0 + (z1 - z0) * e
        ox = px * e * self.w
        oy = py * e * self.h
        k = int(t * 4000)
        wx = self.weave[0][k] * 2.2
        wy = self.weave[1][k] * 1.6

        # map frame pixel -> source pixel (frame is 1920x800, source may be larger)
        sx = (self.xx - FW / 2) / z + self.w / 2 + ox + wx
        sy = (self.yy - FH / 2) / z + self.h / 2 + oy + wy

        # depth-driven parallax: nearer pixels move more
        dz = bilinear(self.depth, sx, sy)[..., 0]
        amp = par * (12.0 + 26.0 * e)
        sx = sx + (dz - 0.45) * amp * np.sign(px if px else 1) * (1.0 if px else 0.35)
        sy = sy + (dz - 0.45) * amp * 0.35 * (np.sign(py) if py else 0.0)

        img = bilinear(self.src, sx, sy)
        return self.post(img, t)

    def post(self, img, t):
        # anamorphic bloom: wide horizontal streak off the highlights
        hi = np.clip(img.max(2) - 0.72, 0, None)[..., None]
        img = img + blur(hi, 130, 5) * np.array([0.55, 0.70, 1.00], np.float32) * 0.85
        img = img + blur(hi, 22, 22) * 0.35

        # subtle chromatic aberration toward the frame edges
        r = np.sqrt(((self.xx / FW - .5) * 2) ** 2 + ((self.yy / FH - .5) * 2) ** 2)
        s = 1.0 + 0.0016 * r
        cx = (self.xx - FW / 2) / s + FW / 2
        cy = (self.yy - FH / 2) / s + FH / 2
        img[..., 0] = bilinear(img[..., :1], cx, cy)[..., 0]

        # vignette
        img *= (1 - 0.34 * np.clip(r / 1.35, 0, 1) ** 2.1)[..., None]

        # filmic curve + slight teal shadows / warm highlights
        img = np.clip(img, 0, 4)
        img = img / (1 + img * 0.30)
        l = img.mean(2, keepdims=True)
        img += (np.array([-0.012, 0.004, 0.020], np.float32) * (1 - l)
                + np.array([0.020, 0.006, -0.014], np.float32) * l)
        img = (img - 0.5) * 1.06 + 0.5

        # animated film grain, heavier in the shadows
        g = self.rng.standard_normal((FH, FW, 1)).astype(np.float32)
        g = blur(g, 1, 1)
        img += g * (0.022 * self.grain) * (1.25 - l)
        return np.clip(img, 0, 1)
