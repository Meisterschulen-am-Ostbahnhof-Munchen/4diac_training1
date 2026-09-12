"""Rename the 16 ObjectPointer_SoftKey_* objects so the page they belong
to is explicit in the name, per: "ObjectPointer_SoftKey_FIRST
ObjectPointer_SoftKey_FIRST_1 ist komplett doof. da weiss man nicht wo das
hin gehoert. nenne die SINNVOLL."

The old naming used a bare role name for Ausgaenge (ObjectPointer_SoftKey_
FIRST) and a "_1" suffix for Eingaenge (ObjectPointer_SoftKey_FIRST_1) -
neither tells you which page it's on at a glance. Both sides are renamed
for symmetry: ObjectPointer_SoftKey_Ausgaenge_FIRST /
ObjectPointer_SoftKey_Eingaenge_FIRST.
"""
import io

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"

ROLES = ["Back", "DOWN", "FIRST", "LAST", "Lock", "PAGE_DOWN", "PAGE_UP", "UP"]


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert "\r\n" in text

    rename_map = {}
    for role in ROLES:
        rename_map[f"ObjectPointer_SoftKey_{role}"] = f"ObjectPointer_SoftKey_Ausgaenge_{role}"
        rename_map[f"ObjectPointer_SoftKey_{role}_1"] = f"ObjectPointer_SoftKey_Eingaenge_{role}"

    count = 0
    for old, new in rename_map.items():
        old_tag = f'ObjectName="{old}"'
        new_tag = f'ObjectName="{new}"'
        n = text.count(old_tag)
        assert n == 1, f"{old}: found {n} times"
        text = text.replace(old_tag, new_tag)
        count += 1

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"Renamed {count} ObjectPointer_SoftKey_* objects.")


if __name__ == "__main__":
    main()
