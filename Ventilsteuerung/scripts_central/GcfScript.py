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
    parser.add_argument(
        "--variables-only", dest="variables_only", action="store_true", default=False,
        help="For InputNumber/OutputNumber widgets that have a bound CNumberVariable, "
             "emit ONLY the NumberVariable-named _N constant, not the widget-named one. "
             "Franz's rule: 'wenn eine InputNumber eine NumberVariable hat, MUSS die "
             "NumberVariable fuer alle Operationen verwendet werden.' Makes an accidental "
             "reference to the widget's own _N constant a compile-time 'does not exist' "
             "error in 4diac instead of a silently-wrong-object bug (see Krauternter "
             "Outputs_STG1.SUB stObjVentiloeffnungManuell incident, fixed in commit 365fb1a)."
    )
    args = parser.parse_args()

    # Create the absolute paths using os.path.join
    new_path = os.path.join(os.path.dirname(script_path), args.new_folder)
    old_path = os.path.join(os.path.dirname(script_path), args.old_file)
    jop_path = os.path.join(os.path.dirname(script_path), args.jop_file) if args.jop_file else None

    filepaths = [old_path, new_path, args.new_file, args.package, jop_path, args.variables_only]
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
    """Join folder/filename for writing, rejecting any filename that isn't a plain, single
    path component, then double-check the joined result still resolves inside folder.

    filename is built from CLI-supplied arguments (--newfile plus a fixed suffix); this guards
    against it accidentally (or via a malformed CLI invocation) containing "..", a path
    separator, or an absolute path component that would otherwise let a write escape the
    intended --newfolder directory.
    """
    if not filename or filename in (os.curdir, os.pardir):
        raise ValueError(f"Invalid output filename: {filename!r}")
    if os.path.basename(filename) != filename:
        raise ValueError(f"Output filename must not contain path separators: {filename!r}")

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

def readJOP(jop_filepath, variables_only=False):
    """Parse a JetViewSoft .jop XML file and extract InputNumber and OutputNumber objects.

    Returns a dict keyed by ObjectName:
        { "InputNumber_I1": {"id": 9000, "scale": 1.0, "offset": 0, "decimals": 0}, ... }

    If variables_only is True: for a widget that has a bound CNumberVariable, do NOT
    emit an entry under the widget's own name at all - only the NumberVariable-named
    alias. This enforces Franz's rule ("wenn eine InputNumber eine NumberVariable hat,
    MUSS die NumberVariable fuer alle Operationen verwendet werden") at compile time:
    a .SUB file that still references the widget's own _N constant gets a 4diac
    "does not exist" import error instead of silently writing to the wrong object
    (see Krauternter Outputs_STG1.SUB stObjVentiloeffnungManuell incident, commit
    365fb1a - InputNumber_..._N pointed at the widget's own JVS-ID instead of the
    bound NumberVariable's JVS-ID, both existed so nothing caught it at compile time).
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

        # Find a bound NumberVariable child, if any (a widget binds at most one -
        # if the pool somehow references several, the first one found wins, same
        # as before this refactor).
        bound_var_id = None
        objs_elem = obj.find("Objects")
        if objs_elem is not None:
            for child_obj in objs_elem.findall("Object"):
                child_id = child_obj.get("JVS-ID")
                if child_id and child_id in var_names:
                    bound_var_id = child_id
                    break

        # Emit the widget's own constant unless variables_only is requested AND
        # this widget has a bound NumberVariable (Franz's rule: a widget with a
        # bound variable must be addressed through the variable, never through
        # the widget itself - see readJOP docstring for the incident this fixes).
        if bound_var_id is None or not variables_only:
            result[name] = info

        # Alias logic: if this object references a NumberVariable, create an alias.
        # This allows writing to the variable name directly in the application.
        if bound_var_id is not None:
            alias_name = var_names[bound_var_id]
            # Protect primary object names from being overwritten by aliases.
            if alias_name in primary_names:
                print(f"  Skip alias '{alias_name}': conflicts with primary object name")
            elif scale == 0.0:
                # Guard against physically meaningless zero scales.
                pass
            else:
                # The alias uses the ID of the NumberVariable itself.
                alias_id = int(bound_var_id)
                if alias_name not in result:
                    result[alias_name] = create_numeric_info(alias_id, scale, offset, decimals)
                else:
                    current = result[alias_name]
                    if (current["scale"], current["offset"], current["decimals"]) != (scale, offset, decimals):
                        print(
                            f"  WARNUNG: '{alias_name}' wird von mehreren Widgets mit "
                            f"unterschiedlicher Skalierung gebunden - bisher "
                            f"scale={current['scale']} offset={current['offset']} "
                            f"decimals={current['decimals']}, jetzt von '{name}' "
                            f"scale={scale} offset={offset} decimals={decimals}. Alle "
                            f"Widgets, die dieselbe NumberVariable binden, muessen "
                            f"dieselbe Skalierung haben."
                        )
                    # Compare absolute values to correctly handle negative scales.
                    if abs(scale) < abs(current["scale"]):
                        print(f"  Update alias '{alias_name}': scale {current['scale']} -> {scale}")
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
    """Find the .jvi file in jop_dir (searched recursively, since ISO-Designer lets
    masks live in subfolders, e.g. Diagnosis/Ausgaenge/AusgaengeMask.jvi) whose
    <Components> places object_jvs_id directly.

    Returns (jvi_path, jvi_root) or (None, None) if not found in any .jvi under jop_dir.
    """
    for jvi_path in glob.glob(os.path.join(jop_dir, "**", "*.jvi"), recursive=True):
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


def _find_min_row_spacing(container_obj, by_id):
    """Recursively find the smallest UNIFORMLY repeating vertical Top-spacing anywhere
    in container_obj's subtree, resolving CProxy indirection at each level.

    Why recursive, not just container_obj's direct children: a ListContent's direct
    children may themselves be grouped composites (e.g. one "Container_Ausgaenge_STG1"
    per station, bundling a header + that station's individual channel rows) rather
    than the real atomic per-row containers - grouping rows under a shared header
    container must NOT change what counts as "one row" for scroll purposes (Franz,
    2026-09-22). The real atomic row is the smallest repeating spacing found anywhere
    in the subtree, wherever it actually sits in the nesting.

    Why "uniformly repeating", not just "any 2 siblings with a Top": a single row's own
    decorative content (background rectangle at Top=0, a label/value pair both at
    Top=2, an icon or button also near Top=2) produces small, IRREGULAR Top spacings
    (e.g. tops {0, 2, 18} -> deltas [2, 16], not equal to each other) that are not a
    "row" at all - confirmed real trap, Ausgang_STG1_Q01's own children spuriously gave
    a "row height" of 2px via a naive smallest-any-two-Tops search. A genuine row list
    instead has >=3 siblings spaced by one CONSTANT delta (every consecutive gap
    between sorted, deduplicated Tops is identical) - requiring >=3 (not 2) rules out a
    coincidental single small gap, and requiring every gap equal (not just the smallest
    two) rules out a level that mixes a few real rows with unrelated decoration.

    Returns the smallest positive spacing among all such uniform groups found anywhere
    in the subtree (i.e. the finest real row, even if an outer level also happens to be
    uniformly spaced - see the module's row-height detection call site), or None if no
    qualifying group was found anywhere.

    Two-row fallback: the >=3-siblings rule above would otherwise reject a perfectly
    valid list that only has two rows (no coincidental-decoration risk to guard against
    there - two IS the whole list, not a suspicious subset of it), regressing support
    that the previous single-level implementation had (confirmed review finding on the
    PR that introduced the >=3 rule). If the recursive uniform-group search above found
    nothing anywhere in the subtree, fall back to container_obj's own DIRECT children
    only (not recursively, so this doesn't reopen the original decoration-Top trap at
    every nested level): if exactly 2 distinct Tops are positioned there, use their
    difference.

    Height plausibility guard: the >=3-uniform rule alone doesn't rule out >=3
    decorative siblings that happen to be evenly spaced too (confirmed review finding,
    reproduced with a synthetic 3-label row at Top 2/8/14 - delta 6 - each Height 20:
    without this guard, the recursion keeps descending into every row's own subtree and
    would report row_height=6 instead of the real row spacing, since 6 < the genuine
    row spacing and "smallest wins"). A real row's own Height should not exceed the
    spacing to its neighbour (rows tile without overlapping); overlapping same-line
    decoration (a label next to a value, both roughly centered) routinely has a Height
    larger than its small Top offset from a sibling. So a uniform group is only
    accepted as a row-spacing candidate if none of its members' own Height (where
    known - not every object exposes one) exceeds the detected spacing. Deliberately
    NOT implemented as "stop recursing once a uniform group is found at this level"
    (the fix Krauternter/training1's own review bot suggested) - that reintroduces the
    original bug this function was written to fix: ListContent's own direct children
    (e.g. 5 per-station groups, itself a uniform >=3 group at spacing 546) would then
    win immediately and the walk would never reach the real 42px row underneath,
    verified by literally running that suggested change against the real pool.

    Cycle guard: a CProxy chain that loops back to one of its own ancestors (a
    malformed/hand-corrupted .jop, not something ISO-Designer itself is expected to
    produce, but this function processes external file data and should not trust it)
    would otherwise recurse forever and crash with RecursionError - confirmed by
    reproducing a 2-node synthetic cycle against this function before this guard
    existed. `active` tracks the JVS-IDs on the current DFS path (passed as a new
    frozenset per call, not mutated, so sibling branches don't see each other's
    ancestors); a node already on that path is skipped instead of revisited. This is
    deliberately NOT a global visited-set - the same real object legitimately gets
    reached via CProxy from multiple different parents in this pool (shared background
    rectangles/icons, see the iso-designer-jop skill), and each such reachable path
    must still be walked for its own Top/spacing context. Depth itself isn't separately
    bounded: VT pools are inherently shallow (mask -> container -> row -> widget, a
    handful of levels), so the only realistic unbounded-recursion risk is a cycle,
    which this guard removes."""
    best = None

    def visit(obj, active):
        nonlocal best
        obj_id = obj.get("JVS-ID")
        if obj_id is not None and obj_id in active:
            return
        active = active | {obj_id}
        objs_el = obj.find("Objects")
        if objs_el is None:
            return
        tops = []
        top_to_targets = {}
        child_targets = []
        for ref in objs_el.findall("Object"):
            proxy = by_id.get(ref.get("JVS-ID"))
            if proxy is None:
                continue
            top_val = _get_prop(proxy, "Top")
            target = _resolve_proxy_target(proxy, by_id)
            if target is None and proxy.get("Class") != "CProxy":
                # Not every direct child list uses CProxy indirection - fall back to
                # the reference itself if it's already a real object.
                target = proxy
            if top_val:
                try:
                    t = int(top_val)
                    tops.append(t)
                    if target is not None:
                        top_to_targets.setdefault(t, []).append(target)
                except ValueError:
                    pass  # non-numeric Top (e.g. unset/placeholder) - skip this row, don't fail the whole scan
            if target is not None:
                child_targets.append(target)

        tops = sorted(set(tops))
        if len(tops) >= 3:
            deltas = [b - a for a, b in zip(tops, tops[1:])]
            if len(set(deltas)) == 1 and deltas[0] > 0:
                spacing = deltas[0]
                plausible = True
                for t in tops:
                    for target in top_to_targets.get(t, []):
                        h = _get_prop(target, "Height")
                        if h:
                            try:
                                if int(h) > spacing:
                                    plausible = False
                            except ValueError:
                                pass  # non-numeric Height - can't check for overlap, so don't disqualify the spacing on it
                if plausible and (best is None or spacing < best):
                    best = spacing

        for target in child_targets:
            visit(target, active)

    visit(container_obj, frozenset())

    if best is None:
        top_level_tops = set()
        objs_el = container_obj.find("Objects")
        if objs_el is not None:
            for ref in objs_el.findall("Object"):
                proxy = by_id.get(ref.get("JVS-ID"))
                if proxy is None:
                    continue
                top_val = _get_prop(proxy, "Top")
                if top_val:
                    try:
                        top_level_tops.add(int(top_val))
                    except ValueError:
                        pass  # non-numeric Top - skip this row in the 2-row fallback too
        if len(top_level_tops) == 2:
            lowest_two = sorted(top_level_tops)
            spacing = lowest_two[1] - lowest_two[0]
            if spacing > 0:
                best = spacing

    return best


def _pair_scroll_lists_by_prefix(by_name):
    """Group *_Scrolling_Parent/_Scrolling_Content/_Scrollbar_Parent/_Scrollbar_Content
    ObjectNames by their common prefix (the part before the suffix).

    Multiple scroll lists per pool are supported as long as each list's four container
    names share one consistent prefix (e.g. "Ausgaenge_Scrolling_Parent",
    "Ausgaenge_Scrolling_Content", ... all prefixed "Ausgaenge") - true for pools built
    fresh by a generator script. A pool with historically inconsistent naming (e.g. the
    original Workspace_Scroll pool's "Containerr_Scrolling_Parent" typo vs.
    "Container_Scrolling_Content") would fail to pair here and is skipped with a warning -
    rename in ISO-Designer to a consistent prefix if that happens.

    Returns {prefix: {"list_parent": name, "list_content": name, "bar_parent": name,
                       "bar_content": name}}, only for prefixes where all four are present.
    """
    suffixes = {
        "list_parent":  "_Scrolling_Parent",
        "list_content": "_Scrolling_Content",
        "bar_parent":   "_Scrollbar_Parent",
        "bar_content":  "_Scrollbar_Content",
    }
    by_prefix = {}
    for name in by_name:
        for role, suffix in suffixes.items():
            if name.endswith(suffix):
                prefix = name[:-len(suffix)]
                by_prefix.setdefault(prefix, {})[role] = name

    complete = {p: roles for p, roles in by_prefix.items() if len(roles) == 4}
    incomplete = {p: roles for p, roles in by_prefix.items() if len(roles) != 4}
    for prefix, roles in incomplete.items():
        missing = [role for role in suffixes if role not in roles]
        print(f"  Warning: scroll list prefix '{prefix}' is missing {missing} - "
              "skipped (needs all four *_Scrolling_Parent/_Scrolling_Content/"
              "_Scrollbar_Parent/_Scrollbar_Content names with this exact prefix).")
    return complete


def _read_one_scroll_list(jop_dir, root, by_id, by_name, roles):
    """Extract ScrollObjectPool_S-shaped geometry + button-role data for one scroll list.

    `roles` is one entry from _pair_scroll_lists_by_prefix()'s return value. Returns the
    info dict (see readScrollJOP docstring) or None if geometry couldn't be determined
    (a warning is printed for the specific reason).
    """
    list_parent_obj  = by_name[roles["list_parent"]]
    list_content_obj = by_name[roles["list_content"]]
    bar_parent_obj    = by_name[roles["bar_parent"]]
    bar_content_obj   = by_name[roles["bar_content"]]

    list_parent_id  = int(list_parent_obj.get("JVS-ID"))
    list_content_id = int(list_content_obj.get("JVS-ID"))
    bar_parent_id    = int(bar_parent_obj.get("JVS-ID"))
    bar_content_id   = int(bar_content_obj.get("JVS-ID"))

    list_parent_height  = int(_get_prop(list_parent_obj, "Height") or 0)
    list_content_height = int(_get_prop(list_content_obj, "Height") or 0)
    bar_parent_height    = int(_get_prop(bar_parent_obj, "Height") or 0)

    # Row height = vertical spacing between the smallest repeating group of siblings
    # found ANYWHERE in ListContent's subtree (see _find_min_row_spacing), NOT a row
    # container's own Height property - rows are typically drawn shorter than their
    # spacing to leave a visible gap between them. Recursive, not just ListContent's
    # direct children: ListContent's direct children may themselves be grouped
    # composites (e.g. one "Container_Ausgaenge_STG1" per station, bundling a header +
    # that station's individual channel rows like "Ausgang_STG1_Q01") rather than the
    # real atomic rows - that grouping must not change what counts as "one row" for
    # PAGE_UP/PAGE_DOWN's i32Step, otherwise a page-scroll degenerates to the same
    # single "whole group" step as a line-scroll (confirmed real case, Franz 2026-09-22:
    # Ausgaenge/Eingaenge_Scroll's direct ListContent children are per-station groups
    # spaced 546px apart, while the real per-channel row is 42px).
    row_height = _find_min_row_spacing(list_content_obj, by_id)

    if not row_height:
        print("  Warning: could not determine row height (need at least two row "
              "containers positioned somewhere inside the list content) - skipping "
              "scroll struct generation.")
        return None

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
        return None

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
        return None

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


def readScrollJOP(jop_filepath):
    """Parse a .jop file and extract scroll-list geometry into ScrollObjectPool_S data,
    for every scroll list found in the pool (see _pair_scroll_lists_by_prefix()).

    Detects each scroll list by four CGroup ObjectNames sharing one prefix and ending in
    "_Scrolling_Parent", "_Scrolling_Content", "_Scrollbar_Parent", "_Scrollbar_Content"
    (see SCROLL_KONZEPT.md in Workspace_Scroll). Multiple scroll lists per pool are
    supported as long as each one's four names share a consistent prefix.

    Returns a dict keyed by each list's prefix:
        { "Ausgaenge": {"list_parent_id": 3006, "list_content_id": 3031, "row_height": 42,
                         "bar_parent_id": 3000, "bar_content_id": 3010, "bar_base_offset": -252,
                         "bar_travel": 252, "pos_max": 13, "step": 6, ...}, ... }
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

    lists_by_prefix = _pair_scroll_lists_by_prefix(by_name)
    if not lists_by_prefix:
        return {}

    result = {}
    for prefix, roles in sorted(lists_by_prefix.items()):
        info = _read_one_scroll_list(jop_dir, root, by_id, by_name, roles)
        if info is not None:
            result[prefix] = info
    return result


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


BARGRAPHSPLIT_NAME_SUFFIXES = ("_links", "_rechts")  # exactly 2, unlike Scroll's 4

BARGRAPHSPLIT_NAME_SUFFIX = "_BargraphSplit"


def _is_bargraph_rectangle(obj):
    """A CRectangle configured as an ISO 11783-6 Annex B.11.3 Output Linear Bar Graph
    carries its own nested PropertySheet Name="Bargraph" - this excludes any other
    CRectangle that merely happens to end in a matched suffix."""
    if obj.get("Class") != "CRectangle":
        return False
    return any(sheet.get("Name") == "Bargraph" for sheet in obj.findall("PropertySheet"))


def readBargraphSplitJOP(jop_filepath):
    """Parse a .jop file and extract split-bargraph pairs into BargraphSplit_S data.

    Detects each pair by two Bargraph CRectangle ObjectNames sharing a common prefix and
    ending in "_links"/"_rechts" (BARGRAPHSPLIT_NAME_SUFFIXES). Unlike Scroll's single-
    pair-per-pool limit, every distinct prefix is processed independently (like
    readPositionMarkerJOP) - multiple split-bargraph pairs per pool are supported. A
    prefix missing one side, or with more than one match for a side, is skipped with a
    warning; other pairs still succeed. A pair whose two sides disagree on Min/Max is
    also skipped with a warning, since a split bargraph is by construction one signed
    range mirrored around a shared zero.

    Returns a dict keyed by the shared prefix:
        { "Bargraph_Split": {"left_id": 18001, "right_id": 18002, "min": 0.0, "max": 42.0}, ... }
    """
    tree = ET.parse(jop_filepath)
    root = tree.getroot()
    objects_container = root.find("Objects")
    if objects_container is None:
        return {}

    by_suffix = {suffix: {} for suffix in BARGRAPHSPLIT_NAME_SUFFIXES}
    for obj in objects_container.findall("Object"):
        name = obj.get("ObjectName")
        if not name or not _is_bargraph_rectangle(obj):
            continue
        for suffix in BARGRAPHSPLIT_NAME_SUFFIXES:
            if name.endswith(suffix):
                prefix = name[:-len(suffix)]
                by_suffix[suffix].setdefault(prefix, []).append(obj)
                break

    prefixes = set()
    for suffix_map in by_suffix.values():
        prefixes.update(suffix_map.keys())

    result = {}
    for prefix in sorted(prefixes):
        left_suffix, right_suffix = BARGRAPHSPLIT_NAME_SUFFIXES
        left_matches = by_suffix[left_suffix].get(prefix, [])
        right_matches = by_suffix[right_suffix].get(prefix, [])

        if len(left_matches) != 1 or len(right_matches) != 1:
            print(f"  Warning: '{prefix}' has {len(left_matches)} '{left_suffix}' and "
                  f"{len(right_matches)} '{right_suffix}' Bargraph object(s) - need exactly "
                  "one of each, skipping split-bargraph generation for this prefix.")
            continue

        left_obj, right_obj = left_matches[0], right_matches[0]
        left_min, left_max = _get_prop(left_obj, "Min"), _get_prop(left_obj, "Max")
        right_min, right_max = _get_prop(right_obj, "Min"), _get_prop(right_obj, "Max")
        if left_min is None or left_max is None or right_min is None or right_max is None:
            print(f"  Warning: '{prefix}' Bargraph object(s) missing Min/Max - skipping "
                  "split-bargraph generation for this prefix.")
            continue
        if float(left_min) != float(right_min) or float(left_max) != float(right_max):
            print(f"  Warning: '{prefix}' left/right Bargraph Min/Max mismatch "
                  f"({left_suffix}: {left_min}..{left_max}, {right_suffix}: {right_min}..{right_max}) "
                  "- a split bargraph must share one symmetric range, skipping.")
            continue

        result[prefix] = {
            "left_id":  int(left_obj.get("JVS-ID")),
            "right_id": int(right_obj.get("JVS-ID")),
            "min":      float(left_min),
            "max":      float(left_max),
        }

    return result


def writeBargraphSplitGCFfile(data, filepaths):
    """Write a <name>_BargraphSplit.gcf with BargraphSplit_S constants for each detected pair."""
    newfilepath = safe_output_path(filepaths[1], filepaths[2] + '_BargraphSplit.gcf')
    gcf_name    = filepaths[2] + '_BargraphSplit'
    package     = filepaths[3]
    struct_type = "isobus::utils::bargraph::BargraphSplit_S"

    root = ET.Element("GlobalConstants", Name=gcf_name, Comment="Split-bargraph constants (left/right object IDs, shared magnitude bounds)")
    compiler_info = ET.SubElement(root, "CompilerInfo")
    compiler_info.set("packageName", package)
    global_constants = ET.SubElement(root, "GlobalConstants")

    for name, info in sorted(data.items()):
        side_left = (
            f"(u16ObjId := {info['left_id']}, r32Scale := 1.0, i32Offset := 0, u8Decimals := 0)"
        )
        side_right = (
            f"(u16ObjId := {info['right_id']}, r32Scale := 1.0, i32Offset := 0, u8Decimals := 0)"
        )
        initial_value = (
            f"(stLeft := {side_left}, "
            f"stRight := {side_right}, "
            f"r32MinMagnitude := {_format_real(info['min'])}, "
            f"r32MaxMagnitude := {_format_real(info['max'])})"
        )
        ET.SubElement(
            global_constants,
            "VarDeclaration",
            Name=name + BARGRAPHSPLIT_NAME_SUFFIX,
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
        numeric_data = readJOP(filepaths[4], variables_only=filepaths[5])
        writeNumericGCFfile(numeric_data, filepaths)

        scroll_data = readScrollJOP(filepaths[4])
        if scroll_data:
            writeScrollGCFfile(scroll_data, filepaths)

        position_marker_data = readPositionMarkerJOP(filepaths[4])
        if position_marker_data:
            writePositionMarkerGCFfile(position_marker_data, filepaths)

        bargraph_split_data = readBargraphSplitJOP(filepaths[4])
        if bargraph_split_data:
            writeBargraphSplitGCFfile(bargraph_split_data, filepaths)


__author__ = "Lorenz Bauer / Franz Höpfinger"
__version__ = "0.3"
__description__ = "Converts .iop.h to .gcf; optionally converts .jop to NumericObjectPool_S .gcf; strips _<ID> suffix from unique object names"
