#!/usr/bin/env python3
"""Auto-download missing assets from free sources"""
import requests
from PIL import Image
import io

def download_placeholder_character(name, color=(100, 150, 255)):
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.ellipse([20, 20, 236, 236], fill=color + (255,))
    return img

def download_placeholder_background(scene_type="village"):
    img = Image.new('RGB', (1920, 1080))
    colors = {
        "village": ((67, 97, 138), (31, 41, 55)),
        "night": ((17, 24, 39), (0, 0, 20)),
    }
    top, bottom = colors.get(scene_type, colors["village"])
    for y in range(1080):
        t = y / 1079
        r = int(top[0] * (1-t) + bottom[0] * t)
        g = int(top[1] * (1-t) + bottom[1] * t)
        b = int(top[2] * (1-t) + bottom[2] * t)
        for x in range(1920):
            img.putpixel((x, y), (r, g, b))
    return img
