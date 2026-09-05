---
name: vt-icon-pipeline
description: "Use whenever preparing button/icon graphics for an ISOBUS VT pool (ISO-Designer) from a mockup screenshot or a standard ISO 7000 symbol — cropping a mask out of a photo, splitting a SoftKeyMask into its physical keys, and converting to the correct BMP convention (multi-color+pink vs monochrome+white). Trigger on any request to extract/crop/prepare icons for a VT pool, or on `vt_crop_tools.py` / `mark_and_crop.bat`."
---

# VT icon preparation pipeline

Reference knowledge for turning a mockup screenshot (Gemini-generated concept
art, a photo of a real terminal, a hand sketch) or a standard ISO 7000 symbol
into button/icon graphics ready to drop into an ISO-Designer VT pool
(`.jop`/`.jvi` — see the separate `iso-designer-jop` skill for editing the
pool XML itself; this skill is only about producing the image assets).

Canonical implementation: `vt_crop_tools.py` + `mark_and_crop.bat`, first
built in `C:\git\fh\Krauternter\UI-Spec\`. Copy/adapt these into any project
that needs this pipeline rather than re-deriving it — the tool is generic
(nothing Krauternter-specific except the numbers baked into `mark_and_crop.bat`
for that project's own mockups).

## Two completely different output conventions — decide first

Real VT pools use two genuinely different icon conventions. Getting this
wrong (as happened once) produces a working-but-wrong asset that later needs
regenerating.

| | Multi-color custom icon | Standard monochrome (ISO 7000 etc.) |
|---|---|---|
| Use when | The icon has real semantic color (green=up/on, red=down/off) | Icon is a pure black-outline silhouette, no real color content |
| Color depth | Reduced palette (this project: 16, snapped to the websafe grid 0/51/102/153/204/255 per channel) | 1-bit, pure black/white |
| Background/TransColor | **Pink**, `(255,0,255)` = `TransColor 16711935` (0xFF00FF) | **White**, `(255,255,255)` = `TransColor 16777215` (0xFFFFFF) |
| Real-pool example | The custom Hauptmenü icons (`Erntebetrieb.png` etc.) | `BACK.bmp` (stock nav icon) |
| `isobus` command | default mode | `--mono` flag |

Check an existing similar icon's `TransColor` property in the pool before
guessing which convention a new icon should follow.

For genuine ISO 7000 symbols specifically, there's already an established
reference pipeline in a sibling project:
`C:\git\ms\4diac_training1\Ventilsteuerung\ISO-DesignerProjects\Workspace_TECU\DefaultPool\img\script\_0_Convert.bat`
— shave the registration-mark border, resize to 64x64 (SoftKeyMask) / 98x98
(DataMask), `-monochrome`, save `BMP3:`. Measure the actual registration-mark
thickness per source (`-shave 2x2` was right for that project's source
resolution but wrong for a 200x200 ISO 7000 PNG, which needed ~20px — always
verify by cropping a corner and looking, don't assume the reference value).

## Physical size constraints

- A SoftKey object is **80x80 px, hard maximum**. Every SoftKeyMask button
  icon must fit inside that after all processing — check with `identify`,
  don't assume trim+crop already got you there.
- DataMask-embedded icons commonly used at ~98x98 in the sibling project's
  convention; SoftKeyMask icons there at 64x64. Match whatever the target
  pool's own existing icons use rather than assuming one fixed number.

## The `vt_crop_tools.py` workflow

Every command is deliberately manual/pixel-precise — no contour detection,
no AI segmentation (`rembg` was tried and abandoned: it hallucinates on
small, ambiguous UI crops that don't look like "a photo subject on a
background", which is what these background-removal models are actually
trained for).

1. **`mark <image> <x1> <y1> <x2> <y2> [output]`** — draws a red rectangle
   at the given corners over a COPY of the image (non-destructive preview
   only). Iterate coordinates until the rectangle exactly wraps the target
   region, checking the output PNG visually each time.
2. **`crop <image> <x1> <y1> <x2> <y2> <output>`** — cuts the confirmed
   rectangle for real.
3. **`markx <image> <x> [output]`** / **`splitx <image> <x> <left> <right>`**
   — same mark/confirm discipline, but for a single vertical split line
   (e.g. separating DataMask from SoftKeyMask within an already-cropped
   mask) instead of a full rectangle. Height is read from the image itself,
   never hand-computed — a value that has to be kept in sync by hand with
   another step's output *will* drift the moment that other step's
   coordinates change (this happened once with a duplicated height
   constant).
4. **`split <image> <cols> <rows> <output_dir> [prefix] [row_h] [col_w] [y_start] [x_start]`**
   — cuts a grid (e.g. SoftKeyMask → 12 buttons). **Do not assume
   `image_height / rows` is the real per-row pitch.** Card-style mockups
   often have a gap between cells, so pitch = card_size + gap ≠
   total_height / count — dividing naively drifts more with every row and
   eventually bleeds one row's content into the next. Measure the real
   pitch first: sample a column of pixels near a cell edge (not through
   icon content) and look for the actual light/dark plateau transitions,
   then pass `row_h`/`y_start` explicitly.
5. **`trim <image_or_dir> <links> <oben> <rechts> <unten> <output>`** — same
   4 margins for every file in a batch, so relative scale between icons is
   preserved. Rounded card corners leave small residual artifacts that a
   straight trim can't reach — don't chase them here, `isobus`'s
   corner-blanking handles that next.
6. **`resize <image_or_dir> <max_w> <max_h> <output>`** — shrink-to-fit
   (PIL `.thumbnail`, aspect preserved, never upscales). Always run this
   before `isobus` for SoftKeyMask icons — see the 80x80 constraint above.
7. **`isobus <image_or_dir> <output> [corner_px=8] [max_colors=16] [fuzz=30] [--mono]`**
   — the final conversion: background detection + color reduction/mono +
   correct TransColor + `BMP3` save. See below for how background detection
   actually works — it's the one non-obvious part of this whole pipeline.

### Background detection: border-connectivity, not global color distance

A naive "is this pixel's color close to the sampled background color"
check fails in both directions on real icons:

- **False positive (background bleeds into the icon):** an icon element
  with a light metallic gradient (a chrome/steel highlight) can pass
  through shades colorimetrically close to the pale background, even
  though it's visually and topologically part of the icon, walled off from
  the true background by a black outline. Plain distance-thresholding
  turns those pixels pink/transparent — visible as the background color
  "bleeding into" the icon.
- **False negative (icon interior wrongly becomes foreground):** an icon
  that's a pure outline (e.g. a house symbol) has an interior that is
  *exactly* the untouched background color, just enclosed by the outline
  instead of touching the image border. If background is defined as "only
  the region connected to the border", this correctly-colored hole gets
  reclassified as foreground and rendered solid black in mono mode.

The fix implemented in `_detect_bg_mask` (search `vt_crop_tools.py`):
1. Threshold by color distance to get a loose "candidate" background mask.
2. Label connected components (`scipy.ndimage.label`); components that
   touch the image border are real background.
3. For components that DON'T touch the border (enclosed islands): promote
   them to background anyway, but only if their **mean** color distance to
   the sampled background is within a much **stricter** threshold (roughly
   fuzz/4) than the loose candidate threshold. A true untouched-background
   hole matches almost exactly (distance ~2-3); a gradient highlight that
   merely passed the loose threshold does not.

If background detection looks wrong on a new icon, check which of these two
failure modes it is before changing thresholds — they need opposite fixes.

Also apply a 3x3 median filter (`_denoise`) to the foreground pixels before
palette-snapping/quantizing — otherwise JPEG-style compression speckle in a
mockup source survives into the reduced palette as visible pixel noise
instead of a flat fill.

### Real vs. hand-drawn alpha input

`isobus` also has to handle icons that were hand-drawn (SVG → transparent
PNG) rather than cropped from an opaque mockup photo. If the input already
has real alpha variation (some fully transparent, some fully opaque pixels),
that alpha is authoritative and used directly as the background mask —
color-distance detection is skipped entirely. Without this check, PIL's
internal `(0,0,0)` fill for transparent pixels gets treated as "near the
black outline color" and the outline itself gets wiped out. Only fall back
to color-distance detection when the image is already fully opaque (the
normal case for a cropped mockup screenshot).

## Script discipline (established the hard way in this project)

- **Every step always starts from the same named source(s)** (`Original\`)
  — never chain a script's own prior output as its *next run's* implicit
  input across separate script files. Within ONE script run, later steps
  MAY consume an earlier step's freshly-produced output (e.g. `splitx`
  consuming that run's own `crop` result) — that's the intended chaining,
  not a violation of this rule.
- Every calibration (`mark`/`markx`) and its confirmed follow-up
  (`crop`/`splitx`) belong in the **same committed `.bat` file** with the
  same variables, not run ad hoc from a shell — otherwise the two drift out
  of sync (this happened: `mark.bat` and `crop.bat` as separate files ended
  up with different coordinates, producing a bad crop nobody caught until
  visual review).
- Prefer one flexible generic tool (`vt_crop_tools.py`) over one-off
  scripts per image — new mask/button sets should mean new variables in
  `mark_and_crop.bat`, not new Python code, unless a genuinely new
  operation is needed.
- `git commit` the `.bat` alongside every regenerated output file, so the
  exact coordinates that produced a given asset stay reconstructable.
