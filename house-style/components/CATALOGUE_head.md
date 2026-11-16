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
