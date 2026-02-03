import os

# Configuration
ROOT_DIR = r"C:\git\ms"
STD_LIB_ROOT = os.path.join(ROOT_DIR, r"typelibrary")
AX_LIB_ROOT = os.path.join(ROOT_DIR, r"4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\adapter-3.0.0\typelib")

def get_fbs(root_dir):
    fbs = set()
    if not os.path.exists(root_dir):
        return fbs
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".fbt") or f.endswith(".adp"):
                # Store relative path to grouping folder for better context?
                # Or just name. Let's try name first.
                name = f[:-4]
                fbs.add(name)
    return fbs

def main():
    std_fbs = get_fbs(STD_LIB_ROOT)
    ax_fbs = get_fbs(AX_LIB_ROOT)
    
    print(f"Standard FBs found: {len(std_fbs)}")
    print(f"AX FBs found: {len(ax_fbs)}")
    
    # Analyze missing counterparts
    # Logic: 
    # 1. E_XXX -> AX_XXX (Events)
    # 2. FB_XXX -> AX_FB_XXX (IEC61131)
    # 3. F_XXX -> AX_XXX (Functions, maybe? e.g. F_MUX -> AX_MUX)
    
    missing_ax = []
    
    for std in sorted(list(std_fbs)):
        potential_ax_names = []
        
        if std.startswith("E_"):
            potential_ax_names.append("AX_" + std[2:]) # E_DELAY -> AX_DELAY (or AE_DELAY)
            potential_ax_names.append("AE_" + std[2:])
        elif std.startswith("FB_"):
            potential_ax_names.append("AX_" + std)     # FB_SR -> AX_FB_SR
        elif std.startswith("F_"):
            potential_ax_names.append("AX_" + std[2:]) # F_MUX_2 -> AX_MUX_2
        else:
            # Generic prefix?
            potential_ax_names.append("AX_" + std)
            
        found = False
        for ax in potential_ax_names:
            if ax in ax_fbs:
                found = True
                break
        
        if not found:
            # Filter some noise? No, let's see all.
            missing_ax.append(f"{std} (Expected: {potential_ax_names})")
            
    print("\n--- Potential Missing AX FBs (Top 100) ---")
    for m in missing_ax[:100]:
        print(m)

if __name__ == "__main__":
    main()
