"""Find FB instances whose Name suggests the wrong plain-vs-adapter variant of its Type.

Across the logiBUS/isobus type library, many FB families ship two sibling
blocks: a plain service-interface FB and an "...A" composite/adapter FB
built on top of it, e.g. Softkey_IX / Softkey_IXA, logiBUS_QX / logiBUS_QXA,
Button_IX / Button_IXA, NumericValue_PHYS / NumericValue_PHYSA, etc.
(discovered dynamically below - see find_plain_to_adapter_pairs()).

Copy/pasting a SubApp network (e.g. deriving one wrapper SUB from another)
can leave a leftover instance Name from the wrong variant, e.g.:

    <FB Name="Button_IXA" Type="isobus::UT::io::Button::Button_IX" .../>
    <FB Name="logiBUS_QXA" Type="logiBUS::io::DQ::logiBUS_QX" .../>

The Type (not the Name) drives actual behavior, so these still compile -
but the Name is misleading and signals a copy/paste mistake.

This script scans all .SUB/.fbt files for `<FB Name="..." Type="...">` tags
where the instance Name matches the *other* variant's base type name.
"""

import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# glob's "**" does not descend into dot-directories (like ".lib", where most
# of the type library actually lives), so walk the tree manually instead.
SCAN_EXTENSIONS = {".fbt", ".sub"}  # matched case-insensitively
SKIP_DIR_NAMES = {".git"}


FBTYPE_NAME_PATTERN = re.compile(r'<FBType\s+Name="([^"]+)"')
FB_TAG_PATTERN = re.compile(r"<FB\b[^>]*>")
ATTR_PATTERN = re.compile(r'(\w+)="([^"]*)"')


def name_indicates(instance_name, candidate_type_name):
    """True if instance_name is exactly candidate_type_name, or candidate_type_name
    followed by a '_<disambiguator>' suffix (e.g. 'Softkey_IXA_1')."""
    return instance_name == candidate_type_name or instance_name.startswith(candidate_type_name + "_")


def find_all_files():
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in SCAN_EXTENSIONS:
                yield os.path.join(dirpath, filename)


def find_plain_to_adapter_pairs():
    """Scan all .fbt FBType definitions and return {plain_name: adapter_name}
    for every pair where both '<Name>' and '<Name>A' exist as FB types."""
    type_names = set()
    for path in find_all_files():
        if not path.lower().endswith(".fbt"):
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        match = FBTYPE_NAME_PATTERN.search(content)
        if match:
            type_names.add(match.group(1))

    pairs = {}
    for name in type_names:
        adapter_name = name + "A"
        if adapter_name in type_names:
            pairs[name] = adapter_name
    return pairs


def instance_base_name(name):
    """Best-effort strip of a trailing disambiguator ('_1', '_S1', ...) from
    an FB instance name, to compare against a base type name."""
    match = INSTANCE_NAME_PATTERN.match(name)
    return match.group(1) if match else name


def check_file(path, plain_to_adapter, adapter_to_plain):
    issues = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, start=1):
            for tag_match in FB_TAG_PATTERN.finditer(line):
                tag = tag_match.group(0)
                attrs = dict(ATTR_PATTERN.findall(tag))
                name = attrs.get("Name")
                type_ = attrs.get("Type")
                if not name or not type_:
                    continue

                type_base = type_.rsplit("::", 1)[-1]
                name_base = instance_base_name(name)

                expected_other = None
                if type_base in plain_to_adapter and name_base == plain_to_adapter[type_base]:
                    expected_other = f"plain variant '{type_base}'"
                elif type_base in adapter_to_plain and name_base == adapter_to_plain[type_base]:
                    expected_other = f"adapter variant '{type_base}'"

                if expected_other:
                    issues.append((lineno, name, type_, expected_other))
    return issues


def main():
    plain_to_adapter = find_plain_to_adapter_pairs()
    adapter_to_plain = {v: k for k, v in plain_to_adapter.items()}

    print(f"Found {len(plain_to_adapter)} plain/adapter FB type pairs in the type library.")
    print()

    total_issues = 0
    files_checked = 0
    for path in sorted(find_all_files()):
        files_checked += 1
        issues = check_file(path, plain_to_adapter, adapter_to_plain)
        if not issues:
            continue
        rel = os.path.relpath(path, REPO_ROOT)
        for lineno, name, type_, expected_other in issues:
            total_issues += 1
            print(f"{rel}:{lineno}")
            print(f"    FB Name=\"{name}\" looks like the {expected_other}, but Type=\"{type_}\"")

    print()
    print(f"Checked {files_checked} files, found {total_issues} plain/adapter name-vs-type mismatch(es).")


if __name__ == "__main__":
    main()
