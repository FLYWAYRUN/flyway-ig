# -*- coding: utf-8 -*-
"""Running silhouette as smooth closed outlines.

The skeleton is still parametric (full pose control), but each limb chain is
emitted as ONE spline-smoothed outline instead of straight tapered segments
welded together. That continuous edge is what reads as drawn rather than built.
"""
import math

def _p(x, y, a, L):
    r = math.radians(a)
    return (x + L*math.sin(r), y + L*math.cos(r))

def _resample(pts, per=14):
    """Subdivide a joint polyline so the width profile can vary smoothly."""
    out = []
    for i in range(len(pts)-1):
        a, b = pts[i], pts[i+1]
        for k in range(per):
            t = k/per
            out.append((a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t))
    out.append(pts[-1])
    return out

def _normals(pts):
    n = []
    for i, p in enumerate(pts):
        a = pts[max(i-1, 0)]; b = pts[min(i+1, len(pts)-1)]
        dx, dy = b[0]-a[0], b[1]-a[1]
        L = math.hypot(dx, dy) or 1
        n.append((-dy/L, dx/L))
    return n

def _w_at(t, prof):
    """Piecewise-linear width lookup along the chain, t in 0..1."""
    for i in range(len(prof)-1):
        t0, w0 = prof[i]; t1, w1 = prof[i+1]
        if t0 <= t <= t1:
            u = (t-t0)/(t1-t0 or 1)
            return w0 + (w1-w0)*u
    return prof[-1][1]

def _catmull(pts, closed=True):
    """Catmull-Rom through the points, emitted as an SVG cubic path."""
    n = len(pts)
    g = (lambda i: pts[i % n]) if closed else (lambda i: pts[min(max(i,0), n-1)])
    d = f"M {g(0)[0]:.2f} {g(0)[1]:.2f}"
    last = n if closed else n-1
    for i in range(last):
        p0, p1, p2, p3 = g(i-1), g(i), g(i+1), g(i+2)
        c1 = (p1[0] + (p2[0]-p0[0])/6, p1[1] + (p2[1]-p0[1])/6)
        c2 = (p2[0] - (p3[0]-p1[0])/6, p2[1] - (p3[1]-p1[1])/6)
        d += f" C {c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {p2[0]:.2f} {p2[1]:.2f}"
    return d + (" Z" if closed else "")

def chain(joints, prof, per=14):
    """One closed, smoothed outline around a joint chain."""
    pts = _resample(joints, per)
    nrm = _normals(pts)
    m = len(pts)-1
    left  = [(p[0]+nx*_w_at(i/m, prof), p[1]+ny*_w_at(i/m, prof))
             for i, (p, (nx, ny)) in enumerate(zip(pts, nrm))]
    right = [(p[0]-nx*_w_at(i/m, prof), p[1]-ny*_w_at(i/m, prof))
             for i, (p, (nx, ny)) in enumerate(zip(pts, nrm))]
    # round the two ends instead of cutting them flat
    def cap(c, a, b, steps=7):
        out = []
        va = (a[0]-c[0], a[1]-c[1]); vb = (b[0]-c[0], b[1]-c[1])
        r = math.hypot(*va)
        a0 = math.atan2(va[1], va[0]); a1 = math.atan2(vb[1], vb[0])
        while a1 - a0 > math.pi:  a1 -= 2*math.pi
        while a1 - a0 < -math.pi: a1 += 2*math.pi
        for k in range(1, steps):
            t = a0 + (a1-a0)*k/steps
            out.append((c[0]+r*math.cos(t), c[1]+r*math.sin(t)))
        return out
    ring = left + cap(pts[-1], left[-1], right[-1]) + right[::-1] + cap(pts[0], right[0], left[0])
    return _catmull(ring, True)
