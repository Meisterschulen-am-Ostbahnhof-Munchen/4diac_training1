# Creating a whole new DataMask + SoftKeyMask by hand

This is a different job from editing objects on an existing mask (the rest
of this skill covers that). Here you're adding a brand new page the
operator can navigate to - a new file pair, new navigation, and a handful
of new objects, none of which exist yet anywhere in the pool. Worked
end-to-end on the Krauternter project's "Overrides" page
(2026-09-28, commit `54df5372` - read that commit for a concrete, complete
example of every step below).

## 0. First, know which project files actually matter

A `.jop` project directory has more files in it than just the pool and its
masks, and it's tempting to assume they all need updating together when
you add a new page. They don't. Only two kinds of file are structural:

- **`<Pool>.jop`** - the single source of truth for every object, including
  the new `CDataMask`/`CSoftKeyMask` objects themselves.
- **`<MaskFolder>/<MaskName>.jvi`** - one per mask, referenced *from* the
  `.jop` by the `Path` property on that mask's own object. Nothing else
  points at a `.jvi` file by name or path except that one `Path` property.

Everything else you'll see change in `git status` after a build is a
**pure IDE UI-state cache**, not a registry your new page needs to be
added to:

| File | What it actually is | Do you need to touch it? |
|---|---|---|
| `<Pool>.jod` | "Default objects" - remembers what child objects the GUI paired with each *class* last time you dropped one (e.g. "a CCheckBox comes with this font + this kind of NumberVariable by default"). Keyed by class, not by object name. | No. Leave it. |
| `<Pool>.jops` | Object-pool tree browser's scroll/expand/sort state. | No. Leave it. |
| `<Pool>.jtl` | Tree-view expand/collapse state, by index position, not by object ID or name. | No. Leave it. |
| `<Pool>.jvd` | ISO-device manager profile (screen colors, softkey pixel dimensions, font capabilities). Global to the project, not per-mask. | No. The build tool rewrites this wholesale regardless of what you changed. |
| `<Pool>.jvp` | The actual project manifest - lists every `.jvi` file with a GUID. This one **is** structural... | ...but you still don't hand-edit it. The build (`compile_default_pool.py`, run via the project's `RunSkript_Build<Pool>.bat`) auto-discovers any `.jvi` path it finds referenced from a `CDataMask`/`CSoftKeyMask`'s `Path` property in the `.jop` and appends a fresh-GUID entry for it. Just make sure you run the build after creating the new `.jvi` files, and confirm the entry appeared in the diff. |

Practical upshot: write the `.jop` additions and the new `.jvi` files, then
run the project's build script once. Don't hand-edit `.jod`/`.jops`/`.jtl`/
`.jvd`/`.jvp` at all - the diffs you see in them afterward (sometimes a
*huge* line-count diff purely from reformatting) are the build/IDE doing
its own bookkeeping, not something you produced or need to check by hand.
If a `.jvp` entry for your new mask doesn't show up after the build, that
means the `.jop` `Path` property is wrong or the mask object itself didn't
save correctly - go back and check those, not the `.jvp`.

## 1. Pick where the new page is reached from

Before allocating any IDs, decide the navigation entry point. Two options,
with a real space trap on one of them:

- **A tile `CButton` on an existing hub `DataMask`** (e.g. a "Diagnose"
  overview page with a few big buttons stacked vertically). These tiles
  are typically ~110px tall with a small gap, inside a mask that's often
  only 480px tall with `EnableScrolling="0"` - i.e. **no scrolling**. Do
  the arithmetic before committing to this: if adding a 4th tile pushes
  the bottom past the mask's own `Height`, that tile is invisible and
  unreachable on the real hardware, not just visually clipped in a
  preview. Only do this if there's genuinely room, or if you're prepared
  to also resize/reflow the existing tiles (higher-risk, touches objects
  that already work).
- **A `CSoftKey` in a free slot of an existing mask's `SoftKeyMask`** -
  much lower risk. A `SoftKeyMask` almost always has 12 fixed slots
  (`SoftkeymaskDesignatorNo` 0-11); slot 0 is usually the mask's own
  "Back" key, and it's common for most of the remaining 11 slots to still
  be `CPointer`-to-`ObjectPointer_NULL` (JVS-ID `27140`) placeholders,
  never filled in. Grep the target `SoftKeyMask_*.jvi` for `CPointer`
  Components - each one is a free slot. Turning a placeholder slot into a
  real key is a two-attribute edit (see step 4), not a new Component.

## 2. Allocate IDs

You need, at minimum:

- One `CDataMask` ID (1000-block, see the main skill's ID-block table -
  just take the next free one).
- One `CSoftKeyMask` ID (4000-block) for the new page's own key strip.
- One `CSoftKey` ID (5000-block) for its Back key, plus one more if you're
  also adding the *forward*-navigation key on the source page.
- One `CMacro` ID for the forward navigation (**Macro IDs are their own
  tiny sequential space - 1, 2, 3... - completely unrelated to the
  ObjectID blocks**, don't confuse the two). Check whether a
  `Macro_GoTo_<the mask you're linking FROM>` already exists for the
  *return* trip before making a new one - these are frequently reused,
  since "go back to the Diagnose hub" is the same action regardless of
  which sub-page you came from.
- Two `CProxy` IDs (4194304+ space) for the two keys' icons.
- Whatever content objects the page itself needs (checkbox+NumberVariable,
  labels, etc. - covered by the main skill's ID-block table and CProxy
  section, nothing special here).

Find "next free" for each by scanning the `.jop` for the max existing
JVS-ID of that `Class` - a one-line regex per class, not a manual scroll.

## 3. Write the `.jop` objects

**`CDataMask`** (`PropertySheet Name="Model"`): `MaskType=1`,
`Path=".\<Folder>\<DataMaskName>.jvi"`, plain `Comment="AAA="` (empty).
No `Width`/`Height` here - those live in the `.jvi` itself.

**`CSoftKeyMask`**: same shape, `MaskType=2`,
`Path=".\<Folder>\<SoftKeyMaskName>.jvi"`.

**Forward-nav `CSoftKey`** (wherever you decided to place it in step 1)
and **back-nav `CSoftKey`** (in the new mask's own `SoftKeyMask`): both are
plain `CSoftKey` objects, `Width=80 Height=80`, with an `<Events>` block:

```xml
<Events>
  <Event>
    <Property Name="ID"><Value><![CDATA[25]]></Value></Property>
    <Property Name="Name"><Value><![CDATA[OnKeyRelease]]></Value></Property>
    <Property Name="Param"><Value><![CDATA[]]></Value></Property>
    <Property Name="Macros"><Value><![CDATA[<macro id>]]></Value></Property>
    <Property Name="Conditions"><Value><![CDATA[]]></Value></Property>
    <Property Name="KeyCode"><Value><![CDATA[0]]></Value></Property>
  </Event>
</Events>
<Objects>
  <Object JVS-ID="<new CProxy ID>"/>
</Objects>
```

Note the event is **`OnKeyRelease`** (ID `24`... no - `25`), not
`OnKeyPress` (`24`) - that's the one big tile `CButton`s use instead. Mixing
these up doesn't error, it just means the key never fires.

**`CMacro`** (forward direction only - reuse the existing one for back):

```xml
<Object Class="CMacro" JVS-ID="<id>" ObjectName="Macro_GoTo_<NewPage>" Pinned="FALSE">
  <Commands>
    <Command id="173" subid="-1">
      <Params>
        <Param Name="Workingset" Type="7">0 - WorkingSet_0</Param>
        <Param Name="New active Mask" Type="8"><DataMask ID> - DataMask_<NewPage></Param>
      </Params>
    </Command>
  </Commands>
  <Property Name="Comment"><Value><![CDATA[AAA=]]></Value></Property>
</Object>
```

**Icon `CProxy`s**: don't create new bitmaps for a first pass unless the
user actually asked for custom art - reuse an existing `CImage` that's
already in the SoftKeyMask ID half (20500-20999, see the main skill's
scaling table) and is a reasonable semantic fit (a padlock for an
"override/unlock" concept, for instance). Each `CSoftKey` still needs its
*own* fresh `CProxy` wrapper even when two keys share the same underlying
icon - see the main skill's CProxy section for why (sharing happens at the
CProxy layer, never by two objects pointing at the same CProxy).

## 4. Wire the forward key into its slot

If you're using a free `SoftKeyMask` slot (the low-risk path from step 1),
the existing Component there is a `CPointer` referencing the shared
`ObjectPointer_NULL` (`27140`). Change exactly two things and nothing else
- keep its `Top`/`Left`/`SoftkeymaskDesignatorNo` exactly as found, that's
what puts it in the right physical grid cell:

```diff
- <Component ID="1" Class="CPointer" Name="Pointer">
+ <Component ID="1" Class="CSoftKey" Name="SoftKey">
    ...
    <Objects>
-     <Object JVS-ID="27140"/>
+     <Object JVS-ID="<your new forward CSoftKey's ID>"/>
    </Objects>
  </Component>
```

## 5. Write the two new `.jvi` files

Copy the shape of an existing simple mask pair as your template (in this
project, `TECU_PTO/DataMask_TECU_PTO.jvi` +
`TECU_PTO/SoftKeyMask_TECU_PTO.jvi` are small and clean). Key points that
are easy to get subtly wrong:

- The `.jvi`'s own `<Property Name="ObjectID"><Value>` under `PropertySheet
  Name="General"` must equal the JVS-ID you gave the matching
  `CDataMask`/`CSoftKeyMask` object in the `.jop` - this is what lets the
  IDE connect the two halves.
- `DataMask`: `SoftKeyMask` property points at your new `CSoftKeyMask`'s
  ID (not `-1`). `Width`/`Height` `480`/`480` matches this project's other
  simple pages; `EnableScrolling="0"` too - remember that means anything
  placed outside the visible area is simply gone at runtime, not scrollable.
- `SoftKeyMask`: `Width="640" Height="480"` (the key-strip mask is wider
  than the content mask it belongs to), `SoftKeyMask` property `-1` (a
  SoftKeyMask doesn't have a SoftKeyMask of its own).
- Each `<Component>` in a `.jvi` is a **placement**, not a definition -
  its own `Top`/`Left`/`Transform` plus a single `<Objects><Object
  JVS-ID="..."/></Objects>` pointing at the real object already defined in
  the `.jop`. A `SoftKeyMask`'s 12 slots follow a fixed pixel grid (two
  columns of 6, `Left` 480 or 560, `Top` stepping by 80) - copy the
  existing template's coordinates verbatim per slot rather than
  recomputing them.

## 6. Build, then validate, then check the `.jvp` diff

Run the project's build script. Confirm: 0 warnings/errors, the new
`.jvi` paths show up as new entries in the auto-regenerated `.jvp`
(confirms the `.jop` `Path` properties resolved correctly), and any new
plain-UINT/NumericObjectPool_S constants you need landed in the generated
GCF. Then run this skill's usual validation pass (well-formed, no
duplicate/dangling IDs, every text/number object has its font child) on
the full `.jop` plus both new `.jvi` files before calling it done.
