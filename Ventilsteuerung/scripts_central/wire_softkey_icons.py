"""Wire up real icons and softkey-mask placements for the Ausgaenge/
Eingaenge diagnostic pages' scroll navigation, per "dann die Object-Pointer
und Softkeys für das Scrollen, wie in der Vorlage" (Workspace_Scroll
template) plus the user's follow-up decisions:
- 8 keys per page (FIRST/PAGE_UP/UP/DOWN/PAGE_DOWN/LAST + Back/Lock, matching
  the template's Back/Lock slots), not just the 4 scroll buttons the
  template icons alone would cover.
- Two hardware key columns of 6 (12 total, matching this VT's physical
  layout) - 6 scroll keys in column 1 (Left=560, designators 0-5), Back/Lock
  in column 2 (Left=480, designators 6-7) - so every key stays at the
  template's native 80px height, no shrinking.
- FIRST/LAST have no icon in the template or in Images/ - newly created
  (FIRST.bmp/LAST.bmp, same 80x80 1bpp style: arrow + bar, see
  create_first_last_icons.py-equivalent inline generation this session).

What already existed before this script (from build_diagnostic_pages.py):
12 CSoftKey objects (UP/DOWN/PAGE_UP/PAGE_DOWN/FIRST/LAST x2 pages) each
with a placeholder "Icon" CProxy child pointing at the shared grey
Rectangle_RowBg-style rect (JVS-ID 14002), plus their ObjectPointer/CProxy
wrapper chains - already correctly resolved by GcfScript.py. This script:
1. Creates 8 shared CImage objects (one per icon, referenced from both
   pages via CProxy - same multi-instance pattern as HeaderBg etc.).
2. Retargets the 12 existing "Icon" CProxy placeholders from 14002 to the
   matching new CImage.
3. Creates the 4 new CSoftKey + CProxy + CProxy + CPointer chains needed
   for Back/Lock on both pages (these never existed before - only the 6
   scroll roles were pre-built).
4. Writes the <Components> section into both SoftKeyMask .jvi files
   (currently completely empty - no designators placed at all), using the
   template's Component/CPointer format.
"""
import argparse
import io
import os
import re

_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument(
    "-d", "--pool-dir", dest="pool_dir", required=True,
    help="ISO-Designer pool workspace folder, relative to this script's "
         "parent directory (i.e. relative to the project's Ventilsteuerung/ "
         "folder) - e.g. ISO-DesignerProjects/Workspace/DefaultPool",
)
_args, _ = _parser.parse_known_args()
_script_dir = os.path.dirname(os.path.abspath(__file__))
POOL_DIR = os.path.join(os.path.dirname(_script_dir), _args.pool_dir)
JOP_PATH = os.path.join(POOL_DIR, "DefaultPool.jop")
AUSGAENGE_JVI = os.path.join(POOL_DIR, "Diagnosis", "Ausgaenge", "AusgaengeSoftKeyMask.jvi")
EINGAENGE_JVI = os.path.join(POOL_DIR, "Diagnosis", "Eingaenge", "EingaengeSoftKeyMask.jvi")

PLACEHOLDER_RECT_ID = 14002

# role -> (icon bmp filename, CImage id)
ICON_SPECS = {
    "PAGE_UP":   "Arr_UP_UP.bmp",
    "UP":        "Arr_UP.bmp",
    "DOWN":      "Arr_DOWN.bmp",
    "PAGE_DOWN": "Arr_DOWN_DOWN.bmp",
    "FIRST":     "FIRST.bmp",
    "LAST":      "LAST.bmp",
    "Back":      "BACK.bmp",
    "Lock":      "LOCK.bmp",
}

# Existing (role -> icon-proxy JVS-ID) per page, from prior discovery.
EXISTING_ICON_PROXY = {
    "": {  # Ausgaenge
        "PAGE_UP": 4194770, "UP": 4194772, "DOWN": 4194774,
        "PAGE_DOWN": 4194776, "FIRST": 4194768, "LAST": 4194778,
    },
    "_1": {  # Eingaenge
        "PAGE_UP": 4195252, "UP": 4195254, "DOWN": 4195256,
        "PAGE_DOWN": 4195258, "FIRST": 4195250, "LAST": 4195260,
    },
}

# Column 1 (scroll keys, Left=560): designator 0-5, Top 0/80/.../400.
COLUMN1_ORDER = ["FIRST", "PAGE_UP", "UP", "DOWN", "PAGE_DOWN", "LAST"]
# Column 2 (Back/Lock, Left=480): designator 6-7, Top 0/80.
COLUMN2_ORDER = ["Back", "Lock"]


def emit_cimage(jid, name, bmp_filename):
    return (
        f'\t\t<Object Class="CImage" Name="Image" ObjectName="{name}" Pinned="FALSE" JVS-ID="{jid}">\r\n'
        f'\t\t\t<PropertySheet Name="Image">\r\n'
        f'\t\t\t\t<Property Name="Path">\r\n\t\t\t\t\t<Value>\r\n\t\t\t\t\t\t<![CDATA[.\\Images\\{bmp_filename}]]>\r\n\t\t\t\t\t</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="ResourceID">\r\n\t\t\t\t\t<Value/>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Retain Aspect Ratio">\r\n\t\t\t\t\t<Value>1</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Transparency">\r\n\t\t\t\t\t<Value>1</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="TransColor">\r\n\t\t\t\t\t<Value>16777215</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="ControlType">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="BitPerPixel">\r\n\t\t\t\t\t<Value>1</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="IsFlashing">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Encoding">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Extended">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="RealImageWidth">\r\n\t\t\t\t\t<Value>80</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="RealImageHeight">\r\n\t\t\t\t\t<Value>80</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="RotationAngle">\r\n\t\t\t\t\t<Value>0.000000</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Width">\r\n\t\t\t\t\t<Value>80</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Height">\r\n\t\t\t\t\t<Value>80</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Visible">\r\n\t\t\t\t\t<Value>1</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Locked">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Comment">\r\n\t\t\t\t\t<Value>\r\n\t\t\t\t\t\t<![CDATA[AAA=]]>\r\n\t\t\t\t\t</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Disabled">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t</PropertySheet>\r\n'
        f'\t\t</Object>\r\n'
    )


def emit_softkey(jid, objname, icon_proxy_id):
    return (
        f'\t\t<Object Class="CSoftKey" Name="SoftKey" ObjectName="{objname}" Pinned="FALSE" JVS-ID="{jid}">\r\n'
        f'\t\t\t<PropertySheet Name="SoftKey">\r\n'
        f'\t\t\t\t<Property Name="BackColor">\r\n\t\t\t\t\t<Value>13421772</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="KeyCode">\r\n\t\t\t\t\t<Value>1</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Hotkey">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Width">\r\n\t\t\t\t\t<Value>80</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Height">\r\n\t\t\t\t\t<Value>80</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Visible">\r\n\t\t\t\t\t<Value>1</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Comment">\r\n\t\t\t\t\t<Value>\r\n\t\t\t\t\t\t<![CDATA[AAA=]]>\r\n\t\t\t\t\t</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Disabled">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="ExternalReferenceAllowed">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t</PropertySheet>\r\n'
        f'\t\t\t<Objects>\r\n\t\t\t\t<Object JVS-ID="{icon_proxy_id}"/>\r\n\t\t\t</Objects>\r\n'
        f'\t\t</Object>\r\n'
    )


def emit_named_proxy(jid, name, target_id):
    return (
        f'\t\t<Object Class="CProxy" Name="{name}" ObjectName="" Pinned="FALSE" JVS-ID="{jid}">\r\n'
        f'\t\t\t<PropertySheet Name="Proxy">\r\n'
        f'\t\t\t\t<Property Name="Top">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Left">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Name">\r\n\t\t\t\t\t<Value>{name}</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="TabIndex">\r\n\t\t\t\t\t<Value>-1</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Transform">\r\n\t\t\t\t\t<Value>(1.0000000000000000)(0.0000000000000000)(0.0000000000000000)(0.0000000000000000)(1.0000000000000000)(0.0000000000000000)</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t</PropertySheet>\r\n'
        f'\t\t\t<Objects>\r\n\t\t\t\t<Object JVS-ID="{target_id}"/>\r\n\t\t\t</Objects>\r\n'
        f'\t\t</Object>\r\n'
    )


def emit_objectpointer(jid, objname, target_id):
    return (
        f'\t\t<Object Class="CPointer" Name="Pointer" ObjectName="{objname}" Pinned="FALSE" JVS-ID="{jid}">\r\n'
        f'\t\t\t<PropertySheet Name="Pointer">\r\n'
        f'\t\t\t\t<Property Name="Visible">\r\n\t\t\t\t\t<Value>1</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Locked">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Comment">\r\n\t\t\t\t\t<Value>\r\n\t\t\t\t\t\t<![CDATA[AAA=]]>\r\n\t\t\t\t\t</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="Disabled">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t\t<Property Name="ExternalReferenceAllowed">\r\n\t\t\t\t\t<Value>0</Value>\r\n\t\t\t\t</Property>\r\n'
        f'\t\t\t</PropertySheet>\r\n'
        f'\t\t\t<Objects>\r\n\t\t\t\t<Object JVS-ID="{target_id}"/>\r\n\t\t\t</Objects>\r\n'
        f'\t\t</Object>\r\n'
    )


def main():
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        jop_text = f.read()
    assert "\r\n" in jop_text

    next_cimage = 20008
    next_softkey = 5014
    next_pointer = 27136
    next_proxy = 4195262

    new_objects = []
    cimage_id = {}
    for role, bmp in ICON_SPECS.items():
        jid = next_cimage
        next_cimage += 1
        cimage_id[role] = jid
        name = f"PictureGraphic_{role}"
        new_objects.append(emit_cimage(jid, name, bmp))

    # Retarget the 12 pre-existing "Icon" proxies (scroll roles only) from
    # the grey placeholder rect to their matching new CImage.
    retarget_count = 0
    for suffix, roles in EXISTING_ICON_PROXY.items():
        for role, proxy_id in roles.items():
            old_tag = f'<Object JVS-ID="{PLACEHOLDER_RECT_ID}"/>'
            block_pat = re.compile(
                r'<Object Class="CProxy" Name="Icon" ObjectName="" Pinned="FALSE" JVS-ID="' + str(proxy_id) + r'">.*?</Object>\r\n',
                re.DOTALL,
            )
            m = block_pat.search(jop_text)
            assert m, f"Icon proxy {proxy_id} ({role}{suffix}) not found"
            block = m.group(0)
            assert old_tag in block, f"Icon proxy {proxy_id} ({role}{suffix}) does not target {PLACEHOLDER_RECT_ID}"
            new_block = block.replace(old_tag, f'<Object JVS-ID="{cimage_id[role]}"/>')
            jop_text = jop_text[: m.start()] + new_block + jop_text[m.end():]
            retarget_count += 1

    # Back/Lock: build new CSoftKey + Icon-CProxy + SoftKey-CProxy + ObjectPointer
    # chains for both pages.
    objectpointer_id = {"": {}, "_1": {}}
    for suffix in ("", "_1"):
        for role in ("Back", "Lock"):
            icon_proxy_id = next_proxy
            next_proxy += 1
            new_objects.append(emit_named_proxy(icon_proxy_id, "Icon", cimage_id[role]))

            softkey_id = next_softkey
            next_softkey += 1
            new_objects.append(emit_softkey(softkey_id, f"SoftKey_{role}{suffix}", icon_proxy_id))

            wrapper_proxy_id = next_proxy
            next_proxy += 1
            new_objects.append(emit_named_proxy(wrapper_proxy_id, f"SoftKey_{role}", softkey_id))

            ptr_id = next_pointer
            next_pointer += 1
            new_objects.append(emit_objectpointer(ptr_id, f"ObjectPointer_SoftKey_{role}{suffix}", wrapper_proxy_id))
            objectpointer_id[suffix][role] = ptr_id

    new_text = "".join(new_objects)
    marker = "\t</Objects>\r\n</JetView-ObjectPool>"
    assert marker in jop_text, "insertion marker not found"
    jop_text = jop_text.replace(marker, new_text + marker, 1)

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(jop_text)

    print(f"Created {len(cimage_id)} CImage objects, retargeted {retarget_count} icon proxies, "
          f"created {2 * 2} Back/Lock softkey chains.")

    # Existing scroll-role ObjectPointer IDs, for the .jvi Components.
    existing_ptr_id = {
        "": {"PAGE_UP": 27061, "UP": 27062, "DOWN": 27063, "PAGE_DOWN": 27064, "FIRST": 27060, "LAST": 27065},
        "_1": {"PAGE_UP": 27131, "UP": 27132, "DOWN": 27133, "PAGE_DOWN": 27134, "FIRST": 27130, "LAST": 27135},
    }

    def build_components(suffix, id_seed):
        parts = []
        zorder = 0
        comp_id = id_seed
        for i, role in enumerate(COLUMN1_ORDER):
            top = i * 80
            ptr_id = existing_ptr_id[suffix][role]
            parts.append(emit_component(comp_id, zorder, top, 560, i, ptr_id))
            comp_id += 1
            zorder += 1
        for i, role in enumerate(COLUMN2_ORDER):
            top = i * 80
            designator = 6 + i
            ptr_id = objectpointer_id[suffix][role]
            parts.append(emit_component(comp_id, zorder, top, 480, designator, ptr_id))
            comp_id += 1
            zorder += 1
        return "".join(parts)

    def emit_component(comp_id, zorder, top, left, designator, ptr_id):
        return (
            f'\t\t<Component ID="{comp_id}" Class="CPointer" Name="Pointer">\r\n'
            f'\t\t\t<PropertySheets>\r\n'
            f'\t\t\t\t<PropertySheet Name="General">\r\n'
            f'\t\t\t\t\t<Property Name="ZOrder">\r\n\t\t\t\t\t\t<Value>{zorder}</Value>\r\n\t\t\t\t\t</Property>\r\n'
            f'\t\t\t\t</PropertySheet>\r\n'
            f'\t\t\t\t<PropertySheet Name="Proxy">\r\n'
            f'\t\t\t\t\t<Property Name="Top">\r\n\t\t\t\t\t\t<Value>{top}</Value>\r\n\t\t\t\t\t</Property>\r\n'
            f'\t\t\t\t\t<Property Name="Left">\r\n\t\t\t\t\t\t<Value>{left}</Value>\r\n\t\t\t\t\t</Property>\r\n'
            f'\t\t\t\t\t<Property Name="Transform">\r\n\t\t\t\t\t\t<Value>(1.0000000000000000)(0.0000000000000000)({left}.0000000000000000)(0.0000000000000000)(1.0000000000000000)({top}.0000000000000000)</Value>\r\n\t\t\t\t\t</Property>\r\n'
            f'\t\t\t\t\t<Property Name="ReferencedObjectForMask">\r\n\t\t\t\t\t\t<Value>-1</Value>\r\n\t\t\t\t\t</Property>\r\n'
            f'\t\t\t\t\t<Property Name="SoftkeymaskDesignatorNo">\r\n\t\t\t\t\t\t<Value>{designator}</Value>\r\n\t\t\t\t\t</Property>\r\n'
            f'\t\t\t\t</PropertySheet>\r\n'
            f'\t\t\t</PropertySheets>\r\n'
            f'\t\t\t<Objects>\r\n\t\t\t\t<Object JVS-ID="{ptr_id}"/>\r\n\t\t\t</Objects>\r\n'
            f'\t\t</Component>\r\n'
        )

    for jvi_path, suffix, id_seed in ((AUSGAENGE_JVI, "", 900000001), (EINGAENGE_JVI, "_1", 900000101)):
        with io.open(jvi_path, "r", encoding="utf-8", newline="") as f:
            jvi_text = f.read()
        assert "\r\n" in jvi_text
        assert "<Components>" not in jvi_text, f"{jvi_path} already has Components"
        components_xml = "\t<Components>\r\n" + build_components(suffix, id_seed) + "\t</Components>\r\n"
        jvi_text = jvi_text.replace("</JetView-Document>", components_xml + "</JetView-Document>")
        with io.open(jvi_path, "w", encoding="utf-8", newline="") as f:
            f.write(jvi_text)
        print(f"Wrote Components to {jvi_path}")


if __name__ == "__main__":
    main()
