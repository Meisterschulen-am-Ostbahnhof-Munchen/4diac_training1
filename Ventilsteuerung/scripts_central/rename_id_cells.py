"""Roll out the OutputString_STG1_Q01_ID rename (from OutputString_11013)
to the remaining 99 STG-pattern rows' column-3 "Anschlussbezeichnung"
cells (width 100), per "OutputString_11016 muss werden
OutputString_STG1_Q02_ID usw.". Pure rename only - no font/height change,
matching what was done for row 1's _ID cell.

Target name derived from each row's own container name (e.g.
"Ausgang_STG1_Q02" -> "OutputString_STG1_Q02_ID"), same approach as
rename_function_name_cells.py/rename_status_pointers.py. Uses a single
self-contained literal match per object (old ObjectName + matching
JVS-ID in one line), same safe pattern as rename_status_pointers.py -
no unbounded regex spanning object boundaries.
"""
import io
import re

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"


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

    outtext_width = {}
    outtext_name = {}
    for m in re.finditer(
        r'<Object Class="COutputText" Name="([^"]*)" ObjectName="([^"]*)" Pinned="FALSE" JVS-ID="(\d+)">(.*?)</Object>',
        text, re.DOTALL,
    ):
        objname, oid, body = m.group(2), int(m.group(3)), m.group(4)
        wm = re.search(r'<Property Name="Width">\s*<Value>(\d+)</Value>', body)
        outtext_width[oid] = int(wm.group(1)) if wm else None
        outtext_name[oid] = objname

    row_pattern = re.compile(
        r'<Object Class="CGroup" Name="((?:Ausgang|Eingang)_(STG\d+_[QI]\d+))" ObjectName="\1" '
        r'Pinned="FALSE" JVS-ID="(\d+)">(.*?)</Object>',
        re.DOTALL,
    )

    count = 0
    skipped = 0
    for row_name, stg_pin, cid, body in row_pattern.findall(text):
        children = [
            int(x) for x in re.findall(
                r'<Object JVS-ID="(\d+)"/>',
                re.search(r"<Objects>(.*?)</Objects>", body, re.DOTALL).group(1),
            )
        ]
        col3 = None
        for c in children:
            tgt = proxy_target.get(c)
            if tgt in outtext_width and outtext_width[tgt] == 100:
                col3 = tgt
        assert col3 is not None, f"no column-3 cell found for {row_name}"

        old_name = outtext_name[col3]
        new_name = f"OutputString_{stg_pin}_ID"
        if old_name == new_name:
            skipped += 1
            continue

        old_tag = f'Name="{old_name}" ObjectName="{old_name}" Pinned="FALSE" JVS-ID="{col3}">'
        new_tag = f'Name="{new_name}" ObjectName="{new_name}" Pinned="FALSE" JVS-ID="{col3}">'
        text, n = re.subn(re.escape(old_tag), new_tag, text)
        assert n == 1, f"{old_name} (JVS-ID {col3}) rename matched {n} times"
        count += 1

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"Renamed {count} ID cells ({skipped} already done).")


if __name__ == "__main__":
    main()
