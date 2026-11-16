"""Recap and end cards: recap_checklist (three ticked lines on a sheet), recap_cards (three numbered takeaway cards and the
limitation) and end_card (the plain end screen: left half empty for YouTube's video element, logo and subscribe line right)."""
from kit import *

ROLE = {"o": ORANGE, "b": BLUE, "g": DGREEN, "k": BROWN, "n": INK}
def _cap(f, size):
    bb = F(f, size).getbbox("H0"); return (bb[3] - bb[1]) / S

# ------------------------------------------------------------------ recap checklist
@component("endcards", "recap_checklist", dur=5.5, cam=[(0, 720, 430, 1.15), (1.3, 960, 540, 1.0), (5.5, 960, 540, 1.03)], still=5.0,
           use="The recap before the end card: three short lines, each ticked off as the narrator says it, with its key figure picked out.")
def recap_checklist(base, d, lt, cam, headline="THE SHORT", key_word="VERSION", hk="g",
                    lines=(("Paying in", "£100", "a month adds up", "o"), ("Left for", "10 years", "it has time to grow", "b"), ("At an example", "5%", "that is the gap", "g")),
                    key_line=2, side_pic="scale", t_head=.15, t_sheet=.6, t_lines=(1.2, 2.2, 3.2)):
    """lines: (before, figure, after, colour role). key_line: index of the line whose figure also gets a highlighter swipe (or None)."""
    x0, y0, x1, y1 = 200, 320, 1340, 900; n = len(lines); stepy = (y1 - y0 - 60) / n
    deco(base, cam, "blobG", 1590, 620, .25); deco(base, cam, "dots", 1740, 230, .15)
    kline(d, lt, 110, 150, [(headline, t_head, INK, None), (key_word, t_head + .3, INK, hk)], 84, "a")
    a = panel(base, lt, (x0, y0, x1, y1), t_sheet, CARD, seed=27, frm=(0, 60))
    if a > .02:
        for i, (pre, fig, post, role) in enumerate(lines):
            ym = y0 + 30 + stepy * (i + .5); t0 = t_lines[i]; al = fa(lt, t0, .3); bx = x0 + 70
            if i: d.line([X(x0 + 50), X(ym - stepy / 2), X(x1 - 50), X(ym - stepy / 2)], fill=mix(CARD, (200, 220, 240), a * .8), width=2)
            stroke(d, [(bx, ym - 26), (bx + 52, ym - 27), (bx + 53, ym + 26), (bx + 1, ym + 27), (bx, ym - 26)], fa(lt, t_sheet + .3 + .1 * i, .4), INK, 4, 40 + i, .9)
            sz, fz = 48, 66; sp = tw(" ", sz, "o") * 1.4; segs = [(pre, "o", sz, INK), (fig, "a", fz, ROLE[role]), (post, "o", sz, INK)]
            tot = sum(tw(s, z, f) for s, f, z, _ in segs if s) + sp * (sum(1 for s in segs if s[0]) - 1); k = min(1, (x1 - 60 - (bx + 96)) / tot)
            x = bx + 96; base_y = ym + _cap("o", sz * k) / 2
            for s, f, z, col in segs:
                if not s: continue
                w = tw(s, z * k, f)
                if f == "a" and key_line == i:
                    ph = appear(lt, t0 + .55, .4, "marker")
                    if ph > .01: hl(d, x, base_y - _cap("a", z * k) - 5, x + w, base_y + 8, mix(CARD, HLC.get(role, HLC["o"]), .95), ph)
                T(d, x, base_y, s, z * k, f, col, "ls", al, CARD, dy=10 * (1 - eout((lt - t0) / .3))); x += w + sp * k
            p = appear(lt, t0 + .25, .35, "marker")
            stroke(d, [(bx + 8, ym - 4), (bx + 24, ym + 16), (bx + 66, ym - 42)], p, GREEN, 10, 50 + i, .7)
    if side_pic: cut(base, lt, side_pic, 1590, 610, 200, t_sheet + .3, rot=4, disc=("g", 124), sfx=None)
    chime(lt, t_lines[-1] + .5)

# ------------------------------------------------------------------ recap cards
@lru_cache(maxsize=32)
def _recap_card(num, text, fig, col, w, h):
    """A numbered takeaway card with its text baked in (canvas px sprite, unrotated). Returns sprite and text boxes relative to the card centre (stage px)."""
    sp = panel_sprite(int(w * S), int(h * S), CARD, 50 + num).copy(); dd = ImageDraw.Draw(sp); o = PAD; r = 34 * S; bx, by = o + 62 * S, o + 64 * S
    dd.ellipse([bx - r, by - r, bx + r, by + r], fill=INK); dd.text((bx, by), str(num), font=F("a", 42), fill=CREAM, anchor="mm")
    dd.line([o + 112 * S, by, o + (w - 36) * S, by], fill=mix(CARD, LIGHT, .8), width=int(3 * S))
    ls = wrap(text, 38, "o", w - 76)[:3]; y = 128
    for ln in ls: dd.text((o + 38 * S, o + y * S), ln, font=F("o", 38), fill=INK, anchor="la"); y += 54
    fz = 104
    while F("a", fz).getlength(fig) / S > w - 70: fz -= 6
    dd.text((o + w * S / 2, o + (h - 92) * S), fig, font=F("a", fz), fill=col, anchor="mm"); fw = F("a", fz).getlength(fig) / S; fh = _cap("a", fz)
    boxes = (((28 - w / 2, 30 - h / 2, 96 - w / 2, 98 - h / 2), str(num)), ((38 - w / 2, 128 - h / 2, w / 2 - 38, y - h / 2), text),
             ((-fw / 2, h / 2 - 92 - fh / 2 - 4, fw / 2, h / 2 - 92 + fh / 2 + 4), fig))
    return sp, boxes
def _rbox(b, cx, cy, deg):
    """Stage bounding box of a centre-relative box after rotating by deg about (cx, cy)."""
    t = math.radians(deg); c, s = math.cos(t), math.sin(t); pts = [(x * c + y * s, -x * s + y * c) for x in (b[0], b[2]) for y in (b[1], b[3])]
    return (cx + min(p[0] for p in pts), cy + min(p[1] for p in pts), cx + max(p[0] for p in pts), cy + max(p[1] for p in pts))

@component("endcards", "recap_cards", dur=6.0, cam=[(0, 700, 450, 1.16), (1.3, 960, 540, 1.0), (6.0, 960, 540, 1.03)], still=5.4,
           use="A three-point recap as numbered cards, each with one takeaway and one figure, ending on the handwritten limitation.")
def recap_cards(base, d, lt, cam, headline="THREE THINGS", key_word="TO KEEP", hk="o",
                cards=(("Small amounts add up over time", "£100", "o"), ("Time does most of the work", "10 YRS", "b"), ("The rate decides who wins", "5%", "g")),
                limit_note="…if returns beat 5% after fees", t_head=.15, t_cards=(.8, 1.7, 2.6), t_note=3.8):
    """cards: (takeaway, figure, colour role). limit_note: the limitation the result depends on."""
    deco(base, cam, "blobO", 400, 600, .3); deco(base, cam, "blobB", 1520, 600, .3)
    kline(d, lt, 110, 150, [(headline, t_head, INK, None), (key_word, t_head + .3, INK, hk)], 84, "a")
    w, h = 450, 440; n = len(cards)
    for i, (text, fig, role) in enumerate(cards):
        t0 = t_cards[i]; appear(lt, t0, .5, "slide")
        if lt < t0: continue
        u = clamp((lt - t0) / .5); e = back(u); k = i - (n - 1) / 2; cx = 960 + k * 560; cy = 568 - (22 if k == 0 else 0)
        deg = -4.5 * k + (0 if k else 1.5) + (1 - e) * 10 * (1 if k <= 0 else -1); cy += 90 * (1 - e); a = min(1, u * 2.5)
        sp, boxes = _recap_card(i + 1, text, fig, ROLE[role], w, h); rot_paste(base, sp, cx, cy, deg, 1.0, a)
        rec("c", _rbox((-w / 2, -h / 2, w / 2, h / 2), cx, cy, deg), f"card {i + 1}")
        for b, s in boxes: rec("t", _rbox(b, cx, cy, deg), s)
    if limit_note:
        note(d, lt, 960, 868, limit_note, 62, t_note, INK, anchor="ma"); wn = tw(limit_note, 62, "c")
        underline(d, 960 - wn / 2, 960 + wn / 2, 946, appear(lt, t_note + .4, .45, "marker"), ORANGE, 6)

# ------------------------------------------------------------------ end card
_LOGO = {}
def _logo_label(width=560):
    """Option C logo, large: the on-dark lockup on an INK paper label, tilted 1.5 degrees, soft shadow, tape on its top-right corner."""
    if width not in _LOGO:
        lk = Image.open(os.path.join(ROOT, "assets", "lockup_horizontal_on-dark.png")).convert("RGBA"); lw = int((width - 72) * S)
        lk = lk.resize((lw, int(lk.size[1] * lw / lk.size[0])), Image.LANCZOS); w, h = int(width * S), lk.size[1] + int(64 * S)
        a = panel_sprite(w, h, INK, 77).copy(); a.alpha_composite(lk, (PAD + (w - lw) // 2, PAD + (h - lk.size[1]) // 2))
        cv = Image.new("RGBA", (a.size[0] + 160, a.size[1] + 140), (0, 0, 0, 0)); cv.alpha_composite(a, (80, 70))
        tp = Image.new("RGBA", (int(150 * S), int(46 * S)), (236, 226, 190, 168)); td = ImageDraw.Draw(tp)
        for xx in (0, tp.size[0] - 3): td.line([(xx, 0), (xx, tp.size[1])], fill=(236, 226, 190, 90), width=3)
        tp = tp.rotate(-22, Image.BICUBIC, expand=True); cv.alpha_composite(tp, (80 + PAD + w - tp.size[0] // 2 - 16, 70 + PAD - tp.size[1] // 2 + 4))
        cv = cv.rotate(1.5, Image.BICUBIC, expand=True); bb = cv.getchannel("A").point(lambda v: 255 if v > 120 else 0).getbbox()
        c = (cv.size[0] / 2, cv.size[1] / 2); _LOGO[width] = (cv, ((bb[0] - c[0]) / S, (bb[1] - c[1]) / S, (bb[2] - c[0]) / S, (bb[3] - c[1]) / S))
    return _LOGO[width]

@component("endcards", "end_card", dur=6.0, cam=[(0, 960, 540, 1.0), (6.0, 960, 540, 1.0)], still=5.4, logo=False,
           use="The plain end screen for the last 12 s: left half empty for YouTube's video element, logo and subscribe line on the right.",
           notes="Preview is 6 s of a 12 s card: hold the final state for the rest. Nothing is ever drawn at x < 960. Register/play it with the top-left logo hidden.")
def end_card(base, d, lt, cam, cta="Click the logo to subscribe", line1="Narrated with an AI voice", line2="General information, not financial advice",
             logo_w=560, cx=1420, t_logo=.3, t_cta=1.1, t_arrow=2.0, t_lines=2.7):
    """The left half (x < 960) stays empty paper. cx: centre of the right-hand column."""
    sp, bb = _logo_label(logo_w); a = appear(lt, t_logo, .5, "slide"); ly = 390
    if a > .02:
        e = back(clamp((lt - t_logo) / .5)); rot_paste(base, sp, cx, ly - 40 * (1 - e), 3 * (1 - e), .92 + .08 * e, min(1, a * 1.8))
        rec("c", (cx + bb[0], ly + bb[1] - 40 * (1 - e), cx + bb[2], ly + bb[3] - 40 * (1 - e)), "logo label")
    kline(d, lt, cx, 640, [(cta, t_cta, INK, None)], 58, "o", "m")
    wc = tw(cta, 58, "o"); p = appear(lt, t_arrow, .6, "marker")
    arrow(d, (cx - wc / 2 + 30, 630), (cx - logo_w / 2 + 70, ly + bb[3] + 22), p, ORANGE, 6, .32)
    for j, ln in enumerate((line1, line2)):
        if ln: T(d, cx, 790 + 54 * j, ln, 32, "sb", MUTED, "mm", fa(lt, t_lines + .25 * j), dy=8 * (1 - eout((lt - t_lines - .25 * j) / .3)))
