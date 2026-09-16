#!/usr/bin/env python3
"""Fix: OPC-UA IDs must be named GlobalConstants, not inline WSTRING literals
- per user correction 2026-08-25 ("STG2_Q01_READ das ist FALSCH, das muss
eine KONSTANTE sein"), pointing at the proven pattern in
C:\\git\\ms\\4diac_training1\\...\\Button_OPC_UA\\SubStrings.gcf.

Creates one SubStrings_STGn.gcf per module (n=1..5), living alongside that
module's Inputs_STGn.SUB / Outputs_STGn.SUB (same folder, same convention
as the reference file next to the SubApp types that use it). Each constant
is a real opc_ua PubSub address string
(opc_ua[ACTION;/Objects/STGn/DigitalInput|DigitalOutput/<ch>,1:s=STGn.<ch>]),
not just a bare label - namespaced per module per OPC_UA_VERNETZUNG.md
section 4 (STG1.Q01 vs STG3.Q01 must not collide).

Rewrites Inputs_STGn.SUB / Outputs_STGn.SUB / Subscribe_STG{2..5}.SUB (the
latter inside Ventilsteuerung_STG1/) to reference these constants by bare
name instead of inlining the WSTRING literal, with one <Import> per
constant used (matches this project's established per-constant import
style, e.g. logiBUS_DI::Input_I1).

Usage: python3 add_opcua_substring_constants.py
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
NUM_I = 8
NUM_Q = 12


def pkg(n):
    return f"FBs::Ventilsteuerung::Ventilsteuerung_STG{n}"


def substrings_gcf_xml(n):
    decls = []
    original = []
    for i in range(1, NUM_I + 1):
        name = f"STG{n}_I{i}_WRITE"
        val = f"opc_ua[WRITE;/Objects/STG{n}/DigitalInput/I{i},1:s=STG{n}.I{i}]"
        decls.append(f'\t\t<VarDeclaration Name="{name}" Type="WSTRING" InitialValue="&quot;{val}&quot;"/>\n')
        original.append(f'\t\t{name} : WSTRING := "{val}";\n')
    for q in range(1, NUM_Q + 1):
        pp = f"{q:02d}"
        rname = f"STG{n}_Q{pp}_READ"
        rval = f"opc_ua[READ;/Objects/STG{n}/DigitalOutput/Q{pp},1:s=STG{n}.Q{pp}]"
        wname = f"STG{n}_Q{pp}_WRITE"
        wval = f"opc_ua[WRITE;/Objects/STG{n}/DigitalOutput/Q{pp},1:s=STG{n}.Q{pp}]"
        decls.append(f'\t\t<VarDeclaration Name="{rname}" Type="WSTRING" InitialValue="&quot;{rval}&quot;"/>\n')
        decls.append(f'\t\t<VarDeclaration Name="{wname}" Type="WSTRING" InitialValue="&quot;{wval}&quot;"/>\n')
        original.append(f'\t\t{rname} : WSTRING := "{rval}";\n')
        original.append(f'\t\t{wname} : WSTRING := "{wval}";\n')

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<GlobalConstants Name="SubStrings_STG{n}" Comment="OPC-UA PubSub addresses for module STG{n}">\n'
        '\t<Identification Standard="61499-1">\n'
        '\t</Identification>\n'
        '\t<VersionInfo Organization="HR Agrartechnik GmbH" Version="1.0" Author="franz" Date="2026-08-25">\n'
        '\t</VersionInfo>\n'
        f'\t<CompilerInfo packageName="{pkg(n)}">\n'
        '\t</CompilerInfo>\n'
        '\t<GlobalConstants>\n'
        f'{"".join(decls)}'
        '\t</GlobalConstants>\n'
        f'\t<OriginalSource><![CDATA[PACKAGE {pkg(n)};\n'
        '\n'
        f'GLOBALCONSTANTS SubStrings_STG{n}\n'
        '\tVAR_GLOBAL CONSTANT\n'
        f'{"".join(original)}'
        '\tEND_VAR\n'
        'END_GLOBALCONSTANTS\n'
        ']]></OriginalSource>\n'
        '</GlobalConstants>\n'
    )


def write(path, content):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{path}: written")


def import_line(n, const_name):
    return f'\t\t<Import declaration="{pkg(n)}::SubStrings_STG{n}::{const_name}"/>\n'


def rewrite_inputs(n):
    path = f"{BASE}/Ventilsteuerung_STG{n}/Inputs_STG{n}.SUB"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    imports = "".join(import_line(n, f"STG{n}_I{i}_WRITE") for i in range(1, NUM_I + 1))
    content = re.sub(r'(\t<CompilerInfo>\n)', r'\1' + imports, content, count=1)

    for i in range(1, NUM_I + 1):
        old = f'<Parameter Name="ID_WRITE" Value="&quot;STG{n}_I{i}_WRITE&quot;"/>'
        new = f'<Parameter Name="ID_WRITE" Value="STG{n}_I{i}_WRITE"/>'
        assert old in content, f"{path}: {old!r} not found"
        content = content.replace(old, new)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{path}: rewritten (constant references)")


def rewrite_outputs(n):
    path = f"{BASE}/Ventilsteuerung_STG{n}/Outputs_STG{n}.SUB"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    names = []
    for q in range(1, NUM_Q + 1):
        pp = f"{q:02d}"
        names.append(f"STG{n}_Q{pp}_READ")
        names.append(f"STG{n}_Q{pp}_WRITE")
    imports = "".join(import_line(n, nm) for nm in names)
    content = re.sub(r'(\t<CompilerInfo>\n)', r'\1' + imports, content, count=1)

    for q in range(1, NUM_Q + 1):
        pp = f"{q:02d}"
        for kind in ("READ", "WRITE"):
            old = f'<Parameter Name="ID_{kind}" Value="&quot;STG{n}_Q{pp}_{kind}&quot;"/>'
            new = f'<Parameter Name="ID_{kind}" Value="STG{n}_Q{pp}_{kind}"/>'
            assert old in content, f"{path}: {old!r} not found"
            content = content.replace(old, new)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{path}: rewritten (constant references)")


def rewrite_remote_subscribe(remote_n):
    path = f"{BASE}/Ventilsteuerung_STG1/Subscribe_STG{remote_n}.SUB"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    names = [f"STG{remote_n}_Q{q:02d}_WRITE" for q in range(1, NUM_Q + 1)]
    names += [f"STG{remote_n}_I{i}_WRITE" for i in range(1, NUM_I + 1)]
    imports = "".join(import_line(remote_n, nm) for nm in names)
    content = re.sub(r'(\t<CompilerInfo>\n)', r'\1' + imports, content, count=1)

    for nm in names:
        old = f'<Parameter Name="ID" Value="&quot;{nm}&quot;"/>'
        new = f'<Parameter Name="ID" Value="{nm}"/>'
        assert old in content, f"{path}: {old!r} not found"
        content = content.replace(old, new)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{path}: rewritten (constant references)")


def main():
    for n in range(1, 6):
        write(f"{BASE}/Ventilsteuerung_STG{n}/SubStrings_STG{n}.gcf", substrings_gcf_xml(n))
    for n in range(1, 6):
        rewrite_inputs(n)
        rewrite_outputs(n)
    for remote_n in [2, 3, 4, 5]:
        rewrite_remote_subscribe(remote_n)


if __name__ == "__main__":
    main()
