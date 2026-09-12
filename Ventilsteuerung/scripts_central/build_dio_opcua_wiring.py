#!/usr/bin/env python3
"""Wire generic DI/DO OPC-UA publish/subscribe into Ventilsteuerung_STG1..5.sub.

Simplified first pass (user decision 2026-08-25): every input treated as a
plain DI, every output as a plain DO, ignoring the real signal-type mix in
combined_APIXON_Pin_Zuordnung.csv (PWM/analog/etc. follow later). Per module:

  - I1..I8:  logiBUS_IXA  -> AX_PUBLISH_1   (ID = STG<n>_I<p>_WRITE)   [readable]
  - Q1..Q12: AX_SUBSCRIBE_1 (ID = STG<n>_Q<pp>_READ) -> AX_SPLIT_2 -> logiBUS_QXA
             AX_SPLIT_2 also -> AX_PUBLISH_1 (ID = STG<n>_Q<pp>_WRITE) [writable+readable]

STG1 additionally subscribes to STG2..STG5's published Q/I values (aggregation
for the shared VT dashboard, per OPC_UA_VERNETZUNG.md section 3/6) - those
AX_SUBSCRIBE_1 instances are left unconnected for now (no live status-color
wiring yet - deferred next step, user decision 2026-08-25).

No Init/INITO event wiring: mirrors the proven working pattern in
C:\\git\\ms\\4diac_training1\\...\\logiBUS_IXA_BG_OPC.SUB /
Button_IXA_TO_logiBUS_QXA_BG_OPC.SUB (both leave AX_PUBLISH_1/AX_SUBSCRIBE_1's
INIT unconnected) and this project's own already-working ScrollFS_PHYS
instances in Ventilsteuerung_STG1.sub (likewise no event wiring at this level).

Usage: python3 build_dio_opcua_wiring.py [--dry-run]
"""
import re
import sys

ROOT = "4diacIDE-workspace/test/FBs/Ventilsteuerung"
MODULES = [1, 2, 3, 4, 5]
NUM_I = 8
NUM_Q = 12

Y_BASE = 5000


def input_block(n, i, y):
    ixa = f"IXA_STG{n}_I{i}"
    pub = f"Publish_STG{n}_I{i}"
    fb = (
        f'\t\t<FB Name="{ixa}" Type="logiBUS::io::DI::logiBUS_IXA" x="200" y="{y}">\n'
        f'\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
        f'\t\t\t<Parameter Name="Input" Value="Input_I{i}"/>\n'
        f'\t\t</FB>\n'
        f'\t\t<FB Name="{pub}" Type="adapter::net::AX_PUBLISH_1" x="1200" y="{y}">\n'
        f'\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
        f'\t\t\t<Parameter Name="ID" Value="&quot;STG{n}_I{i}_WRITE&quot;"/>\n'
        f'\t\t</FB>\n'
    )
    conn = f'\t\t\t<Connection Source="{ixa}.IN" Destination="{pub}.IN"/>\n'
    return fb, conn


def output_block(n, q, y):
    pp = f"{q:02d}"
    qxa = f"QXA_STG{n}_Q{pp}"
    sub = f"Subscribe_STG{n}_Q{pp}_CMD"
    pub = f"Publish_STG{n}_Q{pp}"
    split = f"Split_STG{n}_Q{pp}"
    fb = (
        f'\t\t<FB Name="{qxa}" Type="logiBUS::io::DQ::logiBUS_QXA" x="2500" y="{y}">\n'
        f'\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
        f'\t\t\t<Parameter Name="Output" Value="Output_Q{q}"/>\n'
        f'\t\t</FB>\n'
        f'\t\t<FB Name="{sub}" Type="adapter::net::AX_SUBSCRIBE_1" x="3500" y="{y}">\n'
        f'\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
        f'\t\t\t<Parameter Name="ID" Value="&quot;STG{n}_Q{pp}_READ&quot;"/>\n'
        f'\t\t</FB>\n'
        f'\t\t<FB Name="{split}" Type="adapter::events::unidirectional::AX_SPLIT_2" x="4500" y="{y}">\n'
        f'\t\t</FB>\n'
        f'\t\t<FB Name="{pub}" Type="adapter::net::AX_PUBLISH_1" x="5500" y="{y}">\n'
        f'\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
        f'\t\t\t<Parameter Name="ID" Value="&quot;STG{n}_Q{pp}_WRITE&quot;"/>\n'
        f'\t\t</FB>\n'
    )
    conns = (
        f'\t\t\t<Connection Source="{sub}.OUT" Destination="{split}.IN"/>\n'
        f'\t\t\t<Connection Source="{split}.OUT1" Destination="{qxa}.OUT"/>\n'
        f'\t\t\t<Connection Source="{split}.OUT2" Destination="{pub}.IN"/>\n'
    )
    return fb, conns


def remote_subscribe_block(local_n, remote_n, kind, idx, y):
    # kind: "Q" (pp zero-padded 2 digits) or "I" (plain digit)
    if kind == "Q":
        label = f"Q{idx:02d}"
        key = f"STG{remote_n}_Q{idx:02d}_WRITE"
    else:
        label = f"I{idx}"
        key = f"STG{remote_n}_I{idx}_WRITE"
    name = f"Subscribe_STG{remote_n}_{label}_Remote"
    x = 7000 + (remote_n - 2) * 1200
    fb = (
        f'\t\t<FB Name="{name}" Type="adapter::net::AX_SUBSCRIBE_1" x="{x}" y="{y}">\n'
        f'\t\t\t<Parameter Name="QI" Value="TRUE"/>\n'
        f'\t\t\t<Parameter Name="ID" Value="&quot;{key}&quot;"/>\n'
        f'\t\t</FB>\n'
    )
    return fb


def build_module(n):
    fbs = []
    conns = []
    y = Y_BASE
    for i in range(1, NUM_I + 1):
        fb, conn = input_block(n, i, y)
        fbs.append(fb)
        conns.append(conn)
        y += 300
    y = Y_BASE
    for q in range(1, NUM_Q + 1):
        fb, conn = output_block(n, q, y)
        fbs.append(fb)
        conns.append(conn)
        y += 300

    if n == 1:
        y = Y_BASE
        for remote_n in [2, 3, 4, 5]:
            for q in range(1, NUM_Q + 1):
                fbs.append(remote_subscribe_block(n, remote_n, "Q", q, y))
                y += 250
            for i in range(1, NUM_I + 1):
                fbs.append(remote_subscribe_block(n, remote_n, "I", i, y))
                y += 250

    block = "".join(fbs)
    block += "\t\t<AdapterConnections>\n"
    block += "".join(conns)
    block += "\t\t</AdapterConnections>\n"
    return block


def main():
    dry_run = "--dry-run" in sys.argv
    for n in MODULES:
        path = f"{ROOT}/Ventilsteuerung_STG{n}.sub"
        with open(path, "r", encoding="utf-8", newline="") as f:
            content = f.read()
        assert "\r\n" not in content, f"{path}: unexpected CRLF, check newline handling"

        block = build_module(n)

        marker = "\t</SubAppNetwork>\n"
        count = content.count(marker)
        assert count == 1, f"{path}: expected exactly one {marker!r}, found {count}"

        new_content = content.replace(marker, block + marker)

        if dry_run:
            added = new_content.count("<FB Name=") - content.count("<FB Name=")
            print(f"{path}: would add {added} FB instances")
        else:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new_content)
            print(f"{path}: written")


if __name__ == "__main__":
    main()
