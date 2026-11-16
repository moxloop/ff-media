"""Number reveals (body gear: calm, one dominant number per screen).

stamp            the figure on a card; a rubber stamp (word in Oswald, double border, uneven ink) thumps down beside it
rolling_counter  an odometer: each digit column rolls to its final digit inside a counter panel, settling left to right
circled_figure   the figure lands on paper, a marker ring is drawn round it, an arrow and a handwritten note point at it

Every string, figure, colour role and cue time is a parameter; the defaults are round example numbers only.
"""
from kit import *

ROLE = {"o": ORANGE, "b": BLUE, "g": GREEN, "k": INK}
INKROLE = {"o": (232, 112, 12), "b": BLUE, "g": DGREEN, "k": INK}          # role colours dark enough to read as ink on a card


def _fig(d, lt, x, y, s, size, t0, t_hl=None, hk=None, f="a", fill=INK, on=PAPER, anchor="l"):
    """A figure that drops in at t0 with an optional highlighter swipe at t_hl. Returns its cap box."""
    fo = F(f, size); w = fo.getlength(s) / S; x0 = x - (w if anchor == "r" else w / 2 if anchor == "m" else 0)
    bb = fo.getbbox("H0"); top, bot = bb[1] / S, bb[3] / S
    if hk and t_hl is not None:
        hl(d, x0, y + top + (bot - top) * .06, x0 + w, y + bot + (bot - top) * .1, mix(on, HLC[hk], .95), appear(lt, t_hl, .45, "marker"))
    u = clamp((lt - t0) / .3)
    if u > 0: T(d, x0, y, s, size, f, fill, "la", min(1, u * 2.2), on, dy=-26 * (1 - back(u)))
    return (x0, y + top, x0 + w, y + bot)


def _lines(d, lt, x, y, s, size, t0, maxw, fill=INK, on=PAPER, f="c", gap=.95, anchor="la"):
    ls = wrap(s, size, f, maxw)
    for i, ln in enumerate(ls): note(d, lt, x, y + i * size * gap, ln, size, t0 + i * .12, fill, on, anchor, f)
    return len(ls)


# ------------------------------------------------------------------ stamp
@lru_cache(maxsize=24)
def _stamp_sprite(word, col, w, h, seed=7):
    """Rubber-stamp impression: double border, the word in Oswald, slightly uneven ink. RGBA, canvas px."""
    Wp, Hp, pad = int(w * S), int(h * S), 14
    m = Image.new("L", (Wp + 2 * pad, Hp + 2 * pad), 0); dd = ImageDraw.Draw(m)
    dd.rounded_rectangle([pad, pad, pad + Wp, pad + Hp], int(20 * S), outline=255, width=int(9 * S))
    ins = int(17 * S); dd.rounded_rectangle([pad + ins, pad + ins, pad + Wp - ins, pad + Hp - ins], int(10 * S), outline=255, width=int(3 * S))
    size = h * .5
    while tw(word, size, "o") > w - 84 and size > 20: size *= .95
    fo = F("o", size); bb = fo.getbbox(word); dd.text((pad + Wp / 2 - (bb[0] + bb[2]) / 2, pad + Hp / 2 - (bb[1] + bb[3]) / 2), word, font=fo, fill=255)
    rng = np.random.default_rng(seed); sh = (m.size[1], m.size[0])
    lo = cv2.GaussianBlur(rng.standard_normal(sh).astype(np.float32), (0, 0), 16); lo /= lo.std()
    hi = cv2.GaussianBlur(rng.standard_normal(sh).astype(np.float32), (0, 0), 1.3); hi /= hi.std()
    k = np.clip(.84 + .13 * lo + .1 * hi, .3, 1.0); k[hi < -1.75] *= .35
    al = (np.asarray(m, np.float32) * k).astype(np.uint8)
    im = Image.new("RGBA", m.size, col + (0,)); im.putalpha(Image.fromarray(al)); return im


@component("reveals", "stamp", dur=4.5, cam=[(0, 960, 520, 1.1), (1.2, 960, 540, 1.0), (4.5, 960, 540, 1.03)], still=3.6,
           use="Land a verdict on one figure: the number sits on a card and a rubber stamp (SAVED, PAID, EXTRA...) thumps down beside it.",
           notes="Stamp colour follows role: green = positive, orange = cost or overpay, blue = invest.")
def stamp(base, d, lt, cam, title=("THE", "RESULT"), label="OVER 20 YEARS", figure="£24,000", word="SAVED", role="g", aside="example figure",
          stamp_rot=-8.0, t_title=.15, t_card=.5, t_figure=1.0, t_stamp=2.0, t_aside=2.9):
    deco(base, cam, "blobG" if role == "g" else "blobO" if role == "o" else "blobB", 1380, 560, .3); deco(base, cam, "dots", 190, 900, .15)
    if title: kline(d, lt, 110, 150, [(title[0], t_title, INK, None), (title[1], t_title + .2, INK, None)], 84, "a")
    CB = (280, 300, 1640, 810); a = panel(base, lt, CB, t_card, CARD, seed=8)
    if a > .02:
        T(d, 352, 338, label, 44, "o", MUTED, a=fa(lt, t_card + .25), on=CARD)
        _fig(d, lt, 352, 396, figure, 236, t_figure, None, None, "a", INK, CARD)
        if aside: note(d, lt, 356, 716, aside, 46, t_aside, MUTED, CARD)
    # the stamp thumps down: arrives oversized, overshoots a touch, settles
    appear(lt, t_stamp, .26, "pop"); u = clamp((lt - t_stamp) / .26)
    if u > 0:
        sc = 1 + .3 * (1 - back(u)); sp = _stamp_sprite(word, INKROLE[role], 370, 156)
        rec("t", rot_paste(base, sp, 1350, 562, stamp_rot, sc, min(1, u * 3) * .93), word)


# ------------------------------------------------------------------ rolling_counter
@lru_cache(maxsize=8)
def _shade(w, h):
    g = np.zeros((h, w), np.float32); n = int(h * .26)
    for i in range(n): v = (1 - i / n) ** 1.6 * 150; g[i, :] = v; g[h - 1 - i, :] = v
    return Image.fromarray(g.astype(np.uint8))
@lru_cache(maxsize=8)
def _rmask(w, h, r):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255); return m
def _column(v, cw, ch, size, win, col, edge):
    """One digit window (canvas px) showing odometer position v (digits scroll upwards as v rises)."""
    im = Image.new("RGB", (cw, ch), win); dd = ImageDraw.Draw(im); fo = F("a", size); b0 = fo.getbbox("0"); n0 = math.floor(v)
    for n in (n0 - 1, n0, n0 + 1):
        s = str(n % 10); bb = fo.getbbox(s); y = ch / 2 + (n - v) * ch
        dd.text((cw / 2 - (bb[0] + bb[2]) / 2, y - (b0[1] + b0[3]) / 2), s, font=fo, fill=col)
    im.paste(edge, (0, 0), _shade(cw, ch)); return im


@component("reveals", "rolling_counter", dur=5.0, cam=[(0, 960, 540, 1.1), (1.2, 960, 540, 1.0), (5.0, 960, 540, 1.03)], still=4.2,
           use="Build up to a total: the digits roll like an odometer and settle left to right, so the size of the number sinks in.",
           notes="panel_role 'ink' (dark counter) or 'card'. The ticks sound is trimmed to the roll: t_roll to t_roll + roll + stagger x (digits - 1).")
def rolling_counter(base, d, lt, cam, title=("ADD IT", "ALL UP"), label="TOTAL PAID IN", figure="£24,000", sub="OVER 20 YEARS", aside="example figures",
                    role="o", panel_role="ink", size=190, t_title=.15, t_panel=.5, t_label=.85, t_roll=1.1, roll=1.0, stagger=.3, t_sub=None, t_aside=None):
    dark = panel_role == "ink"; pf = INK if dark else CARD; win = mix(pf, CARD if dark else INK, .1 if dark else .06)
    col = ROLE[role] if dark else INKROLE[role]; stat = CREAM if dark else INK
    deco(base, cam, "blobO" if role == "o" else "blobB" if role == "b" else "blobG", 960, 570, .3); deco(base, cam, "dots", 1730, 250, .15); deco(base, cam, "dots", 180, 900, .15)
    if title: kline(d, lt, 110, 150, [(title[0], t_title, INK, None), (title[1], t_title + .2, INK, None)], 84, "a")
    fo = F("a", size); b0 = fo.getbbox("0"); gh = (b0[3] - b0[1]) / S; dw, dh, gap = size * .6, gh * 1.36, 10
    ws = [dw if c.isdigit() else tw(c, size, "a") + 6 for c in figure]; total = sum(ws) + gap * (len(ws) - 1)
    CY = 580; x0 = 960 - total / 2; PB = (x0 - 46, CY - dh / 2 - 40, x0 + total + 46, CY + dh / 2 + 40)
    nd = sum(c.isdigit() for c in figure); t_end = t_roll + roll + stagger * max(0, nd - 1)
    t_sub = t_end + .25 if t_sub is None else t_sub; t_aside = t_end + .7 if t_aside is None else t_aside
    a = panel(base, lt, PB, t_panel, pf, seed=12)
    lw = tw(label, 40, "o") + 44
    if label: tag(base, lt, PB[0] + lw / 2 + 8, PB[1] - 52, label, 40, t_label, KRAFT, INK, -2, "o", "pop")
    appear(lt, t_roll, t_end - t_roll, "ticks"); chime(lt, t_end)
    va = fa(lt, t_panel + .3, .25)
    if a > .02 and va > .03:
        x = x0; j = 0; cw, ch = int(dw * S), int(dh * S); mk = _rmask(cw, ch, int(9 * S))
        if va < 1: mk = mk.point(lambda q: int(q * va))
        for c, w in zip(figure, ws):
            if c.isdigit():
                te = t_roll + roll + stagger * j; u = clamp((lt - t_roll) / (te - t_roll)); v = int(c) - (8 + 5 * j) * (1 - eout(u))
                if u >= 1: v = int(c) + .035 * math.sin(min(1, (lt - te) / .22) * math.pi) * (1 if lt - te < .22 else 0)      # tiny settle bounce
                base.paste(_column(v, cw, ch, size, win, mix(stat, col, ease((lt - te + .1) / .25)) if True else col, pf), (int(X(x)), int(X(CY - dh / 2))), mk); j += 1
            else:
                T(d, x + 3, CY + gh / 2, c, size, "a", stat, "ls", va, pf)
            x += w + gap
        rec("t", (x0, CY - dh / 2, x0 + total, CY + dh / 2), figure)
    if sub:
        T(d, 960, PB[3] + 70, sub, 54, "o", INK, "mm", fa(lt, t_sub), dy=14 * (1 - eout((lt - t_sub) / .3)))
        sw = tw(sub, 54, "o"); underline(d, 960 - sw / 2, 960 + sw / 2, PB[3] + 108, appear(lt, t_sub + .3, .4, "marker"), ROLE[role], 6)
    if aside: note(d, lt, 960, PB[3] + 128, aside, 46, t_aside, MUTED, anchor="ma")


# ------------------------------------------------------------------ circled_figure
@component("reveals", "circled_figure", dur=4.5, cam=[(0, 820, 530, 1.14), (1.3, 960, 540, 1.0), (4.5, 960, 540, 1.03)], still=3.8,
           use="Single out the one figure the viewer must remember: it lands on paper, gets a marker ring, an arrow and a handwritten note.")
def circled_figure(base, d, lt, cam, title=("THE NUMBER", "TO WATCH"), label="OVER 20 YEARS", figure="£24,000", note_text="this is the one that matters",
                   footer="Example figure, for illustration", role="o", t_title=.15, t_card=.5, t_figure=1.0, t_ring=1.7, t_note=2.4):
    col = ROLE[role]; deco(base, cam, "dots", 1700, 880, .15); deco(base, cam, "blobO" if role == "o" else "blobB" if role == "b" else "blobG", 1500, 500, .3)
    if title: kline(d, lt, 110, 150, [(title[0], t_title, INK, None), (title[1], t_title + .2, INK, None)], 84, "a")
    CB = (250, 290, 1250, 850); a = panel(base, lt, CB, t_card, CARD, seed=17); FX, FY = 750, 446
    if a > .02:
        T(d, 310, 322, label, 42, "o", MUTED, a=fa(lt, t_card + .25), on=CARD)
        bx = _fig(d, lt, FX, FY, figure, 230, t_figure, None, None, "a", INK, CARD, "m")
        T(d, 310, 798, footer, 24, "r", MUTED, a=fa(lt, t_figure + .4), on=CARD)
        rb = (max(CB[0] + 44, bx[0] - 56), bx[1] - 44, min(CB[2] - 44, bx[2] + 56), bx[3] + 50)
        ring(d, rb, appear(lt, t_ring, .6, "marker"), col, 9, 3)
    else: rb = (350, 470, 1150, 760)
    n = _lines(d, lt, 1330, 372, note_text, 68, t_note, 470, INK)
    arrow(d, (1400, 372 + n * 65 + 34), (rb[2] + 34, (rb[1] + rb[3]) / 2 + 30), appear(lt, t_note + .35, .45, "marker"), INK, 6, -.25)
