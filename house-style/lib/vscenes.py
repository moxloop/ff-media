"""Scenes (stage coordinates, 1920x1080) and camera keyframes for the paper-collage build."""
from vlib import *

def big(d, lt, x, y, s, size, t0, hk=None, f="a", fill=INK, on=PAPER, anchor="l", ref=None):
    """Large figure with an optional highlighter swipe behind it. Returns its right edge."""
    a = ease((lt - t0) / .25); fo = F(f, size); w = fo.getlength(ref or s) / S
    x0 = x - (w if anchor == "r" else w / 2 if anchor == "m" else 0)
    if hk: ph = appear(lt, t0 + .3, .45, "marker")
    if a <= .03: return x0 + w
    bb = fo.getbbox("H0"); top, bot = bb[1] / S, bb[3] / S
    if hk: hl(d, x0, y + top + (bot - top) * .06, x0 + w, y + bot + (bot - top) * .1, mix(on, HLC[hk], .95), ph)
    T(d, x0, y, s, size, f, fill, "la", a, on); return x0 + w
def note(d, lt, x, y, s, size, t0, fill=INK, on=PAPER, anchor="la", f="c"):
    T(d, x, y, s, size, f, fill, anchor, ease((lt - t0) / .3), on, dy=10 * (1 - eout((lt - t0) / .3)))

# ============ hook ============
def s_hook(base, d, lt, L, cam):
    w = lambda p, n=1: Wt("hook", p, n)
    t_over, t_inv, t_one, t_rate = w("do you overpay"), w("or invest"), w("one number"), w("your mortgage rate")
    t4, t4n, t7, t7n, t_same = w("in our example"), w("about seven thousand"), w("at seven percent"), w("about nineteen"), w("same hundred")
    deco(base, cam, "blobO", 330, 520, .3); deco(base, cam, "blobB", 1600, 480, .3); deco(base, cam, "dots", 1700, 930, .15); deco(base, cam, "dots", 160, 190, .15)
    kline(d, lt, 960, 150, [("YOU HAVE", w("you have"), INK, None), ("£100", w("a hundred"), INK, "o"), ("SPARE EACH MONTH", w("spare"), INK, None)], 92, "a", "m")
    cut(base, lt, "hand", 940, 486, 380, .45, rot=-3, duo=False, t1=t_rate - .5)
    cut(base, lt, "house", 400, 480, 220, t_over, rot=-5, disc=("o", 150))
    tag(base, lt, 400, 728, "OVERPAY THE MORTGAGE", 44, t_over + .35, ORANGE, INK, -3)
    cut(base, lt, "chart", 1520, 480, 210, t_inv, rot=4, disc=("b", 150))
    tag(base, lt, 1520, 728, "OR INVEST IT", 44, t_inv + .3, BLUE, CARD, 3)
    note(d, lt, 960, 262, "one number decides it", 62, t_one, anchor="ma")
    tag(base, lt, 960, 470, "5%", 150, t_rate - .1, INK, CARD, -2, "a", "chime", (34, 22))
    ring(d, (800, 352, 1120, 588), appear(lt, t_rate + .45, .5, "marker"), ORANGE, 6)
    tag(base, lt, 960, 640, "YOUR MORTGAGE RATE", 36, t_rate + .25, CARD, INK, 1.5, sfx=None)
    for x0, t0, tn, head, v, hk in ((110, t4, t4n, "AT 4% RETURNS, OVERPAYING ENDS", AHEAD4, "o"), (1020, t7, t7n, "AT 7% RETURNS, INVESTING ENDS", AHEAD7, "b")):
        panel(base, lt, (x0, 790, x0 + 790, 978), t0 - .15, seed=x0)
        kline(d, lt, x0 + 34, 806, [(head, t0 + .2, MUTED, None)], 34, "o", on=CARD, step=.09)
        xe = big(d, lt, x0 + 34, 846, gbp(count(v, lt, tn, 1.1)), 92, tn, hk, on=CARD, ref=gbp(v))
        T(d, xe + 26, 872, "AHEAD", 60, "o", INK, a=ease((lt - tn - 1.0) / .25), on=CARD)
    note(d, lt, 960, 706, "same £100 a month", 54, t_same, anchor="ma")
    arrow(d, (762, 742), (690, 792), appear(lt, t_same + .4, .45, "marker"), INK, 5, -.25); arrow(d, (1158, 742), (1230, 792), ease((lt - t_same - .5) / .45), INK, 5, .25, 9)

def s_sting(base, d, lt, L, cam):
    base.paste(navy_sheet(), (0, 0)); _rec_card((-BLEED, -BLEED, W + BLEED, H + BLEED))
    mark = _scaled("mark_gradient_on-dark", 260); wd = int(mark.size[0] * ease(lt / .6))
    if wd > 2: c = mark.crop((0, 0, wd, mark.size[1])); base.paste(c, (int(X(960) - mark.size[0] / 2), int(X(290))), c)
    b = ease((lt - .6) / .6); wm = _wordmark(92); paste(base, wm, X(960) - wm.size[0] / 2, X(628 - 30 * (1 - b)), b)
    T(d, 960, 790, "Where your money is heading, drawn out.", 40, "r", LIGHT, "ma", ease((lt - 1.2) / .6), INK)
def _rec_card(b): 
    import vlib
    if vlib.FIT is not None: vlib.FIT.append(("c", b, ""))
@lru_cache(maxsize=None)
def _scaled(name, h):
    im = Image.open(os.path.join(HERE, "assets", name + ".png")).convert("RGBA"); hh = int(h * S)
    return im.resize((int(im.size[0] * hh / im.size[1]), hh), Image.LANCZOS)
@lru_cache(maxsize=None)
def _wordmark(h, s=S):
    im = Image.open(os.path.join(HERE, "assets", "lockup_horizontal_on-dark.png")).convert("RGBA").crop((1340, 0, 3938, 800)); im = im.crop(im.getbbox()); hh = int(h * s)
    return im.resize((int(im.size[0] * hh / im.size[1]), hh), Image.LANCZOS)

# ============ promise ============
def s_promise(base, d, lt, L, cam):
    w = lambda p, n=1: Wt("promise", p, n)
    deco(base, cam, "blobK", 240, 400, .3); deco(base, cam, "dots", 1720, 250, .15); deco(base, cam, "blobO", 1650, 800, .3)
    kline(d, lt, 110, 150, [("A SIMPLE EXAMPLE,", w("a simple example"), INK, None), ("NOT FINANCIAL ADVICE", w("not financial"), INK, "o")], 88, "a")
    t_m = w("we'll use")
    cut(base, lt, "house", 222, 412, 176, t_m, rot=-4, disc=("k", 110))
    tag(base, lt, 610, 372, "£200,000", 96, w("two hundred thousand"), CARD, INK, -2, "a")
    tag(base, lt, 1030, 380, "25 YEARS", 96, w("over twenty"), CARD, INK, 2, "a")
    tag(base, lt, 1440, 372, "5% FIXED", 96, w("at five percent"), ORANGE, INK, -1.5, "a")
    note(d, lt, 420, 478, "the same mortgage as Episodes 01 and 03: £1,169.18 a month", 44, w("at five percent") + .5)
    underline(d, 420, 1300, 532, appear(lt, w("at five percent") + .9, .5, "marker"), ORANGE)
    steps = [("first", "lock", "WHAT OVERPAYING", "REALLY EARNS", "o"), ("then what investing", "chart", "WHAT INVESTING", "MIGHT EARN", "b"),
             ("then what fees", "tap", "WHAT FEES AND TAX", "TAKE OFF", "k"), ("and finally", "scale", "THE TWO GO", "HEAD TO HEAD", "g")]
    for i, (cue, ic, l1, l2, dc) in enumerate(steps):
        t0 = w(cue); x0 = 110 + i * 430
        panel(base, lt, (x0, 580, x0 + 400, 972), t0 - .1, seed=i + 3)
        T(d, x0 + 30, 590, str(i + 1), 70, "a", mix(CARD, ORANGE, 1), a=ease((lt - t0 - .15) / .25), on=CARD)
        cut(base, lt, ic, x0 + 215, 715, 150, t0 + .2, rot=(-4, 3, -3, 4)[i], disc=(dc, 92))
        kline(d, lt, x0 + 200, 838, [(l1, t0 + .4, INK, None)], 38, "o", "m", CARD); kline(d, lt, x0 + 200, 890, [(l2, t0 + .65, INK, None)], 38, "o", "m", CARD)

# ============ guaranteed ============
def s_guaranteed(base, d, lt, L, cam):
    w = lambda p, n=1: Wt("guaranteed", p, n)
    t_every, t_lend, t_ret, t_5, t_g = w("every pound"), w("is a pound the lender"), w("that saved interest"), w("five percent and"), w("guaranteed")
    t_think, t_fix, t_bank, t_last, t_saved, t_early = w("think of it"), w("paying a fixed"), w("from a bank"), w("in the last episode"), w("saved twenty"), w("and cleared")
    deco(base, cam, "blobO", 250, 430, .3); deco(base, cam, "dots", 780, 600, .15); deco(base, cam, "blobK", 1700, 200, .25)
    kline(d, lt, 110, 150, [("WHAT", .25, INK, None), ("OVERPAYING", w("overpaying"), INK, "o"), ("REALLY EARNS", w("overpaying") + .4, INK, None)], 88, "a")
    cut(base, lt, "coins", 215, 405, 185, t_every, rot=-5, disc=("o", 112))
    kline(d, lt, 372, 292, [("Every £1 you pay off", t_every + .1, INK, None)], 38, "b", step=.16)
    kline(d, lt, 372, 344, [("early is £1 the lender", t_every + 1.2, INK, None)], 38, "b", step=.16)
    kline(d, lt, 372, 396, [("can't charge", t_lend + .5, INK, None), ("5%", t_lend + 1.6, INK, "o"), ("on", t_lend + 2.1, INK, None)], 38, "b", step=.2)
    note(d, lt, 372, 462, "saved interest = your return", 52, t_ret)
    underline(d, 372, 830, 524, appear(lt, t_ret + 1.0, .5, "marker"), ORANGE)
    big(d, lt, 118, 540, "5%", 132, t_5, "o")
    tag(base, lt, 560, 628, "GUARANTEED", 56, t_g, GREEN, INK, -5, sfx="chime")
    # the bank that can't say no
    pa = panel(base, lt, (930, 270, 1812, 660), t_think - .25, KRAFT, seed=8, frm=(60, 0))
    cut(base, lt, "bank", 1085, 462, 230, t_think + .1, rot=-3, disc=("w", 135))
    T(d, 1262, 300, "THINK OF IT AS", 32, "o", (88, 66, 36), a=ease((lt - t_think - .1) / .25), on=KRAFT)
    kline(d, lt, 1262, 350, [("a savings account", t_think + .8, INK, None)], 40, "b", on=KRAFT, step=.2)
    kline(d, lt, 1262, 402, [("paying a fixed 5%", t_fix, INK, None)], 40, "b", on=KRAFT, step=.2)
    underline(d, 1262, 1620, 458, appear(lt, t_fix + .8, .4, "marker"), CARD, 6)
    note(d, lt, 1262, 478, "from a bank that", 60, t_bank, on=KRAFT); note(d, lt, 1262, 540, "can't say no", 60, t_bank + .9, on=KRAFT)
    ring(d, (1238, 534, 1570, 622), appear(lt, t_bank + 1.5, .5, "marker"), INK, 5)
    # last episode recap
    panel(base, lt, (110, 712, 1812, 972), t_last - .2, INK, seed=5)
    cut(base, lt, "calendar", 232, 842, 165, t_last + .1, rot=-4)
    kline(d, lt, 370, 732, [("LAST EPISODE: AN EXTRA £100 A MONTH", t_last + .2, ORANGE, None)], 34, "o", on=INK, step=.1)
    if lt > t_saved: T(d, 370, 776, gbp(count(SAVED, lt, t_saved, 1.6)), 100, "a", CARD, on=INK)
    else: count(SAVED, lt, t_saved, 1.6)
    T(d, 372, 916, "of interest saved", 30, "sb", LIGHT, a=ease((lt - t_saved - 1.2) / .3), on=INK)
    T(d, 800, 776, "3½ YEARS", 100, "a", CARD, a=appear(lt, t_early + 1.3, .3, "chime"), on=INK)
    T(d, 802, 916, "early: cleared in month 258", 30, "sb", LIGHT, a=ease((lt - t_early - 1.6) / .3), on=INK)
    # 25-year strip with the last 3.5 years cut off
    x0, x1 = 1290, 1770; xc = x0 + (x1 - x0) * END_A / 300; sp_ = appear(lt, t_early, .8, "slide")
    if sp_ > .01:
        d.rectangle([X(x0), X(826), X(x0 + (xc - x0) * sp_), X(866)], fill=ORANGE)
        cutp = ease((lt - t_early - 1.3) / .5); dy = 30 * cutp
        if sp_ >= 1:
            for xx in range(int(xc) + 8, x1 - 6, 18): d.line([X(xx), X(826), X(min(xx + 9, x1)), X(826)], fill=LIGHT, width=3); d.line([X(xx), X(866), X(min(xx + 9, x1)), X(866)], fill=LIGHT, width=3)
            d.line([X(x1), X(826), X(x1), X(866)], fill=LIGHT, width=3)
            if cutp > 0: d.rectangle([X(xc + 8), X(826 + dy), X(x1), X(866 + dy)], fill=mix(INK, (120, 126, 138), .9 * (1 - .5 * cutp)))
        T(d, x0, 784, "25 YEARS", 28, "o", LIGHT, a=sp_, on=INK); T(d, x0, 884, "MONTH 0", 24, "o", LIGHT, a=sp_, on=INK)
        T(d, xc, 884, "258", 24, "o", ORANGE, "ma", a=ease((lt - t_early - 1.3) / .3), on=INK)

# ============ investing ============
BLUE_PATH = [(0, 0), (.06, .07), (.1, .04), (.16, .16), (.2, .13), (.27, .28), (.31, .24), (.38, .40), (.43, .47), (.47, .42), (.52, .30), (.56, .33), (.6, .24), (.65, .29),
             (.7, .44), (.74, .40), (.8, .58), (.84, .54), (.9, .74), (.94, .70), (1, .86)]
def s_investing(base, d, lt, L, cam):
    w = lambda p, n=1: Wt("investing", p, n)
    t_long, t_exp, t_not, t_climb, t_dip, t_bad = w("over long"), w("an expected"), w("not a promised"), w("the line climbs"), w("but it dips"), w("a bad decade")
    t_scale, t_solid, t_g5, t_other, t_4, t_7 = w("so picture"), w("on one side"), w("a guaranteed five"), w("on the other"), w("maybe four"), w("maybe seven")
    deco(base, cam, "blobB", 1500, 600, .3); deco(base, cam, "dots", 1740, 180, .15); deco(base, cam, "blobK", 150, 950, .25)
    kline(d, lt, 110, 150, [("INVESTING", .3, INK, "b"), ("IS DIFFERENT", .95, INK, None)], 88, "a")
    bx = kline(d, lt, 110, 262, [("an", t_exp - .2, INK, None), ("expected", t_exp, INK, "b"), ("return,", t_exp + .6, INK, None), ("not a", t_not, INK, None), ("promised", t_not + .35, INK, None), ("one", t_not + .9, INK, None)], 40, "b", step=.15)
    stroke(d, [(bx[4][0] - 6, bx[4][1] + 20), (bx[4][2] + 8, bx[4][1] + 12)], appear(lt, t_not + 1.0, .35, "marker"), ORANGE, 6, 4)
    # graph paper
    box = (110, 335, 1000, 938); pa = panel(base, lt, box, t_long - .5, seed=12, kind="c")
    if pa > .02:
        _rec_z(box)
        if pa >= 1:
            for gx in range(150, 990, 40): d.line([X(gx), X(352), X(gx), X(920)], fill=(214, 226, 238) if (gx - 150) % 200 else (188, 206, 226), width=2)
            for gy in range(360, 930, 40): d.line([X(126), X(gy), X(984), X(gy)], fill=(214, 226, 238) if (gy - 360) % 200 else (188, 206, 226), width=2)
            px0, px1, py0, py1 = 170, 950, 850, 430
            d.line([X(px0), X(py0), X(px1), X(py0)], fill=INK, width=4); d.line([X(px0), X(py0), X(px0), X(py1 - 30)], fill=INK, width=4)
            T(d, px1, 866, "TIME", 26, "o", MUTED, "ra", on=CARD); 
            po = appear(lt, t_long - .1, 1.2, "marker"); stroke(d, [(px0, py0 - 20), (px1, py0 - 200)], po, ORANGE, 7, 2, .6)
            pb = pw(lt, [(t_long + .9, 0), (t_climb, .2), (t_dip, .45), (t_bad + .9, .68), (t_scale - .2, 1)]); appear(lt, t_climb, .5, "marker")
            pts = [(px0 + (px1 - px0) * u, py0 - 20 - (py0 - py1 - 20) * v) for u, v in BLUE_PATH]
            stroke(d, pts, pb, BLUE, 7, 6, .9)
            lg = ease((lt - t_long - .9) / .3)
            if lg > .03:
                d.line([X(196), X(398), X(250), X(398)], fill=mix(CARD, ORANGE, lg), width=8); T(d, 266, 380, "Overpaying: steady", 28, "sb", INK, a=lg, on=CARD)
                d.line([X(196), X(442), X(250), X(442)], fill=mix(CARD, BLUE, lg), width=8); T(d, 266, 424, "Investing: bumpy", 28, "sb", INK, a=lg, on=CARD)
            note(d, lt, 700, 772, "a bad decade", 48, t_bad, on=CARD)
            arrow(d, (690, 790), (642, 746), appear(lt, t_bad + .3, .4, "marker"), INK, 5, -.3)
    T(d, 112, 950, "Illustration of one possible path, not a forecast or real data", 24, "r", MUTED, a=ease((lt - t_long - 1.0) / .4))
    # the scale: a solid block against one that wobbles
    cx, by, half, drop = 1420, 470, 240, 178; s_ = appear(lt, t_scale, .5, "slide")
    note(d, lt, cx, 345, "picture a scale", 54, t_scale + .1, anchor="ma")
    if s_ > .02:
        rb = ease((lt - t_other - .9) / .4); th = math.radians(2.2) * math.sin(2.6 * lt) * rb * s_
        col = mix(PAPER, INK, s_)
        d.polygon([(X(cx - 90), X(930)), (X(cx + 90), X(930)), (X(cx + 60), X(900)), (X(cx - 60), X(900))], fill=col); d.rectangle([X(cx - 9), X(by), X(cx + 9), X(902)], fill=col)
        ends = [(cx - half * math.cos(th), by - half * math.sin(th)), (cx + half * math.cos(th), by + half * math.sin(th))]
        d.line([(X(ends[0][0]), X(ends[0][1])), (X(ends[1][0]), X(ends[1][1]))], fill=col, width=int(16 * S)); d.ellipse([X(cx - 22), X(by - 22), X(cx + 22), X(by + 22)], fill=mix(PAPER, ORANGE, s_))
        for i, (ex, ey) in enumerate(ends):
            bxx = cx + (half if i else -half); py = ey + drop
            d.line([X(ex), X(ey), X(bxx - 170), X(py)], fill=col, width=4); d.line([X(ex), X(ey), X(bxx + 170), X(py)], fill=col, width=4)
            d.rounded_rectangle([X(bxx - 180), X(py), X(bxx + 180), X(py + 14)], 8, fill=col)
            if i == 0: tag(base, lt, bxx, py - 62, "5%", 78, t_g5, ORANGE, INK, 0, "a", "chime", (30, 16))
            else:
                wob = 4 * math.sin(7 * lt) * rb; txt_ = "4% – 7%" if lt > t_7 + .9 else "7%?" if lt > t_7 else "4%?" if lt > t_4 else "?%"
                appear(lt, t_4, .3, "pop"); appear(lt, t_7, .3, "pop")
                tag(base, lt, bxx + 3 * math.sin(23 * lt) * rb, py - 62, txt_, 78, t_other + .8, BLUE, CARD, wob, "a", "chime", (30, 16))
        T(d, cx - half, 690, "OVERPAYING", 40, "o", INK, "ma", ease((lt - t_solid) / .3)); T(d, cx - half, 746, "a solid block: guaranteed", 28, "sb", MUTED, "ma", ease((lt - t_solid - .9) / .3))
        T(d, cx + half, 690, "INVESTING", 40, "o", INK, "ma", ease((lt - t_other) / .3)); T(d, cx + half, 746, "a block that wobbles", 28, "sb", MUTED, "ma", ease((lt - t_other - .8) / .3))
        cut(base, lt, "lock", cx - half, 872, 100, t_solid + .3, rot=-5); cut(base, lt, "coins", cx + half, 872, 100, t_other + .3, rot=5)
def _rec_z(b):
    import vlib
    if vlib.FIT is not None: vlib.FIT.append(("z", b, ""))

# ============ fees ============
def s_fees(base, d, lt, L, cam):
    w = lambda p, n=1: Wt("fees", p, n)
    t_fee, t_tax, t_unl, t_tap, t_small = w("fund and platform"), w("and tax can"), w("unless the money"), w("fees are like"), w("small but")
    t_on, t_one, t_turn, t_cost = w("on a hundred"), w("a one percent fee"), w("turns six"), w("and costs")
    deco(base, cam, "blobB", 300, 400, .3); deco(base, cam, "dots", 1130, 560, .15); deco(base, cam, "blobO", 200, 900, .25)
    kline(d, lt, 110, 150, [("FEES AND TAX", .3, INK, None), ("COME OFF FIRST", w("is before costs"), INK, "o")], 88, "a")
    T(d, 112, 272, "QUOTED RETURN", 34, "o", MUTED, a=ease((lt - .5) / .3))
    fe = ease((lt - t_fee - .3) / .6); _rec_z((110, 326, 878, 545))
    for i in range(6):
        g = appear(lt, .6 + i * .12, .3, "pop" if i in (0, 3) else None)
        if g <= .02: continue
        fall = fe if i == 5 else 0; col = (255, 158, 66) if (i == 5 and fall > .3) else (84, 166, 255)
        sp = panel_sprite(int(118 * S), int(100 * S), col, 30 + i)
        if fall: sp = sp.rotate(-9 * fall, Image.BICUBIC, expand=False)
        paste(base, sp, X(110 + i * 128 + 14 * fall) - PAD, X(326 + 104 * fall - 20 * (1 - back(g))) - PAD, min(1, g * 2))
    big(d, lt, 902, 318, "6%", 84, 1.3, None, fill=BLUE)
    note(d, lt, 902, 448, "−1% in fees, every year", 46, t_fee + .7)
    kp = appear(lt, t_turn + .3, .5, "marker")
    stroke(d, [(110, 438), (114, 452), (740, 452), (744, 438)], kp, (40, 150, 100), 6, 8, .8)
    big(d, lt, 112, 462, "5%", 84, t_turn + .5, "g")
    T(d, 250, 500, "what you keep, before any tax", 28, "sb", MUTED, a=ease((lt - t_turn - .9) / .3))
    # tax note
    panel(base, lt, (1290, 262, 1812, 662), t_tax - .2, KRAFT, seed=14, frm=(60, 0))
    cut(base, lt, "globe", 1392, 352, 124, t_tax + .1, rot=6)
    T(d, 1492, 296, "TAX", 84, "a", INK, a=ease((lt - t_tax) / .25), on=KRAFT)
    lines = wrap("can take a share of the growth, unless the money sits in tax-free or tax-relieved accounts where you live.", 30, "sb", 462)
    seen = 0
    for j, ln in enumerate(lines):
        t0 = t_tax + .5 + j * .55 if "unless" not in " ".join(lines[:j + 1]) else t_unl + (j - seen) * .9
        if "unless" not in " ".join(lines[:j + 1]): seen = j + 1
        T(d, 1322, 440 + j * 42, ln, 30, "sb", INK, a=ease((lt - t0) / .3), on=KRAFT, dy=8 * (1 - eout((lt - t0) / .3)))
    # the dripping tap
    cut(base, lt, "tap", 215, 818, 205, t_tap, rot=0, disc=("b", 122), extra=(90, 690, 340, 1000))
    if lt > t_tap + .5:
        for n in range(3):
            ph = ((lt - t_tap) * .85 + n / 3) % 1; yy = 925 + 62 * ph * ph; r_ = 7 * (1 - .5 * ph)
            d.ellipse([X(276 - r_), X(yy - r_ * 1.3), X(276 + r_), X(yy + r_ * 1.3)], fill=mix(PAPER, BLUE, 1 - ph ** 3))
    note(d, lt, 376, 716, "fees are like a dripping tap:", 54, t_tap + .3); note(d, lt, 376, 782, "small, but it never stops", 54, t_small)
    underline(d, 376, 800, 846, appear(lt, t_small + 1.2, .5, "marker"), BLUE)
    # what the 1% costs
    panel(base, lt, (950, 712, 1812, 972), t_on - .2, INK, seed=6)
    kline(d, lt, 984, 732, [("£100 A MONTH FOR 25 YEARS", t_on + .1, ORANGE, None)], 32, "o", on=INK, step=.12)
    for j, (lab, v, t0) in enumerate((("at 6%", B[.06], t_on + 1.6), ("at 5%", B[.05], t_turn + .9))):
        a = ease((lt - t0) / .3); T(d, 984, 800 + j * 78, lab, 30, "sb", LIGHT, a=a, on=INK); T(d, 1090, 784 + j * 78, gbp(v), 56, "a", CARD, a=a, on=INK)
    T(d, 1420, 786, "THE 1% FEE COSTS", 34, "o", CARD, a=ease((lt - t_cost) / .3), on=INK)
    if lt > t_cost + .3: T(d, 1420, 828, gbp(count(FEE_COST, lt, t_cost + .3, 1.3)), 104, "a", ORANGE, on=INK)
    else: count(FEE_COST, lt, t_cost + .3, 1.3)
    appear(lt, t_cost + 1.6, .3, "chime")

# ============ see-saw ============
@lru_cache(maxsize=256)
def _plank(q): return panel_sprite(int(1300 * S), int(28 * S), INK, 2).rotate(-q / 20, Image.BICUBIC, expand=True)
def s_seesaw(base, d, lt, L, cam):
    w = lambda p, n=1: Wt("seesaw", p, n)
    t_put, t_exp, t_see, t_bal, t_above, t_below, t_rem, t_only = w("put your"), w("and your expected"), w("it works like"), w("it balances"), w("above that"), w("below it"), w("and remember"), w("only one side")
    deco(base, cam, "blobO", 420, 640, .3); deco(base, cam, "blobB", 1500, 640, .3); deco(base, cam, "dots", 960, 330, .15)
    kline(d, lt, 110, 150, [("THE ONE NUMBER:", .3, INK, None), ("YOUR MORTGAGE RATE", w("the number that") + .5, INK, "o")], 88, "a")
    r = pw(lt, [(t_above, 5), (t_above + 1.0, 7), (t_below, 7), (t_below + 1.1, 4), (t_rem, 4), (t_rem + .9, 5)])
    for t0 in (t_above, t_below, t_rem): appear(lt, t0, .9, "slide")
    px, py = 960, 800; s_ = appear(lt, t_put - .5, .5, "slide"); deg = (r - 5) * 3.5 + (1 - s_) * -6; th = math.radians(deg)
    if s_ > .02:
        tri = panel_sprite(int(190 * S), int(100 * S), KRAFT, 4)       # fulcrum: a kraft block with a triangle of ink on it
        paste(base, tri, X(px - 95) - PAD, X(py + 14) - PAD, s_)
        d.polygon([(X(px), X(py + 16)), (X(px + 52), X(py + 104)), (X(px - 52), X(py + 104))], fill=mix(KRAFT, INK, s_))
        pl = _plank(int(round(deg * 20))); paste(base, pl, X(px) - pl.size[0] / 2, X(py) - pl.size[1] / 2, s_)
    def on_plank(a_, hgt): return (px + a_ * math.cos(th) + (hgt / 2 + 15) * math.sin(th), py + a_ * math.sin(th) - (hgt / 2 + 15) * math.cos(th))
    rs = f"{r:.1f}%" if abs(r - round(r)) > .04 else f"{round(r)}%"
    lx, ly = on_plank(-430, 196); tag(base, lt, lx, ly, (("MORTGAGE RATE", 34, "o"), ("5%", 112, "a")), 0, t_put, ORANGE, INK, -deg, sfx="pop", pad=(26, 18))
    rx, ry = on_plank(430, 236); tag(base, lt, rx, ry, (("EXPECTED RETURN", 34, "o"), (rs, 112, "a"), ("AFTER FEES AND TAX", 24, "o")), 0, t_exp, BLUE, CARD, -deg, sfx="pop", pad=(26, 18))
    cut(base, lt, "house", 190, 610, 150, t_put + .4, rot=-5, disc=("o", 96)); cut(base, lt, "chart", 1730, 610, 140, t_exp + .4, rot=5, disc=("b", 96))
    note(d, lt, 960, 922, "it balances at 5%", 54, t_bal, anchor="ma"); underline(d, 800, 1120, 984, appear(lt, t_bal + .8, .4, "marker"), ORANGE)
    note(d, lt, 1330, 922, "like a see-saw", 48, t_see + .3, MUTED)
    T(d, 1810, 270, "ABOVE 5%", 40, "o", MUTED, "ra", ease((lt - t_above) / .3))
    kline(d, lt, 1810, 326, [("INVESTING", t_above + .6, INK, "b"), ("EXPECTED AHEAD", t_above + 1.3, INK, None)], 62, "a", "r", step=.3)
    T(d, 110, 270, "BELOW 5%", 40, "o", MUTED, a=ease((lt - t_below) / .3))
    kline(d, lt, 110, 326, [("OVERPAYING", t_below + .7, INK, "o"), ("WINS", t_below + 1.6, INK, None)], 62, "a", step=.3)
    ring(d, (lx - 200, ly - 138, lx + 200, ly + 138), appear(lt, t_only + .4, .6, "marker"), INK, 6)
    note(d, lt, 110, 922, "only this side is guaranteed", 54, t_only)

# ============ setup ============
def s_setup(base, d, lt, L, cam):
    w = lambda p, n=1: Wt("setup", p, n)
    t_two, t_sm, t_ss, t_A, t_258, t_then, t_1269, t_until = w("two people"), w("same mortgage"), w("same spare"), w("person a overpays"), w("their mortgage ends"), w("and from then on"), w("one thousand two"), w("until month")
    t_B, t_Bi, t_all, t_both, t_pot, t_whose, t_dep = w("person b pays"), w("and invests a hundred"), w("for all twenty"), w("both finish"), w("each with a pot"), w("whose is bigger"), w("that depends")
    deco(base, cam, "blobO", 230, 450, .3); deco(base, cam, "blobB", 230, 770, .3); deco(base, cam, "dots", 1700, 620, .15)
    kline(d, lt, 110, 150, [("LET'S TEST IT", .3, INK, "o")], 88, "a")
    tag(base, lt, 730, 204, "TWO PEOPLE", 38, t_two, CARD, INK, -3); tag(base, lt, 1030, 198, "SAME MORTGAGE", 38, t_sm, CARD, INK, 2); tag(base, lt, 1500, 204, "SAME SPARE £100 A MONTH", 38, t_ss, INK, CARD, -1.5)
    X0, X1 = 330, 1420; xm = X0 + (X1 - X0) * END_A / 300
    # person A
    cut(base, lt, "personA", 190, 452, 270, t_A - .3, rot=-2, duo=False)
    tag(base, lt, 400, 322, "PERSON A", 40, t_A, ORANGE, INK, -3, sfx=None)
    p1 = strip(base, lt, (X0, 398, xm, 462), t_A + .5, (255, 158, 66), 1.6, 41)
    T(d, X0 + 22, 407, "OVERPAYS: THE MORTGAGE PAYMENT + £100 A MONTH", 32, "o", INK, a=ease((lt - t_A - 2.0) / .3), on=(255, 158, 66))
    note(d, lt, 730, 300, "mortgage ends in month 258", 48, t_258 + .4)
    arrow(d, (1140, 352), (xm - 4, 392), appear(lt, t_258 + 1.2, .45, "marker"), INK, 5, -.25)
    p2 = strip(base, lt, (xm + 6, 398, X1, 462), t_then + .5, (84, 166, 255), .8, 42, rec=False)
    T(d, X0, 474, "MONTH 0", 26, "o", MUTED, a=ease((lt - t_A - .6) / .3)); T(d, xm, 474, "258", 26, "o", MUTED, "ma", ease((lt - t_258 - .9) / .3)); T(d, X1, 474, "300", 26, "o", MUTED, "ma", ease((lt - t_until - .3) / .3))
    xe = X1 + 4
    kline(d, lt, xe, 524, [("THEN INVESTS", t_then + .9, INK, None), ("£1,269.18", t_1269, INK, "b"), ("A MONTH", t_1269 + 1.9, INK, None)], 40, "o", "r", step=.3)
    # person B
    cut(base, lt, "personB", 190, 756, 270, t_B - .3, rot=2, duo=False)
    tag(base, lt, 400, 644, "PERSON B", 40, t_B, BLUE, CARD, 3, sfx=None)
    strip(base, lt, (X0, 706, X1, 762), t_B + .5, KRAFT, 1.4, 43)
    T(d, X0 + 22, 715, "PAYS THE MORTGAGE AS NORMAL, ALL 25 YEARS", 28, "o", INK, a=ease((lt - t_B - 1.6) / .3), on=KRAFT)
    strip(base, lt, (X0, 776, X1, 840), t_Bi + .2, (84, 166, 255), 1.8, 44)
    T(d, X0 + 22, 785, "INVESTS £100 A MONTH FOR ALL 25 YEARS", 32, "o", CARD, a=ease((lt - t_Bi - 1.8) / .3), on=(84, 166, 255))
    T(d, X0, 852, "MONTH 0", 26, "o", MUTED, a=ease((lt - t_B - .6) / .3)); T(d, X1, 852, "300", 26, "o", MUTED, "ma", ease((lt - t_all - .5) / .3))
    for yy, sd in ((430, 3), (772, 4)):
        stroke(d, [(1450, yy), (1466, yy + 20), (1500, yy - 26)], appear(lt, t_both + .5 + sd * .05, .35, "marker"), (40, 150, 100), 7, sd, .6)
    cut(base, lt, "jar", 1650, 436, 200, t_pot, rot=-4); cut(base, lt, "jar", 1650, 756, 200, t_pot + .35, rot=4, flip=True)
    T(d, 1650, 560, "A'S POT", 30, "o", MUTED, "ma", ease((lt - t_pot - .4) / .3)); T(d, 1650, 880, "B'S POT", 30, "o", MUTED, "ma", ease((lt - t_pot - .7) / .3))
    kline(d, lt, 110, 918, [("WHOSE POT IS BIGGER?", t_whose, INK, None)], 62, "a", step=.2)
    tag(base, lt, 1010, 962, "THAT DEPENDS ON THE RETURN", 44, t_dep + .3, INK, CARD, -2, sfx="chime")

SCENES = dict(hook=s_hook, sting=s_sting, promise=s_promise, guaranteed=s_guaranteed, investing=s_investing, fees=s_fees, seesaw=s_seesaw, setup=s_setup)

# ---------------- camera keyframes: (scene time, centre x, centre y, zoom) ----------------
def _cams():
    c = {}; D = {s["k"]: s["dur"] for s in SC}
    w = lambda p: Wt("hook", p)
    c["hook"] = [(0, 960, 430, 1.2), (w("do you overpay") - .5, 960, 440, 1.17), (w("do you overpay") + .5, 960, 520, 1.0), (w("your mortgage rate") - .6, 960, 520, 1.0),
                 (w("your mortgage rate") + .6, 960, 490, 1.1), (w("in our example") - .6, 960, 492, 1.12), (w("in our example") + .4, 960, 546, 1.0), (D["hook"], 960, 550, 1.035)]
    c["sting"] = [(0, 960, 540, 1.0), (STING, 960, 540, 1.07)]
    w = lambda p: Wt("promise", p)
    c["promise"] = [(0, 810, 340, 1.18), (w("we'll use"), 810, 345, 1.16), (w("over twenty"), 960, 440, 1.06), (w("first") - .7, 960, 450, 1.06), (w("first") + .2, 960, 546, 1.0), (D["promise"], 960, 552, 1.035)]
    w = lambda p: Wt("guaranteed", p)
    c["guaranteed"] = [(0, 650, 400, 1.2), (w("think of it") - 1.0, 650, 410, 1.17), (w("think of it") + .2, 960, 470, 1.06), (w("in the last episode") - .7, 960, 474, 1.07),
                       (w("in the last episode") + .4, 960, 546, 1.0), (D["guaranteed"], 960, 552, 1.035)]
    w = lambda p: Wt("investing", p)
    c["investing"] = [(0, 700, 340, 1.2), (w("over long") - .8, 700, 344, 1.18), (w("over long") + .6, 800, 558, 1.08), (w("so picture") - .9, 812, 560, 1.08),
                      (w("so picture") + .3, 960, 546, 1.0), (D["investing"], 960, 552, 1.035)]
    w = lambda p: Wt("fees", p)
    c["fees"] = [(0, 700, 400, 1.2), (w("and tax can") - 1.0, 700, 404, 1.18), (w("and tax can") + .1, 960, 480, 1.05), (w("fees are like") - .7, 960, 484, 1.06),
                 (w("fees are like") + .3, 960, 546, 1.0), (w("on a hundred"), 960, 546, 1.0), (D["fees"], 985, 556, 1.035)]
    w = lambda p: Wt("seesaw", p)
    c["seesaw"] = [(0, 960, 500, 1.12), (w("it works like") - .4, 960, 506, 1.1), (w("it works like") + .8, 960, 546, 1.03), (w("above that") + .9, 985, 546, 1.04),
                   (w("below it"), 985, 546, 1.04), (w("below it") + 1.0, 936, 546, 1.04), (w("and remember") + .8, 960, 546, 1.0), (D["seesaw"], 960, 550, 1.03)]
    w = lambda p: Wt("setup", p)
    c["setup"] = [(0, 860, 380, 1.12), (w("person a overpays") - .7, 860, 384, 1.11), (w("person a overpays") + .4, 870, 440, 1.1), (w("person b pays") - .9, 880, 444, 1.1),
                  (w("person b pays") + .2, 900, 566, 1.05), (w("both finish") - .5, 905, 566, 1.05), (w("both finish") + .5, 960, 546, 1.0), (D["setup"], 960, 550, 1.03)]
    return c
CAMS = _cams()
