"""Read-only: for every DataMask (+ its paired SoftKeyMask), recursively resolve
every object reachable from that mask's .jvi Components down through CProxy /
CGroup / CButton nesting to the leaves, and list them.

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
        "name", nargs="?", default=None,
        help="Only masks whose ObjectName or JVS-ID contains this (case-insensitive)",
    )
    args = parser.parse_args()

    pool_dir = os.path.join(os.path.dirname(script_dir), args.pool_dir)
    jop_path = os.path.join(pool_dir, args.jop_file)
    return pool_dir, jop_path, args.data_only, (args.name.lower() if args.name else None)


def load_pool(jop_path):
    """Return (obj_class, obj_name, obj_children, obj_path) dicts keyed by JVS-ID (int)."""
    tree = ET.parse(jop_path)
    root = tree.getroot()

    obj_class = {}
    obj_name = {}
    obj_children = {}
    obj_path = {}
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

        if cls in ("CDataMask", "CSoftKeyMask"):
            path_val = obj.find("./PropertySheet[@Name='Model']/Property[@Name='Path']/Value")
            if path_val is not None and path_val.text:
                obj_path[jid] = path_val.text.strip()

    return obj_class, obj_name, obj_children, obj_path


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


def main():
    pool_dir, jop_path, data_only, name_filter = parse_args()

    obj_class, obj_name, obj_children, obj_path = load_pool(jop_path)

    datamasks = sorted(jid for jid, cls in obj_class.items() if cls == "CDataMask")

    total_data_objs_seen = set()
    any_mask_selected = False

    for dm_jid in datamasks:
        dm_name = obj_name.get(dm_jid, "")
        if name_filter and name_filter not in dm_name.lower() and name_filter not in str(dm_jid):
            continue
        any_mask_selected = True

        dm_path_rel = obj_path.get(dm_jid)
        if not dm_path_rel:
            print(f"DataMask {dm_jid} {dm_name!r}: no .jvi Path property, skipping")
            continue
        dm_jvi = os.path.normpath(os.path.join(pool_dir, dm_path_rel))
        if not os.path.exists(dm_jvi):
            print(f"DataMask {dm_jid} {dm_name!r}: .jvi not found at {dm_jvi}, skipping")
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

        print(f"=== DataMask {dm_jid} {dm_name!r}  (+ SoftKeyMask {skm_jid} {skm_name!r}) ===")
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

    if name_filter and not any_mask_selected:
        print(f"No DataMask matched filter {name_filter!r}")
        return

    total_data_in_pool = sum(1 for c in obj_class.values() if c in DATA_CLASSES)
    scope = f"selected mask(s) matching {name_filter!r}" if name_filter else "at least one mask"
    print(f"Data objects (CNumberVariable/CStringVariable) reachable from {scope}: "
          f"{len(total_data_objs_seen)} of {total_data_in_pool} total in pool")


if __name__ == "__main__":
    main()
