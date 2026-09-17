#!/usr/bin/env python3
"""Rename the 16 CSoftKey objects (currently generic SoftKey_<ROLE> /
SoftKey_<ROLE>_1) to page-explicit names SoftKey_Ausgaenge_<ROLE> /
SoftKey_Eingaenge_<ROLE> - per user request 2026-08-27 ("SoftKey_LAST_1
soll heissen SoftKey_Eingaenge_LAST, SoftKey_LAST soll heissen
SoftKey_Ausgaenge_LAST und so weiter"), same pattern already applied to
ObjectPointer_SoftKey_* in an earlier session (see
AUSGAENGE_EINGAENGE_POOL_PLAN.md).

Finds each SoftKey's wrapping CProxy by which JVS-ID it actually targets
(<Objects><Object JVS-ID="..."/></Objects>), NOT by the proxy's own
current Name/Value - confirmed necessary: SoftKey_LAST_1's own proxy is
already misnamed "SoftKey_LAST" (stale copy, pre-existing), so a plain
string search for the old name would have silently skipped it (or
worse, renamed the wrong proxy). Matches the iso-designer-jop skill's
renaming discipline (sync every CProxy shadow copy, don't trust its
current name).

Usage: python3 rename_softkeys_by_page.py
"""
import re

POOL = "ISO-DesignerProjects/Workspace/DefaultPool/DefaultPool.jop"

# JVS-ID -> new ObjectName
RENAMES = {
    "5002": "SoftKey_Ausgaenge_FIRST",
    "5003": "SoftKey_Ausgaenge_PAGE_UP",
    "5004": "SoftKey_Ausgaenge_UP",
    "5005": "SoftKey_Ausgaenge_DOWN",
    "5006": "SoftKey_Ausgaenge_PAGE_DOWN",
    "5007": "SoftKey_Ausgaenge_LAST",
    "5014": "SoftKey_Ausgaenge_Back",
    "5015": "SoftKey_Ausgaenge_Lock",
    "5008": "SoftKey_Eingaenge_FIRST",
    "5009": "SoftKey_Eingaenge_PAGE_UP",
    "5010": "SoftKey_Eingaenge_UP",
    "5011": "SoftKey_Eingaenge_DOWN",
    "5012": "SoftKey_Eingaenge_PAGE_DOWN",
    "5013": "SoftKey_Eingaenge_LAST",
    "5016": "SoftKey_Eingaenge_Back",
    "5017": "SoftKey_Eingaenge_Lock",
}


def main():
    with open(POOL, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    assert "\r\n" in content, "expected CRLF in DefaultPool.jop"

    for jvs_id, new_name in RENAMES.items():
        # 1. The CSoftKey definition's own ObjectName.
        def_pattern = re.compile(
            r'(<Object Class="CSoftKey" Name="SoftKey" ObjectName=")[^"]*("'
            r' Pinned="FALSE" JVS-ID="' + jvs_id + r'">)'
        )
        content, n = def_pattern.subn(r'\g<1>' + new_name + r'\g<2>', content)
        assert n == 1, f"CSoftKey definition for JVS-ID {jvs_id} not found exactly once (found {n})"

        # 2. Every CProxy whose sole child targets this JVS-ID - found by
        #    what it wraps, not by its own (possibly stale) current name.
        #    The body must not cross into a sibling Object's closing tag
        #    (bare ".*?" would happily skip past several unrelated objects
        #    to find a later matching child reference - confirmed to
        #    happen and silently corrupt an unrelated proxy).
        proxy_pattern = re.compile(
            r'<Object Class="CProxy" Name="([^"]*)" ObjectName="" Pinned="FALSE" JVS-ID="(\d+)">\r\n'
            r'(?:(?!</Object>).)*?\r\n'
            r'\t\t\t<Objects>\r\n'
            r'\t\t\t\t<Object JVS-ID="' + jvs_id + r'"/>\r\n'
            r'\t\t\t</Objects>\r\n'
            r'\t\t</Object>\r\n',
            re.DOTALL,
        )
        matches = list(proxy_pattern.finditer(content))
        assert len(matches) == 1, f"expected exactly one CProxy wrapping JVS-ID {jvs_id}, found {len(matches)}"
        for m in matches:
            proxy_id = m.group(2)
            old_block = m.group(0)
            new_block = old_block.replace(
                f'<Object Class="CProxy" Name="{m.group(1)}" ObjectName="" Pinned="FALSE" JVS-ID="{proxy_id}">',
                f'<Object Class="CProxy" Name="{new_name}" ObjectName="" Pinned="FALSE" JVS-ID="{proxy_id}">',
                1,
            )
            name_prop_pattern = re.compile(
                r'(<Property Name="Name">\r\n\t+<Value>)[^<]*(</Value>)'
            )
            new_block, n = name_prop_pattern.subn(r'\g<1>' + new_name + r'\g<2>', new_block, count=1)
            assert n == 1, f"proxy {proxy_id} for JVS-ID {jvs_id}: nested Name property not found/updated"
            assert content.count(old_block) == 1
            content = content.replace(old_block, new_block, 1)
            print(f"JVS-ID {jvs_id} -> {new_name}: proxy {proxy_id} updated")

    with open(POOL, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"{POOL}: written")


if __name__ == "__main__":
    main()
