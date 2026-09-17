#!/usr/bin/env python3
"""Add a real CButton per DI/DO Scroll row (Ausgaenge + Eingaenge), replacing
the row's placeholder ObjectPointer_Status (grey/green/red rectangle swap,
never actually redirected) with a small CButton whose own BackColor gets
changed directly at runtime by Q_BackgroundColour / GreenWhiteBackground1_AX
(the mechanism already wired into logiBUS_IXA_BG_OPC /
Button_IXA_TO_logiBUS_QXA_BG_OPC on the FORTE side) - per user request
2026-08-25 ("bei allen Eingaengen und Ausgaengen je einen Button hin").

Only the 100 STG I/Q rows get a button (Ausgang_STG{1..5}_Q{01..12},
Eingang_STG{1..5}_I{1..8}) - the 24 Bosch IMU rows are untouched (different
feature, not part of the DI/DO OPC-UA work) and keep using the shared
grey/green/red rectangles + ObjectPointer indirection.

Button size/position (user decision 2026-08-25, "nur die Status-Flaeche
vergroessern"): 32x32 (was 18x18), same right-aligned slot inside the
432x36 row -> left=394, top=2 (row's existing 3 text columns, ending at
x<=408, are untouched).

Latching: non-latching for now (user decision 2026-08-25, "wir nehmen mal
ueberall non-latching Buttons", can change later) - Latchable=0 for both
input and output buttons. Per user: input buttons exist purely for the
GreenWhiteBackground colour target (not meant to actually be pressed in
practice, mirrors C:\\git\\ms\\4diac_training1\\...\\Workspace_Tester's
input buttons); output buttons are meant to be genuinely pressable.

NOTE on line endings: DefaultPool.jop is CRLF (unlike the LF-only .sub
files) - read/written with newline="" (no translation) and every
constructed line below uses "\r\n" explicitly, per the iso-designer-jop
skill's CRLF-preservation rule.

For each of the 100 rows:
  1. Find the row's CGroup (Ausgang_STG{n}_Q{pp} / Eingang_STG{n}_I{p}),
     read its last child ref (the row-specific ObjectPointer_Status
     CProxy).
  2. Delete that CProxy definition and its target CPointer definition
     entirely (both are per-row, never shared - safe to remove).
  3. Swap that one child reference in the CGroup's <Objects> list for a
     new CProxy wrapping a new CButton (in place, same list position).
  4. Append the new CButton + CProxy object definitions.

IDs allocated sequentially above the current file max per class (CButton
6000 block, CProxy 4194304+ own space) - scanned at script start, not
hardcoded, per the iso-designer-jop skill's ID-block convention.

Usage: python3 add_row_buttons.py [--dry-run]
"""
import re
import sys

POOL = "ISO-DesignerProjects/Workspace/DefaultPool/DefaultPool.jop"
NL = "\r\n"

NUM_I = 8
NUM_Q = 12
MODULES = [1, 2, 3, 4, 5]

BTN_WIDTH = 32
BTN_HEIGHT = 32
BTN_LEFT = 394
BTN_TOP = 2

CHILD_REF_RE = re.compile(r'<Object JVS-ID="(\d+)"/>')


def button_block(jvs_id, object_name, key_code):
    # KeyCode=0 is invalid (ISO-Designer warns and silently defaults it to 1
    # for every button) - each button gets its own unique code instead, per
    # user correction 2026-08-25 ("die Key-Codes sinnvoll setzen ... besser
    # jeder Button einen code").
    lines = [
        f'\t\t<Object Class="CButton" Name="Button" ObjectName="{object_name}" Pinned="FALSE" JVS-ID="{jvs_id}">',
        '\t\t\t<PropertySheet Name="Button">',
        '\t\t\t\t<Property Name="BackColor">',
        '\t\t\t\t\t<Value>10066329</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="BorderColor">',
        '\t\t\t\t\t<Value>10027008</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="KeyCode">',
        f'\t\t\t\t\t<Value>{key_code}</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Hotkey">',
        '\t\t\t\t\t<Value>0</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Latchable">',
        '\t\t\t\t\t<Value>0</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Latched">',
        '\t\t\t\t\t<Value>0</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="SuppressBorder">',
        '\t\t\t\t\t<Value>0</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="TransparentBackground">',
        '\t\t\t\t\t<Value>0</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Enabled">',
        '\t\t\t\t\t<Value>1</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="NoBorder">',
        '\t\t\t\t\t<Value>0</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="RoundEdgeRadius">',
        '\t\t\t\t\t<Value>0</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="AutoAdjustTextarea">',
        '\t\t\t\t\t<Value>0</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="3DStyle">',
        '\t\t\t\t\t<Value>0</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Width">',
        f'\t\t\t\t\t<Value>{BTN_WIDTH}</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Height">',
        f'\t\t\t\t\t<Value>{BTN_HEIGHT}</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Visible">',
        '\t\t\t\t\t<Value>1</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Locked">',
        '\t\t\t\t\t<Value>0</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Comment">',
        '\t\t\t\t\t<Value>',
        '\t\t\t\t\t\t<![CDATA[AAA=]]>',
        '\t\t\t\t\t</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Disabled">',
        '\t\t\t\t\t<Value>0</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="ExternalReferenceAllowed">',
        '\t\t\t\t\t<Value>0</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t</PropertySheet>',
        '\t\t\t<Objects>',
        '\t\t\t</Objects>',
        '\t\t</Object>',
    ]
    return NL.join(lines) + NL


def proxy_block(jvs_id, name, target_id):
    lines = [
        f'\t\t<Object Class="CProxy" Name="{name}" ObjectName="" Pinned="FALSE" JVS-ID="{jvs_id}">',
        '\t\t\t<PropertySheet Name="Proxy">',
        '\t\t\t\t<Property Name="Top">',
        f'\t\t\t\t\t<Value>{BTN_TOP}</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Left">',
        f'\t\t\t\t\t<Value>{BTN_LEFT}</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Name">',
        f'\t\t\t\t\t<Value>{name}</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="TabIndex">',
        '\t\t\t\t\t<Value>-1</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t\t<Property Name="Transform">',
        f'\t\t\t\t\t<Value>(1.0000000000000000)(0.0000000000000000)({BTN_LEFT}.0000000000000000)(0.0000000000000000)(1.0000000000000000)({BTN_TOP}.0000000000000000)</Value>',
        '\t\t\t\t</Property>',
        '\t\t\t</PropertySheet>',
        '\t\t\t<Objects>',
        f'\t\t\t\t<Object JVS-ID="{target_id}"/>',
        '\t\t\t</Objects>',
        '\t\t</Object>',
    ]
    return NL.join(lines) + NL


def find_block_by_id(content, jvs_id):
    """Return (full_match_text, class) for the object definition with this JVS-ID."""
    pattern = re.compile(
        r'\t\t<Object Class="([^"]+)" Name="[^"]*" ObjectName="[^"]*" Pinned="FALSE" JVS-ID="'
        + re.escape(jvs_id) + r'">\r\n'
        r'.*?\r\n'
        r'\t\t</Object>\r\n',
        re.DOTALL,
    )
    m = pattern.search(content)
    assert m, f"block for JVS-ID={jvs_id} not found"
    return m.group(0), m.group(1)


def find_group_block(content, row_name):
    pattern = re.compile(
        r'\t\t<Object Class="CGroup" Name="' + re.escape(row_name) + r'" ObjectName="'
        + re.escape(row_name) + r'" Pinned="FALSE" JVS-ID="(\d+)">\r\n'
        r'.*?\r\n'
        r'\t\t</Object>\r\n',
        re.DOTALL,
    )
    m = pattern.search(content)
    assert m, f"CGroup {row_name} not found"
    return m.group(0)


def main():
    dry_run = "--dry-run" in sys.argv
    with open(POOL, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" in content, "expected CRLF in DefaultPool.jop"
    assert content.count("\n") == content.count("\r\n"), "mixed line endings detected"

    max_button = max(int(m) for m in re.findall(r'Class="CButton"[^>]*JVS-ID="(\d+)"', content))
    max_proxy = max(int(m) for m in re.findall(r'Class="CProxy"[^>]*JVS-ID="(\d+)"', content))
    next_button = max_button + 1
    next_proxy = max_proxy + 1
    print(f"Starting IDs: CButton {next_button}, CProxy {next_proxy}")

    targets = []
    for n in MODULES:
        for q in range(1, NUM_Q + 1):
            targets.append(f"Ausgang_STG{n}_Q{q:02d}")
    for n in MODULES:
        for i in range(1, NUM_I + 1):
            targets.append(f"Eingang_STG{n}_I{i}")
    assert len(targets) == 100

    new_blocks = []
    removed_cproxy = 0
    removed_cpointer = 0

    for key_code, row_name in enumerate(targets, start=1):
        group_block = find_group_block(content, row_name)

        objects_start = group_block.index("<Objects>")
        child_ids = CHILD_REF_RE.findall(group_block[objects_start:])
        assert len(child_ids) == 5, f"{row_name}: expected 5 children, found {len(child_ids)}"
        status_proxy_id = child_ids[-1]

        status_proxy_block, status_proxy_cls = find_block_by_id(content, status_proxy_id)
        assert status_proxy_cls == "CProxy", f"{row_name}: 5th child is {status_proxy_cls}, not CProxy"

        pointer_ids = CHILD_REF_RE.findall(status_proxy_block[status_proxy_block.index("<Objects>"):])
        assert len(pointer_ids) == 1, f"{row_name}: status proxy has {len(pointer_ids)} children, expected 1"
        pointer_id = pointer_ids[0]
        pointer_block, pointer_cls = find_block_by_id(content, pointer_id)
        assert pointer_cls == "CPointer", f"{row_name}: proxy target is {pointer_cls}, not CPointer"

        # Remove old CProxy + CPointer definitions.
        assert content.count(status_proxy_block) == 1
        content = content.replace(status_proxy_block, "", 1)
        removed_cproxy += 1
        assert content.count(pointer_block) == 1
        content = content.replace(pointer_block, "", 1)
        removed_cpointer += 1

        # Allocate new IDs, swap the reference in place.
        btn_id = next_button
        next_button += 1
        prx_id = next_proxy
        next_proxy += 1

        object_name = f"Button_{row_name}"
        proxy_name = f"Button_{row_name}"

        old_ref = f'Object JVS-ID="{status_proxy_id}"/>'
        new_ref = f'Object JVS-ID="{prx_id}"/>'
        assert content.count(old_ref) == 1, f"{row_name}: expected exactly one reference to old proxy {status_proxy_id}"
        content = content.replace(old_ref, new_ref, 1)

        new_blocks.append(button_block(btn_id, object_name, key_code))
        new_blocks.append(proxy_block(prx_id, proxy_name, btn_id))

    # Insert all new object definitions just before the final closing tags.
    marker = "\t</Objects>\r\n</JetView-ObjectPool>"
    assert content.count(marker) == 1, "expected exactly one closing marker"
    content = content.replace(marker, "".join(new_blocks) + marker)

    print(f"Removed {removed_cproxy} CProxy + {removed_cpointer} CPointer (old status pointers)")
    print(f"Added {len(targets)} CButton + {len(targets)} CProxy (new row buttons)")
    print(f"CButton range used: {max_button + 1}-{next_button - 1}")
    print(f"CProxy range used: {max_proxy + 1}-{next_proxy - 1}")

    if dry_run:
        print("--dry-run: not writing file")
        return

    with open(POOL, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{POOL}: written")


if __name__ == "__main__":
    main()
