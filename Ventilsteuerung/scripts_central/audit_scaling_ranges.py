"""Read-only audit: for every object class covered by the ISO 11783-6
DataMask/SoftKeyMask ID-range table (Scaling.md), check whether each
object's current JVS-ID falls in the range matching where it's actually
used (reachable from a DataMask's vs a SoftKeyMask's <Components> roots).

Does not modify anything - prints a compliance report per class.
"""
import re
import xml.etree.ElementTree as ET
from collections import defaultdict

JOP_PATH = r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop"

JVI_FILES = {
    r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\DataMask_HOME.jvi": "DM",
    r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\SoftKeyMask_4000.jvi": "SKM",
    r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\Diagnosis\Ausgaenge\AusgaengeMask.jvi": "DM",
    r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\Diagnosis\Eingaenge\EingaengeMask.jvi": "DM",
    r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\Diagnosis\Ausgaenge\AusgaengeSoftKeyMask.jvi": "SKM",
    r"C:\git\fh\Krauternter\Ventilsteuerung\ISO-DesignerProjects\Workspace\DefaultPool\Diagnosis\Eingaenge\EingaengeSoftKeyMask.jvi": "SKM",
}

# class -> (DM range, SKM range or None)
RANGES = {
    "CDataMask":      ((1000, 1999), None),
    "CAlarmMask":     ((2000, 2999), None),
    "CGroup":         ((3000, 3499), (3500, 3999)),
    "CButton":        ((6000, 6999), None),
    "CSoftKey":       (None, (5000, 5999)),
    "CInputBoolean":  ((7000, 7999), None),
    "CInputString":   ((8000, 8999), None),
    "CInputNumber":   ((9000, 9999), None),
    "CInputList":     ((10000, 10999), None),
    "COutputText":    ((11000, 11499), (11500, 11999)),
    "COutputNumber":  ((12000, 12499), (12500, 12999)),
    "CLine":          ((13000, 13499), (13500, 13999)),
    "CRectangle":     ((14000, 14499), (14500, 14999)),
    "CEllipse":       ((15000, 15499), (15500, 15999)),
    "CPolygon":       ((16000, 16499), (16500, 16999)),
    "CMeter":         ((17000, 17599), None),
    "CLinearBargraph": ((18000, 18599), None),
    "CArchedBargraph": ((19000, 19599), None),
    "CImage":         ((20000, 20499), (20500, 20999)),
    "CFontStyle":     ((23000, 23499), (23500, 23999)),
    "CLineStyle":     ((24000, 24499), (24500, 24900)),
    "CFillStyle":     ((25000, 25499), (25500, 25999)),
    "COutputList":    ((30000, 30999), None),
}


def main():
    tree = ET.parse(JOP_PATH)
    root = tree.getroot()

    obj_class = {}
    obj_name = {}
    obj_children = {}
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

    both = reach["DM"] & reach["SKM"]
    neither = set(obj_class) - reach["DM"] - reach["SKM"]

    print(f"Total objects: {len(obj_class)}, DM-reachable: {len(reach['DM'])}, "
          f"SKM-reachable: {len(reach['SKM'])}, both: {len(both)}, neither: {len(neither)}")
    print()

    by_class = defaultdict(list)
    for jid, cls in obj_class.items():
        by_class[cls].append(jid)

    for cls, (dm_range, skm_range) in RANGES.items():
        ids = sorted(by_class.get(cls, []))
        if not ids:
            continue
        mismatches = []
        for jid in ids:
            in_dm = jid in reach["DM"]
            in_skm = jid in reach["SKM"]
            in_dm_range = dm_range and dm_range[0] <= jid <= dm_range[1]
            in_skm_range = skm_range and skm_range[0] <= jid <= skm_range[1]
            ok = True
            reason = None
            if in_dm and not in_skm:
                if dm_range and not in_dm_range:
                    ok = False
                    reason = f"used in DM but ID not in DM range {dm_range}"
            elif in_skm and not in_dm:
                if skm_range and not in_skm_range:
                    ok = False
                    reason = f"used in SKM but ID not in SKM range {skm_range}"
            elif in_dm and in_skm:
                reason = "used in BOTH DM and SKM (shared/hybrid)"
                ok = None
            else:
                reason = "not reachable from any mask root (orphan/unused or indirectly shared e.g. style object)"
                ok = None
            if ok is False:
                mismatches.append((jid, obj_name.get(jid, ""), reason))
        print(f"{cls}: {len(ids)} objects, range DM={dm_range} SKM={skm_range}, "
              f"{len(mismatches)} definite mismatches")
        for jid, name, reason in mismatches[:10]:
            print(f"    {jid} {name!r}: {reason}")
        if len(mismatches) > 10:
            print(f"    ... and {len(mismatches)-10} more")


if __name__ == "__main__":
    main()
