"""Shorts 9:16 components (stage 1080 x 1920): vertical re-compositions of the landscape hooks, comparisons and number reveals.

Run with FF_ORIENT=v. Every text sits inside the Shorts safe area (x 110-870, y 290-1440); the designs stay inside
x 130-850, y 320-1400 so the small camera move (1.03 -> 1.0 -> 1.02) never pushes text out. The safe area is centred on
x = 490, not on the frame centre, so every layout is centred there. Nothing is drawn below y 1400: burned-in captions go there.
All figures, strings, colour roles and cue times are parameters; the defaults are round illustrations, never real figures.
"""
from kit import *
assert ORIENT == "v", "shorts.py is the 9:16 set: run with FF_ORIENT=v"

L_, R_, CXS = 130, 850, 490                               # design column inside the safe area, and its centre
FILL = {"o": ORANGE, "b": BLUE, "g": GREEN, "k": KRAFT, "n": INK, "r": RED}        # paper colour for a role
FG = {"o": INK, "b": CARD, "g": INK, "k": INK, "n": CREAM, "r": CARD}              # text colour on that paper
INKC = {"o": ORANGE, "b": BLUE, "g": DGREEN, "k": BROWN, "n": INK, "r": RED}       # marker / figure colour on light paper
def camv(dur): return [(0, MX, MY, 1.03), (1.1, MX, MY, 1.0), (dur - 1.6, MX, MY, 1.0), (dur, MX, MY, 1.02)]

# ---------------- module helpers ----------------
def cap(f, size):
    """(offset of the cap top below the 'la' anchor, cap height) in stage px."""
    bb = F(f, size).getbbox("H0"); return bb[1] / S, (bb[3] - bb[1]) / S
def fz(s, size, f, maxw):
    """Largest size <= `size` at which s fits maxw."""
    w = tw(s, size, f); return size if w <= maxw else size * maxw / w
def TB(d, x, ytop, s, size, f="o", fill=INK, al="m", a=1.0, on=PAPER, dy=0.0, maxw=None):
    """Text placed by its cap top (so layouts are exact whatever the font). al: l / m / r."""
    if maxw: size = fz(s, size, f, maxw)
    T(d, x, ytop + cap(f, size)[1], s, size, f, fill, {"l": "ls", "m": "ms", "r": "rs"}[al], a, on, dy)
def head(d, lt, ytop, lines, size, t0, x=CXS, align="m", on=PAPER, maxw=700, step=.32):
    """Anton headline, one kinetic line per entry: lines = ((text, highlighter key or None), ...). Returns the bottom y."""
    size = min(fz(s, size, "a", maxw) for s, _ in lines); ct, ch = cap("a", size); y = ytop
    for i, (s, hk) in enumerate(lines):
        kline(d, lt, x, y - ct, [(s, t0 + i * step, INK, hk)], size, "a", align, on); y += ch * 1.32
    return y - ch * .32
def fig(d, lt, x, ytop, v, size, t0, fill=INK, al="m", on=PAPER, maxw=None, dur=.9, hk=None, t_hk=None, f="a", snd=True):
    """A figure placed by its cap top. A number counts up from zero (ticks last exactly as long as the count); a string pops in.
    hk adds a highlighter swipe (at t_hk, default when the count stops). Returns its final box."""
    num = not isinstance(v, str); final = gbp(v) if num else v
    if maxw: size = fz(final, size, f, maxw)
    w = tw(final, size, f); ct, ch = cap(f, size); x0 = x - (w if al == "r" else w / 2 if al == "m" else 0); box = (x0, ytop, x0 + w, ytop + ch)
    if num: appear(lt, t0, dur, "ticks" if snd else None); s = gbp(round(v * ease((lt - t0) / dur)))
    else: appear(lt, t0, .3, "pop" if snd else None); s = final
    if hk:
        ph = appear(lt, t_hk if t_hk is not None else t0 + (dur if num else .3), .45, "marker")
        if lt >= t0: hl(d, box[0], ytop + ch * .04, box[2], ytop + ch * 1.08, mix(on, HLC[hk], .95), ph)
    a = clamp((lt - t0) / .2)
    if a > .03:
        sc = .6 + .4 * back((lt - t0) / .32); xa = {"l": x0, "m": x0 + w / 2, "r": x0 + w}[al]
        T(d, xa, ytop + ch / 2 + ch * sc / 2, s, size * sc, f, fill, {"l": "ls", "m": "ms", "r": "rs"}[al], a, on)
    return box
def blob(base, cam, kind, x, y, k=.2):
    """Soft colour blob behind the layout with a little parallax (vertical-safe replacement for vlib.deco)."""
    sp = deco_sprite(kind); base.paste(sp, (int(X(x + (cam[0] - MX) * k) - sp.size[0] / 2), int(X(y + (cam[1] - MY) * k) - sp.size[1] / 2)), sp)
def notes(d, lt, x, ytop, lines, size, t0, fill=INK, on=PAPER, al="l", maxw=420, pitch=1.12):
    """Handwritten (Caveat) lines that fade up one after another. Returns the bottom y."""
    lines = [lines] if isinstance(lines, str) else list(lines); size = min(fz(s, size, "c", maxw) for s in lines); y = ytop
    for i, s in enumerate(lines):
        t = t0 + i * .18; TB(d, x, y, s, size, "c", fill, al, ease((lt - t) / .3), on, dy=10 * (1 - eout((lt - t) / .3))); y += size * pitch
    return y
@lru_cache(maxsize=8)
def _tape(w, h, rot):
    tp = Image.new("RGBA", (int(w * S), int(h * S)), (236, 226, 190, 170)); td = ImageDraw.Draw(tp)
    for xx in (0, tp.size[0] - 2): td.line([(xx, 0), (xx, tp.size[1])], fill=(236, 226, 190, 90), width=3)
    return tp.rotate(rot, Image.BICUBIC, expand=True)
def tape(base, cx, cy, a=1.0, w=150, h=44, rot=-4):
    sp = _tape(w, h, rot); paste(base, sp, X(cx) - sp.size[0] / 2, X(cy) - sp.size[1] / 2, a)

# =====================================================================================================
# shorts_hooks
# =====================================================================================================
@component("shorts_hooks", "number_transform", dur=5.5, cam=camv(5.5), still=4.6,
           use="Open a Short on a small everyday figure that counts up into the consequence number on a calculation card, highlighted as it is spoken.")
def number_transform(base, d, lt, cam, headline=(("A SMALL SUM", None), ("ADDS UP", "o")), start=100, start_top="PUT IN", start_sub="A MONTH",
                     end=30000, end_top="THAT COMES TO", end_sub="OVER 25 YEARS", note_lines=("example: £100 x 300", "months, no growth"),
                     picture="coins", role="o", t_head=.15, t_card=.25, t_start=.5, t_turn=1.5, t_hl=2.5, t_pic=3.0, t_note=3.4, count_dur=.9):
    col = INKC[role]; blob(base, cam, "blobO" if role == "o" else "blobB" if role == "b" else "blobG", 760, 520); blob(base, cam, "blobK", 200, 1330, .12)
    head(d, lt, 332, headline, 104, t_head)
    box = (L_, 610, R_, 1110); a = panel(base, lt, box, t_card, CARD, seed=21)
    if a > .5:
        ruled(d, box, fa(lt, t_card + .2))
        morph(d, lt, CXS, 678, [(t_start, start_top, MUTED), (t_turn, end_top, MUTED)], 46, "o", "mm", CARD, dur=.2, snd=None, grow=.04)
        s0, s1 = (gbp(start) if not isinstance(start, str) else start), (gbp(end) if not isinstance(end, str) else end)
        size = fz(s1, 200, "a", 600); ct, ch = cap("a", size); ymid = 850; w1 = tw(s1, size, "a")
        ph = appear(lt, t_hl, .45, "marker")
        if ph > .01: hl(d, CXS - w1 / 2, ymid - ch * .46, CXS + w1 / 2, ymid + ch * .58, mix(CARD, HLC[role], .95), ph)
        if isinstance(start, str) or isinstance(end, str): morph(d, lt, CXS, ymid, [(t_start, s0, INK), (t_turn, s1, INK)], size, "a", "mm", CARD)
        elif lt >= t_start:
            appear(lt, t_turn, count_dur, "ticks"); u = clamp((lt - t_turn) / count_dur); v = start + (end - start) * ease(u)
            sc = (.6 + .4 * back((lt - t_start) / .35)) * (1 + .07 * math.sin(math.pi * u))
            T(d, CXS, ymid + ch * sc / 2, gbp(round(v)), size * sc, "a", INK, "ms", min(1, (lt - t_start) / .2), CARD)
        morph(d, lt, CXS, 1022, [(t_start + .15, start_sub, INK), (t_turn + .1, end_sub, INK)], 60, "o", "mm", CARD, dur=.2, snd=None, grow=.04)
        chime(lt, t_hl + .1)
    cut(base, lt, picture, 250, 1270, 150, t_pic, rot=-5, disc=(role if role in DISC else "k", 96))
    notes(d, lt, 400, 1218, note_lines, 60, t_note, MUTED, maxw=440)

@component("shorts_hooks", "two_paths", dur=6.0, cam=camv(6.0), still=5.0,
           use="Open a Short on a choice: one sum splits down an orange path and a blue path, each ending in its own figure, then the question.")
def two_paths(base, d, lt, cam, headline=(("SAME MONEY,", None), ("TWO PATHS", "o")), token_text="£100", a_label="OVERPAY", a_value="£24,000", a_pic="house",
              b_label="INVEST", b_value="£31,000", b_pic="chart", a_role="o", b_role="b", question="which one wins?",
              t_head=.15, t_token=.7, t_a=1.3, t_b=1.6, t_a_tag=2.0, t_b_tag=2.4, t_q=3.4):
    blob(base, cam, "blobO", 170, 980); blob(base, cam, "blobB", 840, 980)
    head(d, lt, 332, headline, 90, t_head)
    tag(base, lt, CXS, 596, token_text, 100, t_token, INK, CREAM, -2, "a", "pop", (30, 16))
    for (role, t0, tt, x1, lab, val, pic, rot, sd) in ((a_role, t_a, t_a_tag, 300, a_label, a_value, a_pic, -3, 5), (b_role, t_b, t_b_tag, 680, b_label, b_value, b_pic, 3, 9)):
        sgn = -1 if x1 < CXS else 1
        arrow(d, (CXS + sgn * 46, 676), (x1 + sgn * 6, 778), appear(lt, t0, .55, "marker"), INKC[role], 10, bend=-.22 * sgn, seed=sd)
        cut(base, lt, pic, x1, 890, 118, t0 + .45, rot=rot * 1.5, disc=(role, 80), sfx=None)
        vs = fz(val, 84, "a", 286)
        tag(base, lt, x1, 1140, ((lab, 40, "o"), (val, vs, "a")), 0, tt, FILL[role], FG[role], rot, "o", "pop", (22, 16))
    s = fz(question, 88, "c", 640); ct, ch = cap("c", s)
    TB(d, CXS, 1284, question, s, "c", INK, "m", fa(lt, t_q), dy=12 * (1 - eout((lt - t_q) / .3)))
    w = tw(question, s, "c"); underline(d, CXS - w / 2, CXS + w / 2, 1284 + ch + 24, appear(lt, t_q + .45, .4, "marker"), ORANGE, 7)

@component("shorts_hooks", "myth_vs_reality", dur=6.0, cam=camv(6.0), still=5.0,
           use="Open a Short by striking out a common belief, then drop in the real figure highlighted underneath.")
def myth_vs_reality(base, d, lt, cam, myth_kicker="PEOPLE SAY", myth="YOU NEED A BIG LUMP SUM TO START", myth_tag="MYTH", reality_tag="REALITY",
                    reality_lead="YOU CAN START WITH", figure="£25", figure_sub="A MONTH", note_text="example figure", picture="piggybank", role="g",
                    t_card=.15, t_myth=.35, t_cross=1.2, t_tag=1.6, t_reality=2.1, t_lead=2.3, t_fig=2.6, t_pic=3.1, t_note=3.8):
    blob(base, cam, "blobG" if role == "g" else "blobB" if role == "b" else "blobO", 760, 1150)
    size = 84; lines = wrap(myth, size, "a", 640)
    while len(lines) > 3: size -= 4; lines = wrap(myth, size, "a", 640)
    ct, ch = cap("a", size); oy = (3 - len(lines)) * ch * 1.34                 # a shorter myth makes a shorter card (bottom edge fixed)
    box = (L_, 332 + oy, R_, 752); a = panel(base, lt, box, t_card, CARD, seed=14)
    if a > .5:
        TB(d, 170, 368 + oy, myth_kicker, 42, "o", MUTED, "l", fa(lt, t_card + .2), CARD)
        dim = ease((lt - t_cross - .3) / .5); y = 446 + oy
        for i, s in enumerate(lines):
            t0 = t_myth + i * .22; TB(d, 170, y, s, size, "a", mix(INK, LIGHT, dim * .8), "l", fa(lt, t0, .22), CARD, dy=-20 * (1 - back((lt - t0) / .26)))
            stroke(d, [(160, y + ch * .56), (170 + tw(s, size, "a") / 2, y + ch * .44), (182 + tw(s, size, "a"), y + ch * .52)],
                   appear(lt, t_cross + i * .16, .3, "marker" if i == 0 else None), RED, 10, 30 + i, 1.6)
            y += ch * 1.34
        tag(base, lt, 716, 398 + oy, myth_tag, 60, t_tag, RED, CARD, -7, "a", "pop", (20, 12))
    tag(base, lt, L_ + tw(reality_tag, 56, "a") / 2 + 34, 846, reality_tag, 56, t_reality, FILL[role], FG[role], 3, "a", "pop", (24, 14))
    ls = fz(reality_lead, 76, "a", 700); kline(d, lt, L_, 914 - cap("a", ls)[0], [(reality_lead, t_lead, INK, None)], ls, "a")
    fig(d, lt, L_ + 8, 1010, figure, 220, t_fig, INK, "l", maxw=410, hk=role if role in HLC else "o")
    TB(d, L_ + 8, 1238, figure_sub, 58, "o", INK, "l", fa(lt, t_fig + .35), maxw=410)
    cut(base, lt, picture, 704, 1150, 170, t_pic, rot=5, disc=(role if role in DISC else "k", 110))
    notes(d, lt, L_ + 8, 1326, note_text, 54, t_note, MUTED, maxw=600)
    chime(lt, t_fig + .5)

# =====================================================================================================
# shorts_comparisons
# =====================================================================================================
@component("shorts_comparisons", "versus_card", dur=5.5, cam=camv(5.5), still=4.6,
           use="Compare two options head to head in a Short: two stacked cards with a VS disc between, the winner ringed and tagged.")
def versus_card(base, d, lt, cam, a_label="OPTION A", a_value=24000, a_sub="AFTER 10 YEARS", a_pic="house", a_role="o",
                b_label="OPTION B", b_value=31000, b_sub="AFTER 10 YEARS", b_pic="chart", b_role="b", winner="b", win_text="AHEAD",
                t_a=.15, t_b=.45, t_vs=.9, t_fig=1.2, t_win=2.9, count_dur=.9):
    for k, (y0, t0, lab, val, sub, pic, role, sd) in enumerate(((330, t_a, a_label, a_value, a_sub, a_pic, a_role, 4), (905, t_b, b_label, b_value, b_sub, b_pic, b_role, 6))):
        box = (L_, y0, R_, y0 + 465); win = winner == "ab"[k]; a = panel(base, lt, box, t0, CARD, seed=sd, frm=((-60, 0) if k == 0 else (60, 0)))
        if a < .5: continue
        p = strip(base, lt, (L_, y0, R_, y0 + 88), t0 + .3, FILL[role], .45, sd + 20, None)
        if p >= .999: TB(d, 164, y0 + 27, lab, 48, "o", FG[role], "l", fa(lt, t0 + .75, .2), FILL[role], maxw=360)
        cut(base, lt, pic, 272, y0 + 286, 150, t0 + .55, rot=-4 if k == 0 else 4, disc=(role, 98), sfx="pop" if k == 0 else None)
        lose = (winner in ("a", "b") and not win) * ease((lt - t_win) / .5)
        bx = fig(d, lt, 800, y0 + 196, val, 150, t_fig + k * .15, mix(INK, LIGHT, lose * .75), "r", CARD, maxw=370, dur=count_dur, snd=k == 0)
        TB(d, 800, y0 + 196 + (bx[3] - bx[1]) + 36, sub, 40, "o", MUTED, "r", fa(lt, t_fig + k * .15 + .3), CARD, maxw=370)
        if win:
            ring(d, (bx[0] - 22, bx[1] - 24, bx[2] + 14, bx[3] + 26), appear(lt, t_win, .5, "marker"), INKC["g"], 8, 3 + k)
            if p >= .999: tag(base, lt, 812 - tw(win_text, 36, "o") / 2 - 16, y0 + 44, win_text, 36, t_win + .4, GREEN, INK, -3, "o", "chime", (16, 9))
    e = back(clamp((lt - t_vs) / .4)); appear(lt, t_vs, .4, "pop")
    if lt >= t_vs and e > .05:
        r = 68; b = rot_paste(base, panel_sprite(int(2 * r * S), int(2 * r * S), INK, 11, True), CXS, 850, 0, e); rec("c", (CXS - r * e, 850 - r * e, CXS + r * e, 850 + r * e), "vs disc")
        ch = cap("a", 58 * e)[1]; T(d, CXS, 850 + ch / 2, "VS", 58 * e, "a", CREAM, "ms", min(1, e), INK)

@component("shorts_comparisons", "two_jars", dur=6.0, cam=camv(6.0), still=5.0,
           use="Compare two end amounts in a Short as two jars filling to their true proportions, with the difference written underneath.")
def two_jars(base, d, lt, cam, headline=(("SAME MONEY IN,", None), ("TWO JARS", "b")), a_label="OVERPAY", a_value=24000, a_role="o",
             b_label="INVEST", b_value=31000, b_role="b", note_text="£7,000 more in this jar", note_side="b",
             t_head=.15, t_jars=.9, t_fill=1.5, t_note=3.6, fill_dur=1.3):
    blob(base, cam, "blobK", 490, 900, .12)
    head(d, lt, 332, headline, 80, t_head)
    top = max(a_value, b_value, 1); bxs = {}
    stroke(d, [(150, 1086), (490, 1082), (830, 1087)], appear(lt, t_jars - .1, .5, "marker"), INK, 6, 12, 1.0)          # the shelf
    for k, (cx, lab, val, role) in enumerate(((300, a_label, a_value, a_role), (680, b_label, b_value, b_role))):
        t0 = t_jars + k * .2; filling = t_fill <= lt < t_fill + fill_dur
        jar(base, d, lt, cx, 880, t0, .94 * val / top * ease((lt - t_fill) / fill_dur), DISC[role], (2.4, t_fill) if filling else None, w=112, h=190)
        tag(base, lt, cx, 560, lab, 46, t0 + .25, FILL[role], FG[role], -2 if k == 0 else 2, "o", None, (22, 13))
        bxs["ab"[k]] = fig(d, lt, cx, 1124, val, 100, t_fill, INKC[role], "m", maxw=330, dur=fill_dur, snd=k == 0)
    chime(lt, t_fill + fill_dur)
    s = fz(note_text, 62, "c", 660); TB(d, CXS, 1286, note_text, s, "c", INK, "m", fa(lt, t_note), dy=10 * (1 - eout((lt - t_note) / .3)))
    if note_side in bxs:
        bx = bxs[note_side]; underline(d, bx[0], bx[2], bx[3] + 20, appear(lt, t_note + .3, .4, "marker"), INKC[b_role if note_side == "b" else a_role], 7)

TEAR = 858
@lru_cache(maxsize=8)
def _split_sprites(top_fill, bot_fill):
    """Top sheet with a torn lower edge (a white torn fibre edge shows under the tint) and a plain lower sheet. Canvas px."""
    hpx = int(X(TEAR))
    def torn(seed, extra, jit):
        r = random.Random(seed); pts = [(0, 0), (CW, 0)]; x = float(CW)
        while x > 0: pts.append((x, hpx + extra + r.uniform(-jit, jit) + 9 * math.sin(x / 113 + seed))); x -= r.uniform(12, 30)
        pts.append((0, hpx + extra)); m = Image.new("L", (CW, hpx + 90), 0); ImageDraw.Draw(m).polygon(pts, fill=255); return m
    white = V._paper_from_mask(torn(3, 15, 7), CARD, 7, .4, (0, 9), 9); tint = V._paper_from_mask(torn(8, -6, 6), top_fill, 9, 0)
    white.alpha_composite(tint); hb = CH - hpx + int(60 * S)
    return white, V._paper_from_mask(Image.new("L", (CW, hb), 255), bot_fill, 5, 0), hpx
@component("shorts_comparisons", "split_screen", dur=5.5, cam=camv(5.5), still=4.6,
           use="Set two options against each other in a Short as two torn paper halves, orange above and blue below, one figure each.")
def split_screen(base, d, lt, cam, a_label="OVERPAY", a_value="£24,000", a_sub="INTEREST SAVED", a_pic="house", a_role="o",
                 b_label="INVEST", b_value="£31,000", b_sub="POT AT THE END", b_pic="chart", b_role="b",
                 t_split=.1, t_a=.6, t_a_fig=.9, t_b=1.7, t_b_fig=2.0, t_mark=3.2):
    ta, tb = mix(PAPER, FILL[a_role], .30), mix(PAPER, FILL[b_role], .24); top, bot, hpx = _split_sprites(ta, tb)
    e = eout((lt - t_split) / .55); appear(lt, t_split, .55, "slide")
    if lt >= t_split:
        paste(base, bot, 0, hpx - int(60 * S) + (1 - e) * 1100 * S); paste(base, top, 0, -(1 - e) * 1100 * S)
    if e < .995: return
    rec("c", (-BLEED, -BLEED, W + BLEED, TEAR - 16), "top half"); rec("c", (-BLEED, TEAR + 24, W + BLEED, H + BLEED), "bottom half")
    for k, (y0, t0, tf, lab, val, sub, pic, role, on) in enumerate(((330, t_a, t_a_fig, a_label, a_value, a_sub, a_pic, a_role, ta), (912, t_b, t_b_fig, b_label, b_value, b_sub, b_pic, b_role, tb))):
        left = k == 0                                       # top half: picture left, figure right; bottom half mirrored
        tag(base, lt, L_ + tw(lab, 50, "o") / 2 + 28, y0 + 44, lab, 50, t0, FILL[role], FG[role], -2 if left else 2, "o", "pop", (24, 14))
        cut(base, lt, pic, 268 if left else 712, y0 + 300, 160, t0 + .2, rot=-5 if left else 5, disc=("w", 106), sfx=None)
        xa, al = (842, "r") if left else (L_ + 6, "l")
        bx = fig(d, lt, xa, y0 + 196, val, 160, tf, INK, al, on, maxw=400, snd=True)
        TB(d, xa, bx[3] + 44, sub, 44, "o", mix(on, INK, .78), al, fa(lt, tf + .3), on, maxw=400)
        underline(d, bx[0], bx[2], bx[3] + 20, appear(lt, t_mark + k * .3, .4, "marker"), INKC[role], 8, 7 + k)

# =====================================================================================================
# shorts_reveals
# =====================================================================================================
@lru_cache(maxsize=16)
def _stamp_sprite(text, size, col, rot, seed=5):
    """Rubber-stamp word: double border, uneven ink (blotchy pressure plus speckle), rotated. RGBA, canvas px."""
    fo = font("a", int(round(size * S))); tl = int(fo.getlength(text)); bb = fo.getbbox("H0"); chh = bb[3] - bb[1]
    px, py, m = int(44 * S), int(36 * S), 10; w, h = tl + 2 * px, chh + 2 * py
    im = Image.new("L", (w + 2 * m, h + 2 * m), 0); dd = ImageDraw.Draw(im)
    dd.rounded_rectangle([m, m, m + w, m + h], int(18 * S), outline=255, width=int(9 * S))
    i2 = int(16 * S); dd.rounded_rectangle([m + i2, m + i2, m + w - i2, m + h - i2], int(8 * S), outline=255, width=int(3 * S))
    dd.text((m + w / 2, m + py + chh), text, font=fo, fill=255, anchor="ms")
    rng = np.random.default_rng(seed); shp = (im.size[1], im.size[0])
    n1 = cv2.GaussianBlur(rng.standard_normal(shp).astype(np.float32), (0, 0), 16); n1 /= n1.std()
    n2 = cv2.GaussianBlur(rng.standard_normal(shp).astype(np.float32), (0, 0), 1.3); n2 /= n2.std()
    k = np.clip(.84 + .2 * n1, .38, 1) * np.clip((n2 + 1.5) * 2.2, 0, 1)
    al = cv2.GaussianBlur(np.asarray(im, np.float32) * k, (0, 0), .7)
    out = Image.new("RGBA", im.size, tuple(col) + (0,)); out.putalpha(Image.fromarray(np.clip(al, 0, 255).astype(np.uint8)))
    return out.rotate(rot, Image.BICUBIC, expand=True)
@component("shorts_reveals", "stamp", dur=4.5, cam=camv(4.5), still=3.8,
           use="Land a verdict on a figure in a Short: the number sits on a card and a rubber-stamp word thumps down beneath it.")
def stamp(base, d, lt, cam, label="TOTAL INTEREST", value="£24,000", sub="OVER 25 YEARS", stamp_text="SAVED", stamp_role="g", note_text="example figure",
          t_card=.15, t_fig=.4, t_stamp=1.9, t_note=2.8, stamp_rot=-8):
    blob(base, cam, "blobK", 800, 1180, .15)
    box = (140, 372, 840, 862); a = panel(base, lt, box, t_card, CARD, seed=17)
    if a > .5:
        tape(base, CXS, 372, fa(lt, t_card + .25))
        TB(d, CXS, 440, label, 46, "o", MUTED, "m", fa(lt, t_card + .25), CARD, maxw=620)
        bx = fig(d, lt, CXS, 530, value, 210, t_fig, INK, "m", CARD, maxw=600)
        TB(d, CXS, 770, sub, 50, "o", INK, "m", fa(lt, t_fig + .35), CARD, maxw=620)
    size = 130
    while size > 60 and tw(stamp_text, size, "a") + 88 > 470: size -= 4
    appear(lt, t_stamp, .2, "pop")
    if lt >= t_stamp:
        u = clamp((lt - t_stamp) / .16); sc = 1 + .28 * (1 - eout(u)) + .03 * math.sin(math.pi * clamp((lt - t_stamp - .16) / .18))
        b = rot_paste(base, _stamp_sprite(stamp_text, size, INKC[stamp_role], stamp_rot), CXS, 1092, 0, sc, min(1, .35 + u)); rec("t", b, stamp_text)
    notes(d, lt, CXS, 1300, note_text, 56, t_note, MUTED, al="m", maxw=640)

@lru_cache(maxsize=16)
def _odo(cw, ch, size):
    """Digit strip 0-9-0 (canvas px), the rounded window mask and the top/bottom shading of an odometer cell."""
    fo = font("a", size); bb = fo.getbbox("H0"); chh = bb[3] - bb[1]
    stp = Image.new("RGB", (cw, ch * 11), CARD); dd = ImageDraw.Draw(stp)
    for i in range(11):
        dd.text((cw / 2, i * ch + ch / 2 + chh / 2), str(i % 10), font=fo, fill=INK, anchor="ms"); dd.line([(0, i * ch), (cw, i * ch)], fill=mix(CARD, INK, .12), width=2)
    mask = Image.new("L", (cw, ch), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw - 1, ch - 1], int(10 * S), fill=255)
    g = np.abs(np.linspace(-1, 1, ch, dtype=np.float32)) ** 2.4 * 120; sh = np.zeros((ch, cw, 4), np.uint8); sh[:, :, 3] = g[:, None].astype(np.uint8)
    sh[:, :, :3] = INK; shade = Image.fromarray(sh, "RGBA"); shade.putalpha(Image.fromarray(np.minimum(sh[:, :, 3], np.asarray(mask))))
    return stp, mask, shade, chh
@component("shorts_reveals", "rolling_counter", dur=5.0, cam=camv(5.0), still=4.2,
           use="Reveal a total in a Short with tension: odometer digits roll and lock, left to right, onto the final figure.")
def rolling_counter(base, d, lt, cam, label="TOTAL INTEREST", value=48250, sub="OVER 25 YEARS", note_lines=("that's about", "£160 a month"), picture="calculator", role="o",
                    t_label=.15, t_panel=.3, t_roll=.6, t_sub=2.4, t_pic=2.8, t_note=3.1, roll_dur=1.7):
    blob(base, cam, "blobO" if role == "o" else "blobB" if role == "b" else "blobG", 780, 1230)
    tag(base, lt, CXS, 432, label, fz(label, 54, "o", 600), t_label, FILL["k"], INK, -2, "o", "pop", (28, 16))
    box = (L_, 540, R_, 850); a = panel(base, lt, box, t_panel, INK, seed=23)
    s = gbp(value) if not isinstance(value, str) else value; n = len(s); nc = s.count(",") + s.count("."); gap, cmw = 8, 30
    cw = min(108, (660 - nc * cmw - (n - 1) * gap) / max(1, n - nc)); ch = 196; tot = (n - nc) * cw + nc * cmw + (n - 1) * gap
    x = CXS - tot / 2; y0 = 695 - ch / 2; af = fa(lt, t_panel + .3, .25); appear(lt, t_roll, roll_dur, "ticks")
    if a > .5 and af > .03:
        cwp, chp = int(cw * S), int(ch * S); stp, mask, shade, chh = _odo(cwp, chp, int(min(170, cw * 1.72) * S))
        digs = [c for c in s if c.isdigit()]; nd = len(digs); di = 0; m2 = mask if af >= 1 else mask.point(lambda v: int(v * af))
        for c in s:
            if c in ",.":
                T(d, x + cmw / 2, y0 + ch - 34, c, 110, "a", CREAM, "ms", af, INK); x += cmw + gap; continue
            if c.isdigit():
                u = clamp((lt - t_roll) / (roll_dur * (.5 + .5 * (di + 1) / nd))); pos = (int(c) + 10 * (2 + di)) * eout(u) if lt >= t_roll else 0.0; di += 1
            else: pos = None
            if pos is None:
                cell = Image.new("RGB", (cwp, chp), CARD); ImageDraw.Draw(cell).text((cwp / 2, chp / 2 + chh / 2), c, font=font("a", int(min(170, cw * 1.72) * S)), fill=INKC[role], anchor="ms")
            else: off = int((pos % 10) * chp); cell = stp.crop((0, off, cwp, off + chp))
            base.paste(cell, (int(X(x)), int(X(y0))), m2); base.paste(shade, (int(X(x)), int(X(y0))), shade if af >= 1 else shade.getchannel("A").point(lambda v: int(v * af)))
            x += cw + gap
        rec("t", (CXS - tot / 2, y0, CXS + tot / 2, y0 + ch), s)
        done = lt >= t_roll + roll_dur
        d.line([X(CXS - tot / 2 - 8), X(695), X(CXS - tot / 2 - 2), X(695)], fill=FILL[role], width=int(5 * S)); d.line([X(CXS + tot / 2 + 2), X(695), X(CXS + tot / 2 + 8), X(695)], fill=FILL[role], width=int(5 * S))
    chime(lt, t_roll + roll_dur)
    ss = fz(sub, 58, "o", 640); TB(d, CXS, 910, sub, ss, "o", INK, "m", fa(lt, t_sub), dy=12 * (1 - eout((lt - t_sub) / .3)))
    w = tw(sub, ss, "o"); underline(d, CXS - w / 2, CXS + w / 2, 910 + cap("o", ss)[1] + 22, appear(lt, t_sub + .35, .4, "marker"), INKC[role], 7)
    cut(base, lt, picture, 262, 1200, 160, t_pic, rot=-5, disc=(role if role in DISC else "k", 106))
    notes(d, lt, 420, 1134, note_lines, 66, t_note, INK, maxw=420)

@component("shorts_reveals", "circled_figure", dur=5.0, cam=camv(5.0), still=4.2,
           use="Single out one figure in a Short: it lands big, a marker ring is drawn round it and a handwritten note points at it.")
def circled_figure(base, d, lt, cam, headline=(("THAT'S AN EXTRA", None),), value="£7,000", sub="OVER 25 YEARS", note_lines=("more than", "you put in"),
                   picture="jar", role="o", t_head=.15, t_fig=.6, t_ring=1.5, t_sub=2.0, t_note=2.7, t_pic=3.1):
    blob(base, cam, "blobO" if role == "o" else "blobB" if role == "b" else "blobG", 220, 1260)
    hb = head(d, lt, 348, headline, 96, t_head)
    bx = fig(d, lt, CXS, 610, value, 230, t_fig, INK, "m", maxw=560)
    ring(d, (bx[0] - 46, bx[1] - 52, bx[2] + 40, bx[3] + 56), appear(lt, t_ring, .6, "marker"), INKC[role], 10, 3)
    yb = bx[3] + 56 * 1.06 + 50; TB(d, CXS + 60, yb, sub, 54, "o", INK, "m", fa(lt, t_sub), dy=12 * (1 - eout((lt - t_sub) / .3)), maxw=440)
    ny = 1128; notes(d, lt, 150, ny, note_lines, 70, t_note, INK, maxw=390)
    arrow(d, (236, ny - 22), (212, bx[3] + 96), appear(lt, t_note + .35, .5, "marker"), INK, 6, bend=-.22, seed=8)
    cut(base, lt, picture, 690, 1232, 170, t_pic, rot=5, disc=(role if role in DISC else "k", 112))
    chime(lt, t_ring + .5)
