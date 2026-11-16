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
    if a > .02: ruled(d, sb, a, 60); T(d, 1150, 436, "worked example", 28, "c", ORANGE, "ra", fa(lt, t_7), CARD)
    y = 436; x = 420
    xe = big(d, lt, x, y, "7%", 110, t_7, None, fill=BLUE, on=CARD); T(d, x, 562, "GROWTH", 26, "o", MUTED, a=fa(lt, t_7 + .3), on=CARD)
    T(d, xe + 26, y, "−", 110, "a", MUTED, a=fa(lt, t_1), on=CARD); x1 = xe + 26 + tw("−", 110, "a") + 26
    xe = big(d, lt, x1, y, "1%", 110, t_1 + .1, None, fill=ORANGE, on=CARD); appear(lt, t_1 + .1, .3, "click"); T(d, x1, 562, "FEES", 26, "o", MUTED, a=fa(lt, t_1 + .4), on=CARD)
    T(d, xe + 26, y, "=", 110, "a", MUTED, a=fa(lt, t_6), on=CARD); x2 = xe + 26 + tw("=", 110, "a") + 26
    big(d, lt, x2, y, "6%", 110, t_6 + .1, "g", on=CARD); appear(lt, t_6 + .1, .3, "thud"); T(d, x2, 562, "YOU KEEP", 26, "o", MUTED, a=fa(lt, t_6 + .4), on=CARD)
    ring(d, (x2 - 22, y - 2, x2 + tw("6%", 110, "a") + 22, y + 160), appear(lt, t_ret + .9, .5, "marker"), ORANGE, 6)
    # pots drawn as bars; the 7% total re-forms into the 6% total, the gap breaks away as fees
    T(d, 110, 624, "£100 A MONTH FOR 25 YEARS", 30, "o", MUTED, a=fa(lt, t_on))
    xr = 300 + 820 * B6 / B7; B7_ = vlib.B[.07]; assert B7_ - B6 == 11708
    for lab, box, v, t0 in (("AT 7%", (300, 668, 1120, 748), B7_, t_81), ("AT 6%", (300, 772, xr, 852), B6, t_69)):
        T(d, 110, box[1] + 10, lab, 50, "a", INK, a=fa(lt, t0))
        strip(base, lt, box, t0, (84, 166, 255), .9, 40 + int(box[1]) % 7)
        if lt > t0 + .9: T(d, box[2] - 22, box[1] + 10, gbp(count(v, lt, t0 + .9, .6)), 50, "a", CARD, "ra", 1, (84, 166, 255))
        else: count(v, lt, t0 + .9, .6)
    strip(base, lt, (xr, 772, 1120, 852), t_12, (255, 158, 66), .5, 47, "swish")
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
    e = back(clamp((lt - t0) / .5)); w, h = 76 * e, 96 * e
    if drops:
        rate, ts = drops
        if lt > ts:
            for n in range(4):
                ph = ((lt - ts) * rate + n / 4) % 1
                if lt - ts > ph / rate: yy = cy - h - 120 + 120 * ph * ph; d.ellipse([X(cx - 9), X(yy - 9), X(cx + 9), X(yy + 9)], fill=mix(PAPER, BLUE, 1 - ph ** 4))
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
    jar(base, d, lt, 1650, 440, t_jars + .2, lA, (2.2, t_then + .5)); jar(base, d, lt, 1650, 762, t_jars + .55, lB, (.9, t_Bi + .3))
    T(d, 1650, 562, "A'S JAR", 30, "o", MUTED, "ma", fa(lt, t_jars + .6)); T(d, 1650, 884, "B'S JAR", 30, "o", MUTED, "ma", fa(lt, t_jars + .9))
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
    cm["guaranteed"] = [(0, 960, 350, 1.1), (te - .8, 960, 354, 1.09), (te + .3, 960, 560, 1.06), (tf - 1.2, 960, 570, 1.06), (tf - .2, 900, 600, 1.1),
                        (tt - .6, 900, 600, 1.1), (tt + .3, 960, 546, 1.0), (tn - .8, 960, 548, 1.0), (tn + .2, 975, 560, 1.03), (D["guaranteed"], 960, 552, 1.035)]
    c = C("expected"); tl, tp = c("over long stretches"), c("picture a balance")
    cm["expected"] = [(0, 700, 340, 1.2), (tl - .8, 700, 344, 1.18), (tl + .6, 800, 558, 1.08), (tp - .9, 812, 560, 1.08), (tp + .3, 960, 546, 1.0), (D["expected"], 960, 552, 1.035)]
    c = C("fees"); t7, ton, t12, ttx, tso = c("grow at seven"), c("on a hundred pounds"), c("nearly twelve thousand"), c("tax can take"), c("so the number")
    cm["fees"] = [(0, 900, 400, 1.12), (t7 - .5, 905, 404, 1.11), (t7 + .4, 800, 430, 1.16), (ton - .9, 800, 432, 1.16), (ton + .2, 960, 560, 1.0), (t12 - .3, 960, 560, 1.0), (t12 + .6, 990, 600, 1.05),
                  (ttx - .6, 990, 590, 1.05), (ttx + .3, 990, 470, 1.06), (tso - .6, 990, 470, 1.06), (tso + .3, 960, 546, 1.0), (D["fees"], 960, 552, 1.035)]
    c = C("setup"); tj, tB, tbo = c("think of two jars"), c("person b pays"), c("both end")
    cm["setup"] = [(0, 860, 380, 1.12), (tj - .6, 870, 384, 1.11), (tj + .3, 960, 470, 1.04), (tB - .9, 960, 480, 1.04), (tB + .2, 950, 560, 1.04),
                   (tbo - .5, 950, 560, 1.04), (tbo + .5, 960, 546, 1.0), (D["setup"], 960, 550, 1.03)]
    return cm
