"""Follow-up to apply_offene_punkte_fixes.py: the diagnostic-page data-row
cells (Width 100/110/180 - module/pin, function name, connector columns)
still don't fit their column at FontAttributes_16x16 for the longest labels
(e.g. "bAllSignalsReady", "Bunkerfuellband_verstellung", comma-joined multi-
target refs like "Y3.10, Y4.13") - confirmed by decoding all 383 generated
OutputText objects' actual text against their box width. Only the smallest
standard ISO 11783-6 font, 6x8 (JVS-ID 23000), fits every case (user choice,
see AUSGAENGE_EINGAENGE_POOL_PLAN.md).

Header cells (Width 300 - "STG1" etc.) already fit comfortably at 16x16 and
stay there for visual hierarchy against the smaller data rows - only the
Width-100/110/180 cells are repointed here.
"""
import io
import re

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"

OLD_FONT = 23004  # FontAttributes_16x16
NEW_FONT = 23000  # FontAttributes_6x8
ROW_TEXT_ID_MIN = 11010
ROW_TEXT_ID_MAX = 11392
DATA_COLUMN_WIDTHS = {100, 110, 180}


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert "\r\n" in text

    pattern = re.compile(
        r'(<Object Class="COutputText"[^>]*JVS-ID="(\d+)">.*?'
        r'<Property Name="Width">\s*<Value>(\d+)</Value>.*?'
        r'<Objects>\s*<Object JVS-ID=")(\d+)("/>)',
        re.DOTALL,
    )

    count = 0

    def repl(m):
        nonlocal count
        oid = int(m.group(2))
        width = int(m.group(3))
        font = int(m.group(4))
        if (
            ROW_TEXT_ID_MIN <= oid <= ROW_TEXT_ID_MAX
            and width in DATA_COLUMN_WIDTHS
            and font == OLD_FONT
        ):
            count += 1
            return f"{m.group(1)}{NEW_FONT}{m.group(5)}"
        return m.group(0)

    text = pattern.sub(repl, text)
    print(f"Repointed {count} data-row cells to FontAttributes_6x8 ({NEW_FONT}).")

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)


if __name__ == "__main__":
    main()
