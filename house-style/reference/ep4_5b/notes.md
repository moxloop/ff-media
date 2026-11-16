# Ep04 opening: TEST 5b (opus2), the test 4 craft applied to the Fable storyboard

## What made test 4 better than test 5 (written before building, from the two contact sheets and vscenes.py)
1. **Headlines are posters, not titles.** Test 4 sets every headline in ALL-CAPS Anton at 88–92 px, left at (110,150). Each word drops in on its spoken cue (`kline`, 0.24 s overshoot), and a highlighter swipes behind the key word about 0.3 s after it lands. Test 5 used mixed-case Anton at 70 px with a small grey Inter subtitle, so it read like a slide title.
2. **A real type scale with three voices.** Test 4 uses Anton 84–150 px for numbers (counted up and highlighted), Oswald caps for labels and tags, and Caveat handwriting for the narrator's asides ("from a bank that can't say no", "fees are like a dripping tap"). Inter is kept for a few short body lines. Test 5 put almost everything in 26–34 px Inter inside outlined boxes, so it read like a dashboard or spreadsheet.
3. **Collage layering.** Test 4's pictures are big (150–380 px), duotone halftone cut-outs with a white paper border and a slight rotation, sitting on a coloured paper disc in the role colour. Labels are rotated paper tags that pop with overshoot. There are kraft panels for metaphors and dark ink panels for the payoff numbers. Test 5 used small 120–140 px icons on plain white cards with drawn outlines, with no discs, no tags, no kraft or ink panels and no handwriting.
4. **Marker work timed to the narration.** Test 4 draws rings, curved arrows, underlines and strike-throughs 0.4–1.5 s after the word they annotate, so the hand seems to follow the voice. Test 5 had fewer of these, and most of them sat on small text.
5. **The camera tells the story.** Each test 4 scene opens zoomed in at 1.12–1.2 on the first beat. It then pans or pulls out to reveal each new beat as it is spoken, and ends on a slow 1.0 → 1.035 push. Scene changes slide the paper sheet horizontally or vertically, with motion blur. Test 5's camera hardly moved (1.0–1.03), and every transition went the same way.
6. **The frame is composed, not gridded.** Test 4 builds asymmetric compositions that fill the frame, with parallax colour blobs and dot grids behind. Test 5 copied the storyboard's box coordinates one to one, which left large empty areas (the expected scene) and a rigid card grid.
7. **Breathing.** Test 4 keeps each beat to one idea with one large element. Small print is limited to a single caption per scene, and the next beat arrives on the next sentence.

## How I applied it here
- Every scene has an Anton 88 kinetic headline with a word-cued highlighter swipe. Key figures are Anton 92–150 px with count-ups and highlights, labels are Oswald tags, and the asides are Caveat notes.
- Every picture is a duotone cut-out on a role-coloured disc (house/overpay orange, chart/invest blue), except the people, as in test 4.
- Each metaphor gets a kraft panel (the bank, tax) or a drawn diagram (see-saw, balance scale, dripping tap). Each payoff number gets an ink panel (£5 a year, £11,708 gone to fees).
- Every scene has 4–7 camera keyframes tied to the spoken words, starting zoomed in, revealing beats and ending on a push. Transitions alternate between horizontal and vertical slides, as in test 4.
- The storyboard's content, figures, order, metaphors and colour roles are kept. Its box coordinates are not: they are the main thing test 5 copied too literally.

## Build
- **Source:** `build.py`, one file. It imports `ep4_vox/vlib.py` and `render_vox.py` unchanged and writes no bytecode into that folder. Test 4's `vscenes` is stubbed out and never loaded. The plumbing (probe, alignment, timeline, render, mix) is reused from test 5. All the scenes are new.
- **Commands:** `python3 build.py preview t.. | check | render | mix | sheet | sfx`.
- **Inputs:** the script, the voice clips 01–06 and the timeline come from ep4_mix and are not modified. `figures_check.py` prints ALL FIGURES OK. The figures are also asserted in `build.py` against the library: £8,668, £7,082, £11,708, £81,007, £69,299, £1,169.18, month 258, £1,269.18 and £24,505.

## Scenes (start times identical to ep4_mix/build/timeline.json)
| # | key | start | dur |
|---|-----|------:|----:|
| 1 | hook | 0.00 | 24.10 |
| 2 | sting | 24.10 | 2.60 |
| 3 | roadmap | 26.70 | 26.26 |
| 4 | guaranteed | 52.96 | 34.34 |
| 5 | expected | 87.30 | 29.86 |
| 6 | fees | 117.16 | 35.54 |
| 7 | setup | 152.70 | 38.10 |

Total 190.8 s (3:10.8).

What each scene does:
- **hook:** the hand cut-out, then the two choices as tags. A paper see-saw slides in under the house and chart cut-outs and tips 7° on "six per cent" and back on "four per cent", then rocks. Two panels count up £8,668 and £7,082 under highlighters. A "?%" tag gets a marker ring.
- **sting:** test 4's sting: the mark wipes on, then the wordmark image and the tagline appear.
- **roadmap:** a kraft "last time" panel with the camera zoomed in on it. The camera pulls out on "the bigger question" to the headline and a handwritten "is that the best home for the money?". Four numbered step panels follow, then a handwritten "simple example, not advice" with an underline.
- **guaranteed:** the mortgage tags pop, then £1,169.18 counts up. "Every £1 you still owe costs you 5%" appears word by word, followed by a handwritten aside and an ink panel counting up £5 a year. A kraft bank panel follows: "a guaranteed 5%", a GUARANTEED tag, a ring round "can't say no", then the No fees / No tax / No bad years chips.
- **expected:** a graph-paper chart where the blue path draws on "jumps" and "drops, sometimes sharply", with arrows. The balance scale has a solid 5% block and a jittering ?% block, which tip on "heavier" and "lighter". It ends on "you only find out at the end", underlined.
- **fees:** a dripping tap, then 7% − 1% = 6% in Anton at 110 px with a highlighter on 6%. Paper bars unroll for £81,007 and £69,299, with the orange missing piece, and an ink panel counts up £11,708 gone to fees. A kraft TAX panel follows. The closing kinetic line highlights "the return after fees and tax", and 6% gets a ring.
- **setup:** tags, two jars and two people cut-outs. A's timeline is orange to 258, then blue. Handwritten notes mark "gone at month 258" with an arrow, "3½ years early", "empty for years…" and "from day one". B's timeline is kraft plus blue. Then the "same money out" tag, green ticks, and "WHOSE JAR IS FULLER?" with a highlighter.

## Deviations from the storyboard
- **Look:** the scenes are on test 4's paper ground, not the ink background. Headlines are Anton caps, not Inter ExtraBold. Labels are Oswald and the asides are Caveat. The box coordinates were re-laid out (see the top of these notes); content, order, colour roles and figures are kept.
- **Source lines:** only the expected scene keeps one ("Illustration only · investment returns are never guaranteed"). The other scenes' source footers had no room on the composed layouts and should go in the description.
- **Shapes:**
  - The see-saw and scale blocks are paper tags.
  - The "Growth / Fees / You keep" cards became a large type equation.
  - The storyboard's "You keep" outline turning orange is a marker ring round 6%.
  - The setup lane cards became test 4 style strips.
- **Roadmap:** shows four step panels, one per spoken step, as the script voices four steps (the storyboard's last-time card became the kraft recap panel). The recap adds "cleared our example mortgage 3½ years early" (month 258 is asserted).
- **Icons:**
  - The jars are ep4_vox's jar, which has coins in it. The storyboard wants empty jars, but I generated no new image.
  - The document and calculator icons come from ep3/assets.
  - The hand cut-out was added to the hook.
- **Music:** the library's ducked music bed (0.12) is kept, as in tests 4 and 5.

## Checks and output
- **Fit check:** PASS, 764 times sampled every 0.25 s, camera applied. It took three runs: the first found 9 problems (camera framing let the headline cross the logo or text cross the disclaimer, the £5 count crossed its panel's margin, the tap went 1 px off frame, the fees headline was clipped at 1.2 zoom), and two layout overlaps found in the preview were fixed beforehand.
- **Loudness:** draft −15.9 LUFS integrated, review −16.0 LUFS (loudnorm I=−16, TP=−1.5).
- **Sound effects:** 111 in total: pop 36, marker 31, slide 24, whoosh 7, chime 7, ticks 5, sting 1. Marker and slide are derived from whoosh. The 5 ticks are trimmed to each count's length (0.5–0.9 s).
- **Render time:** 515 s for frames (2 processes), 570 s with the fit check, plus about 1 min to mix and about 12 min of review encodes.
- **Visual checks:** 3 downscaled sheets (2 previews and the final contact sheet). No images were generated.
- **Files:**
  - `ep4_vox_opus2_draft.mp4`: 1920×1080, 30 fps, crf 22, AAC 192k, 71.2 MiB.
  - `ep4_vox_opus2_review.mp4`: 1920×1080, crf 32, slow, tune animation, AAC 96k, 13.5 MiB. crf 28 came to 25.7 MiB and crf 30 to 18.5 MiB: the paper grain is expensive to encode.
  - `contact_sheet.png`: 1280 wide, one late frame per scene.
