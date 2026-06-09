import os
import re

LIB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "Ventilsteuerung", "4diacIDE-workspace", ".lib")

EXTENSIONS = (".fbt", ".adp", ".fct", ".dtp", ".gcf")

IMPORT_TEXT = '<Import declaration="eclipse4diac::core::TypeHash"/>'
ATTR_TEXT = '<Attribute Name="eclipse4diac::core::TypeHash" Value="\'\'"/>'

IMPORT_PATTERN = re.compile(IMPORT_TEXT)
ATTR_PATTERN = re.compile(ATTR_TEXT)

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    modified = False

    # --- Ensure exactly one Attribute line, properly placed before closing tag ---
    attr_indices = [i for i, line in enumerate(lines) if ATTR_PATTERN.search(line)]

    if len(attr_indices) > 1:
        # Remove all but keep the best-positioned one later
        for i in reversed(attr_indices):
            if i != attr_indices[-1]:
                del lines[i]
        modified = True

    # Check if attribute exists (after potential dedup)
    has_attr = any(ATTR_PATTERN.search(line) for line in lines)
    if not has_attr:
        # Insert before closing root tag
        for i in range(len(lines) - 1, -1, -1):
            stripped = lines[i].strip()
            if stripped.startswith("</"):
                lines.insert(i, "\t" + ATTR_TEXT + "\n")
                modified = True
                break
    else:
        # Ensure remaining attribute is properly indented with tab
        for i, line in enumerate(lines):
            if ATTR_PATTERN.search(line):
                current_indent = line[:len(line) - len(line.lstrip())]
                if current_indent != "\t":
                    lines[i] = "\t" + line.lstrip()
                    modified = True
                break

    # --- Ensure Import exists in CompilerInfo ---
    has_import = any(IMPORT_PATTERN.search(line) for line in lines)

    if not has_import:
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("<CompilerInfo"):
                if ">" in line:
                    lines.insert(i + 1, "\t\t" + IMPORT_TEXT + "\n")
                    modified = True
                    break
                else:
                    for j in range(i, min(i + 10, len(lines))):
                        if ">" in lines[j]:
                            lines.insert(j + 1, "\t\t" + IMPORT_TEXT + "\n")
                            modified = True
                            break
                    break

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return True
    return False

def main():
    total = 0
    modified_files = []
    for root, dirs, files in os.walk(LIB_DIR):
        for f in files:
            if f.endswith(EXTENSIONS):
                total += 1
                filepath = os.path.join(root, f)
                if process_file(filepath):
                    modified_files.append(filepath)

    print(f"Total files scanned: {total}")
    print(f"Files modified: {len(modified_files)}")
    for mf in modified_files:
        rel = os.path.relpath(mf, LIB_DIR)
        print(f"  Modified: {rel}")

if __name__ == "__main__":
    main()
