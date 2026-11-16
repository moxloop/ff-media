"""Figures Forward component kit: the shared harness every component in this folder is built on.

It loads lib/vlib.py UNCHANGED (only the Episode 04 audio/word-timing block is skipped at load time, because a
component library has no narration of its own), adds the Option C logo, a camera, the fit check from
lib/render_vox.py, and the preview / still / contact-sheet / catalogue tooling.

Orientation: FF_ORIENT=h (default, 1920x1080) or FF_ORIENT=v (1080x1920 Shorts, safe area x 110-870, y 290-1440).

A component is a function  fn(base, d, lt, cam, **params)  that draws on the stage at local time `lt` (seconds).
Register it with @component(...). Every default parameter value is a generic illustration, never a real figure:
episodes pass their own asserted figures. A transition is  fn(a, b, p) -> frame  on two rendered frames.

Use from a build:
    import sys; sys.path.insert(0, ".../house-style/components")
    from kit import *; import hooks, reveals            # etc.
    hooks.number_transform(base, d, lt, cam, start="£100", ...)

Tooling:  python3 run.py check|render|still|sheet|catalogue|time [filter]      (FF_ORIENT=v for the Shorts set)
"""
import os, sys, types, math, random, json, subprocess, inspect, time
sys.dont_write_bytecode = True
HERE_C = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE_C)
ORIENT = os.environ.get("FF_ORIENT", "h"); assert ORIENT in ("h", "v")

def _load_vlib():
    p = os.path.join(ROOT, "lib", "vlib.py"); src = open(p).read()
    a, b = src.index("# ---------------- scenes and word timing"), src.index("# ---------------- small helpers")
    src = src[:a] + src[b:]
    if ORIENT == "v":
        assert "W, H, FPS = 1920, 1080, 30" in src; src = src.replace("W, H, FPS = 1920, 1080, 30", "W, H, FPS = 1080, 1920, 30")
    m = types.ModuleType("vlib"); m.__file__ = os.path.join(ROOT, "vlib.py")       # so fonts/, assets/ and seg/ resolve to house-style/
    os.makedirs(os.path.join(ROOT, "seg"), exist_ok=True)
    exec(compile(src, p, "exec"), m.__dict__); sys.modules["vlib"] = m; return m
V = _load_vlib()
globals().update({k: v for k, v in V.__dict__.items() if not k.startswith("__")})
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

MX, MY = W / 2, H / 2                                   # stage centre
SAFE = (110, 290, 870, 1440)                            # Shorts safe area (frame px)
BROWN = (88, 66, 36); DGREEN = (40, 150, 100); RED = (214, 72, 56); GRID = (214, 226, 238); GRID2 = (188, 206, 226)
V.HLC.setdefault("y", (255, 232, 120))

# ---------------- craft helpers (ported from reference/ep4_5b and ep4_5c) ----------------
def rec(kind, box, name=""):
    """Record a box for the fit check. kind: 'c' card, 't' text, 'i' picture, 'z' chart. Stage coordinates."""
    if V.FIT is not None: V.FIT.append((kind, tuple(box), name))
def fa(lt, t0, d=.3): return ease((lt - t0) / d)
def fx(lt, t1, d=.3): return 1 - ease((lt - t1) / d)
def chime(lt, t0): appear(lt, t0, .4, "chime")
def sfx(lt, t0, name, d=.3): appear(lt, t0, d, name)
def par(cam, x, y, k=.07, lt=0, seed=0):
    """Foreground parallax (moves against the camera) plus a slow paper float."""
    return x - (cam[0] - MX) * k, y - (cam[1] - MY) * k + 4 * math.sin(2 * math.pi * lt / 3.2 + seed)
def note(d, lt, x, y, s, size, t0, fill=INK, on=PAPER, anchor="la", f="c", t1=None):
    """Handwritten (Caveat) aside that fades up."""
    a = ease((lt - t0) / .3) * (fx(lt, t1) if t1 else 1)
    T(d, x, y, s, size, f, fill, anchor, a, on, dy=10 * (1 - eout((lt - t0) / .3)))
def big(d, lt, x, y, s, size, t0, hk=None, f="a", fill=INK, on=PAPER, anchor="l", ref=None):
    """Large figure with an optional highlighter swipe behind it. Returns (x0, top, x1, bottom) in stage px."""
    a = ease((lt - t0) / .25); fo = F(f, size); w = fo.getlength(ref or s) / S
    x0 = x - (w if anchor == "r" else w / 2 if anchor == "m" else 0)
    bb = fo.getbbox("H0"); top, bot = bb[1] / S, bb[3] / S
    if hk:
        ph = appear(lt, t0 + .3, .45, "marker")
        if a > .03: hl(d, x0, y + top + (bot - top) * .06, x0 + w, y + bot + (bot - top) * .1, mix(on, HLC[hk], .95), ph)
    if a > .03: T(d, x0, y, s, size, f, fill, "la", a, on)
    return (x0, y + top, x0 + w, y + bot)
def ruled(d, box, a=1.0, step=56, on=CARD):
    """Ruled-paper lines and a margin line inside a card box."""
    for yy in range(int(box[1]) + 46, int(box[3]) - 10, step): d.line([X(box[0] + 18), X(yy), X(box[2] - 18), X(yy)], fill=mix(on, (200, 220, 240), a * .7), width=2)
    d.line([X(box[0] + 22), X(box[1] + 10), X(box[0] + 22), X(box[3] - 10)], fill=mix(on, (255, 190, 170), a), width=2)
def graph(d, box, step=40, a=1.0, on=CARD, inset=16):
    """Graph-paper grid inside a card box (draw after the card has landed). Also records the chart box."""
    x0, y0, x1, y1 = box
    for i, gx in enumerate(range(int(x0 + inset), int(x1 - inset) + 1, step)): d.line([X(gx), X(y0 + inset), X(gx), X(y1 - inset)], fill=mix(on, GRID2 if i % 5 == 0 else GRID, a), width=2)
    for i, gy in enumerate(range(int(y0 + inset), int(y1 - inset) + 1, step)): d.line([X(x0 + inset), X(gy), X(x1 - inset), X(gy)], fill=mix(on, GRID2 if i % 5 == 0 else GRID, a), width=2)
    rec("z", box)
def morph(d, lt, x, y, seq, size, f="a", anchor="mm", on=PAPER, dur=.35, snd="pop", grow=.12):
    """Kinetic text that re-forms: each entry (t0, text, colour) scales in while the previous one swells and fades."""
    for i, (t0, _, _) in enumerate(seq):
        if i: appear(lt, t0, dur, snd)
    cur = None
    for i, (t0, _, _) in enumerate(seq):
        if lt >= t0: cur = i
    if cur is None: return
    t0, s, col = seq[cur]; u = clamp((lt - t0) / dur)
    if cur and u < 1: _, ps, pcol = seq[cur - 1]; T(d, x, y, ps, size * (1 + grow * u), f, pcol, anchor, 1 - u * 1.4, on)
    T(d, x, y, s, size * (.55 + .45 * back(u)), f, col, anchor, min(1, u * 1.8), on)
def vmorph(d, lt, x, y, keys, size, on=CARD, dur=.8, f="a", anchor="rm", fmt=None):
    """A figure that counts and re-forms into the next figure: keys = [(t0, value, colour)]; the first value is the start."""
    fmt = fmt or (lambda v: gbp(round(v)))
    for t0, _, _ in keys[1:]: appear(lt, t0, dur, "ticks")
    if lt < keys[0][0]: return
    v, col, pulse = keys[0][1], keys[0][2], 0.0
    for (t0, v1, c1) in keys[1:]:
        if lt >= t0: u = clamp((lt - t0) / dur); v = v + (v1 - v) * ease(u); col = c1; pulse = math.sin(math.pi * u) * .14
    sc = (.6 + .4 * back((lt - keys[0][0]) / .35)) * (1 + pulse)
    T(d, x, y, fmt(v), size * sc, f, col, anchor, min(1, (lt - keys[0][0]) / .2), on)
def token(base, lt, p0, p1, t_on, t_go, text, fill, fg, rot, t1=None, size=52):
    """A paper token (e.g. £100) that pops on at p0 and slides in an arc to p1."""
    appear(lt, t_go, .5, "slide")
    u = eout((lt - t_go) / .55); x = p0[0] + (p1[0] - p0[0]) * u; y = p0[1] + (p1[1] - p0[1]) * u - 40 * math.sin(math.pi * u)
    tag(base, lt, x, y, text, size, t_on, fill, fg, rot * (1 - u) + 2 * u * (1 if rot >= 0 else -1), "a", "pop", (18, 10), t1)
def jar(base, d, lt, cx, cy, t0, level, col=None, drops=None, w=72, h=88, on=PAPER):
    """A paper jar drawn in code (empty to start) that fills to `level` (0-1). drops=(rate, t_start) shows coins dropping in."""
    a = appear(lt, t0, .5, "pop")
    if a <= .03: return
    col = col or DISC["b"]; e = back(clamp((lt - t0) / .5)); w, h = w * e, h * e
    if drops:
        rate, ts = drops
        if lt > ts:
            for n in range(4):
                ph = ((lt - ts) * rate + n / 4) % 1
                if lt - ts > ph / rate: yy = cy - h - 64 + 64 * ph * ph; d.ellipse([X(cx - 9), X(yy - 9), X(cx + 9), X(yy + 9)], fill=mix(on, col, 1 - ph ** 4))
    d.rounded_rectangle([X(cx - w), X(cy - h), X(cx + w), X(cy + h)], int(26 * S), fill=mix(on, (244, 246, 248), a))
    if level > .005:
        top = cy + h - 8 - (2 * h - 16) * clamp(level)
        d.rounded_rectangle([X(cx - w + 8), X(top), X(cx + w - 8), X(cy + h - 8)], int(18 * S), fill=col)
    d.rounded_rectangle([X(cx - w), X(cy - h), X(cx + w), X(cy + h)], int(26 * S), outline=mix(on, INK, a), width=int(5 * S))
    d.rounded_rectangle([X(cx - w * .78), X(cy - h - 24), X(cx + w * .78), X(cy - h + 2)], int(6 * S), fill=mix(on, KRAFT, a), outline=mix(on, INK, a), width=int(3 * S))
    rec("i", (cx - w - 4, cy - h - 30, cx + w + 4, cy + h + 4), "jar")
def rot_paste(base, sprite, cx, cy, deg=0.0, scale=1.0, a=1.0):
    """Paste an RGBA sprite (canvas px) centred on a stage point, rotated and scaled. Returns its stage bounding box."""
    sp = sprite
    if abs(scale - 1) > .004: sp = sp.resize((max(2, int(sp.size[0] * scale)), max(2, int(sp.size[1] * scale))), Image.BILINEAR)
    if abs(deg) > .05: sp = sp.rotate(deg, Image.BICUBIC, expand=True)
    paste(base, sp, X(cx) - sp.size[0] / 2, X(cy) - sp.size[1] / 2, a)
    return (cx - sp.size[0] / 2 / S, cy - sp.size[1] / 2 / S, cx + sp.size[0] / 2 / S, cy + sp.size[1] / 2 / S)

# ---------------- registry ----------------
REG = {}
FAMILIES = [("hooks", "Hook openers"), ("transitions", "Transitions"), ("charts", "Charts"), ("comparisons", "Comparisons"),
            ("evidence", "Evidence"), ("reveals", "Number reveals"), ("endcards", "Recap and end cards"),
            ("shorts_hooks", "Shorts 9:16 hook openers"), ("shorts_comparisons", "Shorts 9:16 comparisons"), ("shorts_reveals", "Shorts 9:16 number reveals")]
def component(family, name, dur=5.0, cam=None, use="", still=None, logo=True, notes=""):
    """Register a component. cam: [(t, cx, cy, zoom), ...] stage keyframes (default: start close, pull out, slow push)."""
    def wrap_(fn):
        REG[f"{family}/{name}"] = dict(kind="component", fn=fn, family=family, name=name, dur=dur, cam=cam, use=use, still=still, logo=logo, notes=notes); return fn
    return wrap_
def transition(name, dur=.9, use="", notes="", snd="whoosh"):
    """Register a transition  fn(a, b, p) -> frame  (a, b: HxWx3 uint8 frames before the logo is added; p: 0-1)."""
    def wrap_(fn):
        REG[f"transitions/{name}"] = dict(kind="transition", fn=fn, family="transitions", name=name, dur=5.0, tdur=dur, use=use, still=None, logo=True, notes=notes, snd=snd); return fn
    return wrap_

# ---------------- camera, stage and frame ----------------
def cam_at(keys, lt, dur):
    ks = keys or ([(0, MX, MY, 1.08), (1.1, MX, MY, 1.0), (dur, MX, MY, 1.03)] if ORIENT == "h" else [(0, MX, MY, 1.0), (dur, MX, MY, 1.0)])
    cx = pw(lt, [(k[0], k[1]) for k in ks]); cy = pw(lt, [(k[0], k[2]) for k in ks]); z = pw(lt, [(k[0], k[3]) for k in ks])
    cx += 5 * math.sin(.6 * lt); cy += 3 * math.sin(.43 * lt + 1)
    cx = clamp(cx, W / 2 / z - BLEED + 2, W + BLEED - W / 2 / z - 2); cy = clamp(cy, H / 2 / z - BLEED + 2, H + BLEED - H / 2 / z - 2)
    return cx, cy, z
def stage(fn, lt, cam, params=None, fit=False, seed=0):
    """Draw one component on fresh paper and apply the camera. Returns the frame (no logo yet) and, with fit, its boxes in frame px."""
    cx, cy, z = cam; ox = int(seed * 911 - (cx - MX) * S * .45) % TW_; oy = int(seed * 577 - (cy - MY) * S * .45) % (2 * TH_ - CH)
    base = Image.fromarray(np.ascontiguousarray(tile2()[oy:oy + CH, ox:ox + CW])); d = ImageDraw.Draw(base)
    if fit: V.FIT = []
    fn(base, d, lt, cam, **(params or {}))
    M = np.float32([[z / S, 0, W / 2 - (cx + BLEED) * z], [0, z / S, H / 2 - (cy + BLEED) * z]])
    out = cv2.warpAffine(np.asarray(base), M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if not fit: return out
    items = [(k, ((b[0] - cx) * z + W / 2, (b[1] - cy) * z + H / 2, (b[2] - cx) * z + W / 2, (b[3] - cy) * z + H / 2), n) for k, b, n in V.FIT]
    V.FIT = None; return out, items

_HUD = None
def hud():
    """Fixed overlays in frame px. Logo: Option C, the on-dark lockup on a dark ink label, tilted 1.5 degrees, soft shadow,
    a strip of semi-transparent tape on its top-right corner; top left, same size on every scene. Plus the disclaimer label."""
    global _HUD
    if _HUD is None:
        lh = 46 if ORIENT == "h" else 40; fs = 24 if ORIENT == "h" else 20
        lk = Image.open(os.path.join(ROOT, "assets", "lockup_horizontal_on-dark.png")).convert("RGBA"); lk = lk.resize((int(lk.size[0] * lh / lk.size[1]), lh), Image.LANCZOS)
        w, h = lk.size[0] + 30, lh + 20; a = panel_sprite(w, h, INK, 77).copy(); a.alpha_composite(lk, (PAD + 15, PAD + 10))
        cv = Image.new("RGBA", (a.size[0] + 60, a.size[1] + 50), (0, 0, 0, 0)); cv.alpha_composite(a, (20, 30))
        tp = Image.new("RGBA", (78, 26), (236, 226, 190, 168)); td = ImageDraw.Draw(tp)
        for xx in (0, 76): td.line([(xx, 0), (xx, 26)], fill=(236, 226, 190, 90), width=2)
        tp = tp.rotate(-22, Image.BICUBIC, expand=True); cv.alpha_composite(tp, (20 + PAD + w - tp.size[0] // 2 - 8, 30 + PAD - tp.size[1] // 2 + 2))
        cv = cv.rotate(1.5, Image.BICUBIC, expand=True)
        bb = cv.getchannel("A").point(lambda v: 255 if v > 120 else 0).getbbox()
        lx, ly = (44, 26) if ORIENT == "h" else (SAFE[0], 196)
        px, py = lx - bb[0], ly - bb[1]; lbox = (lx, ly, lx + bb[2] - bb[0], ly + bb[3] - bb[1])
        txt = "General information, not financial advice"; fo = font("sb", fs); tl = int(fo.getlength(txt)); w2, h2 = tl + (40 if ORIENT == "h" else 32), 2 * fs
        b = panel_sprite(w2, h2, INK, 78).copy(); pad2 = (w2 - tl) // 2; ImageDraw.Draw(b).text((PAD + pad2, PAD + h2 / 2), txt, font=fo, fill=CREAM, anchor="lm")
        dbox = (W - 44 - w2, H - 26 - h2, W - 44, H - 26) if ORIENT == "h" else (SAFE[2] - w2, 214, SAFE[2], 214 + h2)
        tb = ImageDraw.Draw(b).textbbox((PAD + pad2, PAD + h2 / 2), txt, font=fo, anchor="lm"); tbox = (dbox[0] + tb[0] - PAD, dbox[1] + tb[1] - PAD, dbox[0] + tb[2] - PAD, dbox[1] + tb[3] - PAD)
        def prep(im, x, y):
            arr = np.asarray(im, np.float32); return (int(x), int(y), arr[:, :, :3], arr[:, :, 3:] / 255)
        _HUD = (prep(cv, px, py), prep(b, dbox[0] - PAD, dbox[1] - PAD), lbox, dbox, tbox, txt)
    return _HUD
LOGO_BOX = lambda: hud()[2]
DISCLAIMER_BOX = lambda: hud()[3]
def _put(out, spr, a=1.0):
    x, y, rgb, al = spr; x0, y0 = max(0, -x), max(0, -y); rgb = rgb[y0:, x0:]; al = al[y0:, x0:] * a; x, y = max(0, x), max(0, y)
    h, w = rgb.shape[:2]; reg = out[y:y + h, x:x + w].astype(np.float32)
    out[y:y + h, x:x + w] = (reg * (1 - al) + rgb * al).astype(np.uint8)
_VIG = None
def _vig():
    global _VIG
    if _VIG is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 1.414
        v = np.clip(1 - .30 * r ** 2.6, 0, 1); _VIG = np.dstack([v, v, v]).astype(np.float32)
    return _VIG
def finish(out, logo=1.0, items=None):
    """Vignette, then the logo label and the disclaimer. With items (fit boxes) the HUD boxes are appended."""
    out = cv2.multiply(out.astype(np.float32), _vig()).astype(np.uint8); lg, ds, lbox, dbox, tbox, txt = hud()
    if logo > .01: _put(out, lg, logo)
    _put(out, ds)
    if items is not None:
        if logo > .5: items.append(("c", lbox, "logo"))
        items += [("c", dbox, "disclaimer"), ("t", tbox, txt)]
    return out

# ---- demo scenes used only to preview transitions ----
def _demo_a(base, d, lt, cam):
    kline(d, lt, 110, 150, [("SCENE", -1, INK, None), ("ONE", -1, INK, "o")], 88, "a")
    panel(base, lt, (110, 330, 900, 800), -1, CARD, sfx=None, seed=3); T(d, 160, 380, "BEFORE", 40, "o", MUTED, on=CARD); T(d, 160, 470, "£1,000", 170, "a", ORANGE, on=CARD)
    cut(base, lt, "house", 1400, 560, 300, -1, rot=-5, disc=("o", 190), sfx=None)
def _demo_b(base, d, lt, cam):
    kline(d, lt, 110, 150, [("SCENE", .15, INK, None), ("TWO", .3, INK, "b")], 88, "a")
    panel(base, lt, (1020, 330, 1810, 800), .2, KRAFT, sfx=None, seed=5); T(d, 1070, 380, "AFTER", 40, "o", BROWN, on=KRAFT, a=fa(lt, .4)); T(d, 1070, 470, "£2,000", 170, "a", INK, on=KRAFT, a=fa(lt, .5))
    cut(base, lt, "chart", 520, 560, 300, .3, rot=4, disc=("b", 190), sfx=None)
T_CUT = 2.0
def frame(key, t, fit=False, params=None):
    """Finished frame of a registered component (or of a transition's demo) at time t."""
    e = REG[key]
    if e["kind"] == "transition":
        td = e["tdur"]; ca = cam_at(None, t, 5.0); cb = cam_at(None, max(0, t - T_CUT), 5.0); items = None
        if t < T_CUT: r = stage(_demo_a, t + 3, ca, fit=fit, seed=1); out, items = r if fit else (r, None)
        elif t >= T_CUT + td: r = stage(_demo_b, t - T_CUT - td * .5, cb, fit=fit, seed=2); out, items = r if fit else (r, None)
        else: out = e["fn"](stage(_demo_a, t + 3, ca, seed=1), stage(_demo_b, max(0, t - T_CUT - td * .5), cb, seed=2), (t - T_CUT) / td); items = [] if fit else None
        out = finish(np.ascontiguousarray(out), 1.0, items); return (out, items) if fit else out
    cam = cam_at(e["cam"], t, e["dur"]); r = stage(e["fn"], t, cam, params, fit)
    out, items = r if fit else (r, None); lg = 1.0 if e["logo"] else 0.0
    out = finish(out, lg, items); return (out, items) if fit else out

# ---------------- fit check (same rules as lib/render_vox.py, plus the Shorts safe area) ----------------
def _hit(a, b, pad=0): return not (a[2] + pad <= b[0] or a[0] - pad >= b[2] or a[3] + pad <= b[1] or a[1] - pad >= b[3])
def _inside(a, b, m): return a[0] >= b[0] + m and a[1] >= b[1] + m and a[2] <= b[2] - m and a[3] <= b[3] - m
def fit_items(items, margin=6):
    """Problems for one frame's boxes: text inside any card it touches (6 px) and on-frame; no text on a picture and pictures
    >= 20 px from text; a picture is inside a card or >= 40 px from it; no card over a chart; Shorts text inside the safe area."""
    bad = []; cards = [(b, nm) for k, b, nm in items if k == "c"]; texts = [(b, s) for k, b, s in items if k == "t"]; hudt = hud()[5]
    for k, ib, nm in items:
        if k != "i": continue
        if ib[0] < 0 or ib[1] < 0 or ib[2] > W or ib[3] > H: bad.append((nm, "picture off frame"))
        for tb, s in texts:
            if _hit(ib, tb): bad.append((s, f"overlaps the {nm} picture"))
            elif _hit(ib, tb, 20): bad.append((s, f"closer than 20 px to the {nm} picture"))
        for c, cn in cards:
            if not _inside(ib, c, margin) and _hit(ib, c, 40): bad.append((nm, f"picture within 40 px of a card {cn}"))
    for z_ in [b for k, b, _ in items if k == "z"]:
        for c, cn in cards:
            if _hit(c, z_) and not (abs(c[0] - z_[0]) < 1 and abs(c[2] - z_[2]) < 1): bad.append((f"card {cn}", "overlaps a chart"))
    for tb, s in texts:
        if tb[0] < 0 or tb[1] < 0 or tb[2] > W or tb[3] > H: bad.append((s, "off frame"))
        if ORIENT == "v" and s != hudt and not _inside(tb, SAFE, 0): bad.append((s, "outside the Shorts safe area"))
        for c, cn in cards:
            if _hit(tb, c) and not _inside(tb, c, margin): bad.append((s, f"crosses a card {cn}"))
    return bad
def fit_check(key, step=.2, verbose=True):
    e = REG[key]; bad = {}; t = 0.0; n = 0
    while t < e["dur"]:
        _, items = frame(key, t, True); n += 1
        for s, why in fit_items(items): bad.setdefault((s, why), t)
        t += step
    if verbose:
        for (s, why), tt in sorted(bad.items(), key=lambda kv: kv[1]): print(f"  FIT FAIL {key} @{tt:.2f}s: {s!r} {why}")
        print(f"fit {key} ({n} samples, camera applied):", "PASS" if not bad else f"{len(bad)} problems")
    return not bad, n
def sfx_events(key, params=None):
    """(time, sound, length) for every entrance in a component, for the builder's mix."""
    e = REG[key]; V.COLLECT = []; base = Image.new("RGB", (CW, CH), PAPER)
    e["fn"](base, ImageDraw.Draw(base), 9999.0, (MX, MY, 1), **(params or {})); ev = sorted(V.COLLECT); V.COLLECT = None; return ev

# ---------------- previews, stills, contact sheet, catalogue ----------------
SUF = "" if ORIENT == "h" else "_v"
def fname(key): return key.replace("/", "__")
def render(key):
    e = REG[key]; pv = os.path.join(HERE_C, "previews"); os.makedirs(pv, exist_ok=True); out = os.path.join(pv, fname(key) + ".mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", f"scale={W // 2}:{H // 2}:flags=area", "-c:v", "libx264", "-preset", "slow", "-crf", "30", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for f in range(round(e["dur"] * FPS)): p.stdin.write(np.ascontiguousarray(frame(key, f / FPS)).tobytes())
    p.stdin.close(); p.wait(); still(key); return out
def still_t(e): return e["still"] if e["still"] is not None else ((T_CUT + e["tdur"] * .5) if e["kind"] == "transition" else e["dur"] - .35)
def still(key):
    e = REG[key]; sd = os.path.join(HERE_C, "stills"); os.makedirs(sd, exist_ok=True); out = os.path.join(sd, fname(key) + ".jpg")
    Image.fromarray(frame(key, still_t(e))).resize((W * 2 // 3, H * 2 // 3), Image.LANCZOS).save(out, quality=86); return out
def _params(fn):
    return [(n, repr(p.default)) for n, p in list(inspect.signature(fn).parameters.items())[(2 if REG_KIND.get(fn) == "transition" else 4):] if p.default is not inspect._empty]
REG_KIND = {}
def manifest(results=None):
    """Write manifest_<orient>.json: what the catalogue is generated from."""
    for e in REG.values(): REG_KIND[e["fn"]] = e["kind"]
    p = os.path.join(HERE_C, f"manifest_{ORIENT}.json"); old = {m["key"]: m for m in (json.load(open(p)) if os.path.exists(p) else [])}; rows = []
    for key, e in REG.items():
        o = old.get(key, {}); r = (results or {}).get(key)
        rows.append(dict(key=key, family=e["family"], name=e["name"], kind=e["kind"], module=e["fn"].__module__, func=e["fn"].__name__, use=e["use"], notes=e["notes"],
                         dur=e.get("tdur", e["dur"]), params=_params(e["fn"]), preview=f"previews/{fname(key)}.mp4", still=f"stills/{fname(key)}.jpg",
                         fit=("PASS" if r[0] else "FAIL") if r else o.get("fit", "not run"), samples=r[1] if r else o.get("samples", 0)))
    json.dump(rows, open(p, "w"), indent=1); return rows
def sheets():
    """Contact sheets from the saved stills: contact_sheet.png (16:9) and contact_sheet_vertical.png (9:16)."""
    for o, cols, cw, ch in (("h", 4, 480, 270), ("v", 6, 216, 384)):
        p = os.path.join(HERE_C, f"manifest_{o}.json")
        if not os.path.exists(p): continue
        rows = json.load(open(p)); n = len(rows); lab = 34; fo = ImageFont.truetype(FONTS["sb"][0], 15 if o == "h" else 12)
        sh = Image.new("RGB", (cols * (cw + 8) + 8, ((n + cols - 1) // cols) * (ch + lab + 8) + 8), INK); dd = ImageDraw.Draw(sh)
        for j, m in enumerate(rows):
            x, y = 8 + (j % cols) * (cw + 8), 8 + (j // cols) * (ch + lab + 8); sp = os.path.join(HERE_C, m["still"])
            if os.path.exists(sp): sh.paste(Image.open(sp).resize((cw, ch), Image.LANCZOS), (x, y))
            txt = m["key"] if o == "h" else m["name"]; dd.text((x + 2, y + ch + 8), txt, font=fo, fill=CREAM)
        sh.save(os.path.join(HERE_C, "contact_sheet.png" if o == "h" else "contact_sheet_vertical.png"))
def catalogue():
    rows = []
    for o in ("h", "v"):
        p = os.path.join(HERE_C, f"manifest_{o}.json")
        if os.path.exists(p): rows += json.load(open(p))
    head = open(os.path.join(HERE_C, "CATALOGUE_head.md")).read() if os.path.exists(os.path.join(HERE_C, "CATALOGUE_head.md")) else "# Figures Forward component catalogue\n"
    out = [head.rstrip(), "", "## Summary", "", "| Family | Variants | Fit check |", "|---|---|---|"]
    for fam, title in FAMILIES:
        rs = [r for r in rows if r["family"] == fam]
        if rs: out.append(f"| {title} | {len(rs)}: {', '.join(r['name'] for r in rs)} | {'all PASS' if all(r['fit'] == 'PASS' for r in rs) else 'SEE BELOW'} |")
    out += ["", f"Total: **{len(rows)} variants**. Contact sheets: `contact_sheet.png` (16:9) and `contact_sheet_vertical.png` (9:16).", ""]
    for fam, title in FAMILIES:
        rs = [r for r in rows if r["family"] == fam]
        if not rs: continue
        out += [f"## {title}", ""]
        for r in rs:
            sig = "a, b, p" if r["kind"] == "transition" else "base, d, lt, cam, ..."
            out += [f"### `{r['module']}.{r['func']}({sig})`", "", f"**When to use:** {r['use']}", ""]
            if r["notes"]: out += [r["notes"], ""]
            if r["params"]: out += ["| Parameter | Default (illustration only) |", "|---|---|"] + [f"| `{n}` | `{v}` |" for n, v in r["params"]] + [""]
            out += [f"Preview: `{r['preview']}` ({'transition ' + str(r['dur']) + ' s, shown between two demo scenes' if r['kind'] == 'transition' else str(r['dur']) + ' s'}) · Still: `{r['still']}` · Fit check: {r['fit']} ({r['samples']} samples)", ""]
    open(os.path.join(HERE_C, "CATALOGUE.md"), "w").write("\n".join(out) + "\n"); return len(rows)

MODULES = ["hooks", "transitions", "charts", "comparisons", "evidence", "reveals", "endcards"] if ORIENT == "h" else ["shorts"]
def main():
    import importlib
    for m in (os.environ["FF_MODULES"].split(",") if os.environ.get("FF_MODULES") else MODULES):
        if os.path.exists(os.path.join(HERE_C, m + ".py")): importlib.import_module(m)
    mode = (sys.argv[1:] or ["check"])[0]; flt = sys.argv[2] if len(sys.argv) > 2 else ""; keys = [k for k in REG if flt in k]
    if mode == "check":
        res = {k: fit_check(k) for k in keys}; manifest(res); ok = all(r[0] for r in res.values())
        print("ALL PASS" if ok else "FAILURES", len(res), "components"); sys.exit(0 if ok else 1)
    elif mode == "render":
        res = {}
        for k in keys:
            res[k] = fit_check(k)
            if not res[k][0]: print("  not rendered (fit check failed):", k); continue
            t0 = time.time(); render(k); print("rendered", k, round(time.time() - t0), "s")
        manifest(res)
    elif mode == "still":
        for k in keys: print(still(k))
    elif mode == "peek":                                   # python3 run.py peek <filter> t1 t2 ... -> /tmp/peek.jpg (2x2 sheet)
        ts = [float(a) for a in sys.argv[3:]] or [1, 2.5, 4, 4.8]; ims = [Image.fromarray(frame(keys[0], t)).resize((W // 2, H // 2), Image.LANCZOS) for t in ts[:4]]
        sh = Image.new("RGB", (W, H)); [sh.paste(im, ((j % 2) * (W // 2), (j // 2) * (H // 2))) for j, im in enumerate(ims)]
        pk = f"/tmp/peek_{fname(keys[0])}.jpg"; sh.resize((W * 2 // 3, H * 2 // 3) if ORIENT == "h" else (W, H)).save(pk, quality=80); print(pk, keys[0], ts[:4])
    elif mode == "sheet": manifest(); sheets()
    elif mode == "catalogue": manifest(); sheets(); print(catalogue(), "variants in CATALOGUE.md")
    elif mode == "time":
        t0 = time.time(); [frame(keys[0], t) for t in (1, 2, 3, 4)]; print("s/frame", (time.time() - t0) / 4)
