"""Figures Forward Ep04 opening, TEST 5b: test 4's paper-collage craft applied to the ep4_mix (Fable) storyboard.
python3 build.py preview t.. | check | render | mix | sheet | sfx"""
import os, sys, types, json, math, subprocess, time
from functools import lru_cache
sys.dont_write_bytecode = True                     # never write into the library folder
OUT = os.path.dirname(os.path.abspath(__file__)); SP = os.path.dirname(OUT)
VOX = os.path.join(SP, "ep4_vox"); MIX = os.path.join(SP, "ep4_mix"); SEG = os.path.join(OUT, "seg")
sys.path.insert(0, VOX)
sys.modules["vscenes"] = types.SimpleNamespace(SCENES={}, CAMS={}, _wordmark=None)   # test 4's scenes are NOT loaded
import vlib, render_vox as RV
from vlib import (W, H, FPS, S, INK, PAPER, CARD, KRAFT, ORANGE, BLUE, GREEN, MUTED, LIGHT, CREAM, HLC, LEAD, clamp, ease, eout, back,
                  mix, X, pw, F, tw, T, hl, kline, stroke, ring, arrow, underline, panel, strip, cut, tag, count, appear, panel_sprite,
                  navy_sheet, deco, gbp, PAD, wrap, paste)
from PIL import Image
import numpy as np

# ---------------- re-point the library at this episode's audio, script, timeline and icons ----------------
KEYS = ["hook", "roadmap", "guaranteed", "expected", "fees", "setup"]
os.makedirs(SEG, exist_ok=True)
def probe():
    p = os.path.join(SEG, "probe.json")
    if os.path.exists(p): return json.load(open(p))
    import re; out = {}
    for i, k in enumerate(KEYS):
        f = os.path.join(MIX, "build", "audio", f"{i+1:02d}.mp3")
        d = float(vlib._run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).stdout)
        e = vlib._run(["ffmpeg", "-hide_banner", "-i", f, "-af", "silencedetect=noise=-38dB:d=0.18", "-f", "null", "-"]).stderr
        st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", e)]; en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", e)]
        out[k] = dict(dur=d, sil=list(zip(st, en + [d] * (len(st) - len(en)))))
    json.dump(out, open(p, "w")); return out
vlib.KEYS = KEYS; vlib.PROBE = probe(); AUD = vlib.AUD = {k: vlib.PROBE[k]["dur"] for k in KEYS}
vlib.SCRIPT = dict(l.strip().split("|", 1) for l in open(os.path.join(MIX, "script.txt")) if "|" in l)
vlib.ALIGN = {k: vlib._align(k) for k in KEYS}
TL = json.load(open(os.path.join(MIX, "build", "timeline.json")))
ORDER = ["hook", "sting", "roadmap", "guaranteed", "expected", "fees", "setup"]; TOTAL = TL["TOTAL"]; SC = []
for j, k in enumerate(ORDER):
    st = TL[k]; en = TL[ORDER[j + 1]] if j + 1 < len(ORDER) else TOTAL
    SC.append(dict(k=k, start=st, dur=en - st, speech=None if k == "sting" else st + LEAD))
    if k != "sting": assert abs(en - st - (LEAD + AUD[k] + 1.2)) < .02, k          # same timing as the voiced timeline
BYKEY = {s["k"]: s for s in SC}
@lru_cache(maxsize=None)
def _asset(name):
    for dd in (os.path.join(VOX, "assets"), os.path.join(SP, "ep3", "assets")):
        p = os.path.join(dd, name + ".png")
        if os.path.exists(p): return Image.open(p).convert("RGBA")
    raise FileNotFoundError(name)
vlib._asset = _asset

# ---------------- figures (asserted; same values as ep4_mix/figures_check.py) ----------------
A4, B4, A6, B6, B7 = vlib.A[.04], vlib.B[.04], vlib.A[.06], vlib.B[.06], vlib.B[.07]
assert B6 - A6 == 8668 and A4 - B4 == 7082 and B7 - B6 == 11708 and (B7, B6) == (81007, 69299) and vlib.PAY == 1169.18
assert vlib.END_A == 258 and vlib.FREED == 1269.18 and vlib.SAVED == 24505

# ---------------- test 4 craft helpers ----------------
BROWN = (88, 66, 36)
def big(d, lt, x, y, s, size, t0, hk=None, f="a", fill=INK, on=PAPER, anchor="l", ref=None):
    """Large figure with an optional highlighter swipe behind it (test 4). Returns its right edge."""
    a = ease((lt - t0) / .25); fo = F(f, size); w = fo.getlength(ref or s) / S
    x0 = x - (w if anchor == "r" else w / 2 if anchor == "m" else 0)
    if hk: ph = appear(lt, t0 + .3, .45, "marker")
    if a <= .03: return x0 + w
    bb = fo.getbbox("H0"); top, bot = bb[1] / S, bb[3] / S
    if hk: hl(d, x0, y + top + (bot - top) * .06, x0 + w, y + bot + (bot - top) * .1, mix(on, HLC[hk], .95), ph)
    T(d, x0, y, s, size, f, fill, "la", a, on); return x0 + w
def note(d, lt, x, y, s, size, t0, fill=INK, on=PAPER, anchor="la", f="c"):
    T(d, x, y, s, size, f, fill, anchor, ease((lt - t0) / .3), on, dy=10 * (1 - eout((lt - t0) / .3)))
def fa(lt, t0, d=.3): return ease((lt - t0) / d)
def C(k): return lambda ph, n=1: vlib.Wt(k, ph, n)
def _rec(kind, b):
    if vlib.FIT is not None: vlib.FIT.append((kind, tuple(b), ""))
def chime(lt, t0): appear(lt, t0, .4, "chime")
@lru_cache(maxsize=512)
def _plank(q, length): return panel_sprite(int(length * S), int(24 * S), INK, 2).rotate(-q / 20, Image.BICUBIC, expand=True)

# ================= 1 hook =================
def s_hook(base, d, lt, L, cam):
    c = C("hook")
    t_got, t_sp, t_mo, t_mort, t_inv, t_over = c("you've got"), c("a spare hundred"), c("pounds a month"), c("on the mortgage"), c("into investments"), c("over twenty five")
    t_if, t_87, t_4, t_7k, t_see, t_one, t_know = c("if investing returns"), c("about eight thousand"), c("at four per cent"), c("by about seven"), c("it's a see saw"), c("one number decides"), c("you already know")
    deco(base, cam, "blobO", 330, 560, .3); deco(base, cam, "blobB", 1600, 560, .3); deco(base, cam, "dots", 1720, 930, .15); deco(base, cam, "dots", 170, 200, .15)
    kline(d, lt, 960, 150, [("YOU'VE GOT", t_got, INK, None), ("£100", t_sp + .35, INK, "o"), ("SPARE A MONTH", t_mo, INK, None)], 92, "a", "m")
    cut(base, lt, "hand", 960, 500, 300, .45, rot=-3, duo=False, t1=t_over - .3)
    # the see-saw: a paper plank on a kraft fulcrum; the two choices ride its ends
    deg = pw(lt, [(t_if, 0), (t_if + .8, 7), (t_4, 7), (t_4 + .8, -7), (t_see, -7), (t_see + .7, 0)])
    if lt > t_see + .7: deg += 2 * math.sin(2 * math.pi * (lt - t_see - .7) / 2.4) * clamp((lt - t_see - .7) / .6)
    for t0 in (t_if, t_4, t_see): appear(lt, t0, .8, "slide")
    th = math.radians(deg); px, py = 960, 700; s_ = appear(lt, t_over, .6, "slide")
    if s_ > .02:
        paste(base, panel_sprite(int(180 * S), int(96 * S), KRAFT, 4), X(px - 90) - PAD, X(py + 14) - PAD, s_)
        d.polygon([(X(px), X(py + 16)), (X(px + 50), X(py + 104)), (X(px - 50), X(py + 104))], fill=mix(KRAFT, INK, s_))
        pl = _plank(int(round(deg * 20)), 940); paste(base, pl, X(px) - pl.size[0] / 2, X(py) - pl.size[1] / 2 + 20 * (1 - s_) * S, s_)
    def on_plank(a_, off): return (px + a_ * math.cos(th) + off * math.sin(th), py + a_ * math.sin(th) - off * math.cos(th))
    hx, hy = on_plank(-440, 112); cx_, cy_ = on_plank(440, 112)
    cut(base, lt, "house", hx, hy, 160, t_mort, rot=-5, disc=("o", 95))
    cut(base, lt, "chart", cx_, cy_, 150, t_inv, rot=4, disc=("b", 95))
    tag(base, lt, 450, 340, "THE MORTGAGE?", 44, t_mort + .35, ORANGE, INK, -3)
    tag(base, lt, 1470, 340, "OR INVESTMENTS?", 44, t_inv + .3, BLUE, CARD, 3)
    # the two outcomes
    for x0, t0, tn, head, v, hk, word in ((1160, t_87 - .9, t_87, "AT 6% AFTER FEES, INVESTING ENDS", B6 - A6, "b", "AHEAD"),
                                          (110, t_4 + .2, t_7k, "AT 4%, OVERPAYING WINS BY", A4 - B4, "o", "")):
        panel(base, lt, (x0, 800, x0 + 650, 985), t0 - .15, seed=x0)
        kline(d, lt, x0 + 34, 816, [(head, t0 + .2, MUTED, None)], 34, "o", on=CARD, step=.09)
        xe = big(d, lt, x0 + 34, 856, gbp(count(v, lt, tn, .9)), 92, tn, hk, on=CARD, ref=gbp(v))
        if word: T(d, xe + 26, 882, word, 60, "o", INK, a=ease((lt - tn - .9) / .25), on=CARD)
    note(d, lt, 960, 262, "one number decides which way it tips", 50, t_one, anchor="ma")
    tag(base, lt, 960, 500, "?%", 150, t_one + .3, CARD, INK, -2, "a", "chime", (34, 22))
    ring(d, (800, 405, 1120, 595), appear(lt, t_one + .9, .5, "marker"), ORANGE, 6)
    note(d, lt, 960, 606, "you already know it", 46, t_know, MUTED, anchor="ma")

def s_sting(base, d, lt, L, cam):
    base.paste(navy_sheet(), (0, 0)); _rec("c", (-160, -160, W + 160, H + 160))
    mark = _scaled("mark_gradient_on-dark", 260); wd = int(mark.size[0] * ease(lt / .6))
    if wd > 2: cc = mark.crop((0, 0, wd, mark.size[1])); base.paste(cc, (int(X(960) - mark.size[0] / 2), int(X(290))), cc)
    b = ease((lt - .6) / .6); wm = _wordmark(92); paste(base, wm, X(960) - wm.size[0] / 2, X(628 - 30 * (1 - b)), b)
    T(d, 960, 790, "Where your money is heading, drawn out.", 40, "r", LIGHT, "ma", ease((lt - 1.2) / .6), INK)
@lru_cache(maxsize=None)
def _scaled(name, h):
    im = _asset(name); hh = int(h * S); return im.resize((int(im.size[0] * hh / im.size[1]), hh), Image.LANCZOS)
@lru_cache(maxsize=None)
def _wordmark(h):
    im = _asset("lockup_horizontal_on-dark").crop((1340, 0, 3938, 800)); im = im.crop(im.getbbox()); hh = int(h * S)
    return im.resize((int(im.size[0] * hh / im.size[1]), hh), Image.LANCZOS)

# ================= 3 roadmap =================
def s_roadmap(base, d, lt, L, cam):
    c = C("roadmap")
    t_last, t_100, t_ex, t_big, t_best = c("last time"), c("one hundred pounds"), c("our example mortgage"), c("the bigger question"), c("is that the best")
    deco(base, cam, "blobO", 260, 380, .3); deco(base, cam, "blobB", 1650, 330, .3); deco(base, cam, "dots", 1740, 980, .15)
    kline(d, lt, 110, 150, [("THE BIGGER QUESTION:", t_big, INK, None), ("OVERPAY", t_big + 1.0, INK, "o"), ("OR INVEST?", t_big + 1.4, INK, "b")], 88, "a")
    panel(base, lt, (110, 290, 1150, 510), .15, KRAFT, seed=8, frm=(-60, 0))
    cut(base, lt, "house", 230, 400, 150, t_last + .1, rot=-4, disc=("o", 92))
    T(d, 372, 306, "LAST TIME", 34, "o", BROWN, a=fa(lt, t_last + .2), on=KRAFT)
    kline(d, lt, 372, 344, [("+£100 A MONTH", t_100, INK, "o"), ("OVERPAID", t_100 + 1.0, INK, None)], 64, "a", on=KRAFT, step=.12)
    note(d, lt, 372, 438, "cleared our example mortgage 3½ years early", 44, t_ex, on=KRAFT)
    note(d, lt, 1215, 300, "is that the best", 60, t_best); note(d, lt, 1215, 366, "home for the money?", 60, t_best + .8)
    underline(d, 1215, 1215 + tw("home for the money?", 60, "c"), 440, appear(lt, t_best + 1.6, .5, "marker"), BLUE)
    steps = [("first what overpaying", "lock", "WHAT OVERPAYING", "REALLY EARNS", "o"), ("then what investing", "chart", "WHAT INVESTING", "CAN EARN", "b"),
             ("and what fees", "tap", "WHAT FEES AND TAX", "TAKE OFF THE TOP", "k"), ("then we'll race", "calculator", "THE RACE:", "25 YEARS, HEAD TO HEAD", "g")]
    for i, (cue, ic, l1, l2, dc) in enumerate(steps):
        t0 = c(cue); x0 = 110 + i * 430
        panel(base, lt, (x0, 550, x0 + 400, 930), t0 - .1, seed=i + 3)
        T(d, x0 + 30, 560, str(i + 1), 70, "a", ORANGE, a=ease((lt - t0 - .15) / .25), on=CARD)
        cut(base, lt, ic, x0 + 215, 680, 140, t0 + .2, rot=(-4, 3, -3, 4)[i], disc=(dc, 88))
        kline(d, lt, x0 + 200, 795, [(l1, t0 + .4, INK, None)], 38, "o", "m", CARD); kline(d, lt, x0 + 200, 847, [(l2, t0 + .65, INK, None)], 38, "o", "m", CARD)
    t_s = c("this is a simple"); s = "a simple example, not advice. There's no single right answer."
    note(d, lt, 110, 952, s, 46, t_s)
    x0 = 110 + tw("a simple example, ", 46, "c"); underline(d, x0, x0 + tw("not advice.", 46, "c"), 1010, appear(lt, c("not advice") + .4, .45, "marker"), ORANGE)

# ================= 4 guaranteed =================
def s_guaranteed(base, d, lt, L, cam):
    c = C("guaranteed")
    t_here, t_200, t_25, t_5, t_pay = c("here's the mortgage"), c("two hundred thousand"), c("over twenty five"), c("at five per cent"), c("one thousand one hundred")
    t_every, t_costs, t_so, t_stops, t_off, t_five, t_never = c("every pound you still"), c("costs you five"), c("so every pound"), c("stops costing"), c("pay off an extra"), c("about five pounds"), c("interest you never")
    t_think, t_acc, t_paying, t_g, t_bank, t_nf, t_nt, t_nb = c("think of overpaying"), c("a savings account"), c("paying a guaranteed"), c("guaranteed five"), c("from a bank"), c("no fees"), c("no tax"), c("no bad years")
    deco(base, cam, "blobO", 240, 470, .3); deco(base, cam, "dots", 1700, 330, .15); deco(base, cam, "blobK", 1600, 760, .25)
    kline(d, lt, 110, 150, [("WHAT", .25, INK, None), ("OVERPAYING", .5, INK, "o"), ("REALLY EARNS", .9, INK, None)], 88, "a")
    cut(base, lt, "house", 215, 385, 170, t_here + .1, rot=-5, disc=("o", 105))
    tag(base, lt, 530, 330, "£200,000", 64, t_200, CARD, INK, -2, "a")
    tag(base, lt, 840, 336, "25 YEARS", 64, t_25, CARD, INK, 2, "a")
    tag(base, lt, 1080, 330, "5%", 64, t_5, ORANGE, INK, -1.5, "a")
    note(d, lt, 1220, 300, "the same mortgage as", 44, t_here + .6, MUTED); note(d, lt, 1220, 350, "Episodes 01 and 03", 44, t_here + 1.2, MUTED)
    xe = big(d, lt, 380, 398, gbp(count(vlib.PAY, lt, t_pay, .8), 2), 100, t_pay, "o", ref="£1,169.18")
    T(d, xe + 24, 430, "A MONTH", 50, "o", INK, a=fa(lt, t_pay + .9))
    # every pound owed costs 5%
    cut(base, lt, "coins", 215, 650, 160, t_every, rot=-5, disc=("o", 100))
    kline(d, lt, 372, 556, [("Every £1 you", t_every + .1, INK, None), ("still owe", t_every + .6, INK, None)], 40, "b", step=.16)
    kline(d, lt, 372, 608, [("costs you", t_costs, INK, None), ("5%", t_costs + .5, INK, "o"), ("a year", t_costs + .9, INK, None)], 40, "b", step=.16)
    note(d, lt, 372, 672, "so every £1 you overpay", 50, t_so); note(d, lt, 372, 726, "stops costing you that", 50, t_stops)
    underline(d, 372, 372 + tw("stops costing you that", 50, "c"), 790, appear(lt, t_stops + 1.0, .5, "marker"), ORANGE)
    # the payoff on an extra £100
    panel(base, lt, (110, 812, 900, 985), t_off - .2, INK, seed=5)
    kline(d, lt, 144, 828, [("PAY OFF AN EXTRA £100", t_off + .1, ORANGE, None)], 32, "o", on=INK, step=.1)
    if lt > t_five: T(d, 144, 852, gbp(count(5, lt, t_five, .5)), 90, "a", CARD, on=INK)
    else: count(5, lt, t_five, .5)
    chime(lt, t_five + .5)
    T(d, 290, 872, "OF INTEREST YOU NEVER PAY,", 34, "o", CARD, a=fa(lt, t_never), on=INK)
    T(d, 290, 918, "EVERY YEAR", 34, "o", GREEN, a=fa(lt, t_never + .8), on=INK)
    # the bank that can't say no
    panel(base, lt, (960, 550, 1812, 990), t_think - .25, KRAFT, seed=8, frm=(60, 0))
    cut(base, lt, "bank", 1085, 690, 180, t_think + .1, rot=-3, disc=("w", 110))
    T(d, 1232, 570, "THINK OF IT AS", 30, "o", BROWN, a=fa(lt, t_think + .1), on=KRAFT)
    kline(d, lt, 1232, 612, [("a savings account", t_acc, INK, None)], 40, "b", on=KRAFT, step=.2)
    kline(d, lt, 1232, 664, [("paying a", t_paying, INK, None), ("guaranteed", t_g - .2, INK, None)], 40, "b", on=KRAFT, step=.2)
    big(d, lt, 1232, 704, "5%", 100, t_g + .3, "o", on=KRAFT)
    tag(base, lt, 1570, 772, "GUARANTEED", 48, t_g + .7, GREEN, INK, -5, sfx="chime")
    note(d, lt, 1000, 848, "from a bank that can't say no", 50, t_bank, on=KRAFT)
    x0 = 1000 + tw("from a bank that ", 50, "c"); ring(d, (x0 - 16, 846, x0 + tw("can't say no", 50, "c") + 16, 914), appear(lt, t_bank + 1.4, .5, "marker"), INK, 5)
    for t0, s, x, r in ((t_nf, "NO FEES", 1100, -3), (t_nt, "NO TAX", 1310, 2), (t_nb, "NO BAD YEARS", 1560, -2)):
        tag(base, lt, x, 948, s, 34, t0, GREEN, INK, r)

# ================= 5 expected =================
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
    # the balance scale: a solid block against one that won't sit still
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
            if i == 0: tag(base, lt, ex, py - 62, "5%", 78, t_solid, ORANGE, INK, 0, "a", "pop", (34, 16))
            else:
                jit = 4 * math.sin(2 * math.pi * lt / .45) * rb
                tag(base, lt, ex + jit, py - 62, "?%", 78, t_other + .3, BLUE, CARD, round(2 * math.sin(5 * lt) * rb), "a", "pop", (34, 16))
        T(d, cx - half, 690, "OVERPAYING", 40, "o", INK, "ma", ease((lt - t_solid) / .3)); T(d, cx - half, 746, "a solid block: guaranteed", 26, "sb", MUTED, "ma", ease((lt - t_g5) / .3))
        T(d, cx + half, 690, "INVESTING", 40, "o", INK, "ma", ease((lt - t_other) / .3)); T(d, cx + half, 746, "a block that won't sit still", 26, "sb", MUTED, "ma", ease((lt - t_still) / .3))
        cut(base, lt, "lock", cx - half, 872, 100, t_g5, rot=-5); cut(base, lt, "chart", cx + half, 872, 100, t_other + .6, rot=5)
    note(d, lt, 1810, 258, "you only find out at the end", 54, t_end, anchor="ra"); chime(lt, t_end + .2)
    underline(d, 1810 - tw("you only find out at the end", 54, "c"), 1810, 326, appear(lt, t_end + 1.0, .5, "marker"), ORANGE)

# ================= 6 fees =================
def s_fees(base, d, lt, L, cam):
    c = C("fees")
    t_isnt, t_fees, t_tap, t_7, t_1, t_6, t_on = c("isn't what you keep"), c("fees come out"), c("like a dripping tap"), c("grow at seven"), c("charges take one"), c("you keep six"), c("on a hundred pounds")
    t_81, t_69, t_12, t_tax, t_unl, t_so, t_ret = c("about eighty one"), c("about sixty nine"), c("nearly twelve thousand"), c("tax can take"), c("unless the money"), c("so the number"), c("the return after")
    deco(base, cam, "blobB", 260, 420, .3); deco(base, cam, "dots", 1100, 300, .15); deco(base, cam, "blobO", 1500, 760, .25)
    kline(d, lt, 110, 150, [("THE HEADLINE RETURN", .3, INK, None), ("ISN'T WHAT YOU KEEP", t_isnt, INK, "o")], 88, "a")
    # the dripping tap
    cut(base, lt, "tap", 215, 400, 200, t_fees, rot=0, disc=("b", 122), extra=(90, 278, 340, 600))
    if lt > t_tap + .3:
        for n in range(3):
            ph = ((lt - t_tap) * .85 + n / 3) % 1; yy = 507 + 62 * ph * ph; r_ = 7 * (1 - .5 * ph)
            d.ellipse([X(276 - r_), X(yy - r_ * 1.3), X(276 + r_), X(yy + r_ * 1.3)], fill=mix(PAPER, ORANGE, 1 - ph ** 3))
    note(d, lt, 376, 286, "fees come out every year,", 54, t_fees + .2); note(d, lt, 376, 346, "like a dripping tap", 54, t_tap)
    underline(d, 376, 376 + tw("like a dripping tap", 54, "c"), 412, appear(lt, t_tap + 1.0, .5, "marker"), ORANGE)
    # 7% - 1% = 6%
    y = 428; xe = big(d, lt, 376, y, "7%", 110, t_7, None, fill=BLUE); T(d, 376, 560, "GROWTH", 26, "o", MUTED, a=fa(lt, t_7 + .3))
    T(d, xe + 26, y, "−", 110, "a", MUTED, a=fa(lt, t_1)); x1 = xe + 26 + tw("−", 110, "a") + 26
    xe = big(d, lt, x1, y, "1%", 110, t_1 + .1, None, fill=ORANGE); appear(lt, t_1 + .1, .3, "pop"); T(d, x1, 560, "FEES", 26, "o", MUTED, a=fa(lt, t_1 + .4))
    T(d, xe + 26, y, "=", 110, "a", MUTED, a=fa(lt, t_6)); x2 = xe + 26 + tw("=", 110, "a") + 26
    big(d, lt, x2, y, "6%", 110, t_6 + .1, "g"); appear(lt, t_6 + .1, .3, "pop"); T(d, x2, 560, "YOU KEEP", 26, "o", MUTED, a=fa(lt, t_6 + .4))
    ring(d, (x2 - 26, y - 6, x2 + tw("6%", 110, "a") + 26, y + 150), appear(lt, t_ret + .9, .5, "marker"), ORANGE, 6)
    # what the 1% costs over 25 years
    T(d, 110, 612, "£100 A MONTH FOR 25 YEARS", 30, "o", MUTED, a=fa(lt, t_on))
    xr = 300 + 820 * B6 / B7
    for lab, box, v, t0 in (("AT 7%", (300, 656, 1120, 740), B7, t_81), ("AT 6%", (300, 764, xr, 848), B6, t_69)):
        T(d, 110, box[1] + 12, lab, 50, "a", INK, a=fa(lt, t0))
        strip(base, lt, box, t0, (84, 166, 255), .9, 40 + int(box[1]) % 7)
        T(d, box[2] - 22, box[1] + 12, gbp(v), 50, "a", CARD, "ra", fa(lt, t0 + .9), (84, 166, 255))
    strip(base, lt, (xr, 764, 1120, 848), t_12, (255, 158, 66), .5, 47, "pop")
    arrow(d, (1126, 812), (1180, 770), appear(lt, t_12 + .6, .45, "marker"), INK, 5, .3)
    panel(base, lt, (1190, 640, 1812, 860), t_12 + .1, INK, seed=6)
    kline(d, lt, 1224, 656, [("GONE TO FEES", t_12 + .3, ORANGE, None)], 34, "o", on=INK, step=.1)
    if lt > t_12 + .5: T(d, 1224, 702, gbp(count(B7 - B6, lt, t_12 + .5, .9)), 110, "a", CARD, on=INK)
    else: count(B7 - B6, lt, t_12 + .5, .9)
    chime(lt, t_12 + 1.4)
    # tax
    panel(base, lt, (1190, 270, 1812, 580), t_tax - .2, KRAFT, seed=14, frm=(60, 0))
    cut(base, lt, "document", 1290, 362, 110, t_tax + .1, rot=6)
    T(d, 1392, 290, "TAX", 84, "a", INK, a=fa(lt, t_tax, .25), on=KRAFT)
    lines = wrap("can take another slice, unless the money sits in tax-free or tax-relieved accounts where you live.", 28, "sb", 560); seen = 0
    for j, ln in enumerate(lines):
        pre = "unless" not in " ".join(lines[:j + 1])
        t0 = t_tax + .5 + j * .55 if pre else t_unl + (j - seen) * .9
        if pre: seen = j + 1
        T(d, 1222, 456 + j * 38, ln, 28, "sb", INK, a=fa(lt, t0), on=KRAFT, dy=8 * (1 - eout((lt - t0) / .3)))
    kline(d, lt, 110, 905, [("SO COMPARE YOUR MORTGAGE RATE WITH", t_so + .2, INK, None), ("THE RETURN AFTER FEES AND TAX", t_ret, INK, "o")], 56, "a", step=.12)
    chime(lt, t_ret + 1.2)

# ================= 7 setup =================
def s_setup(base, d, lt, L, cam):
    c = C("setup")
    t_fair, t_two, t_sm, t_ss, t_jars, t_A, t_empty, t_258, t_35 = c("a fair race"), c("two people"), c("the same mortgage"), c("the same spare"), c("think of two jars"), c("person a overpays"), c("stays empty"), c("is gone at month"), c("three and a half")
    t_then, t_1269, t_B, t_Bi, t_all, t_same, t_both, t_q, t_whose = c("from then on"), c("one thousand two"), c("person b pays"), c("and drops a hundred"), c("for all three"), c("same money out"), c("both end"), c("the only question"), c("whose jar")
    deco(base, cam, "blobO", 230, 450, .3); deco(base, cam, "blobB", 230, 770, .3); deco(base, cam, "dots", 1700, 620, .15)
    kline(d, lt, 110, 150, [("A FAIR RACE", t_fair, INK, "o")], 88, "a")
    tag(base, lt, 730, 204, "TWO PEOPLE", 38, t_two, CARD, INK, -3); tag(base, lt, 1030, 198, "SAME MORTGAGE", 38, t_sm, CARD, INK, 2); tag(base, lt, 1480, 204, "SAME SPARE £100", 38, t_ss, INK, CARD, -1.5)
    cut(base, lt, "jar", 1650, 436, 200, t_jars + .2, rot=-4); cut(base, lt, "jar", 1650, 756, 200, t_jars + .55, rot=4, flip=True)
    T(d, 1650, 560, "A'S JAR", 30, "o", MUTED, "ma", fa(lt, t_jars + .6)); T(d, 1650, 880, "B'S JAR", 30, "o", MUTED, "ma", fa(lt, t_jars + .9))
    X0, X1 = 330, 1420; xm = X0 + (X1 - X0) * vlib.END_A / 300
    # person A
    cut(base, lt, "personA", 190, 452, 270, t_A - .3, rot=-2, duo=False)
    tag(base, lt, 400, 322, "PERSON A", 40, t_A, ORANGE, INK, -3, sfx=None)
    strip(base, lt, (X0, 398, xm, 462), t_A + .4, (255, 158, 66), 1.4, 41)
    T(d, X0 + 22, 407, "OVERPAYS £100 A MONTH", 32, "o", INK, a=fa(lt, t_A + 1.7), on=(255, 158, 66))
    note(d, lt, 1490, 300, "empty for years...", 40, t_empty, MUTED, anchor="ra")
    note(d, lt, 560, 296, "mortgage gone at month 258,", 44, t_258); note(d, lt, 560, 340, "3½ years early", 44, t_35, (40, 150, 100))
    arrow(d, (850, 372), (xm - 6, 394), appear(lt, t_35 + .6, .45, "marker"), INK, 5, -.25)
    strip(base, lt, (xm + 6, 398, X1, 462), t_then + .4, (84, 166, 255), .7, 42, rec=False)
    T(d, X0, 474, "MONTH 0", 26, "o", MUTED, a=fa(lt, t_A + .6)); T(d, xm, 474, "258", 26, "o", MUTED, "ma", fa(lt, t_258 + .5)); T(d, X1, 474, "300", 26, "o", MUTED, "ma", fa(lt, t_then + 1.0))
    kline(d, lt, X1 + 4, 524, [("THEN ALL", t_then + .5, INK, None), ("£1,269.18", t_1269, INK, "b"), ("A MONTH GOES IN THE JAR", t_1269 + 2.0, INK, None)], 36, "o", "r", step=.2)
    # person B
    cut(base, lt, "personB", 190, 756, 270, t_B - .3, rot=2, duo=False)
    tag(base, lt, 400, 644, "PERSON B", 40, t_B, BLUE, CARD, 3, sfx=None)
    strip(base, lt, (X0, 706, X1, 762), t_B + .4, KRAFT, 1.4, 43)
    T(d, X0 + 22, 715, "PAYS THE MORTGAGE AS NORMAL, ALL 25 YEARS", 28, "o", INK, a=fa(lt, t_B + 1.5), on=KRAFT)
    strip(base, lt, (X0, 776, X1, 840), t_Bi + .2, (84, 166, 255), 1.8, 44)
    T(d, X0 + 22, 785, "£100 A MONTH INTO THE JAR, ALL 300 MONTHS", 32, "o", CARD, a=fa(lt, t_all), on=(84, 166, 255))
    note(d, lt, 1490, 608, "from day one", 40, t_Bi + .6, MUTED, anchor="ra")
    T(d, X0, 852, "MONTH 0", 26, "o", MUTED, a=fa(lt, t_B + .6)); T(d, X1, 852, "300", 26, "o", MUTED, "ma", fa(lt, t_all + .4))
    tag(base, lt, 640, 958, "SAME MONEY OUT, EVERY MONTH", 38, t_same, INK, CARD, -2)
    for yy, sd in ((430, 3), (772, 4)):
        stroke(d, [(1450, yy), (1466, yy + 20), (1500, yy - 26)], appear(lt, t_both + .4 + sd * .05, .35, "marker"), (40, 150, 100), 7, sd, .6)
    kline(d, lt, 950, 920, [("WHOSE JAR IS", t_whose, INK, None), ("FULLER?", t_whose + .5, INK, "o")], 62, "a", step=.2)
    chime(lt, t_whose + 1.0)

SCENES = dict(hook=s_hook, sting=s_sting, roadmap=s_roadmap, guaranteed=s_guaranteed, expected=s_expected, fees=s_fees, setup=s_setup)

# ---------------- camera keyframes (scene time, centre x, centre y, zoom), tied to spoken cues ----------------
def _cams():
    D = {k: BYKEY[k]["dur"] for k in ORDER}; cm = {}
    c = C("hook"); to, t1 = c("over twenty five"), c("one number decides")
    cm["hook"] = [(0, 960, 430, 1.2), (to - .5, 960, 440, 1.17), (to + .6, 960, 540, 1.0), (t1 - .4, 960, 540, 1.0), (t1 + .5, 960, 535, 1.04), (D["hook"], 960, 545, 1.035)]
    cm["sting"] = [(0, 960, 540, 1.0), (2.6, 960, 540, 1.07)]
    c = C("roadmap"); tb, tf = c("the bigger question"), c("first what overpaying")
    cm["roadmap"] = [(0, 640, 400, 1.2), (tb - .7, 650, 405, 1.18), (tb + .2, 960, 400, 1.08), (tf - .7, 960, 410, 1.08), (tf + .2, 960, 546, 1.0), (D["roadmap"], 960, 552, 1.035)]
    c = C("guaranteed"); te, tt, tn = c("every pound you still"), c("think of overpaying"), c("no fees")
    cm["guaranteed"] = [(0, 960, 350, 1.1), (te - .8, 960, 354, 1.09), (te + .3, 960, 560, 1.06), (tt - .6, 960, 562, 1.06), (tt + .3, 960, 546, 1.0),
                        (tn - .8, 960, 548, 1.0), (tn + .2, 975, 560, 1.03), (D["guaranteed"], 960, 552, 1.035)]
    c = C("expected"); tl, tp = c("over long stretches"), c("picture a balance")
    cm["expected"] = [(0, 700, 340, 1.2), (tl - .8, 700, 344, 1.18), (tl + .6, 800, 558, 1.08), (tp - .9, 812, 560, 1.08), (tp + .3, 960, 546, 1.0), (D["expected"], 960, 552, 1.035)]
    c = C("fees"); ton, t12, ttx, tso = c("on a hundred pounds"), c("nearly twelve thousand"), c("tax can take"), c("so the number")
    cm["fees"] = [(0, 900, 400, 1.12), (ton - .9, 905, 404, 1.11), (ton + .2, 960, 560, 1.0), (t12 - .3, 960, 560, 1.0), (t12 + .6, 990, 600, 1.05),
                  (ttx - .6, 990, 590, 1.05), (ttx + .3, 990, 470, 1.06), (tso - .6, 990, 470, 1.06), (tso + .3, 960, 546, 1.0), (D["fees"], 960, 552, 1.035)]
    c = C("setup"); tj, tB, tbo = c("think of two jars"), c("person b pays"), c("both end")
    cm["setup"] = [(0, 860, 380, 1.12), (tj - .6, 870, 384, 1.11), (tj + .3, 960, 470, 1.04), (tB - .9, 960, 480, 1.04), (tB + .2, 950, 560, 1.04),
                   (tbo - .5, 950, 560, 1.04), (tbo + .5, 960, 546, 1.0), (D["setup"], 960, 550, 1.03)]
    return cm
RV.SC, RV.BYKEY, RV.TOTAL, RV.AUD, RV.SCENES, RV.CAMS = SC, BYKEY, TOTAL, AUD, SCENES, _cams()
RV.DIRS = [(1, 0), (1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (1, 0)]; RV.BOUND = [s["start"] for s in SC[1:]]

def sfx_events():
    ev = RV.sfx_events(); ev.insert(0, (0.0, "whoosh", 0)); return ev
NCH = 16
def render_chunk(j):
    n = round(TOTAL * FPS); n0, n1 = n * j // NCH, n * (j + 1) // NCH; out = os.path.join(SEG, f"c{j:02d}.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-threads", "2", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for f in range(n0, n1): p.stdin.write(RV.frame(f / FPS).tobytes())
    p.stdin.close(); p.wait(); return out
def mix_audio():
    """The library's mix (derived marker/slide sounds, ticks cut to count length, ducked music, -16 LUFS), pointed at this build."""
    from collections import Counter
    sd, x = SEG, os.path.join(VOX, "sfx"); VOL = RV.VOL
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{x}/whoosh.mp3", "-af", "atrim=0.08:0.62,asetpts=PTS-STARTPTS,atempo=1.9,highpass=f=2400,lowpass=f=9000,afade=t=in:d=0.03,afade=t=out:st=0.16:d=0.12,volume=1.6", f"{sd}/marker.wav"])
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{x}/whoosh.mp3", "-af", "atempo=0.7,highpass=f=300,lowpass=f=1500,afade=t=in:d=0.08,afade=t=out:st=0.5:d=0.5,volume=1.2", f"{sd}/slide.wav"])
    src = lambda nm: f"{sd}/{nm}.wav" if nm in ("marker", "slide") else f"{x}/{nm}.mp3"
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
        ins += ["-i", os.path.join(MIX, "build", "audio", f"{i+1:02d}.mp3")]; ms = int(BYKEY[k]["speech"] * 1000)
        filt.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]"); lab.append(f"[a{i}]")
    nv = len(KEYS); ins += ["-i", silent, "-stream_loop", "-1", "-i", f"{x}/music.mp3", "-i", sfxw]; vi, mi, si = nv, nv + 1, nv + 2
    filt.append("".join(lab) + f"amix=inputs={nv}:normalize=0,apad=whole_dur={TOTAL:.2f},asplit=2[v1][v2]")
    filt.append(f"[{mi}:a]atrim=0:{TOTAL:.2f},asetpts=PTS-STARTPTS,volume=0.12,afade=t=in:d=2,afade=t=out:st={TOTAL-1.5:.2f}:d=1.5[mus]")
    filt.append("[mus][v2]sidechaincompress=threshold=0.02:ratio=10:attack=30:release=600[duck]")
    filt.append(f"[v1][duck][{si}:a]amix=inputs=3:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=7,volume=0.6dB,apad=whole_dur={TOTAL:.2f}[aout]")
    out = os.path.join(OUT, "ep4_vox_opus2_draft.mp4")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(filt), "-map", f"{vi}:v", "-map", "[aout]",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{TOTAL:.2f}", "-movflags", "+faststart", out])
    cnt = Counter(e[1] for e in ev)
    json.dump({s["k"]: round(s["start"], 2) for s in SC} | {"TOTAL": round(TOTAL, 2), "sfx": len(ev), "sfx_by_type": cnt}, open(os.path.join(SEG, "timeline.json"), "w"), indent=1)
    print("master", round(TOTAL, 1), "s,", len(ev), "sound effects", dict(cnt))

def sheet(ts, path, w=640):
    h = w * 9 // 16; ims = [Image.fromarray(RV.frame(t)).resize((w, h), Image.LANCZOS) for t in ts]
    sh = Image.new("RGB", (2 * w, h * ((len(ims) + 1) // 2))); [sh.paste(im, ((j % 2) * w, (j // 2) * h)) for j, im in enumerate(ims)]; sh.save(path)

if __name__ == "__main__":
    mode = (sys.argv[1:] or ["preview"])[0]
    if mode == "preview": sheet([float(a) for a in sys.argv[2:]], os.path.join(SEG, "preview.png"))
    elif mode == "check": sys.exit(0 if RV.fit_check() else 1)
    elif mode == "render":
        if not RV.fit_check(): sys.exit("fit check failed: fix before rendering")
        from multiprocessing import Pool
        t0 = time.time(); vlib.tile2()
        with Pool(2) as p: p.map(render_chunk, range(NCH), chunksize=1)
        open(os.path.join(SEG, "render_time.txt"), "w").write(str(round(time.time() - t0))); print("render seconds", round(time.time() - t0))
    elif mode == "mix": mix_audio()
    elif mode == "sheet": sheet([s["start"] + s["dur"] - (.6 if s["k"] != "sting" else .55) for s in SC], os.path.join(OUT, "contact_sheet.png"))
    elif mode == "cues":
        for k in KEYS: print(k, [(w, round(t + LEAD, 2)) for w, t in zip(*vlib.ALIGN[k])][:200:6])
    elif mode == "sfx": ev = sfx_events(); from collections import Counter; print(len(ev), Counter(e[1] for e in ev))
