"""Figures Forward Ep04 opening, TEST 5c: the first 52.96 s (hook, sting, roadmap) in the 5b collage style,
plus kinetic morphs, drawn charts, parallax cut-outs, a zoomed calculation sheet, acting £100 tokens and synced sfx.
python3 build.py preview t.. | check | render | mix | sheet | cues"""
import os, sys, types, json, math, subprocess, time
from functools import lru_cache
sys.dont_write_bytecode = True
B = os.path.dirname(os.path.abspath(__file__)); SRC = "/home/claude/v5c/src"; OUTD = "/home/claude/v5c"
LIB = os.path.join(B, "lib"); SEG = os.path.join(B, "seg"); MIX = os.path.join(SRC, "mix")
os.makedirs(SEG, exist_ok=True); sys.path.insert(0, LIB)
sys.modules["vscenes"] = types.SimpleNamespace(SCENES={}, CAMS={}, _wordmark=None)
import vlib, render_vox as RV
from vlib import (W, H, FPS, S, INK, PAPER, CARD, KRAFT, ORANGE, BLUE, GREEN, MUTED, LIGHT, CREAM, HLC, LEAD, clamp, ease, eout, back,
                  mix, X, pw, F, tw, T, hl, kline, stroke, ring, arrow, underline, panel, strip, cut, tag, count, appear, panel_sprite,
                  navy_sheet, deco, gbp, PAD, wrap, paste)
from PIL import Image
import numpy as np

KEYS = ["hook", "roadmap", "guaranteed", "expected", "fees", "setup"]
def probe():
    p = os.path.join(SEG, "probe.json")
    if os.path.exists(p): return json.load(open(p))
    import re; out = {}
    for i, k in enumerate(KEYS):
        f = os.path.join(MIX, "audio", f"{i+1:02d}.mp3")
        d = float(vlib._run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).stdout)
        e = vlib._run(["ffmpeg", "-hide_banner", "-i", f, "-af", "silencedetect=noise=-38dB:d=0.18", "-f", "null", "-"]).stderr
        st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", e)]; en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", e)]
        out[k] = dict(dur=d, sil=list(zip(st, en + [d] * (len(st) - len(en)))))
    json.dump(out, open(p, "w")); return out
vlib.KEYS = KEYS; vlib.PROBE = probe(); AUD = vlib.AUD = {k: vlib.PROBE[k]["dur"] for k in KEYS}
vlib.SCRIPT = dict(l.strip().split("|", 1) for l in open(os.path.join(MIX, "script.txt")) if "|" in l)
vlib.ALIGN = {k: vlib._align(k) for k in KEYS}
TL = json.load(open(os.path.join(MIX, "timeline.json")))
ORDER = ["hook", "sting", "roadmap", "guaranteed", "expected", "fees", "setup"]; TOTAL = TL["TOTAL"]; SC = []
for j, k in enumerate(ORDER):
    st = TL[k]; en = TL[ORDER[j + 1]] if j + 1 < len(ORDER) else TOTAL
    SC.append(dict(k=k, start=st, dur=en - st, speech=None if k == "sting" else st + LEAD))
    if k != "sting": assert abs(en - st - (LEAD + AUD[k] + 1.2)) < .02, k
assert (TL["hook"], TL["sting"], TL["roadmap"], TL["guaranteed"], TL["expected"], TL["fees"], TL["setup"], TOTAL) == (0.0, 24.1, 26.7, 52.96, 87.3, 117.16, 152.7, 190.8)
BYKEY = {s["k"]: s for s in SC}

# ---------------- figures (asserted against figures_check.py values) ----------------
A4, B4, A6, B6 = vlib.A[.04], vlib.B[.04], vlib.A[.06], vlib.B[.06]
assert (A6, B6, A4, B4) == (60631, 69299, 58495, 51413) and B6 - A6 == 8668 and A4 - B4 == 7082
assert vlib.PAY == 1169.18 and vlib.END_A == 258 and 300 - vlib.END_A == 42 and vlib.P == 200000
def balances(rows):
    b, out = float(vlib.P), [float(vlib.P)]
    for it, cap in rows: b -= cap; out.append(max(0.0, b))
    return out
BAL0, BAL1 = balances(vlib.BASE), balances(vlib.X100)
assert len(BAL1) - 1 == 258 and len(BAL0) - 1 in (300, 301)

# ---------------- helpers ----------------
BROWN = (88, 66, 36); DGREEN = (40, 150, 100)
def fa(lt, t0, d=.3): return ease((lt - t0) / d)
def fx(lt, t1, d=.3): return 1 - ease((lt - t1) / d)               # exit factor
def C(k): return lambda ph, n=1: vlib.Wt(k, ph, n)
def note(d, lt, x, y, s, size, t0, fill=INK, on=PAPER, anchor="la", f="c", t1=None):
    a = ease((lt - t0) / .3) * (fx(lt, t1) if t1 else 1)
    T(d, x, y, s, size, f, fill, anchor, a, on, dy=10 * (1 - eout((lt - t0) / .3)))
def _rec(kind, b):
    if vlib.FIT is not None: vlib.FIT.append((kind, tuple(b), ""))
def chime(lt, t0): appear(lt, t0, .4, "chime")
def par(cam, x, y, k=.07, lt=0, seed=0):
    """Foreground parallax (moves against the camera) plus a slow paper float."""
    return x - (cam[0] - 960) * k, y - (cam[1] - 540) * k + 4 * math.sin(2 * math.pi * lt / 3.2 + seed)
@lru_cache(maxsize=512)
def _plank(q, length): return panel_sprite(int(length * S), int(22 * S), INK, 2).rotate(-q / 20, Image.BICUBIC, expand=True)
def morph(d, lt, x, y, seq, size, f="a", anchor="mm", on=PAPER, dur=.35, sfx="click", grow=.12):
    """Kinetic text that re-forms: each entry (t0, text, colour) scales in while the previous one swells and fades."""
    for i, (t0, _, _) in enumerate(seq):
        if i: appear(lt, t0, dur, sfx)
    cur = None
    for i, (t0, _, _) in enumerate(seq):
        if lt >= t0: cur = i
    if cur is None: return
    t0, s, col = seq[cur]; u = clamp((lt - t0) / dur)
    if cur and u < 1: _, ps, pcol = seq[cur - 1]; T(d, x, y, ps, size * (1 + grow * u), f, pcol, anchor, 1 - u * 1.4, on)
    T(d, x, y, s, size * (.55 + .45 * back(u)), f, col, anchor, min(1, u * 1.8), on)
def vmorph(d, lt, x, y, keys, size, on=CARD, dur=.8, f="a", anchor="rm"):
    """A figure that counts and re-forms into the next figure: keys = [(t0, value, colour)]; first value is the start."""
    for t0, _, _ in keys[1:]: appear(lt, t0, dur, "ticks")
    if lt < keys[0][0]: return
    v, col, pulse = keys[0][1], keys[0][2], 0.0
    for (t0, v1, c1) in keys[1:]:
        if lt >= t0: u = clamp((lt - t0) / dur); v = v + (v1 - v) * ease(u); col = c1; pulse = math.sin(math.pi * u) * .14
    sc = (.6 + .4 * back((lt - keys[0][0]) / .35)) * (1 + pulse)
    T(d, x, y, gbp(round(v)), size * sc, f, col, anchor, min(1, (lt - keys[0][0]) / .2), on)
def token(base, lt, p0, p1, t_on, t_go, text, fill, fg, rot, t1=None, sfx="swish"):
    """A £100 paper token that pops on at p0 and slides to p1."""
    appear(lt, t_go, .5, sfx)
    u = eout((lt - t_go) / .55); x = p0[0] + (p1[0] - p0[0]) * u; y = p0[1] + (p1[1] - p0[1]) * u - 40 * math.sin(math.pi * u)
    tag(base, lt, x, y, text, 52, t_on, fill, fg, rot * (1 - u) + 2 * u * (1 if rot >= 0 else -1), "a", "pop", (18, 10), t1)

# ================= 1 hook =================
SX0, SY0, SX1, SY1 = 110, 280, 1010, 930                           # the calculation sheet
def s_hook(base, d, lt, L, cam):
    c = C("hook")
    t_got, t_sp, t_mo, t_mort, t_inv, t_over = c("you've got"), c("a spare hundred"), c("pounds a month"), c("on the mortgage"), c("into investments"), c("over twenty five")
    t_if, t_six, t_87, t_4, t_win, t_7k, t_see, t_one, t_know = c("if investing returns"), c("six per cent"), c("about eight thousand"), c("at four per cent"), c("overpaying wins"), c("by about seven"), c("it's a see saw"), c("one number decides"), c("you already know")
    deco(base, cam, "blobO", 330, 560, .3); deco(base, cam, "blobB", 1600, 560, .3); deco(base, cam, "dots", 1720, 930, .15); deco(base, cam, "dots", 170, 200, .15)
    # --- A: £100 slides on, between a hand and a pile of coins (parallax cut-outs) ---
    hx, hy = par(cam, 470, 500, .08, lt, 1); cut(base, lt, "hand", hx, hy, 240, t_got + .1, rot=-4, t1=t_mort - .1, sfx="pop")
    kx, ky = par(cam, 1450, 520, .08, lt, 2); cut(base, lt, "coins", kx, ky, 200, t_sp + .9, rot=5, disc=("o", 118), t1=t_mort - .1)
    ex = fx(lt, t_mort, .3)
    T(d, 960, 290, "YOU'VE GOT A SPARE", 64, "a", INK, "mm", fa(lt, t_got, .25) * ex, dy=-20 * (1 - back((lt - t_got) / .3)))
    appear(lt, t_sp + .2, .45, "slide"); appear(lt, t_sp + .6, .2, "thud")
    u = clamp((lt - t_sp - .2) / .45); sc = 1 - .45 * ease((lt - t_mort) / .25)
    T(d, 960 + 300 * (1 - back(u)), 470, "£100", 230 * sc, "a", ORANGE, "mm", min(1, u * 2) * fx(lt, t_mort, .25))
    T(d, 960, 650, "A MONTH", 60, "o", INK, "mm", fa(lt, t_mo, .25) * ex, dy=16 * (1 - eout((lt - t_mo) / .3)))
    # --- B: the £100 splits into the two choices ---
    cut(base, lt, "house", 330, 600, 200, t_mort, rot=-5, disc=("o", 120), t1=t_over - .15)
    cut(base, lt, "chart", 1590, 600, 190, t_inv, rot=4, disc=("b", 115), t1=t_over - .15)
    tag(base, lt, 330, 380, "THE MORTGAGE?", 44, t_mort + .3, ORANGE, INK, -3, t1=t_over - .15)
    tag(base, lt, 1590, 380, "OR INVESTMENTS?", 44, t_inv + .3, BLUE, CARD, 3, t1=t_over - .15)
    t_tok = t_mort + .26; R1, R2, RV_ = 530, 610, 745
    for t0 in (t_mort + .4, t_inv, t_over): appear(lt, t0, .5, "swish")
    token(base, lt, (960, 470), (640, 600), t_tok, t_mort + .4, "£100", ORANGE, INK, -4, None, None) if lt < t_over else None
    token(base, lt, (960, 470), (1280, 600), t_tok, t_inv, "£100", BLUE, CARD, 4, None, None) if lt < t_over else None
    # --- C: tokens fly onto the calculation sheet and re-form into the 25-year pots ---
    t_fin = t_six + .1
    if lt >= t_over:
        token(base, lt, (1280, 600), (880, R1), t_tok, t_over, "£100", BLUE, CARD, 2, t_fin, None)
        token(base, lt, (640, 600), (880, R2), t_tok, t_over + .08, "£100", ORANGE, INK, -2, t_fin, None)
    t_sh = t_over + .7; a = panel(base, lt, (SX0, SY0, SX1, SY1), t_sh, CARD, seed=21, frm=(-70, 0))
    if a > .02:
        for yy in range(400, 900, 60): d.line([X(SX0 + 20), X(yy), X(SX1 - 20), X(yy)], fill=mix(CARD, (200, 220, 240), a * .7), width=2)
        d.line([X(140), X(SY0 + 12), X(140), X(SY1 - 12)], fill=mix(CARD, (255, 190, 170), a), width=2)
        T(d, 150, 300, "FIGURES FORWARD CALCULATION", 28, "o", MUTED, a=fa(lt, t_sh + .2), on=CARD)
        T(d, 970, 296, "worked example", 36, "c", ORANGE, "ra", fa(lt, t_sh + .35), CARD)
        T(d, 150, 352, "£100 a month for 25 years (300 months): pots at the end", 26, "sb", INK, a=fa(lt, t_sh + .45), on=CARD)
    if a > .02:
        morph(d, lt, 150, 440, [(t_if, "If investing returns 6% after fees", BLUE), (t_4, "If it returns 4% a year instead", ORANGE)], 46, "c", "lm", CARD)
        T(d, 150, R1, "Invest £100 every month", 30, "sb", INK, "lm", fa(lt, t_if + .4), CARD)
        T(d, 150, R2, "Overpay first, then invest", 30, "sb", INK, "lm", fa(lt, t_if + .6), CARD)
        vmorph(d, lt, 970, R1, [(t_fin + .27, 100, BLUE), (t_fin + .3, B6, BLUE), (t_4 + .3, B4, BLUE)], 60)
        vmorph(d, lt, 970, R2, [(t_fin + .27, 100, ORANGE), (t_fin + .4, A6, ORANGE), (t_4 + .45, A4, ORANGE)], 60)
        stroke(d, [(150, 668), (560, 664), (970, 667)], appear(lt, t_87 - .45, .35, "marker"), INK, 4, 9, .8)
        # the number that matters: highlighter swipe as it is spoken
        ref = gbp(B6 - A6); x0 = 970 - tw(ref, 96, "a"); fo = F("a", 96); bb = fo.getbbox("H0"); hh = (bb[3] - bb[1]) / S
        hb = appear(lt, t_87 + .9, .45, "marker") * fx(lt, t_4, .2); ho = appear(lt, t_7k + .9, .45, "marker")
        if hb > .01: hl(d, x0, RV_ - hh / 2 - 6, 970, RV_ + hh / 2 + 10, mix(CARD, HLC["b"], .95), hb)
        if ho > .01: hl(d, x0, RV_ - hh / 2 - 6, 970, RV_ + hh / 2 + 10, mix(CARD, HLC["o"], .95), ho)
        morph(d, lt, 150, RV_, [(t_87, "Investing ends ahead by", BLUE), (t_win, "Overpaying ends ahead by", ORANGE)], 48, "c", "lm", CARD)
        vmorph(d, lt, 970, RV_, [(t_87, 0, BLUE), (t_87 + .05, B6 - A6, BLUE), (t_7k, A4 - B4, ORANGE)], 96)
        T(d, 150, 870, "Pot values after 25 years · same money out every month", 24, "r", MUTED, "lm", fa(lt, t_87 + 1.2), CARD)
    # --- D: the see-saw on the right; one number decides ---
    px, py = 1460, 600
    deg = pw(lt, [(t_see, 0), (t_see + .5, 7), (t_see + 1.0, 7), (t_see + 1.6, -7), (t_one, -7), (t_one + .7, 0)])
    if lt > t_one + .7: deg += 2.2 * math.sin(2 * math.pi * (lt - t_one - .7) / 2.4) * clamp((lt - t_one - .7) / .6)
    for t0 in (t_see, t_see + 1.0, t_one): appear(lt, t0, .6, "slide")
    th = math.radians(deg); s_ = fa(lt, t_see + .1, .5)
    if s_ > .02:
        paste(base, panel_sprite(int(150 * S), int(80 * S), KRAFT, 4), X(px - 75) - PAD, X(py + 14) - PAD, s_)
        d.polygon([(X(px), X(py + 16)), (X(px + 46), X(py + 96)), (X(px - 46), X(py + 96))], fill=mix(KRAFT, INK, s_))
        pl = _plank(int(round(deg * 20)), 640); paste(base, pl, X(px) - pl.size[0] / 2, X(py) - pl.size[1] / 2 + 20 * (1 - s_) * S, s_)
    def on_plank(a_, off): return (px + a_ * math.cos(th) + off * math.sin(th), py + a_ * math.sin(th) - off * math.cos(th))
    (hx2, hy2), (cx2, cy2) = on_plank(-250, 82), on_plank(250, 82)
    cut(base, lt, "house", hx2, hy2, 118, t_see + .65, rot=-5, disc=("o", 70), sfx="thud")
    cut(base, lt, "chart", cx2, cy2, 112, t_see + .8, rot=4, disc=("b", 68), sfx="thud")
    morph(d, lt, px, 250, [(t_see + .1, "IT'S A SEE-SAW", INK), (t_one, "ONE NUMBER DECIDES IT", INK)], 64, "a", "mm")
    tag(base, lt, px, 780, "?%", 110, t_one + .5, CARD, INK, -2, "a", "chime", (34, 18))
    ring(d, (px - 120, 700, px + 120, 862), appear(lt, t_one + 1.2, .5, "marker"), ORANGE, 6)
    note(d, lt, px, 880, "you already know it", 46, t_know, MUTED, anchor="ma")

def s_sting(base, d, lt, L, cam):
    base.paste(navy_sheet(), (0, 0)); _rec("c", (-160, -160, W + 160, H + 160))
    mark = _scaled("mark_gradient_on-dark", 260); wd = int(mark.size[0] * ease(lt / .6))
    if wd > 2: cc = mark.crop((0, 0, wd, mark.size[1])); base.paste(cc, (int(X(960) - mark.size[0] / 2), int(X(290))), cc)
    b = ease((lt - .6) / .6); wm = _wordmark(92); paste(base, wm, X(960) - wm.size[0] / 2, X(628 - 30 * (1 - b)), b)
    T(d, 960, 790, "Where your money is heading, drawn out.", 40, "r", LIGHT, "ma", ease((lt - 1.2) / .6), INK)
@lru_cache(maxsize=None)
def _scaled(name, h):
    im = vlib._asset(name); hh = int(h * S); return im.resize((int(im.size[0] * hh / im.size[1]), hh), Image.LANCZOS)
@lru_cache(maxsize=None)
def _wordmark(h):
    im = vlib._asset("lockup_horizontal_on-dark").crop((1340, 0, 3938, 800)); im = im.crop(im.getbbox()); hh = int(h * S)
    return im.resize((int(im.size[0] * hh / im.size[1]), hh), Image.LANCZOS)

# ================= 3 roadmap =================
GX0, GX1, GY0, GY1 = 720, 1110, 470, 330                            # balance plot: x months 0..300, y £0..£200,000
def gpt(m, b): return (GX0 + (GX1 - GX0) * m / 300, GY0 - (GY0 - GY1) * b / vlib.P)
P0 = tuple(gpt(m, BAL0[m]) for m in list(range(0, 300, 4)) + [300])
P1 = tuple(gpt(m, BAL1[m]) for m in list(range(0, 258, 4)) + [258])
def s_roadmap(base, d, lt, L, cam):
    c = C("roadmap")
    t_last, t_100, t_does, t_ex, t_big, t_best = c("last time"), c("one hundred pounds"), c("does to our"), c("our example mortgage"), c("the bigger question"), c("is that the best")
    deco(base, cam, "blobO", 260, 380, .3); deco(base, cam, "blobB", 1650, 330, .3); deco(base, cam, "dots", 1740, 980, .15)
    kline(d, lt, 110, 150, [("THE BIGGER QUESTION:", t_big, INK, None), ("OVERPAY", t_big + 1.0, INK, "o"), ("OR INVEST?", t_big + 1.4, INK, "b")], 88, "a")
    # last time: the mortgage balance drawn as it is described; the £100 pulls the orange line down early
    box = (110, 270, 1150, 530); a = panel(base, lt, box, .1, CARD, seed=8, frm=(-60, 0))
    if a > .02:
        _rec("z", box)
        T(d, 140, 286, "LAST TIME", 30, "o", BROWN, a=fa(lt, t_last + .1), on=CARD)
        kline(d, lt, 140, 328, [("+£100 A MONTH", t_100, INK, "o")], 54, "a", on=CARD, step=.12)
        kline(d, lt, 140, 400, [("OVERPAID", t_100 + .7, INK, None)], 54, "a", on=CARD, step=.12)
        note(d, lt, 140, 470, "£200,000 · 25 years · 5%", 38, t_ex, MUTED, CARD)
        ga = fa(lt, t_last + .2)
        if ga > .03:
            d.line([X(GX0), X(GY0), X(GX1 + 6), X(GY0)], fill=mix(CARD, INK, ga), width=4); d.line([X(GX0), X(GY0), X(GX0), X(GY1 - 18)], fill=mix(CARD, INK, ga), width=4)
            T(d, GX0 + 10, 290, "Balance £200,000", 22, "sb", MUTED, a=ga, on=CARD); T(d, GX0, 482, "0", 22, "sb", MUTED, "ma", ga, CARD)
        stroke(d, list(P0), clamp((lt - t_last - .4) / (t_100 - t_last - .3)), MUTED, 5, 31, .6); appear(lt, t_last + .4, .4, "marker")
        p1 = clamp((lt - t_100 - .3) / (t_ex + 1.2 - t_100 - .3)); appear(lt, t_100 + .3, .4, "marker")
        tip = stroke(d, list(P1), p1, ORANGE, 7, 32, .6)
        if tip and p1 < 1:
            lx = max(GX0 + 10, tip[-1][0] - tw("−£100 a month", 30, "c") - 8); T(d, lx, min(tip[-1][1] + 6, GY0 - 44), "−£100 a month", 30, "c", ORANGE, a=fa(lt, t_100 + .5), on=CARD)
        t_end = t_ex + 1.25; appear(lt, t_end, .2, "thud"); chime(lt, t_end + .25)
        stroke(d, [gpt(258, 0), gpt(300, 0)], appear(lt, t_end + .1, .3, None), DGREEN, 9, 33, .3)
        T(d, gpt(258, 0)[0], 482, "month 258", 22, "sb", DGREEN, "ma", fa(lt, t_end), CARD)
        note(d, lt, GX1 + 20, 290, "3½ years early", 34, t_end + .25, DGREEN, CARD, "ra")
        arrow(d, (1090, 340), (1084, 452), appear(lt, t_end + .5, .4, None), DGREEN, 4, -.15)
    note(d, lt, 1215, 300, "is that the best", 60, t_best); note(d, lt, 1215, 366, "home for the money?", 60, t_best + .8)
    underline(d, 1215, 1215 + tw("home for the money?", 60, "c"), 440, appear(lt, t_best + 1.6, .5, "marker"), BLUE)
    steps = [("first what overpaying", "lock", "WHAT OVERPAYING", "REALLY EARNS", "o"), ("then what investing", "chart", "WHAT INVESTING", "CAN EARN", "b"),
             ("and what fees", "tap", "WHAT FEES AND TAX", "TAKE OFF THE TOP", "k"), ("then we'll race", "calculator", "THE RACE:", "25 YEARS, HEAD TO HEAD", "g")]
    for i, (cue, ic, l1, l2, dc) in enumerate(steps):
        t0 = c(cue); x0 = 110 + i * 430
        panel(base, lt, (x0, 560, x0 + 400, 930), t0 - .1, seed=i + 3)
        T(d, x0 + 30, 570, str(i + 1), 70, "a", ORANGE, a=ease((lt - t0 - .15) / .25), on=CARD)
        ix, iy = par(cam, x0 + 215, 690, .05, lt, i)
        cut(base, lt, ic, ix, iy, 140, t0 + .2, rot=(-4, 3, -3, 4)[i], disc=(dc, 88))
        kline(d, lt, x0 + 200, 805, [(l1, t0 + .4, INK, None)], 38, "o", "m", CARD); kline(d, lt, x0 + 200, 857, [(l2, t0 + .65, INK, None)], 38, "o", "m", CARD)
    t_s = c("this is a simple"); s = "a simple example, not advice. There's no single right answer."
    note(d, lt, 110, 952, s, 46, t_s)
    x0 = 110 + tw("a simple example, ", 46, "c"); underline(d, x0, x0 + tw("not advice.", 46, "c"), 1010, appear(lt, c("not advice") + .4, .45, "marker"), ORANGE)

# ---- appended for the full-length build: scenes 4-7 (5b layouts + the seven techniques) ----
def big(d, lt, x, y, s, size, t0, hk=None, f="a", fill=INK, on=PAPER, anchor="l", ref=None):
    a = ease((lt - t0) / .25); fo = F(f, size); w = fo.getlength(ref or s) / S
    x0 = x - (w if anchor == "r" else w / 2 if anchor == "m" else 0)
    if hk: ph = appear(lt, t0 + .3, .45, "marker")
    if a <= .03: return x0 + w
    bb = fo.getbbox("H0"); top, bot = bb[1] / S, bb[3] / S
    if hk: hl(d, x0, y + top + (bot - top) * .06, x0 + w, y + bot + (bot - top) * .1, mix(on, HLC[hk], .95), ph)
    T(d, x0, y, s, size, f, fill, "la", a, on); return x0 + w
def ruled(d, box, a, step=56):
    for yy in range(int(box[1]) + 46, int(box[3]) - 10, step): d.line([X(box[0] + 18), X(yy), X(box[2] - 18), X(yy)], fill=mix(CARD, (200, 220, 240), a * .7), width=2)
    d.line([X(box[0] + 22), X(box[1] + 10), X(box[0] + 22), X(box[3] - 10)], fill=mix(CARD, (255, 190, 170), a), width=2)

def s_guaranteed(base, d, lt, L, cam):
    c = C("guaranteed")
    t_here, t_200, t_25, t_5, t_pay = c("here's the mortgage"), c("two hundred thousand"), c("over twenty five"), c("at five per cent"), c("one thousand one hundred")
    t_every, t_costs, t_so, t_stops, t_off, t_five, t_never = c("every pound you still"), c("costs you five"), c("so every pound"), c("stops costing"), c("pay off an extra"), c("about five pounds"), c("interest you never")
    t_think, t_acc, t_paying, t_g, t_bank, t_nf, t_nt, t_nb = c("think of overpaying"), c("a savings account"), c("paying a guaranteed"), c("guaranteed five"), c("from a bank"), c("no fees"), c("no tax"), c("no bad years")
    deco(base, cam, "blobO", 240, 470, .3); deco(base, cam, "dots", 1700, 330, .15); deco(base, cam, "blobK", 1600, 760, .25)
    kline(d, lt, 110, 150, [("WHAT", .25, INK, None), ("OVERPAYING", .5, INK, "o"), ("REALLY EARNS", .9, INK, None)], 88, "a")
    hx, hy = par(cam, 215, 385, .05, lt, 1); cut(base, lt, "house", hx, hy, 170, t_here + .1, rot=-5, disc=("o", 105))
    tag(base, lt, 530, 330, "£200,000", 64, t_200, CARD, INK, -2, "a")
    tag(base, lt, 840, 336, "25 YEARS", 64, t_25, CARD, INK, 2, "a")
    tag(base, lt, 1080, 330, "5%", 64, t_5, ORANGE, INK, -1.5, "a")
    note(d, lt, 1220, 300, "the same mortgage as", 44, t_here + .6, MUTED); note(d, lt, 1220, 350, "Episodes 01 and 03", 44, t_here + 1.2, MUTED)
    # the payment counter flips up digit by digit, then re-forms with a pulse
    appear(lt, t_pay, .9, "ticks"); appear(lt, t_pay + .9, .2, "thud")
    if lt > t_pay:
        u = clamp((lt - t_pay) / .9); v = vlib.PAY * ease(u); sc = 1 + .1 * math.sin(math.pi * clamp((lt - t_pay - .9) / .3))
        T(d, 380, 398 + 12 * (1 - eout(u)), gbp(v, 2), 100 * sc, "a", INK, "la", min(1, u * 3))
        hl_p = appear(lt, t_pay + 1.0, .45, "marker"); xe = 380 + tw("£1,169.18", 100, "a")
    else: appear(lt, t_pay + 1.0, .45, "marker"); xe = 380 + tw("£1,169.18", 100, "a")
    T(d, xe + 24, 430, "A MONTH", 50, "o", INK, a=fa(lt, t_pay + .9))
    underline(d, 380, xe, 520, appear(lt, t_pay + 1.0, .45, None), ORANGE, 6)
    kx, ky = par(cam, 215, 650, .07, lt, 2); cut(base, lt, "coins", kx, ky, 160, t_every, rot=-5, disc=("o", 100))
    kline(d, lt, 372, 556, [("Every £1 you", t_every + .1, INK, None), ("still owe", t_every + .6, INK, None)], 40, "b", step=.16)
    kline(d, lt, 372, 608, [("costs you", t_costs, INK, None), ("5%", t_costs + .5, INK, "o"), ("a year", t_costs + .9, INK, None)], 40, "b", step=.16)
    note(d, lt, 372, 672, "so every £1 you overpay", 50, t_so); note(d, lt, 372, 726, "stops costing you that", 50, t_stops)
    underline(d, 372, 372 + tw("stops costing you that", 50, "c"), 790, appear(lt, t_stops + 1.0, .5, "marker"), ORANGE)
    # evidence: the £100 token re-forms into our worked sum on a calculation sheet; the £5 is highlighted as it's spoken
    box = (110, 812, 900, 985); a = panel(base, lt, box, t_off - .2, CARD, seed=5)
    if a > .02:
        ruled(d, box, a, 60); T(d, 146, 822, "FIGURES FORWARD CALCULATION", 22, "o", MUTED, a=fa(lt, t_off), on=CARD)
    tag(base, lt, 300, 892, "£100", 52, t_off + .15, ORANGE, INK, -3, "a", "pop", (18, 10), t_five - .7)
    t_eq = t_five - .4; appear(lt, t_eq, .3, "click")
    if a > .02:
        sc = .6 + .4 * back((lt - t_eq) / .35)
        T(d, 146, 890, "£100 × 5% =", 56 * sc, "a", INK, "lm", fa(lt, t_eq, .2), CARD)
        xv = 146 + tw("£100 × 5% = ", 56, "a"); fo = F("a", 56); bb = fo.getbbox("H0"); hh = (bb[3] - bb[1]) / S
        hp = appear(lt, t_five + .45, .4, "marker")
        if hp > .01: hl(d, xv, 890 - hh / 2 - 6, xv + tw("£5", 56, "a"), 890 + hh / 2 + 8, mix(CARD, HLC["g"], .95), hp)
        if lt > t_five: T(d, xv, 890, gbp(count(5, lt, t_five, .4)), 56, "a", DGREEN, "lm", 1, CARD)
        else: count(5, lt, t_five, .4)
        T(d, xv + tw("£5 ", 56, "a"), 890, "A YEAR", 34, "o", INK, "lm", fa(lt, t_five + .4), CARD)
        note(d, lt, 146, 930, "of interest you never pay, every year", 32, t_never, MUTED, CARD)
    chime(lt, t_five + .5)
    # the bank that can't say no (layered cut-out on kraft)
    panel(base, lt, (960, 550, 1812, 990), t_think - .25, KRAFT, seed=8, frm=(60, 0))
    bx, by_ = par(cam, 1085, 690, .03, lt, 3); cut(base, lt, "bank", bx, by_, 180, t_think + .1, rot=-3, disc=("w", 110))
    T(d, 1232, 570, "THINK OF IT AS", 30, "o", BROWN, a=fa(lt, t_think + .1), on=KRAFT)
    kline(d, lt, 1232, 612, [("a savings account", t_acc, INK, None)], 40, "b", on=KRAFT, step=.2)
    kline(d, lt, 1232, 664, [("paying a", t_paying, INK, None), ("guaranteed", t_g - .2, INK, None)], 40, "b", on=KRAFT, step=.2)
    big(d, lt, 1232, 704, "5%", 100, t_g + .3, "o", on=KRAFT)
    tag(base, lt, 1570, 772, "GUARANTEED", 48, t_g + .7, GREEN, INK, -5, sfx="chime")
    note(d, lt, 1000, 848, "from a bank that can't say no", 50, t_bank, on=KRAFT)
    x0 = 1000 + tw("from a bank that ", 50, "c"); ring(d, (x0 - 16, 846, x0 + tw("can't say no", 50, "c") + 16, 914), appear(lt, t_bank + 1.4, .5, "marker"), INK, 5)
    for t0, s, x, r in ((t_nf, "NO FEES", 1100, -3), (t_nt, "NO TAX", 1310, 2), (t_nb, "NO BAD YEARS", 1560, -2)):
        tag(base, lt, x, 948, s, 34, t0, GREEN, INK, r)

BLUE_PATH = [(0, 0), (.06, .07), (.1, .04), (.16, .16), (.2, .13), (.27, .28), (.31, .24), (.38, .40), (.43, .47), (.47, .42), (.52, .30), (.56, .33), (.6, .24), (.65, .29),
             (.7, .44), (.74, .40), (.8, .58), (.84, .54), (.9, .74), (.94, .70), (1, .86)]
def s_expected(base, d, lt, L, cam):
    c = C("expected")
    t_diff, t_long, t_exp, t_not, t_jump, t_drop, t_sharp = c("is a different"), c("over long stretches"), c("an expected return"), c("not a promised"), c("some years it jumps"), c("some years it drops"), c("sometimes sharply")
    t_pic, t_solid, t_g5, t_other, t_still, t_heavy, t_light, t_end = c("picture a balance"), c("a solid block"), c("a guaranteed five"), c("on the other"), c("won't sit still"), c("might be heavier"), c("might be lighter"), c("you only find out")
    deco(base, cam, "blobB", 1500, 620, .3); deco(base, cam, "dots", 1740, 180, .15); deco(base, cam, "blobK", 150, 950, .25)
    kline(d, lt, 110, 150, [("INVESTING", .3, INK, "b"), ("IS A DIFFERENT ANIMAL", t_diff, INK, None)], 88, "a")
    bx = kline(d, lt, 110, 262, [("an", t_exp - .2, INK, None), ("expected", t_exp, INK, "b"), ("return,", t_exp + .6, INK, None), ("not a", t_not, INK, None), ("promised", t_not + .3, INK, None), ("one", t_not + .8, INK, None)], 40, "b", step=.15)
    stroke(d, [(bx[4][0] - 6, bx[4][1] + 20), (bx[4][2] + 8, bx[4][1] + 12)], appear(lt, t_not + 1.0, .35, "marker"), ORANGE, 6, 4)
    box = (110, 335, 1000, 938); pa = panel(base, lt, box, t_long - .5, seed=12)
    if pa > .02:
        _rec("z", box)
        if pa >= 1:
            for gx in range(150, 990, 40): d.line([X(gx), X(352), X(gx), X(920)], fill=(214, 226, 238) if (gx - 150) % 200 else (188, 206, 226), width=2)
            for gy in range(360, 930, 40): d.line([X(126), X(gy), X(984), X(gy)], fill=(214, 226, 238) if (gy - 360) % 200 else (188, 206, 226), width=2)
            px0, px1, py0, py1 = 170, 950, 850, 430
            d.line([X(px0), X(py0), X(px1), X(py0)], fill=INK, width=4); d.line([X(px0), X(py0), X(px0), X(py1 - 30)], fill=INK, width=4)
            T(d, px1, 866, "TIME", 26, "o", MUTED, "ra", on=CARD)
            stroke(d, [(px0, py0 - 20), (px1, py0 - 200)], appear(lt, t_long - .1, 1.2, "marker"), ORANGE, 7, 2, .6)
            pb = pw(lt, [(t_long + .9, 0), (t_jump - .3, .2), (t_jump + .6, .45), (t_drop + .6, .62), (t_sharp + .5, .68), (t_pic - .2, 1)])
            for t0 in (t_jump, t_drop): appear(lt, t0, .3, "swish")
            stroke(d, [(px0 + (px1 - px0) * u, py0 - 20 - (py0 - py1 - 20) * v) for u, v in BLUE_PATH], pb, BLUE, 7, 6, .9)
            lg = ease((lt - t_long - .9) / .3)
            if lg > .03:
                d.line([X(196), X(398), X(250), X(398)], fill=mix(CARD, ORANGE, lg), width=8); T(d, 266, 380, "Overpaying: a steady 5%", 28, "sb", INK, a=lg, on=CARD)
                d.line([X(196), X(442), X(250), X(442)], fill=mix(CARD, BLUE, lg), width=8); T(d, 266, 424, "Shares: have tended to grow faster", 28, "sb", INK, a=lg, on=CARD)
            note(d, lt, 380, 548, "some years it jumps", 44, t_jump, on=CARD)
            arrow(d, (560, 604), (510, 634), appear(lt, t_jump + .4, .4, "marker"), INK, 5, -.3)
            note(d, lt, 690, 744, "it drops,", 42, t_drop, on=CARD); note(d, lt, 690, 788, "sometimes sharply", 42, t_sharp, on=CARD)
            arrow(d, (684, 764), (646, 742), appear(lt, t_drop + .4, .4, "marker"), INK, 5, .3, 9)
    T(d, 112, 950, "Illustration only · investment returns are never guaranteed", 24, "r", MUTED, a=ease((lt - t_long - 1.0) / .4))
    cx, by, half, drop = 1420, 470, 240, 178; s_ = appear(lt, t_pic, .5, "slide")
    note(d, lt, cx, 345, "picture a balance scale", 54, t_pic + .1, anchor="ma")
    if s_ > .02:
        rb = ease((lt - t_still) / .4)
        rock = 3 * math.sin(2 * math.pi * (lt - t_still) / 1.8) * rb if lt > t_still else 0
        if lt < t_still: deg = pw(lt, [(t_solid + .2, 0), (t_solid + .7, -5), (t_other + .2, -5), (t_other + .7, 0)])
        elif lt < t_heavy: deg = rock
        elif lt < t_light: deg = rock + (6 - rock) * ease((lt - t_heavy) / .5)
        else: u, v = ease((lt - t_light) / .5), ease((lt - t_light - .7) / .5); deg = (6 - 12 * u) * (1 - v) + rock * v
        for t0 in (t_heavy, t_light): appear(lt, t0, .5, "slide")
        th = math.radians(deg); col = mix(PAPER, INK, s_)
        d.polygon([(X(cx - 90), X(930)), (X(cx + 90), X(930)), (X(cx + 60), X(900)), (X(cx - 60), X(900))], fill=col); d.rectangle([X(cx - 9), X(by), X(cx + 9), X(902)], fill=col)
        ends = [(cx - half * math.cos(th), by - half * math.sin(th)), (cx + half * math.cos(th), by + half * math.sin(th))]
        d.line([(X(ends[0][0]), X(ends[0][1])), (X(ends[1][0]), X(ends[1][1]))], fill=col, width=int(16 * S)); d.ellipse([X(cx - 22), X(by - 22), X(cx + 22), X(by + 22)], fill=mix(PAPER, ORANGE, s_))
        for i, (ex, ey) in enumerate(ends):
            py = ey + drop
            d.line([X(ex), X(ey), X(ex - 170), X(py)], fill=col, width=4); d.line([X(ex), X(ey), X(ex + 170), X(py)], fill=col, width=4)
            d.rounded_rectangle([X(ex - 180), X(py), X(ex + 180), X(py + 14)], 8, fill=col)
            if i == 0: tag(base, lt, ex, py - 62, "5%", 78, t_solid, ORANGE, INK, 0, "a", "thud", (34, 16))
            else:
                jit = 4 * math.sin(2 * math.pi * lt / .45) * rb
                tag(base, lt, ex + jit, py - 62, "?%", 78, t_other + .3, BLUE, CARD, round(2 * math.sin(5 * lt) * rb), "a", "thud", (34, 16))
        T(d, cx - half, 690, "OVERPAYING", 40, "o", INK, "ma", ease((lt - t_solid) / .3)); T(d, cx - half, 746, "a solid block: guaranteed", 26, "sb", MUTED, "ma", ease((lt - t_g5) / .3))
        T(d, cx + half, 690, "INVESTING", 40, "o", INK, "ma", ease((lt - t_other) / .3)); T(d, cx + half, 746, "a block that won't sit still", 26, "sb", MUTED, "ma", ease((lt - t_still) / .3))
        cut(base, lt, "lock", cx - half, 872 + 3 * math.sin(lt * 2), 100, t_g5, rot=-5); cut(base, lt, "chart", cx + half, 872 + 3 * math.sin(lt * 2 + 1), 100, t_other + .6, rot=5)
    note(d, lt, 1810, 258, "you only find out at the end", 54, t_end, anchor="ra"); chime(lt, t_end + .2)
    underline(d, 1810 - tw("you only find out at the end", 54, "c"), 1810, 326, appear(lt, t_end + 1.0, .5, "marker"), ORANGE)

def s_fees(base, d, lt, L, cam):
    c = C("fees")
    t_isnt, t_fees, t_tap, t_7, t_1, t_6, t_on = c("isn't what you keep"), c("fees come out"), c("like a dripping tap"), c("grow at seven"), c("charges take one"), c("you keep six"), c("on a hundred pounds")
    t_81, t_69, t_12, t_tax, t_unl, t_so, t_ret = c("about eighty one"), c("about sixty nine"), c("nearly twelve thousand"), c("tax can take"), c("unless the money"), c("so the number"), c("the return after")
    deco(base, cam, "blobB", 260, 420, .3); deco(base, cam, "dots", 1100, 300, .15); deco(base, cam, "blobO", 1500, 760, .25)
    kline(d, lt, 110, 150, [("THE HEADLINE RETURN", .3, INK, None), ("ISN'T WHAT YOU KEEP", t_isnt, INK, "o")], 88, "a")
    cut(base, lt, "tap", 215, 400, 200, t_fees, rot=0, disc=("b", 122), extra=(90, 278, 340, 600))
    if lt > t_tap + .3:
        for n in range(3):
            ph = ((lt - t_tap) * .85 + n / 3) % 1; yy = 507 + 62 * ph * ph; r_ = 7 * (1 - .5 * ph)
            d.ellipse([X(276 - r_), X(yy - r_ * 1.3), X(276 + r_), X(yy + r_ * 1.3)], fill=mix(PAPER, ORANGE, 1 - ph ** 3))
    note(d, lt, 376, 286, "fees come out every year,", 54, t_fees + .2); note(d, lt, 376, 346, "like a dripping tap", 54, t_tap)
    underline(d, 376, 376 + tw("like a dripping tap", 54, "c"), 412, appear(lt, t_tap + .9, .5, "marker"), ORANGE)
    # evidence: 7% - 1% = 6% worked on a calculation sheet, the 6% highlighted as it's spoken
    sb = (390, 424, 1170, 604); a = panel(base, lt, sb, t_7 - .3, CARD, seed=17, frm=(0, 40))
    if a > .02: ruled(d, sb, a, 60)
    y = 436; x = 420
    xe = big(d, lt, x, y, "7%", 110, t_7, None, fill=BLUE, on=CARD); T(d, x, 562, "GROWTH", 26, "o", MUTED, a=fa(lt, t_7 + .3), on=CARD)
    T(d, xe + 26, y, "−", 110, "a", MUTED, a=fa(lt, t_1), on=CARD); x1 = xe + 26 + tw("−", 110, "a") + 26
    xe = big(d, lt, x1, y, "1%", 110, t_1 + .1, None, fill=ORANGE, on=CARD); appear(lt, t_1 + .1, .3, "click"); T(d, x1, 562, "FEES", 26, "o", MUTED, a=fa(lt, t_1 + .4), on=CARD)
    T(d, xe + 26, y, "=", 110, "a", MUTED, a=fa(lt, t_6), on=CARD); x2 = xe + 26 + tw("=", 110, "a") + 26
    big(d, lt, x2, y, "6%", 110, t_6 + .1, "g", on=CARD); appear(lt, t_6 + .1, .3, "thud"); T(d, x2, 562, "YOU KEEP", 26, "o", MUTED, a=fa(lt, t_6 + .4), on=CARD)
    ring(d, (x2 - 22, y - 2, x2 + tw("6%", 110, "a") + 22, y + 160), appear(lt, t_ret + .9, .5, "marker"), ORANGE, 6)
    # pots drawn as bars; the 7% total re-forms into the 6% total, the gap breaks away as fees
    T(d, 110, 624, "£100 A MONTH FOR 25 YEARS", 30, "o", MUTED, a=fa(lt, t_on))
    B7_ = vlib.B[.07]; assert B7_ - B6 == 11708 and B7_ == 81007; xr = 300 + 820 * B6 / B7_
    for lab, box, v, t0 in (("AT 7%", (300, 664, 1120, 748), B7_, t_81), ("AT 6%", (300, 768, xr, 852), B6, t_69)):
        T(d, 110, box[1] + 10, lab, 50, "a", INK, a=fa(lt, t0))
        strip(base, lt, box, t0, (84, 166, 255), .9, 40 + int(box[1]) % 7)
        if lt > t0 + .9: T(d, box[2] - 22, box[1] + 12, gbp(count(v, lt, t0 + .9, .6)), 44, "a", CARD, "ra", 1, (84, 166, 255))
        else: count(v, lt, t0 + .9, .6)
    strip(base, lt, (xr, 768, 1120, 852), t_12, (255, 158, 66), .5, 47, "swish")
    arrow(d, (1126, 818), (1180, 776), appear(lt, t_12 + .6, .45, "marker"), INK, 5, .3)
    panel(base, lt, (1190, 646, 1812, 866), t_12 + .1, INK, seed=6)
    kline(d, lt, 1224, 662, [("GONE TO FEES", t_12 + .3, ORANGE, None)], 34, "o", on=INK, step=.1)
    if lt > t_12 + .5: T(d, 1224, 708, gbp(count(B7_ - B6, lt, t_12 + .5, .9)), 110, "a", CARD, on=INK)
    else: count(B7_ - B6, lt, t_12 + .5, .9)
    chime(lt, t_12 + 1.4)
    panel(base, lt, (1190, 270, 1812, 580), t_tax - .2, KRAFT, seed=14, frm=(60, 0))
    cut(base, lt, "coins", 1290, 362, 110, t_tax + .1, rot=6)
    T(d, 1392, 290, "TAX", 84, "a", INK, a=fa(lt, t_tax, .25), on=KRAFT)
    lines = wrap("can take another slice, unless the money sits in tax-free or tax-relieved accounts where you live.", 28, "sb", 560); seen = 0
    for j, ln in enumerate(lines):
        pre = "unless" not in " ".join(lines[:j + 1])
        t0 = t_tax + .5 + j * .55 if pre else t_unl + (j - seen) * .9
        if pre: seen = j + 1
        T(d, 1222, 456 + j * 38, ln, 28, "sb", INK, a=fa(lt, t0), on=KRAFT, dy=8 * (1 - eout((lt - t0) / .3)))
    kline(d, lt, 110, 905, [("SO COMPARE YOUR MORTGAGE RATE WITH", t_so + .2, INK, None), ("THE RETURN AFTER FEES AND TAX", t_ret, INK, "o")], 56, "a", step=.12)
    chime(lt, t_ret + 1.2)

def jar(base, d, lt, cx, cy, t0, level, drops=None):
    """A paper jar drawn in code (empty to start) that fills as money drops in."""
    a = appear(lt, t0, .5, "thud")
    if a <= .03: return
    e = back(clamp((lt - t0) / .5)); w, h = 72 * e, 88 * e
    if drops:
        rate, ts = drops
        if lt > ts:
            for n in range(4):
                ph = ((lt - ts) * rate + n / 4) % 1
                if lt - ts > ph / rate: yy = cy - h - 64 + 64 * ph * ph; d.ellipse([X(cx - 9), X(yy - 9), X(cx + 9), X(yy + 9)], fill=mix(PAPER, BLUE, 1 - ph ** 4))
    d.rounded_rectangle([X(cx - w), X(cy - h), X(cx + w), X(cy + h)], int(26 * S), fill=mix(PAPER, (244, 246, 248), a))
    if level > .005:
        top = cy + h - 8 - (2 * h - 16) * level
        d.rounded_rectangle([X(cx - w + 8), X(top), X(cx + w - 8), X(cy + h - 8)], int(18 * S), fill=(84, 166, 255))
    d.rounded_rectangle([X(cx - w), X(cy - h), X(cx + w), X(cy + h)], int(26 * S), outline=mix(PAPER, INK, a), width=int(5 * S))
    d.rounded_rectangle([X(cx - w * .78), X(cy - h - 24), X(cx + w * .78), X(cy - h + 2)], int(6 * S), fill=mix(PAPER, KRAFT, a), outline=mix(PAPER, INK, a), width=int(3 * S))
    vlib._rec("i", (cx - w - 4, cy - h - 30, cx + w + 4, cy + h + 4), "jar")

def s_setup(base, d, lt, L, cam):
    c = C("setup")
    t_fair, t_two, t_sm, t_ss, t_jars, t_A, t_empty, t_258, t_35 = c("a fair race"), c("two people"), c("the same mortgage"), c("the same spare"), c("think of two jars"), c("person a overpays"), c("stays empty"), c("is gone at month"), c("three and a half")
    t_then, t_1269, t_B, t_Bi, t_all, t_same, t_both, t_q, t_whose = c("from then on"), c("one thousand two"), c("person b pays"), c("and drops a hundred"), c("for all three"), c("same money out"), c("both end"), c("the only question"), c("whose jar")
    deco(base, cam, "blobO", 230, 450, .3); deco(base, cam, "blobB", 230, 770, .3); deco(base, cam, "dots", 1700, 620, .15)
    kline(d, lt, 110, 150, [("A FAIR RACE", t_fair, INK, "o")], 88, "a")
    tag(base, lt, 730, 204, "TWO PEOPLE", 38, t_two, CARD, INK, -3); tag(base, lt, 1030, 198, "SAME MORTGAGE", 38, t_sm, CARD, INK, 2); tag(base, lt, 1480, 204, "SAME SPARE £100", 38, t_ss, INK, CARD, -1.5)
    # jars fill as money drops in: B from day one, slowly; A only after month 258, fast. Levels stop equal: the race is next scene.
    lB = .42 * clamp((lt - t_Bi - .3) / (t_whose - t_Bi - .3)); lA = .42 * clamp((lt - t_then - .5) / (t_whose - t_then - .5)) ** 1.3
    jar(base, d, lt, 1650, 440, t_jars + .2, lA, (2.2, t_then + .5)); jar(base, d, lt, 1650, 746, t_jars + .55, lB, (.9, t_Bi + .3))
    T(d, 1650, 562, "A'S JAR", 30, "o", MUTED, "ma", fa(lt, t_jars + .6)); T(d, 1650, 864, "B'S JAR", 30, "o", MUTED, "ma", fa(lt, t_jars + .9))
    X0, X1 = 330, 1420; xm = X0 + (X1 - X0) * vlib.END_A / 300
    ax, ay = par(cam, 190, 452, .06, lt, 1); cut(base, lt, "personA", ax, ay, 270, t_A - .3, rot=-2, duo=False)
    tag(base, lt, 400, 322, "PERSON A", 40, t_A, ORANGE, INK, -3, sfx=None)
    strip(base, lt, (X0, 398, xm, 462), t_A + .4, (255, 158, 66), 1.4, 41)
    T(d, X0 + 22, 407, "OVERPAYS £100 A MONTH", 32, "o", INK, a=fa(lt, t_A + 1.7), on=(255, 158, 66))
    note(d, lt, 1490, 300, "empty for years...", 40, t_empty, MUTED, anchor="ra")
    note(d, lt, 560, 296, "mortgage gone at month 258,", 44, t_258); note(d, lt, 560, 340, "3½ years early", 44, t_35, DGREEN)
    arrow(d, (850, 372), (xm - 6, 394), appear(lt, t_35 + .6, .45, "marker"), INK, 5, -.25)
    strip(base, lt, (xm + 6, 398, X1, 462), t_then + .4, (84, 166, 255), .7, 42, rec=False)
    T(d, X0, 474, "MONTH 0", 26, "o", MUTED, a=fa(lt, t_A + .6)); T(d, xm, 474, "258", 26, "o", MUTED, "ma", fa(lt, t_258 + .5)); T(d, X1, 474, "300", 26, "o", MUTED, "ma", fa(lt, t_then + 1.0))
    # kinetic: the mortgage payment plus the £100 re-forms into the £1,269.18 that now goes in the jar
    morph(d, lt, X1 + 4, 544, [(t_then + .5, "THEN £1,169.18 + £100", INK), (t_1269, "= £1,269.18 A MONTH INTO THE JAR", BLUE)], 36, "o", "rm")
    bpx, bpy = par(cam, 190, 756, .06, lt, 2); cut(base, lt, "personB", bpx, bpy, 270, t_B - .3, rot=2, duo=False)
    tag(base, lt, 400, 644, "PERSON B", 40, t_B, BLUE, CARD, 3, sfx=None)
    strip(base, lt, (X0, 706, X1, 762), t_B + .4, KRAFT, 1.4, 43)
    T(d, X0 + 22, 715, "PAYS THE MORTGAGE AS NORMAL, ALL 25 YEARS", 28, "o", INK, a=fa(lt, t_B + 1.5), on=KRAFT)
    strip(base, lt, (X0, 776, X1, 840), t_Bi + .2, (84, 166, 255), 1.8, 44)
    T(d, X0 + 22, 785, "£100 A MONTH INTO THE JAR, ALL 300 MONTHS", 32, "o", CARD, a=fa(lt, t_all), on=(84, 166, 255))
    note(d, lt, 1490, 608, "from day one", 40, t_Bi + .6, MUTED, anchor="ra")
    T(d, X0, 852, "MONTH 0", 26, "o", MUTED, a=fa(lt, t_B + .6)); T(d, X1, 852, "300", 26, "o", MUTED, "ma", fa(lt, t_all + .4))
    tag(base, lt, 640, 958, "SAME MONEY OUT, EVERY MONTH", 38, t_same, INK, CARD, -2)
    for yy, sd in ((430, 3), (772, 4)):
        stroke(d, [(1450, yy), (1466, yy + 20), (1500, yy - 26)], appear(lt, t_both + .4 + sd * .05, .35, "marker"), DGREEN, 7, sd, .6)
    kline(d, lt, 950, 920, [("WHOSE JAR IS", t_whose, INK, None), ("FULLER?", t_whose + .5, INK, "o")], 62, "a", step=.2)
    chime(lt, t_whose + 1.0)

def cams_full(cm):
    D = {k: BYKEY[k]["dur"] for k in ORDER}
    c = C("guaranteed"); te, tt, tn, tf = c("every pound you still"), c("think of overpaying"), c("no fees"), c("about five pounds")
    cm["guaranteed"] = [(0, 960, 350, 1.1), (te - .8, 960, 354, 1.09), (te + .3, 960, 560, 1.06), (tf - 1.2, 960, 565, 1.06), (tf - .2, 955, 562, 1.06),
                        (tt - .6, 955, 562, 1.06), (tt + .3, 960, 546, 1.0), (tn - .8, 960, 548, 1.0), (tn + .2, 975, 560, 1.03), (D["guaranteed"], 960, 552, 1.035)]
    c = C("expected"); tl, tp = c("over long stretches"), c("picture a balance")
    cm["expected"] = [(0, 700, 340, 1.2), (tl - .8, 700, 344, 1.18), (tl + .6, 800, 558, 1.08), (tp - .9, 812, 560, 1.08), (tp + .3, 960, 546, 1.0), (D["expected"], 960, 552, 1.035)]
    c = C("fees"); t7, ton, t12, ttx, tso = c("grow at seven"), c("on a hundred pounds"), c("nearly twelve thousand"), c("tax can take"), c("so the number")
    cm["fees"] = [(0, 900, 400, 1.12), (t7 - .5, 905, 404, 1.11), (t7 + .4, 800, 430, 1.16), (ton - .9, 800, 432, 1.16), (ton + .2, 960, 560, 1.0), (t12 - .3, 960, 560, 1.0), (t12 + .6, 990, 600, 1.05),
                  (ttx - .6, 990, 590, 1.05), (ttx + .3, 990, 470, 1.06), (tso - .6, 990, 470, 1.06), (tso + .3, 960, 546, 1.0), (D["fees"], 960, 552, 1.035)]
    c = C("setup"); tj, tB, tbo = c("think of two jars"), c("person b pays"), c("both end")
    cm["setup"] = [(0, 860, 380, 1.12), (tj - .6, 870, 384, 1.11), (tj + .3, 960, 470, 1.04), (tB - .9, 960, 480, 1.04), (tB + .2, 950, 560, 1.04),
                   (tbo - .5, 950, 560, 1.04), (tbo + .5, 960, 546, 1.0), (D["setup"], 960, 550, 1.03)]
    return cm

SCENES = dict(hook=s_hook, sting=s_sting, roadmap=s_roadmap, guaranteed=s_guaranteed, expected=s_expected, fees=s_fees, setup=s_setup)
def _cams():
    D = {k: BYKEY[k]["dur"] for k in ORDER}; cm = {}
    c = C("hook"); tm, to, ti, t8, ts = c("on the mortgage"), c("over twenty five"), c("if investing returns"), c("about eight thousand"), c("it's a see saw")
    cm["hook"] = [(0, 960, 480, 1.25), (tm - .4, 960, 485, 1.22), (tm + .4, 960, 520, 1.05), (to + .5, 960, 520, 1.05), (ti + .3, 580, 605, 1.3),
                  (t8 - .2, 580, 605, 1.32), (t8 + .6, 580, 605, 1.4), (ts - .3, 580, 605, 1.4), (ts + .55, 960, 545, 1.0), (D["hook"], 960, 545, 1.035)]
    cm["sting"] = [(0, 960, 540, 1.0), (2.6, 960, 540, 1.07)]
    c = C("roadmap"); tb, tf = c("the bigger question"), c("first what overpaying")
    cm["roadmap"] = [(0, 630, 400, 1.45), (tb - .6, 640, 405, 1.42), (tb + .3, 960, 400, 1.08), (tf - .7, 960, 410, 1.08), (tf + .2, 960, 546, 1.0), (D["roadmap"], 960, 552, 1.035)]
    return cams_full(cm)
RV.SC, RV.BYKEY, RV.TOTAL, RV.AUD, RV.SCENES, RV.CAMS = SC, BYKEY, TOTAL, AUD, SCENES, _cams()
RV.DIRS = [(1, 0), (0, 1), (0, 1), (1, 0), (0, 1), (1, 0), (1, 0)]; RV.BOUND = [s["start"] for s in SC[1:]]

def sfx_events():
    ev = RV.sfx_events(); ev.insert(0, (0.0, "whoosh", 0)); return [e for e in ev if e[1]]
NCH = 16
def render_chunk(j):
    n = round(TOTAL * FPS); n0, n1 = n * j // NCH, n * (j + 1) // NCH; out = os.path.join(SEG, f"c{j:02d}.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-threads", "1", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for f in range(n0, n1): p.stdin.write(RV.frame(f / FPS).tobytes())
    p.stdin.close(); p.wait(); return out
VOL = dict(whoosh=.4, pop=.3, ticks=.28, chime=.42, sting=.9, marker=.38, slide=.3, swish=.34, click=.4, thud=.5)
def mix_audio():
    from collections import Counter
    sd, x = SEG, os.path.join(SRC, "sfx")
    der = {"marker": f"-i {x}/whoosh.mp3 -af atrim=0.08:0.62,asetpts=PTS-STARTPTS,atempo=1.9,highpass=f=2400,lowpass=f=9000,afade=t=in:d=0.03,afade=t=out:st=0.16:d=0.12,volume=1.6",
           "slide": f"-i {x}/whoosh.mp3 -af atempo=0.7,highpass=f=300,lowpass=f=1500,afade=t=in:d=0.08,afade=t=out:st=0.5:d=0.5,volume=1.2",
           "swish": f"-i {x}/whoosh.mp3 -af atrim=0.05:0.5,asetpts=PTS-STARTPTS,atempo=1.4,highpass=f=900,lowpass=f=6500,afade=t=in:d=0.04,afade=t=out:st=0.2:d=0.12",
           "click": f"-i {x}/pop.mp3 -af aresample=48000,asetrate=76800,aresample=48000,atrim=0:0.09,highpass=f=1800,afade=t=out:st=0.04:d=0.05,volume=0.9",
           "thud": f"-i {x}/pop.mp3 -af aresample=48000,asetrate=26400,aresample=48000,lowpass=f=700,afade=t=out:st=0.18:d=0.15,volume=1.6"}
    for nm, a in der.items(): subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error"] + a.split() + [f"{sd}/{nm}.wav"])
    src = lambda nm: f"{sd}/{nm}.wav" if nm in der else f"{x}/{nm}.mp3"
    open(f"{sd}/list.txt", "w").write("".join(f"file '{sd}/c{j:02d}.mp4'\n" for j in range(NCH))); silent = f"{sd}/silent.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{sd}/list.txt", "-c", "copy", silent])
    ev = sfx_events(); ins, filt, lab = [], [], []
    for j, (tt, nm, dd) in enumerate(ev):
        ins += ["-i", src(nm)]; ms = int(max(0, tt) * 1000)
        trim = f"atrim=0:{dd:.2f},afade=t=out:st={max(0, dd - .15):.2f}:d=0.15," if nm == "ticks" else ""
        filt.append(f"[{j}:a]{trim}aformat=sample_rates=48000:channel_layouts=stereo,adelay={ms}|{ms},volume={VOL[nm]}[s{j}]"); lab.append(f"[s{j}]")
    filt.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0,apad=whole_dur={TOTAL:.2f}[out]")
    sfxw = f"{sd}/sfx_track.wav"; open(f"{sd}/sfx_filter.txt", "w").write(";".join(filt))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex_script", f"{sd}/sfx_filter.txt", "-map", "[out]", "-t", f"{TOTAL:.2f}", sfxw])
    ins, filt, lab = [], [], []
    for i, k in enumerate(KEYS):
        ins += ["-i", os.path.join(MIX, "audio", f"{i+1:02d}.mp3")]; ms = int(BYKEY[k]["speech"] * 1000)
        filt.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]"); lab.append(f"[a{i}]")
    nv = len(KEYS); ins += ["-i", silent, "-stream_loop", "-1", "-i", f"{x}/music.mp3", "-i", sfxw]; vi, mi, si = nv, nv + 1, nv + 2
    filt.append("".join(lab) + f"amix=inputs={nv}:normalize=0,apad=whole_dur={TOTAL:.2f},asplit=2[v1][v2]")
    filt.append(f"[{mi}:a]atrim=0:{TOTAL:.2f},asetpts=PTS-STARTPTS,volume=0.12,afade=t=in:d=2,afade=t=out:st={TOTAL-1.5:.2f}:d=1.5[mus]")
    filt.append("[mus][v2]sidechaincompress=threshold=0.02:ratio=10:attack=30:release=600[duck]")
    filt.append(f"[v1][duck][{si}:a]amix=inputs=3:normalize=0,loudnorm=I=-16:TP=-2:LRA=7,apad=whole_dur={TOTAL:.2f}[aout]")
    out = os.path.join(OUTD, "v5c_full_draft.mp4")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(filt), "-map", f"{vi}:v", "-map", "[aout]",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{TOTAL:.2f}", "-movflags", "+faststart", out])
    cnt = Counter(e[1] for e in ev)
    json.dump({"sfx": len(ev), "by_type": cnt, "events": [(round(t, 2), n) for t, n, _ in ev]}, open(os.path.join(SEG, "sfx.json"), "w"))
    print("master", round(TOTAL, 2), "s,", len(ev), "sound effects", dict(cnt))

def sheet(ts, path, w=640):
    h = w * 9 // 16; ims = [Image.fromarray(RV.frame(t)).resize((w, h), Image.LANCZOS) for t in ts]
    sh = Image.new("RGB", (2 * w, h * ((len(ims) + 1) // 2))); [sh.paste(im, ((j % 2) * w, (j // 2) * h)) for j, im in enumerate(ims)]; sh.save(path)
def cues():
    h, r = C("hook"), C("roadmap"); R0 = BYKEY["roadmap"]["start"]
    names = {"£100 slides on": h("a spare hundred") + .2, "split to mortgage": h("on the mortgage"), "split to investments": h("into investments"),
             "tokens fly to sheet": h("over twenty five"), "tokens re-form into pots": h("six per cent") + .4, "£8,668 + highlight": h("about eight thousand"),
             "pots morph to 4%": h("at four per cent") + .3, "£7,082 + highlight": h("by about seven"), "see-saw": h("it's a see saw"), "?% ": h("one number decides") + .5,
             "balance lines draw": R0 + r("last time") + .4, "orange line (−£100)": R0 + r("one hundred pounds") + .3, "month 258 / 3½ yrs": R0 + r("our example mortgage") + 1.25,
             "headline": R0 + r("the bigger question"), "step 1": R0 + r("first what overpaying"), "step 4": R0 + r("then we'll race"), "not advice": R0 + r("not advice")}
    print(json.dumps({k: round(v, 2) for k, v in names.items()}, indent=0)); return names

if __name__ == "__main__":
    mode = (sys.argv[1:] or ["preview"])[0]
    if mode == "preview": sheet([float(a) for a in sys.argv[2:]], os.path.join(SEG, "preview.png"))
    elif mode == "check": sys.exit(0 if RV.fit_check() else 1)
    elif mode == "render":
        from multiprocessing import Pool
        t0 = time.time(); vlib.tile2()
        with Pool(2) as p: p.map(render_chunk, range(NCH), chunksize=1)
        open(os.path.join(SEG, "render_time.txt"), "w").write(str(round(time.time() - t0))); print("render seconds", round(time.time() - t0))
    elif mode == "mix": mix_audio()
    elif mode == "sheet": sheet([float(a) for a in sys.argv[2:]], os.path.join(OUTD, "contact_sheet_full.png"))
    elif mode == "cues": cues()
