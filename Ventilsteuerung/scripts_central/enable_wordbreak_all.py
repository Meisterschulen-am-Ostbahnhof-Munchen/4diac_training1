"""Set WordBreak=1 on every COutputText object in the pool (user request:
"bitte mal in alle Strings das Wrap reinmachen ... COutputText ALLE").

Operates block-by-block (each match is the single object's own bounded
<Object Class="COutputText">...</Object> span, found via re.finditer before
any substitution happens) so there is no risk of a fix touching more than
one object at a time - unlike the earlier rename_function_name_cells.py bug,
this script never lets a pattern's non-greedy portion escape a block it
found first.
"""
import io
import re

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert "\r\n" in text

    block_pat = re.compile(r'<Object Class="COutputText".*?</Object>', re.DOTALL)

    total = 0
    changed = 0

    def repl(m):
        nonlocal total, changed
        total += 1
        block = m.group(0)
        new_block, n = re.subn(
            r'(<Property Name="WordBreak">\s*<Value>)\d+(</Value>)',
            r"\g<1>1\g<2>",
            block,
            count=1,
        )
        assert n == 1, "COutputText block without a WordBreak property found"
        if new_block != block:
            changed += 1
        return new_block

    text = block_pat.sub(repl, text)
    print(f"Scanned {total} COutputText objects, set WordBreak=1 on {changed} that were 0.")

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)


if __name__ == "__main__":
    main()
