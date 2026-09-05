from argparse import ArgumentParser
import glob
import os
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Security Audit.

def getPaths():
    script_path = os.path.dirname(os.path.abspath(__file__))
    parser = ArgumentParser()
    parser.add_argument("-o", "--oldfile", dest="old_file", required=True)
    parser.add_argument("-n", "--newfile", dest="new_file", required=True)
    parser.add_argument("-p", "--newfolder", dest="new_folder", required=True)
    parser.add_argument("-k", "--package", dest="package", required=True)
    parser.add_argument("-j", "--jopfile", dest="jop_file", required=False, default=None)
    args = parser.parse_args()

    # Create the absolute paths using os.path.join
    new_path = os.path.join(os.path.dirname(script_path), args.new_folder)
    old_path = os.path.join(os.path.dirname(script_path), args.old_file)
    jop_path = os.path.join(os.path.dirname(script_path), args.jop_file) if args.jop_file else None

    filepaths = [old_path, new_path, args.new_file, args.package, jop_path]
    return filepaths

def printPaths(filepaths):
    print('')
    print('')
    print(f"Old File:     {filepaths[0]}")
    print(f"New Folder:   {filepaths[1]}")
    print(f"New File:     {filepaths[2]}")
    if filepaths[4]:
        print(f"Jop File:     {filepaths[4]}")

def checkPath(path):
    if os.path.exists(path):
        print(f'Path exists : {path}')
    else:
        raise FileNotFoundError(f"The new file '{path}' does not exist.")

def safe_output_path(folder, filename):
    """Join folder/filename for writing, and verify the result actually stays inside folder.

    filename is built from CLI-supplied arguments (--newfile plus a fixed suffix); this guards
    against it accidentally (or via a malformed CLI invocation) containing ".." or an absolute
    path component that would otherwise let a write escape the intended --newfolder directory.
    """
    folder = os.path.realpath(folder)
    candidate = os.path.realpath(os.path.join(folder, filename))
    if os.path.commonpath([folder, candidate]) != folder:
        raise ValueError(f"Refusing to write outside of '{folder}': '{candidate}'")
    return candidate

def compute_rename_map(definitions):
    """For names that end with _<value> (numeric), strip the suffix if the result is unique.

    Returns {original_name: stripped_name} only for unambiguous renames.
    Prints a warning for cases where two names would produce the same stripped name.
    """
    all_names = set(definitions.keys())
    candidate_to_originals = {}

    for name, value_str in definitions.items():
        try:
            int(value_str)
        except ValueError:
            continue
        suffix = '_' + value_str
        if name.endswith(suffix) and len(name) > len(suffix):
            candidate = name[:-len(suffix)]
            candidate_to_originals.setdefault(candidate, []).append(name)

    rename_map = {}
    for candidate, originals in sorted(candidate_to_originals.items()):
        if len(originals) != 1:
            print(f"  Skip rename to '{candidate}': ambiguous ({', '.join(sorted(originals))})")
            continue
        original = originals[0]
        # Candidate must not already exist as a different, non-renamed name
        if candidate in all_names and candidate != original:
            print(f"  Skip rename '{original}' -> '{candidate}': conflicts with existing name")
            continue
        rename_map[original] = candidate
        print(f"  Rename: '{original}' -> '{candidate}'")

    return rename_map

def readIOPH(filepaths):
    oldfilepath   = filepaths[0]
    newfilepath   = filepaths[1]

    print("Oldfilepath")
    checkPath(oldfilepath)
    print("Newfilepath")
    checkPath(newfilepath)

    pattern = re.compile(r'#define\s+(\w+)\s+(\S+)')
    definitions = {}
    with open(oldfilepath, 'r') as file:
        for line in file:
            match = pattern.match(line)
            if match:
                name, number = match.groups()
                definitions[name] = number

    rename_map = compute_rename_map(definitions)

    renamed = {rename_map.get(name, name): value for name, value in definitions.items()}
    return renamed, rename_map

def create_numeric_info(obj_id, scale, offset, decimals):
    """Factory to create a numeric info dictionary."""
    return {
        "id":       obj_id,
        "scale":    scale,
        "offset":   offset,
        "decimals": decimals,
    }

def readJOP(jop_filepath):
    """Parse a JetViewSoft .jop XML file and extract InputNumber and OutputNumber objects.

    Returns a dict keyed by ObjectName:
        { "InputNumber_I1": {"id": 9000, "scale": 1.0, "offset": 0, "decimals": 0}, ... }
    """
    tree = ET.parse(jop_filepath)
    root = tree.getroot()
    objects_container = root.find("Objects")
    if objects_container is None:
        return {}

    # Pre-scan for names to avoid alias collisions
    var_names = {}
    primary_names = set()
    for obj in objects_container.findall("Object"):
        cls = obj.get("Class")
        if cls == "CNumberVariable":
            v_id = obj.get("JVS-ID")
            v_name = obj.get("ObjectName")
            if v_id and v_name:
                var_names[v_id] = v_name
        elif cls in ("CInputNumber", "COutputNumber"):
            name = obj.get("ObjectName")
            if name:
                primary_names.add(name)

    result = {}

    for obj in objects_container.findall("Object"):
        cls = obj.get("Class")
        if cls not in ("CInputNumber", "COutputNumber"):
            continue

        name = obj.get("ObjectName")
        jvs_id = obj.get("JVS-ID")
        if not name or not jvs_id:
            continue

        # Extract properties from the PropertySheet children
        props = {}
        for prop in obj.iter("Property"):
            prop_name = prop.get("Name")
            value_el = prop.find("Value")
            if prop_name and value_el is not None and value_el.text:
                props[prop_name] = value_el.text.strip()

        obj_id   = int(jvs_id)
        scale    = float(props.get("Scale", "1"))
        offset   = int(props.get("Offset", "0"))
        decimals = int(props.get("NoOfDecimals", "0"))

        # The alias uses the parent object's scale/offset/decimals, since
        # CNumberVariable itself carries no scaling properties.
        info = create_numeric_info(obj_id, scale, offset, decimals)
        result[name] = info

        # Alias logic: if this object references a NumberVariable, create an alias.
        # This allows writing to the variable name directly in the application.
        objs_elem = obj.find("Objects")
        if objs_elem is not None:
            for child_obj in objs_elem.findall("Object"):
                child_id = child_obj.get("JVS-ID")
                if not child_id:
                    continue
                if child_id in var_names:
                    alias_name = var_names[child_id]
                    # Protect primary object names from being overwritten by aliases.
                    if alias_name in primary_names:
                        print(f"  Skip alias '{alias_name}': conflicts with primary object name")
                        continue
                    
                    # Guard against physically meaningless zero scales.
                    if scale == 0.0:
                        continue
                    
                    # If multiple objects point to the same variable, prefer the one with the smaller
                    # absolute scale factor (usually the base SI unit or the highest precision).
                    # The alias should use the ID of the NumberVariable itself (child_id).
                    alias_id = int(child_id)
                    if alias_name not in result:
                        result[alias_name] = create_numeric_info(alias_id, scale, offset, decimals)
                    else:
                        # Compare absolute values to correctly handle negative scales.
                        current_scale = result[alias_name]["scale"]
                        if abs(scale) < abs(current_scale):
                            print(f"  Update alias '{alias_name}': scale {current_scale} -> {scale}")
                            result[alias_name] = create_numeric_info(alias_id, scale, offset, decimals)

    return result

def update_jop_objectnames(jop_path, rename_map):
    """Replace ObjectName="old" with ObjectName="new" in the .jop XML file (in-place, idempotent)."""
    if not rename_map:
        return

    with open(jop_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    changed = []
    for old_name, new_name in rename_map.items():
        search = f'ObjectName="{old_name}"'
        replacement = f'ObjectName="{new_name}"'
        if search in new_content:
            new_content = new_content.replace(search, replacement)
            changed.append(f"  {old_name} -> {new_name}")

    if changed:
        with open(jop_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated ObjectNames in {jop_path}:")
        for c in changed:
            print(c)
    else:
        print(f"No ObjectName changes needed in {jop_path}")

def writeGCFfile(data, filepaths):
    newfilepath = safe_output_path(filepaths[1], filepaths[2]+'.gcf')

    root = ET.Element("GlobalConstants", Name=filepaths[2], Comment="Global constants")

    compiler_info = ET.SubElement(root, "CompilerInfo")
    compiler_info.set("packageName", filepaths[3])

    global_constants = ET.SubElement(root, "GlobalConstants")

    for name, value in data.items():
        var_declaration = ET.SubElement(global_constants, "VarDeclaration", Name=name, Type="UINT", InitialValue=value)

        if name == 'ISO_VERSION_LABEL':
            var_declaration.set('Type', 'STRING')
            var_declaration.set('InitialValue', '')

    # Create an ElementTree object and write it to a file
    tree = ET.ElementTree(root)

    # Create a string with indentation
    xml_str = ET.tostring(root, encoding='utf-8').decode()
    xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")

    # Adding UTF8-encoding
    xml_str = xml_str[:19] + ' ' + 'encoding="UTF-8"' + xml_str[20:]

    # Write the formatted XML to a file
    with open(newfilepath, "w") as file:
        file.write(xml_str)

def _format_real(value):
    """Format a float as an IEC 61131-3 REAL literal (no scientific notation)."""
    val = float(value)
    s = f"{val:.10f}".rstrip('0')
    if s.endswith('.'):
        s += '0'
    return s

NUMERIC_NAME_SUFFIX = "_N"

def writeNumericGCFfile(data, filepaths):
    """Write a <name>_Numeric.gcf with NumericObjectPool_S constants for each InputNumber/OutputNumber.

    Each constant name gets NUMERIC_NAME_SUFFIX appended, since the plain name is
    already used by the UINT constant of the same name in the non-numeric .gcf
    (same package) - without the suffix, 4diac's name resolution collides.
    """
    newfilepath = safe_output_path(filepaths[1], filepaths[2] + '_Numeric.gcf')
    gcf_name    = filepaths[2] + '_Numeric'
    package     = filepaths[3]
    struct_type = "logiBUS::utils::conversion::phys::NumericObjectPool_S"

    root = ET.Element("GlobalConstants", Name=gcf_name, Comment="Numeric object pool constants (ID, Scale, Offset, Decimals)")

    compiler_info = ET.SubElement(root, "CompilerInfo")
    compiler_info.set("packageName", package)

    global_constants = ET.SubElement(root, "GlobalConstants")

    for name, info in sorted(data.items(), key=lambda x: x[1]["id"]):
        scale_str    = _format_real(info["scale"])
        offset_str   = str(info["offset"])
        decimals_str = str(info["decimals"])
        obj_id_str   = str(info["id"])

        initial_value = (
            f"(u16ObjId := {obj_id_str}, "
            f"r32Scale := {scale_str}, "
            f"i32Offset := {offset_str}, "
            f"u8Decimals := {decimals_str})"
        )

        ET.SubElement(
            global_constants,
            "VarDeclaration",
            Name=name + NUMERIC_NAME_SUFFIX,
            Type=struct_type,
            InitialValue=initial_value,
        )

    xml_str = ET.tostring(root, encoding='utf-8').decode()
    xml_str = minidom.parseString(xml_str).toprettyxml(indent="\t")
    xml_str = xml_str[:19] + ' ' + 'encoding="UTF-8"' + xml_str[20:]

    with open(newfilepath, "w") as file:
        file.write(xml_str)

    print(f"Written: {newfilepath}")


def _get_prop(obj, prop_name):
    """Read a top-level <Property Name="..."><Value>...</Value></Property> from a .jop Object element."""
    for prop in obj.iter("Property"):
        if prop.get("Name") == prop_name:
            value_el = prop.find("Value")
            if value_el is not None and value_el.text:
                return value_el.text.strip()
    return None


def _resolve_proxy_target(proxy_obj, by_id):
    """Follow a CProxy's own <Objects><Object JVS-ID="X"/></Objects> to the real target Object element."""
    objs_el = proxy_obj.find("Objects")
    if objs_el is None:
        return None
    target_ref = objs_el.find("Object")
    if target_ref is None:
        return None
    return by_id.get(target_ref.get("JVS-ID"))


def _get_jvi_property(jvi_root, prop_name):
    """Read a <PropertySheets><PropertySheet><Property Name="..."><Value> from a .jvi root element."""
    sheets = jvi_root.find("PropertySheets")
    if sheets is None:
        return None
    for sheet in sheets.findall("PropertySheet"):
        for prop in sheet.findall("Property"):
            if prop.get("Name") == prop_name:
                val = prop.find("Value")
                if val is not None and val.text:
                    return val.text.strip()
    return None


def _find_hosting_jvi(jop_dir, object_jvs_id):
    """Find the .jvi file in jop_dir whose <Components> places object_jvs_id directly.

    Returns (jvi_path, jvi_root) or (None, None) if not found in any .jvi in jop_dir.
    """
    for jvi_path in glob.glob(os.path.join(jop_dir, "*.jvi")):
        root = ET.parse(jvi_path).getroot()
        components = root.find("Components")
        if components is None:
            continue
        for comp in components.findall("Component"):
            objs = comp.find("Objects")
            if objs is None:
                continue
            for obj_ref in objs.findall("Object"):
                if obj_ref.get("JVS-ID") == str(object_jvs_id):
                    return jvi_path, root
    return None, None


BUTTON_ROLE_KEYWORDS = [
    # Check the more specific "fast/page" keywords before the plain up/down ones, so
    # e.g. a "SoftKey_UP_UP" or "PageUp" object name isn't also claimed by the generic
    # "up" role. Both the original terse naming (UP_UP/DOWN_DOWN) and the "nicer"
    # PAGE_UP/PAGE_DOWN naming are recognized, since ISO-Designer object names and the
    # FB's own event names are independent naming spaces.
    ("u16BtnPageUpId", ("pageup", "page_up", "up_up")),
    ("u16BtnPageDownId", ("pagedown", "page_down", "down_down")),
    ("u16BtnTopId", ("top", "first")),
    ("u16BtnBottomId", ("bottom", "last")),
    ("u16BtnUpId", ("up",)),
    ("u16BtnDownId", ("down",)),
]


def _resolve_to_real_object(obj_id, by_id, max_hops=5):
    """Follow CPointer/CProxy indirection (obj's own <Objects> single child) until a
    non-pointer, non-proxy object is reached.

    A SoftKeyMask's children are typically ObjectPointer objects (Annex B.5), which point
    at a CProxy, which in turn wraps the real Key object - so resolving "the softkey
    behind this SoftKeyMask child" is normally a 2-hop walk, but this also transparently
    handles a SoftKeyMask child that's already a direct Key object (0 hops).

    Returns (real_id, real_obj), or (None, None) if unresolvable within max_hops.
    """
    current_id = obj_id
    for _ in range(max_hops):
        obj = by_id.get(current_id)
        if obj is None:
            return None, None
        if obj.get("Class") not in ("CPointer", "CProxy"):
            return current_id, obj
        target = _resolve_proxy_target(obj, by_id)
        if target is None:
            return None, None
        current_id = target.get("JVS-ID")
    return None, None


def _match_button_roles(candidates):
    """Match a list of (pointer_id, key_id, object_name) candidates to the 6
    ScrollControls_S button roles by keyword in the object name (case-insensitive).
    `object_name` is the name of the SoftKeyMask child itself (normally an
    ObjectPointer, which is where the descriptive naming lives - see
    _resolve_to_real_object), `key_id` is its resolved real Key object.

    Each candidate is used for at most one role. Returns (roles, pointer_roles,
    unmatched_candidates):
      - roles: role field -> matched key_id (str) or None - this is what Softkey_IE
        needs (u16ObjId must be the real Key, not the ObjectPointer).
      - pointer_roles: role field -> matched pointer_id (str) or None - kept
        separately since the ObjectPointer itself is needed for a later feature
        (redirecting/hiding the softkey icon when scroll is at a limit), even though
        it's not part of ScrollControls_S yet.
    """
    remaining = list(candidates)
    roles = {}
    pointer_roles = {}
    for field, keywords in BUTTON_ROLE_KEYWORDS:
        match = None
        for cand in remaining:
            _, _, cand_name = cand
            lname = (cand_name or "").lower()
            if any(kw in lname for kw in keywords):
                match = cand
                break
        if match:
            pointer_id, key_id, _ = match
            roles[field] = key_id
            pointer_roles[field] = pointer_id
            remaining.remove(match)
        else:
            roles[field] = None
            pointer_roles[field] = None
    return roles, pointer_roles, remaining


def _find_scroll_button_controls(jop_dir, jop_root, by_id, list_parent_id):
    """Trace list_parent_id -> hosting mask .jvi -> its SoftKeyMask JVS-ID -> that
    SoftKeyMask's own .jvi -> candidate SoftKeyMask children (normally ObjectPointer
    objects, Annex B.5) -> resolved real Key object behind each (see
    _resolve_to_real_object), then match candidates to the 6 ScrollControls_S button
    roles by the ObjectPointer's name (that's where the descriptive naming lives, e.g.
    "ObjectPointer_SoftKey_DOWN" pointing at real Key object "SoftKey_DOWN").

    Returns (roles, pointer_roles, warnings_list):
      - roles: all 6 ScrollControls_S fields -> resolved real Key JVS-ID (int) or None.
        This is what Softkey_IE.u16ObjId needs - NOT the ObjectPointer's own ID.
      - pointer_roles: same 6 fields -> the ObjectPointer's own JVS-ID (int) or None.
        Not part of ScrollControls_S (yet) - kept for a later feature (redirecting the
        ObjectPointer to hide/change the softkey icon when scroll is at a limit).
    """
    roles = {field: None for field, _ in BUTTON_ROLE_KEYWORDS}
    pointer_roles = {field: None for field, _ in BUTTON_ROLE_KEYWORDS}
    warnings = []

    mask_jvi_path, mask_jvi_root = _find_hosting_jvi(jop_dir, list_parent_id)
    if mask_jvi_root is None:
        warnings.append("could not find a .jvi mask hosting the list parent container "
                         "- button IDs left as ID_NULL placeholders")
        return roles, pointer_roles, warnings

    softkeymask_id = _get_jvi_property(mask_jvi_root, "SoftKeyMask")
    if not softkeymask_id or softkeymask_id == "-1":
        warnings.append(f"hosting mask ({os.path.basename(mask_jvi_path)}) has no "
                         "associated SoftKeyMask - button IDs left as ID_NULL placeholders")
        return roles, pointer_roles, warnings

    skm_obj = by_id.get(softkeymask_id)
    if skm_obj is None:
        warnings.append(f"SoftKeyMask object {softkeymask_id} not found in .jop "
                         "- button IDs left as ID_NULL placeholders")
        return roles, pointer_roles, warnings

    skm_jvi_rel = _get_prop(skm_obj, "Path")
    if not skm_jvi_rel:
        warnings.append(f"SoftKeyMask object {softkeymask_id} has no Path property "
                         "- button IDs left as ID_NULL placeholders")
        return roles, pointer_roles, warnings

    skm_jvi_path = os.path.join(jop_dir, skm_jvi_rel.lstrip(".\\/"))
    if not os.path.exists(skm_jvi_path):
        warnings.append(f"SoftKeyMask .jvi file not found: {skm_jvi_path} "
                         "- button IDs left as ID_NULL placeholders")
        return roles, pointer_roles, warnings

    skm_root = ET.parse(skm_jvi_path).getroot()
    components = skm_root.find("Components")
    if components is None:
        warnings.append(f"{os.path.basename(skm_jvi_path)} has no <Components> "
                         "- button IDs left as ID_NULL placeholders")
        return roles, pointer_roles, warnings

    candidates = []
    for comp in components.findall("Component"):
        objs = comp.find("Objects")
        if objs is None:
            continue
        for obj_ref in objs.findall("Object"):
            pointer_id = obj_ref.get("JVS-ID")
            pointer_obj = by_id.get(pointer_id)
            name = pointer_obj.get("ObjectName") if pointer_obj is not None else ""
            key_id, _key_obj = _resolve_to_real_object(pointer_id, by_id)
            candidates.append((pointer_id, key_id, name))

    if not candidates:
        warnings.append(f"SoftKeyMask {softkeymask_id} ({os.path.basename(skm_jvi_path)}) "
                         "has no child objects - button IDs left as ID_NULL placeholders")
        return roles, pointer_roles, warnings

    unresolved = [(pid, name) for pid, kid, name in candidates if kid is None]
    if unresolved:
        names = ", ".join(f"{pid}:{name or '?'}" for pid, name in unresolved)
        warnings.append(f"could not resolve the real Key object behind {len(unresolved)} "
                         f"SoftKeyMask child(ren) ({names}) - excluded from role matching")
    candidates = [c for c in candidates if c[1] is not None]

    matched_roles, matched_pointers, unmatched = _match_button_roles(candidates)
    roles = {field: (int(v) if v is not None else None) for field, v in matched_roles.items()}
    pointer_roles = {field: (int(v) if v is not None else None) for field, v in matched_pointers.items()}

    missing = [field for field, v in roles.items() if v is None]
    if missing:
        warnings.append(
            f"could not match a candidate for: {', '.join(missing)} (found "
            f"{len(candidates)} resolvable objects on SoftKeyMask {softkeymask_id}, none "
            "of their names matched the expected keywords - left as ID_NULL, rename in "
            "ISO-Designer and rerun, or fill in by hand)")
    if unmatched:
        names = ", ".join(f"{pid}:{name or '?'}" for pid, kid, name in unmatched)
        warnings.append(f"{len(unmatched)} object(s) on SoftKeyMask {softkeymask_id} were "
                         f"not claimed by any role ({names}) - e.g. a 'Back' key is expected here")

    return roles, pointer_roles, warnings


def readScrollJOP(jop_filepath):
    """Parse a .jop file and extract scroll-list geometry into ScrollObjectPool_S data.

    Detects a scroll list by four CGroup ObjectNames ending in "_Scrolling_Parent",
    "_Scrolling_Content", "_Scrollbar_Parent", "_Scrollbar_Content" (see SCROLL_KONZEPT.md
    in Workspace_Scroll). Only the single-scroll-list-per-pool case is supported; if more
    than one candidate is found for any suffix, generation is skipped with a warning
    (multi-list prefix pairing is not implemented, since real object names in this project
    are not guaranteed to share a consistent prefix - e.g. "Containerr_Scrolling_Parent" vs
    "Container_Scrolling_Content").

    Returns a dict keyed by a name derived from the content container's ObjectName:
        { "Container": {"list_parent_id": 3006, "list_content_id": 3031, "row_height": 42,
                         "bar_parent_id": 3000, "bar_content_id": 3010, "bar_base_offset": -252,
                         "bar_travel": 252, "pos_max": 13, "step": 6}, ... }
    """
    jop_dir = os.path.dirname(jop_filepath)
    tree = ET.parse(jop_filepath)
    root = tree.getroot()
    objects_container = root.find("Objects")
    if objects_container is None:
        return {}

    all_objects = objects_container.findall("Object")
    by_name = {}
    by_id = {}
    for obj in all_objects:
        cls = obj.get("Class")
        if not cls:
            continue
        jvs_id = obj.get("JVS-ID")
        if jvs_id:
            by_id[jvs_id] = obj
        name = obj.get("ObjectName")
        if name:
            by_name[name] = obj

    def names_ending(suffix):
        return [n for n in by_name if n.endswith(suffix)]

    list_parents  = names_ending("_Scrolling_Parent")
    list_contents = names_ending("_Scrolling_Content")
    bar_parents   = names_ending("_Scrollbar_Parent")
    bar_contents  = names_ending("_Scrollbar_Content")

    if not (list_parents and list_contents and bar_parents and bar_contents):
        return {}

    if max(len(list_parents), len(list_contents), len(bar_parents), len(bar_contents)) > 1:
        print("  Warning: multiple scroll lists detected in this pool - prefix-based "
              "pairing is not implemented, skipping scroll struct generation.")
        return {}

    list_parent_obj  = by_name[list_parents[0]]
    list_content_obj = by_name[list_contents[0]]
    bar_parent_obj    = by_name[bar_parents[0]]
    bar_content_obj   = by_name[bar_contents[0]]

    list_parent_id  = int(list_parent_obj.get("JVS-ID"))
    list_content_id = int(list_content_obj.get("JVS-ID"))
    bar_parent_id    = int(bar_parent_obj.get("JVS-ID"))
    bar_content_id   = int(bar_content_obj.get("JVS-ID"))

    list_parent_height  = int(_get_prop(list_parent_obj, "Height") or 0)
    list_content_height = int(_get_prop(list_content_obj, "Height") or 0)
    bar_parent_height    = int(_get_prop(bar_parent_obj, "Height") or 0)

    # Row height = vertical spacing between rows (Top of row 2 minus Top of row 1 as
    # positioned inside ListContent), NOT a row container's own Height property - rows
    # are typically drawn shorter than their spacing to leave a visible gap between them.
    row_tops = {}
    lc_children = list_content_obj.find("Objects")
    if lc_children is not None:
        for child_ref in lc_children.findall("Object"):
            proxy_obj = by_id.get(child_ref.get("JVS-ID"))
            if proxy_obj is None:
                continue
            target_obj = _resolve_proxy_target(proxy_obj, by_id)
            if target_obj is None:
                continue
            target_name = target_obj.get("ObjectName") or ""
            m = re.search(r'_Row_0*([12])$', target_name)
            if m:
                top_val = _get_prop(proxy_obj, "Top")
                if top_val:
                    row_tops[int(m.group(1))] = int(top_val)

    row_height = None
    if 1 in row_tops and 2 in row_tops:
        row_height = row_tops[2] - row_tops[1]

    if not row_height:
        print("  Warning: could not determine row height (need '*_Row_01' and '*_Row_02' "
              "containers positioned inside the list content) - skipping scroll struct "
              "generation.")
        return {}

    pos_max = max(0, (list_content_height - list_parent_height) // row_height)
    step = max(1, list_parent_height // row_height)

    # Scrollbar indicator height: BarContent's single child proxy -> its real target -> Height.
    indicator_height = None
    bc_children = bar_content_obj.find("Objects")
    if bc_children is not None:
        child_ref = bc_children.find("Object")
        if child_ref is not None:
            proxy_obj = by_id.get(child_ref.get("JVS-ID"))
            if proxy_obj is not None:
                target_obj = _resolve_proxy_target(proxy_obj, by_id)
                if target_obj is not None:
                    h = _get_prop(target_obj, "Height")
                    if h:
                        indicator_height = int(h)

    if indicator_height is None:
        print("  Warning: could not determine scrollbar indicator height "
              "- skipping scroll struct generation.")
        return {}

    bar_travel = bar_parent_height - indicator_height

    # Bar base offset: current Top of the proxy positioning BarContent inside BarParent
    # (this is the pos=0 baseline as currently set up in ISO-Designer).
    bar_base_offset = None
    bp_children = bar_parent_obj.find("Objects")
    if bp_children is not None:
        for child_ref in bp_children.findall("Object"):
            proxy_obj = by_id.get(child_ref.get("JVS-ID"))
            if proxy_obj is None:
                continue
            target_obj = _resolve_proxy_target(proxy_obj, by_id)
            if target_obj is not None and target_obj.get("JVS-ID") == str(bar_content_id):
                top_val = _get_prop(proxy_obj, "Top")
                if top_val:
                    bar_base_offset = int(top_val)
                break

    if bar_base_offset is None:
        print("  Warning: could not determine scrollbar content base offset "
              "- skipping scroll struct generation.")
        return {}

    content_name = list_contents[0]
    suffix = "_Scrolling_Content"
    key_name = content_name[:-len(suffix)] if content_name.endswith(suffix) else content_name

    # Button IDs: traced via list_parent_id's hosting mask -> its associated SoftKeyMask
    # -> that SoftKeyMask's own child objects (ObjectPointers) -> the real Key object
    # each one resolves to, matched to the 6 roles by the ObjectPointer's name. The
    # ObjectPointer IDs themselves are kept too (control_pointers) - not used yet, but
    # needed later to redirect/hide a softkey's icon when the scroll position is at a
    # limit. The direct-position InputNumber field has no analogous discoverable link
    # (nothing in the pool currently marks a field as "the goto input") - stays
    # None/ID_NULL until such a field exists and gets a naming convention.
    button_roles, button_pointer_roles, button_warnings = _find_scroll_button_controls(
        jop_dir, root, by_id, list_parent_id)
    for w in button_warnings:
        print(f"  Warning: {w}")

    return {
        key_name: {
            "list_parent_id":  list_parent_id,
            "list_content_id": list_content_id,
            "row_height":      row_height,
            "bar_parent_id":    bar_parent_id,
            "bar_content_id":   bar_content_id,
            "bar_base_offset":  bar_base_offset,
            "bar_travel":       bar_travel,
            "pos_max":          pos_max,
            "step":             step,
            "controls":         button_roles,
            "control_pointers": button_pointer_roles,
        }
    }


SCROLL_NAME_SUFFIX = "_Scroll"


SCROLL_ID_NULL = 65535  # isobus::UT::Q::const::IDs::ID_NULL, spelled out since .gcf
                        # InitialValue expressions aren't resolved against other packages


def writeScrollGCFfile(data, filepaths):
    """Write a <name>_Scroll.gcf with ScrollFull_S constants for each detected scroll list.

    stGeometry is derived from the .jop (list/scrollbar container geometry). stControls'
    6 button IDs are traced via the list's hosting mask -> its SoftKeyMask -> that mask's
    child objects, matched to a role by name (see _find_scroll_button_controls); any role
    that couldn't be matched falls back to ID_NULL (readScrollJOP already printed a
    warning for those). u16GotoInputId has no discoverable link in the pool yet and is
    always ID_NULL until such a field exists with a naming convention.
    """
    newfilepath = safe_output_path(filepaths[1], filepaths[2] + '_Scroll.gcf')
    gcf_name    = filepaths[2] + '_Scroll'
    package     = filepaths[3]
    struct_type = "isobus::utils::scroll::ScrollFull_S"

    root = ET.Element("GlobalConstants", Name=gcf_name, Comment="Scroll list configuration constants (geometry + controls)")

    compiler_info = ET.SubElement(root, "CompilerInfo")
    compiler_info.set("packageName", package)

    global_constants = ET.SubElement(root, "GlobalConstants")

    for name, info in sorted(data.items()):
        geometry = (
            f"(u16ListParentId := {info['list_parent_id']}, "
            f"u16ListContentId := {info['list_content_id']}, "
            f"i32RowHeight := {info['row_height']}, "
            f"u16BarParentId := {info['bar_parent_id']}, "
            f"u16BarContentId := {info['bar_content_id']}, "
            f"i32BarBaseOffset := {info['bar_base_offset']}, "
            f"i32BarTravel := {info['bar_travel']}, "
            f"i32PosMax := {info['pos_max']}, "
            f"i32Step := {info['step']})"
        )

        controls_info = info.get("controls") or {}
        def _ctl(field):
            v = controls_info.get(field)
            return v if v is not None else SCROLL_ID_NULL
        pointers_info = info.get("control_pointers") or {}
        def _ptr(field):
            v = pointers_info.get(field)
            return v if v is not None else SCROLL_ID_NULL
        controls = (
            f"(u16BtnTopId := {_ctl('u16BtnTopId')}, "
            f"u16BtnPageUpId := {_ctl('u16BtnPageUpId')}, "
            f"u16BtnUpId := {_ctl('u16BtnUpId')}, "
            f"u16BtnDownId := {_ctl('u16BtnDownId')}, "
            f"u16BtnPageDownId := {_ctl('u16BtnPageDownId')}, "
            f"u16BtnBottomId := {_ctl('u16BtnBottomId')}, "
            f"u16GotoInputId := {SCROLL_ID_NULL}, "
            f"u16BtnPageUpPtrId := {_ptr('u16BtnPageUpId')}, "
            f"u16BtnUpPtrId := {_ptr('u16BtnUpId')}, "
            f"u16BtnDownPtrId := {_ptr('u16BtnDownId')}, "
            f"u16BtnPageDownPtrId := {_ptr('u16BtnPageDownId')})"
        )
        initial_value = f"(stGeometry := {geometry}, stControls := {controls})"

        ET.SubElement(
            global_constants,
            "VarDeclaration",
            Name=name + SCROLL_NAME_SUFFIX,
            Type=struct_type,
            InitialValue=initial_value,
        )
        print(f"  Note: {name}{SCROLL_NAME_SUFFIX}.stControls.u16GotoInputId left as "
              f"ID_NULL - no direct-position input field exists in the pool yet.")

    xml_str = ET.tostring(root, encoding='utf-8').decode()
    xml_str = minidom.parseString(xml_str).toprettyxml(indent="\t")
    xml_str = xml_str[:19] + ' ' + 'encoding="UTF-8"' + xml_str[20:]

    with open(newfilepath, "w") as file:
        file.write(xml_str)

    print(f"Written: {newfilepath}")


POSITIONMARKER_NAME_SUFFIXES = ("_Sollwertmarker",)  # tuple: room to add more suffixes later

POSITIONMARKER_NAME_SUFFIX = "_PositionMarker"


def _bbox_width(obj):
    """Return an object's bounding-box width in pixels: prefer an explicit Width
    property (CRectangle, CGroup, ...); fall back to parsing a CPolygon's Points
    property (which has no Width of its own) as max(x) - min(x)."""
    width = _get_prop(obj, "Width")
    if width is not None:
        return int(width)
    points = _get_prop(obj, "Points")
    if points is None:
        return None
    coords = re.findall(r'\(([-\d]+),([-\d]+)\)', points)
    if not coords:
        return None
    xs = [int(x) for x, _y in coords]
    return max(xs) - min(xs)


def readPositionMarkerJOP(jop_filepath):
    """Parse a .jop file and extract position-marker geometry into PositionMarker_S data.

    Detects each marker by a container (CGroup) ObjectName ending in one of
    POSITIONMARKER_NAME_SUFFIXES (e.g. "_Sollwertmarker"). Unlike Scroll, any number
    of markers per pool is supported - each is processed independently, since there is
    no cross-suffix pairing ambiguity here (a marker needs only one container name plus
    its already-nested child reference).

    r32MinPos is always 0.0 (a marker can't travel left of the container's own left
    edge). r32MaxPos is derived from ContainerWidth - ChildBoundingBoxWidth. r32Center
    is read from the child's own CProxy "Left" property - the pos=0 baseline as
    currently set up in ISO-Designer, exactly like readScrollJOP derives bar_base_offset
    from the scrollbar proxy's "Top" rather than assuming a formula.

    Returns a dict keyed by the container's ObjectName with its suffix stripped:
        { "Container": {"child_id": 16000, "parent_id": 3000, "min_pos": 0.0,
                         "max_pos": 84.0, "center": 42.0, "y_position": 0}, ... }
    """
    tree = ET.parse(jop_filepath)
    root = tree.getroot()
    objects_container = root.find("Objects")
    if objects_container is None:
        return {}

    by_name = {}
    by_id = {}
    for obj in objects_container.findall("Object"):
        jvs_id = obj.get("JVS-ID")
        if jvs_id:
            by_id[jvs_id] = obj
        name = obj.get("ObjectName")
        if name:
            by_name[name] = obj

    result = {}
    for name, container_obj in by_name.items():
        suffix = next((s for s in POSITIONMARKER_NAME_SUFFIXES if name.endswith(s)), None)
        if suffix is None:
            continue
        key_name = name[:-len(suffix)]

        width_str = _get_prop(container_obj, "Width")
        if width_str is None:
            print(f"  Warning: '{name}' has no Width property - skipping position marker generation.")
            continue
        container_width = int(width_str)

        child_refs = container_obj.find("Objects")
        child_ref = child_refs.find("Object") if child_refs is not None else None
        if child_ref is None:
            print(f"  Warning: '{name}' has no child object - skipping position marker generation.")
            continue
        proxy_obj = by_id.get(child_ref.get("JVS-ID"))
        if proxy_obj is None:
            print(f"  Warning: '{name}' child reference not found - skipping position marker generation.")
            continue

        if proxy_obj.get("Class") == "CProxy":
            target_obj = _resolve_proxy_target(proxy_obj, by_id)
            proxy_left = _get_prop(proxy_obj, "Left")
        else:
            target_obj = proxy_obj
            proxy_left = _get_prop(proxy_obj, "Left")

        if target_obj is None:
            print(f"  Warning: '{name}' proxy target not found - skipping position marker generation.")
            continue

        child_width = _bbox_width(target_obj)
        if child_width is None:
            print(f"  Warning: '{name}' child object has neither Points nor Width - skipping position marker generation.")
            continue
        if proxy_left is None:
            print(f"  Warning: '{name}' child reference has no Left property - skipping position marker generation.")
            continue

        result[key_name] = {
            "child_id":   int(target_obj.get("JVS-ID")),
            "parent_id":  int(container_obj.get("JVS-ID")),
            "min_pos":    0.0,
            "max_pos":    float(container_width - child_width),
            "center":     float(proxy_left),
            "y_position": 0,
        }

    return result


def writePositionMarkerGCFfile(data, filepaths):
    """Write a <name>_PositionMarker.gcf with PositionMarker_S constants for each detected marker."""
    newfilepath = safe_output_path(filepaths[1], filepaths[2] + '_PositionMarker.gcf')
    gcf_name    = filepaths[2] + '_PositionMarker'
    package     = filepaths[3]
    struct_type = "isobus::utils::childposition::PositionMarker_S"

    root = ET.Element("GlobalConstants", Name=gcf_name, Comment="Position marker constants (child/parent object IDs, travel bounds, center offset)")
    compiler_info = ET.SubElement(root, "CompilerInfo")
    compiler_info.set("packageName", package)
    global_constants = ET.SubElement(root, "GlobalConstants")

    for name, info in sorted(data.items()):
        initial_value = (
            f"(u16ChildId := {info['child_id']}, "
            f"u16ParentId := {info['parent_id']}, "
            f"r32MinPos := {_format_real(info['min_pos'])}, "
            f"r32MaxPos := {_format_real(info['max_pos'])}, "
            f"r32Center := {_format_real(info['center'])}, "
            f"s16YPosition := {info['y_position']})"
        )
        ET.SubElement(
            global_constants,
            "VarDeclaration",
            Name=name + POSITIONMARKER_NAME_SUFFIX,
            Type=struct_type,
            InitialValue=initial_value,
        )

    xml_str = ET.tostring(root, encoding='utf-8').decode()
    xml_str = minidom.parseString(xml_str).toprettyxml(indent="\t")
    xml_str = xml_str[:19] + ' ' + 'encoding="UTF-8"' + xml_str[20:]

    with open(newfilepath, "w") as file:
        file.write(xml_str)

    print(f"Written: {newfilepath}")


if __name__ == "__main__":

    # Gets filepaths and saves it in a variable
    filepaths = getPaths()

    os.makedirs(filepaths[1], exist_ok=True)

    # Prints filepaths
    printPaths(filepaths)
    file_data, rename_map = readIOPH(filepaths)
    writeGCFfile(file_data, filepaths)

    # If a .jop file was provided, update ObjectNames and generate the Numeric struct GCF
    if filepaths[4]:
        checkPath(filepaths[4])
        update_jop_objectnames(filepaths[4], rename_map)
        numeric_data = readJOP(filepaths[4])
        writeNumericGCFfile(numeric_data, filepaths)

        scroll_data = readScrollJOP(filepaths[4])
        if scroll_data:
            writeScrollGCFfile(scroll_data, filepaths)

        position_marker_data = readPositionMarkerJOP(filepaths[4])
        if position_marker_data:
            writePositionMarkerGCFfile(position_marker_data, filepaths)


__author__ = "Lorenz Bauer / Franz Höpfinger"
__version__ = "0.3"
__description__ = "Converts .iop.h to .gcf; optionally converts .jop to NumericObjectPool_S .gcf; strips _<ID> suffix from unique object names"
