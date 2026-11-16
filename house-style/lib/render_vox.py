"""python3 render_vox.py preview [t ...] | check | render | mix | sheet      Episode 04 opening, paper-collage build (test 4)."""
import time
from multiprocessing import Pool
from collections import Counter
import vlib
from vlib import *
from vscenes import SCENES, CAMS, _wordmark

DIRS = [(1, 0), (1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (1, 0)]      # paper travel at each scene change
BOUND = [s["start"] for s in SC[1:]]
def scene_at(t):
    for i, s in enumerate(SC):
        if s["start"] <= t < s["start"] + s["dur"]: return i
    return len(SC) - 1
def cam_at(i, lt):
    s = SC[i]; ks = CAMS[s["k"]]; t = s["start"] + lt
    cx = pw(lt, [(k[0], k[1]) for k in ks]); cy = pw(lt, [(k[0], k[2]) for k in ks]); z = pw(lt, [(k[0], k[3]) for k in ks])
    cx += 5 * math.sin(.6 * t); cy += 3 * math.sin(.43 * t + 1)
    if i < len(SC) - 1: e = clamp((lt - (s["dur"] - .45)) / .45) ** 2; cx += DIRS[i][0] * 70 * e; cy += DIRS[i][1] * 50 * e
    if i > 0: e = 1 - eout(lt / .55); cx -= DIRS[i - 1][0] * 70 * e; cy -= DIRS[i - 1][1] * 50 * e
    cx = clamp(cx, W / 2 / z - BLEED + 2, W + BLEED - W / 2 / z - 2); cy = clamp(cy, H / 2 / z - BLEED + 2, H + BLEED - H / 2 / z - 2)
    return cx, cy, z
def scroll(t):
    gx = gy = 0.0
    for b, (dx, dy) in zip(BOUND, DIRS): u = ease((t - (b - .36)) / .62); gx += dx * 1700 * u; gy += dy * 1300 * u
    return gx, gy
def content_alpha(i, lt): return 1.0 if i == len(SC) - 1 else 1 - ease((lt - (SC[i]["dur"] - .42)) / .28)

_HUD = None
def hud():
    """Fixed overlays in frame px: the logo label top left, the disclaimer label bottom right."""
    global _HUD
    if _HUD is None:
        lk = Image.open(os.path.join(HERE, "assets", "lockup_horizontal_on-dark.png")).convert("RGBA"); lk = lk.resize((int(lk.size[0] * 46 / lk.size[1]), 46), Image.LANCZOS)
        w, h = lk.size[0] + 30, 66; a = panel_sprite(w, h, INK, 77).copy(); a.alpha_composite(lk, (PAD + 15, PAD + 10)); lbox = (44, 28, 44 + w, 28 + h)
        txt = "General information, not financial advice"; fo = font("sb", 24); tl = int(fo.getlength(txt)); w2, h2 = tl + 40, 48
        b = panel_sprite(w2, h2, INK, 78).copy(); ImageDraw.Draw(b).text((PAD + 20, PAD + h2 / 2), txt, font=fo, fill=CREAM, anchor="lm"); dbox = (W - 44 - w2, H - 26 - h2, W - 44, H - 26)
        tb = ImageDraw.Draw(b).textbbox((PAD + 20, PAD + h2 / 2), txt, font=fo, anchor="lm"); tbox = (dbox[0] + tb[0] - PAD, dbox[1] + tb[1] - PAD, dbox[0] + tb[2] - PAD, dbox[1] + tb[3] - PAD)
        def prep(im, box):
            arr = np.asarray(im, np.float32); return (box[0] - PAD, box[1] - PAD, arr[:, :, :3], arr[:, :, 3:] / 255)
        _HUD = (prep(a, lbox), prep(b, dbox), lbox, dbox, tbox, txt)
    return _HUD
def put(out, spr, a=1.0):
    x, y, rgb, al = spr; h, w = rgb.shape[:2]; reg = out[y:y + h, x:x + w].astype(np.float32); al = al * a
    out[y:y + h, x:x + w] = (reg * (1 - al) + rgb * al).astype(np.uint8)
_VIG = None
def vig():
    global _VIG
    if _VIG is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 1.414
        v = np.clip(1 - .30 * r ** 2.6, 0, 1); _VIG = np.dstack([v, v, v]).astype(np.float32)
    return _VIG

def frame(t, fit=False):
    """Returns the 1920x1080 RGB frame (numpy). With fit=True also returns the recorded boxes in frame coordinates."""
    i = scene_at(t); s = SC[i]; lt = t - s["start"]; cam = cam_at(i, lt); cx, cy, z = cam; al = content_alpha(i, lt)
    gx, gy = scroll(t); ox = int(gx - (cx - 960) * S * .45) % TW_; oy = int(gy - (cy - 540) * S * .45) % TH_
    bg = tile2()[oy:oy + CH, ox:ox + CW]
    M = np.float32([[z / S, 0, W / 2 - (cx + BLEED) * z], [0, z / S, H / 2 - (cy + BLEED) * z]])
    items = []
    if al > .01:
        base = Image.fromarray(np.ascontiguousarray(bg)); d = ImageDraw.Draw(base)
        if fit: vlib.FIT = []
        SCENES[s["k"]](base, d, lt, AUD.get(s["k"], s["dur"]), cam)
        if fit:
            if al > .05: items = [(k, ((b[0] - cx) * z + W / 2, (b[1] - cy) * z + H / 2, (b[2] - cx) * z + W / 2, (b[3] - cy) * z + H / 2), n) for k, b, n in vlib.FIT]
            vlib.FIT = None
        out = cv2.warpAffine(np.asarray(base), M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if al < .995: out = cv2.addWeighted(out, al, cv2.warpAffine(np.ascontiguousarray(bg), M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT), 1 - al, 0)
    else:
        out = cv2.warpAffine(np.ascontiguousarray(bg), M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    g0, g1 = scroll(t - .5 / FPS), scroll(t + .5 / FPS); vx, vy = (g1[0] - g0[0]) * .8, (g1[1] - g0[1]) * .8
    if abs(vx) > 3 or abs(vy) > 3: out = cv2.blur(out, (int(abs(vx) * .5) | 1, int(abs(vy) * .5) | 1))
    out = cv2.multiply(out.astype(np.float32), vig()).astype(np.uint8)
    lg, ds, lbox, dbox, tbox, txt = hud()
    la = (0.0 if s["k"] == "sting" else min(al, ease(lt / .3) if i > 0 else 1.0))
    if la > .01: put(out, lg, la)
    put(out, ds)
    if fit:
        if la > .5: items.append(("c", lbox, "logo"))
        items += [("c", dbox, "disclaimer"), ("t", tbox, txt)]
        return out, items
    return out

def _hit(a, b, pad=0): return not (a[2] + pad <= b[0] or a[0] - pad >= b[2] or a[3] + pad <= b[1] or a[1] - pad >= b[3])
def _inside(a, b, m): return a[0] >= b[0] + m and a[1] >= b[1] + m and a[2] <= b[2] - m and a[3] <= b[3] - m
def fit_check(step=0.25, margin=6):
    """Sampled every `step` s, after the camera transform: text fully on-frame and inside any card it touches (6 px);
    no text on a picture and pictures >= 20 px from text; a picture is inside a card or >= 40 px from it; no card over a chart."""
    bad = {}; t = 0.0; n = 0
    while t < TOTAL:
        _, items = frame(t, True); n += 1
        cards = [(b, nm) for k, b, nm in items if k == "c"]; texts = [(b, s) for k, b, s in items if k == "t"]
        for k, ib, nm in items:
            if k != "i": continue
            if ib[0] < 0 or ib[1] < 0 or ib[2] > W or ib[3] > H: bad.setdefault((nm, "picture off frame"), t)
            for tb, s in texts:
                if _hit(ib, tb): bad.setdefault((s, f"overlaps the {nm} picture"), t)
                elif _hit(ib, tb, 20): bad.setdefault((s, f"closer than 20 px to the {nm} picture"), t)
            for c, cn in cards:
                if not _inside(ib, c, margin) and _hit(ib, c, 40): bad.setdefault((nm, f"picture within 40 px of a card {cn}"), t)
        for z_ in [b for k, b, _ in items if k == "z"]:
            for c, cn in cards:
                if _hit(c, z_) and not (abs(c[0] - z_[0]) < 1 and abs(c[2] - z_[2]) < 1): bad.setdefault((f"card {cn}", "overlaps a chart"), t)
        for tb, s in texts:
            if tb[0] < 0 or tb[1] < 0 or tb[2] > W or tb[3] > H: bad.setdefault((s, "off frame"), t)
            for c, cn in cards:
                if _hit(tb, c) and not _inside(tb, c, margin): bad.setdefault((s, f"crosses a card {cn}"), t)
        t += step
    for (s, why), tt in sorted(bad.items(), key=lambda kv: kv[1]):
        print(f"FIT FAIL {SC[scene_at(tt)]['k']} @{tt:.2f}s (local {tt - SC[scene_at(tt)]['start']:.2f}): {s!r} {why}")
    print(f"fit check ({n} sampled times, camera applied):", "PASS" if not bad else f"{len(bad)} problems")
    return not bad

def sfx_events():
    ev = []
    for i, s in enumerate(SC):
        vlib.COLLECT = []; base = Image.new("RGB", (CW, CH), PAPER); d = ImageDraw.Draw(base)
        SCENES[s["k"]](base, d, 9999.0, AUD.get(s["k"], s["dur"]), (960, 540, 1))
        for t0, nm, dd in vlib.COLLECT:
            if 0 <= t0 < s["dur"] - .3: ev.append((s["start"] + t0, nm, dd))
        if i: ev.append((s["start"] - .34, "whoosh", 0))
    vlib.COLLECT = None
    ev.append((BYKEY["sting"]["start"] + .05, "sting", 0)); ev.sort(); out = []
    gap = dict(marker=.5, slide=.4)
    for e in ev:
        if not any(e[1] == o[1] and abs(e[0] - o[0]) < gap.get(e[1], .25) for o in out): out.append(e)
    return out

NCH = 16
def render_chunk(j):
    n = round(TOTAL * FPS); n0, n1 = n * j // NCH, n * (j + 1) // NCH; out = os.path.join(HERE, "seg", f"c{j:02d}.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-threads", "2", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for f in range(n0, n1): p.stdin.write(frame(f / FPS).tobytes())
    p.stdin.close(); p.wait(); return out

VOL = dict(whoosh=.5, pop=.45, ticks=.4, chime=.55, sting=.9, marker=.5, slide=.45)
def mix_audio():
    sd = os.path.join(HERE, "seg"); x = os.path.join(HERE, "sfx")
    # paper-slide and marker sounds, made procedurally from the existing whoosh (no new sound generation)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{x}/whoosh.mp3", "-af", "atrim=0.08:0.62,asetpts=PTS-STARTPTS,atempo=1.9,highpass=f=2400,lowpass=f=9000,afade=t=in:d=0.03,afade=t=out:st=0.16:d=0.12,volume=1.6", f"{sd}/marker.wav"])
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{x}/whoosh.mp3", "-af", "atempo=0.7,highpass=f=300,lowpass=f=1500,afade=t=in:d=0.08,afade=t=out:st=0.5:d=0.5,volume=1.2", f"{sd}/slide.wav"])
    src = lambda nm: f"{sd}/{nm}.wav" if nm in ("marker", "slide") else f"{x}/{nm}.mp3"
    open(f"{sd}/list.txt", "w").write("".join(f"file '{sd}/c{j:02d}.mp4'\n" for j in range(NCH))); silent = f"{sd}/silent.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{sd}/list.txt", "-c", "copy", silent])
    ev = sfx_events(); ins, filt, lab = [], [], []
    for j, (tt, nm, dd) in enumerate(ev):
        ins += ["-i", src(nm)]; ms = int(max(0, tt) * 1000)
        trim = f"atrim=0:{dd:.2f},afade=t=out:st={max(0, dd - .15):.2f}:d=0.15," if nm == "ticks" else ""     # ticks stop when the count stops
        filt.append(f"[{j}:a]{trim}aformat=sample_rates=48000:channel_layouts=stereo,adelay={ms}|{ms},volume={VOL[nm]}[s{j}]"); lab.append(f"[s{j}]")
    filt.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0,apad=whole_dur={TOTAL:.2f}[out]")
    sfxw = f"{sd}/sfx_track.wav"; open(f"{sd}/sfx_filter.txt", "w").write(";".join(filt))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex_script", f"{sd}/sfx_filter.txt", "-map", "[out]", "-t", f"{TOTAL:.2f}", sfxw])
    ins, filt, lab = [], [], []
    for i, k in enumerate(KEYS):
        ins += ["-i", os.path.join(HERE, "audio", f"{i+1:02d}.mp3")]; ms = int(BYKEY[k]["speech"] * 1000)
        filt.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]"); lab.append(f"[a{i}]")
    nv = len(KEYS); ins += ["-i", silent, "-stream_loop", "-1", "-i", f"{x}/music.mp3", "-i", sfxw]; vi, mi, si = nv, nv + 1, nv + 2
    filt.append("".join(lab) + f"amix=inputs={nv}:normalize=0,apad=whole_dur={TOTAL:.2f},asplit=2[v1][v2]")
    filt.append(f"[{mi}:a]atrim=0:{TOTAL:.2f},asetpts=PTS-STARTPTS,volume=0.12,afade=t=in:d=2,afade=t=out:st={TOTAL-1.5:.2f}:d=1.5[mus]")
    filt.append("[mus][v2]sidechaincompress=threshold=0.02:ratio=10:attack=30:release=600[duck]")
    filt.append(f"[v1][duck][{si}:a]amix=inputs=3:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=7,volume=0.6dB,apad=whole_dur={TOTAL:.2f}[aout]")
    out = os.path.join(HERE, "ep4_vox_draft.mp4")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(filt), "-map", f"{vi}:v", "-map", "[aout]",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{TOTAL:.2f}", "-movflags", "+faststart", out])
    cnt = Counter(e[1] for e in ev)
    json.dump({s["k"]: round(s["start"], 2) for s in SC} | {"TOTAL": round(TOTAL, 2), "sfx": len(ev), "sfx_by_type": cnt}, open(os.path.join(HERE, "timeline.json"), "w"), indent=1)
    print("master", round(TOTAL, 1), "s,", len(ev), "sound effects", dict(cnt))

if __name__ == "__main__":
    mode = (sys.argv[1:] or ["preview"])[0]
    if mode in ("render", "mix") and not fit_check(): sys.exit("fit check failed: fix before rendering")
    if mode == "preview":
        ts = [float(a) for a in sys.argv[2:]]; os.makedirs(os.path.join(HERE, "preview"), exist_ok=True)
        ims = [Image.fromarray(frame(t)).resize((960, 540), Image.LANCZOS) for t in ts]
        for n in range(0, len(ims), 4):
            sh = Image.new("RGB", (1920, 1080)); [sh.paste(im, ((j % 2) * 960, (j // 2) * 540)) for j, im in enumerate(ims[n:n + 4])]
            sh.save(os.path.join(HERE, "preview", f"p{n // 4}.png"))
    elif mode == "sheet":
        ims = [Image.fromarray(frame(s["start"] + s["dur"] - (.6 if s["k"] != "sting" else .55))).resize((640, 360), Image.LANCZOS) for s in SC]
        sh = Image.new("RGB", (1280, 360 * ((len(ims) + 1) // 2))); [sh.paste(im, ((j % 2) * 640, (j // 2) * 360)) for j, im in enumerate(ims)]
        sh.save(os.path.join(HERE, "contact_sheet.png"))
    elif mode == "render":
        t0 = time.time(); tile2()
        with Pool(2) as p: p.map(render_chunk, range(NCH), chunksize=1)
        print("render seconds", round(time.time() - t0)); open(os.path.join(HERE, "seg", "render_time.txt"), "w").write(str(round(time.time() - t0)))
    elif mode == "mix": mix_audio()
    elif mode == "check": sys.exit(0 if fit_check() else 1)
    elif mode == "time":
        t0 = time.time(); [frame(float(a)) for a in sys.argv[2:]]; print("s/frame", (time.time() - t0) / max(1, len(sys.argv) - 2))
