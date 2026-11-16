# Figures Forward — Video Design Standard (house style)

**Status:** Approved by Darran, 16 Nov 2026. Agreed through the Episode 04 style tests (12–16 Nov) and the six Learnings log rows approved on 16 Nov at 13:03. The winning reference is the **spliced build**: build 5c's hook (0:00–0:24), then build 5b for the rest.
**Applies from:** Episode 05 onwards, for long videos and Shorts.
**Change rule:** change this standard only through Learnings log rows that Darran marks Approved.

---

## 1. What we are aiming for

A calm, credible, explainer-collage look. Paper, cut-outs and handwritten notes carry one clear number at a time, timed to the voice. The hook grabs attention, then the body explains calmly. The figures are the hero, the working is shown, and nothing moves without a reason.

## 2. How a video is made (pipeline)

1. **Strategist** writes the brief and tags the treatment: *Consequence*, *Hidden Trap* or *Choice*. Episode 04 is a Choice.
2. **Script writer (Fable only)** writes the script and a precise storyboard:
   - beats tied to narration cues (e.g. "@0.30")
   - exact on-screen text, colour roles and layout boxes
   - which reusable component each beat uses
   - which pictures it needs, existing ones first
   - all figures checked in a `figures_check.py` with asserts
3. **Producer (Opus)** voices the script, then builds the video from the storyboard using the style library (section 10). It renders a ~3-minute draft for Darran's review, then the full episode, Shorts and thumbnails.
4. **QA** runs the checks in section 9 before anything reaches Darran.
5. **Publisher** works from the hand-off on the hub. Nothing goes public without Darran's approval.

Keep heavy work in helper agents with fresh context. Keep the chat for decisions only.

## 3. Structure: two gears

| Part | Time | Gear | What it does |
|---|---|---|---|
| Hook | first ~20–25 s | **Hook gear** (from 5c) | Dense and fast. The consequence number is on screen early, numbers transform, there's a visual transformation and a zoom into the calculation sheet with a highlighter, and the sound is tight and synced. |
| Logo sting | ~2.6 s | Sting | Logo sting after the hook. |
| Body | rest of video | **Body gear** (from 5b) | Calm and consistent, so each idea lands. A new visual development only when the explanation needs it, typically every 3–6 s. |
| End | last 12 s | End screen | Plain. Left half empty for YouTube's video element; logo and "Click the logo to subscribe" on the right; AI-voice and not-advice lines. |

**Technique budget (body):** at most **one highlighted "moment" per scene**, on that scene's key number or reveal. Examples are the calculation sheet with a highlighter, a number transformation, or a chart morphing into the next idea. Everything else stays in 5b's rhythm.

**One dominant number per screen.** Every other element is quieter, in size, colour and motion.

Use the **focus technique** (an item grows and comes to the centre while the rest dims) only for a specific call-out, never for every item.

## 4. Look

**Paper and layers**
- Grained paper background (PAPER `#ECE4D3`) with fibres and a soft vignette. Use cards (`#FBF8F0`) and kraft panels (`#CDB086`) for grouping, with dark ink (`#0F1218`) for contrast panels.
- Pictures are printed-paper cut-outs with white borders, soft drop shadows and a slight rotation, often on coloured discs, with paper tags for labels. Use gentle parallax between layers.
- Charts are drawn on graph paper. Lines draw on; bars appear whole and never grow from a stub. Label them with handwritten callouts.

**Colour meaning (never change):** orange `#FF8A1F` = overpay or emphasis; blue `#178AFD` = invest; green `#50C88C` = positive; greys for context. Highlighter tints: orange `#FFBC68`, blue `#96CAFF`, green `#A0E4BE`.

**Typography**
- Headlines: Anton, in big capitals, dropping in word by word, with a highlighter swipe on the key word as it's spoken.
- Sub-heads and numbers: Oswald 600.
- Handwritten notes, arrows and circles: Caveat 700. Permanent Marker for occasional emphasis.
- UI and labels: Inter.

**Camera:** each scene starts close and pulls out to reveal each point as it's spoken. Slides between scenes alternate direction, eased with no jitter. Every piece of text must stay on-frame during camera moves.

**Logo:** use **Option C**, "dark label, taped on". The existing on-dark lockup sits on a dark ink label, tilted about 1.5°, with a soft shadow and a strip of semi-transparent tape on its top-right corner. It stays top-left at the same size on every scene, and is hidden on the sting and end cards. Mock-up: `reference/logo_options.png`, third row.

**Disclaimer:** "General information, not financial advice" is visible from the first frame.

## 5. The calculation sheet (signature)

A paper "Figures Forward calculation" sheet showing our real working, from the asserted figures. Use it **once in the hook** and **once at the episode's key figure**: the camera zooms in and the number that matters gets a highlighter swipe as it's spoken. It shows the channel does the maths. Never show a real bank's documents, names, logos or account numbers. Any receipt or payslip must be generic.

## 6. Reusable components (name them in the storyboard)

1. **Two-option comparison:** versus card, scale, see-saw or two jars.
2. **Repayment or balance timeline:** with year track and markers.
3. **Animated chart:** line draw-on, whole bars, waterfall for fees, morph to the next chart.
4. **Number reveal:** count-up (ticks trimmed to the count), stamp, circle or highlighter.
5. **Calculation highlight:** the calculation sheet zoom.

Each component should have 2–3 visual variants in the library so episodes can mix and match. Collecting these is a one-off Fable task, prompt to follow. Keep a picture index on the hub (name, what it shows, which episode added it), and the storyboard picks existing pictures before asking for new ones.

## 7. Shorts (9:16)

- **First 3 seconds:** the consequence number is already on screen, then explained.
- **Arc:** Hook → Context → Explanation → Reveal → Takeaway, ending with the result **and its limitation** (e.g. "…if returns beat 5% after fees").
- Same look, colours and logo as the long video, with captions burned in. Text sits inside the safe area (x 110–870, y 290–1440), at least 20 px below the logo and above the caption area.

## 8. Sound

- Episode 01 sound set (whoosh, pop, chime, ticks, sting), plus marker and paper-slide sounds derived from it. No newly generated sounds.
- Sounds are subtle and synced to movement and reveals. Hook gear is denser; body gear is quieter (5b used about 110 effects in 3 minutes; 5c's 133 was too busy for the body).
- Count-up ticks stop when the number stops.
- Mix: voice, plus music ducked under the voice, plus sound effects. Loudness −16 LUFS, true peak ≤ −1.5 dBTP.
- Voice: "Alistair – Clear, Neutral and Informative" (Eleven v4, default settings), tone-checked against the Episode 01 reference. AI narration is always disclosed.

## 9. Checks (must pass before Darran sees a build)

- **Figures:** every figure is computed and asserted in code. Correct the brief if it's wrong, and flag the correction.
- **Fit check, sampled through camera moves:**
  - text sits inside any card or panel it touches, with a 6 px margin, and stays on-frame
  - no text on a picture
  - pictures are at least 20 px from any text and at least 40 px from any card they sit outside
  - no card over a chart
- **Honesty:** illustrative charts are labelled "Illustration, not real returns", with no year labels. If a thumbnail figure depends on an assumption, the assumption appears on the thumbnail.
- **Wording:**
  - £ on screen, "pounds" in narration, "per cent" in captions
  - never name ISA, SIPP or 401(k); say "tax-free or tax-relieved accounts where you live"
  - no personal questions to viewers
- **Thumbnails:** Stamp house style; no picture touching text; bottom-right corner left empty.

## 10. Files

- **Style kit:** branch `house-style` of the internal file host, folder `house-style/`. It contains:
  - `lib/vlib.py`: paper, cut-outs, highlighter, marker, kinetic type, camera, fit recording
  - `lib/render_vox.py`: frame, camera, mix, fit check and render tail
  - `lib/vscenes.py`: the original craft reference
  - `fonts/`, `assets/`, `sfx/`
- **Reference builds:**
  - `reference/ep4_5b/build.py`: body-gear reference
  - `reference/ep4_5c/`: hook-gear reference
  - `reference/ep4_story/`: Fable script, storyboard, figures check and timeline
  - `reference/ep4_reference_spliced.mp4`: the approved look
- The file host is internal only and is never referenced publicly.

## 11. Cost guide (API-equivalent, from the tests)

| Item | Approx. cost |
|---|---|
| Fable script and storyboard, 3 min | ~$2.70–3.50 |
| Opus build, 3 min, house style from the library | ~$4.50–8.50 |
| Full 9-minute episode, house style | ~$25–35 |

Run each role in a fresh chat or helper agent. Long chats re-read everything and cost several times more.

## 12. Measuring it

The Analyst compares first-30-second retention, average view duration and completion between Episode 04 (old style) and the first episode in the house style. One video doesn't prove the style; review after several episodes.
