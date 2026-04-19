import os
import xml.etree.ElementTree as ET

# Configuration
ROOT_DIR = r"C:\git\ms"
EX_DIRS = [
    os.path.join(ROOT_DIR, r"4diac_training1\Ventilsteuerung\4diacIDE-workspace\test_B\Uebungen"),
    os.path.join(ROOT_DIR, r"4diac_training1\Ventilsteuerung\4diacIDE-workspace\test_AX\Uebungen")
]

LIB_DIRS = [
    os.path.join(ROOT_DIR, r"typelibrary\iec61131-3-3.0.0\typelib"),
    os.path.join(ROOT_DIR, r"typelibrary\events-3.0.0\typelib"),
    os.path.join(ROOT_DIR, r"typelibrary\convert-3.0.0\typelib"),
    os.path.join(ROOT_DIR, r"4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\adapter-3.0.0\typelib"),
    os.path.join(ROOT_DIR, r"4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\events_plus-3.0.0\typelib"),
]

def scan_valid_types():
    types = set()
    for lib_root in LIB_DIRS:
        if not os.path.exists(lib_root): continue
        for root, _, files in os.walk(lib_root):
            for f in files:
                if f.endswith(".fbt") or f.endswith(".adp"):
                    types.add(f[:-4])
    return types

def check_file(filepath, valid_types):
    issues = []
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        for fb in root.findall(".//FB"):
            name = fb.get("Name")
            full_type = fb.get("Type")
            
            if not name or not full_type:
                continue
                
            # Strip namespace from type
            if '::' in full_type:
                type_name = full_type.split('::')[-1]
            else:
                type_name = full_type
            
            # Check: Instance Name is a known Type, but not THE type used
            if name in valid_types:
                if name != type_name:
                    issues.append(f"  - FB '{name}': Instance Name is a valid Type, but actual Type is '{type_name}'")
            
            # Heuristic: Name implies a specific type?
            # e.g. Name="E_T_FF" -> expects E_T_FF*
            # e.g. Name="MyTimer" -> neutral
            
            # User example: Name="E_T_FF", Type="E_T_FF_SR"
            # Here "E_T_FF" is a valid type.
            
    except Exception as e:
        issues.append(f"  - Error parsing: {e}")
        
    if issues:
        print(f"File: {os.path.basename(filepath)}")
        for i in issues:
            print(i)

def main():
    print("Scanning for known FB Types...")
    valid_types = scan_valid_types()
    print(f"Found {len(valid_types)} valid types.")
    
    print("\nScanning Exercises for Naming Mismatches...")
    for d in EX_DIRS:
        if not os.path.exists(d): continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".SUB"):
                check_file(os.path.join(d, f), valid_types)

if __name__ == "__main__":
    main()
