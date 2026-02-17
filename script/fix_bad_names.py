import os
import xml.etree.ElementTree as ET
import re

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

def get_type_name(full_type):
    if '::' in full_type:
        return full_type.split('::')[-1]
    return full_type

def fix_file(filepath, valid_types):
    try:
        # Use read/write strings to preserve formatting better than ElementTree's write
        # But for Attribute replacement, regex/string replace is safer for indentation
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        replacements = [] # List of (old_name, new_name)
        
        # Track used names in file to ensure uniqueness
        used_names = set()
        for fb in root.findall(".//FB"):
            used_names.add(fb.get("Name"))
            
        for fb in root.findall(".//FB"):
            old_name = fb.get("Name")
            full_type = fb.get("Type")
            
            if not old_name or not full_type:
                continue
                
            type_name = get_type_name(full_type)
            
            # Check for bad naming
            if old_name in valid_types and old_name != type_name:
                # Issue detected!
                
                # Determine new name
                base_new_name = type_name
                new_name = base_new_name
                counter = 1
                while new_name in used_names:
                    # If we are renaming to self (e.g. E_T_FF -> E_T_FF), but it's used?
                    # No, old_name is E_T_FF (bad), type is E_T_FF_SR. New name should be E_T_FF_SR.
                    # If E_T_FF_SR is already used, make it E_T_FF_SR_1
                    new_name = f"{base_new_name}_{counter}"
                    counter += 1
                
                used_names.add(new_name)
                replacements.append((old_name, new_name))
                print(f"  Fixing {old_name} -> {new_name} (Type: {type_name})")

        if not replacements:
            return

        # Apply replacements
        # We must be careful not to replace partial matches or wrong attributes.
        # Replacing Name="Old" with Name="New"
        # Also need to replace references in Connections: Source="Old.Pin" -> Source="New.Pin"
        # and Destination="Old.Pin" -> Destination="New.Pin"
        
        new_content = content
        for old, new in replacements:
            # 1. FB Definition
            # <FB Name="Old" ...>
            # Use strict regex to avoid matching substrings
            # Name="Old" -> Name="New"
            new_content = re.sub(f'Name="{old}"', f'Name="{new}"', new_content)
            
            # 2. Connections
            # Source="Old. ...
            # Destination="Old. ...
            # Connection Source="Old. -> Source="New.
            
            # Regex for Source="Old.
            new_content = re.sub(f'Source="{old}\.', f'Source="{new}.', new_content)
            
            # Regex for Destination="Old.
            new_content = re.sub(f'Destination="{old}\.', f'Destination="{new}.', new_content)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

def main():
    print("Loading valid types...")
    valid_types = scan_valid_types()
    
    print("Fixing Exercises...")
    for d in EX_DIRS:
        if not os.path.exists(d): continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".SUB"):
                fix_file(os.path.join(d, f), valid_types)

if __name__ == "__main__":
    main()
