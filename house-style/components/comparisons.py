"""Comparisons: two options side by side. versus_card (two cards and a VS disc), two_jars (paper jars that fill in
proportion to their figures), split_screen (the frame torn in two tinted halves). All figures are illustrations."""
from kit import *

ROLE = {"o": ORANGE, "b": BLUE, "g": GREEN, "k": KRAFT, "n": INK}
def _fg(role): return CARD if role in ("b", "n") else INK
def _cap(f, size):
    bb = F(f, size).getbbox("H0"); return (bb[3] - bb[1]) / S
def _tick(d, x, y, p, col=INK, w=7, k=1.0, seed=31):
    """Hand-drawn tick whose elbow sits at (x, y)."""
    stroke(d, [(x - 15 * k, y - 13 * k), (x, y), (x + 30 * k, y - 36 * k)], p, col, w, seed, .6)

# ------------------------------------------------------------------ versus card
@component("comparisons", "versus_card", dur=5.5, cam=[(0, 700, 470, 1.18), (1.5, 960, 540, 1.0), (5.5, 960, 540, 1.03)], still=5.0,
           use="Two named options head to head with one figure each, when the script says 'A or B' and then names the winner.")
def versus_card(base, d, lt, cam, headline="WHICH ONE", key_word="WINS?", hk="o",
                a_label="OPTION A", a_sub="AFTER 10 YEARS", a_value=1000, a_pic="house", a_role="o",
                b_label="OPTION B", b_sub="AFTER 10 YEARS", b_value=2000, b_pic="chart", b_role="b",
                fmt="£{:,.0f}", vs_text="VS", winner="b", win_style="tag", win_text="AHEAD", win_role="g",
                t_head=.15, t_a=.7, t_vs=1.35, t_b=1.6, t_fig_a=2.3, t_fig_b=2.9, t_win=3.8):
    """winner: "a", "b" or None. win_style: "tag" (GREEN tick tag under the winning card) or "ring" (marker ring round its figure)."""
    deco(base, cam, "blobO", 380, 640, .3); deco(base, cam, "blobB", 1560, 640, .3); deco(base, cam, "dots", 1740, 210, .15)
    kline(d, lt, 110, 150, [(headline, t_head, INK, None), (key_word, t_head + .3, INK, hk)], 84, "a")
    Y0, Y1, CWd = 290, 870, 680; figbox = {}
    for side, x0, lab, sub, val, pic, role, t0, tf, rot in (("a", 150, a_label, a_sub, a_value, a_pic, a_role, t_a, t_fig_a, -4),
                                                            ("b", 1090, b_label, b_sub, b_value, b_pic, b_role, t_b, t_fig_b, 4)):
        cx = x0 + CWd / 2
        a = panel(base, lt, (x0, Y0, x0 + CWd, Y1), t0, CARD, seed=41 if side == "a" else 43, frm=(-70 if side == "a" else 70, 0))
        if a <= .02: continue
        ah = fa(lt, t0 + .22, .25)                                         # role-coloured header strip, once the card has landed
        if ah > .02:
            hb = (x0 + 16, Y0 + 16, x0 + CWd - 16, Y0 + 90)
            paste(base, panel_sprite(int((hb[2] - hb[0]) * S), int((hb[3] - hb[1]) * S), ROLE[role], 31, False, 0), X(hb[0]) - PAD, X(hb[1]) - PAD, ah)
            rec("c", hb, "header"); T(d, cx, (hb[1] + hb[3]) / 2, lab, 44, "o", _fg(role), "mm", ah, ROLE[role])
        cut(base, lt, pic, cx, Y0 + 242, 172, t0 + .4, rot=rot, disc=(role if role in DISC else "k", 100), sfx=None)
        T(d, cx, Y0 + 392, sub, 28, "o", MUTED, "mm", fa(lt, tf - .15), CARD)
        size = 116 if winner not in ("a", "b") else (132 if winner == side else 100)
        if lt >= tf:
            u = clamp((lt - tf) / .6); appear(lt, tf, .6, "ticks"); s = fmt.format(val * ease(u)); ref = fmt.format(val)
            T(d, cx, Y0 + 488, s, size * (.7 + .3 * back((lt - tf) / .3)), "a", ROLE[role], "mm", min(1, (lt - tf) / .15), CARD)
            w = tw(ref, size, "a"); h = _cap("a", size); figbox[side] = (cx - w / 2, Y0 + 488 - h / 2, cx + w / 2, Y0 + 488 + h / 2)
        else: appear(lt, tf, .6, "ticks")
    # the VS disc
    av = appear(lt, t_vs, .4, "pop")
    if lt >= t_vs:
        e = back((lt - t_vs) / .4); r = 82
        if e > .05:
            rot_paste(base, panel_sprite(int(2 * r * S), int(2 * r * S), INK, 12, True), 960, 580, 0, e, min(1, av * 2))
            rec("c", (960 - r, 580 - r, 960 + r, 580 + r), "vs"); T(d, 960, 580, vs_text, 70 * e, "a", CREAM, "mm", min(1, av * 2), INK)
    # the winner
    if winner in ("a", "b"):
        wcx = 150 + CWd / 2 if winner == "a" else 1090 + CWd / 2
        if win_style == "ring":
            p = appear(lt, t_win, .5, "marker"); chime(lt, t_win + .35)
            if winner in figbox and p > .01:
                b = figbox[winner]; ring(d, (b[0] - 34, b[1] - 20, b[2] + 34, b[3] + 22), p, DGREEN if win_role == "g" else ROLE[win_role], 7, 13)
        else:
            txt = "       " + win_text; rot = -2 if winner == "a" else 2
            if tag(base, lt, wcx, 926, txt, 40, t_win, ROLE[win_role], _fg(win_role), rot, "o", "chime"):
                w = tw(txt, 40, "o"); _tick(d, wcx - w / 2 + 16, 938 + (4 if winner == "a" else -4) * (w / 2 - 16) / 114, appear(lt, t_win + .35, .3, "marker"), _fg(win_role), 6, .8)

# ------------------------------------------------------------------ two jars
@component("comparisons", "two_jars", dur=6.0, cam=[(0, 720, 470, 1.16), (1.4, 960, 540, 1.0), (6.0, 960, 540, 1.03)], still=5.4,
           use="Two pots built from the same money that end at different sizes: the jars fill in proportion to the two figures.")
def two_jars(base, d, lt, cam, headline="SAME MONEY,", key_word="TWO JARS", hk="b",
             a_label="OPTION A", a_value=10000, a_role="o", b_label="OPTION B", b_value=15000, b_role="b",
             fmt="£{:,.0f}", sub="AFTER 10 YEARS", top_level=.9, diff_note=None,
             t_head=.15, t_jars=.7, t_fill=1.4, fill_dur=2.2, t_note=4.2):
    """The fuller jar fills to top_level (0-1); the other level is computed so both are proportional to the figures.
    diff_note=None writes the difference from the figures."""
    top = max(a_value, b_value, 1e-9); lv = {"a": top_level * a_value / top, "b": top_level * b_value / top}
    big_side = None if a_value == b_value else ("a" if a_value > b_value else "b")
    deco(base, cam, "blobO", 420, 600, .3); deco(base, cam, "blobB", 1240, 600, .3); deco(base, cam, "dots", 1740, 900, .15)
    kline(d, lt, 110, 150, [(headline, t_head, INK, None), (key_word, t_head + .3, INK, hk)], 84, "a")
    u = clamp((lt - t_fill) / fill_dur); e = ease(u); appear(lt, t_fill, fill_dur, "ticks"); JW, JH, CY = 118, 158, 575
    for side, cx, lab, val, role, tj in (("a", 400, a_label, a_value, a_role, t_jars), ("b", 1160, b_label, b_value, b_role, t_jars + .2)):
        col = DISC.get(role, DISC["k"]); filling = t_fill < lt < t_fill + fill_dur - .1 and val > 0
        stroke(d, [(cx - 150, CY + JH + 8), (cx, CY + JH + 5), (cx + 150, CY + JH + 8)], fa(lt, tj + .1, .4), INK, 5, 21 if side == "a" else 23, 1.0)
        jar(base, d, lt, cx, CY, tj, lv[side] * e, col, drops=((1.2 + 1.4 * val / top, t_fill) if filling else None), w=JW, h=JH)
        tag(base, lt, cx, CY + JH + 104, lab, 40, tj + .3, ROLE[role], _fg(role), -2 if side == "a" else 2, "o", None)
        size = 112 if big_side is None else (136 if big_side == side else 92); fx0 = cx + JW + 44
        if lt >= t_fill:
            T(d, fx0, CY - 40, fmt.format(val * e), size, "a", ROLE[role], "lm", min(1, (lt - t_fill) / .2))
            T(d, fx0 + 4, CY - 40 + _cap("a", size) / 2 + 34, sub, 28, "o", MUTED, "lm", fa(lt, t_fill + .2))
        if big_side == side or (big_side is None and side == "b"):
            txt = diff_note or (f"{fmt.format(abs(a_value - b_value))} more in this jar" if big_side else "level pegging")
            ny = CY - 40 + _cap("a", size) / 2 + 74; note(d, lt, fx0 + 4, ny, txt, 56, t_note, INK)
            underline(d, fx0 + 4, fx0 + 4 + tw(txt, 56, "c"), ny + 66, appear(lt, t_note + .35, .4, "marker"), ROLE[role], 6)
    chime(lt, t_fill + fill_dur)

# ------------------------------------------------------------------ split screen
_DIV = {}
def _divider(wd=38):
    """Torn strip of card paper, full canvas height (canvas px sprite)."""
    if wd not in _DIV:
        r = random.Random(17); w = int(wd * S) + 2 * PAD; m = Image.new("L", (w, CH), 0); dd = ImageDraw.Draw(m)
        L = [(PAD + r.uniform(0, 10), y) for y in range(-12, CH + 24, 12)]; R = [(w - PAD - r.uniform(0, 10), y) for y in range(CH + 12, -24, -12)]
        dd.polygon(L + R, fill=255); _DIV[wd] = V._paper_from_mask(m, CARD, 5, .42, (3, 0), 9)
    return _DIV[wd]
def _tint(base, x0, x1, col):
    """Tint the paper between two stage x positions (full height), keeping its grain."""
    a, b = max(0, int(X(x0))), min(CW, int(X(x1)))
    if b - a < 2: return
    reg = np.asarray(base.crop((a, 0, b, CH)), np.int16) + (np.array(col, np.int16) - np.array(PAPER, np.int16))
    base.paste(Image.fromarray(np.clip(reg, 0, 255).astype(np.uint8)), (a, 0))

@component("comparisons", "split_screen", dur=5.5, cam=[(0, 960, 560, 1.1), (1.5, 960, 540, 1.0), (5.5, 960, 540, 1.03)], still=5.0,
           use="Two worlds side by side (two people, two choices, before and after): the frame is torn in half and each half carries one figure.")
def split_screen(base, d, lt, cam, a_head="OPTION A", a_pic="house", a_value=1000, a_sub="EXAMPLE TOTAL", a_role="o",
                 b_head="OPTION B", b_pic="chart", b_value=1500, b_sub="EXAMPLE TOTAL", b_role="b",
                 fmt="£{:,.0f}", favour=None, shift=56, tint=.62,
                 t_split=.1, t_a=.8, t_b=1.4, t_fig_a=2.2, t_fig_b=2.8, t_shift=3.7):
    """favour: "a", "b" or None (None = the larger figure). The divider slides `shift` px to give the favoured half more room."""
    fav = favour or (None if a_value == b_value else ("a" if a_value > b_value else "b"))
    sg = 0 if fav is None else (1 if fav == "a" else -1); appear(lt, t_shift, .7, "slide") if sg else None
    div = 960 + sg * shift * ease((lt - t_shift) / .7)
    ca, cb = mix(PAPER, HLC.get(a_role, KRAFT), tint), mix(PAPER, HLC.get(b_role, KRAFT), tint)
    p = eout((lt - t_split) / .6); appear(lt, t_split, .6, "whoosh")
    if p > .01:                                                            # the tints soak in over the whole half (no moving edge under the labels)
        _tint(base, -BLEED, div, mix(PAPER, ca, p)); _tint(base, div, W + BLEED, mix(PAPER, cb, p))
        rec("c", (-BLEED, -BLEED, div, H + BLEED), "left half"); rec("c", (div, -BLEED, W + BLEED, H + BLEED), "right half")
    td = t_split + .4; pd = eout((lt - td) / .5); appear(lt, td, .5, "slide")
    if lt > td:
        sp = _divider(); paste(base, sp, X(div) - sp.size[0] / 2, -(1 - pd) * CH)
        rec("c", (div - 19, -BLEED - (1 - pd) * (H + 2 * BLEED), div + 19, H + BLEED - (1 - pd) * (H + 2 * BLEED)), "divider")
    for side, cx, head, pic, val, sub, role, on, t0, tf, rot in (("a", 480, a_head, a_pic, a_value, a_sub, a_role, ca, t_a, t_fig_a, -3),
                                                                 ("b", 1440, b_head, b_pic, b_value, b_sub, b_role, cb, t_b, t_fig_b, 3)):
        tag(base, lt, cx, 236, head, 50, t0, ROLE[role], _fg(role), rot, "o", "pop")
        cut(base, lt, pic, cx, 484, 226, t0 + .25, rot=-rot, disc=("w", 132), sfx=None)
        size = 128 if fav is None else (152 if fav == side else 108)
        if lt >= tf:
            T(d, cx, 762, fmt.format(val), size * (.6 + .4 * back((lt - tf) / .35)), "a", INK, "mm", min(1, (lt - tf) / .15), on)
            T(d, cx, 762 + _cap("a", size) / 2 + 40, sub, 32, "o", mix(on, INK, .72), "mm", fa(lt, tf + .25), on)
        appear(lt, tf, .35, "pop")
    if sg: chime(lt, t_shift + .6)
