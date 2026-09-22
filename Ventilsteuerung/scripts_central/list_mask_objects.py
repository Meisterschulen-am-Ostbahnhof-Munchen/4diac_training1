"""Read-only: for every ISO 11783-6 VT root/visibility-defining object actually
present in this pool - DataMask, AlarmMask (+ each one's paired SoftKeyMask),
WorkingSet, AuxFunction, and any SoftKeyMask NOT paired to a Data/AlarmMask -
recursively resolve every object reachable from that root down through CProxy
/ CGroup / CButton nesting to the leaves, and list them.

These root types are NOT all governed by the same visibility rule - see
BERICHT_2026-09-18_VT_SICHTBARKEITS_KONZEPT.md before wiring firmware logic
against --emit-visibility's output: DataMask/AlarmMask mask_id is an
ActiveMask comparison target, an unpaired SoftKeyMask's mask_id is an
active_softkey_mask comparison target, but WorkingSet and AuxFunction are NOT
ActiveMask-gated at all (WorkingSet's own descriptor is always potentially
visible; AuxFunction is assigned via a VT-independent AUX-assignment list).
CWindowMask/CKeyGroup exist in the norm but have 0 instances in this pool
(verified against DefaultPool.jop) and are deliberately not handled below.

Why: don't conclude an object is "not placed on mask X" from a shallow grep of
that mask's .jvi alone - a value widget can be buried many CProxy hops deep
inside a composite CButton "tile" and never gets its own top-level .jvi entry.
This script does the full recursive walk instead (see
~/.claude/skills/iso-designer-jop/SKILL.md, "File roles" section, for the
underlying CProxy-indirection background).

Also intended for later reuse: once/if OPC-UA bus load needs throttling, this
gives - per mask - exactly which CNumberVariable/CStringVariable objects are
actually visible while that mask is active, so publish/subscribe traffic for
data objects belonging to a mask nobody is currently looking at can be
throttled or paused.

No path is hardcoded - the pool directory is always a required argument (see
--pool-dir below), matching GcfScript.py's convention in this same folder.
Project-specific invocation goes through a thin .bat/.sh wrapper (which
supplies the concrete relative path for that project) plus an IDE .launch
entry, not by editing this file - see
Ventilsteuerung/4diacIDE-workspace/test/scripts/RunSkript_ListMaskObjects.bat
and .sh, and the matching entry under .../test/Launches/, in this repo.

Usage (arguments after -- pass-through, as the .bat/.sh wrappers do):
    python list_mask_objects.py --pool-dir <path/to/DefaultPool>
    python list_mask_objects.py --pool-dir <path> --jop DefaultPool.jop
    python list_mask_objects.py --pool-dir <path> DataMask_Ernte   # only
        # masks whose ObjectName or JVS-ID contains this
    python list_mask_objects.py --pool-dir <path> --data-only       # only
        # CNumberVariable/CStringVariable leaves
    python list_mask_objects.py --pool-dir <path> --data-only Ernte # combine
    python list_mask_objects.py --pool-dir <path> --emit-visibility OUT.csv
        # write the object->mask/scroll visibility CSV instead of printing -
        # see BERICHT_2026-09-18_VT_SICHTBARKEITS_KONZEPT.md for the format
        # and the runtime algorithm it feeds.

Prints, per DataMask (paired with its SoftKeyMask): every reachable object as
"depth  Class  ObjectName  (JVS-ID)", plus a summary count by class (objects
reachable from both the DataMask and its paired SoftKeyMask are counted once,
not twice).
"""
import argparse
import os
import sys
from collections import defaultdict

# Prefer defusedxml (guards against XXE) when it's available, but don't hard-
# require it: this repo has no Python dependency management, so a `python` on
# PATH without it installed would otherwise break the tool outright. This
# tool only ever parses local .jop/.jvi pool files this same team authors via
# ISO-Designer - never externally supplied/untrusted XML - so falling back to
# the standard library is safe, just not defense-in-depth.
try:
    import defusedxml.ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    print(
        "Note: defusedxml not installed - using the standard library's "
        "xml.etree.ElementTree instead (safe here: this tool only parses "
        "locally-authored .jop/.jvi files, never untrusted input). For "
        "defense-in-depth, run: pip install defusedxml",
        file=sys.stderr,
    )

DATA_CLASSES = {"CNumberVariable", "CStringVariable"}


def parse_args():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-d", "--pool-dir", dest="pool_dir", required=True,
        help="ISO-Designer pool workspace folder (the one containing the "
             ".jop file), relative to this script's parent directory "
             "(i.e. relative to the project's Ventilsteuerung/ folder) - "
             "e.g. ISO-DesignerProjects/Workspace/DefaultPool",
    )
    parser.add_argument(
        "-j", "--jop", dest="jop_file", default="DefaultPool.jop",
        help="Pool file name inside --pool-dir (default: DefaultPool.jop)",
    )
    parser.add_argument(
        "--data-only", action="store_true",
        help="Only list CNumberVariable/CStringVariable leaves",
    )
    parser.add_argument(
        "--emit-visibility", dest="emit_visibility", default=None, metavar="OUT_CSV",
        help="Instead of printing, write the object-visibility CSV described in "
             "BERICHT_2026-09-18_VT_SICHTBARKEITS_KONZEPT.md to OUT_CSV - one row "
             "per (object_id, mask_id) reachability pair, plus scroll-container "
             "geometry (scroll_container_id, row_top_px, row_height_px) for "
             "objects nested in a '*_Scrolling_Content' container. Deploy this "
             "file alongside the matching DefaultPool.iop/.iop.h build.",
    )
    parser.add_argument(
        "--emit-visibility-json", dest="emit_visibility_json", default=None, metavar="OUT_JSON",
        help="Same data as --emit-visibility, written as JSON instead of CSV - "
             "generate whichever (or both) the consuming firmware/tooling prefers. "
             "On the ESP32 cJSON is a standard ESP-IDF component (no extra "
             "dependency either way); CSV's only remaining advantage is file size "
             "(~2.2x smaller for this purely numeric table).",
    )
    parser.add_argument(
        "name", nargs="?", default=None,
        help="Only masks whose ObjectName or JVS-ID contains this (case-insensitive)",
    )
    args = parser.parse_args()

    pool_dir = os.path.join(os.path.dirname(script_dir), args.pool_dir)
    jop_path = os.path.join(pool_dir, args.jop_file)
    return (pool_dir, jop_path, args.data_only, (args.name.lower() if args.name else None),
            args.emit_visibility, args.emit_visibility_json)


def load_pool(jop_path):
    """Return (obj_class, obj_name, obj_children, obj_path, obj_top, obj_height)
    dicts keyed by JVS-ID (int).

    obj_top: for CProxy objects only - their own "Top" property (position in
    px relative to whatever parent's <Objects> list references them).
    obj_height: for real (non-CProxy) objects that carry a "Height" property
    directly on one of their own PropertySheets (CGroup row containers,
    COutputNumber/CInputNumber/CButton widgets, ...) - NOT recursive, so a
    child object's Height never leaks onto its parent by accident.
    """
    tree = ET.parse(jop_path)
    root = tree.getroot()

    obj_class = {}
    obj_name = {}
    obj_children = {}
    obj_path = {}
    obj_top = {}
    obj_height = {}
    for obj in root.iter("Object"):
        cls = obj.get("Class")
        jid_attr = obj.get("JVS-ID")
        if cls is None or jid_attr is None:
            continue
        jid = int(jid_attr)
        obj_class[jid] = cls
        obj_name[jid] = obj.get("ObjectName") or obj.get("Name") or ""
        kids = []
        objs_el = obj.find("Objects")
        if objs_el is not None:
            for child in objs_el.findall("Object"):
                cjid = child.get("JVS-ID")
                if cjid is not None:
                    kids.append(int(cjid))
        obj_children[jid] = kids

        if cls in ("CDataMask", "CAlarmMask", "CSoftKeyMask", "CWorkingSet"):
            # All four classes store their own .jvi reference at this same
            # PropertySheet/Property location (verified against a real
            # CAlarmMask and the real CWorkingSet in this pool, not assumed
            # by analogy to CDataMask) - CAlarmMask was previously missing
            # from this tuple, silently dropping every Alarm Mask's .jvi.
            path_val = obj.find("./PropertySheet[@Name='Model']/Property[@Name='Path']/Value")
            if path_val is not None and path_val.text:
                # The .jop stores this Path property with the separator of whatever OS the
                # ISO-Designer project was last saved on - Windows-authored projects (the
                # normal case here) write literal backslashes (e.g. ".\Hauptmenue\Foo.jvi").
                # os.path.join()/os.path.normpath() only translate "/" on POSIX, so a
                # backslash-separated string is treated as one literal filename there instead
                # of being descended into - every such root then fails to resolve its .jvi
                # and gets silently skipped. Normalizing to "/" here makes the path work
                # identically on Windows and POSIX (Windows accepts "/" natively too).
                obj_path[jid] = path_val.text.strip().replace("\\", "/")

        if cls == "CProxy":
            top_val = obj.find("./PropertySheet[@Name='Proxy']/Property[@Name='Top']/Value")
            if top_val is not None and top_val.text:
                try:
                    obj_top[jid] = int(float(top_val.text.strip()))
                except ValueError:
                    pass
        else:
            height_val = obj.find("./PropertySheet/Property[@Name='Height']/Value")
            if height_val is not None and height_val.text:
                try:
                    obj_height[jid] = int(float(height_val.text.strip()))
                except ValueError:
                    pass

    return obj_class, obj_name, obj_children, obj_path, obj_top, obj_height


# ISO 11783-6:2018 Annex B object types that carry a "Variable Reference"
# attribute: when bound (i.e. not left at 0xFFFF/NULL), the referenced
# Number/String Variable is the actual ChangeNumericValue wire target, not
# the widget itself - the widget's own ObjectID only becomes the row when it
# has NO bound variable (Franz: "wenn eine Output Number oder Input Number
# KEINE Variable hat geht die Input oder Output Nummer, wenn sie eine
# Variable hat dann wird die Variable genommen" - confirmed by the norm to
# generalize to all object types below, not just Output/InputNumber).
#
# Verified against this project's real pool: CInputNumber (35 instances) and
# COutputNumber (252 instances) - both bind CNumberVariable exclusively here.
# The other 8 norm-listed types have ZERO instances in the current pool, so
# their ISO-Designer Class strings below are UNVERIFIED best guesses,
# following this project's own naming convention - do not trust them without
# checking a real instance first. A wrong guess is a safe no-op: the
# consolidation simply won't trigger for that type (one harmless extra row),
# it can never produce a wrong or missing row for anything that actually
# exists in the pool. Known naming trap: ISO "Output String" turned out to be
# ISO-Designer class "COutputText" (not "COutputString") in this project -
# the same kind of mismatch could easily apply to "Output List" or either
# Bargraph type below; both plausible spellings are listed for the latter.
VR_CAPABLE_CLASSES = {
    "CInputBoolean": {"CNumberVariable"},    # ISO "Input Boolean" - unverified, 0 instances
    "CInputString": {"CStringVariable"},     # ISO "Input String" - unverified, 0 instances
    "CInputNumber": {"CNumberVariable"},     # ISO "Input Number" - verified, 35 instances
    "CInputList": {"CNumberVariable"},       # ISO "Input List" (index variable) - unverified, 0 instances
    "COutputText": {"CStringVariable"},      # ISO "Output String" - unverified as VR-capable; 0 instances bind a variable here (COutputText is this project's confirmed real class for "Output String")
    "COutputNumber": {"CNumberVariable"},    # ISO "Output Number" - verified, 252 instances
    "COutputList": {"CNumberVariable"},      # ISO "Output List" (index variable) - unverified, 0 instances, real class name unconfirmed
    "CMeter": {"CNumberVariable"},           # ISO "Output Meter" - unverified, 0 instances
    "CLinearBargraph": {"CNumberVariable"},  # ISO "Output Linear Bar Graph" - unverified, 0 instances, real class name unconfirmed
    "CLinearBarGraph": {"CNumberVariable"},  # alternate spelling, same reason
    "CArchedBargraph": {"CNumberVariable"},  # ISO "Output Arched Bar Graph" - unverified, 0 instances, real class name unconfirmed
    "CArchedBarGraph": {"CNumberVariable"},  # alternate spelling, same reason
    # Both Bargraph types can carry TWO independent Variable References (main
    # value + target-value marker) per the norm - no special-casing needed
    # for that here: if two variables are bound, both simply get their own
    # rows via the normal child recursion below: the "has_variable_child"
    # check only decides whether the WIDGET's own row is skipped (yes, as
    # soon as at least one variable is bound), never how many variable rows
    # result.
}


# ISO 11783-6:2018 VT root/visibility-defining object types, and what each
# one's mask_id in the emitted rows actually means - verified against the
# real DefaultPool.jop, not assumed from the norm text alone (grep confirmed
# 0 CWindowMask/CKeyGroup instances; see module docstring). Full writeup:
# BERICHT_2026-09-18_VT_SICHTBARKEITS_KONZEPT.md.
#
# - CDataMask / CAlarmMask: classic "ActiveMask" semantics (norm 4.6.8 /
#   4.6.14) - exactly one is the Working Set's ActiveMask at a time. mask_id
#   is directly comparable against the VT status message's ActiveMask field.
# - CSoftKeyMask: normally paired 1:1 with a CDataMask/CAlarmMask via that
#   mask's own .jvi "SoftKeyMask" property (jvi_softkeymask_id() below) - its
#   objects get mask_id = the PAIRED mask's own JVS-ID (the two activate
#   together). A SoftKeyMask NOT referenced by any Data/AlarmMask (0 in the
#   current pool - all 17 are paired - but ISO-Designer permits it) is
#   instead its own root below, mask_id = its own JVS-ID, matching the
#   report's separate active_softkey_mask comparison target.
# - CWorkingSet: NOT ActiveMask-gated. Its own .jvi holds the Working Set
#   descriptor content (norm 4.6.8: "can be used by the VT any time the
#   Working Set needs to be represented to the operator") - potentially
#   visible whenever the Working Set itself is active/displayed, independent
#   of the current Data/Alarm Mask. mask_id = the WorkingSet's own JVS-ID (0
#   in this pool, by the ObjectID block convention in
#   ~/.claude/skills/iso-designer-jop/SKILL.md). The ECU must NOT compare
#   this against ActiveMask.
# - CAuxFunction (ISO "Auxiliary Function", Type 2 in this project): not
#   reachable through any mask hierarchy at all - assigned to a physical
#   input device through a separate, VT-independent AUX-assignment list.
#   mask_id = the CAuxFunction's own JVS-ID, and that same JVS-ID is also
#   the AuxFunction's own leaf row (e.g. its BackColor is what a
#   ChangeBackgroundColour command actually targets - confirmed real case:
#   AuxFunction2_Lenkdeichsel_Links/Rechts, 31000/31001). NOT an
#   ActiveMask/active_softkey_mask comparison target either.


def _resolve_own_jvi_geometry(root_jid, obj_path, pool_dir, obj_children, obj_class,
                               obj_top, obj_height, scroll_root_ids):
    """Resolve a single root object's OWN .jvi Components (no SoftKeyMask
    pairing) into a geometry dict, or {} if its .jvi Path can't be resolved.
    Shared by the orphan-CSoftKeyMask and CWorkingSet root handling in
    compute_visibility_rows() - both are single, unpaired roots with a normal
    'Path' .jvi exactly like CDataMask, just without CDataMask's extra
    SoftKeyMask-pairing step."""
    path_rel = obj_path.get(root_jid)
    if not path_rel:
        return {}
    jvi = os.path.normpath(os.path.join(pool_dir, path_rel))
    if not os.path.exists(jvi):
        return {}
    seen = set()
    roots = jvi_component_roots(jvi)
    return resolve_tree_with_geometry(
        roots, obj_children, obj_class, obj_top, obj_height, scroll_root_ids, seen)


def resolve_tree_with_geometry(root_ids, obj_children, obj_class, obj_top, obj_height,
                                scroll_root_ids, seen):
    """Like resolve_tree, but additionally tracks - while walking down - the
    accumulated CProxy Top offset since the nearest scroll-container ancestor,
    and the nearest real object's own Height above each leaf. Returns a dict
    {jid: (scroll_container_jid_or_None, row_top_px, row_height_px)} for
    EVERY real (non-CProxy) object reached from root_ids - not a curated
    subset of classes, so nothing the ECU might write to is silently missing
    (Franz: "schreib ALLE Objekte auf, sonst werden wir dumm") - except the
    VR_CAPABLE_CLASSES widget-vs-bound-variable consolidation above.

    scroll_root_ids: JVS-IDs of CGroup objects that are themselves a
    "*_Scrolling_Content" container - entering one of these (as opposed to
    just being nested somewhere below it) resets accumulated_top to 0 and
    starts tracking that container as the current scroll_container_jid for
    everything nested inside it.
    """
    geometry = {}

    def visit(jid, scroll_container, acc_top, nearest_height):
        if jid in seen:
            return
        seen.add(jid)

        if jid in scroll_root_ids:
            scroll_container = jid
            acc_top = 0

        cls = obj_class.get(jid, "?")
        if cls == "CProxy" and jid in obj_top:
            acc_top = acc_top + obj_top[jid]
        elif jid in obj_height:
            nearest_height = obj_height[jid]

        if cls != "CProxy":
            variable_classes = VR_CAPABLE_CLASSES.get(cls)
            has_variable_child = variable_classes is not None and any(
                obj_class.get(c) in variable_classes for c in obj_children.get(jid, []))
            if not has_variable_child:
                geometry[jid] = (scroll_container, acc_top if scroll_container is not None else 0,
                                  nearest_height if scroll_container is not None else 0)

        for child in obj_children.get(jid, []):
            visit(child, scroll_container, acc_top, nearest_height)

    for root in root_ids:
        visit(root, None, 0, 0)
    return geometry


def compute_scroll_viewports(obj_class, obj_children, obj_height, scroll_root_ids):
    """For each scroll container root (a '*_Scrolling_Content' CGroup), find the
    nearest real (non-CProxy) ancestor - by this pool's construction its
    '*_Scrolling_Parent' container, reached through exactly one CProxy hop
    (verified against Ausgaenge_Scrolling_Parent/_Content, JVS-ID 3067/3066) -
    and read that ancestor's own Height. The walk isn't hardcoded to one hop
    so it stays correct if a pool ever nests a scroll container one level
    deeper. Returns {scroll_container_jid: viewport_height_px}, only for
    containers whose real parent could be resolved and has a Height.
    See BERICHT_2026-09-20_SCROLL_VIEWPORT_AUFTRAG.md."""
    parent_of = {}
    for pid, kids in obj_children.items():
        for kid in kids:
            parent_of[kid] = pid

    viewports = {}
    for root_jid in scroll_root_ids:
        jid = parent_of.get(root_jid)
        while jid is not None and obj_class.get(jid) == "CProxy":
            jid = parent_of.get(jid)
        if jid is not None and jid in obj_height:
            viewports[root_jid] = obj_height[jid]
    return viewports


def jvi_component_roots(jvi_path):
    """Top-level Component target JVS-IDs placed directly on one mask's .jvi."""
    roots = []
    t = ET.parse(jvi_path)
    comps = t.getroot().find("Components")
    if comps is None:
        return roots
    for c in comps.findall("Component"):
        objs = c.find("Objects")
        if objs is None:
            continue
        for o in objs.findall("Object"):
            jid = o.get("JVS-ID")
            if jid is not None:
                roots.append(int(jid))
    return roots


def jvi_softkeymask_id(jvi_path):
    """The paired SoftKeyMask's ObjectID, from a DataMask .jvi's General sheet."""
    t = ET.parse(jvi_path)
    val = t.getroot().find("./PropertySheets/PropertySheet[@Name='General']/Property[@Name='SoftKeyMask']/Value")
    if val is not None and val.text and val.text.strip() not in ("", "-1"):
        return int(val.text.strip())
    return None


def resolve_tree(root_ids, obj_children, seen):
    """DFS from root_ids through obj_children; returns list of (depth, jid) in
    parent-immediately-followed-by-children order (so printed indentation
    reads as an actual tree). `seen` is shared across calls (e.g. across a
    DataMask's tree and its paired SoftKeyMask's tree) so an object reachable
    from both is only visited - and counted - once, under whichever root
    reaches it first."""
    order = []

    def visit(jid, depth):
        if jid in seen:
            return
        seen.add(jid)
        order.append((depth, jid))
        for child in obj_children.get(jid, []):
            visit(child, depth + 1)

    for root in root_ids:
        visit(root, 0)
    return order


def compute_visibility_rows(pool_dir, obj_class, obj_name, obj_children, obj_path,
                             obj_top, obj_height):
    """Shared computation for --emit-visibility / --emit-visibility-json: one row per
    (object_id, mask_id) reachability pair, sorted. scroll_container_id/row_top_px/
    row_height_px are 0 when the object sits directly on a static (non-scrolling)
    mask. Returns (rows, jop_hash, masks_with_jvi, scroll_viewports) - the last being
    {scroll_container_id: viewport_height_px}, see compute_scroll_viewports().

    Covers every ISO 11783-6 VT root/visibility-defining object type actually
    present in this pool - see the comment block above _resolve_own_jvi_geometry
    for what each root's mask_id means (NOT always an ActiveMask comparison -
    see BERICHT_2026-09-18_VT_SICHTBARKEITS_KONZEPT.md). masks_with_jvi only
    counts the classic CDataMask/CAlarmMask bucket (kept for the existing
    --emit-visibility console summary line / regression baseline), not the
    WorkingSet/AuxFunction/orphan-SoftKeyMask additions below.
    """
    activemask_roots = sorted(
        jid for jid, cls in obj_class.items() if cls in ("CDataMask", "CAlarmMask"))
    # Excludes CProxy: the CProxy wrapping a "*_Scrolling_Content" CGroup carries the
    # same string in its own Name attribute (obj_name falls back to Name when
    # ObjectName is empty, which it always is for a CProxy) - verified real case
    # Ausgaenge_Scrolling_Content, JVS-ID 3066 (real CGroup) vs. 4194764 (its wrapping
    # CProxy, same Name). Harmless for the "rows" walk below (the real object's own
    # scroll_root_ids hit immediately re-sets scroll_container/acc_top right after the
    # CProxy's), but compute_scroll_viewports() below needs the real containers only.
    scroll_root_ids = {
        jid for jid, nm in obj_name.items()
        if nm.endswith("_Scrolling_Content") and obj_class.get(jid) != "CProxy"
    }

    rows = []  # (object_id, mask_id, scroll_container_id, row_top_px, row_height_px)
    masks_with_jvi = 0
    paired_softkeymasks = set()
    for root_jid in activemask_roots:
        root_path_rel = obj_path.get(root_jid)
        if not root_path_rel:
            continue
        root_jvi = os.path.normpath(os.path.join(pool_dir, root_path_rel))
        if not os.path.exists(root_jvi):
            continue
        masks_with_jvi += 1

        seen = set()
        roots = jvi_component_roots(root_jvi)
        geometry = resolve_tree_with_geometry(
            roots, obj_children, obj_class, obj_top, obj_height, scroll_root_ids, seen)

        # Fold-in: a paired SoftKeyMask's own objects (SoftKey/Image/Pointer etc. that
        # are NOT reachable from the DataMask/AlarmMask's own .jvi at all - verified
        # empirically for DataMask 1000 / SoftKeyMask 4000: 9 disjoint objects) get the
        # PAIRED mask's mask_id here, not their own SoftKeyMask's JVS-ID. That's correct
        # ONLY as long as this pool never switches a Working Set's SoftKeyMask at
        # runtime independently of its .jvi default pairing - true today because
        # isobus-3.0.0's Q_SoftKeyMask/cmd_change_softkey_mask FB type is never
        # instantiated anywhere in the FBT network (grep confirmed, 2026-09-19). If that
        # ever changes, this fold-in becomes wrong for the affected mask: the SoftKeyMask
        # would need its own mask_id bucket here (like the orphan-CSoftKeyMask branch
        # below) plus a second "active_softkey_mask" ECU-side comparison independent of
        # the paired DataMask's ActiveMask - see BERICHT_2026-09-18_VT_SICHTBARKEITS_KONZEPT.md
        # Abschnitt 6.
        skm_jid = jvi_softkeymask_id(root_jvi)
        if skm_jid is not None and skm_jid in obj_path:
            paired_softkeymasks.add(skm_jid)
            skm_jvi = os.path.normpath(os.path.join(pool_dir, obj_path[skm_jid]))
            if os.path.exists(skm_jvi):
                skm_roots = jvi_component_roots(skm_jvi)
                geometry.update(resolve_tree_with_geometry(
                    skm_roots, obj_children, obj_class, obj_top, obj_height,
                    scroll_root_ids, seen))

        for leaf_jid, (scroll_container, row_top, row_height) in geometry.items():
            rows.append((leaf_jid, root_jid, scroll_container or 0, row_top, row_height))

    # Orphan CSoftKeyMask (not paired to any Data/AlarmMask above) - own root,
    # mask_id = its own JVS-ID. 0 in the current pool (all 17 are paired).
    orphan_softkeymasks = sorted(
        jid for jid, cls in obj_class.items()
        if cls == "CSoftKeyMask" and jid not in paired_softkeymasks)
    for skm_jid in orphan_softkeymasks:
        geometry = _resolve_own_jvi_geometry(
            skm_jid, obj_path, pool_dir, obj_children, obj_class, obj_top, obj_height,
            scroll_root_ids)
        for leaf_jid, (scroll_container, row_top, row_height) in geometry.items():
            rows.append((leaf_jid, skm_jid, scroll_container or 0, row_top, row_height))

    # CWorkingSet - NOT ActiveMask-gated, see comment block above. 1 instance
    # in the current pool (JVS-ID 0).
    workingsets = sorted(jid for jid, cls in obj_class.items() if cls == "CWorkingSet")
    for ws_jid in workingsets:
        geometry = _resolve_own_jvi_geometry(
            ws_jid, obj_path, pool_dir, obj_children, obj_class, obj_top, obj_height,
            scroll_root_ids)
        for leaf_jid, (scroll_container, row_top, row_height) in geometry.items():
            rows.append((leaf_jid, ws_jid, scroll_container or 0, row_top, row_height))

    # CAuxFunction - mask-independent, see comment block above. No .jvi Path
    # (native pool object, children already in obj_children) - walk directly
    # from the AuxFunction's own JVS-ID so it also becomes its own leaf row.
    #
    # This same generic walk already resolves the CPointer-owning-AuxFunction2
    # question from BERICHT_2026-09-20_AUX_ZUWEISUNG_AUFTRAG.md for free: any
    # CPointer (ISO "Object Pointer") reachable under a CAuxFunction gets its
    # own row here with mask_id = that CAuxFunction's JVS-ID - exactly the
    # (object_id, owning_auxfunction2_id) pair the ECU-side GAux gate needs,
    # since resolve_tree_with_geometry() is class-agnostic (Franz: "schreib
    # ALLE Objekte auf"), not curated per root type. No script change was
    # needed for that request - verified 2026-09-20 against the real pool:
    # CAuxFunction = ISO "Auxiliary Function Type 2" here (confirmed no
    # "Type 1" objects exist - the 29000-29999 ID block per the ObjectID
    # convention is empty), and it is currently the ONLY class in
    # DefaultPool.jop occupying 31000-31999. Currently 0 of the pool's 44
    # CPointer objects sit under any CAuxFunction (the GAux icon-swap pool
    # this task describes isn't built yet) - same "0 real instances, but the
    # generic code path is already correct by construction" situation as
    # CWindowMask/CKeyGroup above, not a gap to fix once that pool exists.
    auxfunctions = sorted(jid for jid, cls in obj_class.items() if cls == "CAuxFunction")
    for af_jid in auxfunctions:
        seen = set()
        geometry = resolve_tree_with_geometry(
            [af_jid], obj_children, obj_class, obj_top, obj_height, scroll_root_ids, seen)
        for leaf_jid, (scroll_container, row_top, row_height) in geometry.items():
            rows.append((leaf_jid, af_jid, scroll_container or 0, row_top, row_height))

    rows.sort()

    scroll_viewports = compute_scroll_viewports(obj_class, obj_children, obj_height, scroll_root_ids)

    import hashlib
    jop_hash = "unknown"
    try:
        jop_bytes = open(os.path.join(pool_dir, "DefaultPool.jop"), "rb").read()
        jop_hash = hashlib.sha1(jop_bytes).hexdigest()[:12]
    except OSError:
        pass

    return rows, jop_hash, masks_with_jvi, scroll_viewports


def write_visibility_csv(rows, jop_hash, scroll_viewports, out_path):
    """Format spec: see BERICHT_2026-09-18_VT_SICHTBARKEITS_KONZEPT.md, Abschnitt 2.1.
    ~2.2x smaller on the wire/in flash than the JSON variant for this purely
    numeric, flat table - its only real advantage now that cJSON (ESP-IDF's
    standard JSON library) makes the "no library" argument moot on the ESP32.

    scroll_viewports ({scroll_container_id: viewport_height_px}, see
    compute_scroll_viewports()) is written as extra comment lines, not data rows -
    the ECU only reads the JSON variant for this (see
    BERICHT_2026-09-20_SCROLL_VIEWPORT_AUFTRAG.md), so the exact comment format here
    is secondary."""
    from datetime import datetime, timezone
    with open(out_path, "w", encoding="ascii", newline="\n") as f:
        f.write("# DefaultPool.vis.csv - VT object -> mask/scroll visibility table\n")
        f.write(f"# Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')} "
                f"from DefaultPool.jop (source hash: {jop_hash})\n")
        f.write("# Format version: 1\n")
        f.write("# Columns: object_id,mask_id,scroll_container_id,row_top_px,row_height_px\n")
        f.write("# Scroll viewport columns: scroll_container_id,viewport_height_px\n")
        for container_id, height in sorted(scroll_viewports.items()):
            f.write(f"# ScrollViewport: {container_id},{height}\n")
        for r in rows:
            f.write(",".join(str(v) for v in r) + "\n")


def write_visibility_json(rows, jop_hash, scroll_viewports, out_path):
    """Same data as write_visibility_csv, as JSON - offered as an alternative for
    whichever firmware/tooling ends up consuming this, in case a JSON library is
    already in use elsewhere in that codebase. Same schema, one object per row
    (not a nested per-object-id structure), so both files carry identical
    information and either can be regenerated from the other.

    scroll_viewports ({scroll_container_id: viewport_height_px}, see
    compute_scroll_viewports()) is emitted as its own top-level "scroll_viewports"
    array, same array-of-arrays shape as "rows" so the ECU-side parser can reuse
    the same row-reading code - see BERICHT_2026-09-20_SCROLL_VIEWPORT_AUFTRAG.md."""
    import json
    from datetime import datetime, timezone
    doc = {
        "format_version": 1,
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_jop_hash": jop_hash,
        "columns": ["object_id", "mask_id", "scroll_container_id", "row_top_px", "row_height_px"],
        "rows": [list(r) for r in rows],
        "scroll_viewport_columns": ["scroll_container_id", "viewport_height_px"],
        "scroll_viewports": [list(item) for item in sorted(scroll_viewports.items())],
    }
    with open(out_path, "w", encoding="ascii", newline="\n") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")


def main():
    (pool_dir, jop_path, data_only, name_filter,
     emit_visibility, emit_visibility_json) = parse_args()

    obj_class, obj_name, obj_children, obj_path, obj_top, obj_height = load_pool(jop_path)

    if emit_visibility or emit_visibility_json:
        rows, jop_hash, masks_with_jvi, scroll_viewports = compute_visibility_rows(
            pool_dir, obj_class, obj_name, obj_children, obj_path, obj_top, obj_height)
        if emit_visibility:
            write_visibility_csv(rows, jop_hash, scroll_viewports, emit_visibility)
            print(f"Wrote {len(rows)} rows ({masks_with_jvi} masks with a resolvable "
                  f".jvi, {len(scroll_viewports)} scroll viewports) to {emit_visibility}")
        if emit_visibility_json:
            write_visibility_json(rows, jop_hash, scroll_viewports, emit_visibility_json)
            print(f"Wrote {len(rows)} rows ({masks_with_jvi} masks with a resolvable "
                  f".jvi, {len(scroll_viewports)} scroll viewports) to {emit_visibility_json}")
        return

    mask_roots = sorted(
        jid for jid, cls in obj_class.items() if cls in ("CDataMask", "CAlarmMask"))
    workingsets = sorted(jid for jid, cls in obj_class.items() if cls == "CWorkingSet")
    auxfunctions = sorted(jid for jid, cls in obj_class.items() if cls == "CAuxFunction")

    total_data_objs_seen = set()
    any_mask_selected = False

    for dm_jid in mask_roots:
        dm_cls = obj_class.get(dm_jid, "?")
        dm_name = obj_name.get(dm_jid, "")
        if name_filter and name_filter not in dm_name.lower() and name_filter not in str(dm_jid):
            continue
        any_mask_selected = True

        dm_path_rel = obj_path.get(dm_jid)
        if not dm_path_rel:
            print(f"{dm_cls} {dm_jid} {dm_name!r}: no .jvi Path property, skipping")
            continue
        dm_jvi = os.path.normpath(os.path.join(pool_dir, dm_path_rel))
        if not os.path.exists(dm_jvi):
            print(f"{dm_cls} {dm_jid} {dm_name!r}: .jvi not found at {dm_jvi}, skipping")
            continue

        seen = set()
        roots = jvi_component_roots(dm_jvi)
        tree = resolve_tree(roots, obj_children, seen)

        skm_jid = jvi_softkeymask_id(dm_jvi)
        skm_tree = []
        skm_name = None
        if skm_jid is not None and skm_jid in obj_path:
            skm_name = obj_name.get(skm_jid, "")
            skm_jvi = os.path.normpath(os.path.join(pool_dir, obj_path[skm_jid]))
            if os.path.exists(skm_jvi):
                skm_roots = jvi_component_roots(skm_jvi)
                skm_tree = resolve_tree(skm_roots, obj_children, seen)

        print(f"=== {dm_cls} {dm_jid} {dm_name!r}  (+ SoftKeyMask {skm_jid} {skm_name!r}) ===")
        by_class = defaultdict(int)
        for depth, jid in tree + skm_tree:
            cls = obj_class.get(jid, "?")
            by_class[cls] += 1
            if cls in DATA_CLASSES:
                total_data_objs_seen.add(jid)
            if data_only and cls not in DATA_CLASSES:
                continue
            nm = obj_name.get(jid, "")
            print(f"  {'  ' * depth}{cls:<16} {nm:<55} ({jid})")
        summary = ", ".join(f"{c}:{n}" for c, n in sorted(by_class.items()))
        print(f"  -- {len(tree) + len(skm_tree)} objects total, deduplicated ({summary})")
        print()

    # WorkingSet and AuxFunction are NOT ActiveMask-gated (see module
    # docstring) - printed separately so their "=== ... ===" header can say
    # so explicitly, instead of implying an ActiveMask/SoftKeyMask pairing
    # that doesn't apply to them.
    for ws_jid in workingsets:
        ws_name = obj_name.get(ws_jid, "")
        if name_filter and name_filter not in ws_name.lower() and name_filter not in str(ws_jid):
            continue
        any_mask_selected = True

        ws_path_rel = obj_path.get(ws_jid)
        if not ws_path_rel:
            print(f"CWorkingSet {ws_jid} {ws_name!r}: no .jvi Path property, skipping")
            continue
        ws_jvi = os.path.normpath(os.path.join(pool_dir, ws_path_rel))
        if not os.path.exists(ws_jvi):
            print(f"CWorkingSet {ws_jid} {ws_name!r}: .jvi not found at {ws_jvi}, skipping")
            continue

        seen = set()
        roots = jvi_component_roots(ws_jvi)
        tree = resolve_tree(roots, obj_children, seen)

        print(f"=== CWorkingSet {ws_jid} {ws_name!r}  "
              f"(NOT ActiveMask-gated - always potentially visible, norm 4.6.8) ===")
        by_class = defaultdict(int)
        for depth, jid in tree:
            cls = obj_class.get(jid, "?")
            by_class[cls] += 1
            if cls in DATA_CLASSES:
                total_data_objs_seen.add(jid)
            if data_only and cls not in DATA_CLASSES:
                continue
            nm = obj_name.get(jid, "")
            print(f"  {'  ' * depth}{cls:<16} {nm:<55} ({jid})")
        summary = ", ".join(f"{c}:{n}" for c, n in sorted(by_class.items()))
        print(f"  -- {len(tree)} objects total ({summary})")
        print()

    for af_jid in auxfunctions:
        af_name = obj_name.get(af_jid, "")
        if name_filter and name_filter not in af_name.lower() and name_filter not in str(af_jid):
            continue
        any_mask_selected = True

        seen = set()
        tree = resolve_tree([af_jid], obj_children, seen)

        print(f"=== CAuxFunction {af_jid} {af_name!r}  "
              f"(mask-independent - AUX-assignment list, not any Data/Alarm Mask) ===")
        by_class = defaultdict(int)
        for depth, jid in tree:
            cls = obj_class.get(jid, "?")
            by_class[cls] += 1
            if cls in DATA_CLASSES:
                total_data_objs_seen.add(jid)
            if data_only and cls not in DATA_CLASSES:
                continue
            nm = obj_name.get(jid, "")
            print(f"  {'  ' * depth}{cls:<16} {nm:<55} ({jid})")
        summary = ", ".join(f"{c}:{n}" for c, n in sorted(by_class.items()))
        print(f"  -- {len(tree)} objects total ({summary})")
        print()

    if name_filter and not any_mask_selected:
        print(f"No mask/root matched filter {name_filter!r}")
        return

    total_data_in_pool = sum(1 for c in obj_class.values() if c in DATA_CLASSES)
    scope = f"selected mask(s) matching {name_filter!r}" if name_filter else "at least one mask"
    print(f"Data objects (CNumberVariable/CStringVariable) reachable from {scope}: "
          f"{len(total_data_objs_seen)} of {total_data_in_pool} total in pool")


if __name__ == "__main__":
    main()
