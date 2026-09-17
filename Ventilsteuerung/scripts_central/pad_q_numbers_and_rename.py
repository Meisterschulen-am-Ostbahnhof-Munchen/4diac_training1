"""Apply the user's requested renames for row Ausgang_STG1_Q01's remaining
cells, and standardize all Ausgaenge Q-numbers to always be two digits
("bitte ueberall Q01 ... Q12 schreiben also immer 2-stellig"):

1. OutputString_11013 -> OutputString_STG1_Q01_ID (column-3 "Anschluss-
   bezeichnung" cell for that row).
2. ObjectPointer_Status_27000 -> ObjectPointer_Status_STG1_Q01 (that row's
   status-color pointer).
3. The 45 two-line module/pin labels OutputString_STGn_Qm with a single-
   digit m (Q1..Q9, from apply_stg_pin_two_line_labels.py) are renamed to
   OutputString_STGn_Q0m, and - so the on-screen label matches its own
   object name - their visible text "STGn\\r\\nQm" is rewritten to
   "STGn\\r\\nQ0m" as well. Q10-Q12 were already two digits and Eingaenge's
   I-numbers are deliberately left single digit (established convention:
   Ausgaenge WITH leading zero, Eingaenge without).
4. OutputString_STG1_Q1_name (renamed in the previous step, before this
   2-digit rule was stated) is corrected to OutputString_STG1_Q01_name.
"""
import base64
import io
import re

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"


def encode_text(s):
    return base64.b64encode((s + "\0").encode("utf-16-le")).decode("ascii")


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert "\r\n" in text

    # 1. OutputString_11013 -> OutputString_STG1_Q01_ID
    text, n = re.subn(
        r'Name="OutputString_11013" ObjectName="OutputString_11013"',
        'Name="OutputString_STG1_Q01_ID" ObjectName="OutputString_STG1_Q01_ID"',
        text,
    )
    assert n == 1, f"OutputString_11013 rename matched {n} times"
    print("Renamed OutputString_11013 -> OutputString_STG1_Q01_ID")

    # 2. ObjectPointer_Status_27000 -> ObjectPointer_Status_STG1_Q01
    text, n = re.subn(
        r'ObjectName="ObjectPointer_Status_27000"',
        'ObjectName="ObjectPointer_Status_STG1_Q01"',
        text,
    )
    assert n == 1, f"ObjectPointer_Status_27000 rename matched {n} times"
    print("Renamed ObjectPointer_Status_27000 -> ObjectPointer_Status_STG1_Q01")

    # 3. Fix OutputString_STG1_Q1_name -> OutputString_STG1_Q01_name (already
    #    renamed once before the 2-digit rule was given).
    text, n = re.subn(
        r'Name="OutputString_STG1_Q1_name" ObjectName="OutputString_STG1_Q1_name"',
        'Name="OutputString_STG1_Q01_name" ObjectName="OutputString_STG1_Q01_name"',
        text,
    )
    assert n == 1, f"OutputString_STG1_Q1_name rename matched {n} times"
    print("Renamed OutputString_STG1_Q1_name -> OutputString_STG1_Q01_name")

    # 4. Two-line labels: OutputString_STGn_Qm (single digit m) -> Q0m, plus
    #    rewrite their visible "STGn\r\nQm" text to "STGn\r\nQ0m" so the label
    #    matches its own new name.
    count = 0
    for stg in range(1, 6):
        for m in range(1, 10):
            old_name = f"OutputString_STG{stg}_Q{m}"
            new_name = f"OutputString_STG{stg}_Q0{m}"
            old_text = f"STG{stg}\r\nQ{m}"
            new_text = f"STG{stg}\r\nQ0{m}"

            block_pat = re.compile(
                r'<Object Class="COutputText" Name="' + re.escape(old_name) +
                r'" ObjectName="' + re.escape(old_name) + r'" Pinned="FALSE" JVS-ID="(\d+)">.*?</Object>',
                re.DOTALL,
            )
            m_block = block_pat.search(text)
            assert m_block, f"block for {old_name} not found"
            block = m_block.group(0)

            # Normally 2 occurrences (Text + Value properties); some rows also mirror the
            # text into the Comment property (seen after the user's manual ISO-Designer
            # edit of the STG1/Q1 prototype), giving 3 - replace all of them either way.
            old_b64 = encode_text(old_text)
            hits = block.count(f"<![CDATA[{old_b64}]]>")
            assert hits in (2, 3), f"{old_name}: expected 2 or 3 occurrences of the old text CDATA, found {hits}"

            new_block = block.replace(f'Name="{old_name}" ObjectName="{old_name}"',
                                       f'Name="{new_name}" ObjectName="{new_name}"')
            new_block = new_block.replace(f"<![CDATA[{old_b64}]]>", f"<![CDATA[{encode_text(new_text)}]]>")

            text = text[: m_block.start()] + new_block + text[m_block.end():]
            count += 1

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"Renamed {count} two-line label objects to two-digit Q0m names and rewrote their text.")


if __name__ == "__main__":
    main()
