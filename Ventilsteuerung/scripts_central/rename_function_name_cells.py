"""Roll out the OutputString_STG1_Q01_name prototype (renamed from
OutputString_11012, Height 18->24, FontAttributes_8x12) to the remaining
column-2 "Funktionsname" cells (width 180) of the 100 STG-pattern data
rows (60 Ausgaenge Q-rows + 40 Eingaenge I-rows). Width is left unchanged,
matching "Schrift und Groesse ident. usw."

Target name is derived from each row's own container name (e.g.
"Ausgang_STG1_Q02" -> "OutputString_STG1_Q02_name"), not guessed from
position - same approach as rename_data_rows.py. Rows already done
(Ausgang_STG1_Q01) are skipped automatically since their cell no longer
matches the "still on FontAttributes_6x8" old-state check.

The 24 Bosch rows have no STGn/pin identifier and are out of scope here.
"""
import io
import re

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"

OLD_FONT = 23000  # FontAttributes_6x8
NEW_FONT = 23002  # FontAttributes_8x12
OLD_HEIGHT = "18"
NEW_HEIGHT = "24"


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert "\r\n" in text

    proxy_target = {}
    for m in re.finditer(
        r'<Object Class="CProxy" Name="[^"]*" ObjectName="[^"]*" Pinned="FALSE" JVS-ID="(\d+)">(.*?)</Object>',
        text, re.DOTALL,
    ):
        pid, body = int(m.group(1)), m.group(2)
        ref_m = re.search(r'<Objects>\s*<Object JVS-ID="(\d+)"/>\s*</Objects>', body)
        if ref_m:
            proxy_target[pid] = int(ref_m.group(1))

    row_pattern = re.compile(
        r'<Object Class="CGroup" Name="((?:Ausgang|Eingang)_(STG\d+_[QI]\d+))" ObjectName="\1" '
        r'Pinned="FALSE" JVS-ID="(\d+)">(.*?)</Object>',
        re.DOTALL,
    )

    targets = []  # (old_id, new_name)
    for row_name, stg_pin, cid, body in row_pattern.findall(text):
        children = [
            int(x) for x in re.findall(
                r'<Object JVS-ID="(\d+)"/>',
                re.search(r"<Objects>(.*?)</Objects>", body, re.DOTALL).group(1),
            )
        ]
        for c in children:
            tgt = proxy_target.get(c)
            if tgt is None:
                continue
            obj_pat = re.compile(
                r'<Object Class="COutputText" Name="OutputString_' + str(tgt) +
                r'" ObjectName="OutputString_' + str(tgt) + r'" Pinned="FALSE" JVS-ID="' + str(tgt) + r'">'
                r'.*?<Property Name="Width">\s*<Value>180</Value>.*?'
                r'<Objects>\s*<Object JVS-ID="' + str(OLD_FONT) + r'"/>',
                re.DOTALL,
            )
            if obj_pat.search(text):
                targets.append((tgt, f"OutputString_{stg_pin}_name"))

    print(f"Found {len(targets)} function-name cells still to convert.")

    count = 0
    for oid, new_name in targets:
        block_pat = re.compile(
            r'<Object Class="COutputText" Name="OutputString_' + str(oid) +
            r'" ObjectName="OutputString_' + str(oid) + r'" Pinned="FALSE" JVS-ID="' + str(oid) + r'">.*?</Object>',
            re.DOTALL,
        )
        m = block_pat.search(text)
        assert m, f"block for {oid} not found"
        block = m.group(0)

        new_block = block.replace(
            f'Name="OutputString_{oid}" ObjectName="OutputString_{oid}"',
            f'Name="{new_name}" ObjectName="{new_name}"',
        )
        new_block = re.sub(
            r'(<Property Name="Height">\s*<Value>)' + OLD_HEIGHT + r'(</Value>)',
            r"\g<1>" + NEW_HEIGHT + r"\g<2>",
            new_block,
            count=1,
        )
        new_block, n_font = re.subn(
            r'(<Objects>\s*<Object JVS-ID=")' + str(OLD_FONT) + r'("/>)',
            r"\g<1>" + str(NEW_FONT) + r"\g<2>",
            new_block,
            count=1,
        )
        assert n_font == 1, f"font swap for {oid} matched {n_font} times"

        text = text[: m.start()] + new_block + text[m.end():]
        count += 1

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"Converted {count} function-name cells.")


if __name__ == "__main__":
    main()
