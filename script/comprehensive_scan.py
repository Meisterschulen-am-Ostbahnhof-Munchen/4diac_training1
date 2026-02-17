import os
import xml.etree.ElementTree as ET

ROOT_DIR = r"C:\git\ms"
STD_EX_DIR = os.path.join(ROOT_DIR, r"4diac_training1\Ventilsteuerung\4diacIDE-workspace\test_B\Uebungen")
AX_EX_DIR = os.path.join(ROOT_DIR, r"4diac_training1\Ventilsteuerung\4diacIDE-workspace\test_AX\Uebungen")

LIB_DIRS = [
    os.path.join(ROOT_DIR, r"typelibrary\iec61131-3-3.0.0\typelib"),
    os.path.join(ROOT_DIR, r"typelibrary\events-3.0.0\typelib"),
    os.path.join(ROOT_DIR, r"typelibrary\convert-3.0.0\typelib"),
    os.path.join(ROOT_DIR, r"4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\adapter-3.0.0\typelib"),
    os.path.join(ROOT_DIR, r"4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\events_plus-3.0.0\typelib"),
]

def get_fb_types_from_sub(filepath):
    types = set()
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        for fb in root.findall(".//FB"):
            t = fb.get("Type")
            if t:
                if '::' in t:
                    types.add(t.split('::')[-1])
                else:
                    types.add(t)
    except:
        pass
    return types

def map_all_used_fbs():
    used = set()
    for d in [STD_EX_DIR, AX_EX_DIR]:
        if not os.path.exists(d): continue
        for f in os.listdir(d):
            if f.endswith(".SUB"):
                used.update(get_fb_types_from_sub(os.path.join(d, f)))
    return used

def scan_libs():
    all_fbs = {} # FB_Name -> Path
    for lib_root in LIB_DIRS:
        if not os.path.exists(lib_root): continue
        for root, dirs, files in os.walk(lib_root):
            for f in files:
                if f.endswith(".fbt") or f.endswith(".adp"):
                    name = f[:-4]
                    all_fbs[name] = os.path.join(root, f)
    return all_fbs

def main():
    used_fbs = map_all_used_fbs()
    lib_fbs = scan_libs()
    
    unused = []
    for name in sorted(lib_fbs.keys()):
        if name not in used_fbs:
            unused.append((name, lib_fbs[name]))
            
    print(f"Total Unique FBs in Libraries: {len(lib_fbs)}")
    print(f"Total Unique FBs used in Exercises: {len(used_fbs)}")
    print(f"Unused FBs: {len(unused)}")
    print("\n--- Unused FBs (Top 50) ---")
    for name, path in unused[:100]:
        # Simplify path for display
        rel_path = os.path.relpath(path, ROOT_DIR)
        print(f"- {name} ({rel_path})")

if __name__ == "__main__":
    main()
