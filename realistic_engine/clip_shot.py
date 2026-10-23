"""ClipShot: play a motion clip (from i2v.py) where one exists, matched to a 2.5D Shot.

Same .frame(t) interface as camera_mlx.Shot, so render.py can use either
interchangeably. A ~2s SVD clip is ping-pong time-stretched across the (longer) shot
— SVD's micro-motion in slow-mo reads as a living still — plus a gentle push and the
same filmic grade/vignette/grain so motion shots and 2.5D shots share one look.
"""
import numpy as np
import imageio.v3 as iio
from camera import FW, FH, bilinear, blur


def _read(path):
    v = iio.imread(path, plugin="pyav")            # (n,h,w,3) uint8
    return np.asarray(v, np.float32) / 255.0


class ClipShot:
    def __init__(self, path, move_push=0.05, seed=0, grain=1.0):
        f = _read(path)
        # resize every frame to the working frame size
        n, h, w, _ = f.shape
        if (h, w) != (FH, FW):
            ys = (np.arange(FH) * (h / FH)).astype(np.int32).clip(0, h - 1)
            xs = (np.arange(FW) * (w / FW)).astype(np.int32).clip(0, w - 1)
            f = f[:, ys][:, :, xs]
        self.f = f
        self.n = len(f)
        self.push = move_push
        self.grain = grain
        self.rng = np.random.default_rng(seed)
        yy, xx = np.mgrid[0:FH, 0:FW].astype(np.float32)
        self.xx, self.yy = xx, yy
        self.r = np.sqrt(((xx / FW - .5) * 2) ** 2 + ((yy / FH - .5) * 2) ** 2)

    def _sample(self, t):
        # ping-pong through the clip so there is no hard loop seam
        u = t * (self.n - 1) * 2
        k = u % (2 * (self.n - 1))
        idx = k if k <= self.n - 1 else 2 * (self.n - 1) - k
        i0 = int(np.floor(idx)); i1 = min(i0 + 1, self.n - 1); a = idx - i0
        return self.f[i0] * (1 - a) + self.f[i1] * a

    def frame(self, t):
        img = self._sample(np.clip(t, 0, 1))
        # gentle push so the motion shot still has camera life
        z = 1.0 + self.push * (t * t * (3 - 2 * t))
        sx = (self.xx - FW / 2) / z + FW / 2
        sy = (self.yy - FH / 2) / z + FH / 2
        img = bilinear(img, sx, sy)
        return self._grade(img)

    def _grade(self, img):
        hi = np.clip(img.max(2) - 0.72, 0, None)[..., None]
        img = img + blur(hi, 130, 5) * np.array([0.55, 0.70, 1.00], np.float32) * 0.55
        img = img * (1 - 0.34 * np.clip(self.r / 1.35, 0, 1) ** 2.1)[..., None]
        img = np.clip(img, 0, 4)
        img = img / (1 + img * 0.30)
        l = img.mean(2, keepdims=True)
        img += (np.array([-0.012, 0.004, 0.020], np.float32) * (1 - l)
                + np.array([0.020, 0.006, -0.014], np.float32) * l)
        img = (img - 0.5) * 1.06 + 0.5
        g = self.rng.standard_normal((FH, FW, 1)).astype(np.float32)
        img += g * (0.020 * self.grain) * (1.25 - l)
        return np.clip(img, 0, 1)
