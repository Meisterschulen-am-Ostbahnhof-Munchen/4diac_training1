---
name: iso-designer-jop
description: "Use whenever editing ISOBUS VT pool source files from Jetter/ISO-Designer by hand — `.jop` object pool files and their per-mask `.jvi` companions. Covers the CProxy indirection mechanism, the ISO-11783-6 ObjectID block convention, text-property encoding, and the cross-reference sync discipline needed to rename/renumber/duplicate objects without corrupting the pool. Trigger on any `.jop`/`.jvi` file, any ISO-Designer/JetViewERS/Workspace_* project, or a request to renumber, clean up, duplicate, or generate VT pool objects."
---

# ISO-Designer `.jop` / `.jvi` editing

Reference knowledge for hand-editing ISOBUS Virtual Terminal object pool project
files produced by Jetter ISO-Designer, without going through the GUI. These
rules apply across all of the user's ISO-Designer projects — not just the one
you found this in.

## File roles

- **`<Workspace>/<Pool>/<Pool>.jop`** — the actual editable VT pool source.
  One big XML file (`<JetView-ObjectPool>` root, a flat `<Objects>` list of
  every object, no nesting by class). This is what you edit.
- **`<Workspace>/<Pool>/<MaskName>.jvi`** — one file per mask
  (`DataMask_invisible.jvi`, `MainMask.jvi`, `MainSoftKeyMask.jvi`,
  `WorkingSet_0.jvi`, ...). Each is a small `<JetView-Document>` that places a
  handful of top-level objects (via `<Component Class="..." Name="...">` +
  its own `Proxy` PropertySheet) onto that mask. **If you rename or renumber
  an object that a `.jvi` file references, that file's `JVS-ID=` and
  `Name="Type_ID"` attributes must be updated too**, or the pool loads but
  the mask is broken. Not every object appears in a `.jvi` — containers that
  only exist as children of other containers (e.g. a nested scroll-content
  container) usually don't, only the ones placed directly on a mask do. Grep
  all `.jvi` files for the old ID/name before assuming no sync is needed.
- The compiled binary `.iop` and any generated `.iop.h` / `.gcf` are
  downstream artifacts — don't hand-edit those; regenerate via ISO-Designer
  or the project's own build script instead.

## The CProxy indirection mechanism

An object is **never** nested directly inside its parent's `<Objects>` list.
Instead each parent→child edge is a separate `CProxy` "positioning wrapper"
object:

```xml
<Object Class="CProxy" Name="Rectangle" ObjectName="" Pinned="FALSE" JVS-ID="4194369">
  <PropertySheet Name="Proxy">
    <Property Name="Top"><Value>0</Value></Property>
    <Property Name="Left"><Value>0</Value></Property>
    <Property Name="Name"><Value>Rectangle</Value></Property>
    <Property Name="TabIndex"><Value>-1</Value></Property>
    <Property Name="Transform"><Value>(1.0)(0.0)(Left)(0.0)(1.0)(Top)</Value></Property>
  </PropertySheet>
  <Objects>
    <Object JVS-ID="14013"/>   <!-- the real target object -->
  </Objects>
</Object>
```

The parent container's own `<Objects>` list then references the **Proxy's**
JVS-ID, not the real object's ID.

This is how ISO-Designer achieves object **sharing/reuse**: the same real
object (typically a `Rectangle`, background graphic, or icon) can be
referenced from many different parents by giving each parent its own fresh
CProxy pointing at the same real target. `ObjectPointer` objects use the same
trick to reference their swappable display target.

Consequences for editing:

- To **duplicate a visual element** (e.g. a background rectangle that should
  look the same in every row of a repeated layout), do **not** duplicate the
  real object — create a new CProxy wrapper pointing at the existing real
  object's JVS-ID. Only actually-unique content (text fields, per-row
  numeric values, per-row status pointers) needs a real new object.
- To **duplicate unique content** (e.g. a text/number field that must hold
  independent values per row), duplicate the real object *and* give it its
  own fresh CProxy wrapper — CProxy wrappers are never shared between two
  different parent slots, even when their target is shared.
- `CProxy` JVS-IDs live in their own ID space starting at **4194304**
  (`Proxy_%ld` — this is ISO-Designer's official internal bookkeeping range,
  confirmed distinct from the 16-bit real `ObjectID` space). Never renumber
  existing CProxy IDs into the type-block ranges below; when generating new
  ones by hand, just take the next free numbers above the current max.
- Every CProxy's own `Name` attribute and nested
  `<Property Name="Name"><Value>` are cosmetic/non-unique — ISO-Designer
  tolerates generic or even stale values here (real files in the wild have
  proxies still named after an object's old auto-generated name). Prefer
  setting them to the target's current `ObjectName` for readability, but
  don't treat mismatches you find as bugs.
- Determine "real object" vs "reference" while parsing: a **definition** is
  `<Object Class="..." ... JVS-ID="N">...</Object>` (open tag, has children);
  a **reference** is the self-closing `<Object JVS-ID="N"/>`.

## ObjectID block convention ("Good Practice")

`ObjectID` is a 16-bit value, 0–65535, with **65535 reserved as NULL** — the
highest valid real ID is 65534. ISO-Designer will happily auto-assign IDs
into the danger zone just under 65535 (e.g. 62000–65200) when objects are
added/cloned repeatedly through the GUI; this is a real, recurring cleanup
task, not a hypothetical.

The convention (matches ISO-11783-6 Annex B numbering, confirmed against
`ISOBUS-Objekt-IDs.md`) is to renumber real objects into per-class blocks of
1000, so `DataMask_1005` etc. From a project's Class×ID scan, use whatever
the object count actually requires — no block will realistically overflow
1000 objects of one type on a VT pool.

| TypeName | Block start | Class attr (ISO-Designer `.jop`) |
|---|---|---|
| WorkingSet | 0 | — |
| DataMask | 1000 | |
| AlarmMask | 2000 | |
| Container | 3000 | `CGroup` |
| SoftKeyMask | 4000 | |
| SoftKey / Key | 5000 | |
| Button | 6000 | `CButton` |
| InputBoolean | 7000 | |
| InputString | 8000 | |
| InputNumber | 9000 | |
| InputList | 10000 | |
| OutputString | 11000 | `COutputText` |
| OutputNumber | 12000 | `COutputNumber` |
| Line | 13000 | |
| Rectangle | 14000 | `CRectangle` |
| Ellipse | 15000 | |
| Polygon | 16000 | |
| Meter | 17000 | |
| LinearBargraph | 18000 | |
| ArchedBargraph | 19000 | |
| PictureGraphic | 20000 | `CImage` |
| NumberVariable | 21000 | |
| StringVariable | 22000 | `CStringVariable` |
| FontAttributes | 23000 | `CFontStyle` |
| LineAttributes | 24000 | `CLineStyle` |
| FillAttributes | 25000 | `CFillStyle` |
| InputAttributes | 26000 | |
| ObjectPointer | 27000 | `CPointer` |
| Macro | 0 (own space) | |
| AuxFunction2 | 31000 | |
| AuxInput2 | 32000 | |
| AuxObjectPointer | 33000 | |
| WindowMask | 34000 | |
| KeyGroup | 35000 | |
| GraphicsContext | 36000 | |
| OutputList | 37000 | |
| ExtendedInputAttributes | 38000 | |
| ColorMap | 39000 | |
| ObjectLabelReferenceList | 40000 | |
| ExternalObjectDefinition | 41000 | |
| ExternalReferenceName | 42000 | |
| ExternalObjectPointer | 43000 | |
| Animation | 44000 | |
| ColorPalette | 45000 | |
| GraphicData | 46000 | |
| WorkingSetSpecialControls | 47000 | |
| ScaledGraphic | 48000 | |
| IDsForTemporaryUse | 64000 | temporary only — never leave permanent objects here |
| **Proxy** | **4194304** | `CProxy` — not a 16-bit ObjectID, don't touch/renumber |

Full annex/wiki links live in the user's `ISOBUS-Objekt-IDs.md` (duplicated
across several of their repos, e.g. `ISOBUS-VT-Objects-docs/docs/de/`) if
deeper per-object-type ISO-11783-6 detail is needed.

## DataMask vs SoftKeyMask ID sub-ranges — scaling is tied to the ID, not the mask

**Critical, easy to get wrong**: several object-type blocks above are not one
flat range — they split into a lower **DataMask** half and an upper
**SoftKeyMask/Aux** half, and the VT runtime picks which *scaling* rules to
apply **based on which half the object's own ID falls into**, regardless of
which mask a `.jvi` actually places it on. Canonical source: the user's
`visual-programming-languages-docs` repo,
`docs/de/runtime/isobus/Scaling.md` (check
`C:\git\ms-docs\visual-programming-languages-docs\` first; clone/locate
similarly to the other ms-docs repos if not found there).

| Type | DataMask range (scaled) | SoftKeyMask/Aux range |
|---|---|---|
| Container (`CGroup`) | 3000–3499 | 3500–3999 |
| SoftKey / Key | — | 5000–5999 (centered, no scaling) |
| OutputString (`COutputText`) | 11000–11499 | 11500–11999 |
| OutputNumber (`COutputNumber`) | 12000–12499 | 12500–12999 |
| Line | 13000–13499 | 13500–13999 |
| Rectangle (`CRectangle`) | 14000–14499 | 14500–14999 |
| Ellipse | 15000–15499 | 15500–15999 |
| Polygon (`CPolygon`) | 16000–16499 | 16500–16999 |
| **PictureGraphic (`CImage`)** | **20000–20499** | **20500–20999 ("Working Set Bitmap")** |
| FontAttributes (`CFontStyle`) | 23000–23499 | 23500–23999 |
| LineAttributes (`CLineStyle`) | 24000–24499 | 24500–24900 |
| FillAttributes (`CFillStyle`) | 25000–25499 | 25500–25999 |

`WorkingSet` (ID 0) and Auxiliary Function/Input objects (29000s–32999) are
always centered/unscaled regardless of range.

**Practical consequence — confirmed real-world bug, not theoretical**: if the
same picture needs to appear both on a SoftKeyMask (e.g. as a softkey's icon)
*and* on a DataMask (e.g. as a status/value icon elsewhere), you need **two
separate `CImage` objects** — one numbered in each half — even though both
reference the identical bitmap file via the same `Path` property. Placing a
single `CImage` object via `.jvi` Components on both a SoftKeyMask *and* a
DataMask (the normal object-sharing pattern used everywhere else in this
skill, e.g. for a shared `CNumberVariable` or a shared background
`CRectangle`) does **not** work correctly here: the object's ID alone decides
its scaling treatment, so a `CImage` sitting in 20500–20999 (softkey/aux
range) gets softkey-style scaling even when a DataMask places it — a
mismatch invisible in the ISO-Designer PC preview (which doesn't reproduce
real-VT-hardware scaling) but real on the actual terminal. **When picking a
new ID for a DataMask-only `CImage`, don't just take "next free ID above the
class-wide max"** — check it lands in 20000–20499 specifically; a project's
existing SoftKeyMask icons routinely already occupy most of 20500–20999,
which makes a naive "max+1" scan silently continue numbering new DataMask
icons into the wrong half.

The same two-objects-per-context rule applies to any of the other split
types above if the identical content must appear in both mask kinds (e.g. a
`CRectangle`/Bargraph or `COutputText` reused across a DataMask and a
SoftKeyMask) — though in practice `CImage` icons are what most commonly get
reused this way across a project.

## Softkey/Key-driven page navigation via Macros

VT object pools can switch the active `DataMask` purely from within the pool
itself — a `CSoftKey`/`CKey` press triggers a `CMacro` containing a "Change
Active Mask" command — with **no FB/SubApp/ECU involvement needed** for the
page switch itself (contrast with an FB-driven approach like
`Q_ActiveMask`/`F_SEL_E_4`, which needs the ECU to see the button press event
and issue the mask change). Two pieces wire together:

1. **The macro itself** — a top-level `CMacro` object:

```xml
<Object Class="CMacro" JVS-ID="2" ObjectName="Macro_M1" Pinned="FALSE">
  <Commands>
    <Command id="173" subid="-1">
      <Params>
        <Param Name="Workingset" Type="7">0 - WorkingSet</Param>
        <Param Name="New active Mask" Type="8">1000 - DataMask_M1</Param>
      </Params>
    </Command>
  </Commands>
  <Property Name="Comment"><Value><![CDATA[AAA=]]></Value></Property>
</Object>
```

   `Command id="173"` is ISO-Designer's "Change Active Mask" VT command; the
   `New active Mask` param names the target `CDataMask`'s JVS-ID/ObjectName.
   Macro JVS-IDs are small sequential integers (1, 2, 3, ...) — their own
   namespace, unrelated to the 1000+/6000+/etc. ObjectID blocks above (see
   the block-convention table's `Macro | 0 (own space)` row).

2. **The event that fires it** — an `<Events>` block on the `CSoftKey`/`CKey`
   object, sibling to its `<PropertySheet>` and `<Objects>` (goes between
   them):

```xml
<Events>
  <Event>
    <Property Name="ID"><Value><![CDATA[24]]></Value></Property>
    <Property Name="Name"><Value><![CDATA[OnKeyPress]]></Value></Property>
    <Property Name="Param"><Value><![CDATA[]]></Value></Property>
    <Property Name="Macros"><Value><![CDATA[2]]></Value></Property>
    <Property Name="Conditions"><Value><![CDATA[]]></Value></Property>
    <Property Name="KeyCode"><Value><![CDATA[0]]></Value></Property>
  </Event>
</Events>
```

   `ID=24`/`Name=OnKeyPress` is the "on key press" VT event; `Macros` holds
   the triggered macro's JVS-ID (a plain integer, comma-separated if more
   than one macro should fire). `Param`/`Conditions`/`KeyCode` are typically
   left empty/`0` for a simple unconditional press-to-navigate key.

To wire up N softkeys each switching to a different mask: one `CMacro` per
target mask, one `<Events>` block per softkey referencing its own macro's
ID. Validate exactly as any other change (well-formed, no duplicate JVS-IDs,
no dangling refs) — nothing about this mechanism is exempt.

## Renumbering / renaming an object: everything that must stay in sync

Renumbering is deceptively easy to get half-right. An object's identity is
scattered across **five** places — miss one and the pool loads with a subtly
broken reference (caught in practice by the user reloading in the real
ISO-Designer GUI and finding stale/garbled content):

1. The object's own `JVS-ID="OLD"` on its definition tag → `NEW`.
2. `ObjectName="Type_OLD"` on that same tag → `Type_NEW`.
3. A separate `Name="Type_OLD"` attribute that can appear on the **same**
   tag, independent of `ObjectName` (easy to miss if you assume they're the
   same attribute).
4. A **nested** `<Property Name="Name"><Value>Type_OLD</Value></Property>`
   inside the object's own PropertySheet.
5. Every `CProxy` that wraps this object as its target carries its **own**
   copies of #3 and #4 (`Name="Type_OLD"` + nested `<Value>Type_OLD</Value>`)
   — and a heavily-shared object (e.g. a common background PictureGraphic)
   can have a dozen or more such shadow copies scattered through the file.
6. Every `.jvi` file that places this object on a mask (see File roles
   above).

Practical approach: build the full old→new ID map first, then do the
`JVS-ID=`/`ObjectName=` substitution pass, then a **second, exhaustive**
regex pass for every remaining `Name="Type_OLD"` and `<Value>Type_OLD</Value>`
occurrence (a plain string search across the whole file for each old name,
not just near the object's own block), then grep all `.jvi` files for the
same old identifiers. Finish with the validation pass below — don't consider
a renumbering done without it.

## Text property encoding

`Text`/`Value` properties on text-bearing objects (`COutputText`,
`COutputNumber`, `CStringVariable`, ...) store their display string as
**base64-encoded UTF-16LE, null-terminated**, inside a `<![CDATA[...]]>`:

```python
import base64
def enc(s: str) -> str:
    return base64.b64encode((s + '\0').encode('utf-16le')).decode()
def dec(b64: str) -> str:
    return base64.b64decode(b64).decode('utf-16le').rstrip('\0')
```

`enc('Label_01')` → `TABhAGIAZQBsAF8AMAAxAAAA`. Verify the round-trip against
a known value from the file before trusting generated output — a silent
off-by-one in the encoding (e.g. forgetting the null terminator) produces a
value that decodes to garbage in the real terminal but still "looks like"
valid base64.

An empty/placeholder CDATA is usually `AAA=` (just the null terminator).

**For `COutputNumber`/`CInputNumber` specifically, this `Text`/`Value` string
is a design-time preview only — not the value the real terminal displays.**
As soon as the object has a bound `CNumberVariable` (a child `<Objects>`
reference alongside the font), the object's own `Value`/`Text` is ignored
entirely at runtime — the variable's `Value` is what actually shows/drives
the field (confirmed by the user, who knows ISO-Designer's real behavior
here). Confirmed real symptom of this: after a plain ISO-Designer GUI
resave with no user edits, several `COutputNumber` `Text` CDATA values
changed (e.g. `"40"` → `"4"`) while their bound `CNumberVariable.Value`
stayed untouched — ISO-Designer silently normalizes/truncates this unused
preview string on its own. Don't chase keeping this string in sync with the
variable's value, and don't read a resave diff here as a real content
change — check the bound variable's own `Value` instead when a value
actually matters. (An object with no bound variable — rare, but the
generation examples elsewhere in this skill always add one — presumably
does use its own `Value` at runtime; the ignore-rule is specifically about
what happens once a variable is attached.)

## Every text-bearing object needs a FontAttributes reference

`COutputText`, `COutputNumber`, `CInputNumber`, and `CStringVariable` objects
each need a **direct, non-CProxy reference** to a `CFontStyle` (FontAttributes)
object in their own `<Objects>` list — the same "non-positioned reference"
mechanism as a bound `CNumberVariable` (see the CProxy section above: Font
references don't need a Proxy wrapper, since they're not visually positioned
children):

```xml
<Object Class="COutputText" Name="Text" ObjectName="Label_Q01" Pinned="FALSE" JVS-ID="11011">
  <PropertySheet Name="Text">
    ...
  </PropertySheet>
  <Objects>
    <Object JVS-ID="23000"/>   <!-- FontAttributes_6x8 -->
  </Objects>
</Object>
```

**Confirmed root cause of a real "build fails / ISO-Designer crashes on load"
incident**: a batch of generated `COutputText` labels was missing this
`<Objects>` block entirely (going straight from `</PropertySheet>` to
`</Object>`). The pool stayed well-formed XML, had no duplicate IDs and no
dangling references — every structural check in the Validation section below
passed clean — yet ISO-Designer's build still failed and the IDE itself
crashed on load, with no error message that named the actual cause. It took
the user manually inspecting objects one by one in the GUI to spot that only
one label (copied from an earlier working project) had a font reference and
all newly-generated ones didn't. **This class of bug is invisible to
duplicate/dangling-reference checks** — you must separately verify every
text-bearing object has a font child, ideally by generating that reference
from the same template you copy the rest of the object from rather than
building each field's `<Objects>` list ad hoc. Two classes correctly have **no** font reference, for two different reasons
— don't "fix" either:

- `CNumberVariable` — a value store, not a rendered object at all (see the
  CProxy section's `parents_of` sharing note).
- `CRectangle` used as a Bargraph (`PropertySheet Name="Bargraph"`, see the
  ObjectID block convention section) — a rendered, positioned object, but a
  graphical one with no text to draw, so it needs a CProxy like any other
  positioned child, just not a font.

The font requirement is specifically about *drawing text*, not about being
"a real object" or "a positioned object" — check each class against that,
not against these two examples by analogy.

## Spec-backed validity rules (canonical reference: ms-docs/ISOBUS-VT-Objects-docs)

The user's `ISOBUS-VT-Objects-docs` repo — locally at
`C:\git\ms-docs\ISOBUS-VT-Objects-docs` (path varies by machine; check
`~/ISOBUS-VT-Objects-docs`, `C:\git\*\ISOBUS-VT-Objects-docs`, or clone from
https://github.com/Meisterschulen-am-Ostbahnhof-Munchen/ISOBUS-VT-Objects-docs
if not found locally — `docs/de/isobus-objects/ID-<n>---<Name>...md` per
object type, plus `docs/de/Leere_Objekte.md`, `docs/de/Ungueltige_Pools.md`,
`docs/de/Objekthierarchie.md`) — is the canonical source for ISO 11783-6
pool-validity rules and full per-object attribute tables. Check it before
guessing at spec behavior this skill doesn't cover; these rules apply to any
VT pool regardless of authoring tool, ISO-Designer included. Rules confirmed
there that matter for hand-editing `.jop`/`.jvi`:

- **Font Attributes is a hard record field, not a convention.** Table B.22
  (Output String, ID 11, `ID-11---Output-string---ISO-11783-6---B.9.2.md`)
  lists `Font attributes` as attribute [4] — a fixed 2-byte Object-ID field
  in the wire record format itself, same as `Width` or `Height`. This is
  *why* the missing-font bug above breaks the build: not a best-practice,
  a required field for every Output String/Number and Input Number/String
  object (`COutputText`/`COutputNumber`/`CInputNumber`/`CStringVariable`).
- **These 5 object types must have ≥1 child, never 0** (`Leere_Objekte.md`):
  Working Set (ID 0), Auxiliary Function Type 1 (29), Auxiliary Input Type 1
  (30), Auxiliary Function Type 2 (31), Auxiliary Input Type 2 (32) — each
  needs a visible designator/icon child, or the whole pool is invalid.
- **A Soft Key Mask (ID 4) may only directly contain Key (ID 5) or Object
  Pointer (ID 27) objects** (`Ungueltige_Pools.md` §4) — a `CButton` inside a
  `CSoftKeyMask` is invalid, even though nothing about it looks structurally
  wrong (well-formed, no dangling refs, no duplicate IDs). Use `CSoftKey`
  objects for softkey mask children, never `CButton`.
- **Exactly one Working Set (ID 0)** may exist per pool — not zero, not two.
- **`65535`/`0xFFFF` is a valid, intentional NULL reference** (e.g. an empty
  softkey slot) — don't flag it as a dangling reference in a validation
  script.
- **Reference type-correctness matters, not just existence** (`Ungueltige_Pools.md`
  §2): e.g. an Input Number's variable reference pointing at a
  `CStringVariable` instead of a `CNumberVariable` is invalid even though the
  ID exists in the pool — the class of the referenced object must match what
  the field expects.
- **`Objekthierarchie.md` (Table A.2) is the authoritative parent→child
  legality matrix**, per minimum VT version — check it when unsure whether a
  class is even allowed to nest under another at all, rather than assuming
  from what other pools in the repo happen to do.

## Button content sizing (fill a CButton's border inset exactly)

A `CButton`'s caption/icon content (the child object placed via the button's
own CProxy — see the CProxy section above) should be sized to exactly fill
the button's interior, inset by its border on all four sides:

- **Content object's `Width`/`Height`** = button's own `Width`/`Height` minus
  `2 × border thickness` (border thickness confirmed as 4px in this project's
  buttons, so `Width-8`/`Height-8`).
- **Content CProxy's `Top`/`Left`** = the border thickness on each side (`4`/`4`
  for a 4px border) — **not** `0`/`0`. The CProxy's coordinate origin is the
  button's *outer* edge (including the border), so "the content starts right
  at the inner edge of the border" (what you'd think of as content-space
  `(0,0)`) is `Top=4, Left=4` in that raw coordinate space, not `Top=0, Left=0`.
  Confirmed empirically (`Button_PWM_Q01_ZERO`, `MyLib`/`PWM12` project,
  74×45 button → content `66×37` at proxy `Top=4, Left=4`).

This scales to any border thickness: content size = button size minus twice
the border, content origin = the border thickness itself (not zero) in each
axis.

## Duplicating a repeated structure (e.g. table rows, list items)

When asked to clone a repeated container structure N times (a common ask —
scroll lists, row templates):

1. Identify which children are **shared graphics** (Rectangles/backgrounds —
   new CProxy only, same real target) vs **unique content** (text/number
   fields, ObjectPointers — new real object *and* new CProxy).
2. Extract the full XML block of one existing instance as the template,
   including every child's exact `Top`/`Left`/`Transform` from its CProxy —
   these relative offsets are normally identical across instances; only the
   top-level container's own position changes (e.g. `Top = rowHeight *
   index`).
3. Watch for less-obvious per-instance objects that aren't visually obvious
   from a naming instruction alone — e.g. a nested sub-container that itself
   holds unique fields, or a `CStringVariable` bound to one of the fields.
   Check the existing instances' `<Objects>` lists child-by-child rather
   than assuming the request's wording lists every object type involved.
4. Pick fresh sequential IDs per class starting just above the current file
   max (scan for it programmatically, don't reuse the numbers noted in any
   prior session/memory — the file changes over time, including via the
   real ISO-Designer GUI's own orphan-object garbage collection on save).
5. Write a single generation script rather than many small edits — at this
   object density (10–15 XML objects per duplicated instance) manual editing
   is where mistakes creep in.

## Validation, every time, before calling it done

```python
import re, xml.etree.ElementTree as ET
ET.parse(path)  # well-formed

content = open(path, encoding='utf-8').read()
defs = re.findall(r'<Object Class="[^"]*"[^>]*JVS-ID="(\d+)"[^>]*>', content)
refs = set(re.findall(r'<Object JVS-ID="(\d+)"/>', content))
# duplicate definitions:
from collections import Counter
dups = {k: v for k, v in Counter(defs).items() if v > 1}
# dangling references (child points at an ID with no definition):
dangling = refs - set(defs)

# every COutputText/COutputNumber/CInputNumber/CStringVariable needs a font child
tree = ET.parse(path)
missing_font = []
def walk(elem):
    for child in elem:
        if child.tag == 'Object' and child.attrib.get('Class') in (
            'COutputText', 'COutputNumber', 'CInputNumber', 'CStringVariable'):
            objs = child.find('Objects')
            child_ids = [c.attrib.get('JVS-ID') for c in objs.findall('Object')] if objs is not None else []
            if not any(cid in FONT_IDS for cid in child_ids):  # FONT_IDS = the project's known CFontStyle JVS-IDs
                missing_font.append(child.attrib.get('JVS-ID'))
        walk(child)
walk(tree.getroot())
```

Both `dups` and `dangling` must be empty, and `missing_font` must be empty —
this last check is the one that catches the font-reference bug above; the
other two checks pass clean even when it's present, so don't skip it.

Also re-grep the whole file (not just the touched object's neighbourhood) for
any remaining occurrence of an old numeric ID or old auto-generated name
string — see the sync-discipline section above for why a narrow search
misses things.

**Regex gotcha when writing your own tag scanner** (e.g. to remove an object
subtree by hand instead of via ElementTree): `<Object` is a **prefix** of
`<Objects>`, the container tag. A naive pattern like `<Object[^>]*>` matches
`<Objects>` too, silently pushing a phantom entry onto a depth-tracking stack
that never gets popped (since `</Objects>` doesn't match a `</Object>` close
pattern) — every subsequent balance check then fails or, worse, silently
mis-scopes a removal span. Always anchor with a word boundary: `<Object\b`
(not `<Object`) for opens, and match `</Object>` literally (already safe,
since `</Objects>` has an extra character before its `>`) for closes.

## Workflow notes

- These files are typically large (10k–20k+ lines after edits) — extract
  exact object blocks with a script (regex on indentation-matched
  `<Object ...>`/`</Object>` pairs) rather than reading the whole file, and
  spot-check one full generated block by eye before trusting the rest.
- Confirm the file is git-clean before running a generation/rewrite script,
  so a script bug is trivially recoverable.
- **Commit right after a clean validation pass, BEFORE the user opens the
  result in the real ISO-Designer GUI** — not after. ISO-Designer itself
  can corrupt files on load/save; a pre-GUI commit is the safety checkpoint
  to roll back to if that happens, so it needs to exist before that risk is
  taken, not after it's confirmed safe. A clean XML/reference validation
  pass is necessary but not sufficient proof the pool is correct — the GUI
  is still the actual test oracle — but that's a reason to commit *sooner*
  here, not later.
