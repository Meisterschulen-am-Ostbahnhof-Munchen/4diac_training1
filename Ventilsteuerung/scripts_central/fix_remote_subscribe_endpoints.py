#!/usr/bin/env python3
"""Fix STG1's 80 remote-aggregation AX_SUBSCRIBE_1 IDs - they were built as
local IDs (no endpoint, ACTION=WRITE reused from the target module's own
publish constant), which is wrong for cross-device access. Per
4diac-documentation/src/communication/opcua.adoc:

  opc_ua[ACTION;ENDPOINT;PAIR1;PAIR2;...]

ENDPOINT is only used/required for remote actions; local PUBLISH/SUBSCRIBE
omit it. STG1 subscribing to STG2..STG5 (different FORTE_PC_STGn devices
per test.sys) IS remote, so it needs opc.tcp://<ip>:4840# - and per the
doc's table, remote continuous monitoring uses ACTION=SUBSCRIBE (not
READ/WRITE, those are for the *local* side only).

IP addresses finalized 2026-08-26: Teltonika RUT906 modem/gateway is
192.168.1.1 (DHCP pool 100-249 on that segment), so the 5 STG controllers
get static IPs 192.168.1.11-15 (STGn -> 192.168.1.1n), clear of both the
gateway and the DHCP range.

Creates Ventilsteuerung_STG1/RemoteSubStrings.gcf (80 constants,
STG{m}_Q{pp}_REMOTE / STG{m}_I{p}_REMOTE) and rewrites
Ventilsteuerung_STG1/Subscribe_STG{2..5}.SUB to import/reference them
instead of the target module's local *_WRITE constant.

Usage: python3 fix_remote_subscribe_endpoints.py
"""
import re

BASE = "4diacIDE-workspace/test/FBs/Ventilsteuerung"
STG1_DIR = f"{BASE}/Ventilsteuerung_STG1"
NUM_I = 8
NUM_Q = 12
REMOTE_MODULES = [2, 3, 4, 5]

# Finalized 2026-08-26: Teltonika RUT906 modem = 192.168.1.1, DHCP pool 100-249.
# STG1-5 get static 192.168.1.11-15.
STG_IP = {n: f"192.168.1.1{n}" for n in [1, 2, 3, 4, 5]}
OPC_UA_PORT = 4840


def endpoint(m):
    return f"opc.tcp://{STG_IP[m]}:{OPC_UA_PORT}#"


def remote_gcf_xml():
    decls = []
    original = []
    for m in REMOTE_MODULES:
        ep = endpoint(m)
        for q in range(1, NUM_Q + 1):
            pp = f"{q:02d}"
            name = f"STG{m}_Q{pp}_REMOTE"
            val = f"opc_ua[SUBSCRIBE;{ep};/Objects/STG{m}/DigitalOutput/Q{pp},1:s=STG{m}.Q{pp}]"
            decls.append(f'\t\t<VarDeclaration Name="{name}" Type="WSTRING" InitialValue="&quot;{val}&quot;"/>\n')
            original.append(f'\t\t{name} : WSTRING := "{val}";\n')
        for i in range(1, NUM_I + 1):
            name = f"STG{m}_I{i}_REMOTE"
            val = f"opc_ua[SUBSCRIBE;{ep};/Objects/STG{m}/DigitalInput/I{i},1:s=STG{m}.I{i}]"
            decls.append(f'\t\t<VarDeclaration Name="{name}" Type="WSTRING" InitialValue="&quot;{val}&quot;"/>\n')
            original.append(f'\t\t{name} : WSTRING := "{val}";\n')

    pkg = "FBs::Ventilsteuerung::Ventilsteuerung_STG1"
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<GlobalConstants Name="RemoteSubStrings" Comment="Remote OPC-UA subscribe addresses for STG1 aggregating STG2..STG5 (static IPs 192.168.1.11-15, Teltonika RUT906 modem/gateway = 192.168.1.1).">\n'
        '\t<Identification Standard="61499-1">\n'
        '\t</Identification>\n'
        '\t<VersionInfo Organization="HR Agrartechnik GmbH" Version="1.0" Author="franz" Date="2026-08-25">\n'
        '\t</VersionInfo>\n'
        f'\t<CompilerInfo packageName="{pkg}">\n'
        '\t</CompilerInfo>\n'
        '\t<GlobalConstants>\n'
        f'{"".join(decls)}'
        '\t</GlobalConstants>\n'
        f'\t<OriginalSource><![CDATA[PACKAGE {pkg};\n'
        '\n'
        '// Static IPs 192.168.1.11-15 (STGn -> 192.168.1.1n); modem/gateway 192.168.1.1\n'
        'GLOBALCONSTANTS RemoteSubStrings\n'
        '\tVAR_GLOBAL CONSTANT\n'
        f'{"".join(original)}'
        '\tEND_VAR\n'
        'END_GLOBALCONSTANTS\n'
        ']]></OriginalSource>\n'
        '</GlobalConstants>\n'
    )


def rewrite_subscribe(m):
    path = f"{STG1_DIR}/Subscribe_STG{m}.SUB"
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" not in content

    names = [f"STG{m}_Q{q:02d}_WRITE" for q in range(1, NUM_Q + 1)]
    names += [f"STG{m}_I{i}_WRITE" for i in range(1, NUM_I + 1)]
    for name in names:
        old_import = f'\t\t<Import declaration="FBs::Ventilsteuerung::Ventilsteuerung_STG{m}::SubStrings_STG{m}::{name}"/>\n'
        assert content.count(old_import) == 1, (path, old_import)
        content = content.replace(old_import, "", 1)

        old_param = f'<Parameter Name="ID" Value="{name}"/>'
        remote_name = name.replace("_WRITE", "_REMOTE")
        new_param = f'<Parameter Name="ID" Value="{remote_name}"/>'
        assert content.count(old_param) == 1, (path, old_param)
        content = content.replace(old_param, new_param, 1)

    remote_names = [n.replace("_WRITE", "_REMOTE") for n in names]
    new_imports = "".join(
        f'\t\t<Import declaration="FBs::Ventilsteuerung::Ventilsteuerung_STG1::RemoteSubStrings::{n}"/>\n'
        for n in remote_names
    )
    content = re.sub(r'(\t<CompilerInfo>\n)', r'\1' + new_imports, content, count=1)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{path}: rewritten (remote endpoint constants)")


def main():
    with open(f"{STG1_DIR}/RemoteSubStrings.gcf", "w", encoding="utf-8", newline="") as f:
        f.write(remote_gcf_xml())
    print(f"{STG1_DIR}/RemoteSubStrings.gcf: written")
    for m in REMOTE_MODULES:
        rewrite_subscribe(m)


if __name__ == "__main__":
    main()
