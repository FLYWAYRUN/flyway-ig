# -*- coding: utf-8 -*-
"""Poster built from the user's own silhouette cut-outs."""
import os, random
from PIL import Image, ImageChops
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = [Image.open(os.path.join(HERE, 'cut', f'fig{i}.png')) for i in (1,2,3)]
VOLT = (212,255,54); INK = (8,9,11)

def _tint(fig, col, alpha=1.0):
    a = fig.split()[3]
    if alpha < 1: a = a.point(lambda v: int(v*alpha))
    return Image.merge('RGBA', (*[Image.new('L', fig.size, c) for c in col], a))

def _place(canvas, fig, cx, foot_y, h, col, alpha=1.0):
    s = h / fig.height
    f = fig.resize((max(1,int(fig.width*s)), int(h)), Image.LANCZOS)
    f = _tint(f, col, alpha)
    canvas.alpha_composite(f, (int(cx - f.width/2), int(foot_y - f.height)))

def build(W, H, rows, seed=7):
    rnd = random.Random(seed)
    base = Image.new('RGBA', (W, H), (*VOLT, 255))
    for r in rows:
        for (fx, fy, fh, fi) in r['figs']:
            if r.get('echo'):
                for k in range(r['echo'], 0, -1):
                    _place(base, FIGS[fi % 3], W*fx - W*0.026*k, fy, fh,
                           r['ecol'], round(0.34**k + 0.05, 3))
            _place(base, FIGS[fi % 3], W*fx, fy, fh, r['col'], r.get('alpha', 1.0))
    # film grain so the flat fill does not look like clip art
    g = np.random.default_rng(seed).normal(0, 4.5, (H, W, 1))
    arr = np.asarray(base.convert('RGB')).astype(np.int16) + g
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

def wide(W=1920, H=800, seed=7):
    G = int(H*0.93)
    return build(W, H, [
      dict(col=(178,214,44), ecol=(198,238,50), alpha=.95,
           figs=[(.46, G-H*.14, H*.30, 0), (.58, G-H*.14, H*.28, 2),
                 (.72, G-H*.14, H*.31, 1), (.86, G-H*.14, H*.29, 0)]),
      dict(col=(104,132,26), ecol=(170,206,42), echo=2,
           figs=[(.52, G-H*.05, H*.46, 2), (.70, G-H*.05, H*.44, 0),
                 (.87, G-H*.05, H*.47, 1)]),
      dict(col=INK, ecol=(150,186,30), echo=3,
           figs=[(.61, G, H*.70, 1), (.83, G, H*.67, 2)]),
    ], seed)

def tall(W=1080, H=1350, seed=11):
    G = int(H*0.955)
    return build(W, H, [
      dict(col=(178,214,44), ecol=(198,238,50), alpha=.95,
           figs=[(.17, G-H*.075, H*.145, 0), (.39, G-H*.075, H*.138, 2),
                 (.61, G-H*.075, H*.150, 1), (.83, G-H*.075, H*.142, 0)]),
      dict(col=(104,132,26), ecol=(170,206,42), echo=2,
           figs=[(.27, G-H*.027, H*.205, 2), (.54, G-H*.027, H*.198, 0),
                 (.80, G-H*.027, H*.210, 1)]),
      dict(col=INK, ecol=(150,186,30), echo=3,
           figs=[(.37, G, H*.305, 1), (.71, G, H*.292, 2)]),
    ], seed)

def make(kind, path, seed=11):
    img = tall(seed=seed) if kind == 'tall' else wide(seed=seed)
    path = os.path.splitext(path)[0] + '.png'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return path
