#!/usr/bin/env python3
"""Wire STG1's 80 remote AX_SUBSCRIBE_1 outputs into GreenWhiteBackground1_AX
instances so the VT buttons for STG2-5's channels actually turn green/white.

Root cause (found via real hardware test 2026-08-27): each module's own
Inputs_STGn/Outputs_STGn already drive their OWN button's background colour
correctly (via GreenWhiteBackground1_AX inside logiBUS_IXA_BG_OPC /
Button_IXA_TO_logiBUS_QXA_BG_OPC) - but only STG1 has an ISOBUS/VT
connection (per OPC_UA_VERNETZUNG.md), so STG2-5 running that same FB
locally has no path to the physical VT screen; the colour command goes
nowhere. Confirmed: STG1's own Input_I1 button turns green, but
Button_Eingang_STG2_I1 does not, even though Subscribe_STG2_I1_Remote
correctly receives the value over OPC-UA.

Fix: add a GreenWhiteBackground1_AX instance per remote channel, living on
STG1 (the only device that can talk to the VT), fed from the existing
Subscribe_STG{m}_*_Remote.OUT adapter - mirrors the same
AX_SPLIT_2->GreenWhiteBackground1_AX wiring already used locally, minus
the split (nothing else consumes the remote value yet).

u16ObjId reuses the same FBs::const::DefaultPool::Button_Ausgang_STGn_Qpp /
Button_Eingang_STGn_Ip constants already used for the local wiring (VT
Object IDs are global, addressable from any FORTE instance's VT commands -
only the *connection* to the VT is STG1-exclusive).

Usage: python3 wire_remote_status_colors.py
"""
import re

BASE = "4diacIDE-workspace/test/FBs/Ventilsteuerung"
STG1_DIR = f"{BASE}/Ventilsteuerung_STG1"
NUM_I = 8
NUM_Q = 12
REMOTE_MODULES = [2, 3, 4, 5]


def button_const(m, kind, num):
    if kind == "Q":
        return f"Button_Ausgang_STG{m}_Q{num:02d}"
    return f"Button_Eingang_STG{m}_I{num}"


def rewrite_subscribe(m):
    path = f"{STG1_DIR}/Subscribe_STG{m}.SUB"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    channels = [("Q", q) for q in range(1, NUM_Q + 1)] + [("I", i) for i in range(1, NUM_I + 1)]

    imports = "".join(
        f'\t\t<Import declaration="FBs::const::DefaultPool::{button_const(m, kind, num)}"/>\n'
        for kind, num in channels
    )
    content = re.sub(r'(\t<CompilerInfo>\n)', r'\1' + imports, content, count=1)

    subapps = ""
    conns = ""
    y = 16000
    for kind, num in channels:
        label = f"Q{num:02d}" if kind == "Q" else f"I{num}"
        subscribe_name = f"Subscribe_STG{m}_{label}_Remote"
        bg_name = f"Background_STG{m}_{label}"
        subapps += (
            f'\t\t<SubApp Name="{bg_name}" Type="GreenWhiteBackground1_AX" x="1500" y="{y}">\n'
            f'\t\t\t<Parameter Name="u16ObjId" Value="{button_const(m, kind, num)}"/>\n'
            f'\t\t</SubApp>\n'
        )
        conns += f'\t\t<Connection Source="{subscribe_name}.OUT" Destination="{bg_name}.DI1"/>\n'
        y += 800

    marker = "\t</SubAppNetwork>\n"
    assert content.count(marker) == 1
    block = subapps + "\t\t<AdapterConnections>\n" + conns + "\t\t</AdapterConnections>\n"
    content = content.replace(marker, block + marker)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{path}: rewritten (+{len(channels)} GreenWhiteBackground1_AX + connections)")


def main():
    for m in REMOTE_MODULES:
        rewrite_subscribe(m)


if __name__ == "__main__":
    main()
