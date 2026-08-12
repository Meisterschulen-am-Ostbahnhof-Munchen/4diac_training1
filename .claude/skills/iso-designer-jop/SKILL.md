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
```

Both `dups` and `dangling` must be empty. Also re-grep the whole file (not
just the touched object's neighbourhood) for any remaining occurrence of an
old numeric ID or old auto-generated name string — see the sync-discipline
section above for why a narrow search misses things.

## Workflow notes

- These files are typically large (10k–20k+ lines after edits) — extract
  exact object blocks with a script (regex on indentation-matched
  `<Object ...>`/`</Object>` pairs) rather than reading the whole file, and
  spot-check one full generated block by eye before trusting the rest.
- Confirm the file is git-clean before running a generation/rewrite script,
  so a script bug is trivially recoverable.
- Don't `git commit` until the user explicitly asks — they want to load the
  result in the real ISO-Designer GUI first as the actual test oracle; a
  clean XML/reference validation pass is necessary but not sufficient proof
  the pool is correct.
