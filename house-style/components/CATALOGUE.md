# Figures Forward component catalogue

Mix-and-match variants in the approved house style (`../VIDEO_DESIGN_STANDARD.md`, approved 16 Nov 2026), built on `lib/vlib.py`
without changing it. Added 16 Nov 2026 by the Script writer (Fable).

**How it is used**

- The **Script writer** picks one variant per beat and names it in the storyboard as `module.function`, with its parameters
  (exact on-screen text, asserted figures, cue times). Proposed rule: no two consecutive episodes reuse the same hook opener.
- The **Producer** imports the module and calls the function inside a scene:

      import sys; sys.path.insert(0, "house-style/components")
      from kit import *            # loads lib/vlib.py unchanged, plus the craft helpers
      import hooks, charts, comparisons, evidence, reveals, endcards, transitions
      def s_hook(base, d, lt, L, cam): hooks.two_paths(base, d, lt, cam, start="£100", t_split=W_("spare"), ...)

  Shorts are built with `FF_ORIENT=v` set before `import kit`, then `import shorts`.
- Every default value is a **generic illustration**, never a real figure. Episodes pass their own figures from `figures_check.py`.
- Sounds: each component reports its entrances through `vlib.appear`, so the builder's mix picks them up
  (`kit.sfx_events(key)`). The preview clips are silent.
- Logo on every component: Option C, dark label taped on (`kit.hud`). It is hidden on the end card.
- Previews are half resolution (960x540, Shorts 540x960) to keep the branch small; stills are 1280x720 (Shorts 720x1280).

**Fit check.** `python3 run.py check` (and `FF_ORIENT=v python3 run.py check`) samples every variant every 0.2 s with the
camera applied: text inside any card it touches with a 6 px margin and on-frame; no text on a picture; pictures at least
20 px from text and at least 40 px from a card they sit outside; no card over a chart; Shorts text inside the safe area
(x 110-870, y 290-1440). The check passes a component's own demo layout. A scene that changes text lengths or combines
components must still pass the episode's fit check.

**Regenerate.** `python3 run.py render [filter]`, then `python3 run.py catalogue` rebuilds this file and the contact sheets.

**Already in the reference builds, not repeated here:** see-saw, balance scale, dripping tap, repayment strips
(`reference/ep4_5b/build.py`), token split and pots morph (`reference/ep4_5c/build.py`).

## Summary

| Family | Variants | Fit check |
|---|---|---|
| Hook openers | 4: number_transform, calc_sheet_zoom, two_paths, myth_vs_reality | all PASS |
| Transitions | 4: paper_slide, page_turn, tear_away, fold | all PASS |
| Charts | 3: line_race, waterfall, timeline_markers | all PASS |
| Comparisons | 3: versus_card, two_jars, split_screen | all PASS |
| Evidence | 3: calc_sheet, payslip, ruler_span | all PASS |
| Number reveals | 3: stamp, rolling_counter, circled_figure | all PASS |
| Recap and end cards | 3: recap_checklist, recap_cards, end_card | all PASS |
| Shorts 9:16 hook openers | 3: number_transform, two_paths, myth_vs_reality | all PASS |
| Shorts 9:16 comparisons | 3: versus_card, two_jars, split_screen | all PASS |
| Shorts 9:16 number reveals | 3: stamp, rolling_counter, circled_figure | all PASS |

Total: **32 variants**. Contact sheets: `contact_sheet.png` (16:9) and `contact_sheet_vertical.png` (9:16).

## Hook openers

### `hooks.number_transform(base, d, lt, cam, ...)`

**When to use:** Open on a small everyday figure that turns into the big consequence number before the first second is out.

| Parameter | Default (illustration only) |
|---|---|
| `start` | `'£100'` |
| `start_label` | `'A MONTH'` |
| `start_value` | `100` |
| `result_value` | `24000` |
| `title` | `('KEEP IT UP FOR', '20 YEARS')` |
| `result_label` | `'PAID IN, BEFORE ANY GROWTH'` |
| `picture` | `'calendar'` |
| `pic_tag` | `'240 MONTHS'` |
| `aside` | `'example figures'` |
| `role` | `'o'` |
| `fmt` | `None` |
| `t_start` | `0.05` |
| `t_shrink` | `0.45` |
| `t_result` | `0.82` |
| `count` | `0.75` |
| `t_swipe` | `1.8` |
| `t_title` | `2.05` |
| `t_pic` | `2.6` |
| `t_label` | `3.1` |
| `t_aside` | `3.8` |

Preview: `previews/hooks__number_transform.mp4` (5.5 s) · Still: `stills/hooks__number_transform.jpg` · Fit check: PASS (56 samples)

### `hooks.calc_sheet_zoom(base, d, lt, cam, ...)`

**When to use:** Show the working: the calculation sheet with three or four lines, then a push in on the figure that matters as it is spoken.

The default camera pushes in on the total line. An episode that highlights another row (key=<row index>) should pass its own camera.

| Parameter | Default (illustration only) |
|---|---|
| `heading` | `'FIGURES FORWARD CALCULATION'` |
| `stamp` | `'worked example'` |
| `subtitle` | `'£100 a month, every month, for 20 years'` |
| `rows` | `(('Paid in each month', '£100'), ('Each year (× 12)', '£1,200'), ('Number of years', '20'))` |
| `total_label` | `'Paid in altogether'` |
| `total` | `'£24,000'` |
| `footer` | `'Example figures, for illustration'` |
| `key` | `'total'` |
| `role` | `'o'` |
| `picture` | `'calculator'` |
| `aside` | `'we show the working'` |
| `t_sheet` | `0.1` |
| `t_total` | `0.6` |
| `t_rows` | `(1.0, 1.35, 1.7, 2.05)` |
| `t_rule` | `2.3` |
| `t_pic` | `1.5` |
| `t_swipe` | `3.6` |
| `t_aside` | `4.4` |

Preview: `previews/hooks__calc_sheet_zoom.mp4` (6.0 s) · Still: `stills/hooks__calc_sheet_zoom.jpg` · Fit check: PASS (61 samples)

### `hooks.two_paths(base, d, lt, cam, ...)`

**When to use:** Open a Choice episode: the same money goes down an orange path or a blue path, each ending at its own figure, then the question.

left_role / right_role keep the colour meaning: orange = overpay or cost, blue = invest.

| Parameter | Default (illustration only) |
|---|---|
| `start` | `'£100'` |
| `start_label` | `'A MONTH'` |
| `left_label` | `'PATH ONE'` |
| `left_fig` | `'£24,000'` |
| `right_label` | `'PATH TWO'` |
| `right_fig` | `'£30,000'` |
| `question` | `'?'` |
| `ask` | `'which path ends ahead?'` |
| `left_pic` | `'house'` |
| `right_pic` | `'chart'` |
| `left_role` | `'o'` |
| `right_role` | `'b'` |
| `t_start` | `0.08` |
| `t_left` | `0.4` |
| `t_right` | `0.55` |
| `draw` | `0.5` |
| `t_left_fig` | `None` |
| `t_right_fig` | `None` |
| `t_pics` | `1.7` |
| `t_question` | `3.2` |
| `t_ask` | `4.1` |

Preview: `previews/hooks__two_paths.mp4` (6.0 s) · Still: `stills/hooks__two_paths.jpg` · Fit check: PASS (61 samples)

### `hooks.myth_vs_reality(base, d, lt, cam, ...)`

**When to use:** Open by knocking down a common belief: the myth is crossed out by hand and the real figure drops in highlighted.

The myth is on screen at once; the real figure follows at t_figure (default 2.6 s) because it is the reveal.

| Parameter | Default (illustration only) |
|---|---|
| `myth_label` | `'PEOPLE SAY'` |
| `myth` | `"£100 A MONTH WON'T CHANGE MUCH"` |
| `myth_tag` | `'MYTH'` |
| `reality_label` | `'WHAT THE SUMS SAY'` |
| `reality` | `'OVER 20 YEARS IT ADDS UP TO'` |
| `figure` | `'£24,000'` |
| `link` | `'so we did the sums'` |
| `aside` | `'paid in, before any growth'` |
| `picture` | `'coins'` |
| `role` | `'o'` |
| `t_myth` | `0.1` |
| `t_cross` | `0.95` |
| `t_tag` | `1.45` |
| `t_reality` | `1.9` |
| `t_figure` | `2.6` |
| `t_swipe` | `3.1` |
| `t_link` | `2.25` |
| `t_pic` | `3.7` |
| `t_aside` | `4.3` |

Preview: `previews/hooks__myth_vs_reality.mp4` (6.0 s) · Still: `stills/hooks__myth_vs_reality.jpg` · Fit check: PASS (61 samples)

## Transitions

### `transitions.paper_slide(a, b, p)`

**When to use:** Default scene change. The new sheet slides over the old one; alternate `direction` between scenes.

| Parameter | Default (illustration only) |
|---|---|
| `direction` | `(1, 0)` |

Preview: `previews/transitions__paper_slide.mp4` (transition 0.8 s, shown between two demo scenes) · Still: `stills/transitions__paper_slide.jpg` · Fit check: PASS (51 samples)

### `transitions.page_turn(a, b, p)`

**When to use:** A new chapter or a change of topic: the old sheet lifts at the right edge and turns away like a page, showing its darker underside, with the new scene on the page beneath.

`flip=True` turns the page the other way (alternate between scenes). `tilt` slants the fold line.

| Parameter | Default (illustration only) |
|---|---|
| `flip` | `False` |
| `tilt` | `0.16` |

Preview: `previews/transitions__page_turn.mp4` (transition 1.0 s, shown between two demo scenes) · Still: `stills/transitions__page_turn.jpg` · Fit check: PASS (51 samples)

### `transitions.tear_away(a, b, p)`

**When to use:** A hard break or a myth being thrown out: the old sheet tears top to bottom along a jagged edge, one piece slides off and the other drops away to reveal the new scene.

The tear line is fixed-seed, so it is identical on every render. `flip=True` mirrors it.

| Parameter | Default (illustration only) |
|---|---|
| `flip` | `False` |

Preview: `previews/transitions__tear_away.mp4` (transition 1.1 s, shown between two demo scenes) · Still: `stills/transitions__tear_away.jpg` · Fit check: PASS (51 samples)

### `transitions.fold(a, b, p)`

**When to use:** Putting an idea away or closing a section: the old sheet folds up panel by panel toward one side like a leaflet (thirds by default, `parts=2` for in half), revealing the new scene.

`parts` = 2 or 3 panels. `flip=True` folds toward the right instead of the left.

| Parameter | Default (illustration only) |
|---|---|
| `parts` | `3` |
| `flip` | `False` |

Preview: `previews/transitions__fold.mp4` (transition 1.2 s, shown between two demo scenes) · Still: `stills/transitions__fold.jpg` · Fit check: PASS (51 samples)

## Charts

### `charts.line_race(base, d, lt, cam, ...)`

**When to use:** Two (or three) options compared over time: the lines race left to right together, each with its label riding the tip, and the one that ends ahead gets the big end value and a handwritten callout.

| Parameter | Default (illustration only) |
|---|---|
| `title` | `'WHICH ONE'` |
| `title_key` | `'ENDS AHEAD?'` |
| `key_role` | `'b'` |
| `series` | `(('PLAN A', 'b', (0, 12, 8, 30, 24, 52, 46, 76, 90, 80, 58, 64, 50, 60, 88, 80, 118, 110, 150, 142, 200)), ('PLAN B', 'o', (0, 8, 15, 22, 30, 38, 45, 52, 60, 68, 75, 82, 90, 98, 105, 112, 120, 128, 135, 142, 150)))` |
| `fmt` | `None` |
| `winner` | `None` |
| `callout` | `'ends ahead'` |
| `x_label` | `'TIME'` |
| `label` | `'Illustration, not real returns'` |
| `t_title` | `0.2` |
| `t_panel` | `0.5` |
| `t_race` | `1.2` |
| `race_dur` | `2.6` |
| `t_end` | `None` |
| `t_callout` | `None` |

Preview: `previews/charts__line_race.mp4` (6.0 s) · Still: `stills/charts__line_race.jpg` · Fit check: PASS (61 samples)

### `charts.waterfall(base, d, lt, cam, ...)`

**When to use:** Fees, charges or deductions eating into a figure: a whole starting bar, each deduction as an orange block stepping down on its cue, ending on the green 'what you keep' bar with the one big number.

| Parameter | Default (illustration only) |
|---|---|
| `title` | `'WHERE THE'` |
| `title_key` | `'MONEY GOES'` |
| `key_role` | `'o'` |
| `start` | `('BEFORE FEES', 1000)` |
| `steps` | `(('FUND FEE', 150), ('PLATFORM FEE', 100), ('ADVICE FEE', 250))` |
| `end_label` | `'WHAT YOU KEEP'` |
| `end_role` | `'g'` |
| `start_role` | `'k'` |
| `fmt` | `None` |
| `aside` | `'half of it gone'` |
| `label` | `'Illustration, not real returns'` |
| `t_title` | `0.2` |
| `t_panel` | `0.5` |
| `t_start` | `1.1` |
| `t_steps` | `None` |
| `t_end` | `None` |
| `t_aside` | `None` |

Preview: `previews/charts__waterfall.mp4` (6.0 s) · Still: `stills/charts__waterfall.jpg` · Fit check: PASS (61 samples)

### `charts.timeline_markers(base, d, lt, cam, ...)`

**When to use:** A repayment or balance timeline: the year track unrolls, two to four markers pop on their cues with handwritten notes, and the gap between two of them (e.g. years saved) is highlighted as the one big figure.

| Parameter | Default (illustration only) |
|---|---|
| `title` | `'THE FINISH LINE'` |
| `title_key` | `'MOVES'` |
| `key_role` | `'o'` |
| `ticks` | `('0', '5', '10', '15', '20', '25')` |
| `unit` | `'YEARS'` |
| `markers` | `((0.0, 'TODAY', 'n', 'start here'), (0.86, 'PAID OFF', 'o', 'with overpayments'), (1.0, 'ORIGINAL END', 'm', 'the plan'))` |
| `span` | `(1, 2, '3½ YEARS EARLY', 'g')` |
| `label` | `'Illustration, not real figures'` |
| `t_title` | `0.2` |
| `t_panel` | `0.5` |
| `t_track` | `0.9` |
| `track_dur` | `1.0` |
| `t_markers` | `(1.1, 2.3, 2.9)` |
| `t_span` | `3.7` |

Preview: `previews/charts__timeline_markers.mp4` (6.0 s) · Still: `stills/charts__timeline_markers.jpg` · Fit check: PASS (61 samples)

## Comparisons

### `comparisons.versus_card(base, d, lt, cam, ...)`

**When to use:** Two named options head to head with one figure each, when the script says 'A or B' and then names the winner.

| Parameter | Default (illustration only) |
|---|---|
| `headline` | `'WHICH ONE'` |
| `key_word` | `'WINS?'` |
| `hk` | `'o'` |
| `a_label` | `'OPTION A'` |
| `a_sub` | `'AFTER 10 YEARS'` |
| `a_value` | `1000` |
| `a_pic` | `'house'` |
| `a_role` | `'o'` |
| `b_label` | `'OPTION B'` |
| `b_sub` | `'AFTER 10 YEARS'` |
| `b_value` | `2000` |
| `b_pic` | `'chart'` |
| `b_role` | `'b'` |
| `fmt` | `'£{:,.0f}'` |
| `vs_text` | `'VS'` |
| `winner` | `'b'` |
| `win_style` | `'tag'` |
| `win_text` | `'AHEAD'` |
| `win_role` | `'g'` |
| `t_head` | `0.15` |
| `t_a` | `0.7` |
| `t_vs` | `1.35` |
| `t_b` | `1.6` |
| `t_fig_a` | `2.3` |
| `t_fig_b` | `2.9` |
| `t_win` | `3.8` |

Preview: `previews/comparisons__versus_card.mp4` (5.5 s) · Still: `stills/comparisons__versus_card.jpg` · Fit check: PASS (56 samples)

### `comparisons.two_jars(base, d, lt, cam, ...)`

**When to use:** Two pots built from the same money that end at different sizes: the jars fill in proportion to the two figures.

| Parameter | Default (illustration only) |
|---|---|
| `headline` | `'SAME MONEY,'` |
| `key_word` | `'TWO JARS'` |
| `hk` | `'b'` |
| `a_label` | `'OPTION A'` |
| `a_value` | `10000` |
| `a_role` | `'o'` |
| `b_label` | `'OPTION B'` |
| `b_value` | `15000` |
| `b_role` | `'b'` |
| `fmt` | `'£{:,.0f}'` |
| `sub` | `'AFTER 10 YEARS'` |
| `top_level` | `0.9` |
| `diff_note` | `None` |
| `t_head` | `0.15` |
| `t_jars` | `0.7` |
| `t_fill` | `1.4` |
| `fill_dur` | `2.2` |
| `t_note` | `4.2` |

Preview: `previews/comparisons__two_jars.mp4` (6.0 s) · Still: `stills/comparisons__two_jars.jpg` · Fit check: PASS (61 samples)

### `comparisons.split_screen(base, d, lt, cam, ...)`

**When to use:** Two worlds side by side (two people, two choices, before and after): the frame is torn in half and each half carries one figure.

| Parameter | Default (illustration only) |
|---|---|
| `a_head` | `'OPTION A'` |
| `a_pic` | `'house'` |
| `a_value` | `1000` |
| `a_sub` | `'EXAMPLE TOTAL'` |
| `a_role` | `'o'` |
| `b_head` | `'OPTION B'` |
| `b_pic` | `'chart'` |
| `b_value` | `1500` |
| `b_sub` | `'EXAMPLE TOTAL'` |
| `b_role` | `'b'` |
| `fmt` | `'£{:,.0f}'` |
| `favour` | `None` |
| `shift` | `56` |
| `tint` | `0.62` |
| `t_split` | `0.1` |
| `t_a` | `0.8` |
| `t_b` | `1.4` |
| `t_fig_a` | `2.2` |
| `t_fig_b` | `2.8` |
| `t_shift` | `3.7` |

Preview: `previews/comparisons__split_screen.mp4` (5.5 s) · Still: `stills/comparisons__split_screen.jpg` · Fit check: PASS (56 samples)

## Evidence

### `evidence.calc_sheet(base, d, lt, cam, ...)`

**When to use:** The signature 'Figures Forward calculation' sheet in body gear: show the working row by row at the episode's key figure, with one highlighter swipe.

Use once at the episode's key figure (and once in the hook). The camera is a calm push to about 1.12, not a pull-out.

| Parameter | Default (illustration only) |
|---|---|
| `title` | `'FIGURES FORWARD CALCULATION'` |
| `tagline` | `'worked example'` |
| `subtitle` | `'£100 a month for 10 years (120 months)'` |
| `rows` | `(('Paid in', '£12,000'), ('Growth at an example 5% a year', '£3,500'), ('Fees taken out', '−£500'))` |
| `total` | `('Ends at', '£15,000')` |
| `key_row` | `'total'` |
| `hk` | `'o'` |
| `footnote` | `'Illustrative figures, rounded'` |
| `side_pic` | `'calculator'` |
| `side_note` | `'the working, shown'` |
| `t_sheet` | `0.15` |
| `t_rows` | `None` |
| `t_total` | `None` |
| `t_hl` | `None` |
| `t_side` | `None` |

Preview: `previews/evidence__calc_sheet.mp4` (6.0 s) · Still: `stills/evidence__calc_sheet.jpg` · Fit check: PASS (61 samples)

### `evidence.payslip(base, d, lt, cam, ...)`

**When to use:** A generic example payslip or receipt when the script walks through pay, deductions or a bill line by line and singles one line out.

Always an obviously made-up document: keep the 'EXAMPLE' tag and never pass a real employer, bank or account number.

| Parameter | Default (illustration only) |
|---|---|
| `headline` | `'WHERE DOES'` |
| `key_word` | `'IT GO?'` |
| `hk` | `'o'` |
| `title` | `'EXAMPLE PAYSLIP'` |
| `sub` | `'Example employer · example month'` |
| `lines` | `(('Gross pay', '£3,000.00', 'pay'), ('Tax', '−£400.00', 'ded'), ('Pension', '−£150.00', 'ded'), ('Other deduction', '−£50.00', 'ded'))` |
| `net` | `('NET PAY', '£2,400.00')` |
| `stamp` | `'EXAMPLE'` |
| `footer` | `'Illustration only · not a real document'` |
| `ring_line` | `2` |
| `ring_role` | `'o'` |
| `ring_note` | `'this line is the one to check'` |
| `side_pic` | `'coins'` |
| `t_head` | `0.15` |
| `t_slip` | `0.6` |
| `t_lines` | `None` |
| `t_net` | `None` |
| `t_ring` | `None` |

Preview: `previews/evidence__payslip.mp4` (6.0 s) · Still: `stills/evidence__payslip.jpg` · Fit check: PASS (61 samples)

### `evidence.ruler_span(base, d, lt, cam, ...)`

**When to use:** A length of time measured out on a paper ruler: mark the span between two points (years saved, months left, time in the market).

| Parameter | Default (illustration only) |
|---|---|
| `headline` | `'HOW MUCH'` |
| `key_word` | `'SOONER?'` |
| `hk` | `'g'` |
| `units` | `25` |
| `unit_label` | `'YEARS'` |
| `major` | `5` |
| `a` | `20` |
| `b` | `25` |
| `span_label` | `'5 YEARS EARLY'` |
| `span_role` | `'g'` |
| `span_note` | `'done here, not at the end'` |
| `ruler_fill` | `(238, 208, 128)` |
| `side_pic` | `'calendar'` |
| `t_head` | `0.15` |
| `t_ruler` | `0.7` |
| `roll_dur` | `1.3` |
| `t_span` | `2.6` |
| `t_label` | `3.2` |
| `t_note` | `4.0` |

Preview: `previews/evidence__ruler_span.mp4` (6.0 s) · Still: `stills/evidence__ruler_span.jpg` · Fit check: PASS (61 samples)

## Number reveals

### `reveals.stamp(base, d, lt, cam, ...)`

**When to use:** Land a verdict on one figure: the number sits on a card and a rubber stamp (SAVED, PAID, EXTRA...) thumps down beside it.

Stamp colour follows role: green = positive, orange = cost or overpay, blue = invest.

| Parameter | Default (illustration only) |
|---|---|
| `title` | `('THE', 'RESULT')` |
| `label` | `'OVER 20 YEARS'` |
| `figure` | `'£24,000'` |
| `word` | `'SAVED'` |
| `role` | `'g'` |
| `aside` | `'example figure'` |
| `stamp_rot` | `-8.0` |
| `t_title` | `0.15` |
| `t_card` | `0.5` |
| `t_figure` | `1.0` |
| `t_stamp` | `2.0` |
| `t_aside` | `2.9` |

Preview: `previews/reveals__stamp.mp4` (4.5 s) · Still: `stills/reveals__stamp.jpg` · Fit check: PASS (45 samples)

### `reveals.rolling_counter(base, d, lt, cam, ...)`

**When to use:** Build up to a total: the digits roll like an odometer and settle left to right, so the size of the number sinks in.

panel_role 'ink' (dark counter) or 'card'. The ticks sound is trimmed to the roll: t_roll to t_roll + roll + stagger x (digits - 1).

| Parameter | Default (illustration only) |
|---|---|
| `title` | `('ADD IT', 'ALL UP')` |
| `label` | `'TOTAL PAID IN'` |
| `figure` | `'£24,000'` |
| `sub` | `'OVER 20 YEARS'` |
| `aside` | `'example figures'` |
| `role` | `'o'` |
| `panel_role` | `'ink'` |
| `size` | `190` |
| `t_title` | `0.15` |
| `t_panel` | `0.5` |
| `t_label` | `0.85` |
| `t_roll` | `1.1` |
| `roll` | `1.0` |
| `stagger` | `0.3` |
| `t_sub` | `None` |
| `t_aside` | `None` |

Preview: `previews/reveals__rolling_counter.mp4` (5.0 s) · Still: `stills/reveals__rolling_counter.jpg` · Fit check: PASS (51 samples)

### `reveals.circled_figure(base, d, lt, cam, ...)`

**When to use:** Single out the one figure the viewer must remember: it lands on paper, gets a marker ring, an arrow and a handwritten note.

| Parameter | Default (illustration only) |
|---|---|
| `title` | `('THE NUMBER', 'TO WATCH')` |
| `label` | `'OVER 20 YEARS'` |
| `figure` | `'£24,000'` |
| `note_text` | `'this is the one that matters'` |
| `footer` | `'Example figure, for illustration'` |
| `role` | `'o'` |
| `t_title` | `0.15` |
| `t_card` | `0.5` |
| `t_figure` | `1.0` |
| `t_ring` | `1.7` |
| `t_note` | `2.4` |

Preview: `previews/reveals__circled_figure.mp4` (4.5 s) · Still: `stills/reveals__circled_figure.jpg` · Fit check: PASS (45 samples)

## Recap and end cards

### `endcards.recap_checklist(base, d, lt, cam, ...)`

**When to use:** The recap before the end card: three short lines, each ticked off as the narrator says it, with its key figure picked out.

| Parameter | Default (illustration only) |
|---|---|
| `headline` | `'THE SHORT'` |
| `key_word` | `'VERSION'` |
| `hk` | `'g'` |
| `lines` | `(('Paying in', '£100', 'a month adds up', 'o'), ('Left for', '10 years', 'it has time to grow', 'b'), ('At an example', '5%', 'that is the gap', 'g'))` |
| `key_line` | `2` |
| `side_pic` | `'scale'` |
| `t_head` | `0.15` |
| `t_sheet` | `0.6` |
| `t_lines` | `(1.2, 2.2, 3.2)` |

Preview: `previews/endcards__recap_checklist.mp4` (5.5 s) · Still: `stills/endcards__recap_checklist.jpg` · Fit check: PASS (56 samples)

### `endcards.recap_cards(base, d, lt, cam, ...)`

**When to use:** A three-point recap as numbered cards, each with one takeaway and one figure, ending on the handwritten limitation.

| Parameter | Default (illustration only) |
|---|---|
| `headline` | `'THREE THINGS'` |
| `key_word` | `'TO KEEP'` |
| `hk` | `'o'` |
| `cards` | `(('Small amounts add up over time', '£100', 'o'), ('Time does most of the work', '10 YRS', 'b'), ('The rate decides who wins', '5%', 'g'))` |
| `limit_note` | `'…if returns beat 5% after fees'` |
| `t_head` | `0.15` |
| `t_cards` | `(0.8, 1.7, 2.6)` |
| `t_note` | `3.8` |

Preview: `previews/endcards__recap_cards.mp4` (6.0 s) · Still: `stills/endcards__recap_cards.jpg` · Fit check: PASS (61 samples)

### `endcards.end_card(base, d, lt, cam, ...)`

**When to use:** The plain end screen for the last 12 s: left half empty for YouTube's video element, logo and subscribe line on the right.

Preview is 6 s of a 12 s card: hold the final state for the rest. Nothing is ever drawn at x < 960. Register/play it with the top-left logo hidden.

| Parameter | Default (illustration only) |
|---|---|
| `cta` | `'Click the logo to subscribe'` |
| `line1` | `'Narrated with an AI voice'` |
| `line2` | `'General information, not financial advice'` |
| `logo_w` | `560` |
| `cx` | `1420` |
| `t_logo` | `0.3` |
| `t_cta` | `1.1` |
| `t_arrow` | `2.0` |
| `t_lines` | `2.7` |

Preview: `previews/endcards__end_card.mp4` (6.0 s) · Still: `stills/endcards__end_card.jpg` · Fit check: PASS (61 samples)

## Shorts 9:16 hook openers

### `shorts.number_transform(base, d, lt, cam, ...)`

**When to use:** Open a Short on a small everyday figure that counts up into the consequence number on a calculation card, highlighted as it is spoken.

| Parameter | Default (illustration only) |
|---|---|
| `headline` | `(('A SMALL SUM', None), ('ADDS UP', 'o'))` |
| `start` | `100` |
| `start_top` | `'PUT IN'` |
| `start_sub` | `'A MONTH'` |
| `end` | `30000` |
| `end_top` | `'THAT COMES TO'` |
| `end_sub` | `'OVER 25 YEARS'` |
| `note_lines` | `('example: £100 x 300', 'months, no growth')` |
| `picture` | `'coins'` |
| `role` | `'o'` |
| `t_head` | `0.15` |
| `t_card` | `0.25` |
| `t_start` | `0.5` |
| `t_turn` | `1.5` |
| `t_hl` | `2.5` |
| `t_pic` | `3.0` |
| `t_note` | `3.4` |
| `count_dur` | `0.9` |

Preview: `previews/shorts_hooks__number_transform.mp4` (5.5 s) · Still: `stills/shorts_hooks__number_transform.jpg` · Fit check: PASS (56 samples)

### `shorts.two_paths(base, d, lt, cam, ...)`

**When to use:** Open a Short on a choice: one sum splits down an orange path and a blue path, each ending in its own figure, then the question.

| Parameter | Default (illustration only) |
|---|---|
| `headline` | `(('SAME MONEY,', None), ('TWO PATHS', 'o'))` |
| `token_text` | `'£100'` |
| `a_label` | `'OVERPAY'` |
| `a_value` | `'£24,000'` |
| `a_pic` | `'house'` |
| `b_label` | `'INVEST'` |
| `b_value` | `'£31,000'` |
| `b_pic` | `'chart'` |
| `a_role` | `'o'` |
| `b_role` | `'b'` |
| `question` | `'which one wins?'` |
| `t_head` | `0.15` |
| `t_token` | `0.7` |
| `t_a` | `1.3` |
| `t_b` | `1.6` |
| `t_a_tag` | `2.0` |
| `t_b_tag` | `2.4` |
| `t_q` | `3.4` |

Preview: `previews/shorts_hooks__two_paths.mp4` (6.0 s) · Still: `stills/shorts_hooks__two_paths.jpg` · Fit check: PASS (61 samples)

### `shorts.myth_vs_reality(base, d, lt, cam, ...)`

**When to use:** Open a Short by striking out a common belief, then drop in the real figure highlighted underneath.

| Parameter | Default (illustration only) |
|---|---|
| `myth_kicker` | `'PEOPLE SAY'` |
| `myth` | `'YOU NEED A BIG LUMP SUM TO START'` |
| `myth_tag` | `'MYTH'` |
| `reality_tag` | `'REALITY'` |
| `reality_lead` | `'YOU CAN START WITH'` |
| `figure` | `'£25'` |
| `figure_sub` | `'A MONTH'` |
| `note_text` | `'example figure'` |
| `picture` | `'piggybank'` |
| `role` | `'g'` |
| `t_card` | `0.15` |
| `t_myth` | `0.35` |
| `t_cross` | `1.2` |
| `t_tag` | `1.6` |
| `t_reality` | `2.1` |
| `t_lead` | `2.3` |
| `t_fig` | `2.6` |
| `t_pic` | `3.1` |
| `t_note` | `3.8` |

Preview: `previews/shorts_hooks__myth_vs_reality.mp4` (6.0 s) · Still: `stills/shorts_hooks__myth_vs_reality.jpg` · Fit check: PASS (61 samples)

## Shorts 9:16 comparisons

### `shorts.versus_card(base, d, lt, cam, ...)`

**When to use:** Compare two options head to head in a Short: two stacked cards with a VS disc between, the winner ringed and tagged.

| Parameter | Default (illustration only) |
|---|---|
| `a_label` | `'OPTION A'` |
| `a_value` | `24000` |
| `a_sub` | `'AFTER 10 YEARS'` |
| `a_pic` | `'house'` |
| `a_role` | `'o'` |
| `b_label` | `'OPTION B'` |
| `b_value` | `31000` |
| `b_sub` | `'AFTER 10 YEARS'` |
| `b_pic` | `'chart'` |
| `b_role` | `'b'` |
| `winner` | `'b'` |
| `win_text` | `'AHEAD'` |
| `t_a` | `0.15` |
| `t_b` | `0.45` |
| `t_vs` | `0.9` |
| `t_fig` | `1.2` |
| `t_win` | `2.9` |
| `count_dur` | `0.9` |

Preview: `previews/shorts_comparisons__versus_card.mp4` (5.5 s) · Still: `stills/shorts_comparisons__versus_card.jpg` · Fit check: PASS (56 samples)

### `shorts.two_jars(base, d, lt, cam, ...)`

**When to use:** Compare two end amounts in a Short as two jars filling to their true proportions, with the difference written underneath.

| Parameter | Default (illustration only) |
|---|---|
| `headline` | `(('SAME MONEY IN,', None), ('TWO JARS', 'b'))` |
| `a_label` | `'OVERPAY'` |
| `a_value` | `24000` |
| `a_role` | `'o'` |
| `b_label` | `'INVEST'` |
| `b_value` | `31000` |
| `b_role` | `'b'` |
| `note_text` | `'£7,000 more in this jar'` |
| `note_side` | `'b'` |
| `t_head` | `0.15` |
| `t_jars` | `0.9` |
| `t_fill` | `1.5` |
| `t_note` | `3.6` |
| `fill_dur` | `1.3` |

Preview: `previews/shorts_comparisons__two_jars.mp4` (6.0 s) · Still: `stills/shorts_comparisons__two_jars.jpg` · Fit check: PASS (61 samples)

### `shorts.split_screen(base, d, lt, cam, ...)`

**When to use:** Set two options against each other in a Short as two torn paper halves, orange above and blue below, one figure each.

| Parameter | Default (illustration only) |
|---|---|
| `a_label` | `'OVERPAY'` |
| `a_value` | `'£24,000'` |
| `a_sub` | `'INTEREST SAVED'` |
| `a_pic` | `'house'` |
| `a_role` | `'o'` |
| `b_label` | `'INVEST'` |
| `b_value` | `'£31,000'` |
| `b_sub` | `'POT AT THE END'` |
| `b_pic` | `'chart'` |
| `b_role` | `'b'` |
| `t_split` | `0.1` |
| `t_a` | `0.6` |
| `t_a_fig` | `0.9` |
| `t_b` | `1.7` |
| `t_b_fig` | `2.0` |
| `t_mark` | `3.2` |

Preview: `previews/shorts_comparisons__split_screen.mp4` (5.5 s) · Still: `stills/shorts_comparisons__split_screen.jpg` · Fit check: PASS (56 samples)

## Shorts 9:16 number reveals

### `shorts.stamp(base, d, lt, cam, ...)`

**When to use:** Land a verdict on a figure in a Short: the number sits on a card and a rubber-stamp word thumps down beneath it.

| Parameter | Default (illustration only) |
|---|---|
| `label` | `'TOTAL INTEREST'` |
| `value` | `'£24,000'` |
| `sub` | `'OVER 25 YEARS'` |
| `stamp_text` | `'SAVED'` |
| `stamp_role` | `'g'` |
| `note_text` | `'example figure'` |
| `t_card` | `0.15` |
| `t_fig` | `0.4` |
| `t_stamp` | `1.9` |
| `t_note` | `2.8` |
| `stamp_rot` | `-8` |

Preview: `previews/shorts_reveals__stamp.mp4` (4.5 s) · Still: `stills/shorts_reveals__stamp.jpg` · Fit check: PASS (45 samples)

### `shorts.rolling_counter(base, d, lt, cam, ...)`

**When to use:** Reveal a total in a Short with tension: odometer digits roll and lock, left to right, onto the final figure.

| Parameter | Default (illustration only) |
|---|---|
| `label` | `'TOTAL INTEREST'` |
| `value` | `48250` |
| `sub` | `'OVER 25 YEARS'` |
| `note_lines` | `("that's about", '£160 a month')` |
| `picture` | `'calculator'` |
| `role` | `'o'` |
| `t_label` | `0.15` |
| `t_panel` | `0.3` |
| `t_roll` | `0.6` |
| `t_sub` | `2.4` |
| `t_pic` | `2.8` |
| `t_note` | `3.1` |
| `roll_dur` | `1.7` |

Preview: `previews/shorts_reveals__rolling_counter.mp4` (5.0 s) · Still: `stills/shorts_reveals__rolling_counter.jpg` · Fit check: PASS (51 samples)

### `shorts.circled_figure(base, d, lt, cam, ...)`

**When to use:** Single out one figure in a Short: it lands big, a marker ring is drawn round it and a handwritten note points at it.

| Parameter | Default (illustration only) |
|---|---|
| `headline` | `(("THAT'S AN EXTRA", None),)` |
| `value` | `'£7,000'` |
| `sub` | `'OVER 25 YEARS'` |
| `note_lines` | `('more than', 'you put in')` |
| `picture` | `'jar'` |
| `role` | `'o'` |
| `t_head` | `0.15` |
| `t_fig` | `0.6` |
| `t_ring` | `1.5` |
| `t_sub` | `2.0` |
| `t_note` | `2.7` |
| `t_pic` | `3.1` |

Preview: `previews/shorts_reveals__circled_figure.mp4` (5.0 s) · Still: `stills/shorts_reveals__circled_figure.jpg` · Fit check: PASS (51 samples)

