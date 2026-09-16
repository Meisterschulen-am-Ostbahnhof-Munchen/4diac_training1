"""Renumber the DataMask-half FontAttributes IDs into ascending ISO 11783-6
FontSize order (23000=6x8 .. 23014=128x192), so FontAttributes_6x8 = 23000 etc.

Two of the 15 (24x32, 12x16) currently sit at 23000/23001 (pre-existing, used
by the HOME menu) and need to move to their size-sorted slot (23006/23003) -
a cyclic permutation, not a simple shift. Applied via a temporary ID range
(90000+) so no two objects ever collide mid-rename. Updates both the
FontAttributes object definitions themselves and every other object's
`<Object JVS-ID="..."/>` reference to them (OutputText objects that use these
fonts).

SoftKeyMask-half fonts (23500-23514) are already in ascending order - untouched.
"""
import io
import re

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"

SIZES = [
    (6, 8), (8, 8), (8, 12), (12, 16), (16, 16), (16, 24), (24, 32), (32, 32),
    (32, 48), (48, 64), (64, 64), (64, 96), (96, 128), (128, 128), (128, 192),
]


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert "\r\n" in text

    # Discover current DataMask-half font IDs by their ObjectName (WxH, no _SKM suffix).
    current = {}
    for m in re.finditer(r'Class="CFontStyle" JVS-ID="(\d+)" ObjectName="FontAttributes_(\d+)x(\d+)"(?!_SKM)', text):
        jid, w, h = int(m.group(1)), int(m.group(2)), int(m.group(3))
        current[(w, h)] = jid

    target = {size: 23000 + i for i, size in enumerate(SIZES)}

    old_to_new = {}
    for size, new_id in target.items():
        old_id = current.get(size)
        assert old_id is not None, f"missing current FontAttributes for size {size}"
        if old_id != new_id:
            old_to_new[old_id] = new_id

    print("Renumbering:", old_to_new)
    if not old_to_new:
        print("Already in order, nothing to do.")
        return

    # Stage 1: old -> temp (90000 + old_id) for every ID that changes.
    def repl_id_attr(old, new):
        nonlocal text
        text = text.replace(f'JVS-ID="{old}"', f'JVS-ID="{new}"')

    temp_of = {old: 90000 + old for old in old_to_new}
    for old, temp in temp_of.items():
        repl_id_attr(old, temp)

    # Stage 2: temp -> final new id.
    for old, temp in temp_of.items():
        new = old_to_new[old]
        repl_id_attr(temp, new)

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"Renumbered {len(old_to_new)} font IDs (and all references to them).")


if __name__ == "__main__":
    main()
