#!/usr/bin/env python3
"""Close the ISOBUS gap for STG2-5 outputs (SZENARIEN_OPC_UA_IO.md
requirement 4): the VT button for a remote module's output already shows
its status colour (AX_SUBSCRIBE_BG_OPC), but nobody reads the button
PRESS and sends it on as a command to that module - so pressing
Button_Ausgang_STG2_Q01 on the (STG1-only) VT does nothing.

Per 4diac-documentation/src/communication/opcua.adoc's table, remote
WRITE uses a CLIENT function block (iec61499::net::CLIENT_1_0), not
AX_PUBLISH_1 (that's local-only - it only creates/writes a node in the
caller's OWN address space). CLIENT_1_0 confirmed from
C:\\git\\ms\\typelibrary\\net-3.0.0\\typelib\\CLIENT_1_0.fbt: EventInputs
INIT(QI,ID)/REQ(QI,SD_1), EventOutputs INITO/CNF, InputVars QI/ID/SD_1(ANY).

New reusable SubApp Type Button_IXA_TO_Remote_WRITE_BG_OPC (lives on
STG1, replaces AX_SUBSCRIBE_BG_OPC for outputs only - inputs have no
button to press, they keep the plain AX_SUBSCRIBE_BG_OPC):
  - Button_IXA reads the VT button press (u16ObjId - same object also
    used for the background colour, one VT object serves both roles,
    mirrors the local Button_IXA_TO_logiBUS_QXA_BG_OPC pattern).
  - AX_X_TO_BOOL converts the adapter's live press-state to a plain
    BOOL+event (non-latching per user decision 2026-08-25: pass the
    momentary press state straight through, no toggle/latch logic).
  - CLIENT_1_0 sends that BOOL as a remote WRITE to the target module's
    own STG{m}_Q{pp}_READ node (the same key its local
    Subscribe_STG{m}_Q{pp}_CMD, part of logiBUS_QXA_OPC, already listens
    on) on every change.
  - AX_SUBSCRIBE_1 + GreenWhiteBackground1_AX (same as AX_SUBSCRIBE_BG_OPC)
    independently show the module's actual confirmed state as colour.

Only the 60 output channels (Q1-12 x STG2-5) need this - the 40 input
channels stay on plain AX_SUBSCRIBE_BG_OPC (no button to press for an
input). Adds a new Remote-WRITE WSTRING constant (STG{m}_Q{pp}_WRITE_REMOTE,
opc_ua[WRITE;opc.tcp://<ip>:4840#;/Objects/STG{m}/DigitalOutput/Q{pp}
target node = the same STG{m}.Q{pp} node the target's local
Subscribe_STG{m}_Q{pp}_CMD already reads from - i.e. writes into
/Objects/STG{m}/DigitalOutput/Q{pp} same identifier as the READ key)
per output channel, in the existing RemoteSubStrings.gcf.

Usage: python3 build_remote_write_button_type.py
"""
import re

BASE = "4diacIDE-workspace/test/FBs/Ventilsteuerung"
STG1_DIR = f"{BASE}/Ventilsteuerung_STG1"
NUM_Q = 12
REMOTE_MODULES = [2, 3, 4, 5]
OPC_UA_PORT = 4840
STG_IP = {n: f"192.168.1.1{n}" for n in [1, 2, 3, 4, 5]}

TYPE_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<SubAppType Name="Button_IXA_TO_Remote_WRITE_BG_OPC" Comment="VT-Button lesen + Remote-OPC-UA-Write an Zielmodul + VT-Hintergrundfarbe aus Remote-Subscribe (generisch, ein Kanal, fuer Ausgaenge auf Modulen ohne eigene VT-Anbindung)">\n'
    '\t<Identification Standard="61499-2">\n'
    '\t</Identification>\n'
    '\t<VersionInfo Version="1.0" Author="franz" Date="2026-08-27">\n'
    '\t</VersionInfo>\n'
    '\t<CompilerInfo>\n'
    '\t\t<Import declaration="isobus::UT::Q::const::IDs::ID_NULL"/>\n'
    '\t</CompilerInfo>\n'
    '\t<SubAppInterfaceList>\n'
    '\t\t<InputVars>\n'
    '\t\t\t<VarDeclaration Name="u16ObjId" Type="UINT" Comment="Object ID Button/Hintergrund (VT)" InitialValue="ID_NULL"/>\n'
    '\t\t\t<VarDeclaration Name="ID_SUBSCRIBE" Type="WSTRING" Comment="Remote-Subscribe-Adresse (Status/Farbe, ACTION=SUBSCRIBE)"/>\n'
    '\t\t\t<VarDeclaration Name="ID_WRITE_REMOTE" Type="WSTRING" Comment="Remote-Write-Adresse zum Zielmodul (Befehl, ACTION=WRITE, CLIENT)"/>\n'
    '\t\t</InputVars>\n'
    '\t</SubAppInterfaceList>\n'
    '\t<SubAppNetwork>\n'
    '\t\t<FB Name="Button_IXA" Type="isobus::UT::io::Button::Button_IXA" x="0" y="0">\n'
    '\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
    '\t\t</FB>\n'
    '\t\t<FB Name="AX_X_TO_BOOL" Type="adapter::conversion::unidirectional::AX_X_TO_BOOL" x="1000" y="0">\n'
    '\t\t</FB>\n'
    '\t\t<FB Name="CLIENT_1_0" Type="iec61499::net::CLIENT_1_0" x="2000" y="0">\n'
    '\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
    '\t\t</FB>\n'
    '\t\t<FB Name="AX_SUBSCRIBE_1" Type="adapter::net::AX_SUBSCRIBE_1" x="0" y="1000">\n'
    '\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
    '\t\t</FB>\n'
    '\t\t<SubApp Name="GreenWhiteBackground1_AX" Type="GreenWhiteBackground1_AX" x="1500" y="1000">\n'
    '\t\t</SubApp>\n'
    '\t\t<EventConnections>\n'
    '\t\t\t<Connection Source="AX_X_TO_BOOL.CNF" Destination="CLIENT_1_0.REQ"/>\n'
    '\t\t</EventConnections>\n'
    '\t\t<DataConnections>\n'
    '\t\t\t<Connection Source="u16ObjId" Destination="Button_IXA.u16ObjId">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Connection>\n'
    '\t\t\t<Connection Source="u16ObjId" Destination="GreenWhiteBackground1_AX.u16ObjId">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Connection>\n'
    '\t\t\t<Connection Source="ID_SUBSCRIBE" Destination="AX_SUBSCRIBE_1.ID">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Connection>\n'
    '\t\t\t<Connection Source="ID_WRITE_REMOTE" Destination="CLIENT_1_0.ID">\n'
    '\t\t\t\t<Attribute Name="Visible" Value="false"/>\n'
    '\t\t\t</Connection>\n'
    '\t\t\t<Connection Source="AX_X_TO_BOOL.IN" Destination="CLIENT_1_0.SD_1"/>\n'
    '\t\t</DataConnections>\n'
    '\t\t<AdapterConnections>\n'
    '\t\t\t<Connection Source="Button_IXA.IN" Destination="AX_X_TO_BOOL.AX_IN"/>\n'
    '\t\t\t<Connection Source="AX_SUBSCRIBE_1.OUT" Destination="GreenWhiteBackground1_AX.DI1"/>\n'
    '\t\t</AdapterConnections>\n'
    '\t</SubAppNetwork>\n'
    '</SubAppType>\n'
)


def endpoint(m):
    return f"opc.tcp://{STG_IP[m]}:{OPC_UA_PORT}#"


def add_remote_write_constants():
    """Append STG{m}_Q{pp}_WRITE_REMOTE constants to the existing
    RemoteSubStrings.gcf (same file the *_REMOTE subscribe constants
    already live in)."""
    path = f"{STG1_DIR}/RemoteSubStrings.gcf"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    decls = []
    original = []
    for m in REMOTE_MODULES:
        ep = endpoint(m)
        for q in range(1, NUM_Q + 1):
            pp = f"{q:02d}"
            name = f"STG{m}_Q{pp}_WRITE_REMOTE"
            # Writes into the SAME node the target's own local
            # Subscribe_STG{m}_Q{pp}_CMD (logiBUS_QXA_OPC) reads from -
            # i.e. the STG{m}_Q{pp}_READ key, just approached remotely.
            val = f"opc_ua[WRITE;{ep};/Objects/STG{m}/DigitalOutput/Q{pp},1:s=STG{m}.Q{pp}]"
            decls.append(f'\t\t<VarDeclaration Name="{name}" Type="WSTRING" InitialValue="&quot;{val}&quot;"/>\n')
            original.append(f'\t\t{name} : WSTRING := "{val}";\n')

    decls_block = "".join(decls)
    original_block = "".join(original)

    marker = "\t</GlobalConstants>\n"
    assert content.count(marker) == 1
    content = content.replace(marker, decls_block + marker, 1)

    end_marker = "\tEND_VAR\n"
    assert content.count(end_marker) == 1
    content = content.replace(end_marker, original_block + end_marker, 1)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{path}: added {len(decls)} *_WRITE_REMOTE constants")


def rewrite_subscribe_outputs(m):
    """Switch the 12 output channels in Subscribe_STG{m}.SUB from
    AX_SUBSCRIBE_BG_OPC to Button_IXA_TO_Remote_WRITE_BG_OPC. Input
    channels (I1-8) are untouched (no button to press for an input)."""
    path = f"{STG1_DIR}/Subscribe_STG{m}.SUB"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    for q in range(1, NUM_Q + 1):
        pp = f"{q:02d}"
        name = f"Subscribe_STG{m}_Q{pp}_Remote"
        old_block = (
            f'\t\t<SubApp Name="{name}" Type="AX_SUBSCRIBE_BG_OPC"'
        )
        assert old_block in content, f"{path}: {old_block!r} not found"
        # Only swap the Type on the opening tag; leave x/y untouched.
        content = re.sub(
            re.escape(f'<SubApp Name="{name}" Type="AX_SUBSCRIBE_BG_OPC"'),
            f'<SubApp Name="{name}" Type="Button_IXA_TO_Remote_WRITE_BG_OPC"',
            content,
            count=1,
        )
        old_params = (
            f'\t\t\t<Parameter Name="ID" Value="STG{m}_Q{pp}_REMOTE"/>\n'
            f'\t\t\t<Parameter Name="u16ObjId" Value="Button_Ausgang_STG{m}_Q{pp}"/>\n'
        )
        assert content.count(old_params) == 1, f"{path}: params for {name} not found as expected"
        new_params = (
            f'\t\t\t<Parameter Name="ID_SUBSCRIBE" Value="STG{m}_Q{pp}_REMOTE"/>\n'
            f'\t\t\t<Parameter Name="ID_WRITE_REMOTE" Value="STG{m}_Q{pp}_WRITE_REMOTE"/>\n'
            f'\t\t\t<Parameter Name="u16ObjId" Value="Button_Ausgang_STG{m}_Q{pp}"/>\n'
        )
        content = content.replace(old_params, new_params, 1)

        # Add the import for the new WRITE_REMOTE constant, next to the
        # existing REMOTE import for the same channel.
        old_import = f'\t\t<Import declaration="FBs::Ventilsteuerung::Ventilsteuerung_STG1::RemoteSubStrings::STG{m}_Q{pp}_REMOTE"/>\n'
        assert content.count(old_import) == 1
        new_import = old_import + f'\t\t<Import declaration="FBs::Ventilsteuerung::Ventilsteuerung_STG1::RemoteSubStrings::STG{m}_Q{pp}_WRITE_REMOTE"/>\n'
        content = content.replace(old_import, new_import, 1)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{path}: {NUM_Q} output channels switched to Button_IXA_TO_Remote_WRITE_BG_OPC")


def main():
    import os
    os.makedirs(f"{BASE}/Button_IXA_TO_Remote_WRITE_BG_OPC", exist_ok=True)
    with open(f"{BASE}/Button_IXA_TO_Remote_WRITE_BG_OPC/Button_IXA_TO_Remote_WRITE_BG_OPC.SUB", "w", encoding="utf-8", newline="") as f:
        f.write(TYPE_XML)
    print("Button_IXA_TO_Remote_WRITE_BG_OPC.SUB: written")

    add_remote_write_constants()

    for m in REMOTE_MODULES:
        rewrite_subscribe_outputs(m)


if __name__ == "__main__":
    main()
