"""Charts on graph paper: line race, fee waterfall, repayment timeline with markers.

All data comes in as parameters; every default is a round, obviously illustrative figure. Lines draw on, bars and
blocks appear whole, and nothing inside the graph paper is a card (labels there are plain or haloed text), so the fit
check's "no card over a chart" rule holds. End-value tags sit just outside the chart's right edge.
"""
from kit import *

ROLE = {"o": ORANGE, "b": BLUE, "g": GREEN, "n": INK, "k": BROWN, "m": MUTED}           # line and text colour per role
FILL = dict(DISC, m=(190, 194, 200))                                                    # paper tone per role (bars, discs, tags)
FG = {"o": INK, "b": CARD, "g": INK, "n": CARD, "k": INK, "m": INK, "w": INK}            # text colour on a role's paper
CHART_CAM = [(0, 760, 505, 1.18), (1.5, MX, MY, 1.0), (6.0, MX, MY, 1.03)]

def _halo(d, x, y, s, size, f, fill, anchor="mm", a=1.0, on=CARD, w=4):
    """Text with a paper-coloured halo so it stays legible over grid lines and chart lines. Recorded for the fit check."""
    if a <= .03 or not s: return
    fo = F(f, size); xy = (X(x), X(y)); sw = int(w * S)
    d.text(xy, s, font=fo, fill=mix(on, fill, a), anchor=anchor, stroke_width=sw, stroke_fill=on)
    rec("t", V._unS(d.textbbox(xy, s, font=fo, anchor=anchor)), s)
def _fit_size(s, size, f, maxw):
    return size if tw(s, size, f) <= maxw else size * maxw / tw(s, size, f)
def _axes(d, px0, px1, py0, py1, a, x_label):
    if a <= .03: return
    col = mix(CARD, INK, a)
    d.line([X(px0), X(py0), X(px1 + 18), X(py0)], fill=col, width=int(4 * S)); d.line([X(px0), X(py0), X(px0), X(py1 - 26)], fill=col, width=int(4 * S))
    if x_label: T(d, px1 + 18, py0 + 12, x_label, 26, "o", MUTED, "ra", a, CARD)
def _bar(base, lt, box, t0, fill, seed=0, snd="pop", d_=.36):
    """A paper bar or block that appears whole (pops on, never grows from a stub). Chart marks are not cards: not recorded."""
    a = appear(lt, t0, d_, snd)
    if lt < t0: return 0.0
    w, h = max(4, int((box[2] - box[0]) * S)), max(4, int((box[3] - box[1]) * S))
    rot_paste(base, panel_sprite(w, h, fill, seed, False, .3), (box[0] + box[2]) / 2, (box[1] + box[3]) / 2, 0, .82 + .18 * back(clamp((lt - t0) / d_)), min(1, a * 2.2))
    return a
def _dash(d, x0, x1, y, p, col, w=3, dash=16, gap=11):
    xe = x0 + (x1 - x0) * clamp(p); x = x0
    while x < xe: d.line([X(x), X(y), X(min(x + dash, xe)), X(y)], fill=col, width=int(w * S)); x += dash + gap

# ============================================================================================ line race
RACE_A = (0, 12, 8, 30, 24, 52, 46, 76, 90, 80, 58, 64, 50, 60, 88, 80, 118, 110, 150, 142, 200)
RACE_B = tuple(round(7.5 * i) for i in range(21))
@component("charts", "line_race", dur=6.0, cam=CHART_CAM, still=5.3,
           use="Two (or three) options compared over time: the lines race left to right together, each with its label riding the tip, and the one that ends ahead gets the big end value and a handwritten callout.")
def line_race(base, d, lt, cam, title="WHICH ONE", title_key="ENDS AHEAD?", key_role="b",
              series=(("PLAN A", "b", RACE_A), ("PLAN B", "o", RACE_B)), fmt=None, winner=None, callout="ends ahead",
              x_label="TIME", label="Illustration, not real returns",
              t_title=.2, t_panel=.5, t_race=1.2, race_dur=2.6, t_end=None, t_callout=None):
    """series: (label, role, values) with equally spaced values (same count each); the y-scale is set from the largest value.
    End values are formatted with fmt (default whole pounds). winner: index of the series to call out (default: highest end)."""
    fmt = fmt or (lambda v: gbp(round(v))); n = len(series); assert 2 <= n <= 3, "line_race takes two or three series"
    t_end = t_race + race_dur + .1 if t_end is None else t_end; t_callout = t_end + .6 if t_callout is None else t_callout
    win = max(range(n), key=lambda i: series[i][2][-1]) if winner is None else winner
    kline(d, lt, 110, 150, [(title, t_title, INK, None), (title_key, t_title + .3, INK, key_role)], 88, "a")
    box = (110, 290, 1500, 940); px0, px1, py0, py1 = 190, 1440, 868, 452
    pa = panel(base, lt, box, t_panel, seed=12)
    top = max(max(s[2]) for s in series) * 1.06; yv = lambda v: py0 - (py0 - py1) * v / top
    ends = [yv(s[2][-1]) for s in series]
    if pa >= 1:
        ga = fa(lt, t_panel + .4, .25); graph(d, box, a=ga); _axes(d, px0, px1, py0, py1, ga, x_label)
        u = clamp((lt - t_race) / race_dur); p = .5 * u + .5 * ease(u); appear(lt, t_race, race_dur, "marker")
        tips = []
        for si, (name, role, vals) in enumerate(series):
            m = len(vals) - 1; pts = [(px0 + (px1 - px0) * i / m, yv(v)) for i, v in enumerate(vals)]; f_ = p * m; k = min(m - 1, int(f_)); r_ = f_ - k
            cutp = pts[:k + 1] + [(pts[k][0] + (pts[k + 1][0] - pts[k][0]) * r_, pts[k][1] + (pts[k + 1][1] - pts[k][1]) * r_)]
            if lt >= t_race and p > .004: stroke(d, tuple(cutp), 1, ROLE[role], 7, 2 + 4 * si, .8)
            tips.append(cutp[-1])
        if lt >= t_race - .25:
            la = fa(lt, t_race - .25, .25)
            for si, (name, role, vals) in enumerate(series):                       # the label rides its line's tip: above if this line leads, below if it trails
                x, y = tips[si]; lead = (1, 0, -1)[si] if n == 3 else (1, -1)[si]               # before the lines separate: first series above, last below
                s_ = clamp(sum(clamp((tips[j][1] - y) / 20, -1, 1) for j in range(n) if j != si) + lead * 1.5 * (1 - clamp(p / .1)), -1, 1)
                w_ = tw(name, 30, "o"); cx = clamp(x - (1 - abs(s_)) * (w_ / 2 + 24), px0 + w_ / 2 + 8, px1 - w_ / 2)
                r = 11 * S; d.ellipse([X(x) - r, X(y) - r, X(x) + r, X(y) + r], fill=mix(CARD, ROLE[role], la), outline=CARD, width=int(3 * S))
                _halo(d, cx, y - 40 * s_, name, 30, "o", ROLE[role] if role != "o" else (214, 104, 8), "mm", la)
    # end values: paper tags just outside the chart's right edge, level with each line's end; the winner's is the dominant number
    ys = sorted(range(n), key=lambda i: ends[i]); ty = {}
    for r_, i in enumerate(ys): ty[i] = clamp(ends[i], 350, 880) if r_ == 0 else max(clamp(ends[i], 350, 880), ty[ys[r_ - 1]] + 112)
    for i, (name, role, vals) in enumerate(series):
        s = fmt(vals[-1]); size = _fit_size(s, 76 if i == win else 46, "a", 236); rot = -2.5 if i == win else 2
        bw = V._rot_bounds(tw(s, size, "a") + 44, size * .78 + 30, rot)[0]
        tag(base, lt, box[2] + 34 + bw / 2, ty[i], s, size, t_end + (0 if i == win else .18 * (1 + ys.index(i))), FILL[role], FG[role], rot, "a", "chime" if i == win else "pop")
    # handwritten callout on the winner (above its tag when there is room, otherwise below the lowest tag)
    lines = wrap(callout, 50, "c", 300); cx = box[2] + 34 + 130; above = ty[win] - 62 - 50 - 50 * len(lines) >= 150
    y0 = ty[win] - 62 - 50 - 50 * len(lines) if above else max(ty.values()) + 62 + 50
    for j, s in enumerate(lines): note(d, lt, cx, y0 + 50 * j, s, 50, t_callout + .12 * j, anchor="ma")
    ap = appear(lt, t_callout + .35, .4, "marker")
    if above: arrow(d, (cx - 60, y0 + 50 * len(lines) + 8), (cx - 76, ty[win] - 58), ap, INK, 5, .25)
    else: arrow(d, (cx + 136, y0 - 2), (cx + 122, ty[win] + 20), ap, INK, 5, .3) if win == ys[-1] else None
    T(d, 112, 950, label, 24, "r", MUTED, a=fa(lt, t_race + .3, .4))

# ============================================================================================ waterfall
@component("charts", "waterfall", dur=6.0, cam=[(0, 700, 520, 1.16), (1.5, MX, MY, 1.0), (6.0, MX, MY, 1.03)], still=5.3,
           use="Fees, charges or deductions eating into a figure: a whole starting bar, each deduction as an orange block stepping down on its cue, ending on the green 'what you keep' bar with the one big number.")
def waterfall(base, d, lt, cam, title="WHERE THE", title_key="MONEY GOES", key_role="o",
              start=("BEFORE FEES", 1000), steps=(("FUND FEE", 150), ("PLATFORM FEE", 100), ("ADVICE FEE", 250)),
              end_label="WHAT YOU KEEP", end_role="g", start_role="k", fmt=None, aside="half of it gone",
              label="Illustration, not real returns",
              t_title=.2, t_panel=.5, t_start=1.1, t_steps=None, t_end=None, t_aside=None):
    """start=(label, amount), steps=[(label, amount), ...]. The end bar is computed: start minus the sum of the steps (asserted).
    t_steps: one cue per step (default: every 0.55 s after the start bar)."""
    fmt = fmt or (lambda v: gbp(round(v))); n = len(steps); assert 1 <= n <= 5, "waterfall takes one to five deductions"
    levels = [start[1]]
    for _, amt in steps: assert amt > 0, "each deduction is a positive amount"; levels.append(levels[-1] - amt)
    end = levels[-1]; assert end >= 0, "deductions exceed the starting amount"
    assert abs(end - (start[1] - sum(a_ for _, a_ in steps))) < 1e-6 and abs(end + sum(a_ for _, a_ in steps) - start[1]) < 1e-6, "end bar must equal start minus the deductions"
    t_steps = [t_start + .7 + .55 * i for i in range(n)] if t_steps is None else list(t_steps); assert len(t_steps) == n
    t_end = t_steps[-1] + .8 if t_end is None else t_end; t_aside = t_end + .7 if t_aside is None else t_aside
    kline(d, lt, 110, 150, [(title, t_title, INK, None), (title_key, t_title + .3, INK, key_role)], 88, "a")
    box = (110, 290, 1810, 940); px0, px1, y0, ytop = 190, 1730, 826, 462
    pa = panel(base, lt, box, t_panel, seed=14)
    slot = (px1 - px0) / (n + 2); bw = min(slot * .66, 230); cxs = [px0 + slot * (i + .5) for i in range(n + 2)]; yv = lambda v: y0 - (y0 - ytop) * v / start[1]
    if pa >= 1:
        ga = fa(lt, t_panel + .4, .25); graph(d, box, a=ga)
        def labels(i, name, amt, col, t0):
            a = fa(lt, t0 + .1, .25)
            T(d, cxs[i], 838, name, _fit_size(name, 26, "o", slot - 18), "o", MUTED, "ma", a, CARD)
            if amt: T(d, cxs[i], 870, amt, _fit_size(amt, 40, "a", slot - 18), "a", col, "ma", a, CARD)
        # the starting whole bar
        _bar(base, lt, (cxs[0] - bw / 2, ytop, cxs[0] + bw / 2, y0), t_start, FILL[start_role], 31); labels(0, start[0], fmt(start[1]), INK, t_start)
        # each deduction: a floating orange block one step down, tied to the previous level by a thin ink line
        for i, ((name, amt), t0) in enumerate(zip(steps, t_steps)):
            ya, yb = yv(levels[i]), yv(levels[i + 1]); x = cxs[i + 1]
            ca = fa(lt, t0 - .05, .2)
            if ca > .03: d.line([X(cxs[i] + bw / 2 + 3), X(ya), X(x - bw / 2 - 3), X(ya)], fill=mix(CARD, INK, ca * .8), width=int(3 * S))
            _bar(base, lt, (x - bw / 2, ya, x + bw / 2, max(yb, ya + 8)), t0, FILL["o"], 33 + i); labels(i + 1, name, "−" + fmt(amt), (214, 104, 8), t0)
        # what you keep
        ye = yv(end); xe = cxs[-1]; ca = fa(lt, t_end - .05, .2)
        if ca > .03: d.line([X(cxs[-2] + bw / 2 + 3), X(ye), X(xe - bw / 2 - 3), X(ye)], fill=mix(CARD, INK, ca * .8), width=int(3 * S))
        _bar(base, lt, (xe - bw / 2, min(ye, y0 - 8), xe + bw / 2, y0), t_end, FILL[end_role], 39, "chime"); labels(n + 1, end_label, None, INK, t_end)
        if lt >= t_start: d.line([X(px0 - 24), X(y0 + 1), X(px1 + 24), X(y0 + 1)], fill=mix(CARD, INK, fa(lt, t_start, .2)), width=int(4 * S))
        s = fmt(end); size = _fit_size(s, 112, "a", 2 * (box[2] - 16 - xe)); cap = F("a", size).getbbox("H0"); nb = ye - 18 - cap[3] / S; ntop = nb + cap[1] / S
        room = ntop - ytop >= 62                                                    # room for the aside between the start level and the big number
        _dash(d, cxs[0] + bw / 2 + 8, (xe + bw / 2) if room else (xe - bw / 2 - 14), ytop, appear(lt, t_end + .3, .5, "marker"), MUTED)
        big(d, lt, xe, nb, s, size, t_end + .15, "g" if end_role in ("g", "n", "k") else end_role, "a", INK, CARD, "m")
        if room and aside: note(d, lt, xe, ytop + 2, aside, _fit_size(aside, 46, "c", 2 * (box[2] - 14 - xe)), t_aside, on=CARD, anchor="ma")
    T(d, 112, 950, label, 24, "r", MUTED, a=fa(lt, t_start + .2, .4))

# ============================================================================================ timeline with markers
@component("charts", "timeline_markers", dur=6.0, cam=[(0, 650, 520, 1.2), (1.9, MX, MY, 1.0), (6.0, MX, MY, 1.03)], still=5.3,
           use="A repayment or balance timeline: the year track unrolls, two to four markers pop on their cues with handwritten notes, and the gap between two of them (e.g. years saved) is highlighted as the one big figure.")
def timeline_markers(base, d, lt, cam, title="THE FINISH LINE", title_key="MOVES", key_role="o",
                     ticks=("0", "5", "10", "15", "20", "25"), unit="YEARS",
                     markers=((0.0, "TODAY", "n", "start here"), (.86, "PAID OFF", "o", "with overpayments"), (1.0, "ORIGINAL END", "m", "the plan")),
                     span=(1, 2, "3½ YEARS EARLY", "g"), label="Illustration, not real figures",
                     t_title=.2, t_panel=.5, t_track=.9, track_dur=1.0, t_markers=(1.1, 2.3, 2.9), t_span=3.7):
    """markers: (position 0-1 along the track, label, role[, handwritten note]); t_markers: one cue each.
    span: (marker index, marker index, text, role) highlights the stretch between two markers, or None."""
    n = len(markers); assert 2 <= n <= 4 and len(t_markers) == n, "two to four markers, one cue each"
    kline(d, lt, 110, 150, [(title, t_title, INK, None), (title_key, t_title + .3, INK, key_role)], 88, "a")
    box = (110, 290, 1810, 940); tx0, tx1, ty0, ty1 = 220, 1650, 690, 728
    pa = panel(base, lt, box, t_panel, seed=16)
    if pa >= 1:
        ga = fa(lt, t_panel + .4, .25); graph(d, box, a=ga); px = lambda p: tx0 + (tx1 - tx0) * p
        up = strip(base, lt, (tx0 - 14, ty0, tx1 + 14, ty1), t_track, KRAFT, track_dur, 18, "slide", rec=False); front = tx0 - 14 + (tx1 - tx0 + 70) * up
        if span and lt >= t_span:                                                   # highlighted stretch of the track
            i, j, s, role = span; xa, xb = sorted((px(markers[i][0]), px(markers[j][0])))
            strip(base, lt, (xa, ty0 - 5, xb, ty1 + 5), t_span, FILL[role], .5, 19, "slide", rec=False)
        for k, s in enumerate(ticks):
            x = px(k / (len(ticks) - 1)); a = clamp((front - x) / 40)
            if a > .03:
                d.line([X(x), X(ty1 + 2), X(x), X(ty1 + 18)], fill=mix(CARD, INK, a), width=int(4 * S)); T(d, x, ty1 + 22, s, 28, "o", MUTED, "ma", a, CARD)
        if unit: T(d, tx1 + 40, (ty0 + ty1) / 2, unit, 24, "o", MUTED, "lm", fa(lt, t_track + track_dur, .3), CARD)
        order = sorted(range(n), key=lambda i: markers[i][0])
        for rank, i in enumerate(order):
            pos, name, role = markers[i][:3]; hand = markers[i][3] if len(markers[i]) > 3 else None; t0 = t_markers[i]
            appear(lt, t0, .4, "pop")
            if lt < t0: continue
            x = px(pos); dy = 612 if rank % 2 == 0 else 470; g = eout((lt - t0) / .3); e = back((lt - t0 - .12) / .32)
            d.line([X(x), X(ty0 - 2), X(x), X(ty0 - 2 - (ty0 - 2 - dy) * g)], fill=INK, width=int(4 * S))
            r = 19 * e * S
            if r > 1: d.ellipse([X(x) - r, X(dy) - r, X(x) + r, X(dy) + r], fill=FILL[role], outline=INK, width=int(4 * S))
            w_ = tw(name, 34, "o"); cx = clamp(x, box[0] + 22 + w_ / 2, box[2] - 22 - w_ / 2)
            _halo(d, cx, dy - 50, name, 34, "o", INK, "mm", fa(lt, t0 + .2, .25))
            if hand:
                w2 = tw(hand, 40, "c"); cx2 = clamp(x, box[0] + 22 + w2 / 2, box[2] - 22 - w2 / 2)
                note(d, lt, cx2, dy - 122, hand, 40, t0 + .45, MUTED if role == "m" else INK, CARD, "ma")
        if span:
            i, j, s, role = span; xa, xb = sorted((px(markers[i][0]), px(markers[j][0]))); by = ty1 + 88
            stroke(d, [(xa, by - 16), (xa, by), (xb, by), (xb, by - 16)], appear(lt, t_span + .25, .4, "marker"), INK, 5, 21, .6)
            size = _fit_size(s, 66, "a", 900); w_ = tw(s, size, "a"); cx = clamp((xa + xb) / 2, box[0] + 30 + w_ / 2, box[2] - 30 - w_ / 2)
            big(d, lt, cx, by + 10, s, size, t_span + .45, role if role in HLC else "g", "a", INK, CARD, "m"); chime(lt, t_span + .45)
    T(d, 112, 950, label, 24, "r", MUTED, a=fa(lt, t_track + .3, .4))
