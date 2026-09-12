"""Roll out the ObjectPointer_Status_STG1_Q01 rename (from ObjectPointer_
Status_27000) to the remaining 123 rows' status-color CPointer objects,
per "ObjectPointer_Status_27001 soll sein ObjectPointer_Status_STG1_Q02
usw.". Only the CPointer's own ObjectName is changed (Name stays the
literal "Pointer"), matching exactly what was done for row 1 - the
proxy that places the pointer inside each row's CGroup is left as-is,
consistent with how OutputString_11012/11013 were handled earlier (only
the underlying object was renamed, not its wrapping CProxy).

Target name is derived from each row's own container name (stripping the
"Ausgang_"/"Eingang_" prefix), e.g. row "Eingang_Bosch_rAccX" ->
ObjectPointer_Status_Bosch_rAccX - covers STG-pattern rows and the 24
Bosch rows alike, since this pointer has no naming constraint tying it to
a Q/I-specific format.

Uses a single self-contained literal match per object (old ObjectName +
matching JVS-ID in one line) - no unbounded regex spanning across object
boundaries, to avoid repeating the bug from rename_function_name_cells.py.
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

    pointer_objname = {
        int(m.group(2)): m.group(1)
        for m in re.finditer(
            r'<Object Class="CPointer" Name="Pointer" ObjectName="([^"]*)" Pinned="FALSE" JVS-ID="(\d+)">',
            text,
        )
    }

    row_pattern = re.compile(
        r'<Object Class="CGroup" Name="((?:Ausgang|Eingang)_(\w+))" ObjectName="\1" '
        r'Pinned="FALSE" JVS-ID="(\d+)">(.*?)</Object>',
        re.DOTALL,
    )

    count = 0
    skipped = 0
    for full_name, suffix, cid, body in row_pattern.findall(text):
        objs_m = re.search(r"<Objects>(.*?)</Objects>", body, re.DOTALL)
        children = [int(x) for x in re.findall(r'<Object JVS-ID="(\d+)"/>', objs_m.group(1))]

        ptr_id = None
        for c in children:
            tgt = proxy_target.get(c)
            if tgt in pointer_objname:
                ptr_id = tgt
        assert ptr_id is not None, f"no status pointer found for row {full_name}"

        old_name = pointer_objname[ptr_id]
        new_name = f"ObjectPointer_Status_{suffix}"
        if old_name == new_name:
            skipped += 1
            continue

        old_tag = f'ObjectName="{old_name}" Pinned="FALSE" JVS-ID="{ptr_id}">'
        new_tag = f'ObjectName="{new_name}" Pinned="FALSE" JVS-ID="{ptr_id}">'
        text, n = re.subn(re.escape(old_tag), new_tag, text)
        assert n == 1, f"{old_name} (JVS-ID {ptr_id}) rename matched {n} times"
        count += 1

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"Renamed {count} status pointers ({skipped} already done).")


if __name__ == "__main__":
    main()
