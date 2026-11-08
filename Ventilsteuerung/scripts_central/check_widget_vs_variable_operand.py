"""Read-only: find CNumberVariable objects in the real pool (DefaultPool.jop)
that are bound to MULTIPLE CInputNumber/COutputNumber widgets (a Variable
Reference, per ISO 11783-6 Annex B - e.g. one InputNumber edit field and one
OutputNumber display sharing the same variable) whose Offset/Scale/MinValue/
MaxValue are NOT identical across those widgets.

Why this matters: the widget only ever displays/edits the RAW value that
travels over the wire via the bound variable; Offset/Scale (and, for
CInputNumber, MinValue/MaxValue) are each widget's OWN local interpretation
of that raw value. If two widgets share one variable but disagree on
Offset/Scale, the same underlying value is shown/edited as two different
physical numbers depending on which widget the operator is looking at/using
- a real, silent inconsistency bug, independent of any FORTE/GCF-constant
question.

Algorithm (Franz, 2026-09-19 - Schritt 1-3):
  1. Find every CNumberVariable in the pool (JVS-ID + ObjectName).
  2. For each one, find every CInputNumber/COutputNumber widget bound to it
     (the widget->variable Variable-Reference binding structure in the .jop
     is list_mask_objects.py's VR_CAPABLE_CLASSES + the "has_variable_child"
     test from its resolve_tree_with_geometry() - reused here via import,
     not re-derived, so a future fix/extension to that logic automatically
     applies here too). A variable can be bound to more than one widget.
  3. For every variable with >=2 bound widgets, compare Offset, Scale,
     MinValue, MaxValue across all of them. COutputNumber has no MinValue/
     MaxValue Property at all (verified against this pool's real .jop:
     CInputNumber's PropertySheet is "EditBox" and has all four;
     COutputNumber's PropertySheet is "Text" and only has Offset/Scale) -
     each property is only compared across the widgets that actually carry
     it, so an OutputNumber+InputNumber pair sharing a variable is only
     checked on Offset/Scale, never flagged for a MinValue/MaxValue the
     OutputNumber simply doesn't have. Values are compared numerically (e.g.
     Scale "1" vs "1.0" is NOT a mismatch), not as raw strings. Not all
     identical -> reported: variable name, the differing property, and each
     involved widget's name/JVS-ID/class/value.

Widget-vs-bound-variable detection is NOT reinvented here: it reuses
list_mask_objects.py's load_pool() (.jop parsing) and VR_CAPABLE_CLASSES
(same folder, imported below). The report is restricted to CInputNumber/
COutputNumber (the two classes with real, verified instances in this pool
per the comment above VR_CAPABLE_CLASSES in that file) - the underlying
binding lookup itself still uses the full VR_CAPABLE_CLASSES table, so it
costs nothing to stay generic and costs nothing to add a class later.

Usage:
    python check_widget_vs_variable_operand.py [--repo-root PATH] [--jop PATH]

--repo-root defaults to the Krauternter repo root (two levels up from this
script: Ventilsteuerung/scripts_central/ -> Ventilsteuerung/ -> repo root),
matching this project's convention of not hardcoding absolute paths.
"""
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# Reused, not reimplemented - see module docstring. ET is list_mask_objects's
# own defusedxml-or-stdlib ElementTree alias - reusing it (instead of a second
# import xml.etree.ElementTree here) also avoids a second "defusedxml not
# installed" stderr note when it's missing.
from list_mask_objects import load_pool, VR_CAPABLE_CLASSES, ET  # noqa: E402

REPORTED_WIDGET_CLASSES = {"CInputNumber", "COutputNumber"}

# See module docstring for why COutputNumber lacks MinValue/MaxValue.
NUMERIC_PROPERTY_NAMES = ["Offset", "Scale", "MinValue", "MaxValue"]


def parse_args():
    default_repo_root = os.path.dirname(os.path.dirname(SCRIPT_DIR))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root", default=default_repo_root,
        help="Krauternter repo root (default: inferred from this script's "
             "own location, %(default)s)",
    )
    parser.add_argument(
        "--jop", default=None,
        help="Path to DefaultPool.jop (default: "
             "<repo-root>/Ventilsteuerung/ISO-DesignerProjects/Workspace/"
             "DefaultPool/DefaultPool.jop)",
    )
    return parser.parse_args()


def collect_number_variables(obj_class, obj_name):
    """Schritt 1. Returns dict: variable_jvs_id (int) -> ObjectName, for
    every CNumberVariable object in the pool."""
    return {jid: obj_name.get(jid, "") for jid, cls in obj_class.items() if cls == "CNumberVariable"}


def collect_variable_widget_bindings(obj_class, obj_children):
    """Schritt 2. Returns dict: variable_jvs_id (int) -> list of
    widget_jvs_id (int), for every CInputNumber/COutputNumber widget bound
    to that variable (same structural "has_variable_child" test as
    list_mask_objects.py's resolve_tree_with_geometry()). This is the
    REVERSE direction of a widget->variable lookup, and collects ALL bound
    widgets per variable (not just the first) - a variable can be bound to
    multiple widgets at once, which is exactly the case Schritt 3 needs to
    compare."""
    bindings = {}
    for jid, cls in obj_class.items():
        if cls not in REPORTED_WIDGET_CLASSES:
            continue
        variable_classes = VR_CAPABLE_CLASSES.get(cls)
        if variable_classes is None:
            continue
        for child in obj_children.get(jid, []):
            if obj_class.get(child) in variable_classes:
                bindings.setdefault(child, []).append(jid)
    return bindings


def collect_widget_numeric_properties(jop_path):
    """Schritt 3 (data gathering half). Returns dict: widget_jvs_id (int) ->
    {property_name: raw_value_string}, for every CInputNumber/COutputNumber
    object's Offset/Scale/MinValue/MaxValue properties actually present on
    it (COutputNumber simply has no MinValue/MaxValue Property element at
    all, so those two keys are just absent for it, never defaulted/guessed).

    Not read from load_pool() (which only captures Height/Top/.jvi-Path, not
    these four generic Property values) - a second, separate parse of the
    same .jop, restricted to the two REPORTED_WIDGET_CLASSES."""
    tree = ET.parse(jop_path)
    root = tree.getroot()
    props = {}
    for obj in root.iter("Object"):
        cls = obj.get("Class")
        if cls not in REPORTED_WIDGET_CLASSES:
            continue
        jid_attr = obj.get("JVS-ID")
        if jid_attr is None:
            continue
        jid = int(jid_attr)
        widget_props = {}
        for prop_name in NUMERIC_PROPERTY_NAMES:
            val_el = obj.find(f"./PropertySheet/Property[@Name='{prop_name}']/Value")
            if val_el is not None and val_el.text and val_el.text.strip():
                widget_props[prop_name] = val_el.text.strip()
        props[jid] = widget_props
    return props


def find_inconsistent_widget_scaling(jop_path):
    """Schritt 3 (comparison half). For every CNumberVariable bound to >=2
    CInputNumber/COutputNumber widgets (collect_variable_widget_bindings),
    compares Offset/Scale/MinValue/MaxValue across all of them, per-property,
    numerically (e.g. Scale "1" vs "1.0" is NOT a mismatch - both parse to
    the same float; only a genuinely different value is), restricted for
    each property to the widgets that actually carry it. Returns a list of
    finding dicts, one per (variable, differing property) - not one per
    variable, so a variable with e.g. both a Scale AND an Offset mismatch
    produces two separate, clearly attributable findings."""
    obj_class, obj_name, obj_children, _obj_path, _obj_top, _obj_height = load_pool(jop_path)
    number_variables = collect_number_variables(obj_class, obj_name)
    variable_widgets = collect_variable_widget_bindings(obj_class, obj_children)
    widget_props = collect_widget_numeric_properties(jop_path)

    findings = []
    for var_id, widget_ids in sorted(variable_widgets.items()):
        if len(widget_ids) < 2:
            continue  # nothing to compare against - can't disagree with itself
        for prop_name in NUMERIC_PROPERTY_NAMES:
            per_widget_raw = {}
            for wid in widget_ids:
                val = widget_props.get(wid, {}).get(prop_name)
                if val is not None:
                    per_widget_raw[wid] = val
            distinct_numeric_values = {float(v) for v in per_widget_raw.values()}
            if len(distinct_numeric_values) > 1:
                findings.append({
                    "var_id": var_id,
                    "var_name": number_variables.get(var_id, ""),
                    "property": prop_name,
                    "widgets": [
                        {
                            "widget_id": wid,
                            "widget_name": obj_name.get(wid, ""),
                            "widget_class": obj_class.get(wid, ""),
                            "value": val,
                        }
                        for wid, val in sorted(per_widget_raw.items())
                    ],
                })
    return findings, number_variables, variable_widgets


def run(repo_root, jop_path=None):
    ventilsteuerung_root = os.path.join(repo_root, "Ventilsteuerung")
    if jop_path is None:
        jop_path = os.path.join(
            ventilsteuerung_root, "ISO-DesignerProjects", "Workspace",
            "DefaultPool", "DefaultPool.jop")
    return find_inconsistent_widget_scaling(jop_path)


def main():
    args = parse_args()
    findings, number_variables, variable_widgets = run(args.repo_root, args.jop)

    multi_widget_variables = {v: w for v, w in variable_widgets.items() if len(w) >= 2}
    print(f"CNumberVariable-Objekte im Pool: {len(number_variables)}")
    print(f"davon an >=2 CInputNumber/COutputNumber-Widgets gebunden: {len(multi_widget_variables)}")
    print()

    if not findings:
        print("Keine Inkonsistenzen gefunden: bei allen NumberVariablen mit mehreren "
              "gebundenen Widgets stimmen Offset/Scale/MinValue/MaxValue ueberein "
              "(jeweils nur ueber die Widgets verglichen, die die Property tatsaechlich haben).")
        return

    print(f"{len(findings)} Inkonsistenz(en) gefunden:\n")
    for f in findings:
        print(f"- NumberVariable {f['var_name']!r} (JVS-ID {f['var_id']}): "
              f"'{f['property']}' stimmt nicht ueberein zwischen den gebundenen Widgets")
        for w in f["widgets"]:
            print(f"    {w['widget_class']:<14} {w['widget_name']:<55} "
                  f"(JVS-ID {w['widget_id']})  {f['property']}={w['value']}")
        print()


if __name__ == "__main__":
    main()
