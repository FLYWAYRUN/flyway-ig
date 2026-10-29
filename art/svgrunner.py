# -*- coding: utf-8 -*-
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgfig import _p, chain, _catmull

def _disc(c, r):
    return (f"M {c[0]-r:.2f} {c[1]:.2f} a {r:.2f} {r:.2f} 0 1 0 {2*r:.2f} 0 "
            f"a {r:.2f} {r:.2f} 0 1 0 {-2*r:.2f} 0 Z")

def _ellipse(c, rx, ry, rot):
    pts = []
    for k in range(26):
        t = 2*math.pi*k/26
        x, y = rx*math.cos(t), ry*math.sin(t)
        a = math.radians(rot)
        pts.append((c[0] + x*math.cos(a) - y*math.sin(a),
                    c[1] + x*math.sin(a) + y*math.cos(a)))
    return _catmull(pts, True)

POSES = [
  dict(lean=11, lead=( 32,  -4, 70), trail=(-34, -16, 54), fwd=( 44, 132), back=(-50,  42)),
  dict(lean=12, lead=( 48,  14, 74), trail=(-38, 206, 80), fwd=( 30, 122), back=(-44,  50)),
  dict(lean=13, lead=( 18, -26, 66), trail=(-30, -44, 50), fwd=( 50, 138), back=(-56,  36)),
  dict(lean=10, lead=( 22, -14, 72), trail=(-42, 212, 84), fwd=( 38, 128), back=(-48,  46)),
]

def paths(x, ground, H, pose):
    """Return a list of SVG path 'd' strings for one runner."""
    lean = pose['lean']
    hx, hy = x, ground - H*0.50
    TH, SH, FT = H*0.250, H*0.240, H*0.062
    UA, FA = H*0.165, H*0.150
    out = []

    def leg(th, sh, ft, s=1.0):
        kn = _p(hx, hy, th, TH)
        an = _p(*kn, sh, SH)
        to = _p(*an, sh+ft, FT)
        # one continuous outline hip -> knee -> ankle -> toe.
        # glute, quad, knee pinch, calf belly, thin ankle, shoe.
        out.append(chain([(hx,hy), kn, an, to], [
            (0.00, H*.068*s), (0.16, H*.060*s), (0.34, H*.045*s),
            (0.48, H*.038*s), (0.58, H*.043*s), (0.74, H*.026*s),
            (0.84, H*.017*s), (0.93, H*.022*s), (1.00, H*.017*s)]))
        out.append(_disc((hx,hy), H*.062*s))   # hip
        out.append(_disc(kn, H*.039*s))
        out.append(_disc(an, H*.017*s))

    def arm(sp, ua, fa, s=1.0):
        el = _p(*sp, ua, UA)
        wr = _p(*el, fa, FA)
        out.append(chain([sp, el, wr], [
            (0.00, H*.040*s), (0.24, H*.034*s), (0.52, H*.025*s),
            (0.76, H*.023*s), (0.92, H*.019*s), (1.00, H*.010*s)]))
        out.append(_disc(el, H*.025*s))

    sp = _p(hx, hy, 180-lean, H*0.300)
    ar = _p(*sp, 180-lean, -H*0.036)
    hd = _p(*sp, 180-lean-10, H*0.078)

    leg(*pose['trail'], 0.94)
    arm(ar, *pose['back'], 0.93)

    # torso + neck + head as one silhouette: chest full, waist in, head sunk in
    ax, ay = sp[0]-hx, sp[1]-hy
    L = math.hypot(ax, ay) or 1
    nx, ny = -ay/L, ax/L
    ux, uy = ax/L, ay/L
    prof = [(-0.04, .062, .058), (0.26, .048, .052), (0.58, .060, .058),
            (0.86, .062, .060), (1.04, .044, .050)]
    front, back = [], []
    for t, wf, wb in prof:
        c = (hx+ax*t, hy+ay*t)
        front.append((c[0]+nx*H*wf, c[1]+ny*H*wf))
        back.append((c[0]-nx*H*wb, c[1]-ny*H*wb))
    out.append(_catmull(front + back[::-1], True))
    out.append(chain([sp, hd], [(0, H*.040), (0.45, H*.034), (1, H*.030)]))  # neck
    hr = H*0.043
    out.append(_ellipse(hd, hr*0.95, hr*1.10, -lean))

    leg(*pose['lead'])
    arm(ar, *pose['fwd'])
    return out

def svg(W, H, runners, bg='#D4FF36', fill='#08090B'):
    body = ''
    for r in runners:
        for d in paths(r['x'], r['g'], r['h'], POSES[r['p'] % len(POSES)]):
            body += f'<path d="{d}" fill="{r.get("col", fill)}"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{bg}"/>'
            f'{body}</svg>')
