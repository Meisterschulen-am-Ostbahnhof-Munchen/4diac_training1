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

Usage:
    python list_mask_objects.py                     # list every mask
    python list_mask_objects.py DataMask_Ernte       # only masks whose
                                                      # ObjectName contains this
    python list_mask_objects.py --data-only          # only CNumberVariable /
                                                      # CStringVariable leaves
    python list_mask_objects.py --data-only Ernte     # combine both

Prints, per DataMask (paired with its SoftKeyMask): every reachable object as
"depth  Class  ObjectName  (JVS-ID)", plus a summary count by class.
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

POOL_DIR = Path(r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool")
JOP_PATH = POOL_DIR / "DefaultPool.jop"

DATA_CLASSES = {"CNumberVariable", "CStringVariable"}


def load_pool(jop_path):
    """Return (obj_class, obj_name, obj_children) dicts keyed by JVS-ID (int)."""
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


def resolve_tree(root_ids, obj_children, obj_class, obj_name):
    """DFS from root_ids through obj_children; returns list of (depth, jid) in
    parent-immediately-followed-by-children order (so printed indentation
    reads as an actual tree), each jid visited exactly once (dedup on
    re-entry via shared CProxy targets, e.g. a common background rectangle -
    a repeat visit is skipped, not reprinted under its second parent)."""
    order = []
    seen = set()

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
    args = sys.argv[1:]
    data_only = "--data-only" in args
    args = [a for a in args if a != "--data-only"]
    name_filter = args[0].lower() if args else None

    obj_class, obj_name, obj_children, obj_path = load_pool(JOP_PATH)

    # id -> (class, name) for the *_MASK* objects only, to iterate DataMasks
    datamasks = sorted(
        (jid for jid, cls in obj_class.items() if cls == "CDataMask"),
        key=lambda jid: jid,
    )

    total_data_objs_seen = set()

    for dm_jid in datamasks:
        dm_name = obj_name.get(dm_jid, "")
        if name_filter and name_filter not in dm_name.lower() and name_filter not in str(dm_jid):
            continue

        dm_path_rel = obj_path.get(dm_jid)
        if not dm_path_rel:
            print(f"DataMask {dm_jid} {dm_name!r}: no .jvi Path property, skipping")
            continue
        dm_jvi = (POOL_DIR / dm_path_rel).resolve()
        if not dm_jvi.exists():
            print(f"DataMask {dm_jid} {dm_name!r}: .jvi not found at {dm_jvi}, skipping")
            continue

        roots = jvi_component_roots(dm_jvi)
        tree = resolve_tree(roots, obj_children, obj_class, obj_name)

        skm_jid = jvi_softkeymask_id(dm_jvi)
        skm_tree = []
        skm_name = None
        if skm_jid is not None and skm_jid in obj_path:
            skm_name = obj_name.get(skm_jid, "")
            skm_jvi = (POOL_DIR / obj_path[skm_jid]).resolve()
            if skm_jvi.exists():
                skm_roots = jvi_component_roots(skm_jvi)
                skm_tree = resolve_tree(skm_roots, obj_children, obj_class, obj_name)

        print(f"=== DataMask {dm_jid} {dm_name!r}  (+ SoftKeyMask {skm_jid} {skm_name!r}) ===")
        by_class = defaultdict(int)
        for depth, jid in tree + [(d, j) for d, j in skm_tree]:
            cls = obj_class.get(jid, "?")
            by_class[cls] += 1
            if data_only and cls not in DATA_CLASSES:
                continue
            nm = obj_name.get(jid, "")
            print(f"  {'  ' * depth}{cls:<16} {nm:<55} ({jid})")
            if cls in DATA_CLASSES:
                total_data_objs_seen.add(jid)
        summary = ", ".join(f"{c}:{n}" for c, n in sorted(by_class.items()))
        print(f"  -- {len(tree) + len(skm_tree)} objects total ({summary})")
        print()

    print(f"Data objects (CNumberVariable/CStringVariable) reachable from at least one mask: "
          f"{len(total_data_objs_seen)} of "
          f"{sum(1 for c in obj_class.values() if c in DATA_CLASSES)} total in pool")


if __name__ == "__main__":
    main()
