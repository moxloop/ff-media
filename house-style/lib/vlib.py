"""Figures Forward Episode 04 (first ~3 minutes), TEST 4: paper-collage explainer look.
Library: verified figures, word timing, paper textures, cut-out sprites, marker strokes, camera, fit check."""
import os, sys, subprocess, json, math, random, re
from functools import lru_cache
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1920, 1080, 30
S, BLEED = 1.25, 160                                   # canvas px per stage px; stage px of spare paper round the stage
CW, CH = int((W + 2 * BLEED) * S), int((H + 2 * BLEED) * S)
INK = (15, 18, 24); PAPER = (236, 228, 211); CARD = (251, 248, 240); KRAFT = (205, 176, 134)
ORANGE = (255, 138, 31); BLUE = (23, 138, 253); GREEN = (80, 200, 140)
MUTED = (96, 98, 104); LIGHT = (176, 180, 188); CREAM = (244, 238, 226)
HLC = {"o": (255, 188, 104), "b": (150, 202, 255), "g": (160, 228, 190)}
LEAD, HOLD, STING = 0.3, 0.7, 2.6

# ---------------- figures, computed and asserted (identical to the earlier build) ----------------
P, R = 200000, .05; I = R / 12
def pmt(Pr, r, n=300): i = r / 12; return Pr * i / (1 - (1 + i) ** -n)
PAY = round(pmt(P, R), 2)
def schedule(extra):
    b = P; rows = []
    while b > .005:
        it = b * I; cap = min(PAY + extra - it, b); rows.append((it, cap)); b -= cap
    return rows
BASE, X100 = schedule(0), schedule(100)
INT0, INT1 = sum(r[0] for r in BASE), sum(r[0] for r in X100)
SAVED = round(INT0 - INT1); END_A = len(X100); FREED = round(PAY + 100, 2)
LAST = sum(X100[-1]); LEFT = round(FREED - LAST, 2)
assert PAY == 1169.18 and len(BASE) in (300, 301) and SAVED == 24505 and END_A == 258 and FREED == 1269.18
assert 300 - END_A == 42 and 42 / 12 == 3.5 and LEFT == 1199.70
assert round(100 * R, 2) == 5.00
def pot_b(r, n=300, m=100): i = r / 12; return m * ((1 + i) ** n - 1) / i
def pot_a(r, leftover=True):
    i = r / 12; pot = LEFT if leftover else 0.0
    for _ in range(END_A + 1, 301): pot = pot * (1 + i) + FREED
    return pot
RATES = (.04, .05, .06, .07)
A = {r: round(pot_a(r)) for r in RATES}; B = {r: round(pot_b(r)) for r in RATES}
assert B == {.04: 51413, .05: 59551, .06: 69299, .07: 81007}
assert A == {.04: 58495, .05: 59551, .06: 60631, .07: 61737}
assert A[.05] == B[.05]
AHEAD4, AHEAD7 = A[.04] - B[.04], B[.07] - A[.07]
assert (AHEAD4, AHEAD7) == (7082, 19270) and round(AHEAD4, -3) == 7000 and round(AHEAD7, -3) == 19000
FEE_COST = B[.06] - B[.05]
assert FEE_COST == 9748 and round(FEE_COST, -2) == 9700 and 6 - 1 == 5
def gbp(x, d=0): return f"£{x:,.{d}f}"

# ---------------- scenes and word timing ----------------
KEYS = ["hook", "promise", "guaranteed", "investing", "fees", "seesaw", "setup"]
def _run(a): return subprocess.run(a, capture_output=True, text=True)
def _probe():
    p = os.path.join(HERE, "seg", "probe.json")
    if os.path.exists(p): return json.load(open(p))
    out = {}
    for i, k in enumerate(KEYS):
        f = os.path.join(HERE, "audio", f"{i+1:02d}.mp3")
        d = float(_run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).stdout)
        e = _run(["ffmpeg", "-hide_banner", "-i", f, "-af", "silencedetect=noise=-38dB:d=0.18", "-f", "null", "-"]).stderr
        st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", e)]; en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", e)]
        out[k] = dict(dur=d, sil=list(zip(st, en + [d] * (len(st) - len(en)))))
    os.makedirs(os.path.join(HERE, "seg"), exist_ok=True); json.dump(out, open(p, "w")); return out
PROBE = _probe()
AUD = {k: PROBE[k]["dur"] for k in KEYS}
SCRIPT = dict(l.strip().split("|", 1) for l in open(os.path.join(HERE, "script.txt")) if "|" in l)
def _norm(w): return re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))
def _align(k):
    """Word start times: speech runs (between detected pauses) are matched to runs of words, preferring punctuation breaks."""
    raw = SCRIPT[k].replace("-", " ").split()
    words = [(_norm(w), w[-1] in ".,:?") for w in raw if _norm(w)]
    d = AUD[k]; sil = [s for s in PROBE[k]["sil"] if s[1] - s[0] > .05]
    runs = []; t = 0.0
    for a, b in sil:
        if a - t > .12: runs.append((t, a))
        t = b
    if d - t > .12: runs.append((t, d))
    n, m = len(words), len(runs); ch = [len(w) + 1.5 for w, _ in words]; cum = [0]
    for c in ch: cum.append(cum[-1] + c)
    rate = sum(b - a for a, b in runs) / cum[-1]; INF = 1e18
    best = [[INF] * (n + 1) for _ in range(m + 1)]; back = [[0] * (n + 1) for _ in range(m + 1)]; best[0][0] = 0
    for j in range(1, m + 1):
        rd = runs[j - 1][1] - runs[j - 1][0]
        for e in range(j, n + 1):
            pen = 0 if (e == n or words[e - 1][1]) else .6
            for s0 in range(j - 1, e):
                if best[j - 1][s0] >= INF: continue
                c = best[j - 1][s0] + (rd - rate * (cum[e] - cum[s0])) ** 2 + pen
                if c < best[j][e]: best[j][e] = c; back[j][e] = s0
    times = [0.0] * n; e = n
    for j in range(m, 0, -1):
        s0 = back[j][e]; a, b = runs[j - 1]; tot = cum[e] - cum[s0]
        for i in range(s0, e): times[i] = a + (b - a) * (cum[i] - cum[s0]) / tot
        e = s0
    return [w for w, _ in words], times
ALIGN = {k: _align(k) for k in KEYS}
def Wt(k, phrase, nth=1):
    """Scene-local time at which `phrase` starts being spoken."""
    ws, ts = ALIGN[k]; ph = [_norm(w) for w in phrase.replace("-", " ").split()]; c = 0
    for i in range(len(ws) - len(ph) + 1):
        if ws[i:i + len(ph)] == ph:
            c += 1
            if c == nth: return LEAD + ts[i]
    raise KeyError(f"{k}: {phrase!r} not in script")

SC = []; _t = 0.0
for _k in KEYS:
    _d = LEAD + AUD[_k] + HOLD + (.8 if _k == KEYS[-1] else 0)
    SC.append(dict(k=_k, start=_t, dur=_d, speech=_t + LEAD)); _t += _d
    if _k == "hook": SC.append(dict(k="sting", start=_t, dur=STING, speech=None)); _t += STING
TOTAL = _t
BYKEY = {s["k"]: s for s in SC}

# ---------------- small helpers ----------------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def mix(c1, c2, a): a = clamp(a); return tuple(int(round(c1[i] + (c2[i] - c1[i]) * a)) for i in range(3))
def X(v): return (v + BLEED) * S
def pw(t, pts):
    """Piecewise eased interpolation through (time, value) points."""
    if t <= pts[0][0]: return pts[0][1]
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t <= t1: return v0 + (v1 - v0) * ease((t - t0) / max(1e-6, t1 - t0))
    return pts[-1][1]
FONTS = {"a": ("fonts/Anton-Regular.ttf", None), "o": ("fonts/Oswald.ttf", 600), "c": ("fonts/Caveat.ttf", 700),
         "b": ("/usr/share/fonts/opentype/inter/Inter-Bold.otf", None), "sb": ("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", None),
         "r": ("/usr/share/fonts/opentype/inter/Inter-Regular.otf", None), "xb": ("/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", None)}
@lru_cache(maxsize=None)
def font(f, px):
    p, wght = FONTS[f]; fo = ImageFont.truetype(p if p.startswith("/") else os.path.join(HERE, p), px)
    if wght: fo.set_variation_by_axes([wght])
    return fo
def F(f, size): return font(f, int(round(size * S)))
def tw(s, size, f): return F(f, size).getlength(s) / S

FIT = None            # when a list: every card, text, picture and chart box drawn is recorded (stage coordinates)
COLLECT = None        # when a list: every entrance records (time, sound, length)
def appear(lt, t0, d=0.4, sfx="pop"):
    if COLLECT is not None and sfx: COLLECT.append((t0, sfx, d))
    return ease((lt - t0) / d)
def _rec(kind, box, name=""):
    if FIT is not None: FIT.append((kind, tuple(box), name))
def _unS(b): return (b[0] / S - BLEED, b[1] / S - BLEED, b[2] / S - BLEED, b[3] / S - BLEED)

def T(d, x, y, s, size, f="b", fill=INK, anchor="la", a=1.0, on=PAPER, dy=0.0):
    if a <= .03 or not s: return
    fo = F(f, size); xy = (X(x), X(y + dy))
    d.text(xy, s, font=fo, fill=mix(on, fill, a), anchor=anchor)
    if s.strip(): _rec("t", _unS(d.textbbox(xy, s, font=fo, anchor=anchor)), s)
def wrap(s, size, f, maxw):
    out, cur = [], ""
    for word in s.split():
        t2 = (cur + " " + word).strip()
        if tw(t2, size, f) <= maxw: cur = t2
        else: out.append(cur); cur = word
    if cur: out.append(cur)
    return out
def hl(d, x0, y0, x1, y1, col, p):
    """A highlighter-marker swipe across a stage box, drawn left to right."""
    if p <= .01: return
    xe = x0 - 10 + (x1 - x0 + 22) * p
    d.polygon([(X(x0 - 10), X(y0 + 3)), (X(xe), X(y0 - 2)), (X(xe + 7), X(y1 - 3)), (X(x0 - 5), X(y1 + 3))], fill=col)
def kline(d, lt, x, y, parts, size, f="a", align="l", on=PAPER, step=.07):
    """Kinetic line: each word drops in at its cue. parts: (text, t0, fill, highlight key or None). Returns part boxes."""
    fo = F(f, size); sp = fo.getlength(" ") / S; items = []; cx = 0.0
    for pi, (text, t0, fill, hk) in enumerate(parts):
        for j, wd in enumerate(text.split()):
            wl = fo.getlength(wd) / S; items.append((pi, wd, cx, wl, t0 + j * step, fill)); cx += wl + sp
    total = cx - sp; x0 = x - (total if align == "r" else total / 2 if align == "m" else 0)
    bb = fo.getbbox("H0"); top, bot = bb[1] / S, bb[3] / S; boxes = []
    for pi, (text, t0, fill, hk) in enumerate(parts):
        its = [it for it in items if it[0] == pi]
        bx = (x0 + its[0][2], y + top, x0 + its[-1][2] + its[-1][3], y + bot); boxes.append(bx)
        if hk:
            ph = appear(lt, t0 + .12 + step * len(its) * .5, .4, "marker")
            hl(d, bx[0], bx[1] + (bot - top) * .06, bx[2], bx[3] + (bot - top) * .1, mix(on, HLC[hk], .95), ph)
    for pi, wd, wx, wl, t0, fill in items:
        p = clamp((lt - t0) / .24)
        if p <= 0: continue
        T(d, x0 + wx, y, wd, size, f, fill, "la", min(1, p * 2.2), on, dy=-24 * (1 - back(p)))
    return boxes

# ---------------- marker strokes ----------------
@lru_cache(maxsize=None)
def _dense(pts, seed, jit):
    r = random.Random(seed); out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 9))
        for i in range(n): u = i / n; out.append((x0 + (x1 - x0) * u + r.uniform(-jit, jit), y0 + (y1 - y0) * u + r.uniform(-jit, jit)))
    out.append(pts[-1]); return out
def stroke(d, pts, p, col=INK, w=5, seed=1, jit=1.3):
    """Hand-drawn line through stage points, drawn on up to fraction p."""
    if p <= .01: return None
    dn = _dense(tuple(pts), seed, jit); n = max(2, int(len(dn) * clamp(p))); seg = [(X(a), X(b)) for a, b in dn[:n]]
    wp = max(2, int(w * S)); d.line(seg, fill=col, width=wp, joint="curve")
    for q in (seg[0], seg[-1]): d.ellipse([q[0] - wp / 2, q[1] - wp / 2, q[0] + wp / 2, q[1] + wp / 2], fill=col)
    return dn[:n]
def ring(d, box, p, col=INK, w=5, seed=3):
    x0, y0, x1, y1 = box; cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2; pts = []
    for i in range(41):
        a = math.radians(-115 + 395 * i / 40); k = 1 + .05 * i / 40
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    stroke(d, pts, p, col, w, seed, 1.0)
def arrow(d, p0, p1, p, col=INK, w=5, bend=.2, seed=5):
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2; dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    c = (mx - dy * bend, my + dx * bend); pts = []
    for i in range(13):
        u = i / 12; pts.append(((1 - u) ** 2 * p0[0] + 2 * u * (1 - u) * c[0] + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * u * (1 - u) * c[1] + u * u * p1[1]))
    stroke(d, pts, clamp(p / .8), col, w, seed, .8)
    if p > .8:
        a = math.atan2(p1[1] - pts[-3][1], p1[0] - pts[-3][0]); L = 22 * clamp((p - .8) / .2)
        for s_ in (-1, 1):
            stroke(d, [p1, (p1[0] - L * math.cos(a + s_ * .5), p1[1] - L * math.sin(a + s_ * .5))], 1, col, w, seed + 1, .3)
def underline(d, x0, x1, y, p, col=ORANGE, w=5, seed=7):
    stroke(d, [(x0, y + 2), ((x0 + x1) / 2, y - 2), (x1, y + 1)], p, col, w, seed, 1.2)

# ---------------- paper textures and sprites ----------------
TW_, TH_ = 3200, 2000
def _tile():
    p = os.path.join(HERE, "seg", "paper.npy")
    if os.path.exists(p): return np.load(p)
    rng = np.random.default_rng(4)
    def nz(sig, amp):
        pd = int(sig * 3) + 2; n = np.pad(rng.standard_normal((TH_, TW_)).astype(np.float32), pd, mode="wrap"); n = cv2.GaussianBlur(n, (0, 0), sig)[pd:-pd, pd:-pd]
        return n / n.std() * amp
    g = nz(90, 3.2) + nz(14, 1.6) + nz(1.1, 2.6)
    fib = Image.new("L", (TW_, TH_), 128); fd = ImageDraw.Draw(fib); r = random.Random(9)
    for _ in range(5200):
        x, y = r.uniform(0, TW_), r.uniform(0, TH_); a = r.uniform(0, math.pi); L = r.uniform(14, 60); c = r.choice((104, 112, 146, 152))
        mx, my = x + L / 2 * math.cos(a) + r.uniform(-6, 6), y + L / 2 * math.sin(a) + r.uniform(-6, 6)
        fd.line([(x, y), (mx, my), (x + L * math.cos(a), y + L * math.sin(a))], fill=c, width=1)
    g += (np.asarray(fib.filter(ImageFilter.GaussianBlur(.8)), np.float32) - 128) * .42
    t = np.clip(np.array(PAPER, np.float32)[None, None, :] + g[:, :, None] * np.array([1, 1, 1.15], np.float32), 0, 255).astype(np.uint8)
    np.save(p, t); return t
_TILE = None; _NOISE = None
def tile2():
    global _TILE, _NOISE
    if _TILE is None:
        t = _tile(); _TILE = np.tile(t, (2, 2, 1)); _NOISE = t[:, :, 0].astype(np.int16) - PAPER[0]
    return _TILE
def grain(w, h, seed=0):
    tile2(); r = random.Random(seed); ox, oy = r.randrange(0, TW_ - w - 1), r.randrange(0, TH_ - h - 1)
    return _NOISE[oy:oy + h, ox:ox + w]
@lru_cache(maxsize=4)
def navy_sheet():
    g = grain(CW, CH, 5).astype(np.float32) * .55
    return Image.fromarray(np.clip(np.array(INK, np.float32)[None, None, :] + 4 + g[:, :, None], 0, 255).astype(np.uint8))

def _paper_from_mask(mask, fill, seed=0, shadow=.38, off=(5, 8), blur=7):
    """RGBA sprite: a grained paper shape with a soft drop shadow, from an L mask (already padded)."""
    w, h = mask.size; g = grain(w, h, seed).astype(np.float32) * .7
    rgb = np.clip(np.array(fill, np.float32)[None, None, :] + g[:, :, None], 0, 255).astype(np.uint8)
    top = Image.fromarray(rgb).convert("RGBA"); top.putalpha(mask)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("L", (w, h), 0); sh.paste(mask, off); sh = sh.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * shadow))
        out = Image.merge("RGBA", (Image.new("L", (w, h), 8), Image.new("L", (w, h), 10), Image.new("L", (w, h), 16), sh))
    out.alpha_composite(top); return out
PAD = 26
def _wob_mask(w, h, seed, jit=2.2, circle=False):
    r = random.Random(seed); k = 2; m = Image.new("L", ((w + 2 * PAD) * k, (h + 2 * PAD) * k), 0); d = ImageDraw.Draw(m); pts = []
    if circle:
        for i in range(48):
            a = 2 * math.pi * i / 48; rr = 1 + r.uniform(-.012, .012); pts.append(((PAD + w / 2 + w / 2 * rr * math.cos(a)) * k, (PAD + h / 2 + h / 2 * rr * math.sin(a)) * k))
    else:
        cs = [(0, 0), (w, 0), (w, h), (0, h)]
        for (x0, y0), (x1, y1) in zip(cs, cs[1:] + cs[:1]):
            n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 140))
            for i in range(n): u = i / n; pts.append(((PAD + x0 + (x1 - x0) * u + r.uniform(-jit, jit)) * k, (PAD + y0 + (y1 - y0) * u + r.uniform(-jit, jit)) * k))
    d.polygon(pts, fill=255); return m.resize((w + 2 * PAD, h + 2 * PAD), Image.LANCZOS)
@lru_cache(maxsize=256)
def panel_sprite(w, h, fill, seed=0, circle=False, shadow=.38):
    return _paper_from_mask(_wob_mask(w, h, seed, circle=circle), fill, seed, shadow)
def paste(base, im, x, y, a=1.0):
    if a <= .01: return
    if a < 1: im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    base.paste(im, (int(round(x)), int(round(y))), im)
def panel(base, lt, box, t0, fill=CARD, sfx="slide", seed=0, frm=(0, 46), kind="c", d_=.4):
    """Paper card (stage box) that slides in and settles."""
    a = appear(lt, t0, d_, sfx)
    if a <= .02: return 0.0
    w, h = int((box[2] - box[0]) * S), int((box[3] - box[1]) * S); e = back(clamp((lt - t0) / d_))
    paste(base, panel_sprite(w, h, fill, seed), X(box[0]) - PAD + frm[0] * S * (1 - e), X(box[1]) - PAD + frm[1] * S * (1 - e), min(1, a * 1.6))
    _rec(kind, box); return a
def strip(base, lt, box, t0, fill, d_=1.0, seed=0, sfx="slide", rec=True):
    """Paper strip that unrolls from its left end."""
    p = appear(lt, t0, d_, sfx)
    if p <= .01: return 0.0
    w, h = int((box[2] - box[0]) * S), int((box[3] - box[1]) * S); sp = panel_sprite(w, h, fill, seed)
    cw = int(PAD + w * p + (PAD if p >= .999 else 0)); paste(base, sp.crop((0, 0, max(2, cw), sp.size[1])), X(box[0]) - PAD, X(box[1]) - PAD)
    if rec and p >= .999: _rec("c", box)
    return p

def _rot_bounds(w, h, deg):
    a = math.radians(abs(deg)); return (w * math.cos(a) + h * math.sin(a), w * math.sin(a) + h * math.cos(a))
@lru_cache(maxsize=160)
def tag_sprite(lines, fill, fg, rot, padx, pady):
    """Rotated paper label with its text baked in. lines: ((text, size, font), ...). Returns sprite, card size, text size (canvas px)."""
    ms = []
    for text, size, f in lines:
        fo = F(f, size); cap = fo.getbbox("H0"); ms.append((fo, fo.getlength(text), cap[3] - cap[1]))
    gap = int(.34 * sum(m[2] for m in ms) / len(ms)); tw_ = int(max(m[1] for m in ms)); th_ = int(sum(m[2] for m in ms) + gap * (len(ms) - 1))
    w, h = tw_ + int(2 * padx * S), th_ + int(2 * pady * S)
    sp = panel_sprite(w, h, fill, hash((lines, fill)) % 997).copy(); d = ImageDraw.Draw(sp); y = PAD + pady * S
    for (text, size, f), (fo, _, capn) in zip(lines, ms):
        d.text((PAD + w / 2, y + capn), text, font=fo, fill=fg, anchor="ms"); y += capn + gap
    if rot: sp = sp.rotate(rot, Image.BICUBIC, expand=True)
    return sp, (w, h), (tw_, th_)
def tag(base, lt, cx, cy, text, size, t0, fill=CARD, fg=INK, rot=0.0, f="o", sfx="pop", pad=(22, 15), t1=None, d_=.42):
    appear(lt, t0, d_, sfx)
    if lt < t0: return False
    lines = ((text, size, f),) if isinstance(text, str) else tuple(text); rot = round(rot * 4) / 4
    sp, (w, h), (tw_, th_) = tag_sprite(lines, fill, fg, rot, pad[0], pad[1])
    e = back((lt - t0) / d_)
    if t1 is not None and lt > t1: e *= 1 - ease((lt - t1) / .25)
    if e <= .05: return False
    if abs(e - 1) > .004: sp = sp.resize((max(2, int(sp.size[0] * e)), max(2, int(sp.size[1] * e))), Image.BILINEAR)
    base.paste(sp, (int(X(cx) - sp.size[0] / 2), int(X(cy) - sp.size[1] / 2)), sp)
    bw, bh = _rot_bounds(w / S, h / S, rot); _rec("c", (cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2))
    bw, bh = _rot_bounds(tw_ / S, th_ / S, rot); _rec("t", (cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), lines[-1][0])
    return True

@lru_cache(maxsize=None)
def _asset(name): return Image.open(os.path.join(HERE, "assets", name + ".png")).convert("RGBA")
def duotone(im):
    """Glossy icon -> navy-and-cream halftone print, so every picture reads as a cut-out from the same magazine."""
    a = np.asarray(im, np.float32); g = (a[:, :, 0] * .299 + a[:, :, 1] * .587 + a[:, :, 2] * .114) / 255
    g = np.clip((g - .5) * 1.6 + .43, 0, 1); h, w = g.shape; yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); cell = 6.0
    pat = .5 + .5 * np.cos(2 * math.pi * (xx + yy) / (cell * 1.414)) * np.cos(2 * math.pi * (xx - yy) / (cell * 1.414))
    hv = np.clip((g * 1.5 - pat * .9) * 2.2 + .35, 0, 1); og = .62 * g + .38 * hv
    lo = np.array((24, 30, 46), np.float32); hi = np.array(CREAM, np.float32)
    rgb = lo[None, None, :] + (hi - lo)[None, None, :] * og[:, :, None]
    out = np.dstack([rgb, a[:, :, 3]]).astype(np.uint8); return Image.fromarray(out, "RGBA")
DISC = {"o": (255, 158, 66), "b": (84, 166, 255), "k": KRAFT, "g": (120, 214, 168), "n": INK, "w": CARD}
@lru_cache(maxsize=128)
def cut_sprite(name, size, rot, duo, disc, flip=False):
    """Cut-out sticker: picture, white paper border, drop shadow, optional coloured paper disc behind, slight rotation.
    Returns the sprite and the opaque bbox relative to its centre (stage px)."""
    im = _asset(name); im = im.crop(im.getbbox()); k = size * S / max(im.size)
    im = im.resize((max(2, int(im.size[0] * k)), max(2, int(im.size[1] * k))), Image.LANCZOS)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if duo: im = duotone(im)
    bw = int(6 * S); m = 30 + bw; w, h = im.size[0] + 2 * m, im.size[1] + 2 * m
    al = Image.new("L", (w, h), 0); al.paste(im.getchannel("A"), (m, m))
    edge = al.filter(ImageFilter.MaxFilter(2 * bw + 1)).filter(ImageFilter.GaussianBlur(1.6)).point(lambda v: 255 if v > 150 else int(v * 1.7))
    sp = _paper_from_mask(edge, CARD, 3, .42, (6, 9), 8); pic = Image.new("RGBA", (w, h), (0, 0, 0, 0)); pic.paste(im, (m, m)); sp.alpha_composite(pic)
    if disc:
        col, r = disc; D = int(2 * r * S); ds = panel_sprite(D, D, DISC[col], 11, True)
        W2, H2 = max(w, ds.size[0]), max(h, ds.size[1]); out = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
        out.alpha_composite(ds, ((W2 - ds.size[0]) // 2, (H2 - ds.size[1]) // 2)); out.alpha_composite(sp, ((W2 - w) // 2, (H2 - h) // 2)); sp = out
    if rot: sp = sp.rotate(rot, Image.BICUBIC, expand=True)
    bb = sp.getchannel("A").point(lambda v: 255 if v > 200 else 0).getbbox(); cx, cy = sp.size[0] / 2, sp.size[1] / 2
    return sp, ((bb[0] - cx) / S, (bb[1] - cy) / S, (bb[2] - cx) / S, (bb[3] - cy) / S)
def cut(base, lt, name, cx, cy, size, t0, rot=0.0, duo=True, disc=None, sfx="pop", t1=None, flip=False, extra=None):
    appear(lt, t0, .5, sfx)
    if lt < t0 or (t1 is not None and lt > t1 + .25): return False
    sp, bb = cut_sprite(name, size, rot, duo, disc, flip); x = clamp((lt - t0) / .5); e = back(x)
    if t1 is not None and lt > t1: e *= 1 - ease((lt - t1) / .25)
    if e <= .05: return False
    if x < 1: sp = sp.rotate((1 - x) * 14, Image.BILINEAR, expand=False)
    if abs(e - 1) > .004: sp = sp.resize((max(2, int(sp.size[0] * e)), max(2, int(sp.size[1] * e))), Image.BILINEAR)
    base.paste(sp, (int(X(cx) - sp.size[0] / 2), int(X(cy) - sp.size[1] / 2)), sp)
    b = [cx + bb[0], cy + bb[1], cx + bb[2], cy + bb[3]]
    if extra: b = [min(b[0], extra[0]), min(b[1], extra[1]), max(b[2], extra[2]), max(b[3], extra[3])]
    _rec("i", b, name); return True
def count(v, lt, t0, d=1.0):
    appear(lt, t0, d, "ticks"); return v * ease((lt - t0) / d)

@lru_cache(maxsize=16)
def deco_sprite(kind):
    if kind == "dots":
        n = 420; im = Image.new("RGBA", (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        for y in range(8, n, 22):
            for x in range(8, n, 22): d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=INK + (30,))
        return im
    col = {"blobO": ORANGE, "blobB": BLUE, "blobK": (170, 136, 92), "blobG": GREEN}[kind]; n = 760
    m = _wob_mask(n - 2 * PAD, n - 2 * PAD, 21, circle=True).point(lambda v: int(v * .16))
    im = Image.new("RGBA", (n, n), col + (0,)); im.putalpha(m); return im
def deco(base, cam, kind, x, y, par=.25):
    sp = deco_sprite(kind); base.paste(sp, (int(X(x + (cam[0] - 960) * par) - sp.size[0] / 2), int(X(y + (cam[1] - 540) * par) - sp.size[1] / 2)), sp)
