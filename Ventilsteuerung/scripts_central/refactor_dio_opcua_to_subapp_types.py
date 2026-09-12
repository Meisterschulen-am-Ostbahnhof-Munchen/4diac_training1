#!/usr/bin/env python3
"""Replace the flat, per-channel FB repetition from build_dio_opcua_wiring.py
with two reusable, parametrized SubApp Types, instantiated once per channel -
per user feedback 2026-08-25 ("Gleichartige Sachen mit Subapps loesen").

Mirrors the proven pattern in
C:\\git\\ms\\4diac_training1\\...\\test_AX\\Type Library\\MyLib\\sys\\
logiBUS_IXA_BG_OPC.SUB / Button_IXA_TO_logiBUS_QXA_BG_OPC.SUB, including the
Button_IXA + GreenWhiteBackground1_AX (VT press/colour feedback) parts the
user explicitly asked to keep ("MIT Button Background"). u16ObjId defaults to
ID_NULL (safe no-op) - no real VT Button/colour objects exist yet in
DefaultPool.jop for these channels; wiring real Object IDs in is a separate,
later step (user decision 2026-08-25).

Creates 3 new reusable SubApp Types (own subfolder each, matching the
IO_Diag/IO_STG2 convention already started by hand in this project):
  - GreenWhiteBackground1_AX  (vendored unchanged from 4diac_training1)
  - logiBUS_IXA_BG_OPC        (DI channel: VT background + OPC-UA publish)
  - Button_IXA_TO_logiBUS_QXA_BG_OPC (DQ channel: VT button+background,
    OPC-UA subscribe(write)+publish(read))

Rewrites Ventilsteuerung_STG{1..5}.sub to instantiate these 8x/12x per
module instead of the flat FB repetition. STG1 keeps its 80 remote
AX_SUBSCRIBE_1 aggregation instances unchanged (already atomic FB reuse,
nothing to wrap). Also removes the now-obsolete IO_STG2.SUB (its content is
superseded by the reusable types).

Usage: python3 refactor_dio_opcua_to_subapp_types.py
"""
import os
import re

import argparse

_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument(
    "-b", "--base", dest="base", required=True,
    help="FBs/Ventilsteuerung folder for this project, relative to the "
         "current working directory - e.g. "
         "4diacIDE-workspace/test/FBs/Ventilsteuerung for Krauternter",
)
_args, _ = _parser.parse_known_args()
BASE = _args.base
MODULES = [1, 2, 3, 4, 5]
NUM_I = 8
NUM_Q = 12

GREENWHITE_SUB = '''<?xml version="1.0" encoding="UTF-8"?>
<SubAppType Name="GreenWhiteBackground1_AX" Comment="Hintergrundfarbe (TRUE -&gt; Gr\u00fcn, FALSE -&gt; Wei\u00df) f\u00fcr 1 Objekt (AX-Adapter)">
\t<Identification Standard="61499-2" Description="Copyright (c) 2022 HR Agrartechnik GmbH  &#10; &#10;This program and the accompanying materials are made  &#10;available under the terms of the Eclipse Public License 2.0  &#10;which is available at https://www.eclipse.org/legal/epl-2.0/  &#10; &#10;SPDX-License-Identifier: EPL-2.0">
\t</Identification>
\t<VersionInfo Organization="HR Agrartechnik GmbH" Version="1.0" Author="Franz H\u00f6pfinger" Date="2022-11-10">
\t</VersionInfo>
\t<CompilerInfo>
\t\t<Import declaration="isobus::UT::Q::const::IDs::ID_NULL"/>
\t\t<Import declaration="isobus::UT::Q::const::colours::COLOR_GREEN"/>
\t\t<Import declaration="isobus::UT::Q::const::colours::COLOR_WHITE"/>
\t</CompilerInfo>
\t<SubAppInterfaceList>
\t\t<SubAppEventOutputs>
\t\t\t<SubAppEvent Name="CNF" Type="Event" Comment="Execution Confirmation">
\t\t\t</SubAppEvent>
\t\t</SubAppEventOutputs>
\t\t<InputVars>
\t\t\t<VarDeclaration Name="u16ObjId" Type="UINT" Comment="Object ID Softkey/Button" InitialValue="ID_NULL">
\t\t\t</VarDeclaration>
\t\t</InputVars>
\t\t<OutputVars>
\t\t\t<VarDeclaration Name="STATUS_1" Type="STRING" Comment="Service Status">
\t\t\t</VarDeclaration>
\t\t\t<VarDeclaration Name="u8OldColour_1" Type="USINT" Comment="Old value of ID">
\t\t\t</VarDeclaration>
\t\t\t<VarDeclaration Name="result_1" Type="INT" Comment="retval see description">
\t\t\t</VarDeclaration>
\t\t</OutputVars>
\t\t<Sockets>
\t\t\t<AdapterDeclaration Name="DI1" Type="adapter::types::unidirectional::AX" Comment="Selector"/>
\t\t</Sockets>
\t</SubAppInterfaceList>
\t<SubAppNetwork>
\t\t<FB Name="Q_BackgroundColour" Type="isobus::UT::Q::Q_BackgroundColour" x="-3106.67" y="706.67">
\t\t</FB>
\t\t<FB Name="AX_SEL" Type="adapter::iec61131::selection::AX_SEL" x="-4306.67" y="2040">
\t\t\t<Parameter Name="IN0" Value="COLOR_WHITE"/>
\t\t\t<Parameter Name="IN1" Value="COLOR_GREEN"/>
\t\t</FB>
\t\t<EventConnections>
\t\t\t<Connection Source="Q_BackgroundColour.CNF" Destination="CNF" dx1="960"/>
\t\t\t<Connection Source="AX_SEL.CNF" Destination="Q_BackgroundColour.REQ" dx1="213.33"/>
\t\t</EventConnections>
\t\t<DataConnections>
\t\t\t<Connection Source="u16ObjId" Destination="Q_BackgroundColour.u16ObjId" dx1="1126.67"/>
\t\t\t<Connection Source="Q_BackgroundColour.s16result" Destination="result_1" dx1="926.67"/>
\t\t\t<Connection Source="Q_BackgroundColour.u8OldColour" Destination="u8OldColour_1" dx1="960"/>
\t\t\t<Connection Source="Q_BackgroundColour.STATUS" Destination="STATUS_1" dx1="946.67"/>
\t\t\t<Connection Source="AX_SEL.OUT" Destination="Q_BackgroundColour.u8Colour" dx1="406.67"/>
\t\t</DataConnections>
\t\t<AdapterConnections>
\t\t\t<Connection Source="DI1" Destination="AX_SEL.G" dx1="660"/>
\t\t</AdapterConnections>
\t</SubAppNetwork>
</SubAppType>
'''

DI_OPC_SUB = '''<?xml version="1.0" encoding="UTF-8"?>
<SubAppType Name="logiBUS_IXA_BG_OPC" Comment="logiBUS DI Kanal: VT-Hintergrundfarbe + OPC-UA-Publish (generisch, ein Kanal)">
\t<Identification Standard="61499-2">
\t</Identification>
\t<VersionInfo Version="1.0" Author="franz" Date="2026-08-25">
\t</VersionInfo>
\t<CompilerInfo>
\t\t<Import declaration="isobus::UT::Q::const::IDs::ID_NULL"/>
\t\t<Import declaration="logiBUS::io::DI::logiBUS_DI::Invalid"/>
\t</CompilerInfo>
\t<SubAppInterfaceList>
\t\t<InputVars>
\t\t\t<VarDeclaration Name="u16ObjId" Type="UINT" Comment="Object ID Hintergrund-Rechteck (VT), ID_NULL = noch kein VT-Objekt" InitialValue="ID_NULL"/>
\t\t\t<VarDeclaration Name="Input" Type="logiBUS::io::DI::logiBUS_DI_S" Comment="Identify the Input Input_I1..I8" InitialValue="logiBUS_DI::Invalid"/>
\t\t\t<VarDeclaration Name="ID_WRITE" Type="WSTRING" Comment="OPC-UA Publish-Key (lesbar)"/>
\t\t</InputVars>
\t</SubAppInterfaceList>
\t<SubAppNetwork>
\t\t<FB Name="logiBUS_IXA" Type="logiBUS::io::DI::logiBUS_IXA" x="-4600" y="-1000">
\t\t\t<Parameter Name="QI" Value="TRUE"/>
\t\t\t<Parameter Name="PARAMS" Value="">
\t\t\t\t<Attribute Name="Visible" Value="false"/>
\t\t\t</Parameter>
\t\t</FB>
\t\t<SubApp Name="GreenWhiteBackground1_AX" Type="GreenWhiteBackground1_AX" x="-2200" y="-1000">
\t\t</SubApp>
\t\t<FB Name="AX_PUBLISH_1" Type="adapter::net::AX_PUBLISH_1" x="-1700" y="100">
\t\t\t<Parameter Name="QI" Value="TRUE"/>
\t\t</FB>
\t\t<FB Name="AX_SPLIT_2" Type="adapter::events::unidirectional::AX_SPLIT_2" x="-3300" y="0">
\t\t</FB>
\t\t<DataConnections>
\t\t\t<Connection Source="Input" Destination="logiBUS_IXA.Input" dx1="2926.67">
\t\t\t\t<Attribute Name="Visible" Value="false"/>
\t\t\t</Connection>
\t\t\t<Connection Source="u16ObjId" Destination="GreenWhiteBackground1_AX.u16ObjId" dx1="2680">
\t\t\t\t<Attribute Name="Visible" Value="false"/>
\t\t\t</Connection>
\t\t\t<Connection Source="ID_WRITE" Destination="AX_PUBLISH_1.ID" dx1="4280">
\t\t\t\t<Attribute Name="Visible" Value="false"/>
\t\t\t</Connection>
\t\t</DataConnections>
\t\t<AdapterConnections>
\t\t\t<Connection Source="logiBUS_IXA.IN" Destination="AX_SPLIT_2.IN" dx1="420"/>
\t\t\t<Connection Source="AX_SPLIT_2.OUT1" Destination="GreenWhiteBackground1_AX.DI1" dx1="173.33"/>
\t\t\t<Connection Source="AX_SPLIT_2.OUT2" Destination="AX_PUBLISH_1.IN" dx1="153.33"/>
\t\t</AdapterConnections>
\t</SubAppNetwork>
</SubAppType>
'''

DQ_OPC_SUB = '''<?xml version="1.0" encoding="UTF-8"?>
<SubAppType Name="Button_IXA_TO_logiBUS_QXA_BG_OPC" Comment="Button IXA -&gt; logiBUS QXA + Hintergrundfarbe, plus OPC-UA Read/Write (generisch, ein Kanal)">
\t<Identification Standard="61499-2">
\t</Identification>
\t<VersionInfo Version="1.0" Author="franz" Date="2026-08-25">
\t</VersionInfo>
\t<CompilerInfo>
\t\t<Import declaration="isobus::UT::Q::const::IDs::ID_NULL"/>
\t\t<Import declaration="logiBUS::io::DQ::logiBUS_DO::Invalid"/>
\t</CompilerInfo>
\t<SubAppInterfaceList>
\t\t<InputVars>
\t\t\t<VarDeclaration Name="u16ObjId" Type="UINT" Comment="Object ID Button/Hintergrund (VT), ID_NULL = noch kein VT-Objekt" InitialValue="ID_NULL"/>
\t\t\t<VarDeclaration Name="Output" Type="logiBUS::io::DQ::logiBUS_DO_S" Comment="Identify the Output Output_Q1..Q12" InitialValue="logiBUS_DO::Invalid"/>
\t\t\t<VarDeclaration Name="ID_READ" Type="WSTRING" Comment="OPC-UA Subscribe-Key (schreibbar)"/>
\t\t\t<VarDeclaration Name="ID_WRITE" Type="WSTRING" Comment="OPC-UA Publish-Key (lesbar)"/>
\t\t</InputVars>
\t</SubAppInterfaceList>
\t<SubAppNetwork>
\t\t<FB Name="logiBUS_QXA" Type="logiBUS::io::DQ::logiBUS_QXA" x="1700" y="-2200">
\t\t\t<Parameter Name="QI" Value="TRUE"/>
\t\t\t<Parameter Name="PARAMS" Value="">
\t\t\t\t<Attribute Name="Visible" Value="false"/>
\t\t\t</Parameter>
\t\t</FB>
\t\t<FB Name="Button_IXA" Type="isobus::UT::io::Button::Button_IXA" x="-7400" y="-1300">
\t\t\t<Parameter Name="QI" Value="TRUE"/>
\t\t</FB>
\t\t<FB Name="AX_SPLIT_3" Type="adapter::events::unidirectional::AX_SPLIT_3" x="-800" y="-1300">
\t\t</FB>
\t\t<SubApp Name="GreenWhiteBackground1_AX" Type="GreenWhiteBackground1_AX" x="1400" y="-1100">
\t\t</SubApp>
\t\t<FB Name="AX_SUBSCRIBE_1" Type="adapter::net::AX_SUBSCRIBE_1" x="-7300" y="-2200">
\t\t\t<Parameter Name="QI" Value="TRUE"/>
\t\t</FB>
\t\t<FB Name="AX_PUBLISH_1" Type="adapter::net::AX_PUBLISH_1" x="2000" y="-200">
\t\t\t<Parameter Name="QI" Value="TRUE"/>
\t\t</FB>
\t\t<FB Name="AX_RF_TRIG_BT" Type="adapter::events::unidirectional::AX_RF_TRIG" x="-4600" y="-1000">
\t\t</FB>
\t\t<FB Name="AX_SR" Type="adapter::events::unidirectional::AX_SR" x="-2900" y="-1600">
\t\t</FB>
\t\t<FB Name="AX_RF_TRIG_OPC" Type="adapter::events::unidirectional::AX_RF_TRIG" x="-4600" y="-1600">
\t\t</FB>
\t\t<EventConnections>
\t\t\t<Connection Source="AX_RF_TRIG_OPC.ER" Destination="AX_SR.S"/>
\t\t\t<Connection Source="AX_RF_TRIG_BT.ER" Destination="AX_SR.S" dx1="380"/>
\t\t\t<Connection Source="AX_RF_TRIG_OPC.EF" Destination="AX_SR.R"/>
\t\t\t<Connection Source="AX_RF_TRIG_BT.EF" Destination="AX_SR.R" dx1="546.67"/>
\t\t</EventConnections>
\t\t<DataConnections>
\t\t\t<Connection Source="u16ObjId" Destination="Button_IXA.u16ObjId" dx1="1546.67">
\t\t\t\t<Attribute Name="Visible" Value="false"/>
\t\t\t</Connection>
\t\t\t<Connection Source="Output" Destination="logiBUS_QXA.Output" dx1="4113.33">
\t\t\t\t<Attribute Name="Visible" Value="false"/>
\t\t\t</Connection>
\t\t\t<Connection Source="u16ObjId" Destination="GreenWhiteBackground1_AX.u16ObjId" dx1="3126.67">
\t\t\t\t<Attribute Name="Visible" Value="false"/>
\t\t\t</Connection>
\t\t\t<Connection Source="ID_READ" Destination="AX_SUBSCRIBE_1.ID" dx1="760">
\t\t\t\t<Attribute Name="Visible" Value="false"/>
\t\t\t</Connection>
\t\t\t<Connection Source="ID_WRITE" Destination="AX_PUBLISH_1.ID" dx1="5026.67">
\t\t\t\t<Attribute Name="Visible" Value="false"/>
\t\t\t</Connection>
\t\t</DataConnections>
\t\t<AdapterConnections>
\t\t\t<Connection Source="Button_IXA.IN" Destination="AX_RF_TRIG_BT.QI" dx1="1580"/>
\t\t\t<Connection Source="AX_SPLIT_3.OUT1" Destination="logiBUS_QXA.OUT" dx1="273.33"/>
\t\t\t<Connection Source="AX_SPLIT_3.OUT2" Destination="GreenWhiteBackground1_AX.DI1" dx1="800"/>
\t\t\t<Connection Source="AX_SR.Q" Destination="AX_SPLIT_3.IN" dx1="840"/>
\t\t\t<Connection Source="AX_SUBSCRIBE_1.OUT" Destination="AX_RF_TRIG_OPC.QI" dx1="1580"/>
\t\t\t<Connection Source="AX_SPLIT_3.OUT3" Destination="AX_PUBLISH_1.IN" dx1="460"/>
\t\t</AdapterConnections>
\t</SubAppNetwork>
</SubAppType>
'''


def write_type_file(name, content):
    folder = f"{BASE}/{name}"
    os.makedirs(folder, exist_ok=True)
    path = f"{folder}/{name}.SUB"
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{path}: written")


def channel_instances(n):
    parts = []
    y = 5000
    for i in range(1, NUM_I + 1):
        parts.append(
            f'\t\t<SubApp Name="Input_I{i}" Type="logiBUS_IXA_BG_OPC" x="200" y="{y}">\n'
            f'\t\t\t<Parameter Name="Input" Value="Input_I{i}"/>\n'
            f'\t\t\t<Parameter Name="ID_WRITE" Value="&quot;STG{n}_I{i}_WRITE&quot;"/>\n'
            f'\t\t</SubApp>\n'
        )
        y += 300
    y = 5000
    for q in range(1, NUM_Q + 1):
        pp = f"{q:02d}"
        parts.append(
            f'\t\t<SubApp Name="Output_Q{pp}" Type="Button_IXA_TO_logiBUS_QXA_BG_OPC" x="1500" y="{y}">\n'
            f'\t\t\t<Parameter Name="Output" Value="Output_Q{q}"/>\n'
            f'\t\t\t<Parameter Name="ID_READ" Value="&quot;STG{n}_Q{pp}_READ&quot;"/>\n'
            f'\t\t\t<Parameter Name="ID_WRITE" Value="&quot;STG{n}_Q{pp}_WRITE&quot;"/>\n'
            f'\t\t</SubApp>\n'
        )
        y += 300
    return "".join(parts)


def remote_subscribe_instances():
    # Unchanged from the first pass: a single reusable FB called repeatedly
    # needs no wrapper type of its own.
    parts = []
    for remote_n in [2, 3, 4, 5]:
        x = 7000 + (remote_n - 2) * 1200
        y = 5000
        for q in range(1, NUM_Q + 1):
            name = f"Subscribe_STG{remote_n}_Q{q:02d}_Remote"
            key = f"STG{remote_n}_Q{q:02d}_WRITE"
            parts.append(
                f'\t\t<FB Name="{name}" Type="adapter::net::AX_SUBSCRIBE_1" x="{x}" y="{y}">\n'
                f'\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
                f'\t\t\t<Parameter Name="ID" Value="&quot;{key}&quot;"/>\n'
                f'\t\t</FB>\n'
            )
            y += 250
        for i in range(1, NUM_I + 1):
            name = f"Subscribe_STG{remote_n}_I{i}_Remote"
            key = f"STG{remote_n}_I{i}_WRITE"
            parts.append(
                f'\t\t<FB Name="{name}" Type="adapter::net::AX_SUBSCRIBE_1" x="{x}" y="{y}">\n'
                f'\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
                f'\t\t\t<Parameter Name="ID" Value="&quot;{key}&quot;"/>\n'
                f'\t\t</FB>\n'
            )
            y += 250
    return "".join(parts)


def rewrite_stg1():
    path = f"{BASE}/Ventilsteuerung_STG1/Ventilsteuerung_STG1.sub"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    new_block = channel_instances(1) + remote_subscribe_instances()

    pattern = re.compile(
        r'\t\t<SubApp Name="SubApp" x="200" y="5000">\n.*?\n\t\t</SubApp>\n',
        re.DOTALL,
    )
    count = len(pattern.findall(content))
    assert count == 1, f"STG1: expected exactly one anonymous grouping SubApp, found {count}"
    new_content = pattern.sub(new_block, content)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)
    print(f"{path}: rewritten (anonymous grouping SubApp replaced)")


def rewrite_stg2():
    path = f"{BASE}/Ventilsteuerung_STG2/Ventilsteuerung_STG2.sub"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    new_block = channel_instances(2)

    marker = '\t\t<SubApp Name="IO_STG2" Type="IO_STG2" x="200" y="5000">\n\t\t</SubApp>\n'
    assert content.count(marker) == 1, "STG2: IO_STG2 SubApp reference not found as expected"
    new_content = content.replace(marker, new_block)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)
    print(f"{path}: rewritten (IO_STG2 reference replaced)")

    io_stg2 = f"{BASE}/Ventilsteuerung_STG2/IO_STG2.SUB"
    if os.path.exists(io_stg2):
        os.remove(io_stg2)
        print(f"{io_stg2}: removed (superseded by reusable types)")


def rewrite_flat_module(n):
    path = f"{BASE}/Ventilsteuerung_STG{n}/Ventilsteuerung_STG{n}.sub"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    new_block = channel_instances(n)

    marker_start = "\t<SubAppNetwork>\n"
    marker_end = "\t</SubAppNetwork>\n"
    start = content.index(marker_start) + len(marker_start)
    end = content.index(marker_end, start)
    new_content = content[:start] + new_block + content[end:]

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)
    print(f"{path}: rewritten (flat FB content replaced)")


def main():
    write_type_file("GreenWhiteBackground1_AX", GREENWHITE_SUB)
    write_type_file("logiBUS_IXA_BG_OPC", DI_OPC_SUB)
    write_type_file("Button_IXA_TO_logiBUS_QXA_BG_OPC", DQ_OPC_SUB)

    rewrite_stg1()
    rewrite_stg2()
    for n in [3, 4, 5]:
        rewrite_flat_module(n)


if __name__ == "__main__":
    main()
