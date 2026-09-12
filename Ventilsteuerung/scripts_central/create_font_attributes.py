"""Create the full ISO 11783-6 Annex B standard FontAttributes size catalog.

Creates all 15 standard VT font sizes (6x8 .. 128x192), once for the DataMask ID
half (23000-23499) and once for the SoftKeyMask ID half (23500-23999) - see
GENERATIVER_POOL_PLAN.md Abschnitt 3 for the DataMask/SoftKeyMask block-splitting
convention. FontAttributes_23000 (24x32) and FontAttributes_23001 (12x16) already
exist (used by the HOME menu) and are reused/renamed rather than duplicated -
renumbering them would break existing references.
"""
import io
import re

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"

# (width, height) - ISO 11783-6 Annex B FontAttributes.FontSize enum, 0..14
SIZES = [
    (6, 8), (8, 8), (8, 12), (12, 16), (16, 16), (16, 24), (24, 32), (32, 32),
    (32, 48), (48, 64), (64, 64), (64, 96), (96, 128), (128, 128), (128, 192),
]


def emit_font(jid, object_name, width, height):
    point_width = round(width * 0.75)
    return (
        f'\t\t<Object Class="CFontStyle" JVS-ID="{jid}" ObjectName="{object_name}" Pinned="FALSE">\n'
        f'\t\t\t<PropertySheet Name="Font" ID="68816">\n'
        f'\t\t\t\t<Property Name="Name">\n\t\t\t\t\t<Value>Lucida Console</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Size">\n\t\t\t\t\t<Value>{width}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Height">\n\t\t\t\t\t<Value>{height}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Color">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Weight">\n\t\t\t\t\t<Value>400</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Italic">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Underline">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Strikeout">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="PointWidth">\n\t\t\t\t\t<Value>{point_width}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Width">\n\t\t\t\t\t<Value>{width}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Inverted">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="FlashInverted">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="FlashHidden">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Proportional">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="ISOFontType">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="ResourceID">\n\t\t\t\t\t<Value/>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Comment">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[AAA=]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t</PropertySheet>\n'
        f'\t\t</Object>\n'
    )


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        jop_text = f.read()
    assert "\r\n" in jop_text

    # Rename the two pre-existing fonts (reused, not duplicated).
    jop_text = jop_text.replace(
        'JVS-ID="23000" ObjectName="FontAttributes_23000"',
        'JVS-ID="23000" ObjectName="FontAttributes_24x32"',
        1,
    )
    existing = {(24, 32): 23000, (12, 16): 23001}

    existing_ids = [int(m) for m in re.findall(r'Class="CFontStyle"[^>]*?JVS-ID="(\d+)"', jop_text)]
    next_dm = max([i for i in existing_ids if i < 23500] + [22999]) + 1
    next_skm = max([i for i in existing_ids if 23500 <= i < 24000] + [23499]) + 1

    new_objects = []
    for width, height in SIZES:
        name = f"FontAttributes_{width}x{height}"
        if (width, height) in existing:
            continue  # DataMask copy already present, reused above
        new_objects.append(emit_font(next_dm, name, width, height))
        next_dm += 1

    for width, height in SIZES:
        name = f"FontAttributes_{width}x{height}_SKM"
        new_objects.append(emit_font(next_skm, name, width, height))
        next_skm += 1

    new_text = "".join(new_objects)
    insertion_marker = "\t</Objects>\r\n</JetView-ObjectPool>"
    assert insertion_marker in jop_text, "insertion point not found"
    jop_text = jop_text.replace(insertion_marker, new_text + insertion_marker, 1)

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(jop_text)

    print(f"Wrote {len(new_objects)} new FontAttributes objects "
          f"(+2 reused/renamed: 23000=24x32, 23001=12x16).")


if __name__ == "__main__":
    main()
