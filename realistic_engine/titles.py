"""Caption + title layer, rendered with PIL (this ffmpeg has no libass/drawtext)."""
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from script import TITLE, SUBTITLE

FONT = "/System/Library/Fonts/Avenir Next.ttc"
MEDIUM, REGULAR, DEMI, ULTRA = 5, 7, 2, 10

W, H, IMG_H = 1920, 1080, 800
BAR = (H - IMG_H) // 2                       # 140px letterbox bar

HOST_COL = {1: (255, 243, 232), 2: (219, 236, 255)}
CAP_SIZE, CAP_LEAD, CAP_MAX = 38, 46, 62     # px, line height, chars per line


def font(size, idx):
    return ImageFont.truetype(FONT, size, index=idx)


def wrap(text, f, max_w, draw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=f) > max_w and cur:
            lines.append(cur); cur = w_
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines[:2] if len(lines) <= 2 else [" ".join(lines[:-1]), lines[-1]]


def tracked(draw, xy, text, f, fill, spacing=0.0, anchor_cx=True):
    """draw text with letter-spacing, optionally centred on xy[0]"""
    widths = [draw.textlength(c, font=f) for c in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = xy[0] - total / 2 if anchor_cx else xy[0]
    for c, w_ in zip(text, widths):
        draw.text((x, xy[1]), c, font=f, fill=fill)
        x += w_ + spacing


def _layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def caption_img(text, host):
    """One caption, centred in the lower letterbox bar."""
    im = _layer()
    d = ImageDraw.Draw(im)
    f = font(CAP_SIZE, MEDIUM)
    lines = wrap(text, f, W - 560, d)
    total_h = len(lines) * CAP_LEAD
    y = H - BAR + (BAR - total_h) / 2 - 2
    col = HOST_COL[host]
    for ln in lines:
        w_ = d.textlength(ln, font=f)
        x = (W - w_) / 2
        d.text((x + 1, y + 2), ln, font=f, fill=(0, 0, 0, 150))     # soft shadow
        d.text((x, y), ln, font=f, fill=(*col, 255))
        y += CAP_LEAD
    return im


def title_img():
    im = _layer()
    d = ImageDraw.Draw(im)
    tracked(d, (W / 2, H / 2 - 88), TITLE, font(92, DEMI), (246, 246, 246, 255), 15)
    d.line([W / 2 - 190, H / 2 + 34, W / 2 + 190, H / 2 + 34], fill=(150, 170, 195, 190), width=2)
    tracked(d, (W / 2, H / 2 + 62), SUBTITLE.upper(), font(30, REGULAR), (176, 194, 214, 255), 6)
    return im


def end_img(line, size=34, idx=REGULAR, col=(214, 226, 240), dy=0, sp=6):
    im = _layer()
    tracked(ImageDraw.Draw(im), (W / 2, H / 2 + dy), line, font(size, idx), (*col, 255), sp)
    return im


def build(lead, tail):
    """-> list of (start, end, fade_in, fade_out, RGBA float array)"""
    T = json.load(open("timings.json"))
    items = [(0.8, lead - 0.2, 1.1, 0.7, title_img())]
    for seg in T:
        for c in seg["captions"]:
            items.append((lead + c["start"] - 0.10, lead + c["end"] + 0.24, 0.16, 0.20,
                          caption_img(c["text"], seg["host"])))
    end = lead + T[-1]["end"]
    items.append((end + 1.5, end + tail - 0.7, 1.0, 1.1,
                  end_img("THEY ANSWERED.", 40, DEMI, (238, 240, 244), -14, 12)))
    items.append((end + 3.4, end + tail - 0.4, 0.9, 0.9,
                  end_img("narration · score · imagery generated locally with open models",
                          24, ULTRA, (140, 158, 178), 60, 3)))
    return [(s, e, fi, fo, np.asarray(im, np.float32) / 255.0) for s, e, fi, fo, im in items]


def composite(frame, layers, t):
    """frame: HxWx3 float 0..1 ; layers from build()"""
    for s, e, fi, fo, arr in layers:
        if not (s <= t < e):
            continue
        a = min(1.0, (t - s) / fi if t - s < fi else 1.0,
                (e - t) / fo if e - t < fo else 1.0)
        a = a * a * (3 - 2 * a)
        al = arr[..., 3:4] * a
        frame = frame * (1 - al) + arr[..., :3] * al
    return frame
