---
name: 4diac-gcf-editing
description: "Use whenever hand-editing a 4diac `.gcf` (GlobalConstants) file, or a `.SUB`/`.fbt` file's Comment attributes, outside the 4diac IDE. Covers: (1) pool-generated `.gcf` files (e.g. `DefaultPool*.gcf`, written by `GcfScript.py`) must NEVER be hand-edited - fix the `.jop` or the generator script and re-run it instead; (2) a confirmed IDE resave bug where a long Comment attribute gets word-wrapped and the IDE fails to read its own wrap back, discarding/truncating the comment; (3) the `<OriginalSource>` CDATA mirror desyncing when hand-written. Trigger on any `.gcf` file edit, or when adding/editing a `Comment=\"...\"` attribute in a `.SUB`/`.fbt` file that will be opened again in the 4diac IDE."
---

# 4diac `.gcf` / `.SUB` Comment editing — confirmed IDE resave bug

## Pool-derived `.gcf` files: never hand-edit, fix the generator instead

**Confirmed rule (Franz, 2026-09-19): never hand-edit a `.gcf` file that is
generated from the VT pool by `GcfScript.py`** (in this project:
`DefaultPool.gcf`, `DefaultPool_Numeric.gcf`, `DefaultPool_Scroll.gcf`,
`DefaultPool_PositionMarker.gcf`, `DefaultPool_BargraphSplit.gcf` — any
`<Pool>_*.gcf` written by `scripts_central/GcfScript.py`, invoked via
`test/scripts/RunSkript_<Pool>.bat`/`.sh`). *"NIE an den GCF rumdrehen. das
macht das GCF Script. ist die GCF falsch müssen wir das script fixen."*

If a value in one of these files is wrong (e.g. a `NumericObjectPool_S`
constant's `r32Scale`/`i32Offset`/`u8Decimals` doesn't match what the VT
pool object should produce): fix the root cause in the `.jop` (the
widget's own `Scale`/`Offset`/`NoOfDecimals` properties), or fix
`GcfScript.py` if the script itself derives the wrong value from a
correct `.jop` — then **re-run the generator** to produce the corrected
`.gcf`, never hand-patch the `.gcf` text. Confirmed incident: hand-editing
24 `NumericObjectPool_S` entries in `DefaultPool_Numeric.gcf` directly
(correct values, wrong method) got silently overwritten by the next
regeneration/IDE resave before it could even be committed — the hand-edit
was pure wasted effort on top of being the wrong approach.

**Do a real ISO-Designer/4diac IDE build BEFORE re-running the generator
script yourself.** Confirmed second correction (Franz, same session, right
after the first): calling `GcfScript.py` directly with whatever `.iop.h`
happens to already sit in `Output/` is not the sanctioned workflow either —
that `--oldfile` input is itself a build artifact and can be stale relative
to the `.jop` edit that motivated the regeneration. *"GCF korrekt per
Script neu erzeugt. das ist Unsinn. ich muss ERST einen BUILD machen."*
Claude cannot trigger a real ISO-Designer build (GUI-only) — so after
fixing a `.jop` property, tell the user what changed and that a rebuild is
needed, rather than unilaterally invoking `GcfScript.py` against a
possibly-stale `.iop.h`. If the fix only touches property values on
objects whose IDs/names are unchanged (not adding/renaming/removing
objects), the regenerated `Scale`/`Offset`/`Decimals` numbers likely come
out correct anyway (they're read straight from the `.jop`, not from the
`.iop.h`) — but that's a lucky case, not a reason to skip asking.

**This rule is specific to pool-generated files.** Hand-authored `.gcf`
files that are NOT generated from a VT pool — `NVS_Keys.gcf`,
`SubStrings_STG*.gcf`, `RemoteSubStrings*.gcf` and similar per-station
OPC-UA/INI constant files in this project — are normal source files, edited
directly as part of regular FB development. The distinguishing question:
*is there a `RunSkript_*.bat`/`GcfScript.py` invocation that regenerates
this exact file from a `.jop`/`.iop.h`?* If yes, never hand-edit it. If no,
it's a normal hand-authored constants file and the rest of this skill
(Comment-length/wrap bug, `<OriginalSource>` comment rules) still applies
to it as usual.

Confirmed real incident, not theoretical: while hand-editing several `.gcf`
`GlobalConstants` files across a multi-station OPC-UA refactor
(`SubStrings_STG1.gcf` and siblings, Krauternter project), the 4diac IDE
discarded/truncated `Comment="..."` attribute text on the next resave.

**Root cause, confirmed by Franz — comment length/line-wrap, NOT a
character-escaping issue.** A first hypothesis (a raw `=` inside the
comment text, e.g. `ACTION=CREATE_METHOD`) turned out to be a red herring —
Franz corrected it explicitly: *"die Länge gibt einen Zeilenumbruch, und den
kann er nicht richtig zurücklesen. 4diac IDE Bug."* (the length triggers a
line-wrap, and the IDE can't read that wrap back correctly). The affected
comments in the incident happened to contain `=` only by coincidence — they
were also long enough to get wrapped, which is what actually broke them.
**Do not reach for `&#61;`-style character escaping as a fix for this — it
does not address the real cause.**

An eclipse-4diac issue report is planned but explicitly deferred by Franz
("das ist ein IDE Fehler. müssen wir ein issue aufnehmen, aber nicht
jetzt.") — don't file it unprompted, only when explicitly asked.

## The actual bug: long comments get wrapped, and the wrap doesn't round-trip

The IDE word-wraps a `Comment="..."` value once it's long enough — visible
in the `<OriginalSource>` CDATA mirror as multiple `//`-prefixed
continuation lines, right-aligned under the value:

```
BUNKERBODEN_MAX_WEB_READ : WSTRING := "opc_ua[READ;/Objects/STG1/Bunkerboden/Max,1:s=STG1.BUNKERBODEN_MAX_WEB]"; // Lokaler Web-Override (vt-ui-mirror, laeuft auf STG1) fuer Bunkerkette Max, ODER-verknuepft mit
                                                                                                                 // dem echten SoftKey/AUX
```

On a later resave, the IDE fails to correctly reconstruct the wrapped
comment back into one value — this is what discards/truncates it. No exact
character threshold is known; don't assume a specific number.

**Rule: keep `Comment="..."` attribute values short enough to avoid
triggering the IDE's own wrap.** There's no confirmed safe length — when in
doubt, write a noticeably shorter comment than the verbose, multi-clause
style used elsewhere in this codebase's Comments, and put the detailed
reasoning somewhere that isn't subject to this bug (see below).

**Put the detailed "why" in a `.md` doc file in the repo, not in the
Comment attribute.** This was the original, correct instinct from the
first time this bug was seen (2026-09-07) — a fact that got lost chasing
the `=`-escaping red herring. Example precedent:
`Ventilsteuerung/OPC_UA_VERNETZUNG.md` for the cross-station wiring
conventions. A `.md` file in the repo survives any IDE resave unconditionally.

## The `<OriginalSource>` CDATA mirror — a second, separate trap

Every `.gcf` `GlobalConstants` file carries the same information twice:
the real `<GlobalConstants><VarDeclaration .../></GlobalConstants>` XML
block (what 4diac actually parses), and an `<OriginalSource><![CDATA[ ...
]]></OriginalSource>` plaintext ST-like mirror for the IDE's own source
view. **The IDE regenerates this CDATA block itself on save** — nothing at
runtime reads it.

**Correction (confirmed 2026-10-18, `test_AX/Meins/OPC_UA_Lokal/const/OpcUaLokal.gcf`):
the IDE rebuilds the XML `Comment=` attributes FROM the `<OriginalSource>`
text on resave (e.g. after moving the file).** A constant mirrored as a bare
line without `// ...` loses its `Comment=` on the next resave — this
happened to all 10 constants of a freshly hand-written GCF. Franz then
showed by example which comment forms the IDE keeps:

| Where in `<OriginalSource>` | Becomes |
|---|---|
| `// text` at the end of a constant's line | that constant's XML `Comment="text"` |
| `(* ... *)` block above a constant | kept in `<OriginalSource>` only — room for longer explanations |
| `(* ... *)` / `// ...` before `PACKAGE`, before `GLOBALCONSTANTS`, at the end | kept in `<OriginalSource>` only (file header) |

Rules that follow from this:

- **New constants:** write the short comment twice — as `Comment="..."` in
  the XML and as a trailing `// ...` on the constant's mirror line (same
  text). Keep it short because of the wrap bug above.
- **Longer explanations** (one per group of constants, a file header) go
  into `(* ... *)` blocks in the mirror — they survive resaves and don't
  touch any `Comment=` attribute. A repo `.md` doc is still the place for
  anything longer than a few lines.
- **Existing lines that the IDE already wrapped** (multi-line `//`
  continuation, right-aligned): leave them exactly as found — the
  wrap-and-align format can't be reproduced reliably by hand. When only
  the value of such a constant changes, replace just the `:= value;` part
  of its first line and keep the comment lines untouched.

## Don't assume you've found the whole story

A future truncation report could still have a cause other than the
confirmed length/wrap bug above. Don't try to silently "fix" truncated
comments in a file the user is actively resaving in the IDE — flag it,
don't revert it.

## Practical checklist when editing a `.gcf`

1. Edit the real `<VarDeclaration>` XML entries first (rename, add, adjust
   `Comment=`/`InitialValue=`) — this is the part that matters functionally.
   Keep the `Comment=` value short; put anything longer in a repo `.md` doc.
2. Mirror the same rename/add into `<OriginalSource>` with the same short
   comment as a trailing `// ...` (otherwise the IDE drops `Comment=` on the
   next resave). Longer explanations as a `(* ... *)` block above the line.
3. Leave every other `<OriginalSource>` line, including its wrapped
   comments, exactly as found.
4. Validate well-formedness (`xml.etree.ElementTree.parse`) — this catches
   XML structure errors but **not** the resave-truncation bug, which only
   manifests inside the real 4diac IDE. Don't treat a clean `ET.parse` as
   proof the file will survive a resave unchanged.
5. Only file the upstream eclipse-4diac issue when explicitly asked — it's
   deliberately deferred, not a standing invitation to do it proactively.
