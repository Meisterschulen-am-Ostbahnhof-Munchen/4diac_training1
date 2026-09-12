#!/usr/bin/env python3
"""Wrap AX_SUBSCRIBE_1 + GreenWhiteBackground1_AX into one reusable
parametrized SubApp Type (AX_SUBSCRIBE_BG_OPC), replacing the flat
per-channel pair I hand-wrote in Subscribe_STG{2..5}.SUB - per user
correction 2026-08-27 ("das ist schwachsinn ... in eine Subapp wandern,
die dann parametriert wird"). Same lesson as
refactor_dio_opcua_to_subapp_types.py: one type, many parametrized
instances, not repeated inline wiring.

AX_SUBSCRIBE_BG_OPC: Input Vars `ID` (WSTRING, remote OPC-UA subscribe
address) and `u16ObjId` (UINT, VT button Object ID) - wires
AX_SUBSCRIBE_1.OUT -> GreenWhiteBackground1_AX.DI1 internally, mirrors
logiBUS_IXA_BG_OPC's own internal shape.

Usage: python3 build_ax_subscribe_bg_type.py
"""
import re

BASE = "4diacIDE-workspace/test/FBs/Ventilsteuerung"
STG1_DIR = f"{BASE}/Ventilsteuerung_STG1"
NUM_I = 8
NUM_Q = 12
REMOTE_MODULES = [2, 3, 4, 5]

TYPE_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<SubAppType Name="AX_SUBSCRIBE_BG_OPC" Comment="OPC-UA Remote-Subscribe + VT-Hintergrundfarbe (generisch, ein Kanal)">\n'
    '\t<Identification Standard="61499-2">\n'
    '\t</Identification>\n'
    '\t<VersionInfo Version="1.0" Author="franz" Date="2026-08-27">\n'
    '\t</VersionInfo>\n'
    '\t<CompilerInfo>\n'
    '\t\t<Import declaration="isobus::UT::Q::const::IDs::ID_NULL"/>\n'
    '\t</CompilerInfo>\n'
    '\t<SubAppInterfaceList>\n'
    '\t\t<InputVars>\n'
    '\t\t\t<VarDeclaration Name="u16ObjId" Type="UINT" Comment="Object ID Hintergrund-Rechteck (VT)" InitialValue="ID_NULL"/>\n'
    '\t\t\t<VarDeclaration Name="ID" Type="WSTRING" Comment="OPC-UA Remote-Subscribe-Adresse"/>\n'
    '\t\t</InputVars>\n'
    '\t</SubAppInterfaceList>\n'
    '\t<SubAppNetwork>\n'
    '\t\t<FB Name="AX_SUBSCRIBE_1" Type="adapter::net::AX_SUBSCRIBE_1" x="0" y="0">\n'
    '\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
    '\t\t</FB>\n'
    '\t\t<SubApp Name="GreenWhiteBackground1_AX" Type="GreenWhiteBackground1_AX" x="1500" y="0">\n'
    '\t\t</SubApp>\n'
    '\t\t<DataConnections>\n'
    '\t\t\t<Connection Source="ID" Destination="AX_SUBSCRIBE_1.ID">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Connection>\n'
    '\t\t\t<Connection Source="u16ObjId" Destination="GreenWhiteBackground1_AX.u16ObjId">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Connection>\n'
    '\t\t</DataConnections>\n'
    '\t\t<AdapterConnections>\n'
    '\t\t\t<Connection Source="AX_SUBSCRIBE_1.OUT" Destination="GreenWhiteBackground1_AX.DI1"/>\n'
    '\t\t</AdapterConnections>\n'
    '\t</SubAppNetwork>\n'
    '</SubAppType>\n'
)


def button_const(m, kind, num):
    if kind == "Q":
        return f"Button_Ausgang_STG{m}_Q{num:02d}"
    return f"Button_Eingang_STG{m}_I{num}"


def id_const(m, kind, num):
    label = f"Q{num:02d}" if kind == "Q" else f"I{num}"
    return f"STG{m}_{label}_REMOTE"


def rewrite_subscribe(m):
    path = f"{STG1_DIR}/Subscribe_STG{m}.SUB"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    channels = [("Q", q) for q in range(1, NUM_Q + 1)] + [("I", i) for i in range(1, NUM_I + 1)]

    # Replace the flat FB+SubApp+connection block with parametrized SubApp instances.
    pattern = re.compile(
        r'\t\t<FB Name="Subscribe_STG' + str(m) + r'_(?:Q\d\d|I\d)_Remote".*?</FB>\n'
        r'(?:\t\t<FB Name="Subscribe_STG' + str(m) + r'_(?:Q\d\d|I\d)_Remote".*?</FB>\n)*'
        r'(?:\t\t<SubApp Name="Background_STG' + str(m) + r'_(?:Q\d\d|I\d)".*?</SubApp>\n)*'
        r'\t\t<AdapterConnections>\n'
        r'(?:\t\t<Connection Source="Subscribe_STG' + str(m) + r'_(?:Q\d\d|I\d)_Remote\.OUT".*?/>\n)*'
        r'\t\t</AdapterConnections>\n',
        re.DOTALL,
    )
    matches = pattern.findall(content)
    assert len(matches) == 1, f"{path}: expected exactly one flat block, found {len(matches)}"

    y = 0
    replacement = ""
    for kind, num in channels:
        label = f"Q{num:02d}" if kind == "Q" else f"I{num}"
        name = f"Subscribe_STG{m}_{label}_Remote"
        replacement += (
            f'\t\t<SubApp Name="{name}" Type="AX_SUBSCRIBE_BG_OPC" x="0" y="{y}">\n'
            f'\t\t\t<Parameter Name="ID" Value="{id_const(m, kind, num)}"/>\n'
            f'\t\t\t<Parameter Name="u16ObjId" Value="{button_const(m, kind, num)}"/>\n'
            f'\t\t</SubApp>\n'
        )
        y += 700

    new_content, count = pattern.subn(replacement, content)
    assert count == 1

    # Add the Button_* imports (from FBs::const::DefaultPool) needed for the new Parameter values.
    imports = "".join(
        f'\t\t<Import declaration="FBs::const::DefaultPool::{button_const(m, kind, num)}"/>\n'
        for kind, num in channels
    )
    new_content = re.sub(r'(\t<CompilerInfo>\n)', r'\1' + imports, new_content, count=1)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)
    print(f"{path}: rewritten (20 flat pairs -> 20 AX_SUBSCRIBE_BG_OPC instances)")


def main():
    type_path = f"{BASE}/AX_SUBSCRIBE_BG_OPC/AX_SUBSCRIBE_BG_OPC.SUB"
    import os
    os.makedirs(f"{BASE}/AX_SUBSCRIBE_BG_OPC", exist_ok=True)
    with open(type_path, "w", encoding="utf-8", newline="") as f:
        f.write(TYPE_XML)
    print(f"{type_path}: written")

    for m in REMOTE_MODULES:
        rewrite_subscribe(m)


if __name__ == "__main__":
    main()
