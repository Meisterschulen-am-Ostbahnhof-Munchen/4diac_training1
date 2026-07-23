"""Rebuild the Background-block variants that CompareMyLibFamilies.py flagged
as missing on one side of test_AX / test_B, after CleanupMyLibTypeLibrary.py
removed the unused duplicate copies.

Three gap categories, each handled by a dedicated generator:

1. "aux" capability missing in test_B (only ever existed as "_aux_AX*"):
   take the existing test_B plain/S file and swap the
   isobus::UT::Q::Q_BackgroundColour FB for its isobus::UT::Q::Q_BackgroundColourAux
   sibling (verified: that FB swap is the *only* difference between an
   "_AX"/"_AXS" file and its "_aux_AX"/"_aux_AXS" counterpart).

2. Whole family missing in test_B (only ever existed as "*_AX*", e.g.
   GreenRedBackground2/4, RedWhiteBackground3/4): invert the existing
   test_AX plain/S file back to the plain-B style - swap the AX-adapter
   selector (Socket DI1 + AX_SEL FB) for the plain-B selector (BOOL DI1
   InputVar + F_SEL_I FB + an explicit REQ trigger event), and the
   per-color imports for the general "colours" package import.

3. "C" (compact, no "S") missing in test_AX (only ever existed as plain
   "*C"): build a compact wrapper around the family's own "_AX" file the
   same way "_AXSC" already wraps "_AXS" - introspect the "_AX" file's
   InputVars + Sockets and pass them straight through.

Every generated file is validated as well-formed XML before being written.
"""

import os
import re
import xml.etree.ElementTree as ET
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENTILSTEUERUNG_DIR = os.path.dirname(SCRIPT_DIR)
WORKSPACE_DIR = os.path.join(VENTILSTEUERUNG_DIR, "4diacIDE-workspace")

AX_SYS = os.path.join(WORKSPACE_DIR, "test_AX", "Type Library", "MyLib", "sys")
B_SYS = os.path.join(WORKSPACE_DIR, "test_B", "Type Library", "MyLib", "sys")

TODAY = date.today().isoformat()


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    ET.fromstring(content)  # raise if not well-formed
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"  wrote {os.path.relpath(path, VENTILSTEUERUNG_DIR)}")


def rename_decl(content, old_name, new_name):
    return content.replace(f'Name="{old_name}" Comment=', f'Name="{new_name}" Comment=', 1)


# ---------------------------------------------------------------------------
# Category 1: aux missing in test_B
# ---------------------------------------------------------------------------

AUX_FAMILIES = [
    "GreenBlueBackground1",
    "GreenRedBackground1",
    "GreenWhiteBackground1",
    "RedGreenBackground1",
    "RedWhiteBackground1",
]


def make_aux(content, old_name, new_name):
    content = content.replace(f'Name="{old_name}"', f'Name="{new_name}"', 1)
    content = re.sub(r"Q_BackgroundColour(?!Aux)", "Q_BackgroundColourAux", content)
    content = re.sub(
        r'(<VersionInfo Organization="Meisterschulen am Ostbahnhof" Version="1\.0" Author="franz" Date=")[^"]*(")',
        rf"\g<1>{TODAY}\g<2>",
        content,
        count=1,
    )
    return content


def build_category1():
    print("=== Category 1: aux missing in test_B ===")
    for family in AUX_FAMILIES:
        # plain -> aux
        plain = read(os.path.join(B_SYS, f"{family}.SUB"))
        aux = make_aux(plain, family, f"{family}_aux")
        write(os.path.join(B_SYS, f"{family}_aux.SUB"), aux)

        # S -> auxS
        s_path = os.path.join(B_SYS, f"{family}S.SUB")
        s_content = read(s_path)
        auxs = make_aux(s_content, f"{family}S", f"{family}_auxS")
        write(os.path.join(B_SYS, f"{family}_auxS.SUB"), auxs)

        # SC -> auxSC: same file, just rename decl + retarget the wrapped SubApp
        sc_path = os.path.join(B_SYS, f"{family}SC.SUB")
        sc_content = read(sc_path)
        auxsc = sc_content.replace(f'Name="{family}SC"', f'Name="{family}_auxSC"', 1)
        auxsc = auxsc.replace(f'Type="MyLib::sys::{family}S"', f'Type="MyLib::sys::{family}_auxS"')
        write(os.path.join(B_SYS, f"{family}_auxSC.SUB"), auxsc)


# ---------------------------------------------------------------------------
# Category 2: whole family missing in test_B
# ---------------------------------------------------------------------------

MISSING_FAMILY = ["GreenRedBackground2", "GreenRedBackground4", "RedWhiteBackground3", "RedWhiteBackground4"]

SOCKET_RE = re.compile(
    r'\t\t<Sockets>\n\t\t\t<AdapterDeclaration Name="DI1" Type="adapter::types::unidirectional::AX"(?: Comment="([^"]*)")?/>\n\t\t</Sockets>\n'
)
ADAPTERCONN_RE = re.compile(
    r'\t\t<AdapterConnections>\n\t\t\t<Connection Source="DI1" Destination="F_SEL_I\.G"([^/]*)/>\n\t\t</AdapterConnections>\n'
)
COLOR_IMPORT_RE = re.compile(r'\t\t<Import declaration="isobus::UT::Q::const::colours::COLOR_\w+"/>\n')


def invert_ax_to_plain(content, new_name):
    old_name = re.search(r'<SubAppType Name="([^"]+)"', content).group(1)

    # FB type + all instance references: AX_SEL -> F_SEL_I
    content = content.replace(
        'Type="adapter::iec61131::selection::AX_SEL"', 'Type="iec61131::selection::F_SEL"'
    )
    content = content.replace("AX_SEL", "F_SEL_I")

    # color constants: bare Value="COLOR_X" -> Value="colours::COLOR_X"
    content = re.sub(r'Value="COLOR_(\w+)"', r'Value="colours::COLOR_\1"', content)

    # two specific colour imports -> one general package import (keep first occurrence position)
    first_color_import = COLOR_IMPORT_RE.search(content)
    content = COLOR_IMPORT_RE.sub("", content)
    content = content.replace(
        '\t\t<Import declaration="isobus::UT::Q::const::IDs::ID_NULL"/>\n',
        '\t\t<Import declaration="isobus::UT::Q::const::IDs::ID_NULL"/>\n\t\t<Import declaration="isobus::UT::Q::const::colours"/>\n',
        1,
    )
    assert first_color_import, "expected color imports not found"

    # Sockets -> InputVars DI1 BOOL
    m = SOCKET_RE.search(content)
    assert m, "Sockets block not found"
    comment = m.group(1) or "Selector"
    content = SOCKET_RE.sub("", content)
    content = content.replace(
        "\t\t<InputVars>\n",
        f'\t\t<InputVars>\n\t\t\t<VarDeclaration Name="DI1" Type="BOOL" Comment="{comment}"/>\n',
        1,
    )

    # AdapterConnections DI1->F_SEL_I.G -> fold into DataConnections
    m = ADAPTERCONN_RE.search(content)
    assert m, "AdapterConnections DI1->F_SEL_I.G not found"
    attrs = m.group(1)
    content = ADAPTERCONN_RE.sub("", content)
    content = re.sub(
        r"(\t\t<DataConnections>\n)",
        rf'\1\t\t\t<Connection Source="DI1" Destination="F_SEL_I.G"{attrs}/>\n',
        content,
        count=1,
    )

    # add REQ event input + wire REQ -> F_SEL_I.REQ
    content = content.replace(
        "\t<SubAppInterfaceList>\n",
        "\t<SubAppInterfaceList>\n"
        "\t\t<SubAppEventInputs>\n"
        '\t\t\t<SubAppEvent Name="REQ" Type="Event" Comment="Normal Execution Request">\n'
        "\t\t\t</SubAppEvent>\n"
        "\t\t</SubAppEventInputs>\n",
        1,
    )
    content = re.sub(
        r"(\t\t<EventConnections>\n)",
        r'\1\t\t\t<Connection Source="REQ" Destination="F_SEL_I.REQ" dx1="473.33"/>\n',
        content,
        count=1,
    )

    # rename decl, strip " (AX-Adapter)" from Comment, simplify Identification/VersionInfo to plain-B house style
    content = content.replace(f'Name="{old_name}"', f'Name="{new_name}"', 1)
    content = content.replace(" (AX-Adapter)", "")
    content = re.sub(
        r'<Identification Standard="61499-2"[^>]*>\n(?:\t.*\n)*?\t</Identification>',
        '<Identification Standard="61499-2">\n\t</Identification>',
        content,
        count=1,
    )
    content = re.sub(
        r'<VersionInfo Organization="[^"]*" Version="1\.0" Author="[^"]*" Date="[^"]*">\n\t</VersionInfo>',
        f'<VersionInfo Organization="Meisterschulen am Ostbahnhof" Version="1.0" Author="franz" Date="{TODAY}">\n\t</VersionInfo>',
        content,
        count=1,
    )
    return content


def build_compact_wrapper(source_content, wrapped_type_qualified, new_name, new_comment, flavor):
    """flavor: 'AX' (Socket DI1 + AdapterConnections, no events) or 'B' (BOOL DI1 InputVar
    + DataConnections + EO event)."""
    inputvars_block = re.search(r"<InputVars>(.*?)</InputVars>", source_content, re.DOTALL).group(1)
    var_decls = re.findall(r'<VarDeclaration Name="(\w+)" Type="([^"]+)"[^>]*(?:/>|>.*?</VarDeclaration>)', inputvars_block, re.DOTALL)
    # DI1 is always handled explicitly below (Socket for AX flavor, dedicated BOOL var for B flavor) -
    # exclude it here so it isn't duplicated when the source already carries a plain-B "DI1" BOOL InputVar.
    var_decls = [(name, vtype) for name, vtype in var_decls if name != "DI1"]

    passthrough_vars = "\n".join(
        f'\t\t\t<VarDeclaration Name="{name}" Type="{vtype}"/>' for name, vtype in var_decls
    )
    data_conns = "\n".join(
        f'\t\t\t<Connection Source="{name}" Destination="Wrapped.{name}" dx1="700"/>' for name, _ in var_decls
    )

    if flavor == "AX":
        interface = (
            f"\t\t<InputVars>\n{passthrough_vars}\n\t\t</InputVars>\n"
            f'\t\t<Sockets>\n\t\t\t<AdapterDeclaration Name="DI1" Type="adapter::types::unidirectional::AX"/>\n\t\t</Sockets>\n'
        )
        network_extra = (
            f'\t\t<AdapterConnections>\n\t\t\t<Connection Source="DI1" Destination="Wrapped.DI1" dx1="680"/>\n\t\t</AdapterConnections>\n'
        )
        events_iface = ""
        events_conn = ""
    else:
        interface = (
            f"\t\t<InputVars>\n{passthrough_vars}\n\t\t\t<VarDeclaration Name=\"DI1\" Type=\"BOOL\" Comment=\"Selector\"/>\n\t\t</InputVars>\n"
        )
        data_conns += '\n\t\t\t<Connection Source="DI1" Destination="Wrapped.DI1" dx1="700"/>'
        network_extra = ""
        events_iface = (
            '\t\t<SubAppEventInputs>\n\t\t\t<SubAppEvent Name="EO" Type="Event">\n\t\t\t</SubAppEvent>\n\t\t</SubAppEventInputs>\n'
        )
        events_conn = '\t\t<EventConnections>\n\t\t\t<Connection Source="EO" Destination="Wrapped.REQ" dx1="666.67"/>\n\t\t</EventConnections>\n'

    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<SubAppType Name="{new_name}" Comment="{new_comment}">
\t<Identification Standard="61499-2">
\t</Identification>
\t<VersionInfo Organization="Meisterschulen am Ostbahnhof" Version="1.0" Author="franz" Date="{TODAY}">
\t</VersionInfo>
\t<CompilerInfo packageName="MyLib::sys">
\t\t<Import declaration="isobus::UT::Q::const::IDs::ID_NULL"/>
\t</CompilerInfo>
\t<SubAppInterfaceList>
{events_iface}{interface}\t</SubAppInterfaceList>
\t<SubAppNetwork>
\t\t<SubApp Name="Wrapped" Type="{wrapped_type_qualified}" x="1700" y="-800">
\t\t</SubApp>
{events_conn}\t\t<DataConnections>
{data_conns}
\t\t</DataConnections>
{network_extra}\t</SubAppNetwork>
</SubAppType>
"""
    return content


def build_category2():
    print("=== Category 2: whole family missing in test_B ===")
    for family in MISSING_FAMILY:
        plain_src = read(os.path.join(AX_SYS, f"{family}_AX.SUB"))
        plain_new = invert_ax_to_plain(plain_src, family)
        write(os.path.join(B_SYS, f"{family}.SUB"), plain_new)

        s_src = read(os.path.join(AX_SYS, f"{family}_AXS.SUB"))
        s_new = invert_ax_to_plain(s_src, f"{family}S")
        write(os.path.join(B_SYS, f"{family}S.SUB"), s_new)

        struct_type = re.search(r'Type="(isobus::UT::Q::types::s\dObjectIDs)"', s_new).group(1)
        comment = re.search(r'Comment="([^"]*)"', s_new).group(1) + " (Kompakt)"
        sc_new = build_compact_wrapper(
            s_new, f"MyLib::sys::{family}S", f"{family}SC", comment, flavor="B"
        )
        sc_new = sc_new.replace('Name="Wrapped"', f'Name="{family}"', 1).replace("Wrapped.", f"{family}.")
        sc_new = sc_new.replace(
            '<Import declaration="isobus::UT::Q::const::IDs::ID_NULL"/>\n',
            f'<Import declaration="isobus::UT::Q::const::IDs::ID_NULL"/>\n\t\t<Import declaration="{struct_type}"/>\n',
            1,
        )
        write(os.path.join(B_SYS, f"{family}SC.SUB"), sc_new)


# ---------------------------------------------------------------------------
# Category 3: "C" (compact of plain) missing in test_AX
# ---------------------------------------------------------------------------

MISSING_C = [
    "GreenWhiteBackground1",
    "GreenWhiteBackground2",
    "GreenWhiteBackground3",
    "GreenWhiteBackground4",
    "RedGreenBackground4",
    "RedWhiteBackground2",
]


def build_category3():
    print('=== Category 3: "C" missing in test_AX ===')
    for family in MISSING_C:
        ax_src = read(os.path.join(AX_SYS, f"{family}_AX.SUB"))
        comment = re.search(r'Comment="([^"]*)"', ax_src).group(1) + " (Kompakt)"
        axc = build_compact_wrapper(
            ax_src, f"MyLib::sys::{family}_AX", f"{family}_AXC", comment, flavor="AX"
        )
        axc = axc.replace('Name="Wrapped"', f'Name="{family}"', 1).replace("Wrapped.", f"{family}.")
        write(os.path.join(AX_SYS, f"{family}_AXC.SUB"), axc)


if __name__ == "__main__":
    build_category1()
    build_category2()
    build_category3()
