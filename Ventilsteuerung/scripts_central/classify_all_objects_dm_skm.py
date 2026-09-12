"""Extend ISO-Designer's Category Browser (<CategoryItems> in
DefaultPool.jops) with DM/SKM sub-categories for every Scaling.md-covered
object class that doesn't have one yet, matching the DM/SKM pattern the
user already built by hand for PictureGraphic and FontAttributes.

Per user decision: only classes that actually appear as their own row in
the ISO 11783-6 DataMask/SoftKeyMask ID-range table (Scaling.md) are
covered - not the ISO-Designer-internal CProxy/CPointer plumbing or the
CDataMask/CSoftKeyMask/CWorkingSet mask objects themselves, none of which
have a Scaling.md row to classify against.

Classification per object:
- If reachable (via BFS from a DataMask's or a SoftKeyMask's <Components>
  roots) from exactly one mask type, use that.
- Otherwise (not yet wired to anything, e.g. spare/reserved objects) fall
  back to which half of the class's ID range it currently sits in - this
  matches what the user's own FontAttributes category already did (all 30
  fonts are listed, including the ones no text object references yet).

Only creates a DM/SKM sub-category when it would be non-empty (a class
that's currently single-context, e.g. Button = DM-only in this pool,
gets just one sub-category, not an empty second one).
"""
import argparse
import io
import os
import re
import xml.etree.ElementTree as ET
from collections import defaultdict

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
JOPS_PATH = os.path.join(POOL_DIR, "DefaultPool.jops")

JVI_FILES = {
    os.path.join(POOL_DIR, "DataMask_HOME.jvi"): "DM",
    os.path.join(POOL_DIR, "SoftKeyMask_4000.jvi"): "SKM",
    os.path.join(POOL_DIR, "Diagnosis", "Ausgaenge", "AusgaengeMask.jvi"): "DM",
    os.path.join(POOL_DIR, "Diagnosis", "Eingaenge", "EingaengeMask.jvi"): "DM",
    os.path.join(POOL_DIR, "Diagnosis", "Ausgaenge", "AusgaengeSoftKeyMask.jvi"): "SKM",
    os.path.join(POOL_DIR, "Diagnosis", "Eingaenge", "EingaengeSoftKeyMask.jvi"): "SKM",
}

# class -> (category label, DM range, SKM range)
CLASSES = [
    ("CGroup",      "Container",      (3000, 3499),  (3500, 3999)),
    ("CButton",     "Button",         (6000, 6999),  None),
    ("CSoftKey",    "Softkey",        None,          (5000, 5999)),
    ("COutputText", "OutputString",   (11000, 11499), (11500, 11999)),
    ("CRectangle",  "Rectangle",      (14000, 14499), (14500, 14999)),
    ("CEllipse",    "Ellipse",        (15000, 15499), (15500, 15999)),
    ("CLineStyle",  "LineAttributes", (24000, 24499), (24500, 24900)),
    ("CFillStyle",  "FillAttributes", (25000, 25499), (25500, 25999)),
]


def main():
    tree = ET.parse(JOP_PATH)
    root = tree.getroot()

    obj_class = {}
    obj_children = {}
    for obj in root.iter("Object"):
        cls = obj.get("Class")
        jid_attr = obj.get("JVS-ID")
        if cls is None or jid_attr is None:
            continue
        jid = int(jid_attr)
        obj_class[jid] = cls
        kids = []
        objs_el = obj.find("Objects")
        if objs_el is not None:
            for child in objs_el.findall("Object"):
                cjid = child.get("JVS-ID")
                if cjid is not None:
                    kids.append(int(cjid))
        obj_children[jid] = kids

    roots = defaultdict(set)
    for path, mtype in JVI_FILES.items():
        t = ET.parse(path)
        comps = t.getroot().find("Components")
        if comps is None:
            continue
        for c in comps.findall("Component"):
            objs = c.find("Objects")
            if objs is None:
                continue
            for o in objs.findall("Object"):
                roots[mtype].add(int(o.get("JVS-ID")))

    reach = {}
    for mtype in ("DM", "SKM"):
        stack = list(roots[mtype])
        seen = set()
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(obj_children.get(cur, []))
        reach[mtype] = seen

    by_class = defaultdict(list)
    for jid, cls in obj_class.items():
        by_class[cls].append(jid)

    category_blocks = []
    for cls, label, dm_range, skm_range in CLASSES:
        ids = sorted(by_class.get(cls, []))
        if not ids:
            continue
        dm_bucket, skm_bucket = [], []
        for jid in ids:
            in_dm = jid in reach["DM"]
            in_skm = jid in reach["SKM"]
            if in_dm and not in_skm:
                dm_bucket.append(jid)
            elif in_skm and not in_dm:
                skm_bucket.append(jid)
            else:
                # Not (yet) reachable from either mask - fall back to which
                # half of the class's ID range it currently occupies.
                if dm_range and dm_range[0] <= jid <= dm_range[1]:
                    dm_bucket.append(jid)
                elif skm_range and skm_range[0] <= jid <= skm_range[1]:
                    skm_bucket.append(jid)
                else:
                    raise AssertionError(f"{cls} object {jid} fits neither range")

        inner = []
        if dm_bucket:
            inner.append('\t\t\t<Category Name="DM">\r\n')
            for jid in dm_bucket:
                inner.append(f'\t\t\t\t<Object JVS-ID="{jid}"/>\r\n')
            inner.append('\t\t\t</Category>\r\n')
        if skm_bucket:
            inner.append('\t\t\t<Category Name="SKM">\r\n')
            for jid in skm_bucket:
                inner.append(f'\t\t\t\t<Object JVS-ID="{jid}"/>\r\n')
            inner.append('\t\t\t</Category>\r\n')

        block = f'\t\t<Category Name="{label}">\r\n' + "".join(inner) + '\t\t</Category>\r\n'
        category_blocks.append(block)
        print(f"{label} ({cls}): DM={len(dm_bucket)} SKM={len(skm_bucket)} total={len(ids)}")

    with io.open(JOPS_PATH, "r", encoding="utf-8", newline="") as f:
        jops_text = f.read()
    assert "\r\n" in jops_text

    marker = "\t</CategoryItems>"
    assert marker in jops_text, "CategoryItems closing tag not found"
    new_text = "".join(category_blocks)
    jops_text = jops_text.replace(marker, new_text + marker, 1)

    with io.open(JOPS_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(jops_text)
    print(f"Added {len(category_blocks)} new categories to DefaultPool.jops.")


if __name__ == "__main__":
    main()
