# -*- coding: utf-8 -*-
"""Volt running poster as a single SVG. Nothing here is traced from a photograph."""
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgrunner import paths, POSES

VOLT='#D4FF36'; INK='#08090B'
FAR='#B2D62C'; MID='#64801８'.replace('８','8'); ECHO='#C6EC32'

def _layer(runners, col, opacity=1.0, blur=0):
    d = ''.join(p for r in runners
                  for p in paths(r['x'], r['g'], r['h'], POSES[r['p'] % len(POSES)]))
    body = ''.join(f'<path d="{p}" fill="{col}"/>' for r in runners
                   for p in paths(r['x'], r['g'], r['h'], POSES[r['p'] % len(POSES)]))
    f = f' filter="url(#b{blur})"' if blur else ''
    return f'<g opacity="{opacity}"{f}>{body}</g>'

def _echo(runners, col, n=3, step=0.026, W=1920):
    out = ''
    for k in range(n, 0, -1):
        off = W*step*k
        shifted = [dict(r, x=r['x']-off) for r in runners]
        out += _layer(shifted, col, opacity=round(0.34**k + 0.04, 3))
    return out

def _svg(W, H, rows, seed):
    defs = ('<defs>'
            '<filter id="b1"><feGaussianBlur stdDeviation="1.6"/></filter>'
            '<filter id="b2"><feGaussianBlur stdDeviation="2.8"/></filter>'
            '<filter id="grain"><feTurbulence baseFrequency="0.9" numOctaves="3" '
            f'seed="{seed}"/><feColorMatrix type="saturate" values="0"/>'
            '<feComponentTransfer><feFuncA type="linear" slope="0.055"/>'
            '</feComponentTransfer></filter></defs>')
    body = ''
    for r in rows:
        if r.get('echo'):
            body += _echo(r['runners'], r['ecol'], r['echo'], W=W)
        body += _layer(r['runners'], r['col'], blur=r.get('blur', 0))
    grain = f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity="0.5"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">{defs}'
            f'<rect width="{W}" height="{H}" fill="{VOLT}"/>{body}{grain}</svg>')

def _rows(W, H, G, sizes, seed):
    rnd = random.Random(seed)
    far, mid, hero = sizes
    def pack(fracs, h, dy, p0):
        return [dict(x=W*f + rnd.uniform(-W*.012, W*.012), g=G+dy,
                     h=h*rnd.uniform(.93, 1.07), p=i+p0) for i, f in enumerate(fracs)]
    return [
      dict(runners=pack([.46,.60,.74,.88], H*far,  -int(H*.15), 0),
           col=FAR, ecol='#C6EC32', blur=1),
      dict(runners=pack([.52,.70,.87],     H*mid,  -int(H*.05), 2),
           col=MID, ecol='#A8CC28', echo=2),
      dict(runners=pack([.60,.82],         H*hero, 0,           1),
           col=INK, ecol='#96BC1E', echo=3),
    ]

def wide(W=1920, H=800, seed=9):
    return _svg(W, H, _rows(W, H, int(H*.80), (.21, .33, .50), seed), seed)

def tall(W=1080, H=1350, seed=11):
    G = int(H*.945)
    rows = _rows(W, H, G, (.105, .155, .225), seed)
    rows[0]['runners'] = [dict(r, x=W*f) for r, f in
                          zip(rows[0]['runners'], [.18,.40,.62,.84])]
    rows[1]['runners'] = [dict(r, x=W*f) for r, f in
                          zip(rows[1]['runners'], [.28,.54,.80])]
    rows[2]['runners'] = [dict(r, x=W*f) for r, f in
                          zip(rows[2]['runners'], [.36,.70])]
    return _svg(W, H, rows, seed)

def make(kind, path, seed=11):
    svg = tall(seed=seed) if kind == 'tall' else wide(seed=seed)
    path = os.path.splitext(path)[0] + '.svg'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(svg)
    return path
