#!/usr/bin/env python3
"""Remove GreenWhiteBackground1_AX / Button_IXA from STG2-STG5's local I/O
wiring - per user correction 2026-08-27. Root cause established with
wire_remote_status_colors.py: only STG1 has an ISOBUS/VT connection
(OPC_UA_VERNETZUNG.md), so anything VT-bound (GreenWhiteBackground1_AX,
and equally Button_IXA - both live under the isobus::UT package and need
a real VT link) is a no-op on STG2-5 and should not be there at all.
STG1's own Inputs_STG1/Outputs_STG1 are untouched (it has the VT link,
this wiring is genuinely live there).

Adds two new reusable types (no VT dependency, for STG2-5 only):
  - logiBUS_IXA_OPC: logiBUS_IXA -> AX_PUBLISH_1 (no background)
  - logiBUS_QXA_OPC: AX_SUBSCRIBE_1 -> AX_SPLIT_2 -> (logiBUS_QXA +
    AX_PUBLISH_1) (no Button_IXA/AX_SR/background)

Rewrites Inputs_STG{2..5}.SUB / Outputs_STG{2..5}.SUB: SubApp Type
switched to the new *_OPC types, the now-unsupported u16ObjId Parameter
line removed, and the now-unused Button_* imports dropped.

Usage: python3 strip_vt_from_non_vt_modules.py
"""
import re

BASE = "4diacIDE-workspace/test/FBs/Ventilsteuerung"
NUM_I = 8
NUM_Q = 12
NON_VT_MODULES = [2, 3, 4, 5]

DI_OPC_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<SubAppType Name="logiBUS_IXA_OPC" Comment="logiBUS DI Kanal: OPC-UA-Publish (generisch, ein Kanal, ohne VT-Hintergrundfarbe - fuer Module ohne ISOBUS/VT-Anbindung)">\n'
    '\t<Identification Standard="61499-2">\n'
    '\t</Identification>\n'
    '\t<VersionInfo Version="1.0" Author="franz" Date="2026-08-27">\n'
    '\t</VersionInfo>\n'
    '\t<CompilerInfo>\n'
    '\t\t<Import declaration="logiBUS::io::DI::logiBUS_DI::Invalid"/>\n'
    '\t</CompilerInfo>\n'
    '\t<SubAppInterfaceList>\n'
    '\t\t<InputVars>\n'
    '\t\t\t<VarDeclaration Name="Input" Type="logiBUS::io::DI::logiBUS_DI_S" Comment="Identify the Input Input_I1..I8" InitialValue="logiBUS_DI::Invalid"/>\n'
    '\t\t\t<VarDeclaration Name="ID_WRITE" Type="WSTRING" Comment="OPC-UA Publish-Key (lesbar)"/>\n'
    '\t\t</InputVars>\n'
    '\t</SubAppInterfaceList>\n'
    '\t<SubAppNetwork>\n'
    '\t\t<FB Name="logiBUS_IXA" Type="logiBUS::io::DI::logiBUS_IXA" x="0" y="0">\n'
    '\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
    '\t\t\t<Parameter Name="PARAMS" Value="">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Parameter>\n'
    '\t\t</FB>\n'
    '\t\t<FB Name="AX_PUBLISH_1" Type="adapter::net::AX_PUBLISH_1" x="1500" y="0">\n'
    '\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
    '\t\t</FB>\n'
    '\t\t<DataConnections>\n'
    '\t\t\t<Connection Source="Input" Destination="logiBUS_IXA.Input">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Connection>\n'
    '\t\t\t<Connection Source="ID_WRITE" Destination="AX_PUBLISH_1.ID">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Connection>\n'
    '\t\t</DataConnections>\n'
    '\t\t<AdapterConnections>\n'
    '\t\t\t<Connection Source="logiBUS_IXA.IN" Destination="AX_PUBLISH_1.IN"/>\n'
    '\t\t</AdapterConnections>\n'
    '\t</SubAppNetwork>\n'
    '</SubAppType>\n'
)

DQ_OPC_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<SubAppType Name="logiBUS_QXA_OPC" Comment="logiBUS DQ Kanal: OPC-UA Read/Write (generisch, ein Kanal, ohne VT-Button/Hintergrundfarbe - fuer Module ohne ISOBUS/VT-Anbindung)">\n'
    '\t<Identification Standard="61499-2">\n'
    '\t</Identification>\n'
    '\t<VersionInfo Version="1.0" Author="franz" Date="2026-08-27">\n'
    '\t</VersionInfo>\n'
    '\t<CompilerInfo>\n'
    '\t\t<Import declaration="logiBUS::io::DQ::logiBUS_DO::Invalid"/>\n'
    '\t</CompilerInfo>\n'
    '\t<SubAppInterfaceList>\n'
    '\t\t<InputVars>\n'
    '\t\t\t<VarDeclaration Name="Output" Type="logiBUS::io::DQ::logiBUS_DO_S" Comment="Identify the Output Output_Q1..Q12" InitialValue="logiBUS_DO::Invalid"/>\n'
    '\t\t\t<VarDeclaration Name="ID_READ" Type="WSTRING" Comment="OPC-UA Subscribe-Key (schreibbar)"/>\n'
    '\t\t\t<VarDeclaration Name="ID_WRITE" Type="WSTRING" Comment="OPC-UA Publish-Key (lesbar)"/>\n'
    '\t\t</InputVars>\n'
    '\t</SubAppInterfaceList>\n'
    '\t<SubAppNetwork>\n'
    '\t\t<FB Name="logiBUS_QXA" Type="logiBUS::io::DQ::logiBUS_QXA" x="0" y="0">\n'
    '\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
    '\t\t\t<Parameter Name="PARAMS" Value="">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Parameter>\n'
    '\t\t</FB>\n'
    '\t\t<FB Name="AX_SUBSCRIBE_1" Type="adapter::net::AX_SUBSCRIBE_1" x="1000" y="0">\n'
    '\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
    '\t\t</FB>\n'
    '\t\t<FB Name="AX_SPLIT_2" Type="adapter::events::unidirectional::AX_SPLIT_2" x="2000" y="0">\n'
    '\t\t</FB>\n'
    '\t\t<FB Name="AX_PUBLISH_1" Type="adapter::net::AX_PUBLISH_1" x="3000" y="0">\n'
    '\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
    '\t\t</FB>\n'
    '\t\t<DataConnections>\n'
    '\t\t\t<Connection Source="Output" Destination="logiBUS_QXA.Output">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Connection>\n'
    '\t\t\t<Connection Source="ID_READ" Destination="AX_SUBSCRIBE_1.ID">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Connection>\n'
    '\t\t\t<Connection Source="ID_WRITE" Destination="AX_PUBLISH_1.ID">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Connection>\n'
    '\t\t</DataConnections>\n'
    '\t\t<AdapterConnections>\n'
    '\t\t\t<Connection Source="AX_SUBSCRIBE_1.OUT" Destination="AX_SPLIT_2.IN"/>\n'
    '\t\t\t<Connection Source="AX_SPLIT_2.OUT1" Destination="logiBUS_QXA.OUT"/>\n'
    '\t\t\t<Connection Source="AX_SPLIT_2.OUT2" Destination="AX_PUBLISH_1.IN"/>\n'
    '\t\t</AdapterConnections>\n'
    '\t</SubAppNetwork>\n'
    '</SubAppType>\n'
)


def rewrite_inputs(n):
    path = f"{BASE}/Ventilsteuerung_STG{n}/Inputs_STG{n}.SUB"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    for i in range(1, NUM_I + 1):
        old_import = f'\t\t<Import declaration="FBs::const::DefaultPool::Button_Eingang_STG{n}_I{i}"/>\n'
        assert content.count(old_import) == 1, (path, old_import)
        content = content.replace(old_import, "", 1)

        old_u16 = f'\n\t\t\t<Parameter Name="u16ObjId" Value="Button_Eingang_STG{n}_I{i}"/>'
        assert content.count(old_u16) == 1, (path, old_u16)
        content = content.replace(old_u16, "", 1)

    content = content.replace('Type="logiBUS_IXA_BG_OPC"', 'Type="logiBUS_IXA_OPC"')

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{path}: rewritten (VT dependency removed)")


def rewrite_outputs(n):
    path = f"{BASE}/Ventilsteuerung_STG{n}/Outputs_STG{n}.SUB"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    for q in range(1, NUM_Q + 1):
        pp = f"{q:02d}"
        old_import = f'\t\t<Import declaration="FBs::const::DefaultPool::Button_Ausgang_STG{n}_Q{pp}"/>\n'
        assert content.count(old_import) == 1, (path, old_import)
        content = content.replace(old_import, "", 1)

        old_u16 = f'\n\t\t\t<Parameter Name="u16ObjId" Value="Button_Ausgang_STG{n}_Q{pp}"/>'
        assert content.count(old_u16) == 1, (path, old_u16)
        content = content.replace(old_u16, "", 1)

    content = content.replace('Type="Button_IXA_TO_logiBUS_QXA_BG_OPC"', 'Type="logiBUS_QXA_OPC"')

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{path}: rewritten (VT dependency removed)")


def main():
    import os
    os.makedirs(f"{BASE}/logiBUS_IXA_OPC", exist_ok=True)
    os.makedirs(f"{BASE}/logiBUS_QXA_OPC", exist_ok=True)

    with open(f"{BASE}/logiBUS_IXA_OPC/logiBUS_IXA_OPC.SUB", "w", encoding="utf-8", newline="") as f:
        f.write(DI_OPC_XML)
    print(f"{BASE}/logiBUS_IXA_OPC/logiBUS_IXA_OPC.SUB: written")

    with open(f"{BASE}/logiBUS_QXA_OPC/logiBUS_QXA_OPC.SUB", "w", encoding="utf-8", newline="") as f:
        f.write(DQ_OPC_XML)
    print(f"{BASE}/logiBUS_QXA_OPC/logiBUS_QXA_OPC.SUB: written")

    for n in NON_VT_MODULES:
        rewrite_inputs(n)
        rewrite_outputs(n)


if __name__ == "__main__":
    main()
