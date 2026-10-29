# -*- coding: utf-8 -*-
"""Running silhouette built from joint angles, with human mass on the limbs.

Angles are ABSOLUTE: 0 = down, 90 = forward (+x), 180 = up, 270 = backward.
Feet are relative to the shin. Lean tilts only torso and head.
"""
from PIL import ImageDraw
import math

SS = 4

def _p(x, y, a, L):
    r = math.radians(a)
    return (x + L*math.sin(r), y + L*math.cos(r))

def _lerp(p, q, t):
    return (p[0] + (q[0]-p[0])*t, p[1] + (q[1]-p[1])*t)

def _seg(d, p0, p1, widths, fill):
    """Limb with a mid-bulge: widths = [(t, halfwidth), ...] along p0->p1.
    This is what separates a leg from a pipe."""
    dx, dy = p1[0]-p0[0], p1[1]-p0[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy/L, dx/L
    left, right = [], []
    for t, w in widths:
        c = _lerp(p0, p1, t)
        left.append((c[0]+nx*w, c[1]+ny*w))
        right.append((c[0]-nx*w, c[1]-ny*w))
    d.polygon(left + right[::-1], fill=fill)
    for (t, w) in (widths[0], widths[-1]):
        c = _lerp(p0, p1, t)
        d.ellipse([c[0]-w, c[1]-w, c[0]+w, c[1]+w], fill=fill)

# proportions read off real runners: head ≈ 1/7.5 of height, legs ≈ half
POSES = [
  dict(lean=11, lead=( 32,  -4, 70), trail=(-34, -16, 54), fwd=( 44, 132), back=(-50,  42)),
  dict(lean=12, lead=( 48,  14, 74), trail=(-38, 206, 80), fwd=( 30, 122), back=(-44,  50)),
  dict(lean=13, lead=( 18, -26, 66), trail=(-30, -44, 50), fwd=( 50, 138), back=(-56,  36)),
  dict(lean=10, lead=( 22, -14, 72), trail=(-42, 212, 84), fwd=( 38, 128), back=(-48,  46)),
]

def runner(d, x, ground, H, pose, fill, ponytail=False):
    # ponytail reads as a cap brim at small sizes; off unless asked for
    lean = pose['lean']
    hx, hy = x, ground - H*0.50
    TH, SH, FT = H*0.250, H*0.240, H*0.070
    UA, FA      = H*0.165, H*0.150
    TORSO       = H*0.300

    def leg(th, sh, ft_rel, s=1.0):
        kn = _p(hx, hy, th, TH)
        an = _p(*kn, sh, SH)
        to = _p(*an, sh + ft_rel, FT)
        # thigh: heavy at the hip, slims into the knee
        _seg(d, (hx,hy), kn, [(0, H*.062*s), (.45, H*.053*s), (1, H*.034*s)], fill)
        # shin: the calf belly sits high, then tapers hard to a thin ankle
        _seg(d, kn, an,   [(0, H*.033*s), (.30, H*.040*s), (.72, H*.024*s), (1, H*.016*s)], fill)
        # shoe
        _seg(d, an, to,   [(0, H*.020*s), (.55, H*.021*s), (1, H*.012*s)], fill)

    def arm(sp, ua, fa, s=1.0):
        el = _p(*sp, ua, UA)
        wr = _p(*el, fa, FA)
        _seg(d, sp, el, [(0, H*.036*s), (.40, H*.033*s), (1, H*.023*s)], fill)
        _seg(d, el, wr, [(0, H*.023*s), (.45, H*.023*s), (1, H*.013*s)], fill)

    sp = _p(hx, hy, 180 - lean, TORSO)        # shoulder
    ar = _p(*sp, 180 - lean, -H*0.034)        # shoulder joint sits below the trap

    leg(*pose['trail'], 0.93)
    arm(ar, *pose['back'], 0.92)

    # torso: chest fuller than waist, shoulders broad. a bar reads as a stick figure.
    ax, ay = sp[0]-hx, sp[1]-hy
    L = math.hypot(ax, ay) or 1
    nx, ny = -ay/L, ax/L
    prof = [(0.00, .054, .050), (0.30, .045, .048),
            (0.64, .058, .055), (0.90, .060, .058), (1.00, .050, .052)]
    front, back = [], []
    for t, wf, wb in prof:
        c = _lerp((hx,hy), sp, t)
        front.append((c[0]+nx*H*wf, c[1]+ny*H*wf))
        back.append((c[0]-nx*H*wb, c[1]-ny*H*wb))
    d.polygon(front + back[::-1], fill=fill)

    # neck + head. head radius ~1/7.5 of total height, carried forward
    nk = _p(*sp, 180 - lean - 6, H*0.018)
    _seg(d, sp, nk, [(0, H*.040), (1, H*.034)], fill)   # short, thick: no gap at the collar
    hr = H*0.042
    hd = _p(*nk, 180 - lean - 12, hr*0.88)
    d.ellipse([hd[0]-hr*0.94, hd[1]-hr*1.10, hd[0]+hr*0.94, hd[1]+hr*1.10], fill=fill)
    if ponytail:
        t0 = _p(*hd, 272 - lean*0.4, hr*0.92)      # back of the skull, not the crown
        t1 = _p(*t0, 288 - lean*0.4, H*0.060)      # streams back, roughly level
        t2 = _p(*t1, 302 - lean*0.4, H*0.038)
        _seg(d, t0, t1, [(0, H*.028), (.55, H*.022), (1, H*.015)], fill)
        _seg(d, t1, t2, [(0, H*.015), (.6, H*.010), (1, H*.004)], fill)

    leg(*pose['lead'])
    arm(ar, *pose['fwd'])
