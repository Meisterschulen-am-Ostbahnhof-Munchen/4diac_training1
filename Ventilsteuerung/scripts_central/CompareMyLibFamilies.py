"""Compare the Background-block "families" that survive in test_AX vs test_B
after CleanupMyLibTypeLibrary.py, and flag capabilities that exist on one side
but have no counterpart at all on the other side.

Context: each family like "GreenBlueBackground1" has variants distinguished by
a suffix - "" (plain), "S", "SC", "C", and an "_aux" (Auxiliary-input-driven)
variant - and, historically, an "_AX" marker for the AX-adapter-based network
implementation of the same capability (e.g. "_AX", "_AXS", "_AXSC",
"_aux_AX", "_aux_AXS", "_aux_AXSC"). CleanupMyLibTypeLibrary.py kept only
"AX"-named variants in test_AX and only non-"AX"-named variants in test_B
(unless actually referenced elsewhere), so a capability such as "_aux" that
only ever existed in "_AX" form now shows up in test_AX but is completely
absent from test_B - not because it was wrongly deleted (it wasn't used
anywhere), but because a non-AX-named counterpart was never authored to begin
with. This script surfaces exactly those gaps for a human decision.
"""

import os
import re
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENTILSTEUERUNG_DIR = os.path.dirname(SCRIPT_DIR)
WORKSPACE_DIR = os.path.join(VENTILSTEUERUNG_DIR, "4diacIDE-workspace")

PROJECTS = ["test_AX", "test_B"]

FAMILY_PATTERN = re.compile(r"^((?:Green|Red)(?:Blue|Red|White|Green)Background\d+)(.*)$")


def stripped_capability(suffix):
    """Remove the 'AX' adapter-flavor marker to get a side-independent capability tag."""
    return suffix.replace("AX", "")


def classify(stripped):
    has_aux = "aux" in stripped
    if stripped.endswith("SC"):
        shape = "SC"
    elif stripped.endswith("S"):
        shape = "S"
    elif stripped.endswith("C"):
        shape = "C"
    else:
        shape = "plain"
    return has_aux, shape


def collect(project):
    mylib_sys = os.path.join(WORKSPACE_DIR, project, "Type Library", "MyLib", "sys")
    families = defaultdict(list)
    for filename in os.listdir(mylib_sys):
        if os.path.splitext(filename)[1].lower() != ".sub":
            continue
        bare = os.path.splitext(filename)[0]
        m = FAMILY_PATTERN.match(bare)
        if not m:
            continue
        family, suffix = m.group(1), m.group(2)
        families[family].append((bare, suffix))
    return families


def main():
    per_project = {p: collect(p) for p in PROJECTS}
    all_families = sorted(set(per_project["test_AX"]) | set(per_project["test_B"]))

    for family in all_families:
        ax_variants = per_project["test_AX"].get(family, [])
        b_variants = per_project["test_B"].get(family, [])

        ax_caps = {classify(stripped_capability(suf)) for _bare, suf in ax_variants}
        b_caps = {classify(stripped_capability(suf)) for _bare, suf in b_variants}

        only_ax = ax_caps - b_caps
        only_b = b_caps - ax_caps

        if not only_ax and not only_b:
            continue  # symmetric, nothing to flag

        print(f"{family}")
        print(f"    test_AX: {', '.join(sorted(bare for bare, _ in ax_variants)) or '(none)'}")
        print(f"    test_B : {', '.join(sorted(bare for bare, _ in b_variants)) or '(none)'}")
        if only_ax:
            print(f"    -> capability only in test_AX: {sorted(only_ax)}")
        if only_b:
            print(f"    -> capability only in test_B:  {sorted(only_b)}")
        print()


if __name__ == "__main__":
    main()
