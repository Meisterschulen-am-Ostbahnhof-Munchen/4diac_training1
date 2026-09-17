#!/usr/bin/env python3
"""Group each module's channels into Inputs_STGn / Outputs_STGn SubApp
Types, one level below Ventilsteuerung_STGn.sub - per user example
Ventilsteuerung_STG5/Inputs_STG5.SUB (built by hand 2026-08-25) and
Outputs_STG5.SUB (same). Elements are written in ascending numeric order
in the XML (user request 2026-08-25: "in der XML sortieren 1-2-3-4-usw."),
unlike the hand-built STG5 files (4diac IDE's own save order is
unsorted) - this script also re-sorts STG5's two files for consistency.

Each Inputs_STGn/Outputs_STGn instantiates the shared reusable types
(logiBUS_IXA_BG_OPC / Button_IXA_TO_logiBUS_QXA_BG_OPC) built in
refactor_dio_opcua_to_subapp_types.py - unchanged by this script.

Ventilsteuerung_STG1.sub keeps its IO_Diag SubApp and the 80 remote
AX_SUBSCRIBE_1 aggregation FBs untouched; only its per-channel SubApp list
is replaced by the two new Inputs_STG1/Outputs_STG1 references.

Usage: python3 split_inputs_outputs_per_module.py
"""
import re

import argparse
import os

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


def inputs_type_xml(n):
    imports = "".join(
        f'\t\t<Import declaration="logiBUS::io::DI::logiBUS_DI::Input_I{i}"/>\n'
        for i in range(1, NUM_I + 1)
    )
    subapps = ""
    y = 0
    for i in range(1, NUM_I + 1):
        subapps += (
            f'\t\t<SubApp Name="Input_I{i}" Type="logiBUS_IXA_BG_OPC" x="0" y="{y}">\n'
            f'\t\t\t<Parameter Name="Input" Value="Input_I{i}"/>\n'
            f'\t\t\t<Parameter Name="ID_WRITE" Value="&quot;STG{n}_I{i}_WRITE&quot;"/>\n'
            f'\t\t</SubApp>\n'
        )
        y += 600
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<SubAppType Name="Inputs_STG{n}" Comment="Subapplication Type">\n'
        '\t<Identification Standard="61499-2">\n'
        '\t</Identification>\n'
        '\t<VersionInfo Version="1.0" Author="franz" Date="2026-08-25">\n'
        '\t</VersionInfo>\n'
        '\t<CompilerInfo>\n'
        f'{imports}'
        '\t</CompilerInfo>\n'
        '\t<SubAppInterfaceList>\n'
        '\t</SubAppInterfaceList>\n'
        '\t<SubAppNetwork>\n'
        f'{subapps}'
        '\t</SubAppNetwork>\n'
        '</SubAppType>\n'
    )


def outputs_type_xml(n):
    # Import order matches the hand-built Outputs_STG5.SUB (Q1, Q10, Q11,
    # Q12, Q2, Q3, ... - lexicographic, as 4diac itself emits): keep that
    # convention for the imports, but sort the SubApp instances themselves.
    order = [1, 10, 11, 12] + list(range(2, 10))
    imports = "".join(
        f'\t\t<Import declaration="logiBUS::io::DQ::logiBUS_DO::Output_Q{q}"/>\n'
        for q in order
    )
    subapps = ""
    y = 0
    for q in range(1, NUM_Q + 1):
        pp = f"{q:02d}"
        subapps += (
            f'\t\t<SubApp Name="Output_Q{pp}" Type="Button_IXA_TO_logiBUS_QXA_BG_OPC" x="0" y="{y}">\n'
            f'\t\t\t<Parameter Name="Output" Value="Output_Q{q}"/>\n'
            f'\t\t\t<Parameter Name="ID_READ" Value="&quot;STG{n}_Q{pp}_READ&quot;"/>\n'
            f'\t\t\t<Parameter Name="ID_WRITE" Value="&quot;STG{n}_Q{pp}_WRITE&quot;"/>\n'
            f'\t\t</SubApp>\n'
        )
        y += 700
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<SubAppType Name="Outputs_STG{n}" Comment="Subapplication Type">\n'
        '\t<Identification Standard="61499-2">\n'
        '\t</Identification>\n'
        '\t<VersionInfo Version="1.0" Author="franz" Date="2026-08-25">\n'
        '\t</VersionInfo>\n'
        '\t<CompilerInfo>\n'
        f'{imports}'
        '\t</CompilerInfo>\n'
        '\t<SubAppInterfaceList>\n'
        '\t</SubAppInterfaceList>\n'
        '\t<SubAppNetwork>\n'
        f'{subapps}'
        '\t</SubAppNetwork>\n'
        '</SubAppType>\n'
    )


def write(path, content):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{path}: written")


def rewrite_top_stg1():
    path = f"{BASE}/Ventilsteuerung_STG1/Ventilsteuerung_STG1.sub"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    # Replace the 20 flat channel SubApp instances (Input_I1..I8,
    # Output_Q01..Q12) with the two grouping SubApp references. IO_Diag and
    # the 80 remote Subscribe_STGx_*_Remote FBs are untouched.
    pattern = re.compile(
        r'(\t\t<SubApp Name="Input_I1" Type="logiBUS_IXA_BG_OPC".*?</SubApp>\n)'
        r'(?:\t\t<SubApp Name="(?:Input_I\d|Output_Q\d\d)".*?</SubApp>\n)*',
        re.DOTALL,
    )
    matches = pattern.findall(content)
    assert len(matches) == 1, f"STG1: expected exactly one channel-SubApp run, found {len(matches)}"

    replacement = (
        '\t\t<SubApp Name="Inputs_STG1" Type="Inputs_STG1" x="0" y="5000">\n'
        '\t\t</SubApp>\n'
        '\t\t<SubApp Name="Outputs_STG1" Type="Outputs_STG1" x="1500" y="5000">\n'
        '\t\t</SubApp>\n'
    )
    new_content, count = pattern.subn(replacement, content)
    assert count == 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)
    print(f"{path}: rewritten (20 flat channel SubApps -> Inputs_STG1/Outputs_STG1)")


def rewrite_top_flat_module(n):
    path = f"{BASE}/Ventilsteuerung_STG{n}/Ventilsteuerung_STG{n}.sub"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    marker_start = "\t<SubAppNetwork>\n"
    marker_end = "\t</SubAppNetwork>\n"
    start = content.index(marker_start) + len(marker_start)
    end = content.index(marker_end, start)

    replacement = (
        f'\t\t<SubApp Name="Inputs_STG{n}" Type="Inputs_STG{n}" x="0" y="5000">\n'
        f'\t\t</SubApp>\n'
        f'\t\t<SubApp Name="Outputs_STG{n}" Type="Outputs_STG{n}" x="1500" y="5000">\n'
        f'\t\t</SubApp>\n'
    )
    new_content = content[:start] + replacement + content[end:]
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)
    print(f"{path}: rewritten (flat channel SubApps -> Inputs_STG{n}/Outputs_STG{n})")


def main():
    for n in MODULES:
        write(f"{BASE}/Ventilsteuerung_STG{n}/Inputs_STG{n}.SUB", inputs_type_xml(n))
        write(f"{BASE}/Ventilsteuerung_STG{n}/Outputs_STG{n}.SUB", outputs_type_xml(n))

    rewrite_top_stg1()
    for n in [2, 3, 4]:
        rewrite_top_flat_module(n)
    # STG5's top file already references Inputs_STG5/Outputs_STG5 (hand-built
    # by the user) - only its two type files were regenerated (sorted) above.


if __name__ == "__main__":
    main()
