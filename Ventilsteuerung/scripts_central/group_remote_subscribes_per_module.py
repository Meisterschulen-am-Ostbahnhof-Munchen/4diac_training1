#!/usr/bin/env python3
"""Group STG1's 80 flat remote-aggregation AX_SUBSCRIBE_1 FBs into 4 SubApp
Types, one per remote module (Subscribe_STG2..Subscribe_STG5) - per user
request 2026-08-25 ("den Subscribe_STG2 in eine Subapp, 3, 4, 5 je eine
Subapp"). Same grouping idea as Inputs_STGn/Outputs_STGn, applied to the
STG1-only aggregation FBs from refactor_dio_opcua_to_subapp_types.py.

Each Subscribe_STGn type lives under Ventilsteuerung_STG1/ (STG1-specific,
not reused elsewhere) and contains that remote module's 12 Q + 8 I
AX_SUBSCRIBE_1 instances, sorted numerically. No CompilerInfo imports
needed (ID is a WSTRING literal, no bare constant referenced).

Usage: python3 group_remote_subscribes_per_module.py
"""
import re

BASE = "4diacIDE-workspace/test/FBs/Ventilsteuerung"
STG1_DIR = f"{BASE}/Ventilsteuerung_STG1"
NUM_I = 8
NUM_Q = 12


def subscribe_type_xml(remote_n):
    subapps = ""
    y = 0
    for q in range(1, NUM_Q + 1):
        pp = f"{q:02d}"
        name = f"Subscribe_STG{remote_n}_Q{pp}_Remote"
        key = f"STG{remote_n}_Q{pp}_WRITE"
        subapps += (
            f'\t\t<FB Name="{name}" Type="adapter::net::AX_SUBSCRIBE_1" x="0" y="{y}">\n'
            f'\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
            f'\t\t\t<Parameter Name="ID" Value="&quot;{key}&quot;"/>\n'
            f'\t\t</FB>\n'
        )
        y += 800
    for i in range(1, NUM_I + 1):
        name = f"Subscribe_STG{remote_n}_I{i}_Remote"
        key = f"STG{remote_n}_I{i}_WRITE"
        subapps += (
            f'\t\t<FB Name="{name}" Type="adapter::net::AX_SUBSCRIBE_1" x="0" y="{y}">\n'
            f'\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
            f'\t\t\t<Parameter Name="ID" Value="&quot;{key}&quot;"/>\n'
            f'\t\t</FB>\n'
        )
        y += 800
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<SubAppType Name="Subscribe_STG{remote_n}" Comment="Subapplication Type">\n'
        '\t<Identification Standard="61499-2">\n'
        '\t</Identification>\n'
        '\t<VersionInfo Version="1.0" Author="franz" Date="2026-08-25">\n'
        '\t</VersionInfo>\n'
        '\t<CompilerInfo>\n'
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
    path = f"{STG1_DIR}/Ventilsteuerung_STG1.sub"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    pattern = re.compile(
        r'(\t\t<FB Name="Subscribe_STG2_Q01_Remote".*?</FB>\n)'
        r'(?:\t\t<FB Name="Subscribe_STG[2-5]_[QI]\d+_Remote".*?</FB>\n)*',
        re.DOTALL,
    )
    matches = pattern.findall(content)
    assert len(matches) == 1, f"expected exactly one remote-FB run, found {len(matches)}"

    replacement = ""
    y = 600
    for remote_n in [2, 3, 4, 5]:
        replacement += (
            f'\t\t<SubApp Name="Subscribe_STG{remote_n}" Type="Subscribe_STG{remote_n}" x="0" y="{y}">\n'
            f'\t\t</SubApp>\n'
        )
        y += 300

    new_content, count = pattern.subn(replacement, content)
    assert count == 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)
    print(f"{path}: rewritten (80 flat remote FBs -> 4 Subscribe_STGn SubApps)")


def main():
    for remote_n in [2, 3, 4, 5]:
        write(f"{STG1_DIR}/Subscribe_STG{remote_n}.SUB", subscribe_type_xml(remote_n))
    rewrite_top_stg1()


if __name__ == "__main__":
    main()
