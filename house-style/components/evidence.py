"""Evidence: the working, shown on paper. calc_sheet (the signature Figures Forward calculation sheet, body gear),
payslip (a generic example payslip / receipt) and ruler_span (a paper ruler for time spans).
Everything here is generic by design: never a real bank's or company's name, logo or account number."""
from kit import *

ROLE = {"o": ORANGE, "b": BLUE, "g": GREEN, "k": KRAFT, "n": INK}
def _fg(role): return CARD if role in ("b", "n") else INK
def _cap(f, size):
    bb = F(f, size).getbbox("H0"); return (bb[3] - bb[1]) / S
def _write(s, lt, t0, cps=42):
    """The part of a string written so far (a quick hand-written 'write on')."""
    return s[:int(math.ceil(len(s) * clamp((lt - t0) * cps / max(1, len(s)))))] if lt > t0 else ""

# ------------------------------------------------------------------ calculation sheet
@component("evidence", "calc_sheet", dur=6.0, cam=[(0, 960, 540, 1.0), (.8, 960, 540, 1.0), (6.0, 905, 548, 1.12)], still=5.5,
           use="The signature 'Figures Forward calculation' sheet in body gear: show the working row by row at the episode's key figure, with one highlighter swipe.",
           notes="Use once at the episode's key figure (and once in the hook). The camera is a calm push to about 1.12, not a pull-out.")
def calc_sheet(base, d, lt, cam, title="FIGURES FORWARD CALCULATION", tagline="worked example", subtitle="£100 a month for 10 years (120 months)",
               rows=(("Paid in", "£12,000"), ("Growth at an example 5% a year", "£3,500"), ("Fees taken out", "−£500")),
               total=("Ends at", "£15,000"), key_row="total", hk="o", footnote="Illustrative figures, rounded",
               side_pic="calculator", side_note="the working, shown",
               t_sheet=.15, t_rows=None, t_total=None, t_hl=None, t_side=None):
    """rows: (label, value) strings. key_row: a row index or "total"; hk: highlighter colour "o", "b", "g" or "y"."""
    n = len(rows); t_rows = t_rows or [1.0 + .75 * i for i in range(n)]; t_total = t_rows[-1] + .9 if t_total is None else t_total
    t_hl = t_total + .6 if t_hl is None else t_hl; t_side = .6 if t_side is None else t_side
    pitch = 48 if n <= 4 else 40; x0, x1 = 300, 1260; hgt = 150 + pitch * 2 * n + 78 + 122; y0 = 545 - hgt / 2; y1 = y0 + hgt
    L = lambda k: y0 + 150 + pitch * k; xl, xr = x0 + 62, x1 - 56
    deco(base, cam, "blobK", 1560, 520, .25); deco(base, cam, "dots", 1700, 900, .15)
    a = panel(base, lt, (x0, y0, x1, y1), t_sheet, CARD, seed=21, frm=(-70, 0))
    if a > .02:
        for k in range(0, 2 * n + 4):
            if L(k) < y1 - 24: d.line([X(x0 + 20), X(L(k)), X(x1 - 20), X(L(k))], fill=mix(CARD, (200, 220, 240), a * .7), width=2)
        d.line([X(x0 + 40), X(y0 + 12), X(x0 + 40), X(y1 - 12)], fill=mix(CARD, (255, 190, 170), a), width=2)
        T(d, xl, y0 + 34, title, 28, "o", MUTED, a=fa(lt, t_sheet + .25), on=CARD)
        T(d, xr, y0 + 26, tagline, 38, "c", ORANGE, "ra", fa(lt, t_sheet + .4), CARD)
        T(d, xl, y0 + 84, subtitle, 26, "sb", INK, a=fa(lt, t_sheet + .5), on=CARD)
        def swipe(val, size, ym, t0):
            w = tw(val, size, "a"); h = _cap("a", size); ph = appear(lt, t0, .45, "marker")
            if ph > .01: hl(d, xr - w, ym - h / 2 - 5, xr, ym + h / 2 + 9, mix(CARD, HLC[hk], .95), ph)
        for i, (lab, val) in enumerate(rows):
            ym = L(2 * i + 1) - 20; t0 = t_rows[i]; appear(lt, t0, .3, "marker" if i == 0 else None)
            if key_row == i: swipe(val, 54, ym, t_hl)
            T(d, xl, ym, _write(lab, lt, t0), 32, "sb", INK, "lm", 1, CARD)
            T(d, xr, ym, val, 54, "a", INK, "rm", fa(lt, t0 + .3, .25), CARD, dy=8 * (1 - eout((lt - t0 - .3) / .3)))
        stroke(d, [(xl, L(2 * n) + 2), ((xl + xr) / 2, L(2 * n) - 2), (xr, L(2 * n) + 1)], appear(lt, t_total - .4, .35, "marker"), INK, 4, 9, .8)
        ym = L(2 * n) + 80
        if key_row == "total": swipe(total[1], 92, ym, t_hl)
        T(d, xl, ym, _write(total[0], lt, t_total, 30), 54, "c", ORANGE if hk in ("o", "y") else ROLE.get(hk, ORANGE) if hk != "g" else DGREEN, "lm", 1, CARD)
        appear(lt, t_total + .2, .3, "pop")
        if lt > t_total + .2: T(d, xr, ym, total[1], 92 * (.75 + .25 * back((lt - t_total - .2) / .35)), "a", INK, "rm", min(1, (lt - t_total - .2) / .15), CARD)
        T(d, xl, y1 - 44, footnote, 22, "r", MUTED, "lm", fa(lt, t_total + .6), CARD)
    if side_pic:
        cut(base, lt, side_pic, 1560, 500, 190, t_side, rot=5, disc=("k", 118), sfx="pop")
        if side_note: note(d, lt, 1560, 660, side_note, 50, t_side + .5, MUTED, anchor="ma")

# ------------------------------------------------------------------ payslip
@lru_cache(maxsize=8)
def _slip_sprite(w, h, seed=41, tooth=13):
    """Slip of card paper with a zigzag (torn-off) bottom edge. Canvas px."""
    m = Image.new("L", (w + 2 * PAD, h + 2 * PAD), 0); dd = ImageDraw.Draw(m); pts = [(PAD, PAD), (PAD + w, PAD)]; k = max(2, int(w / tooth)); st = w / k
    for i in range(k + 1): pts.append((PAD + w - i * st, PAD + h - (tooth if i % 2 else 0)))
    dd.polygon(pts, fill=255); return V._paper_from_mask(m, CARD, seed, .38)

@component("evidence", "payslip", dur=6.0, cam=[(0, 900, 500, 1.08), (1.4, 960, 540, 1.0), (6.0, 1000, 545, 1.04)], still=5.4,
           use="A generic example payslip or receipt when the script walks through pay, deductions or a bill line by line and singles one line out.",
           notes="Always an obviously made-up document: keep the 'EXAMPLE' tag and never pass a real employer, bank or account number.")
def payslip(base, d, lt, cam, headline="WHERE DOES", key_word="IT GO?", hk="o", title="EXAMPLE PAYSLIP", sub="Example employer · example month",
            lines=(("Gross pay", "£3,000.00", "pay"), ("Tax", "−£400.00", "ded"), ("Pension", "−£150.00", "ded"), ("Other deduction", "−£50.00", "ded")),
            net=("NET PAY", "£2,400.00"), stamp="EXAMPLE", footer="Illustration only · not a real document",
            ring_line=2, ring_role="o", ring_note="this line is the one to check", side_pic="coins",
            t_head=.15, t_slip=.6, t_lines=None, t_net=None, t_ring=None):
    """lines: (label, amount, kind) with kind "pay" or "ded" (deductions are drawn in ORANGE). ring_line: an index into lines, "net" or None."""
    n = len(lines); t_lines = t_lines or [1.2 + .45 * i for i in range(n)]; t_net = t_lines[-1] + .6 if t_net is None else t_net
    t_ring = t_net + .8 if t_ring is None else t_ring
    step = 74 if n <= 4 else 60; x0, x1 = 1060, 1700; hgt = 196 + step * n + 240; y0 = 550 - hgt / 2; y1 = y0 + hgt; xl, xr = x0 + 46, x1 - 46
    deco(base, cam, "blobO", 420, 700, .3); deco(base, cam, "dots", 180, 930, .15)
    kline(d, lt, 110, 160, [(headline, t_head, INK, None)], 84, "a"); kline(d, lt, 110, 258, [(key_word, t_head + .3, INK, hk)], 84, "a")
    a = appear(lt, t_slip, .45, "slide"); ringbox = None
    if a > .02:
        e = back(clamp((lt - t_slip) / .45)); paste(base, _slip_sprite(int((x1 - x0) * S), int(hgt * S)), X(x0) - PAD, X(y0) - PAD + 60 * S * (1 - e), min(1, a * 1.6))
        rec("c", (x0, y0, x1, y1 - 14), "payslip"); b = fa(lt, t_slip + .3)
        T(d, xl, y0 + 36, title, 46, "o", INK, a=b, on=CARD); T(d, xl, y0 + 108, sub, 22, "r", MUTED, a=b, on=CARD)
        d.line([X(xl), X(y0 + 156), X(xr), X(y0 + 156)], fill=mix(CARD, INK, b), width=int(3 * S))
        tag(base, lt, x1 - 118, y0 + 70, stamp, 30, t_slip + .55, INK, CREAM, -8, "o", "pop", (16, 10))
        for i, (lab, amt, kind) in enumerate(lines):
            ym = y0 + 208 + step * i; al = fa(lt, t_lines[i], .25); appear(lt, t_lines[i], .25, "pop" if i == 0 else None)
            if al <= .03: continue
            col = ORANGE if kind == "ded" else INK; wl, wa = tw(lab, 30, "sb"), tw(amt, 32, "b")
            for xx in range(int(xl + wl + 18), int(xr - wa - 14), 14): d.ellipse([X(xx) - 2, X(ym + 8) - 2, X(xx) + 2, X(ym + 8) + 2], fill=mix(CARD, LIGHT, al))
            T(d, xl, ym, lab, 30, "sb", INK, "lm", al, CARD); T(d, xr, ym, amt, 32, "b", col, "rm", al, CARD)
            if ring_line == i: ringbox = (xr - wa - 22, ym - 30, xr + 20, ym + 30)
        yr = y0 + 196 + step * n - 6; an = fa(lt, t_net, .3); appear(lt, t_net, .3, "pop")
        d.line([X(xl), X(yr), X(xr), X(yr)], fill=mix(CARD, INK, an), width=int(3 * S)); d.line([X(xl), X(yr + 7), X(xr), X(yr + 7)], fill=mix(CARD, INK, an), width=int(1.5 * S))
        ym = yr + 62; T(d, xl, ym, net[0], 40, "o", INK, "lm", an, CARD); T(d, xr, ym, net[1], 62, "a", INK, "rm", an, CARD)
        if ring_line == "net" and an > .03: w = tw(net[1], 62, "a"); ringbox = (xr - w - 24, ym - 44, xr + 22, ym + 44)
        T(d, (x0 + x1) / 2, y1 - 104, footer, 20, "r", MUTED, "mm", fa(lt, t_net + .3), CARD)
        for xx in range(int(x0 + 18), int(x1 - 30), 26): d.line([X(xx), X(y1 - 58), X(xx + 14), X(y1 - 58)], fill=mix(CARD, MUTED, b), width=int(2.5 * S))
    if ringbox:
        ring(d, ringbox, appear(lt, t_ring, .5, "marker"), ROLE[ring_role], 6, 15)
        if ring_note:
            ls = wrap(ring_note, 58, "c", 620); ny = (ringbox[1] + ringbox[3]) / 2 - 36 - 30 * (len(ls) - 1)
            for j, ln in enumerate(ls): note(d, lt, 150, ny + 60 * j, ln, 58, t_ring + .4 + .1 * j, INK)
            wn = max(tw(ln, 58, "c") for ln in ls)
            arrow(d, (150 + wn + 26, ny + 44), (x0 - 20, (ringbox[1] + ringbox[3]) / 2), appear(lt, t_ring + .7, .5, "marker"), ROLE[ring_role], 5, -.14)
    if side_pic: cut(base, lt, side_pic, 400, 800, 190, t_slip + .3, rot=-5, disc=("k", 112), sfx=None)

# ------------------------------------------------------------------ ruler span
@component("evidence", "ruler_span", dur=6.0, cam=[(0, 640, 450, 1.2), (1.9, 960, 540, 1.0), (6.0, 990, 545, 1.04)], still=5.4,
           use="A length of time measured out on a paper ruler: mark the span between two points (years saved, months left, time in the market).")
def ruler_span(base, d, lt, cam, headline="HOW MUCH", key_word="SOONER?", hk="g", units=25, unit_label="YEARS", major=5,
               a=20, b=25, span_label="5 YEARS EARLY", span_role="g", span_note="done here, not at the end", ruler_fill=(238, 208, 128),
               side_pic="calendar", t_head=.15, t_ruler=.7, roll_dur=1.3, t_span=2.6, t_label=3.2, t_note=4.0):
    """units: length of the ruler; a, b: the span to mark (in units, halves allowed, e.g. a=21.5, b=25, span_label="3½ YEARS EARLY")."""
    rx0, rx1, ry0, ry1 = 140, 1780, 560, 672; inset = 46; px = (rx1 - rx0 - 2 * inset) / units; ux = lambda u: rx0 + inset + u * px
    deco(base, cam, "blobK", 1500, 330, .25); deco(base, cam, "dots", 1720, 900, .15)
    kline(d, lt, 110, 150, [(headline, t_head, INK, None), (key_word, t_head + .3, INK, hk)], 84, "a")
    p = strip(base, lt, (rx0, ry0, rx1, ry1), t_ruler, ruler_fill, roll_dur, seed=61)
    if p > .01:
        edge = rx0 + (rx1 - rx0) * p - 8; xa, xb = ux(min(a, b)), ux(max(a, b))
        ps = appear(lt, t_span, .5, "marker")
        if ps > .01: hl(d, xa, ry0 + 5, xb, ry1 - 7, mix(ruler_fill, HLC.get(span_role, HLC["o"]), .9), ps)
        d.line([X(rx0 + 8), X(ry1 - 9), X(min(edge, rx1 - 8)), X(ry1 - 9)], fill=mix(ruler_fill, BROWN, .5), width=int(2 * S))
        for u in range(0, int(units) + 1):
            x = ux(u)
            if x > edge: break
            mj = u % major == 0; ln = 44 if mj else (30 if (major % 2 == 0 and u % (major // 2) == 0) else 20)
            d.line([X(x), X(ry0 + 3), X(x), X(ry0 + ln)], fill=INK, width=int((4 if mj else 2.4) * S))
            if mj: T(d, x, ry0 + 74, str(u), 32, "o", INK, "mm", 1, ruler_fill)
        T(d, rx0 + 6, ry1 + 22, unit_label, 30, "o", MUTED, "la", fa(lt, t_ruler + roll_dur * .5))
        # the span: bracket, label tag, note
        pb = appear(lt, t_span + .25, .5, None)
        stroke(d, [(xa, ry0 - 12), (xa, ry0 - 40), (xb, ry0 - 40), (xb, ry0 - 12)], pb, INK, 6, 17, .8)
        tcx = clamp((xa + xb) / 2, rx0 + 40 + tw(span_label, 48, "o") / 2, rx1 - 40 - tw(span_label, 48, "o") / 2)
        tag(base, lt, tcx, ry0 - 104, span_label, 48, t_label, ROLE[span_role], _fg(span_role), -2, "o", "chime")
        if span_note:
            wn = tw(span_note, 56, "c"); nx = clamp((xa + xb) / 2 - 60, 760, rx1 - 30 - wn / 2)
            note(d, lt, nx, 800, span_note, 56, t_note, INK, anchor="ma")
            arrow(d, (nx + 40, 792), ((xa + xb) / 2, ry1 + 16), appear(lt, t_note + .3, .5, "marker"), DGREEN if span_role == "g" else ROLE[span_role], 5, .18)
    if side_pic: cut(base, lt, side_pic, 330, 860, 170, t_ruler + .5, rot=-5, disc=("k", 100), sfx="pop")
