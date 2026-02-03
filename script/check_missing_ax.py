import os

# Configuration
ROOT_DIR = r"C:\git\ms"
STD_EX_DIR = os.path.join(ROOT_DIR, r"4diac_training1\Ventilsteuerung\4diacIDE-workspace\test_B\Uebungen")
AX_EX_DIR = os.path.join(ROOT_DIR, r"4diac_training1\Ventilsteuerung\4diacIDE-workspace\test_AX\Uebungen")

def main():
    std_subs = set()
    if os.path.exists(STD_EX_DIR):
        for f in os.listdir(STD_EX_DIR):
            if f.endswith(".SUB"):
                std_subs.add(f[:-4]) # Remove .SUB

    ax_subs = set()
    if os.path.exists(AX_EX_DIR):
        for f in os.listdir(AX_EX_DIR):
            if f.endswith(".SUB"):
                name = f[:-4]
                # Normalize name: Uebung_XXX_AX -> Uebung_XXX
                if name.endswith("_AX"):
                    norm_name = name[:-3]
                    ax_subs.add(norm_name)
                else:
                    ax_subs.add(name)

    missing = sorted(list(std_subs - ax_subs))
    print(f"Missing AX Exercises: {len(missing)}")
    for m in missing:
        print(f"- {m}")

if __name__ == "__main__":
    main()

