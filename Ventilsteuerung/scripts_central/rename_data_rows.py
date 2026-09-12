"""Rename the 124 data-row containers from their generator sequence numbers
(Ausgaenge_Row_NN / Eingaenge_Row_NN) to descriptive names, per the user's
request "Ausgaenge_Row_01 soll heissen Ausgang_STG1_Q01 usw.":

- Ausgaenge STG rows  -> Ausgang_STG{n}_Q{m:02d}  (pin WITH leading zero)
- Eingaenge STG rows  -> Eingang_STG{n}_I{m}       (pin WITHOUT leading zero)
- Eingaenge Bosch rows -> Eingang_Bosch_{field}     (e.g. Eingang_Bosch_rAccX)

The STG number and pin are read from each row's own column-1 title text
(width-110 cell, e.g. "STG1\\r\\nQ1" after the earlier two-line-label pass,
or the bare Bosch field name for the 24 Bosch rows) rather than guessed from
position, so the mapping is exact.

Each row's own page-placement CProxy (which carries a matching friendly
Name, same convention as the shared STG headers) is renamed alongside its
CGroup.

Prerequisite handled separately: GcfScript.py's row-height detection used to
require names ending in '_Row_01'/'_Row_02' - already changed to use the two
smallest Top values in the list content instead, so this rename does not
break it (verified via a dry run before this script was written).
"""
import io
import re
import base64

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"


def build_rename_map(text):
    proxy_target = {}
    for m in re.finditer(
        r'<Object Class="CProxy" Name="([^"]*)" ObjectName="[^"]*" Pinned="FALSE" JVS-ID="(\d+)">(.*?)</Object>',
        text, re.DOTALL,
    ):
        pid, body = int(m.group(2)), m.group(3)
        ref_m = re.search(r'<Objects>\s*<Object JVS-ID="(\d+)"/>\s*</Objects>', body)
        if ref_m:
            proxy_target[pid] = int(ref_m.group(1))

    outtext_info = {}
    for m in re.finditer(
        r'<Object Class="COutputText" Name="([^"]*)" ObjectName="([^"]*)" Pinned="FALSE" JVS-ID="(\d+)">(.*?)</Object>',
        text, re.DOTALL,
    ):
        oid, body = int(m.group(3)), m.group(4)
        wm = re.search(r'<Property Name="Width">\s*<Value>(\d+)</Value>', body)
        cm = re.search(r'<!\[CDATA\[([A-Za-z0-9+/=\s]+?)\]\]', body)
        width = int(wm.group(1)) if wm else None
        s = None
        if cm:
            b64 = re.sub(r"\s+", "", cm.group(1))
            s = base64.b64decode(b64).decode("utf-16-le").rstrip("\0")
        outtext_info[oid] = (width, s)

    row_pattern = re.compile(
        r'<Object Class="CGroup" Name="((?:Ausgaenge|Eingaenge)_Row_\d+)" ObjectName="\1" '
        r'Pinned="FALSE" JVS-ID="(\d+)">(.*?)</Object>',
        re.DOTALL,
    )

    rename_map = {}  # old_name -> new_name
    for old_name, cid, body in row_pattern.findall(text):
        children = [
            int(x) for x in re.findall(
                r'<Object JVS-ID="(\d+)"/>',
                re.search(r"<Objects>(.*?)</Objects>", body, re.DOTALL).group(1),
            )
        ]
        col1 = None
        for c in children:
            tgt = proxy_target.get(c)
            if tgt in outtext_info:
                width, s = outtext_info[tgt]
                if width == 110:
                    col1 = s

        assert col1 is not None, f"no column-1 text found for {old_name} ({cid})"

        is_ausgaenge = old_name.startswith("Ausgaenge")
        if "\r\n" in col1:
            stg, pin = col1.split("\r\n")
            if is_ausgaenge:
                num = int(pin[1:])
                new_name = f"Ausgang_{stg}_Q{num:02d}"
            else:
                new_name = f"Eingang_{stg}_{pin}"
        else:
            assert not is_ausgaenge, f"unexpected non-STG text on Ausgaenge row {old_name}: {col1!r}"
            new_name = f"Eingang_Bosch_{col1}"

        rename_map[old_name] = new_name

    return rename_map


def apply_renames(text, rename_map):
    for old_name, new_name in rename_map.items():
        # CGroup: Name and ObjectName both change.
        text, n1 = re.subn(
            r'Class="CGroup" Name="' + re.escape(old_name) + r'" ObjectName="' + re.escape(old_name) + r'"',
            f'Class="CGroup" Name="{new_name}" ObjectName="{new_name}"',
            text,
        )
        assert n1 == 1, f"CGroup rename for {old_name} matched {n1} times"

        # Placement CProxy: only the Name attribute + the internal Name property change.
        text, n2 = re.subn(
            r'Class="CProxy" Name="' + re.escape(old_name) + r'" ObjectName=""',
            f'Class="CProxy" Name="{new_name}" ObjectName=""',
            text,
        )
        assert n2 == 1, f"CProxy tag rename for {old_name} matched {n2} times"

        text, n3 = re.subn(
            r'(<Property Name="Name">\s*<Value>)' + re.escape(old_name) + r'(</Value>)',
            r"\g<1>" + new_name + r"\g<2>",
            text,
        )
        assert n3 == 1, f"CProxy Name-property rename for {old_name} matched {n3} times"

    return text


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert "\r\n" in text

    rename_map = build_rename_map(text)
    print(f"Renaming {len(rename_map)} data rows.")

    text = apply_renames(text, rename_map)

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)

    for old, new in list(rename_map.items())[:5]:
        print(f"  {old} -> {new}")
    print("  ...")
    for old, new in list(rename_map.items())[-5:]:
        print(f"  {old} -> {new}")


if __name__ == "__main__":
    main()
