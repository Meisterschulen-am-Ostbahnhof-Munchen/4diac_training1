import xml.etree.ElementTree as ET
import os
import re
from pathlib import Path
from collections import defaultdict

def find_sub_files(root_dir):
    """Find all .SUB files recursively."""
    for path in Path(root_dir).rglob("*.SUB"):
        yield path

def has_nvs_or_ini(content):
    """Check if file contains NVS or INI storage blocks."""
    return 'NVS' in content or 'INI' in content

def extract_obj_param(fb_elem, param_name):
    """Extract parameter value from FB element."""
    for param in fb_elem.findall("Parameter"):
        if param.get("Name") == param_name:
            return param.get("Value")
    return None

def get_fb_type(fb_elem):
    return fb_elem.get("Type", "")

def get_fb_name(fb_elem):
    return fb_elem.get("Name", "")

def is_input_numericvalue(fb_type):
    """Check if FB type is an Input NumericValue block."""
    return (
        "NumericValue" in fb_type 
        and "Q_NumericValue" not in fb_type
        and ("PHYS" in fb_type or "IDA" in fb_type or "ID" in fb_type)
    )

def is_output_q_numericvalue(fb_type):
    """Check if FB type is an Output Q_NumericValue block."""
    return "Q_NumericValue" in fb_type

def is_nvs_or_ini_type(fb_type):
    """Check if FB type is NVS or INI storage."""
    return "NVS" in fb_type or "INI" in fb_type

def is_nvs_or_ini_fb(fb_elem):
    fb_type = get_fb_type(fb_elem)
    fb_name = get_fb_name(fb_elem)
    return is_nvs_or_ini_type(fb_type) or is_nvs_or_ini_type(fb_name)

def parse_obj_value(val):
    """Parse object value to determine family and number."""
    if not val:
        return None, None
    
    # Match patterns like InputNumber_I1, OutputNumber_N3, etc.
    m = re.search(r'(InputNumber_I|OutputNumber_N|Input|Output|I|N)(\d+)', val)
    if m:
        prefix = m.group(1)
        num = m.group(2)
        
        # Normalize prefix
        if 'Input' in prefix or prefix == 'I':
            family = 'I'
        elif 'Output' in prefix or prefix == 'N':
            family = 'N'
        else:
            family = prefix
        
        return family, num
    
    # Try other patterns
    if val.startswith("InputNumber_I"):
        num = val.replace("InputNumber_I", "")
        if num.isdigit():
            return "I", num
    elif val.startswith("OutputNumber_N"):
        num = val.replace("OutputNumber_N", "")
        if num.isdigit():
            return "N", num
    elif val.startswith("I") and val[1:].isdigit():
        return "I", val[1:]
    elif val.startswith("N") and val[1:].isdigit():
        return "N", val[1:]
    
    return "OTHER", val

def get_connected_value(root, fb_name, param_name):
    """Try to find value from DataConnections wiring to this parameter."""
    data_conns = root.find(".//DataConnections")
    if data_conns is None:
        return None
    
    target = f"{fb_name}.{param_name}"
    for conn in data_conns.findall("Connection"):
        if conn.get("Destination") == target:
            source = conn.get("Source")
            # If source is a simple value/constant or another FB parameter
            if source and "." not in source:
                return source
    return None

def analyze_file(filepath):
    """Analyze a single .SUB file."""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError as e:
        return {"error": f"XML parse error: {e}"}
    
    # Check for NVS/INI storage blocks
    has_storage = False
    storage_names = []
    
    # Check direct FBs
    for fb in root.findall(".//FB"):
        if is_nvs_or_ini_fb(fb):
            has_storage = True
            storage_names.append(get_fb_name(fb))
    
    # Also check SubApps
    for subapp in root.findall(".//SubApp"):
        subapp_type = get_fb_type(subapp)
        if "NVS" in subapp_type or "INI" in subapp_type:
            has_storage = True
            storage_names.append(get_fb_name(subapp))
    
    if not has_storage:
        return None  # Skip files without storage
    
    # Find Input and Output NumericValue blocks
    inputs = []
    outputs = []
    
    # Check direct FBs
    for fb in root.findall(".//FB"):
        fb_type = get_fb_type(fb)
        fb_name = get_fb_name(fb)
        
        if is_input_numericvalue(fb_type):
            st_obj = extract_obj_param(fb, "stObj")
            u16_obj = extract_obj_param(fb, "u16ObjId")
            val = st_obj or u16_obj
            
            # Also check connections
            if not val:
                val = get_connected_value(root, fb_name, "stObj") or get_connected_value(root, fb_name, "u16ObjId")
            
            inputs.append({
                "name": fb_name,
                "type": fb_type,
                "value": val,
                "param": "stObj" if st_obj else ("u16ObjId" if u16_obj else None)
            })
        
        if is_output_q_numericvalue(fb_type):
            st_obj = extract_obj_param(fb, "stObj")
            u16_obj = extract_obj_param(fb, "u16ObjId")
            val = st_obj or u16_obj
            
            if not val:
                val = get_connected_value(root, fb_name, "stObj") or get_connected_value(root, fb_name, "u16ObjId")
            
            outputs.append({
                "name": fb_name,
                "type": fb_type,
                "value": val,
                "param": "stObj" if st_obj else ("u16ObjId" if u16_obj else None)
            })
    
    # Check SubApp parameters (for wrapper files)
    for subapp in root.findall(".//SubApp"):
        subapp_name = get_fb_name(subapp)
        subapp_type = get_fb_type(subapp)
        
        # Check if this subapp references a NumericValue-related type
        if "NumericValue" in subapp_type and "Q_NumericValue" not in subapp_type:
            st_obj = extract_obj_param(subapp, "stObj")
            u16_obj = extract_obj_param(subapp, "u16ObjId")
            val = st_obj or u16_obj
            if val:
                inputs.append({
                    "name": subapp_name,
                    "type": subapp_type,
                    "value": val,
                    "param": "stObj" if st_obj else "u16ObjId",
                    "is_subapp": True
                })
        
        if "Q_NumericValue" in subapp_type:
            st_obj = extract_obj_param(subapp, "stObj")
            u16_obj = extract_obj_param(subapp, "u16ObjId")
            val = st_obj or u16_obj
            if val:
                outputs.append({
                    "name": subapp_name,
                    "type": subapp_type,
                    "value": val,
                    "param": "stObj" if st_obj else "u16ObjId",
                    "is_subapp": True
                })
    
    if not inputs and not outputs:
        return None  # No relevant blocks
    
    # Check consistency
    issues = []
    
    # Build family map
    input_families = {}
    output_families = {}
    
    for inp in inputs:
        if inp["value"]:
            family, num = parse_obj_value(inp["value"])
            if family and num:
                key = f"{family}{num}"
                input_families[key] = inp
    
    for out in outputs:
        if out["value"]:
            family, num = parse_obj_value(out["value"])
            if family and num:
                key = f"{family}{num}"
                output_families[key] = out
    
    # Check mappings
    # I1 should pair with N1, I2 with N2, etc.
    # In the same file, if Input uses I3, Output should use N3
    
    # Find all I and N numbers
    i_numbers = set()
    n_numbers = set()
    
    for key in input_families:
        if key.startswith("I"):
            i_numbers.add(key[1:])
    
    for key in output_families:
        if key.startswith("N"):
            n_numbers.add(key[1:])
    
    # Check for mismatches
    for num in i_numbers:
        if num not in n_numbers:
            # No matching N found - check if there's an N with different number
            other_n = [k for k in output_families if k.startswith("N")]
            if other_n:
                issues.append(
                    f"Input I{num} found but no matching Output N{num}. "
                    f"Outputs present: {', '.join(sorted(other_n))}"
                )
    
    for num in n_numbers:
        if num not in i_numbers:
            other_i = [k for k in input_families if k.startswith("I")]
            if other_i:
                issues.append(
                    f"Output N{num} found but no matching Input I{num}. "
                    f"Inputs present: {', '.join(sorted(other_i))}"
                )
    
    # If both I and N with same number exist, that's good
    # If I and N with different numbers exist, that's a mismatch
    common_nums = i_numbers & n_numbers
    mismatch_i = i_numbers - n_numbers
    mismatch_n = n_numbers - i_numbers
    
    if mismatch_i and mismatch_n:
        for i_num in mismatch_i:
            for n_num in mismatch_n:
                issues.append(
                    f"MISMATCH: Input I{i_num} does not match Output N{n_num} "
                    f"(expected N{i_num} or I{n_num})"
                )
    
    # Check for cases where input and output have same family (both I or both N)
    for inp in inputs:
        if inp["value"]:
            family, num = parse_obj_value(inp["value"])
            if family == "N":
                issues.append(
                    f"Input block '{inp['name']}' uses Output-style value: {inp['value']}"
                )
    
    for out in outputs:
        if out["value"]:
            family, num = parse_obj_value(out["value"])
            if family == "I":
                issues.append(
                    f"Output block '{out['name']}' uses Input-style value: {out['value']}"
                )
    
    return {
        "inputs": inputs,
        "outputs": outputs,
        "storage": storage_names,
        "issues": issues,
        "i_numbers": sorted(i_numbers),
        "n_numbers": sorted(n_numbers),
        "common_nums": sorted(common_nums)
    }

def main():
    root_dir = r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace"
    
    results = []
    checked = 0
    skipped = 0
    
    for filepath in find_sub_files(root_dir):
        checked += 1
        result = analyze_file(filepath)
        if result:
            results.append((filepath, result))
        else:
            skipped += 1
    
    # Print summary
    print("=" * 80)
    print(f"NVS/INI Input/Output Consistency Check")
    print(f"=" * 80)
    print(f"Total .SUB files scanned: {checked}")
    print(f"Files with NVS/INI + NumericValue blocks: {len(results)}")
    print(f"Files skipped (no relevant blocks): {skipped}")
    print()
    
    # Files with issues
    files_with_issues = [(fp, r) for fp, r in results if r.get("issues")]
    files_clean = [(fp, r) for fp, r in results if not r.get("issues")]
    
    if files_with_issues:
        print(f"FILES WITH ISSUES ({len(files_with_issues)}):")
        print("-" * 80)
        for fp, result in files_with_issues:
            rel_path = fp.relative_to(Path(root_dir).parent.parent)
            print(f"\n{rel_path}")
            print(f"  Storage blocks: {', '.join(result['storage'])}")
            
            for inp in result["inputs"]:
                print(f"  Input:  {inp['name']} ({inp['type']}) -> {inp['param']}={inp['value']}")
            
            for out in result["outputs"]:
                print(f"  Output: {out['name']} ({out['type']}) -> {out['param']}={out['value']}")
            
            for issue in result["issues"]:
                print(f"  *** ISSUE: {issue}")
    else:
        print("No issues found!")
    
    print()
    print("-" * 80)
    print(f"Files with issues: {len(files_with_issues)}")
    print(f"Files OK: {len(files_clean)}")
    print("-" * 80)
    
    # Print all scanned files for reference
    print("\n\nALL SCANNED FILES (for reference):")
    print("=" * 80)
    for fp, result in sorted(results, key=lambda x: str(x[0])):
        rel_path = fp.relative_to(Path(root_dir).parent.parent)
        status = "OK" if not result.get("issues") else "ISSUE"
        
        input_vals = [f"{i['value']}" for i in result["inputs"] if i["value"]]
        output_vals = [f"{o['value']}" for o in result["outputs"] if o["value"]]
        
        print(f"[{status}] {rel_path}")
        print(f"       Inputs:  {', '.join(input_vals) if input_vals else 'none'}")
        print(f"       Outputs: {', '.join(output_vals) if output_vals else 'none'}")
        if result.get("issues"):
            for issue in result["issues"]:
                print(f"       *** {issue}")

if __name__ == "__main__":
    main()
