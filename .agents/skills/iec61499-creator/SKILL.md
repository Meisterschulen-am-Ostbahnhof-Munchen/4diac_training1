---
name: iec61499-creator
description: Use this skill to create, edit, structure, and validate IEC 61499 library elements (Basic FBs, Composite FBs, Service Interface FBs, Adapters, Subapps, Devices, Resources, Systems, DataTypes) against standard schemas.
---

# IEC 61499 Library Element Creator Skill

This skill provides XSD schemas, templates, and validation scripts to create valid IEC 61499 elements.

## Directory Structure

- `schemas/`: XSD schemas defining valid IEC 61499 elements (e.g., `fbtype.xsd`, `adaptertype.xsd`, etc.)
- `templates/`: Boilerplate XML files for various library elements (e.g., `Basic.fbt`, `Composite.fbt`, `Adapter.adp`, `SubApp.sub`, etc.)
- `references/`: Reference documentation for keywords and type compatibility.
- `scripts/validate.py`: Python validation script using `lxml` to validate an XML file against its matching XSD schema.

## How to Use This Skill

### 1. Creating a New Library Element

To create a new element (e.g., a Basic Function Block, Adapter, or Subapp), start by copying the appropriate template from the `templates/` directory:

- **Basic FB**: Use `templates/Basic.fbt` or `templates/TemplateBasic.fbt`
- **Composite FB**: Use `templates/Composite.fbt`
- **Service Interface FB (SIFB)**: Use `templates/ServiceInterface.fbt`
- **Adapter**: Use `templates/Adapter.adp`
- **Subapplication**: Use `templates/SubApp.sub`
- **Data Type**: Use `templates/TemplateStruct.dtp`
- **Attribute Declaration**: Use `templates/AttributeDeclaration.atp`

Copy the template to the desired location and rename it, then update its `Name` attribute on the root tag.

### 2. Validating the XML Element

Always run the validation script to ensure that the XML you created or modified is fully compliant with the XSD schema.

#### Prerequisites

Make sure `lxml` is installed:

```bash
python -m pip install lxml
```

#### Commands

Run the validator by passing the path of the XML file:

```bash
python .agents/skills/iec61499-creator/scripts/validate.py <path_to_xml_file>
```

**Gap: `check_keywords.py` does not check `packageName`.** It only checks `Name`/`Var`-style identifiers, not the `::`-separated segments of a `CompilerInfo packageName` attribute. The real 4diac IDE *does* flag a reserved keyword there ("Package Name: 'X' is a reserved keyword in segment of package name..."), e.g. `Override` (matches `OVERRIDE` in [Keywords.md](references/Keywords.md)). When choosing a new package/folder segment, check it against Keywords.md by hand — a clean `validate.py` run does not guarantee the package name is safe.

### 3. Key XML Schema Guidelines

- **PascalCase Attributes**: All attributes (like `Name`, `Comment`, `Type`, `Var`, `Value`) use PascalCase. Note that `Var` is capitalized (e.g. `<With Var="QI"/>`).
- **Empty Collections**: Elements like `EventInputs`, `EventOutputs`, `InputVars`, and `OutputVars` can be empty (e.g., `<InputVars/>`).
- **Self-Closing Tags**: Empty elements (e.g., `SubAppEvent`, `Identification`, `VersionInfo` with no nested tags) should be written as self-closing tags (e.g. `<Identification />`) to prevent validation failures caused by whitespace character content.

### 4. ST Code, Datatypes & Conversions Guidelines

When writing Structured Text (ST) code in Algorithms or choosing Datatypes/Conversions:

- **Avoid Reserved Keywords**: Do not use reserved IEC 61131-3 / IEC 61499 keywords (e.g., control flow, standard types, time units) as variable, block, or event names. See [Keywords.md](references/Keywords.md) for the complete list.
- **Type Compatibility**: Ensure data connections follow the rule "Target must be able to hold Source" (e.g. `SINT` -> `INT` is allowed, but `INT` -> `UINT` is not). See [Typkompatibilitaet.md](references/Typkompatibilitaet.md) for compatibility matrices.
- **Explicit Casting & Reinterpret Casts**: In ST or networks, use explicit functions (e.g., `[SOURCE]_TO_[TARGET]`). Note that converting bit-strings (like `DWORD`) directly to float/numeric types performs a `reinterpret_cast` of the raw bits. For mathematical float conversion from integer-valued DWORDs, use double casting: `UDINT_TO_REAL(DWORD_TO_UDINT(var))`.
- **Precision Limits**: Use `LREAL` instead of `REAL` for signal values or values exceeding `16,777,216` to prevent precision loss.

### 5. ECC Interlock/Gate Guards

A computed status flag (e.g. an internal "ready"/"enable" BOOL, or an OutputVar like `EINSCHALTBEREIT`) enforces **nothing** by itself — only an actual `Condition` on an `ECTransition` enforces behavior. The flag can be computed correctly and exposed correctly on the interface while the transition that was supposed to check it no longer does.

- **Events cannot be combined with `AND`/`OR` at all — not with each other, and not with Data either.** An Event in IEC 61499 is polar (a momentary trigger), not a persistent level — it only "is" true for the single reaction it fires in, so `EventA AND EventB`, `EventA OR EventB`, and even `EventName AND someBoolVar` are all invalid/meaningless as a `Condition`. The **only** correct way to guard an event with a data condition is the bracket form: `Condition="EventName[boolean_expr]"` (e.g. `Condition="EIN[NOT (STOERUNG_M1 OR STOERUNG_M2)]"`) — this is 4diac's dedicated syntax for "this event, but only act on it while this data condition holds." If a state needs to react to several distinct events, give it one `ECTransition` per event (each with its own `EventName[...]` guard if needed), never one edge trying to join events together.
- **This happens silently.** Renaming states, redrawing edges, or general tidying in the 4diac IDE can drop the `[boolean_expr]` guard from an existing transition `Condition` without any schema/validation error — the file stays perfectly valid XML, the flag is still computed, still wired to an output; only the *enforcement* is gone. XSD validation cannot catch this, since it's a semantic loss, not a structural one.
- **When reviewing or writing an interlock**, don't infer "this is enforced" from the flag's existence or from its Comment/description — grep the actual `Condition` string of the specific `ECTransition` the interlock is supposed to gate, and confirm the `EventName[...]` guard is really there.
- **Don't strip a condition just because it looks tautological.** A sub-condition can be always-true as an *edge gate* (e.g. checking `ZAEHLSTAND = 0` on a transition that's only reachable from a state that already guarantees `ZAEHLSTAND = 0`) while still being the correct formula for a *continuously-read status output* consumed by something outside the FB (a Visu, another FB) at times when the edge isn't even being evaluated. Distinguish "redundant as this edge's guard" from "removable from the formula" — they're not the same question.

### 6. Referencing a FUNCTION's Return Value in a Data Connection

A FUNCTION instance (e.g. `ASSEMBLE_BYTE_FROM_BOOLS`) has no named output variable to address with `.VarName`. Its single return value is referenced by the **instance name followed by a trailing dot with nothing after it**: `Source="MyFunctionInstance."` — this is correct, valid syntax, not a broken/incomplete reference. Don't "fix" it by removing the dot or by guessing/adding a plausible-sounding suffix like `.OUT`. This is easy to get wrong because some standard blocks that *look* like functions (e.g. `F_MUX_32`, `F_MOD`) are actually declared with an explicit `OutputVars` section named `OUT` and genuinely do take `.OUT` — check the block's own `OutputVars`/interface definition rather than assuming either convention.

### 7. `INIT` / `INITO` Wiring: Required in Composite FBs (`.fbt`), Automatic in SubApps (`.SUB`)

- **In Composite FBs (`.fbt`) / Wrappers**:
  Any wrapper or Composite FB must **ALWAYS** expose `INIT` (`Type="EInit"`) and `INITO` (`Type="EInit"`) on its interface list and explicitly wire them inside the `FBNetwork` (`INIT` $\rightarrow$ `internal_FB.INIT`, `internal_FB.INITO` $\rightarrow$ `INITO`). Nothing fires internal `EInit` events in a Composite FB unless explicitly wired from the interface.
  
- **In SubApplications (`.SUB`)**:
  `INIT` is automatically distributed by 4diac IDE to every FB instance in the resource via `E_TRIG` at the `EMB_RES` level once the SubApp is deployed/flattened into an Application/Resource — **for all events declared `Type="EInit"`** (such as `initval_*` blocks).

> [!IMPORTANT]
> **THE RULE "DO NOT CONNECT `INIT` ON `initval`" APPLIES ONLY IN A `.SUB` FILE.**
> In a `.SUB` network, `INIT` on `initval_*` blocks is automatically wired by 4diac IDE upon deployment, so do NOT add explicit event connections to `initval.INIT` or `AR_D_FF_HYS_TMIN.INIT` in a `.SUB`. Conversely, in a Composite FB (`.fbt`), `INIT` and `INITO` **MUST** be exposed on the interface and wired internally.



### 8. Fanning Out One Adapter to Multiple Destinations: Always Use a `*_SPLIT_N`, Never a Bare Multi-Connection

Plain data/event connections can legitimately fan out from one `Source` to several `Destination`s (broadcast semantics apply there). **Adapters do not follow this rule** — do not write several `<Connection Source="SameAdapterName" Destination="..."/>` entries in `AdapterConnections` pointing at different targets. Instead, route the single Socket/Plug through the matching `*_SPLIT_N` block for that adapter type (e.g. `AX_SPLIT_2`..`AX_SPLIT_9` for `AX`, `ATM_SPLIT_2`..`_4` for `ATM`, `AR_SPLIT_2`..for `AR`, etc. — one Socket `IN`, `N` Plugs `OUT1..OUTn`) and connect each `OUTn` individually to its destination. This applies even when fanning out to more than one *inner* FB instance's Socket, not just when delegating outward.

> [!IMPORTANT]
> **CRITICAL CHECKLIST FOR ADAPTER FLIP-FLOPS / FEEDBACK LOOPS:**
> Whenever creating or porting an adapter-native block or subapplication (such as a Toggle Flip-Flop with `AX_E_SWITCH` + `AX_SR`, or any latch / feedback circuit), `AX_SR.Q` is ALWAYS needed in TWO places:
>
> 1. Fed back to `AX_E_SWITCH.G` (gate input to determine the current toggle state).
> 2. Connected to the output (e.g., `DigitalOutput_Q1.OUT` or SubApp interface plug `Q`).
> 
> Because `AX_SR.Q` has TWO destinations, **IT MUST ALWAYS BE ROUTED THROUGH AN `AX_SPLIT_2` FB**:
>
> - `AX_SR.Q` $\rightarrow$ `AX_SPLIT_2.IN`
> - `AX_SPLIT_2.OUT1` $\rightarrow$ `Q` (or `DigitalOutput_QXA.OUT`) — *forward signal (top pin)*
> - `AX_SPLIT_2.OUT2` $\rightarrow$ `AX_E_SWITCH.G` — *feedback signal (bottom pin)*
> 
> **Note on Routing Cleanliness**: Wire `OUT1` forward to the output plug/block and `OUT2` backward to `AX_E_SWITCH.G` so the adapter connection lines do not cross in the 4diac IDE graphical editor!
> 
> **NEVER CONNECT `AX_SR.Q` DIRECTLY TO BOTH `AX_E_SWITCH.G` AND `Q` WITHOUT AN `AX_SPLIT_2`!**


### 9. Never Vendor a Standard-Library Block Into the Project's `.lib` Without Asking First

**Do not copy a standard IEC 61131-3/4diac block from an external source into this project's own `.lib` folder on your own initiative.** Always ask the user first, even if a block looks like an obvious/needed reuse — vendoring is a deliberate per-block decision the user makes, not something to do proactively just because a standard block would fit.

- **`C:\4diac\4diac-ide_...\typelibrary\` is *not* an authoritative source.** It's a local, unversioned nightly-build install on this machine — not a git repo, not necessarily current, not something to treat as "the" upstream. Copying a block from there and calling it vendored is wrong.
- **`C:\git2\ms\4diac-ide` is the actual canonical upstream** — a real git checkout of the eclipse4diac/4diac-ide source. If a standard block genuinely needs vendoring after discussing it with the user, source it from there, not from the nightly install folder.
- This applies to every external/standard block (conversion, comparison, bitwiseOperators, signalprocessing, etc.) — not just ones that happened to come up before. Confirm with the user which exact block, from which exact source, before creating any file under `.lib`.


### 10. Connection Categorization: `<AdapterConnections>` vs `<DataConnections>`

Always strictly place connections in their proper XML tag:

- **`<AdapterConnections>`**: Used ONLY for connections where source and destination are adapter plugs/sockets (e.g. `AX_SR.Q`, `logiBUS_IXA.IN`, `logiBUS_QXA.OUT`, `AX_SPLIT_2.IN`, `AB_TO_AUI.AB_IN`, `AUI_DEMUX_8.K`).
- **`<DataConnections>`**: Used ONLY for primitive data variables (`BOOL`, `BYTE`, `UINT`, `INT`, `DINT`, `REAL`, `LREAL`, `STRING` etc. e.g. `AX_X_TO_BOOL.IN`, `AND_BOOL_2.IN1`, `F_BYTE_TO_UINT.IN`).
- **`<EventConnections>`**: Used ONLY for event triggers (`EI`, `EO`, `REQ`, `CNF`, `IND`, `S`, `R`, `CLK`).

Do NOT place adapter plug/socket connections inside `<DataConnections>`.


### 11. Adapter Block Selection in `test_AX` Exercises

In `test_AX` exercises, always check `.lib/adapter-3.0.0/` and `.lib/MyLib_AX-1.0.0/` for native adapter implementations before placing standard non-adapter FBs:

- **Bistable Elements**: Use `adapter::bistableElements::AX_FB_T_FF`, `AX_FB_RS_T_FF`, `AX_FB_SR_T_FF` (with adapter sockets `CLK`, `SET`/`RESET`, plug `Q1`) instead of standard `FB_T_FF`, `FB_RS_T_FF`, `FB_SR_T_FF`.
- **Event Demultiplexers**: Use `adapter::events::unidirectional::AUI_DEMUX_8` (with `AUI` adapter socket `K`) paired with `adapter::conversion::unidirectional::AB_TO_AUI` instead of standard `E_DEMUX_8` + `F_BYTE_TO_UINT`.
- **SubApplications**: Check if an `_AX` SubApp type exists in `MyLib::sys` (e.g. `T_FF_EVENT_AX`, `T_FF_ILOCK_EVENT_AX`, `AE2_ILOCK_T_FF_TO_AX`) before using non-adapter SubApp types (`T_FF_EVENT`, `T_FF_ILOCK_EVENT`).
- **Analog/Real Random & Hysteresis**: Use `adapter::utils::FB_AR_RANDOM` (wrapping `FB_RANDOM`), `adapter::events::unidirectional::AR_D_FF_HYS_TMIN`, `adapter::types::unidirectional::AR::initval::initval_AR`, and `adapter::iec61131::comparison::AR_GT` for adapter-native analog/real hysteresis flip-flops.



