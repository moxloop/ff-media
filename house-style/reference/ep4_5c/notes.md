# TEST 5c FULL: Ep04 opening, 0.00 to 190.80 s (all seven scenes)

These notes cover the full build. The section that follows them is the original 53 s write-up, which still applies to 0–52.96 s.

- **Starts** (asserted against `mix/timeline.json`): hook 0, sting 24.1, roadmap 26.7, guaranteed 52.96, expected 87.3, fees 117.16, setup 152.7, end 190.8.
- **Voice:** clips 01–06.
- **First 52.5 s:** unchanged in code. The only differences are in the last 0.45 s of the roadmap, which now has the normal exit slide and whoosh into the guaranteed scene, and in the music bed, which now runs on (its fade-out moved to the end).
- **Scenes 4–7:** they keep 5b's storyboard adaptation. The changes from 5b are listed below.

## The seven techniques in the new scenes (times are on the master timeline)

1. **Kinetic typography**
   - 59.2 s: the £1,169.18 counter flips up, lands with a pulse and gets an underline.
   - 72.5 s: the £100 token re-forms into "£100 × 5% = £5 A YEAR".
   - 133.0 s / 135.0 s: the £81,007 and £69,299 pot values count up inside their bars.
   - 170.8 s → 171.5 s: "THEN £1,169.18 + £100" re-forms into "= £1,269.18 A MONTH INTO THE JAR".
2. **Animated charts**
   - 90.0 s: the expected-return chart draws its orange line.
   - 98.4–102.7 s: the blue path draws on "jumps" and "drops, sometimes sharply".
   - 133.0 s / 135.0 s: the fee pot bars unroll.
   - 137.7 s: the orange missing piece breaks away.
   - 161.5 s / 179.2 s: the timelines unroll.
3. **Layered cut-outs**
   - Parallax and float on the house, coins and bank (53–87 s).
   - 102.9–117 s: the scale has paper blocks, and the lock and chart cut-outs float under it.
   - 160–190 s: parallax on the people.
4. **Highlighted evidence**
   - 70.4 s: a "Figures Forward calculation" sheet appears, and £5 gets a green highlighter swipe at 73.3 s.
   - 125–128.3 s: 7% − 1% = 6% is worked on a ruled calculation sheet, with the camera pushed in (1.16) and a green highlighter on 6%.
   - The 6% is ringed on "the return after fees and tax".
5. **Visual transformation**
   - 70.6 s: a £100 token becomes the £5 sum.
   - Drips fall from the fee tap.
   - The jars are drawn in code and fill as blue drops fall in: B's from 179.3 s (slow, from day one), A's from 170.8 s (fast, after month 258).
   - Both jars stop at the same level, so the result stays for the next scene, as the storyboard says.
6. **Sound:** 133 sfx in total, all cut or filtered from the existing files.
   - Counts by type: marker 32, pop 30, slide 25, thud 9, ticks 9, chime 8, whoosh 7, swish 6, click 6, sting 1.
   - New sync points: thuds on the scale blocks and the jars, swishes on the chart's jumps and drops, clicks on the fee maths, and ticks on every count.
7. **Pacing:** each new scene has 12–20 cue-timed beats, roughly one every 2–3 s. The holds come on £5, £11,708 and "WHOSE JAR IS FULLER?".

## Deviations

- The tax icon is the coins cut-out, because `src/assets` has no document image.
- The jars are drawn in code, so they start empty as the storyboard asks. They then fill to an equal level, which shows timing only, not the result.
- The guaranteed-scene camera push stays at 1.06, because a stronger push put the headline under the logo in the fit check.

## Checks (full build)

- **Fit check:** PASS, 764 times sampled, camera applied. Seven problems were fixed before the render:
  - camera push vs logo;
  - parallax house vs headline;
  - pot values vs bar margin;
  - jar label vs disclaimer;
  - jar overshoot vs labels.
- **Visual check:** 1 preview sheet. One fix pass followed it: a sheet label clashed with the 6% ring, and the jar drops crossed the labels.
- **Loudness:**
  - Full draft: −16.1 LUFS, −1.9 dBTP.
  - Full review: −16.2 LUFS, −1.6 dBTP.
  - Method: two-pass linear loudnorm, then a limiter.
- **Render:** 405 s for frames (2 processes), about 80 s for the fit check, about 1 min to mix and about 4 min for the two-pass review.
- **Outputs:**
  - `v5c_full_draft.mp4`: crf 22, AAC 192k, 70.7 MiB.
  - `v5c_full_review.mp4`: 1920×1080, two-pass 500 kbps, AAC 96k, 13.8 MiB.
  - `contact_sheet_full.png`: 7 late frames, 2 × 640 px.
- **Unchanged from the first build:** the 53 s deliverables (`v5c_draft.mp4`, `v5c_review.mp4`, `contact_sheet.png`).

---

# TEST 5c: Ep04 opening, 0.00 to 52.96 s (hook, sting, roadmap)

This build uses the 5b collage look: paper ground, Anton, Oswald and Caveat type, duotone cut-outs on role discs, and marker work. Seven techniques are added on top.

- **Source:** `build/build.py`. It imports copies of `vlib.py` and `render_vox.py` from `build/lib/`. The vlib copy only has its old-path timing block stubbed out. Fonts, assets and sfx are symlinked from `src`.
- **Scene starts:** hook 0.00, sting 24.10, roadmap 26.70, end 52.96. These match `mix/timeline.json` and are asserted in the build.
- **Figures:** asserted against `figures_check.py`:
  - £69,299 / £60,631 / £8,668 at 6%
  - £51,413 / £58,495 / £7,082 at 4%
  - £1,169.18
  - month 258, 3½ years early
  - £200,000 / 25 years / 5%

## The 7 techniques (times are on the master timeline)

1. **Kinetic typography**
   - 1.08 s: £100 slides on with an overshoot.
   - 3.5 s: the £100 shrinks and splits into two £100 tokens.
   - 9.0 s: the tokens re-form into the 25-year pots, counting up from £100 to £69,299 and £60,631.
   - 14.1 s: the pots morph to the 4% figures, £51,413 and £58,495.
   - 15.8 s: £8,668 re-forms into £7,082. At the same moment the label morphs from "Investing ends ahead by" to "Overpaying ends ahead by", and the heading from 6% to 4%.
   - 17.7 s / 19.1 s: the headline morphs from "IT'S A SEE-SAW" to "ONE NUMBER DECIDES IT".
2. **Animated chart**
   - 27.4 s: the normal balance line draws on "last time".
   - 29.2 s: the orange overpay line draws on "one hundred pounds a month… our example mortgage", with a "−£100 a month" label riding its tip.
   - 32.2 s: the line hits zero at month 258, the green 258→300 gap appears, and "3½ years early" is added with an arrow.
3. **Layered cut-outs**
   - 0–3.4 s: hand and coins with foreground parallax and a slow paper float.
   - 3.5–6 s: house and chart on role discs.
   - 6.7 s: the "Figures Forward calculation" sheet slides in (generic ruled paper, no bank names, logos or account numbers).
   - 18.3 s: the house and chart ride the see-saw.
   - 36.8–44.3 s: the step icons have parallax.
4. **Highlighted evidence**
   - 6.5–17.4 s: the camera pushes into the calculation sheet (1.30 → 1.40 zoom).
   - 11.8 s: a blue highlighter swipes £8,668.
   - 16.7 s: an orange highlighter swipes £7,082.
5. **Visual transformation**
   - 3.5 s: the £100 splits into an orange token that goes to the house and a blue token that goes to the chart.
   - 6.0 s: the tokens fly onto the sheet and become the pots.
   - 29.5 s: the £100 pulls the balance line down to zero early.
6. **Purposeful sound design:** 48 sfx, kept subtle under the voice.
   - Counts by type: pop 10, slide 10, marker 9, ticks 4, whoosh 3, thud 3, swish 3, click 3, chime 2, sting 1.
   - Derived with ffmpeg from the existing files, with no new sound generation:
     - click: pop, pitched up 1.6× and trimmed to 90 ms.
     - thud: pop, pitched down 0.55× and low-passed at 700 Hz.
     - swish: whoosh, trimmed, sped up and band-passed.
     - marker and slide: whoosh, as in 5b.
   - Each sound is synced to a movement:
     - ticks are trimmed to each count;
     - clicks on the morphs;
     - thuds on the £100 landing, the see-saw riders and month 258;
     - marker swishes on each highlight and line draw;
     - chimes on "?%" and "3½ years early".
7. **Visual pacing**
   - Something new develops every 1.5–3 s during the explanation.
   - The two key reveals are held: £8,668 for about 3 s, and £7,082 then "?%" for about 4 s each.
   - The roadmap steps arrive about 2.4 s apart.

## Checks

- **Fit check:** PASS. 212 sampled times (every 0.25 s), with the camera applied. It passed first time and passed again after one layout fix to the chart labels, made from the preview sheet.
- **Loudness:**
  - Draft: −16.0 LUFS, true peak −1.6 dBTP (two-pass linear loudnorm).
  - Review: −16.2 LUFS, −1.5 dBTP (AAC 96k, with a limiter).
- **Mix:** voice 01 and 02 at the original speech starts, music bed at 0.12 sidechain-ducked under the voice, plus the sfx track.
- **Render time:** 132 s for frames (2 processes), plus about 20 s for the fit check, about 30 s to mix and about 1.5 min for the two-pass review encode.
- **Visual checks:** 2 (one preview sheet and the final contact sheet). No images or voice were generated.
- **Outputs:**
  - `v5c_draft.mp4`: 1920×1080, 30 fps, crf 22, AAC 192k, 18.3 MiB.
  - `v5c_review.mp4`: 1920×1080, two-pass 1050 kbps, AAC 96k, 7.3 MiB.
  - `contact_sheet.png`: 8 frames, 2 × 640 px.
- **Known nits:**
  - The sting tagline is still mid-fade in the contact sheet frame.
  - The hand cut-out reads as a pinch.
