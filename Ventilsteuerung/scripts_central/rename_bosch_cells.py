"""Rename the Bosch section header and all 24 Bosch data rows' text cells,
eliminating every remaining "_11xxx" raw-ID ObjectName in the diagnostic
pages, per: "Container_Header_3115 in Container_Header_ACC1 umbenennen,
OutputString_11320 in OutputString_ACC1 und 32 hoch machen OutputString_11321
usw nach dem Muster benennen wie gehabt".

- Container_Header_3115 -> Container_Header_ACC1 (Bosch section header
  container - the only header not already renamed, since it has no STGn
  counterpart to derive a name from).
- OutputString_11320 (the header's own title text, "Neigungs-/
  Beschleunigungssensor (Bosch)") -> OutputString_ACC1, Height 18 -> 32
  (needs two lines at its existing FontAttributes_16x16 to fit the long
  title in its 300px-wide box).
- The 24 Bosch rows' three text cells each (matching the STG rows' column
  layout - width 110/180/100, verified per-row before writing this script)
  renamed following the SAME pattern already used for STG rows: base name
  from the row's own container name (e.g. "Eingang_Bosch_rAccX" ->
  "Bosch_rAccX"), column 2 gets "_name", column 3 gets "_ID". Pure
  renames, no font/height/width change for the data cells (only the
  header's height was explicitly requested).
"""
import io
import re

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert "\r\n" in text

    # 1. Container_Header_3115 -> Container_Header_ACC1
    text, n = re.subn(
        r'Name="Container_Header_3115" ObjectName="Container_Header_3115"',
        'Name="Container_Header_ACC1" ObjectName="Container_Header_ACC1"',
        text,
    )
    assert n == 1, f"Container_Header_3115 rename matched {n} times"
    print("Renamed Container_Header_3115 -> Container_Header_ACC1")

    # 2. OutputString_11320 -> OutputString_ACC1, Height 18 -> 32.
    block_pat = re.compile(
        r'<Object Class="COutputText" Name="OutputString_11320" ObjectName="OutputString_11320" '
        r'Pinned="FALSE" JVS-ID="11320">.*?</Object>',
        re.DOTALL,
    )
    m = block_pat.search(text)
    assert m, "OutputString_11320 block not found"
    block = m.group(0)
    new_block = block.replace(
        'Name="OutputString_11320" ObjectName="OutputString_11320"',
        'Name="OutputString_ACC1" ObjectName="OutputString_ACC1"',
    )
    new_block, n_h = re.subn(
        r'(<Property Name="Height">\s*<Value>)18(</Value>)', r"\g<1>32\g<2>", new_block, count=1
    )
    assert n_h == 1, f"OutputString_11320 height change matched {n_h} times"
    text = text[: m.start()] + new_block + text[m.end():]
    print("Renamed OutputString_11320 -> OutputString_ACC1, Height 18 -> 32")

    # 3. The 24 Bosch rows' three cells each.
    proxy_target = {}
    for pm in re.finditer(
        r'<Object Class="CProxy" Name="[^"]*" ObjectName="[^"]*" Pinned="FALSE" JVS-ID="(\d+)">(.*?)</Object>',
        text, re.DOTALL,
    ):
        pid, body = int(pm.group(1)), pm.group(2)
        ref_m = re.search(r'<Objects>\s*<Object JVS-ID="(\d+)"/>\s*</Objects>', body)
        if ref_m:
            proxy_target[pid] = int(ref_m.group(1))

    outtext_width = {}
    outtext_name = {}
    for om in re.finditer(
        r'<Object Class="COutputText" Name="([^"]*)" ObjectName="([^"]*)" Pinned="FALSE" JVS-ID="(\d+)">(.*?)</Object>',
        text, re.DOTALL,
    ):
        objname, oid, body = om.group(2), int(om.group(3)), om.group(4)
        wm = re.search(r'<Property Name="Width">\s*<Value>(\d+)</Value>', body)
        outtext_width[oid] = int(wm.group(1)) if wm else None
        outtext_name[oid] = objname

    row_pattern = re.compile(
        r'<Object Class="CGroup" Name="(Eingang_Bosch_(\w+))" ObjectName="\1" '
        r'Pinned="FALSE" JVS-ID="(\d+)">(.*?)</Object>',
        re.DOTALL,
    )

    SUFFIX_BY_WIDTH = {110: "", 180: "_name", 100: "_ID"}

    count = 0
    for row_name, field, cid, body in row_pattern.findall(text):
        children = [
            int(x) for x in re.findall(
                r'<Object JVS-ID="(\d+)"/>',
                re.search(r"<Objects>(.*?)</Objects>", body, re.DOTALL).group(1),
            )
        ]
        cols = {}
        for c in children:
            tgt = proxy_target.get(c)
            if tgt in outtext_width and outtext_width[tgt] in SUFFIX_BY_WIDTH:
                cols[outtext_width[tgt]] = tgt
        assert set(cols) == {110, 180, 100}, f"row {row_name}: expected 3 text columns, found {cols}"

        for width, oid in cols.items():
            old_name = outtext_name[oid]
            new_name = f"OutputString_Bosch_{field}{SUFFIX_BY_WIDTH[width]}"
            if old_name == new_name:
                continue
            old_tag = f'Name="{old_name}" ObjectName="{old_name}" Pinned="FALSE" JVS-ID="{oid}">'
            new_tag = f'Name="{new_name}" ObjectName="{new_name}" Pinned="FALSE" JVS-ID="{oid}">'
            text, n = re.subn(re.escape(old_tag), new_tag, text)
            assert n == 1, f"{old_name} (JVS-ID {oid}) rename matched {n} times"
            count += 1

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"Renamed {count} Bosch data-row cells.")


if __name__ == "__main__":
    main()
