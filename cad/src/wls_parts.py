"""WellSense repo-specific CAD helpers (kit 1.9): small ISO screws and nuts, standoffs, circuit boards and
electronic components that .kit/cad_parts.py does not supply (it covers M5 and up).

Conventions follow .kit/cad_parts.py: a fastener is built along +Z with its head on the XY plane at z = 0
and its shank down -Z; threads are drawn as plain shanks at the nominal diameter. `on_axis()` places a part
built along +Z at a point with its +Z along any direction. Repo-specific; nothing here goes into .kit/.

Dimensions (nominal, typical catalogue values):
    ISO 7045 pan head (cross recess)  M2: dk 4.0, k 1.6     M3: dk 5.6, k 1.8     M4: dk 8.0, k 2.4
    ISO 7380 button head (hex socket) M5: dk 9.5, k 2.75
    ISO 10642 countersunk (hex socket) M4: dk 8.96, k 2.48 (90 degree head)
    ISO 4032 hex nut                  M3: s 5.5, m 2.4      M4: s 7.0, m 3.2
"""
from __future__ import annotations

import math

from build123d import Box, Cone, Cylinder, Plane, Pos, RegularPolygon, Rot, Vector, extrude, fillet, chamfer, Axis

PAN = {2: (4.0, 1.6), 3: (5.6, 1.8), 4: (8.0, 2.4)}
BUTTON = {5: (9.5, 2.75), 4: (7.6, 2.2), 3: (5.7, 1.65)}
CSK = {4: (8.96, 2.48), 3: (6.72, 1.86)}
NUT = {3: (5.5, 2.4), 4: (7.0, 3.2)}


def on_axis(shape, origin, direction):
    """Place a part built along +Z so that its local origin sits at `origin` and its +Z points along
    `direction` (any vector)."""
    d = Vector(*direction).normalized()
    x = Vector(0, 0, 1).cross(d)
    if x.length < 1e-6:
        x = Vector(1, 0, 0)
    pl = Plane(origin=Vector(*origin), x_dir=x.normalized(), z_dir=d)
    return pl.location * shape


def _shank(d, length):
    s = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    try:
        s = chamfer(s.edges().sort_by(Axis.Z)[0], d * 0.1)
    except Exception:
        pass
    return s


def pan_screw(d, length):
    """ISO 7045 pan head screw Md x length: domed head z 0 to k, shank down to -length."""
    dk, k = PAN[d]
    head = Pos(0, 0, k / 2) * Cylinder(dk / 2, k)
    try:
        head = fillet(head.edges().sort_by(Axis.Z)[-1:], k * 0.6)
    except Exception:
        pass
    slot = Pos(0, 0, k) * Box(dk * 0.6, d * 0.3, k * 0.9) + Pos(0, 0, k) * Box(d * 0.3, dk * 0.6, k * 0.9)
    return head - slot + _shank(d, length)


def button_screw(d, length):
    """ISO 7380 button head hex socket screw."""
    dk, k = BUTTON[d]
    head = Pos(0, 0, k / 2) * Cylinder(dk / 2, k)
    try:
        head = fillet(head.edges().sort_by(Axis.Z)[-1:], k * 0.7)
    except Exception:
        pass
    sock = Pos(0, 0, k) * extrude(RegularPolygon(d * 0.36, 6), -k * 0.6)
    return head - sock + _shank(d, length)


def csk_screw(d, length):
    """ISO 10642 countersunk hex socket screw: head top face on z = 0, cone down to -k, shank to -length."""
    dk, k = CSK[d]
    head = Pos(0, 0, -k) * Cone(d / 2, dk / 2, k, align=None)
    sock = extrude(RegularPolygon(d * 0.32, 6), -k * 0.7)
    return head - sock + Pos(0, 0, -k) * _shank(d, length - k)


def csk_seat(d, depth_extra=0.0):
    """The 90 degree countersink a csk_screw head sits in (to subtract from a plate), top at z = 0."""
    dk, k = CSK[d]
    return Pos(0, 0, -k) * Cone(d / 2 + 0.2, dk / 2 + 0.2, k + 0.01, align=None) + Pos(0, 0, depth_extra / 2) * Cylinder(dk / 2 + 0.2, max(depth_extra, 0.01))


def nut(d):
    """ISO 4032 hex nut M3 or M4, from z 0 to m, bore at the nominal diameter."""
    s, m = NUT[d]
    prism = extrude(RegularPolygon(s / math.sqrt(3), 6), m)
    try:
        cap = Pos(0, 0, m / 2) * Cylinder(s / math.sqrt(3), m)
        cap = chamfer(cap.edges(), s / math.sqrt(3) - s / 2 * 0.95)
        prism = prism & cap
    except Exception:
        pass
    return prism - Pos(0, 0, m / 2) * Cylinder(d / 2, m + 1)


def sealing_washer(d, t=1.0):
    """Bonded sealing washer under a screw head, z 0 to t."""
    return Pos(0, 0, t / 2) * (Cylinder(d * 1.2, t) - Cylinder(d / 2 + 0.05, t + 1))


def standoff(height, d=3, s=5.5, stud=5.4, bore=4.5):
    """Male-female hex standoff: hex body z 0 to height with a blind tapped bore from the top (drawn at the
    nominal diameter), and a male stud from z 0 down to -stud."""
    body = extrude(RegularPolygon(s / math.sqrt(3), 6), height)
    body = body - Pos(0, 0, height - bore / 2 + 0.01) * Cylinder(d / 2, bore)
    return body + Pos(0, 0, -stud / 2) * Cylinder(d / 2, stud)


def pcb(w, h, t=1.6, holes=(), r=1.0):
    """Circuit board w (X) x h (Y) x t (Z from 0) with rounded corners and mounting holes [(x, y, d)]."""
    from build123d import RectangleRounded, Sketch, Circle
    sk = Sketch() + RectangleRounded(w, h, r)
    for x, y, dd in holes:
        sk -= Pos(x, y) * Circle(dd / 2)
    return extrude(sk, t)


def ic(w, h, t, pins=True):
    """A moulded IC package w x h x t on z = 0 (a pin-1 dimple on top, gull-wing pin rows if pins)."""
    body = Pos(0, 0, t / 2) * Box(w, h, t)
    try:
        body = fillet(body.edges().filter_by(Axis.Z), min(w, h) * 0.06)
    except Exception:
        pass
    body = body - Pos(-w / 2 + min(w, h) * 0.2, h / 2 - min(w, h) * 0.2, t) * Cylinder(min(w, h) * 0.08, 0.3)
    if pins:
        n = max(2, int(h // 1.27))
        for i in range(n):
            y = -h / 2 + (i + 0.5) * h / n
            for sx in (-1, 1):
                body = body + Pos(sx * (w / 2 + 0.4), y, 0.25) * Box(0.8, 0.4, 0.5)
    return body


def can_cap(r, h):
    """Electrolytic capacitor (aluminium can with a vent cross) on z = 0."""
    c = Pos(0, 0, h / 2) * Cylinder(r, h)
    try:
        c = fillet(c.edges().sort_by(Axis.Z)[-1:], r * 0.15)
    except Exception:
        pass
    return c - Pos(0, 0, h) * Box(r * 1.2, 0.3, 0.4) - Pos(0, 0, h) * Box(0.3, r * 1.2, 0.4)


def inductor(w, h):
    """Shielded power inductor, square w with chamfered corners, height h, on z = 0."""
    b = Pos(0, 0, h / 2) * Box(w, w, h)
    try:
        b = chamfer(b.edges().filter_by(Axis.Z), w * 0.15)
    except Exception:
        pass
    return b


def header(n, pitch=2.54, h=8.5):
    """Single-row pin header of n pins along X on z = 0 (plastic strip and square pins)."""
    strip = Pos(0, 0, 1.25) * Box(n * pitch, pitch, 2.5)
    for i in range(n):
        strip = strip + Pos(-n * pitch / 2 + (i + 0.5) * pitch, 0, h / 2) * Box(0.64, 0.64, h)
    return strip


def terminal_block(n, pitch=5.0, depth=10.0, h=10.0):
    """Pluggable screw terminal block of n ways along X on z = 0: body with a screw hole on top and a wire
    entry on the front (+Y) of each way."""
    body = Pos(0, 0, h / 2) * Box(n * pitch, depth, h)
    for i in range(n):
        x = -n * pitch / 2 + (i + 0.5) * pitch
        body = body - Pos(x, -depth * 0.15, h - 1.5) * Cylinder(pitch * 0.32, 3.2)
        body = body - Pos(x, depth / 2 - 1.5, h * 0.35) * Box(pitch * 0.6, 3.2, h * 0.4)
    return body
