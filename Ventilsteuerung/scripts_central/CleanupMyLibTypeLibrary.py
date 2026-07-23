"""Clean up a project-local Type Library/MyLib folder: keep everything that is
actually used anywhere in that project, and for anything unused, keep only
the types that match the project's naming convention.

Rule (as specified by the project owner):
  - test_AX/Type Library/MyLib: keep types that are used anywhere in test_AX.
    For unused types, keep only those whose name contains "AX"; delete the rest.
  - test_B/Type Library/MyLib: keep types that are used anywhere in test_B.
    For unused types, keep only those whose name does NOT contain "AX"; delete the rest.

"Used" means: the type's fully qualified name (packageName + "::" + Name, taken
from its own <SubAppType>/<FBType> + <CompilerInfo packageName="..."> tags) shows
up anywhere else in the project tree (as a Type="..." reference or an
Import declaration="..."), INCLUDING references from other MyLib types (e.g. a
compact "...C" wrapper that nests another MyLib SubApp).

That last point matters: usage is computed as a fixed point. A MyLib type that
is only referenced by another MyLib type which is itself unused-and-slated-for-
deletion does NOT count as "used" - once the referencer is removed, the
referenced type is re-evaluated on its own (naming convention only). Without
this, a chain like "AXSC wraps AXS" would keep AXS alive purely because AXSC
(which is about to be deleted) mentions it once.

Run with --apply to actually delete; without it, this only prints a report
(dry run, the default, so it's safe to re-run any time).
"""

import argparse
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENTILSTEUERUNG_DIR = os.path.dirname(SCRIPT_DIR)
WORKSPACE_DIR = os.path.join(VENTILSTEUERUNG_DIR, "4diacIDE-workspace")

# (project folder name, token that must appear in an *unused* type's name for it to survive)
PROJECTS = [
    ("test_AX", "AX"),
    ("test_B", None),  # None => must NOT contain "AX"
]

TYPE_NAME_PATTERN = re.compile(r'<(?:SubAppType|FBType)\s+[^>]*\bName="([^"]+)"')
PACKAGE_PATTERN = re.compile(r'<CompilerInfo\s+packageName="([^"]+)"')

BINARY_EXTS = {
    ".zip", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".ttf", ".otf",
    ".exe", ".dll", ".so", ".a", ".obj", ".pdf", ".doc", ".docx", ".xls",
    ".xlsx", ".jar", ".class",
}


def find_types(mylib_root):
    """Return {filepath: (qualified_name, bare_name, content)} for every .SUB
    file under mylib_root that declares a SubAppType/FBType."""
    results = {}
    for dirpath, dirnames, filenames in os.walk(mylib_root):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() != ".sub":
                continue
            path = os.path.join(dirpath, filename)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except OSError:
                continue
            name_m = TYPE_NAME_PATTERN.search(content)
            if not name_m:
                print(f"  [SKIP - unrecognized format] {path}")
                continue
            pkg_m = PACKAGE_PATTERN.search(content)
            if pkg_m:
                package = pkg_m.group(1)
            else:
                # No explicit packageName (e.g. <CompilerInfo></CompilerInfo>) -
                # 4diac falls back to the package implied by the folder structure.
                rel_dir = os.path.relpath(dirpath, mylib_root)
                parts = [] if rel_dir == "." else rel_dir.split(os.sep)
                package = "::".join(["MyLib"] + parts)
            qualified = f"{package}::{name_m.group(1)}"
            results[path] = (qualified, name_m.group(1), content)
    return results


def build_outside_corpus(project_root, mylib_root):
    """Concatenate all non-binary file contents under project_root that are
    NOT inside mylib_root, for fast substring/regex membership checks."""
    mylib_root_norm = os.path.normcase(os.path.abspath(mylib_root))
    chunks = []
    for dirpath, dirnames, filenames in os.walk(project_root):
        if os.path.normcase(os.path.abspath(dirpath)).startswith(mylib_root_norm):
            continue
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in BINARY_EXTS:
                continue
            path = os.path.join(dirpath, filename)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    chunks.append(f.read())
            except OSError:
                continue
    return "\n".join(chunks)


def resolve(types, outside_corpus, must_contain):
    """Fixed-point resolution: returns (keep_used, keep_naming, delete), each a
    list of (path, qualified) resp. (path, qualified, occurrences)."""
    alive = dict(types)  # path -> (qualified, bare_name, content)
    removed = []

    while True:
        alive_mylib_corpus = "\n".join(content for _qual, _bare, content in alive.values())
        full_corpus = outside_corpus + "\n" + alive_mylib_corpus

        round_used = {}
        round_naming_keep = []
        round_remove = []

        for path, (qualified, bare_name, content) in alive.items():
            pattern = re.compile(re.escape(qualified) + r'(?![A-Za-z0-9_])')
            occurrences = len(pattern.findall(full_corpus))
            if occurrences > 0:
                round_used[path] = (qualified, occurrences)
                continue

            has_ax = "AX" in bare_name
            survives_naming = has_ax if must_contain else not has_ax
            if survives_naming:
                round_naming_keep.append((path, qualified))
            else:
                round_remove.append(path)

        if not round_remove:
            keep_used = [(path, qual, occ) for path, (qual, occ) in round_used.items()]
            return keep_used, round_naming_keep, removed

        for path in round_remove:
            removed.append((path, alive[path][0]))
            del alive[path]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Actually delete files (default: dry run / report only)")
    args = parser.parse_args()

    for project, must_contain in PROJECTS:
        project_root = os.path.join(WORKSPACE_DIR, project)
        mylib_root = os.path.join(project_root, "Type Library", "MyLib")

        print("=" * 70)
        print(f"Project: {project}  (unused types must {'contain' if must_contain else 'NOT contain'} 'AX' to survive)")
        print("=" * 70)

        types = find_types(mylib_root)
        print(f"Found {len(types)} types under {mylib_root}")

        print("Building searchable corpus of the rest of the project (this can take a moment)...")
        outside_corpus = build_outside_corpus(project_root, mylib_root)

        keep_used, keep_naming, delete = resolve(types, outside_corpus, must_contain)

        print()
        print(f"KEEP (used elsewhere in {project}, incl. by other surviving MyLib types): {len(keep_used)}")
        for path, qualified, occurrences in sorted(keep_used):
            print(f"    {os.path.relpath(path, VENTILSTEUERUNG_DIR)}  ({occurrences}x '{qualified}')")

        print()
        print(f"KEEP (unused, but matches naming convention): {len(keep_naming)}")
        for path, qualified in sorted(keep_naming):
            print(f"    {os.path.relpath(path, VENTILSTEUERUNG_DIR)}")

        print()
        print(f"DELETE (unused, wrong naming convention for {project}): {len(delete)}")
        for path, qualified in sorted(delete):
            print(f"    {os.path.relpath(path, VENTILSTEUERUNG_DIR)}")

        if args.apply:
            for path, qualified in delete:
                os.remove(path)
            print()
            print(f"Deleted {len(delete)} file(s).")
        print()


if __name__ == "__main__":
    main()
