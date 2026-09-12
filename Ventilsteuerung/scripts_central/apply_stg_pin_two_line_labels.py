"""Roll out the user's hand-built two-line module/pin label prototype
(OutputString_STG1_I1, JVS-ID 11196: text "STG1\\r\\nI1", Height=32,
FontAttributes_12x16) to the remaining 99 module/pin cells (column width
110, JVS-ID range 11010-11392) that still show the single-line
"STGn <middle dot> Qn/In" text on FontAttributes_6x8.

Only cells containing the middle-dot separator (U+00B7) are touched - the
24 bare Bosch field names sharing the same 110px column (rAccX, uiSysStatus,
...) already fit on one line at 6x8 and have no natural two-part split, so
they are left alone. 11196 itself is already converted and is skipped.

For each matched cell:
- Text "STGn <sep> Xn" -> "STGn\\r\\nXn" (CRLF line break, same as prototype)
- Height 18 -> 32, WordBreak 0 -> 1 (MultiLine was already 1)
- Font reference 23000 (FontAttributes_6x8) -> 23003 (FontAttributes_12x16)
- ObjectName/Name -> OutputString_STGn_Xn (matches the prototype's naming)

StringLength is deliberately left unchanged, matching what the user's own
hand-edit of 11196 did (it also left StringLength at its pre-edit value).
"""
import base64
import io
import re

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"

ROW_TEXT_ID_MIN = 11010
ROW_TEXT_ID_MAX = 11392
COLUMN_WIDTH = 110
OLD_FONT = 23000
NEW_FONT = 23003
MIDDLE_DOT = "\u00b7"


def encode_text(s):
    return base64.b64encode((s + "\0").encode("utf-16-le")).decode("ascii")


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert "\r\n" in text

    obj_pattern = re.compile(
        r'<Object Class="COutputText" Name="OutputString_(\d+)" ObjectName="OutputString_\d+" '
        r'Pinned="FALSE" JVS-ID="\d+">.*?</Object>',
        re.DOTALL,
    )

    count = 0

    def repl(m):
        nonlocal count
        block = m.group(0)
        oid = int(m.group(1))
        if not (ROW_TEXT_ID_MIN <= oid <= ROW_TEXT_ID_MAX):
            return block

        width_m = re.search(r'<Property Name="Width">\s*<Value>(\d+)</Value>', block)
        font_m = re.search(r'<Objects>\s*<Object JVS-ID="(\d+)"/>', block)
        if not width_m or not font_m:
            return block
        if int(width_m.group(1)) != COLUMN_WIDTH or int(font_m.group(1)) != OLD_FONT:
            return block

        cdata_m = re.search(r'<!\[CDATA\[([A-Za-z0-9+/=]+)\]\]', block)
        s = base64.b64decode(cdata_m.group(1)).decode("utf-16-le").rstrip("\0")
        if MIDDLE_DOT not in s:
            return block

        part1, part2 = (p.strip() for p in s.split(MIDDLE_DOT, 1))
        new_text = f"{part1}\r\n{part2}"
        new_b64 = encode_text(new_text)

        new_block = block
        new_block = re.sub(
            r'<!\[CDATA\[[A-Za-z0-9+/=]+\]\]', f"<![CDATA[{new_b64}]]>", new_block
        )
        new_block = re.sub(
            r'(<Property Name="Height">\s*<Value>)\d+(</Value>)',
            r"\g<1>32\g<2>",
            new_block,
        )
        new_block = re.sub(
            r'(<Property Name="WordBreak">\s*<Value>)\d+(</Value>)',
            r"\g<1>1\g<2>",
            new_block,
        )
        new_block = re.sub(
            r'(<Objects>\s*<Object JVS-ID=")\d+("/>)',
            r"\g<1>" + str(NEW_FONT) + r"\g<2>",
            new_block,
        )
        new_name = f"OutputString_{part1}_{part2}"
        new_block = new_block.replace(
            f'Name="OutputString_{oid}" ObjectName="OutputString_{oid}"',
            f'Name="{new_name}" ObjectName="{new_name}"',
        )

        count += 1
        return new_block

    text = obj_pattern.sub(repl, text)
    print(f"Converted {count} module/pin cells to the two-line STG/pin label pattern.")

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)


if __name__ == "__main__":
    main()
