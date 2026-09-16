"""Corrective fix for a bug in rename_function_name_cells.py: its "already
converted?" detection regex used an unbounded '.*?' that could cross past
an object's own closing </Object> tag, so for 99 rows it incorrectly also
renamed/resized the width-100 "Anschlussbezeichnung" (column 3) cell to
the same name/font/height meant only for the width-180 "Funktionsname"
(column 2) cell - producing duplicate ObjectNames.

This restores just those 99 width-100 objects to their pre-bug state:
ObjectName/Name back to "OutputString_<JVS-ID>", Height 24 -> 18, font
FontAttributes_8x12 (23002) -> FontAttributes_6x8 (23000). The correct
width-180 renames from the same run are left untouched.
"""
import io
import re

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert "\r\n" in text

    block_pat = re.compile(
        r'<Object Class="COutputText" Name="(OutputString_STG\d+_[QI]\d+_name)" ObjectName="\1" '
        r'Pinned="FALSE" JVS-ID="(\d+)">.*?</Object>',
        re.DOTALL,
    )

    count = 0

    def repl(m):
        nonlocal count
        block = m.group(0)
        bad_name, jid = m.group(1), m.group(2)

        width_m = re.search(r'<Property Name="Width">\s*<Value>(\d+)</Value>', block)
        if width_m.group(1) != "100":
            return block

        fixed_name = f"OutputString_{jid}"
        new_block = block.replace(
            f'Name="{bad_name}" ObjectName="{bad_name}"',
            f'Name="{fixed_name}" ObjectName="{fixed_name}"',
        )
        new_block = re.sub(
            r'(<Property Name="Height">\s*<Value>)24(</Value>)',
            r"\g<1>18\g<2>",
            new_block,
            count=1,
        )
        new_block, n_font = re.subn(
            r'(<Objects>\s*<Object JVS-ID=")23002("/>)',
            r"\g<1>23000\g<2>",
            new_block,
            count=1,
        )
        assert n_font == 1, f"{jid}: font fix matched {n_font} times"

        count += 1
        return new_block

    text = block_pat.sub(repl, text)
    print(f"Fixed {count} wrongly-touched width-100 cells.")

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)


if __name__ == "__main__":
    main()
