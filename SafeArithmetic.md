# SAFE Arithmetic Lib — SAFE_ADD/SUB/MUL/DIV (saturating, ANY-generic)

> Status: implemented (typelib + native FORTE backend), not yet built/flashed/hardware-tested.
> This document was originally written as a plan before implementation; it has been rewritten
> to describe what was actually built, since the plan diverged from the final result in several
> places (repo locations, and the shape of SAFE_ADD/SAFE_MUL — see below).

## Context

`Uebung_011b3` (`test_B/Uebungen/Uebung_011b3.SUB`) demonstrates on real ESP32-P4
hardware that `F_SUB` (`iec61131::arithmetic::F_SUB`, generic IEC 61131-3
function) computes `UDINT#1 - UDINT#12 = UDINT#4294967285` — a silent
two's-complement wraparound. This is exactly the IEC 61131-3-specified
behavior for unsigned types, **not a bug**, but it is documented in
`test_B/sys/Training_B/NOTIZ_Hardware_Test_Uebung_011b3.md` as an open,
deliberately deferred item: for real measurement-technology use (setpoint
differences, remaining-distance calculations) a silent wraparound is
dangerous. The note explicitly calls for a **SAFE Arithmetic Lib**
(clamping and/or overflow/underflow detection).

Behavior on overflow/underflow/division-by-zero: **saturating arithmetic** —
the result is clamped into the valid range of the concrete type, and a
`LIMIT_HIT: BOOL` output signals that clamping occurred (division by zero
counts as a clamp: `OUT := 0`, `LIMIT_HIT := TRUE`).

## Repos and locations actually used

Three repos ended up involved, all local clones of the user's GitHub-hosted
training forks (`Meisterschulen-am-Ostbahnhof-Munchen/*`) — **not** the
`C:\git\ms\*` clones (those track different remotes, e.g. `4diac-forte`'s
`C:\git\ms` clone points at an internal Azure DevOps remote, not GitHub):

- **`C:\git\proj3\4diac_training1`**, branch `feature/SafeArithmetic` — the
  4diac IDE workspace. New library bundle
  `Ventilsteuerung\4diacIDE-workspace\.lib\SafeArithmetic-3.0.0\`.
- **`C:\git2\ms\4diac-forte`**, branch `feature/SafeArithmetic` — the FORTE
  C++ runtime. New module `modules\SafeArithmetic\`.
- **`C:\git2\ms\4diac-ide`** — the 4diac IDE source repo itself (typelibrary
  shipped with the IDE). Related but separate upstream contributions (not
  part of the `SafeArithmetic` library): adding the missing generic
  `MUL_2/3/4.fbt` (branch `GEN_MUL`) and fixing generic
  `First/Second function input` comments to proper math terminology across
  `F_ADD/F_SUB/F_MUL/F_DIV`, `ADD_2/3/4` (branch `arithm`). These informed
  the design of `SAFE_ADD`/`SAFE_MUL` below (IEC 61131-3 defines both ADD
  and MUL as *extensible* — see next section) and the `IN1`/`IN2` comment
  wording used throughout `SafeArithmetic`.

`F_SUB`/`F_GE` (the standard library's generic functions) are
**hand-written** C++ (not IDE-codegen'd — no `4DIAC FORTE Export Filter`
marker) using `CIEC_ANY_MAGNITUDE_VARIANT` / `CIEC_ANY_ELEMENTARY_VARIANT` +
`std::visit` runtime type dispatch; there is no `.fbt` XML for `F_SUB`
anywhere in `4diac-forte` — the IDE-facing interface stub lives separately,
bundled inside the IDE's own `iec61131-3-3.0.0` typelib
(`C:\4diac\4diac-ide_...\typelibrary\iec61131-3-3.0.0\typelib\arithmetic\F_SUB.fbt`).
`SafeArithmetic` follows the same split: `.fbt` interface stubs in the IDE
workspace repo, hand-written C++ backend in the forte repo.

## What SAFE_ADD/SAFE_SUB/SAFE_MUL/SAFE_DIV actually are

Correcting the original plan: **not** four uniform fixed-2-input FBs.
IEC 61131-3 defines ADD and MUL as *extensible* arithmetic functions
(`OUT := IN1 op IN2 op ... op INn`), same as the standard library's
`ADD_2/3/4.fbt` (generic, backed by `GEN_ADD`) — but the standard library
is missing an equivalent `MUL_2/3/4` (a gap fixed upstream in `4diac-ide`,
see above). SUB and DIV are **not** extensible this way (not
associative/commutative in a useful sense), so they stay fixed 2-input,
matching `F_SUB`/`F_DIV`.

- **`SAFE_ADD_2/3/4`** and **`SAFE_MUL_2/3/4`** — generic N-ary FBs,
  `Attribute GenericClassName="'GEN_SAFE_ADD'"` / `'GEN_SAFE_MUL'`,
  backed by native `GEN_SAFE_ADD`/`GEN_SAFE_MUL` classes
  (`CGenFunctionBlock<CFunctionBlock>`, mirroring the standard `GEN_ADD`).
  `SAFE_ADD_*` uses `ANY_MAGNITUDE` (like `F_ADD`), `SAFE_MUL_*` uses
  `ANY_NUM` (like `F_MUL`).
- **`SAFE_SUB`** and **`SAFE_DIV`** — fixed 2-input FBs, hand-written
  directly like `F_SUB`/`F_DIV` (no generic-arity mechanism).
  `SAFE_SUB` uses `ANY_MAGNITUDE`, `SAFE_DIV` uses `ANY_NUM`.
- No `TIME`-flavored siblings (`F_ADD_DT_TIME`, `F_MULTIME`, …) — out of
  scope for this first version, per the original request ("ANY erst mal,
  TIME nicht").
- `IN1`/`IN2`(`/IN3`/`IN4`) input comments use proper mathematical
  terminology, not generic "input N": **summand** (`SAFE_ADD_*`),
  **minuend**/**subtrahend** (`SAFE_SUB`), **factor** (`SAFE_MUL_*`),
  **dividend**/**divisor** (`SAFE_DIV`) — matching the fix applied
  upstream to `F_ADD/F_SUB/F_MUL/F_DIV`/`ADD_2/3/4` in `4diac-ide`.

## Part A — IDE typelib stubs (repo: `C:\git\proj3\4diac_training1`)

Bundle `Ventilsteuerung\4diacIDE-workspace\.lib\SafeArithmetic-3.0.0\`,
modeled on `iec61131-3-bool-3.0.0` (smallest existing bundle, same
dependency shape: `.project`/`MANIFEST.MF` require `core` and
`iec61131-3`, both `Version="3.0.0"`).

`typelib\arithmetic\` contains 8 `.fbt` files, all interface-only `FBType`
(no `BasicFB`/`ECC` — matches the hand-written-native pattern),
`CompilerInfo packageName="SafeArithmetic::arithmetic"`,
`Classification="saturating arithmetic function"`, `EventOutputs`/`CNF`
carries both `OUT` and `LIMIT_HIT`:

- `SAFE_ADD_2.fbt`, `SAFE_ADD_3.fbt`, `SAFE_ADD_4.fbt` — generic,
  `ANY_MAGNITUDE`, `GenericClassName="'GEN_SAFE_ADD'"`.
- `SAFE_MUL_2.fbt`, `SAFE_MUL_3.fbt`, `SAFE_MUL_4.fbt` — generic,
  `ANY_NUM`, `GenericClassName="'GEN_SAFE_MUL'"`.
- `SAFE_SUB.fbt` — fixed 2-input, `ANY_MAGNITUDE`.
- `SAFE_DIV.fbt` — fixed 2-input, `ANY_NUM`.

All 8 validated with
`python .agents/skills/iec61499-creator/scripts/validate.py <file>`
against `schemas/fbtype.xsd`.

## Part B — Native FORTE backend (repo: `C:\git2\ms\4diac-forte`)

Module `modules\SafeArithmetic\` — **nested under `modules\`**, mirroring
`modules\IEC61131-3\`'s exact layout and CMake chain (not a top-level
sibling of `logiBUS-modules`/`OSCAT-modules` as the original plan assumed).
`option(FORTE_MODULE_SAFEARITHMETIC ...)`, `add_library(forte-safearithmetic)`,
linked against `forte-core` only (no dependency on `forte-iec61131-3`, since
`func_ADD.h` etc. and `forte_any_magnitude_variant.h`/`forte_any_num_variant.h`
live in `core/include/forte/...`). Registered in `modules\CMakeLists.txt`
(alphabetical, between `rt_events` and `signalprocessing`). No
`setup_esp32p4.sh` in this repo/clone — the root `CMakeLists.txt`'s
`add_subdirectory(modules)` picks the new module up automatically once the
`FORTE_MODULE_SAFEARITHMETIC` option is turned on at configure time.

`include\forte\SafeArithmetic\arithmetic\` / `src\SafeArithmetic\arithmetic\`
(namespace `forte::SafeArithmetic::arithmetic`):

- **`safe_arithmetic_ops.h`** — shared header with:
  - Native (`safe_add_native<V>`/`safe_sub_native<V>`/`safe_mul_native<V>`/`safe_div_native<V>`)
    helpers operating on the plain C++ value type `V`:
    - Integral `V`: `__builtin_{add,sub,mul}_overflow`; on overflow, clamp
      to `std::numeric_limits<V>::max()`/`::min()`, direction from operand
      signs (`if constexpr (std::is_signed_v<V>)`, unsigned always clamps
      in the one direction that's possible for that op — e.g. unsigned
      `SAFE_SUB` underflow always clamps to `0`, exactly the
      `UDINT#1 - UDINT#12` case from `Uebung_011b3`). `SAFE_DIV`: divide
      by zero clamps to `0`; the `INT_MIN / -1` edge case clamps to `max()`.
      Requires GCC/Clang (`#error` on other compilers — not yet ported to
      MSVC intrinsics).
    - Floating (`REAL`/`LREAL`) `V`: plain operation, then
      `limitHit = isfinite(in1) && isfinite(in2) && !isfinite(result)`,
      clamp to `±numeric_limits<V>::max()`. `SAFE_DIV` treats `in2 == 0.0`
      as a clamp too (avoids producing `INF`/`NaN`).
  - CIEC-level wrappers (`safe_add<T,U>`/`safe_sub<T,U>`/`safe_mul<T,U>`/`safe_div<T,U>`)
    that deduce the result type via `mpl::get_{add,sub,mul,div}_operator_result_type_t<T,U>`
    (same traits `func_ADD`/`func_SUB`/`func_MUL`/`func_DIV` use), and for
    `safe_add`/`safe_sub` fall back unchanged to `func_ADD`/`func_SUB` when
    the result type's `TValueType` isn't arithmetic (i.e. a `TIME`/`DATE`
    pair result) — `safe_mul`/`safe_div` `static_assert` instead, since
    `ANY_NUM` never produces those.
- **`SAFE_SUB_fbt.h`/`.cpp`**, **`SAFE_DIV_fbt.h`/`.cpp`** — hand-written
  fixed-2-input FBs, copied from `F_SUB_fbt`/`F_DIV_fbt`'s structure
  (`CIEC_ANY_MAGNITUDE_VARIANT`/`CIEC_ANY_NUM_VARIANT` + `std::visit`
  dispatch), extended with a `CIEC_BOOL var_LIMIT_HIT` data output
  (index 1, alongside `var_OUT` at index 0) and calling `safe_sub`/`safe_div`
  instead of `func_SUB`/`func_DIV`. `DEFINE_FIRMWARE_FB` string
  (`"SafeArithmetic::arithmetic::SAFE_SUB"_STRID` etc.) matches the `.fbt`'s
  `packageName::Name` exactly.
- **`GEN_SAFE_ADD_fbt.h`/`.cpp`**, **`GEN_SAFE_MUL_fbt.h`/`.cpp`** —
  generic N-ary FBs, copied from the standard library's `GEN_ADD_fbt`
  structure (`CGenFunctionBlock<CFunctionBlock>`, `createInterfaceSpec`
  parses the arity from the trailing `_<N>` in the instance type name via
  `strrchr`/`util::strtoul`, `mGenDIs` is a runtime-sized
  `CIEC_ANY_MAGNITUDE_VARIANT[]`/`CIEC_ANY_NUM_VARIANT[]`). `OUT` and
  `LIMIT_HIT` are fixed (non-generic) data outputs (`getGenDOOffset()`
  returns `2`), only the inputs are variable-arity. `executeEvent` folds
  the inputs pairwise via `safe_add`/`safe_mul`, OR-ing `LIMIT_HIT` across
  every step. `DEFINE_GENERIC_FIRMWARE_FB` string matches the `.fbt`'s
  `GenericClassName` attribute.

## Verification

- All 8 `.fbt` files validated against `schemas/fbtype.xsd`
  (`iec61499-creator` skill's `validate.py`) — pass.
- Manual review: each `SAFE_*`/`GEN_SAFE_*` C++ pair structurally matches
  its `F_*`/`GEN_ADD` template; `DEFINE_(GENERIC_)FIRMWARE_FB` strings
  match their `.fbt` counterparts; `LIMIT_HIT` wired consistently across
  all 6 FB implementations.
- **Not done**: compiling `4diac-forte` (POSIX or ESP32-P4), flashing, or
  hardware-testing — left to the user. A natural follow-up once built:
  a `Uebung_011b3`-style exercise swapping `F_SUB` → `SAFE_SUB` to confirm
  `1 - 12` now clamps to `UDINT#0` with `LIMIT_HIT = TRUE` instead of
  wrapping to `4294967285`.

## Commits

- `4diac_training1` (`feature/SafeArithmetic`): typelib bundle + `SAFE_ADD_2/3/4`/`SAFE_MUL_2/3/4`
  as generic FBs, plus the terminology fix, both on top of the initial plan-document commit.
- `4diac-forte` (`feature/SafeArithmetic`, `C:\git2\ms\4diac-forte`):
  `modules/SafeArithmetic/` (`SAFE_SUB`/`SAFE_DIV`/`GEN_SAFE_ADD`/`GEN_SAFE_MUL`).
- `4diac-ide` (branches `GEN_MUL`, `arithm`, `C:\git2\ms\4diac-ide`): related
  upstream fixes (`MUL_2/3/4.fbt`, IN1/IN2 terminology) that this library's
  design follows.
