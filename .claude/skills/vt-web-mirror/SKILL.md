---
name: vt-web-mirror
description: "Use whenever generating or updating a Vue page that visually mirrors an ISOBUS VT DataMask/SoftKeyMask (the `vt-ui-mirror`-style web client next to an ISO-Designer pool). Covers the px()/py() coordinate-mapping convention, the dm-icon/dm-label/dm-value/dm-unit CSS class system and its font-size tiers, sourcing positions from the real `.jvi` (not the mockup image), page-navigation wiring, and the build-and-browser-verify loop. Trigger on any request to build/update a page under a `*-ui-mirror`/`vt-ui-mirror` Vue project, or to mirror a DataMask's content into a web page."
---

# VT web-mirror page generation

Reference knowledge for building/updating one Vue page in a `vt-ui-mirror`-style
project — a pixel-faithful web reconstruction of one ISOBUS VT mask, living
alongside the real ISO-Designer pool (see the separate `iso-designer-jop`
skill for the pool XML itself, and `vt-icon-pipeline` for producing the icon
image assets this skill imports). This skill is only about the Vue page:
what markup/CSS pattern to generate, where to get the numbers from, and how
to verify the result.

## Source of truth for positions: the `.jvi`, never the mockup image

**Do not derive a field's `Left`/`Top`/`Width` by measuring pixels in the
customer's mockup PNG.** The mockup image's aspect ratio rarely matches the
mask's true pool dimensions exactly, per-element positions in the mockup
were laid out by eye (not on a strict grid the image's own pixel scale
reproduces), and a naive `mockup_px / image_total_px * 480` conversion
compounds across multiple reference points into positions that are off by
tens of pixels — confirmed the hard way mid-project chasing a "mittiger
Bargraph" row's position purely from image measurements before switching to
the method below.

The reliable method: **once a field exists in the real pool, read its exact
`Left`/`Top`/`Width`/`Height` straight out of the `.jvi` Component and/or the
`.jop` object**, and use those numbers verbatim in `px()`/`py()` calls — this
guarantees the web mirror and the real pool agree pixel-for-pixel, because
they're reading the same source numbers. When adding a field to the pool and
the web mirror in the same session, write the pool side first (or at least
finalize its exact coordinates on paper) and copy those numbers into the Vue
page, not the other way around.

Use the mockup image only for: what a field visually *is* (icon shape,
whether it's bordered, roughly which row/column it sits in) and — cross-
checked against the customer's actual hand-drawn Strichzeichnung, not just
the polished mockup — *whether an elaborate visual (a bargraph, a colored
fill) is a real requirement at all*, since a professionally-rendered mockup
PNG can contain graphic-designer embellishments the customer never asked
for (confirmed real incident: a "segmented bargraph" look in a polished
mockup for a plain measured-value field that the customer's own sketch drew
as an ordinary bordered box).

## Coordinate system: `px()`/`py()` against `--mask-x-total`/`--mask-y-total`

Every positioned element uses two page-local helpers, defined once per page:

```ts
function px(n: number) {
  return `calc(${n} / var(--mask-x-total) * 100cqw)`
}
function py(n: number) {
  return `calc(${n} / var(--mask-y-total) * 100cqh)`
}
```

`--mask-x-total`/`--mask-y-total` are global CSS custom properties (set once,
e.g. in `App.vue`, at `480`/`480` for a landscape 640x480 mask's DataMask
area — see the shared `VtScreen.vue` component for how the DataMask and
SoftKeyMask areas size themselves off the same two variables and reflow
between landscape/portrait via `@media (orientation: ...)`). Every `px(n)`/
`py(n)` call takes the **raw pool pixel coordinate** — the exact same number
that appears as a `Left`/`Top`/`Width`/`Height` value in the `.jvi`/`.jop` —
so positions transfer 1:1 with zero mental unit conversion. Never hand-roll
a percentage or a different divisor for one field "because it looks right"
— if a field looks wrong, the fix is the pool-sourced number, not a fudge
factor here.

A page's root markup is a `<VtScreen :data-mask-color="..." :soft-key-mask-color="...">`
wrapping a title `<div>` plus one absolutely-positioned element per pool
object, followed by a `<template #softkeys>` block of `VtSoftKeyButton`s (see
Navigation section below) — `VtScreen`/`VtSoftKeyButton` are the project's
shared layout primitives; don't reimplement the DataMask/SoftKeyMask
sizing logic per page.

## The `dm-*` class system and font-size tiers

Four element kinds, each an absolutely-positioned `<div>` (icons are `<img>`)
sized/placed entirely via inline `:style` using `px()`/`py()`, with the CSS
class only supplying font-size/color/border/background:

```html
<img class="dm-icon" :src="iconFoo" :style="{ top: py(55), left: px(10), width: px(55), height: py(40) }" />
<div class="dm-label" :style="{ top: py(140), left: px(60), width: px(20), height: py(30) }">R</div>
<div class="dm-value dm-value--output" :style="{ top: py(58), left: px(75), width: px(80), height: py(35) }">3,0</div>
<div class="dm-unit" :style="{ top: py(58), left: px(160), width: px(55), height: py(35) }">km/h</div>
```

- **`.dm-icon`** — `position: absolute; object-fit: contain`. Width/height
  from `px()`/`py()` match the `CImage`'s pool `Width`/`Height` (or the
  intended display size when reusing an icon at a different size than its
  other placement — see the `iso-designer-jop` skill's DataMask/SoftKeyMask
  ID sub-range note if the *same* underlying bitmap is used in both a
  SoftKeyMask and a DataMask in the real pool: the web mirror has no
  equivalent scaling-context bug, but keep pool-side and mirror-side asset
  choices in sync regardless).
- **`.dm-label`** — flex, `align-items: center`, no border/background; short
  static text (`R`/`L`, a Roman-numeral field tag, a footer caption).
- **`.dm-value`** — flex, bordered (`1px solid #888`), `padding-left: 6`;
  always paired with exactly one of:
  - `.dm-value--output` (background `#d7dcdb`, matches a real `COutputNumber`)
  - `.dm-value--input` (background `#fff`, matches a real `CInputNumber`) —
    **default to input/editable** when the pool's own field type is
    ambiguous or not yet built; this project's convention is that most
    numeric DataMask fields turn out to be editable, not display-only.
- **`.dm-unit`** — flex, no border; sits immediately right of a `.dm-value`.

Three font-size tiers, applied as an additional modifier class on
`.dm-value`/`.dm-unit`/`.dm-label`, mirroring the pool's own `FontAttributes`
tiers — **pick the web tier that matches whatever `CFontStyle` the pool field
actually references**, don't default to full-size everywhere:

| Modifier | Font size | Roughly matches pool font |
|---|---|---|
| *(none)* | `22` (value/unit) / `16` (label) | `FontAttributes_24x32` / `_12x16` |
| `--small` | `16` | `FontAttributes_16x24` |
| `--tiny` | `11`, plus `padding-left: 2` and `justify-content: center` on values | `FontAttributes_8x12` |

All font sizes are themselves `calc(N / var(--mask-x-total) * 100cqw)`, same
pattern as `px()` — never a bare `px`/`rem` value, or the text stops scaling
with the rest of the mask.

**Confirmed real incident — the two previews disagree on text width**: the
real VT bitmap font renders noticeably wider per character than the `system-ui`
web font at the "same" pixel size used here. A layout that looks fine in the
web mirror (built first, reviewed only in-browser) can overflow its box or a
neighboring element on the *real* ISO-Designer render, and vice versa —
treat a browser check and a real-GUI screenshot as two **separate**,
both-required validation passes, not one substituting for the other. When a
value needs 4+ digits or a long unit string, prefer sizing generously (or
stepping down a font tier) rather than assuming the web preview's apparent
fit transfers to hardware.

## Navigation wiring

Each page defines `defineEmits<{ navigate: [target: string] }>()` and a
`softkeys` array of `{ name: string; icon: ImportedAsset }` (empty `name`
for a not-yet-wired designator, which `VtSoftKeyButton` renders as a
disabled/inert key):

```ts
const softkeys = [
  { name: 'DataMask_Hauptmenue', icon: iconBack }, // Home
  { name: '', icon: iconAus },
  // ...
]
```
```html
<VtSoftKeyButton v-for="b in softkeys" :key="b.name" :icon="b.icon" @press="b.name && emit('navigate', b.name)" />
```

The parent (`App.vue`) owns a single `TARGETS: Record<string, Page>` map
translating each emitted `target` string to a page-id, and a `page` ref
switching which page component renders — mirrors the real pool's
`CMacro`-driven "Change Active Mask" navigation (see `iso-designer-jop`
skill) one macro/target at a time. When the pool adds a new cross-mask
softkey (e.g. a softkey that should reuse one mask's Home icon but macro to
a *different* mask than that icon's other placement — a real case: two
different DataMasks share the same visual Back-arrow icon object in the
pool, but one of them needed to macro to a third mask instead of Home),
add the matching new key to `TARGETS` and use a distinct target string
matching the new macro's naming, not the shared icon's name.

## Doc-comment block: write down what a fresh reader can't derive

Every page's `<script setup>` opens with a comment block covering, in order:
1. Which pool object this mirrors (`DataMask_X`, JVS-ID) and where its
   content spec came from (Strichzeichnung page N).
2. Deliberate scope cuts — what was left out and why (a customer ask like
   "just the simple fields first", a not-yet-built pool feature, a status
   indicator that has no real backing logic yet). Update this list the
   moment scope changes; a stale "still excluded" note next to now-present
   markup is worse than no note.
3. One line per field/group explaining what it *measures or controls* in
   domain terms (not what the CSS does) — especially anything non-obvious
   or confirmed via the customer rather than guessed.
4. The SoftKeyMask's full designator list in DOM order, cross-referenced
   against the `.jvi`'s own `Left`/`SoftkeymaskDesignatorNo` layout (2
   columns × 6 rows is the common case — state which column is "inner"
   (`Left=480`) vs "outer" (`Left=560`) once per page, since DOM order and
   physical layout don't otherwise correspond).

## Build-and-verify loop — every change, no exceptions

1. `npx vue-tsc --noEmit` (type-check).
2. `npx vite build` (this project inlines everything into one
   `dist/*.html` via `vite-plugin-singlefile` — check for that plugin's
   inlining log lines to confirm it actually ran, not just "built
   successfully").
3. Serve the built file (`npx vite preview --port <port>`) and drive it with
   the browser-automation tool: navigate to the root, click through from
   the home page to the target mask (menu tiles/softkeys aren't necessarily
   at the coordinates you expect after a build — re-screenshot rather than
   assuming prior coordinates still apply), then **zoom into each changed
   region specifically** rather than trusting a single full-page screenshot
   to reveal a small overflow.
4. `document.title` does **not** update on this app's internal page
   switches (it's a single-page app swapping components, not a real route)
   — confirm the actual page via `document.body.innerText` or a DOM query
   instead of trusting the tab title after a `navigate` click.
5. Only after both this browser check *and* (when the pool side changed
   too) a real ISO-Designer GUI screenshot look acceptable, consider the
   layout done — see the font-width caveat above for why both are needed.
6. Kill the preview server (`pkill`/background-process cleanup) and close
   any browser tabs opened for verification before finishing.

## Icon imports

New page-specific icons import from `../assets/icons/<Name>.png` (produced
by the `vt-icon-pipeline` skill's `web` command — full color, alpha-
transparent, NOT the pink/mono `isobus` BMP variant used in the real pool).
Reusing an icon already used by another page/softkey: import the *same*
already-existing asset file rather than re-cropping a duplicate — check
existing `import icon... from '../assets/icons/...'` lines across the
project first.
