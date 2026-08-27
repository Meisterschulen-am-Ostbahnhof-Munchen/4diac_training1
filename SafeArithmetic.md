# SAFE Arithmetic Lib — SAFE_ADD/SUB/MUL/DIV (saturating, ANY-generic)

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

This plan starts that library: `SAFE_ADD`, `SAFE_SUB`, `SAFE_MUL`,
`SAFE_DIV` — generic (`ANY_MAGNITUDE`-typed, like the standard `F_ADD` /
`F_SUB` / `F_MUL` / `F_DIV`), **not** per-type variants, and **not**
including the `TIME`-flavored siblings (`F_ADD_DT_TIME`, `F_MULTIME`, …)
for now. Behavior on overflow/underflow: **saturating arithmetic** — the
result is clamped into the valid range of the concrete type, and a new
`LIMIT_HIT: BOOL` output signals that clamping occurred (division by zero
counts as a clamp: `OUT := 0`, `LIMIT_HIT := TRUE`).

Two repositories are involved, mirroring how the *existing* generic
functions (`F_SUB`, `F_GE`) are built:

- **`C:\git\ms\4diac_training1`** (this repo) — the 4diac IDE workspace.
  The IDE only ever sees a `.fbt` XML **interface stub** for a generic
  function; there is no `.fbt` XML for `F_SUB` anywhere in this repo or in
  `4diac-forte` — it ships inside the 4diac IDE's own bundled
  `iec61131-3-3.0.0` typelib
  (`C:\4diac\4diac-ide_...\4diac-ide\typelibrary\iec61131-3-3.0.0\typelib\arithmetic\F_SUB.fbt`).
  Our new library is project-specific, so its `.fbt` stubs belong in this
  repo's `Ventilsteuerung\4diacIDE-workspace\.lib\` (same place as
  `adapter-3.0.0`, `iec61131-3-bool-3.0.0`, etc.), as a new bundle
  `SafeArithmetic-3.0.0`.
- **`C:\git\ms\4diac-forte`** (separate git repo, own Azure DevOps
  remote) — the FORTE C++ runtime that actually gets cross-compiled and
  flashed to the ESP32-P4 (`setup_esp32p4.sh`). `F_SUB`/`F_GE` are
  **hand-written** C++ (not IDE-codegen'd — no `4DIAC FORTE Export
  Filter` marker) using `CIEC_ANY_MAGNITUDE_VARIANT` /
  `CIEC_ANY_ELEMENTARY_VARIANT` + `std::visit` runtime type dispatch. Our
  `SAFE_*` FBs must follow the same hand-written pattern, extended with
  overflow-checked arithmetic (`__builtin_add_overflow` /
  `__builtin_sub_overflow` / `__builtin_mul_overflow` for integer types;
  finite-check + clamp for `REAL`/`LREAL`), based on the candidates the
  user pointed at (GCC/Clang overflow builtins, intel/safe-arithmetic,
  boost::safe_numerics — the builtins are the simplest fit since they're
  natively available in the ESP-IDF GCC toolchain and need no extra
  dependency).

**Scope of this session:** implement the `.fbt` interface stubs, the
native C++ implementation, and the CMake/build registration in both
repos. **No compiling, cross-building, or flashing** — that is left to
the user to run afterward (confirmed explicitly: "Code + Registrierung,
kein Build/Flash").

## Part A — IDE typelib stub (repo: `4diac_training1`)

New bundle `Ventilsteuerung\4diacIDE-workspace\.lib\SafeArithmetic-3.0.0\`,
modeled directly on `iec61131-3-bool-3.0.0` (smallest existing bundle,
same dependency shape):

- `.project` — copy `iec61131-3-bool-3.0.0/.project`, rename
  `<name>SafeArithmetic-3.0.0</name>`; keep the `Standard Libraries/core`
  and `Standard Libraries/iec61131-3` linked-resource entries (we depend
  on `ANY_MAGNITUDE` from `iec61131-3`).
- `MANIFEST.MF` — copy `iec61131-3-bool-3.0.0/MANIFEST.MF`, set
  `Product Name="SafeArithmetic" SymbolicName="SafeArithmetic" Comment="Saturating/checked arithmetic for measurement-technology use"`,
  keep `Required SymbolicName="core"` and `Required SymbolicName="iec61131-3"`
  (both `Version="3.0.0"`), `VersionInfo Author="Franz Höpfinger"`.
- `.settings/org.eclipse.core.resources.prefs` — copy verbatim from
  `iec61131-3-bool-3.0.0`.
- `typelib\arithmetic\SAFE_ADD.fbt`, `SAFE_SUB.fbt`, `SAFE_MUL.fbt`,
  `SAFE_DIV.fbt` — each modeled on
  `C:\4diac\4diac-ide_...\typelibrary\iec61131-3-3.0.0\typelib\arithmetic\F_ADD.fbt`
  (etc.), i.e. an **interface-only** `FBType` (no `BasicFB`/`ECC` —
  matches the hand-written-native pattern), `CompilerInfo
  packageName="SafeArithmetic::arithmetic"`, `Classification="saturating arithmetic function"`.
  Interface, using `SAFE_SUB` as the concrete example:
  - `EventInputs`: `REQ` (`Event`, `With IN1`, `With IN2`)
  - `EventOutputs`: `CNF` (`Event`, `With OUT`, `With LIMIT_HIT`)
  - `InputVars`: `IN1: ANY_MAGNITUDE`, `IN2: ANY_MAGNITUDE`
  - `OutputVars`: `OUT: ANY_MAGNITUDE`, `LIMIT_HIT: BOOL` (comment:
    "TRUE if the result was clamped due to overflow/underflow/division-by-zero")

Run `python .agents/skills/iec61499-creator/scripts/validate.py <file>`
on each new `.fbt` against `schemas/fbtype.xsd` before considering Part A
done (per the `iec61499-creator` skill).

## Part B — Native FORTE backend (repo: `4diac-forte`)

New top-level module `SafeArithmetic-modules\SafeArithmetic-arithmetic\`,
structured exactly like `logiBUS-modules\logiBUS-utils\` (Franz
Höpfinger's own prior module in this fork) — **not** nested under
`modules\IEC61131-3\`, since `func_SUB.h`, `func_ADD.h`, `func_MUL.h`,
`func_DIV.h` and `forte_any_magnitude_variant.h` all live in
`core\include\forte\...`, so a new module only needs `forte-core`, no
dependency on `forte-iec61131-3`.

- `SafeArithmetic-modules\SafeArithmetic-arithmetic\CMakeLists.txt` —
  copy `logiBUS-modules/logiBUS-utils/CMakeLists.txt`, adapt:
  `option(FORTE_MODULE_SAFEARITHMETIC "SAFE Arithmetic FBs (saturating, overflow-checked)" OFF)`,
  `add_library(forte-safearithmetic-arithmetic)`,
  `target_link_libraries(forte-safearithmetic-arithmetic PUBLIC forte-core)`,
  whole-archive-link into `forte` (same `$<IF:$<BOOL:${BUILD_SHARED_LIBS}>,...>` pattern),
  `add_subdirectory(include)` / `add_subdirectory(src)`, `install(...)`.
- Root `CMakeLists.txt` (repo root, near the existing
  `add_subdirectory(logiBUS-modules)` / `add_subdirectory(OSCAT-modules)`
  lines) — add `add_subdirectory(SafeArithmetic-modules)`, and
  `SafeArithmetic-modules\CMakeLists.txt` — add
  `add_subdirectory(SafeArithmetic-arithmetic)` (mirrors `modules/CMakeLists.txt`).
- `setup_esp32p4.sh` — add `-DFORTE_MODULE_SAFEARITHMETIC=ON` alongside
  the existing `-DFORTE_MODULE_IEC61131=ON` etc. flags.
- `include\forte\SafeArithmetic\arithmetic\safe_arithmetic_ops.h` — new
  shared header with template helpers `safe_add<T,U>`, `safe_sub<T,U>`,
  `safe_mul<T,U>`, `safe_div<T,U>`, each `(T in1, U in2, bool &limitHit) -> ResultType`:
  - Integral `ResultType`: use `__builtin_add_overflow` /
    `__builtin_sub_overflow` / `__builtin_mul_overflow` on the deduced
    result type; on overflow, set `limitHit = true` and clamp to
    `std::numeric_limits<ResultType>::max()` or `::min()` — direction
    determined from operand signs (e.g. for `SAFE_ADD`: clamp high when
    `in2 >= 0`, clamp low otherwise; for `SAFE_SUB`: clamp low when
    `in2 >= 0` — exactly the `1 - 12` case from `Uebung_011b3`, which
    should now clamp to `UDINT#0` instead of wrapping — clamp high
    otherwise; for `SAFE_MUL`: clamp high when operand signs match, low
    otherwise).
  - Integral `SAFE_DIV`: `in2 == 0` → `limitHit = true`, return `0`;
    else plain division (integer division cannot overflow except the
    `INT_MIN / -1` edge case, which also sets `limitHit`).
  - Floating (`REAL`/`LREAL`) `ResultType`: perform the plain operation,
    then `limitHit = std::isfinite(in1) && std::isfinite(in2) &&
    !std::isfinite(result)`; on hit, clamp to `±std::numeric_limits<ResultType>::max()`
    (sign from the unclamped result). `SAFE_DIV` additionally treats
    `in2 == 0.0` as a clamp (`limitHit = true`, `OUT := 0`) rather than
    producing `INF`/`NaN`.
- `include\forte\SafeArithmetic\arithmetic\SAFE_ADD_fbt.h` (+ `SAFE_SUB`,
  `SAFE_MUL`, `SAFE_DIV`) and matching `src\SafeArithmetic\arithmetic\SAFE_ADD_fbt.cpp`
  (+ 3 more) — copy `F_SUB_fbt.h`/`.cpp` (arithmetic) as the direct
  template (and `F_ADD_fbt.cpp`/`F_MUL_fbt.cpp`/`F_DIV_fbt.cpp` for the
  respective `mpl::get_add_operator_result_type` /
  `get_mul_operator_result_type` / `get_div_operator_result_type` trait
  names — confirm each exists in `core/include/forte/...` before using
  it), with these changes:
  - Namespace `forte::SafeArithmetic::arithmetic`, class
    `FORTE_SAFE_ADD` (etc.), `DECLARE_FIRMWARE_FB(FORTE_SAFE_ADD)` /
    `DEFINE_FIRMWARE_FB(FORTE_SAFE_ADD, "SafeArithmetic::arithmetic::SAFE_ADD"_STRID)`
    — the string **must** exactly match the `.fbt`'s
    `packageName::Name` from Part A for FORTE to resolve the type at
    deployment.
  - Add `CIEC_BOOL var_LIMIT_HIT` data output alongside `var_OUT`, wired
    through `cFBInterfaceSpec.mDONames = {"OUT"_STRID, "LIMIT_HIT"_STRID}`,
    `getDO`/`writeOutputData`/`getDOConUnchecked` extended for index 1,
    plus a second `COutDataConnection<CIEC_BOOL> conn_LIMIT_HIT`.
  - In `executeEvent`'s `std::visit` lambda, replace the direct
    `func_SUB(paIN1, paIN2)` call with
    `safe_sub(paIN1, paIN2, limitHit)` (etc.), assign the result into
    `var_OUT` and `limitHit` into `var_LIMIT_HIT` before
    `sendOutputEvent`.
- Each new leaf `CMakeLists.txt` under `include\SafeArithmetic\arithmetic\`
  and `src\SafeArithmetic\arithmetic\` — copy the
  `modules/IEC61131-3/src/iec61131/arithmetic/CMakeLists.txt` pattern
  (explicit `target_sources(... PRIVATE SAFE_ADD_fbt.cpp ...)` /
  `FILE_SET HEADERS FILES SAFE_ADD_fbt.h ...)`, one entry per new file.

## Verification (this session)

- Run `python .agents/skills/iec61499-creator/scripts/validate.py` on
  each new `.fbt` in Part A.
- Manual review: confirm each `SAFE_*_fbt.h`/`.cpp` pair structurally
  matches its `F_*_fbt` template (same boilerplate methods present, same
  `DEFINE_FIRMWARE_FB` string matches the `.fbt` exactly, `LIMIT_HIT`
  wired consistently across all 4 FBs).
- **Not done this session** (explicitly deferred to the user): compiling
  `4diac-forte` (POSIX or ESP32-P4), flashing, or hardware-testing. A
  natural next step once the user builds it themselves would be a
  `Uebung_011b3`-style exercise swapping `F_SUB` → `SAFE_SUB` to
  re-confirm `1 - 12` now clamps to `UDINT#0` with `LIMIT_HIT = TRUE`
  instead of wrapping to `4294967285` — left for a follow-up session.
