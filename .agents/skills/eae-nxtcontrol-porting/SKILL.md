---
name: eae-nxtcontrol-porting
description: Use when porting a function block, adapter, or subapplication from EAE/nxtControl format (Schneider Electric EcoStruxure Automation Expert / nxtControl, recognizable by DOCTYPE FBType SYSTEM "../LibraryElement.dtd" - e.g. from the UniversalAutomation.org / Valeriy Vyatkin IEC 61499 curriculum exercises, or any other EAE .sln export) into 4diac's fordiac XSD format. Do NOT use for authoring new 4diac elements from scratch - see the iec61499-creator skill for that; this skill is only for translating an existing EAE-format file.
---

# EAE/nxtControl → 4diac Porting Skill

EAE (EcoStruxure Automation Expert) and 4diac use different, incompatible
XML dialects to represent the same IEC 61499 concepts. This skill covers
translating an EAE-format `.fbt` into a valid, working 4diac `.fbt` — always
validate the result with `iec61499-creator`'s
`scripts/validate.py`, this skill only covers the parts validate.py can't
catch (semantic/convention issues, not XSD schema issues).

**Identify the source format first:** an EAE file starts with
`<!DOCTYPE FBType SYSTEM "../LibraryElement.dtd">` right after the XML
declaration. A native 4diac file has no DOCTYPE line at all. If you don't
see that DOCTYPE, this skill doesn't apply — the file is already 4diac
format.

## 1. Mechanical format translation

| EAE | 4diac |
|---|---|
| `<ST Text="line1;&#xD;&#xA;line2;"/>` (attribute, CRLF-escaped) | `<ST><![CDATA[line1;\nline2;]]></ST>` (element, real newlines) |
| `<Event Name="X">` (Type often omitted) | `<Event Name="X" Type="Event">` (Type is **required**) |
| `GUID="..."` on the `FBType` root | drop — 4diac doesn't use it |
| `<Attribute Name="Configuration.FB.IDCounter" .../>` | drop — EAE-only editor bookkeeping |
| `<Attribute Name="FBType.Basic.Algorithm.Order" .../>` | drop — 4diac infers algorithm order from the ECC itself |
| `<Attribute Name="Runtime.Persistence.Storage" .../>` (seen on Service Interface FBs) | drop |
| `ArraySize="3" InitialValue="[3(FALSE)]"` | **unchanged** — this syntax is identical in both formats, confirmed working as-is |

Also add a proper 4diac `Identification`/`VersionInfo`/`CompilerInfo`
header (see `iec61499-creator`'s templates) — EAE's own `Identification`
line (just `Standard="61499-2"`) and `VersionInfo` are much sparser.
**Keep the original author's `VersionInfo` entry unchanged** (their
Organization, Version, Author, Date) for provenance — don't merge it away
or edit its content. Add your own **new** `VersionInfo` entry above/below
it for the port itself (this repo's org, `Version="1.0"`, today's date,
remarks describing what changed in the port). Add another new entry (not
an edit to an existing one) for every later fix round, e.g.
`Version="1.1"`, `"1.2"` — this keeps a readable changelog directly in the
file instead of only in git history.

## 2. `INIT`/`INITO` must be `Type="EInit"` — always

This is a hard convention, **not enforced by the XSD** (`Type` is a free
`xs:string`, so `Type="Event"` validates fine) — but it is enforced by the
4diac IDE / real-world expectations, confirmed the hard way across three
separate ported files and three rounds of PR review in this repo.

Apply it even when the event doesn't follow the usual `QI`/`QO`-qualifier
convention and instead carries arbitrary business data (common in EAE
files, which often bundle a whole parameter set onto `INIT` via multiple
`<With Var="..."/>` entries) — the `Type="EInit"` fix is independent of
what data the event carries; don't restructure the interface to force a
`QI`/`QO`-only shape unless you have another reason to.

```xml
<!-- EAE original -->
<Event Name="INIT" Comment="Initialization Request">
  <With Var="pv1"/>
  ...
</Event>
<!-- 4diac port -->
<Event Name="INIT" Type="EInit" Comment="Initialization Request">
  <With Var="pv1"/>
  ...
</Event>
```

If the original names an event/state literally `RESET` for **both** the
event and its handling state (EAE allows this), consider renaming the
state (e.g. `RESET_ST`) as a precaution — not confirmed to actually be a
problem in 4diac, but cheap to avoid.

## 3. EAE's `Condition="X OR Y"` doesn't exist in 4diac

EAE lets you write a plain boolean expression with an event antecedent
directly in a transition condition, e.g. `Condition="REQ OR pending_reqs"`
(fire on the `REQ` event, **or** whenever `pending_reqs` is already true
regardless of which event arrived). 4diac's ECC condition grammar has no
`OR` between an event name and a bare guard like this.

Fix: split into **two parallel transitions to the same destination
state** — since both go to the same place, evaluation order between them
doesn't matter:

```xml
<!-- EAE original: one transition -->
<ECTransition Source="WAITING" Destination="READ_REQS" Condition="REQ OR pending_reqs"/>

<!-- 4diac port: two transitions, same destination -->
<ECTransition Source="WAITING" Destination="READ_REQS" Condition="REQ"/>
<ECTransition Source="WAITING" Destination="READ_REQS" Condition="[pending_reqs]"/>
```

Bracket-guard syntax reference (confirmed real, established 4diac
syntax, precedent: `quarter-3.0.0/typelib/utils/quarter/QUARTER_TO_STR_STATUS.fbt`):
- `EventName[BoolExpr]` — fires only on that specific event, gated by the
  boolean expression (e.g. `REQ[IB = quarter::STATUS_ENABLED]`).
- `[BoolExpr]` (no event name) — evaluated on **any** incoming event, no
  specific trigger required.

## 4. Check the standard library before porting a "helper" block

EAE composites often instantiate small generic-sounding blocks
(`E_CYCLE`, `E_MERGE`, `E_R_TRIG`, ...) that may already exist as a real
4diac standard library block under a different (or the same) name — don't
blindly port a duplicate. Search the local 4diac install's
`typelibrary/` folder first (e.g.
`C:\4diac\<version>\4diac-ide\typelibrary\events-3.0.0\typelib\`), and
reference the real standard type (e.g. `iec61499::events::E_CYCLE`)
instead of authoring a copy. See the `check-standard-lib-before-creating`
memory lesson for the general version of this rule (the `E_PERMIT`
incident) — it applies just as much to EAE ports as to slide-based
patterns.

## 5. "Ground-truth port" philosophy: preserve behavior, fix format

The whole point of porting real EAE reference material (rather than
writing your own FB) is that it's an authentic, external ground truth —
so **preserve the original's actual behavior by default**, including its
quirks and even its bugs. Only fix things that are purely artifacts of
the format translation (missing `Type=`, the `OR`-condition syntax, CDATA
escaping) — not the underlying logic.

When a reviewer (human or bot) flags something that looks like a genuine
behavior bug in the *original* design, judge case by case — this came up
three times in one PR with three different right answers:

- **Comment/code contradiction inherited from the original** (a variable's
  comment claimed `ABS(pv)` accumulation, the code never applied `ABS()`)
  → fix the **comment** to describe what the code actually does, not the
  code to match a possibly-stale comment. The code is the ground truth;
  the comment was wrong in the original too.
- **A real, low-risk, clearly beneficial fix** (an `INIT` event declared
  request data as `With Var`s but the algorithm never read them, so a
  request already active at deployment was silently dropped until a later
  event) → apply it. Small, safe, obviously correct, worth deviating from
  the original for.
- **A structural ECC design flaw** (declaration-order transition priority
  makes two states permanently unreachable under normal operation) → do
  **not** restructure the ECC to fix it. This is a real architectural
  change (new states, reordered/rewritten conditions), which is a much
  bigger deviation from the ground truth than the port is meant to make,
  and if it has no observable effect on how the block is actually used
  in this repo, it's not worth the risk. Document it as a known
  limitation instead (in the relevant `ECState`/`VarDeclaration` comments
  and the `Documentation` attribute), so a future reuse of the block in a
  context where it *does* matter has a paper trail.

Rule of thumb: small, mechanical, obviously-correct fixes — apply them.
Anything that requires redesigning control flow or changing the shape of
the interface — document, don't silently rewrite, unless you have a
specific reason this block needs to actually work differently than the
original (and if so, say so explicitly in a new `VersionInfo` entry, not
buried in a comment).

## 6. Native Service Interface FBs (SIFBs) can't be ported

An EAE composite sometimes wires in a `Comment="Service Interface
Function Block Type"` instance (e.g. an HMI display panel) with no
`BasicFB`/ECC/`Algorithm` content of its own — it's backed by native
runtime code, not portable ST. You can't translate what isn't there.

Instead: read what it's wired to, and figure out whether it plays a
**structural** role beyond its display/native function (e.g. relaying an
`INITO` event onward to kick off a timer elsewhere in the network). If
so, replace the SIFB instance with a **direct connection** carrying that
same structural role, and drop the display-only pins (labels, status
strings) it also exposed. Document the substitution and what was dropped
in the port's `VersionInfo`/`Documentation`.
