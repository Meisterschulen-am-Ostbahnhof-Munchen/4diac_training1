"""Merge the per-page STG1-STG5 module header containers into one shared
instance each, per the user's request: "Container_Header_3070 soll heissen
Container_Header_STG1 usw. Container_Header_3001 soll derselbe Container
sein (Multi Instance)".

Both diagnostic pages currently build their own independent copy of each
"STGn" header (CGroup + a HeaderBg CProxy pointing at the already-shared
background rectangle 14001 + a per-copy CProxy/COutputText title). This
duplicates 5 CGroups, 10 CProxy wrappers and 5 COutputText objects for
content that is pixel-identical on both pages.

For each of the 5 STG numbers:
- The Eingaenge-side copy becomes the single canonical instance: its CGroup
  is renamed Container_Header_STGn, its title COutputText and the CProxy
  wrapping it inside the CGroup are renamed OutputString_STGn, and its
  page-placement CProxy is renamed Container_Header_STGn.
- The Ausgaenge-side placement CProxy is retargeted to reference the
  (renamed) Eingaenge-side CGroup instead of its own copy, and renamed
  Container_Header_STGn to match.
- The now fully-unreferenced Ausgaenge-side CGroup, its two CProxy children
  (HeaderBg wrapper + title wrapper) and its title COutputText are deleted.

Mapping (Ausgaenge CGroup/OutputText id -> Eingaenge CGroup/OutputText id),
discovered by decoding each header's title text and tracing CProxy targets:
STG1 3001/11010 -> 3070/11195, STG2 3014/11047 -> 3079/11220,
STG3 3027/11084 -> 3088/11245, STG4 3040/11121 -> 3097/11270,
STG5 3053/11158 -> 3106/11295.
"""
import io
import re

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"

# n: (ausg_cgroup, ausg_text, ausg_headerbg_proxy, ausg_text_proxy, ausg_placement_proxy,
#     eing_cgroup, eing_text, eing_text_proxy, eing_placement_proxy)
PAIRS = {
    1: (3001, 11010, 4194329, 4194330, 4194331, 3070, 11195, 4194781, 4194782),
    2: (3014, 11047, 4194416, 4194417, 4194418, 3079, 11220, 4194840, 4194841),
    3: (3027, 11084, 4194503, 4194504, 4194505, 3088, 11245, 4194899, 4194900),
    4: (3040, 11121, 4194590, 4194591, 4194592, 3097, 11270, 4194958, 4194959),
    5: (3053, 11158, 4194677, 4194678, 4194679, 3106, 11295, 4195017, 4195018),
}


def replace_block(text, jid, new_block_fn):
    """Find the single <Object ... JVS-ID="jid">...</Object> block and
    replace it with new_block_fn(block)."""
    pat = re.compile(r'<Object Class="\w+"[^>]*JVS-ID="' + str(jid) + r'">.*?</Object>\r\n', re.DOTALL)
    matches = list(pat.finditer(text))
    assert len(matches) == 1, f"expected exactly one block for JVS-ID {jid}, found {len(matches)}"
    m = matches[0]
    new_block = new_block_fn(m.group(0))
    return text[: m.start()] + new_block + text[m.end():]


def delete_block(text, jid):
    pat = re.compile(r'\t*<Object Class="\w+"[^>]*JVS-ID="' + str(jid) + r'">.*?</Object>\r\n', re.DOTALL)
    matches = list(pat.finditer(text))
    assert len(matches) == 1, f"expected exactly one block to delete for JVS-ID {jid}, found {len(matches)}"
    m = matches[0]
    return text[: m.start()] + text[m.end():]


def rename_plain(block, new_name):
    return re.sub(r'Name="[^"]*" ObjectName="[^"]*"', f'Name="{new_name}" ObjectName="{new_name}"', block, count=1)


def rename_proxy(block, new_name):
    block = re.sub(r'Name="[^"]*" ObjectName=""', f'Name="{new_name}" ObjectName=""', block, count=1)
    block = re.sub(
        r'(<Property Name="Name">\s*<Value>)[^<]*(</Value>)',
        r"\g<1>" + new_name + r"\g<2>",
        block,
        count=1,
    )
    return block


def retarget_proxy(block, new_target):
    return re.sub(
        r'(<Objects>\s*<Object JVS-ID=")\d+("/>\s*</Objects>)',
        r"\g<1>" + str(new_target) + r"\g<2>",
        block,
        count=1,
    )


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert "\r\n" in text

    for n, (
        ausg_cgroup, ausg_text, ausg_bg_proxy, ausg_text_proxy, ausg_place_proxy,
        eing_cgroup, eing_text, eing_text_proxy, eing_place_proxy,
    ) in PAIRS.items():
        cgroup_name = f"Container_Header_STG{n}"
        text_name = f"OutputString_STG{n}"

        # 1. Rename the canonical (Eingaenge) CGroup and its title text.
        text = replace_block(text, eing_cgroup, lambda b: rename_plain(b, cgroup_name))
        text = replace_block(text, eing_text, lambda b: rename_plain(b, text_name))
        text = replace_block(text, eing_text_proxy, lambda b: rename_proxy(b, text_name))
        text = replace_block(text, eing_place_proxy, lambda b: rename_proxy(b, cgroup_name))

        # 2. Retarget the Ausgaenge placement proxy to the canonical CGroup and rename it.
        def fix_ausg_placement(b, cgroup_name=cgroup_name, eing_cgroup=eing_cgroup):
            b = rename_proxy(b, cgroup_name)
            b = retarget_proxy(b, eing_cgroup)
            return b

        text = replace_block(text, ausg_place_proxy, fix_ausg_placement)

        # 3. Delete the now fully-unreferenced Ausgaenge-side objects.
        text = delete_block(text, ausg_cgroup)
        text = delete_block(text, ausg_bg_proxy)
        text = delete_block(text, ausg_text_proxy)
        text = delete_block(text, ausg_text)

        print(f"STG{n}: canonical={cgroup_name} (was {eing_cgroup}); "
              f"deleted CGroup {ausg_cgroup}, proxies {ausg_bg_proxy}/{ausg_text_proxy}, text {ausg_text}")

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("Done.")


if __name__ == "__main__":
    main()
