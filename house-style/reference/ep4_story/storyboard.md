# Episode 04 — storyboard, first ~3 minutes
"Overpay the mortgage or invest? The one number that decides it" · script in `script.txt` · figures in `figures_check.py` (passing).

## Conventions (apply to every scene)
- Frame 1920×1080, ink background, Episode 03 toolkit (`title`, `card`, `icon`, `hbar`, `count`, `appear`, `source`, `header`). Boxes are `[x1,y1,x2,y2]`; points are `(x,y)`.
- Timing: clip = 0.3 s lead + narration length L + 1.2 s hold. A cue `@0.30` means `at(L, 0.30)`; `@0.00` means scene start (lt = 0).
- Colour roles: ORANGE = overpay / emphasis · BLUE = invest · GREEN = positive · MUTED grey = labels · FG = neutral values · SLATE = source line.
- Header lockup at (120,46), 62 px high, on every scene except the sting. Side margins 120 px (content x 120–1800).
- `title()` = 64 ExtraBold at (120,150); subtitle 38 Regular MUTED at (122,234). Source line 24 SLATE at (120,1035).
- Sound: whoosh at every scene start; pop on each card/icon entrance; chime only where marked; ticks only under a count-up, cut to the count's length.
- Icons pop in (0.5 s overshoot) then stay still. Only the see-saw and scale diagrams move. Bars fade in whole.
- Spacing: pictures ≥20 px from any text and ≥40 px from cards they sit outside; all text inside its card. If a line overruns its card in the fit check, drop its size in 2 px steps; do not move elements.
- Text in "quotes" is exact on-screen text. Sizes are px, Inter; weights as named.
- Estimated durations assume 155 words a minute; real cue times follow the voiced clip lengths.

| # | key | words | narration | clip |
|---|-----|------:|----------:|-----:|
| 1 | hook | 62 | 24.0 s | 25.5 s |
| 2 | sting | – | – | 2.6 s |
| 3 | roadmap | 69 | 26.7 s | 28.2 s |
| 4 | guaranteed | 92 | 35.6 s | 37.1 s |
| 5 | expected | 78 | 30.2 s | 31.7 s |
| 6 | fees | 93 | 36.0 s | 37.5 s |
| 7 | setup | 105 | 40.6 s | 42.1 s |
| | **total** | 499 | **3:13** | **3:25** |

---

## 1. `hook` — the question and the payoff inside 10 seconds (~25.5 s)
**Voiced metaphor:** "It's a see-saw, and one number decides which way it tips."
Icons: coins, house, chart (new). Diagram: see-saw (drawn in code).

| Cue | Build |
|---|---|
| @0.00 | Whoosh. Disclaimer from frame 1, held all scene: "General information, not financial advice", 26 Regular SLATE, right-anchored at (1800,1035). Source line: "Figures Forward calculation · £100 a month for 25 years · returns after fees". |
| @0.00 | `coins` icon 240 px, centre (260,330). Headline "A spare £100 a month", 72 ExtraBold FG at (420,230). Under it "£200,000 mortgage · 25 years · 5% · £1,169.18 a month", 30 Regular MUTED at (422,325). |
| @0.00 | See-saw fades in level (no sound): pivot triangle apex (960,800), base y 900, base width 140, fill PANEL, outline LINE. Beam centre (960,790), 880 long (x 520–1400), 18 thick, rounded, MUTED. `house` icon 150 px riding the left end (centre (600,700) when level); `chart` icon 150 px riding the right end (centre (1320,700)). Icons move only with the beam ends. |
| @0.14 "on the mortgage" | Pop. Orange-tint card (fill 42,30,18) [420,380,790,470]: "Overpay?" 50 ExtraBold ORANGE, centred (605,425). |
| @0.24 "into investments" | Pop. Card [830,380,1200,470], BLUE outline: "Invest?" 50 ExtraBold BLUE, centred (1015,425). |
| @0.30 "if investing returns six per cent" | Beam tilts 7° right-side down over 0.8 s (chart end sinks, house end rises). |
| @0.48 "about eight thousand, seven hundred" | Pop + ticks. Card [1480,600,1800,820]: "B: invest" 30 SemiBold MUTED, centred (1640,640); count-up to "+£8,668" 60 ExtraBold BLUE, centred (1640,710), 0.9 s; "ahead at 6%" 30 Regular MUTED, centred (1640,780). |
| @0.60 "At four per cent" | Beam swings through level to 7° left-side down over 0.8 s. |
| @0.68 "by about seven thousand" | Pop + ticks. Card [120,600,440,820]: "A: overpay" 30 SemiBold MUTED, centred (280,640); count-up to "+£7,082" 60 ExtraBold ORANGE, centred (280,710); "ahead at 4%" 30 Regular MUTED, centred (280,780). |
| @0.76 "It's a see-saw" | Beam returns to level, then rocks ±2° on a slow 2.4 s sine until the scene ends. |
| @0.82 "one number decides" | Chime. Orange-tint card under the pivot [860,915,1060,985]: "? %" 48 ExtraBold ORANGE, centred (960,950). Hold to end. |

Clearances: icon travel is ±54 px vertically (y 571–829 overall); nearest cards are 85 px away at x 440 and x 1480.

## 2. `sting` — logo sting (2.6 s, no narration)
Reuse the Episode 03 sting unchanged (`ep3/_sting.py`): gradient mark and wordmark on ink, sting sound, no header, no other elements.

## 3. `roadmap` — what the episode will do (~28.2 s)
Four picture cards in a row, Episode 03 `s_promise` layout: card i at x = 120 + i×435, box [x,300,x+390,800]; icon 230 px centred (x+195,470); heading 42 ExtraBold centred at (x+195,640); sub-line 32 Regular MUTED centred from y 705, wrapped to 350 px; "→" 28 Bold between cards at (x+412,550), pulsing MUTED↔ORANGE. Icons: house, lock, chart (new), calculator.

| Cue | Build |
|---|---|
| @0.00 | Whoosh. Title "Overpay or invest?". Card 1 pops: `house`; heading "Last time" (FG); sub "what +£100 a month does". |
| @0.24 "the bigger question" | Subtitle fades in: "Is that the best home for the money?" |
| @0.41 "First, what overpaying" | Card 2 pops, orange-tint fill: `lock`; heading "Overpaying" (ORANGE); sub "what it really earns". |
| @0.50 "Then what investing" | Card 3 pops: `chart`; heading "Investing" (BLUE); sub "minus fees and tax". |
| @0.70 "Then we'll race the two" | Card 4 pops: `calculator`; heading "The race" (FG); sub "£100 a month · 25 years". |
| @0.82 "a simple example" | Line at (120,900), 36 Regular MUTED: "A simple example, not advice. There's no single right answer." |

## 4. `guaranteed` — overpaying earns a guaranteed 5% (~37.1 s)
**Voiced metaphor:** "a savings account paying a guaranteed five per cent, from a bank that can't say no."
Icons: house, coins, bank. Source line: "Figures Forward calculation · interest saved on a 5% mortgage".

| Cue | Build |
|---|---|
| @0.00 | Whoosh. Title "What overpaying really earns"; subtitle "£200,000 · 25 years · 5% fixed". Card [120,320,760,560]: `house` 140 px at (210,440); "Monthly payment" 32 SemiBold MUTED at (300,350); "5% fixed · 300 payments" 32 Regular MUTED at (300,490). |
| @0.16 "one thousand, one hundred…" | Ticks. In the same card, count-up to "£1,169.18" 70 ExtraBold FG at (300,395), 0.8 s. |
| @0.30 "Every pound you still owe" | Pop. Card [120,590,760,760]: "Every £1 you owe costs" 32 SemiBold MUTED at (150,615); "5% a year" 70 ExtraBold ORANGE at (150,660). |
| @0.43 "every pound you overpay" | Pop. Card [840,320,1800,560]: `coins` 140 px at (930,440); "Overpay an extra £100" 32 SemiBold MUTED at (1020,350); "interest you never pay, every year" 32 Regular MUTED at (1020,490). |
| @0.62 "about five pounds" | Ticks, then chime as it lands. Count-up to "£5 a year" 70 ExtraBold GREEN at (1020,395), 0.6 s (count the number; " a year" static). |
| @0.72 "Think of overpaying as a savings account" | Pop. Orange-tint card [840,590,1800,860]: `bank` 150 px at (940,725); "Like a savings account paying" 34 SemiBold FG at (1050,625); "a guaranteed 5%" 64 ExtraBold ORANGE at (1050,675). |
| @0.86 "from a bank that can't say no" | Chime. Same card: "from a bank that can't say no" 34 SemiBold FG at (1050,770). |
| @0.93 / @0.96 / @0.985 | Three pops. Chips, 30 Bold GREEN, text centred: [120,800,300,880] "No fees" · [320,800,490,880] "No tax" · [510,800,760,880] "No bad years". |

## 5. `expected` — investing is an expected return (~31.7 s)
**Voiced metaphor:** "Picture a balance scale… a solid block… a block that won't sit still."
Icons: chart (new). Diagram: balance scale (drawn in code). Source line: "Illustration only · investment returns are never guaranteed".

Scale geometry (right half): post from (1490,430) to (1490,860), 14 thick; base plate [1390,860,1590,880]; beam centre (1490,430), 440 long (x 1270–1710), 14 thick; each pan a 180×12 plate hung 200 px below its beam end on two thin lines (left pan x 1180–1360, right pan x 1620–1800, pan y 630 when level). Blocks are 150×110 rounded rectangles sitting on the pans, text centred inside. Labels sit below, fixed (they do not move with the pans).

| Cue | Build |
|---|---|
| @0.00 | Whoosh. Title "What investing can earn". `chart` icon 260 px at (300,470). Card [500,330,1100,560], BLUE outline: "Investing" 32 SemiBold MUTED at (530,355). Scale fades in empty and level, drawn in LINE colour (dim), no blocks. |
| @0.26 "an expected return" | Pop. In the card: "Expected" 70 ExtraBold BLUE at (530,400). Subtitle fades in: "An expected return, not a promised one". |
| @0.33 "not a promised one" | In the card: "not promised" 40 Bold FG at (530,490). |
| @0.38 "Some years it jumps" | Pop. Chip [500,590,790,670]: "Good years ↑" 32 Bold GREEN, centred. |
| @0.43 "Some years it drops" | Pop. Chip [810,590,1100,670]: "Bad years ↓" 32 Bold FG, centred. |
| @0.50 "Picture a balance scale" | Scale brightens from LINE to MUTED over 0.4 s (no sound). |
| @0.58 "a solid block" | Pop. ORANGE block lands on the left pan: "5%" 48 ExtraBold FG inside. Fixed label "Guaranteed" 32 Bold ORANGE centred (1270,740). Beam dips 5° left. |
| @0.70 "On the other" | Pop. BLUE block lands on the right pan: "?%" 48 ExtraBold FG inside. Fixed label "Expected" 32 Bold BLUE centred (1710,740). Beam returns to level. |
| @0.76 "won't sit still" | Beam rocks ±3° on a 1.8 s sine; the blue block also jitters ±4 px sideways on its pan. The orange block never jitters. |
| @0.81 "might be heavier" | Beam swings to 6° right-side down (0.5 s). |
| @0.86 "might be lighter" | Beam swings to 6° left-side down (0.5 s), then resumes the ±3° rock. |
| @0.91 "You only find out at the end" | Chime. Text "You only find out at the end" 36 Bold FG at (500,730). |

Clearances: pan travel at 6° is ±23 px (pan and block stay within y 497–665); fixed labels start at y 724. Scale's left edge x 1180 is 80 px right of the card/chips and of the closing line.

## 6. `fees` — fees and tax shrink the expected return (~37.5 s)
**Voiced metaphor:** "Fees come out every year, like a dripping tap."
Icons: tap, document. Source line: "Figures Forward calculation · £100 a month for 25 years, monthly compounding".

| Cue | Build |
|---|---|
| @0.00 | Whoosh. Title "The return you actually keep"; subtitle "£100 a month invested for 25 years". `tap` icon 220 px at (250,450). Card [440,340,740,560]: "Growth" 32 SemiBold MUTED centred (590,385). |
| @0.08 "like a dripping tap" | Drips: one small ORANGE drop (12 px) every 0.9 s falls from the spout, (250,565) to (250,615), fading out; continues to the end of the scene. No sound. |
| @0.19 "seven per cent" | Pop. In the Growth card: "7%" 90 ExtraBold BLUE centred (590,470). |
| @0.27 "charges take one" | Pop. "−" 70 Bold MUTED centred (790,450). Card [840,340,1140,560]: "Fees" 32 SemiBold MUTED centred (990,385); "1%" 90 ExtraBold ORANGE centred (990,470). |
| @0.31 "You keep six" | Pop. "=" 70 Bold MUTED centred (1190,450). Card [1240,340,1540,560]: "You keep" 32 SemiBold MUTED centred (1390,385); "6%" 90 ExtraBold FG centred (1390,470). |
| @0.44 "about eighty-one thousand" | Pop. Label "At 7%" 34 SemiBold MUTED at (120,680) left-middle. Whole BLUE bar x 440–1340 (900 wide), y 640–720. Value "£81,007" 40 ExtraBold FG inside the bar, right-anchored at (1320,680). |
| @0.50 "about sixty-nine thousand, three hundred" | Pop. Label "At 6%" at (120,800). Whole BLUE bar x 440–1210 (770 wide = 0.855), y 760–840. Value "£69,299" inside, right-anchored at (1190,800). |
| @0.57 "Nearly twelve thousand pounds" | Whole ORANGE segment x 1210–1340, y 760–840 fades in (the missing piece). Pop + ticks, chime as it lands: orange-tint card [1400,730,1800,880]: "Gone to fees" 30 SemiBold MUTED at (1430,748); count-up to "£11,708" 64 ExtraBold ORANGE at (1430,792), 0.9 s. |
| @0.65 "Tax can take another slice" | Pop. `document` icon 110 px at (250,940). Card [440,890,1340,990]: "Tax can take another slice" 32 Bold FG at (470,903); "unless in tax-free or tax-relieved accounts where you live" 28 Regular MUTED at (470,947). |
| @0.84 "the return after fees and tax" | Chime. Orange-tint card [1380,890,1800,990]: "Compare your mortgage rate with" 26 Regular MUTED centred (1590,922); "return after fees and tax" 28 Bold ORANGE centred (1590,960). The "You keep" card outline turns ORANGE at the same moment. |

Never show account names (no ISA, SIPP, 401(k)).

## 7. `setup` — the fair head-to-head (~42.1 s)
**Voiced metaphor:** "Think of two jars… whose jar is fuller?"
Icons: jar (new) ×2, calculator. Source line: "Figures Forward calculation · A's final mortgage payment in month 258 is £69.48; the other £1,199.70 goes in the jar".

Two lanes: card A [120,320,940,860] ORANGE outline; card B [980,320,1800,860] BLUE outline. Timeline bars are 500 px = 300 months, 60 high.

| Cue | Build |
|---|---|
| @0.00 | Whoosh. Title "A fair race: two people, one spare £100". Both lane cards appear. "Person A: overpay" 44 ExtraBold ORANGE at (150,345). "Person B: invest" 44 ExtraBold BLUE at (1010,345). `jar` 200 px at (250,560) in A; `jar` 200 px at (1110,560) in B (pops 0.15 s apart). |
| @0.09 "the same mortgage" | Subtitle fades in: "Same mortgage · same £100 · 25 years". |
| @0.21 "Person A overpays" | Pop. A's timeline: whole ORANGE bar x 400–830, y 440–500 (months 1–258); "Overpay +£100" 26 SemiBold FG inside at (415,470) left-middle. Ticks under the bar, 24 Regular SLATE: "month 1" left-anchored at (400,512); "258" centred (830,512). |
| @0.24 "stays empty for years" | Caption under A's jar: "Empty at first" 28 Regular MUTED centred (250,700). |
| @0.33 "gone at month two hundred and fifty-eight" | Chime. "Mortgage gone: month 258" 34 Bold FG at (400,570); @0.41 "3½ years early" 30 Regular GREEN at (400,618). |
| @0.46 "From then on" | Pop. Whole BLUE segment x 830–900, y 440–500 (months 259–300); tick "300" right-anchored at (900,512). "Then £1,269.18 a month" 34 Bold BLUE at (400,690); "into the jar, for the last 42 months" 28 Regular MUTED at (400,738). |
| @0.64 "Person B pays the mortgage as normal" | Pop. B's timeline: whole BLUE bar x 1260–1760, y 440–500; "Invest £100 every month" 26 SemiBold FG inside at (1275,470). Ticks "month 1" at (1260,512), "300" right-anchored at (1760,512). "Mortgage paid as normal" 34 Bold FG at (1260,570); "ends month 300" 30 Regular MUTED at (1260,618). |
| @0.72 "drops a hundred pounds into the jar" | Pop. "£100 a month into the jar" 34 Bold BLUE at (1260,690); "for all 300 months" 28 Regular MUTED at (1260,738). Caption under B's jar: "From day one" 28 Regular MUTED centred (1110,700). |
| @0.83 "Same money out" | Pop. Card [120,890,1100,990]: `calculator` 76 px at (180,940); "Same money out every month: £1,269.18 each" 34 Bold FG at (250,940) left-middle. |
| @0.95 "whose jar is fuller?" | Chime. Orange-tint card [1140,890,1800,990]: "Whose jar is fuller?" 44 ExtraBold ORANGE centred (1470,940). Hold to end; the next scene runs the race. |

The jars stay empty in this scene (no coins, no fill): the result belongs to the next scene.

---

## Figure notes for the Producer and Darran
- **Brief discrepancy (flag):** the brief's Option A column (£57,115 / £58,122 / £59,152 / £60,205) leaves out £1,199.70 in month 258, when the final mortgage payment is only £69.48. On a like-for-like basis (both people spend £1,269.18 every month) A is £58,495 / £59,551 / £60,631 / £61,737. Option B is unchanged.
- Corrected differences: 4% overpay ahead by £7,082 (brief £5,702); 5% dead level (brief: investing ahead £1,429); 6% investing ahead by £8,668 (brief £10,147); 7% investing ahead by £19,270 (brief £20,802). Break-even is exactly 5.00%, the mortgage rate (brief "about 4.9%").
- Knock-on outside this storyboard: thumbnail B ("£69,299 vs £59,152") should read £69,299 vs £60,631; the rest of the script should use the corrected column.
- Hook figures use the corrected values. All other figures (£1,169.18, month 258, 3½ years, £1,269.18, £81,007, £69,299, £11,708) match the brief.
- "Shares have tended to grow faster than that" is a general historical statement with no figure attached; the brief's Vanguard and Charles Stanley sources cover it for the description.
