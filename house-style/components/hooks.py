"""Hook openers (hook gear: dense and fast, the consequence number on screen inside the first second).

number_transform   a big figure lands, shrinks to a token and re-forms / counts into the consequence number
calc_sheet_zoom    the "Figures Forward calculation" sheet slides in, the camera pushes in on the key line
two_paths          one token splits into an orange path and a blue path, each ending at its figure
myth_vs_reality    a myth card is crossed out by hand, the reality line drops in with the real figure

Every string, figure, colour role and cue time is a parameter; the defaults are round example numbers only.
"""
from kit import *

ROLE = {"o": ORANGE, "b": BLUE, "g": GREEN, "k": INK}
ROLE_FG = {"o": INK, "b": CARD, "g": INK, "k": CARD}


def _fig(d, lt, x, y, s, size, t0, t_hl=None, hk=None, f="a", fill=INK, on=PAPER, anchor="l"):
    """A figure that drops in at t0 with a highlighter swipe at t_hl. Returns its cap box (x0, top, x1, bottom)."""
    fo = F(f, size); w = fo.getlength(s) / S; x0 = x - (w if anchor == "r" else w / 2 if anchor == "m" else 0)
    bb = fo.getbbox("H0"); top, bot = bb[1] / S, bb[3] / S
    if hk and t_hl is not None:
        hl(d, x0, y + top + (bot - top) * .06, x0 + w, y + bot + (bot - top) * .1, mix(on, HLC[hk], .95), appear(lt, t_hl, .45, "marker"))
    u = clamp((lt - t0) / .28)
    if u > 0: T(d, x0, y, s, size, f, fill, "la", min(1, u * 2.2), on, dy=-26 * (1 - back(u)))
    return (x0, y + top, x0 + w, y + bot)


def _bez(p0, c, p1, n=26):
    return [((1 - u) ** 2 * p0[0] + 2 * u * (1 - u) * c[0] + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * u * (1 - u) * c[1] + u * u * p1[1]) for u in [i / n for i in range(n + 1)]]


def _lines(d, lt, x, y, s, size, t0, maxw, fill=INK, on=PAPER, f="c", gap=1.0, anchor="la"):
    """Wrapped handwritten note, line by line."""
    for i, ln in enumerate(wrap(s, size, f, maxw)): note(d, lt, x, y + i * size * gap, ln, size, t0 + i * .12, fill, on, anchor, f)


# ------------------------------------------------------------------ number_transform
@component("hooks", "number_transform", dur=5.5, cam=[(0, 960, 545, 1.25), (.5, 960, 545, 1.25), (1.5, 960, 540, 1.0), (5.5, 960, 540, 1.03)], still=4.7,
           use="Open on a small everyday figure that turns into the big consequence number before the first second is out.")
def number_transform(base, d, lt, cam, start="£100", start_label="A MONTH", start_value=100, result_value=24000,
                     title=("KEEP IT UP FOR", "20 YEARS"), result_label="PAID IN, BEFORE ANY GROWTH", picture="calendar", pic_tag="240 MONTHS",
                     aside="example figures", role="o", fmt=None,
                     t_start=.05, t_shrink=.45, t_result=.82, count=.75, t_swipe=1.8, t_title=2.05, t_pic=2.6, t_label=3.1, t_aside=3.8):
    col = ROLE[role]; fmt = fmt or (lambda v: gbp(round(v))); CX, RY = 960, 600
    deco(base, cam, "blobO" if role == "o" else "blobB" if role == "b" else "blobG", 960, 600, .3); deco(base, cam, "dots", 1720, 930, .15); deco(base, cam, "dots", 170, 880, .15)
    # the everyday figure lands big, then shrinks away into a token
    appear(lt, t_start, .3, "pop"); u = clamp((lt - t_start) / .3); g = clamp((lt - t_shrink) / .17)
    if u > 0 and g < 1:
        T(d, CX, 520, start, 270 * (.6 + .4 * back(u)) * (1 - .62 * ease(g)), "a", col, "mm", min(1, u * 2.5) * (1 - g))
        T(d, CX, 705, start_label, 64, "o", INK, "mm", fa(lt, t_start + .15, .2) * (1 - g))
    tk, tp = (CX, 520), (385, 405)
    token(base, lt, tk, tp, t_shrink + .18, t_shrink + .26, ((start, 96, "a"), (start_label, 36, "o")), col, ROLE_FG[role], -4)
    # the consequence number counts up out of it, then gets the highlighter
    ref = fmt(result_value); w = tw(ref, 250, "a"); fo = F("a", 250); bb = fo.getbbox("H0"); hh = (bb[3] - bb[1]) / S
    hl(d, CX - w / 2, RY - hh / 2 - 2, CX + w / 2, RY + hh / 2 + 16, mix(PAPER, HLC[role], .95), appear(lt, t_swipe, .45, "marker"))
    vmorph(d, lt, CX, RY, [(t_result, start_value, INK), (t_result + .04, result_value, INK)], 250, PAPER, count, "a", "mm", fmt)
    arrow(d, (tp[0] + 95, tp[1] + 92), (CX - w / 2 - 6, RY - hh / 2 - 34), appear(lt, t_result + count + .05, .4, "marker"), col, 6, -.28)
    # context
    if title: kline(d, lt, 110, 150, [(title[0], t_title, INK, None), (title[1], t_title + .25, col if role != "g" else DGREEN, None)], 84, "a")
    if picture: cut(base, lt, picture, 1620, 560, 205, t_pic, rot=5, disc=("k", 125))
    if pic_tag: tag(base, lt, 1620, 775, pic_tag, 40, t_pic + .3, CARD, INK, -2, "o", None)
    T(d, CX, 800, result_label, 50, "o", INK, "mm", fa(lt, t_label), dy=14 * (1 - eout((lt - t_label) / .3)))
    if aside: note(d, lt, CX, 850, aside, 46, t_aside, MUTED, anchor="ma")


# ------------------------------------------------------------------ calc_sheet_zoom
@component("hooks", "calc_sheet_zoom", dur=6.0, cam=[(0, 960, 520, 1.14), (1.2, 960, 540, 1.0), (2.7, 960, 540, 1.0), (3.5, 880, 570, 1.3), (6.0, 880, 570, 1.33)], still=4.6,
           use="Show the working: the calculation sheet with three or four lines, then a push in on the figure that matters as it is spoken.",
           notes="The default camera pushes in on the total line. An episode that highlights another row (key=<row index>) should pass its own camera.")
def calc_sheet_zoom(base, d, lt, cam, heading="FIGURES FORWARD CALCULATION", stamp="worked example", subtitle="£100 a month, every month, for 20 years",
                    rows=(("Paid in each month", "£100"), ("Each year (× 12)", "£1,200"), ("Number of years", "20")),
                    total_label="Paid in altogether", total="£24,000", footer="Example figures, for illustration", key="total", role="o",
                    picture="calculator", aside="we show the working",
                    t_sheet=.1, t_total=.6, t_rows=(1.0, 1.35, 1.7, 2.05), t_rule=2.3, t_pic=1.5, t_swipe=3.6, t_aside=4.4):
    SX0, SY0, SX1, SY1 = 520, 150, 1400, 925; LX, RX = 574, 1352; n = len(rows)
    a = panel(base, lt, (SX0, SY0, SX1, SY1), t_sheet, CARD, seed=21, frm=(-70, 0))
    step = 100 if n <= 4 else 300 / (n - 1); ys = [335 + i * step for i in range(n)]; RULE, TY = 708, 728
    if a > .02:
        for yy in sorted(set([y + 40 for y in ys] + [375 + 100 * j for j in range(4)] + [878])): d.line([X(SX0 + 20), X(yy), X(SX1 - 20), X(yy)], fill=mix(CARD, (200, 220, 240), a * .7), width=2)
        d.line([X(SX0 + 30), X(SY0 + 12), X(SX0 + 30), X(SY1 - 12)], fill=mix(CARD, (255, 190, 170), a), width=2)
        T(d, LX, 180, heading, 34, "o", MUTED, a=fa(lt, t_sheet + .2), on=CARD)
        T(d, RX, 174, stamp, 40, "c", ORANGE, "ra", fa(lt, t_sheet + .3), CARD)
        T(d, LX, 244, subtitle, 27, "sb", INK, a=fa(lt, t_sheet + .35), on=CARD)
        for i, ((lab, val), y) in enumerate(zip(rows, ys)):
            t0 = t_rows[min(i, len(t_rows) - 1)] + max(0, i - len(t_rows) + 1) * .3; hk = role if key == i else None
            if hk: w = tw(val, 52, "o"); hl(d, RX - w, y - 26, RX, y + 30, mix(CARD, HLC[role], .95), appear(lt, t_swipe, .45, "marker"))
            T(d, LX, y, lab, 34, "sb", INK, "lm", fa(lt, t0), CARD)
            T(d, RX, y, val, 52, "o", INK, "rm", fa(lt, t0 + .1), CARD, dy=-10 * (1 - eout((lt - t0 - .1) / .25)))
        stroke(d, [(LX, RULE + 2), ((LX + RX) / 2, RULE - 2), (RX, RULE + 1)], appear(lt, t_rule, .35, "marker"), INK, 4, 9, .8)
        # the total: on the sheet inside the first second, highlighted later as the camera arrives
        T(d, LX, TY + 62, total_label, 54, "c", INK, "lm", fa(lt, t_total), CARD)
        _fig(d, lt, RX, TY, total, 112, t_total + .1, t_swipe if key == "total" else None, role, "a", INK, CARD, "r")
        T(d, LX, 892, footer, 24, "r", MUTED, "lm", fa(lt, t_rule + .3), CARD)
    if key == "total": chime(lt, t_swipe + .35)
    if picture: cut(base, lt, picture, 312, 560, 190, t_pic, rot=-5, disc=("k", 112))
    if aside: _lines(d, lt, 312, 716, aside, 46, t_aside, 230, MUTED, anchor="ma", gap=.95)


# ------------------------------------------------------------------ two_paths
@component("hooks", "two_paths", dur=6.0, cam=[(0, 960, 400, 1.25), (.45, 960, 400, 1.25), (1.3, 960, 540, 1.0), (6.0, 960, 540, 1.03)], still=5.0,
           use="Open a Choice episode: the same money goes down an orange path or a blue path, each ending at its own figure, then the question.",
           notes="left_role / right_role keep the colour meaning: orange = overpay or cost, blue = invest.")
def two_paths(base, d, lt, cam, start="£100", start_label="A MONTH", left_label="PATH ONE", left_fig="£24,000", right_label="PATH TWO", right_fig="£30,000",
              question="?", ask="which path ends ahead?", left_pic="house", right_pic="chart", left_role="o", right_role="b",
              t_start=.08, t_left=.4, t_right=.55, draw=.5, t_left_fig=None, t_right_fig=None, t_pics=1.7, t_question=3.2, t_ask=4.1):
    t_left_fig = t_left + draw if t_left_fig is None else t_left_fig; t_right_fig = t_right + draw if t_right_fig is None else t_right_fig
    deco(base, cam, "blobO" if left_role == "o" else "blobG", 380, 620, .3); deco(base, cam, "blobB" if right_role == "b" else "blobG", 1540, 620, .3)
    TOKY = 250
    for sgn, role, t0, t1, seed in ((-1, left_role, t_left, t_left_fig, 31), (1, right_role, t_right, t_right_fig, 37)):
        col = ROLE[role]; ex = 960 + sgn * 520
        pts = _bez((960 + sgn * 120, TOKY + 10), (960 + sgn * 500, TOKY + 20), (ex, 590), 30)
        p = appear(lt, t0, draw, "marker"); stroke(d, pts, p, col, 13, seed, 1.6)
        if p > .97:
            for s_ in (-1, 1): stroke(d, [(ex, 596), (ex + s_ * 30, 556)], 1, col, 13, seed + 3 + s_, .4)
    tag(base, lt, 960, TOKY, ((start, 96, "a"), (start_label, 36, "o")), 0, t_start, KRAFT, INK, -2, "a", "pop", (26, 16))
    tag(base, lt, 440, 715, ((left_label, 38, "o"), (left_fig, 92, "a")), 0, t_left_fig, ROLE[left_role], ROLE_FG[left_role], -3, "a", "pop", (30, 20))
    tag(base, lt, 1480, 715, ((right_label, 38, "o"), (right_fig, 92, "a")), 0, t_right_fig, ROLE[right_role], ROLE_FG[right_role], 3, "a", "pop", (30, 20))
    if left_pic: cut(base, lt, left_pic, 255, 390, 170, t_pics, rot=-5, disc=(left_role if left_role in "obg" else "k", 104))
    if right_pic: cut(base, lt, right_pic, 1665, 390, 165, t_pics + .2, rot=4, disc=(right_role if right_role in "obg" else "k", 104), sfx=None)
    # the question lands last
    tag(base, lt, 960, 610, question, 150, t_question, CARD, INK, -2, "a", "chime", (40, 22))
    ring(d, (960 - 125, 505, 960 + 125, 715), appear(lt, t_question + .5, .5, "marker"), INK, 6)
    if ask: note(d, lt, 960, 770, ask, 60, t_ask, INK, anchor="ma")


# ------------------------------------------------------------------ myth_vs_reality
@component("hooks", "myth_vs_reality", dur=6.0, cam=[(0, 700, 400, 1.2), (1.3, 700, 400, 1.17), (2.1, 960, 540, 1.0), (6.0, 960, 540, 1.03)], still=5.0,
           use="Open by knocking down a common belief: the myth is crossed out by hand and the real figure drops in highlighted.",
           notes="The myth is on screen at once; the real figure follows at t_figure (default 2.6 s) because it is the reveal.")
def myth_vs_reality(base, d, lt, cam, myth_label="PEOPLE SAY", myth="£100 A MONTH WON'T CHANGE MUCH", myth_tag="MYTH",
                    reality_label="WHAT THE SUMS SAY", reality="OVER 20 YEARS IT ADDS UP TO", figure="£24,000", link="so we did the sums",
                    aside="paid in, before any growth", picture="coins", role="o",
                    t_myth=.1, t_cross=.95, t_tag=1.45, t_reality=1.9, t_figure=2.6, t_swipe=3.1, t_link=2.25, t_pic=3.7, t_aside=4.3):
    col = ROLE[role]; deco(base, cam, "dots", 1700, 240, .15); deco(base, cam, "blobO" if role == "o" else "blobB" if role == "b" else "blobG", 1150, 760, .3)
    MB = (170, 180, 1090, 500); a = panel(base, lt, MB, t_myth, KRAFT, seed=14, frm=(-60, 0))
    lines = wrap(myth, 82, "a", 800)[:2]; x0 = 222; y0 = 274 if len(lines) > 1 else 318; xm = x0 + max(tw(l, 82, "a") for l in lines)
    if a > .02:
        T(d, x0, 208, myth_label, 32, "o", BROWN, a=fa(lt, t_myth + .15), on=KRAFT)
        tc = mix(INK, (126, 104, 72), ease((lt - t_cross - .2) / .5))
        for i, ln in enumerate(lines): kline(d, lt, x0, y0 + i * 104, [(ln, t_myth + .22 + i * .2, tc, None)], 82, "a", on=KRAFT)
        yb = y0 + 104 * len(lines) + 4
        stroke(d, [(x0 - 14, y0 + 16), ((x0 + xm) / 2, (y0 + yb) / 2 - 6), (xm + 16, yb - 6)], appear(lt, t_cross, .28, "marker"), col, 13, 41, 2.2)
        stroke(d, [(xm + 10, y0 + 12), ((x0 + xm) / 2, (y0 + yb) / 2 + 6), (x0 - 10, yb - 2)], appear(lt, t_cross + .25, .28, "marker"), col, 13, 43, 2.2)
    tag(base, lt, 962, 238, myth_tag, 58, t_tag, col, ROLE_FG[role], -8, "a", "pop", (24, 12))
    # reality drops in from above
    RB = (650, 560, 1590, 958); a2 = panel(base, lt, RB, t_reality, CARD, seed=15, frm=(0, -70))
    if a2 > .02:
        T(d, 704, 590, reality_label, 32, "o", MUTED, a=fa(lt, t_reality + .2), on=CARD)
        kline(d, lt, 704, 636, [(reality, t_reality + .3, INK, None)], 60, "a", on=CARD)
        bx = _fig(d, lt, 704, 706, figure, 172, t_figure, t_swipe, role, "a", INK, CARD)
        if aside: _lines(d, lt, bx[2] + 46, 786, aside, 44, t_aside, RB[2] - bx[2] - 70, MUTED, CARD, gap=.95)
    if link:
        _lines(d, lt, 1250, 268, link, 64, t_link, 520, INK, gap=.95)
        arrow(d, (1400, 420), (1340, 540), appear(lt, t_link + .3, .45, "marker"), INK, 6, .25)
    if picture: cut(base, lt, picture, 395, 750, 200, t_pic, rot=-5, disc=(role if role in "obg" else "k", 125))
