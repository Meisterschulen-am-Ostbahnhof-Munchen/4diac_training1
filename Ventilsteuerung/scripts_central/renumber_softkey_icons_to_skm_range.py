"""Move the 8 softkey-icon CImage objects (PictureGraphic_PAGE_UP etc.,
created by wire_softkey_icons.py) from the DataMask PictureGraphic range
(20000-20499) into the correct SoftKeyMask/Working-Set-Bitmap range
(20500-20999), per the ISO 11783-6 ID-range table in
ms-docs/visual-programming-languages-docs/docs/de/runtime/isobus/Scaling.md.

These icons are only ever referenced from CSoftKey objects inside the
Ausgaenge/Eingaenge SoftKeyMasks, never from a DataMask, so 20000-20499
was the wrong half of the PictureGraphic block. The 8 pre-existing HOME
menu pictures (20000-20007, referenced from CButton objects on
DataMask_HOME) are correctly in the DataMask range already and are left
untouched.

Applied via a temporary ID range (+90000) so no two objects ever collide
mid-rename, same approach as renumber_fonts.py.
"""
import io
import re

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"

OLD_IDS = [20008, 20009, 20010, 20011, 20012, 20013, 20014, 20015]
NEW_BASE = 20500


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert "\r\n" in text

    old_to_new = {old: NEW_BASE + i for i, old in enumerate(OLD_IDS)}
    print("Renumbering:", old_to_new)

    def repl_id_attr(old, new):
        nonlocal text
        text = text.replace(f'JVS-ID="{old}"', f'JVS-ID="{new}"')

    temp_of = {old: 90000 + old for old in old_to_new}
    for old, temp in temp_of.items():
        repl_id_attr(old, temp)
    for old, temp in temp_of.items():
        repl_id_attr(temp, old_to_new[old])

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"Renumbered {len(old_to_new)} softkey-icon CImage IDs into the 20500+ SoftKeyMask range.")


if __name__ == "__main__":
    main()
