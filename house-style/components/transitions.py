"""Transitions between scenes. Each is fn(a, b, p) -> frame on two rendered frames (numpy HxWx3), p from 0 to 1."""
from kit import *

@transition("paper_slide", dur=.8, use="Default scene change. The new sheet slides over the old one; alternate `direction` between scenes.")
def paper_slide(a, b, p, direction=(1, 0)):
    e = ease(p); h, w = a.shape[:2]; dx, dy = int(direction[0] * w * (1 - e)), int(direction[1] * h * (1 - e)); out = a.copy()
    M = np.float32([[1, 0, dx], [0, 1, dy]]); mask = cv2.warpAffine(np.full((h, w), 255, np.uint8), M, (w, h)); bb = cv2.warpAffine(b, M, (w, h))
    sh = cv2.GaussianBlur(cv2.warpAffine(np.full((h, w), 255, np.uint8), np.float32([[1, 0, dx - 26 * direction[0]], [0, 1, dy - 26 * direction[1]]]), (w, h)), (0, 0), 18).astype(np.float32) / 255 * .45
    out = (out.astype(np.float32) * (1 - sh[:, :, None])).astype(np.uint8); m = (mask > 0)[:, :, None]; return np.where(m, bb, out)

# ---------------- physical-paper transitions (numpy/cv2 only; sizes always from a.shape so portrait frames work) ----------------
_TC = {}
def _grid(h, w):
    """Cached float32 x and y coordinate grids for a frame size."""
    if ("g", h, w) not in _TC: yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); _TC[("g", h, w)] = (xx, yy)
    return _TC[("g", h, w)]
def _under(h, w):
    """Cached underside of a sheet: plain grained paper, a little darker than the front."""
    if ("u", h, w) not in _TC:
        n = cv2.GaussianBlur(np.random.default_rng(11).standard_normal((h, w)).astype(np.float32), (0, 0), 1.2) * 9
        _TC[("u", h, w)] = np.clip(np.array((226, 217, 198), np.float32)[None, None, :] + n[:, :, None], 0, 255)
    return _TC[("u", h, w)]
def _soft(mask, k=8, sig=3.0):
    """Cheap soft shadow from a float mask: blur at 1/k size and scale back up."""
    h, w = mask.shape[:2]; sm = cv2.resize(mask, (max(2, w // k), max(2, h // k)), interpolation=cv2.INTER_AREA)
    return cv2.resize(cv2.GaussianBlur(sm, (0, 0), sig), (w, h), interpolation=cv2.INTER_LINEAR)

@transition("page_turn", dur=1.0, snd="slide", use="A new chapter or a change of topic: the old sheet lifts at the right edge and turns away like a page, showing its darker underside, with the new scene on the page beneath.",
            notes="`flip=True` turns the page the other way (alternate between scenes). `tilt` slants the fold line.")
def page_turn(a, b, p, flip=False, tilt=.16):
    if flip: return page_turn(a[:, ::-1], b[:, ::-1], p, False, tilt)[:, ::-1]
    h, w = a.shape[:2]; e = ease(p); xx, yy = _grid(h, w); lift = math.sin(math.pi * clamp(p * 1.15)) ** .6
    slant = tilt * (1 - .7 * e); span = w + abs(slant) * h + 40
    f = (w + abs(slant) * h / 2 + 20) - span * e * 1.02                           # fold line x at mid-height, moving right to left
    dist = xx - (f + slant * (yy - h / 2))                                        # signed distance from the slanted fold line (+ = already turned)
    # the turned part lies mirrored across the fold line: its underside, with a little show-through of the old sheet
    M = np.float32([[-1, 2 * slant, 2 * f - slant * h], [0, 1, 0]])
    ghost = cv2.warpAffine(a, M, (w, h), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
    curl = np.clip(-dist / (w * .11), 0, 1)                                       # 0 on the fold, 1 well onto the flap
    shade = (.60 + .40 * curl ** .7) * (1 - .10 * np.exp(-((curl - .22) / .09) ** 2))     # dark in the curl, a soft crease band, lighter on the flat
    flap = (_under(h, w) * .86 + ghost * .14) * shade[:, :, None]
    src_x = 2 * f - xx + 2 * slant * (yy - h / 2)                                 # where each flap pixel came from on the old sheet
    is_flap = (dist <= 0) & (src_x < w)
    edge = np.where(src_x >= w, src_x - w, 1e6)                                   # distance beyond the flap's free edge, on the old sheet
    out = a.astype(np.float32) * (1 - .42 * lift * np.exp(-edge / (w * .018)) * (dist <= 0))[:, :, None]
    out = np.where(is_flap[:, :, None], flap, out)
    sh = .55 * lift * np.exp(-np.clip(dist, 0, None) / (w * .035)) + .12 * lift * np.exp(-np.clip(dist, 0, None) / (w * .16))
    newp = b.astype(np.float32) * (1 - sh)[:, :, None]                            # the curl's shadow on the page beneath
    out = np.where((dist > 0)[:, :, None], newp, out)
    hl_ = np.exp(-(dist / 2.2) ** 2) * .5 * lift                                  # thin light line on the fold itself
    return np.clip(out + hl_[:, :, None] * 60, 0, 255).astype(np.uint8)

def _tear_masks(h, w):
    """Fixed-seed jagged tear down the sheet: float masks (left piece incl. its white fibre band, fibre band alone, right piece)."""
    if ("t", h, w) not in _TC:
        r = np.random.RandomState(7); n = 46; ys = np.linspace(-20, h + 20, n)
        wander = np.cumsum(r.uniform(-1, 1, n)) * w * .006; wander -= np.linspace(wander[0], wander[-1], n)
        xs = w * .47 + w * .05 * (ys / h - .5) + wander + r.uniform(-1, 1, n) * w * .007
        ys2 = np.linspace(-20, h + 20, n * 4); xs2 = np.interp(ys2, ys, xs) + r.uniform(-1, 1, n * 4) * 3.5       # fine tooth on the coarse zig-zag
        fib = np.interp(ys2, ys, xs + r.uniform(5, 15, n)) + r.uniform(-2, 2, n * 4)                              # ragged outer limit of the torn fibres
        def left_of(x_):
            m = np.zeros((h, w), np.uint8); pts = np.concatenate([[[-10, -30]], np.stack([x_, ys2], 1), [[-10, h + 30]]]).astype(np.int32)
            cv2.fillPoly(m, [pts], 255, lineType=cv2.LINE_AA); return m.astype(np.float32) / 255
        core, full = left_of(xs2), left_of(fib)
        _TC[("t", h, w)] = (full, np.clip(full - core, 0, 1), 1 - core, (float(np.interp(0, ys, xs)), float(np.interp(h, ys, xs))))
    return _TC[("t", h, w)]
@transition("tear_away", dur=1.1, snd="whoosh", use="A hard break or a myth being thrown out: the old sheet tears top to bottom along a jagged edge, one piece slides off and the other drops away to reveal the new scene.",
            notes="The tear line is fixed-seed, so it is identical on every render. `flip=True` mirrors it.")
def tear_away(a, b, p, flip=False):
    if flip: return tear_away(a[:, ::-1], b[:, ::-1], p, False)[:, ::-1]
    h, w = a.shape[:2]; left, fibre, right, (xt, xb) = _tear_masks(h, w); af = a.astype(np.float32)
    white = np.float32((250, 248, 242)); lf = fibre[:, :, None]
    L4 = np.dstack([af * (1 - lf) + white * lf, left * 255]); R4 = np.dstack([af, right * 255])
    u = ease(clamp(p / .42)); v = clamp((p - .38) / .62); vin = v * v * (3 - 2 * v) * v            # tear runs down, then the pieces leave
    py_ = h * 1.02 * u; px_ = xt + (xb - xt) * u                                                    # the tear front: pieces hinge open about it
    def about(deg, cx, cy, dx, dy):
        M = cv2.getRotationMatrix2D((cx, cy), deg, 1.0); M[0, 2] += dx; M[1, 2] += dy; return M
    ML = about(1.1 * u + 5 * vin, px_, py_, -w * .62 * vin, h * .05 * vin)
    MR = about(-1.6 * u - 13 * vin, px_, py_, w * .10 * vin, h * 1.20 * vin)
    Lw = cv2.warpAffine(L4, ML, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    Rw = cv2.warpAffine(R4, MR, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    la, ra = Lw[:, :, 3] / 255, Rw[:, :, 3] / 255; off = int(8 + 22 * max(u * .5, vin)); 
    cover = np.maximum(la, ra); sh = _soft(cover, 8, 1.2 + 2.2 * max(u * .4, vin))
    sh = cv2.warpAffine(sh, np.float32([[1, 0, off * .6], [0, 1, off]]), (w, h), borderMode=cv2.BORDER_REPLICATE)
    out = b.astype(np.float32) * (1 - .5 * sh * (1 - cover))[:, :, None]
    out = out * (1 - ra[:, :, None]) + Rw[:, :, :3] * ra[:, :, None]
    rs = cv2.warpAffine(la, np.float32([[1, 0, 7], [0, 1, 5]]), (w, h)) * .22 * (1 - la)              # the left piece sits on top: a faint shadow on the right one
    out = out * (1 - (rs * ra)[:, :, None])
    out = out * (1 - la[:, :, None]) + Lw[:, :, :3] * la[:, :, None]
    return np.clip(out, 0, 255).astype(np.uint8)

@transition("fold", dur=1.2, snd="slide", use="Putting an idea away or closing a section: the old sheet folds up panel by panel toward one side like a leaflet (thirds by default, `parts=2` for in half), revealing the new scene.",
            notes="`parts` = 2 or 3 panels. `flip=True` folds toward the right instead of the left.")
def fold(a, b, p, parts=3, flip=False):
    if flip: return fold(a[:, ::-1], b[:, ::-1], p, parts, False)[:, ::-1]
    h, w = a.shape[:2]; n = max(2, int(parts)); pw_ = w / n; under = _under(h, w)
    wts = [1.0] * (n - 1) + [.75]; tot = sum(wts); acc = 0.0; k = n - 1; u = 1.0                   # folds run one after another; the last panel folds away off the edge
    for i, wt in enumerate(wts):
        if p * tot < acc + wt: k = i; u = (p * tot - acc) / wt; break
        acc += wt
    m = n - 1 - k; c = int(round(m * pw_)); x1 = int(round((m + 1) * pw_))                         # moving panel m, hinged on the crease at its left edge
    last = m == 0; phi = (math.pi / 2 * (u * u * (3 - 2 * u)) ** 1.3 * 1.0) if last else math.pi * ease(u)
    cs, sn = math.cos(phi), math.sin(phi); out = b.astype(np.float32)
    edge = max(c, int(c + pw_ * cs)) if cs > 0 else c                                              # right-hand limit of the old sheet's stack
    rw = min(w - edge, int(w * .05))
    if rw > 2:                                                                                      # the stack's soft shadow on the new scene
        ramp = 1 - (.42 * (.45 + .55 * sn)) * np.exp(-np.arange(rw, dtype=np.float32) / (w * .012)); out[:, edge:edge + rw] *= ramp[None, :, None]
    if c > 0:
        out[:, :c] = a[:, :c]
        if k > 0: out[:, c - int(round(pw_)) if c - int(round(pw_)) > 0 else 0:c] = a[:, max(0, c - int(round(pw_))):c]
        if cs < 0:                                                                                  # panel coming down onto its neighbour: shadow ahead of its free edge
            xf = int(c + pw_ * cs); sw = min(xf, int(w * .07))
            if sw > 2: out[:, xf - sw:xf] *= (1 - .5 * sn * np.exp(-np.arange(sw, 0, -1, dtype=np.float32) / (w * .02)))[None, :, None]
    # the moving panel: old-sheet content on the first fold, plain underside after that (earlier panels are folded behind it)
    face = a[:, c:x1].astype(np.float32) if (k == 0 and cs > 0) else under[:, c:x1]
    fw = face.shape[1]; grad = np.linspace(0, 1, fw, dtype=np.float32)
    lightv = (1 - .34 * sn) * (1 - .10 * sn * (1 - grad)) if cs > 0 else (1 - .30 * sn) * (.96 + .04 * grad)
    face = face * lightv[None, :, None]
    if k > 0 or cs <= 0: face[:, :3] *= .88; face[:, -3:] *= .9                                    # paper edges of the folded packet
    grow = (.10 if not last else .16) * sn * h / 2; xf = c + pw_ * cs
    src = np.float32([[0, 0], [fw, 0], [fw, h], [0, h]]); dst = np.float32([[c, 0], [xf, -grow], [xf, h + grow], [c, h]])
    if abs(xf - c) > 1.5:
        P = cv2.getPerspectiveTransform(src, dst); x0b, x1b = max(0, int(min(c, xf)) - 2), min(w, int(max(c, xf)) + 3)
        T_ = np.float32([[1, 0, -x0b], [0, 1, 0], [0, 0, 1]]) @ P.astype(np.float32)
        wp = cv2.warpPerspective(np.dstack([face, np.full(face.shape[:2], 255, np.float32)]), T_, (x1b - x0b, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        al = wp[:, :, 3:] / 255; out[:, x0b:x1b] = out[:, x0b:x1b] * (1 - al) + wp[:, :, :3] * al
    if c > 0 and sn > .02:                                                                         # the crease
        out[:, max(0, c - 2):c + 2] *= 1 - .35 * sn
    return np.clip(out, 0, 255).astype(np.uint8)
