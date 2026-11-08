"""Check for ISO-VT object names that are re-used across different Workspace_* projects.

Each ISO-Designer project (ISO-DesignerProjects/Workspace*) generates a
DefaultPool.iop.h with one `#define <ObjectName> <ID>` per object in the pool
(Buttons, DataMasks, InputNumbers, SoftKeys, ...). Since all these projects feed
into the same 4diac workspace (see scripts_central/GcfScript.py), an object name
that is reused in two different projects causes a name collision once both are
imported as global constants.

WorkingSet / WorkingSet_0 and the generic ISO-Designer header constants
(ISO_DESIGNATOR_WIDTH, MASK_WIDTH, ...) are expected to exist identically in
every project and are not real object names, so they are ignored here.
"""

import glob
import os
import re
from collections import defaultdict

ISO_PROJECTS_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "ISO-DesignerProjects",
)

IOP_H_GLOB = os.path.join(ISO_PROJECTS_ROOT, "Workspace*", "DefaultPool", "Output", "DefaultPool.iop.h")

IGNORED_NAMES = {
    "WorkingSet",
    "WorkingSet_0",
    "ISO_DESIGNATOR_WIDTH",
    "ISO_DESIGNATOR_HEIGHT",
    "ISO_MASK_SIZE",
    "ISO_VERSION_LABEL",
    "MASK_WIDTH",
    "MASK_HEIGHT",
}

DEFINE_PATTERN = re.compile(r"#define\s+(\w+)\s+(\S+)")


def project_name(iop_h_path):
    # .../ISO-DesignerProjects/<Project>/DefaultPool/Output/DefaultPool.iop.h
    return os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(iop_h_path))))


def read_definitions(iop_h_path):
    definitions = {}
    with open(iop_h_path, "r") as f:
        for line in f:
            match = DEFINE_PATTERN.match(line)
            if match:
                name, value = match.groups()
                definitions[name] = value
    return definitions


def main():
    iop_h_files = sorted(glob.glob(IOP_H_GLOB))
    if not iop_h_files:
        print(f"No DefaultPool.iop.h files found under {ISO_PROJECTS_ROOT}")
        return

    # name -> list of (project, value)
    occurrences = defaultdict(list)

    for iop_h_path in iop_h_files:
        project = project_name(iop_h_path)
        definitions = read_definitions(iop_h_path)
        for name, value in definitions.items():
            if name in IGNORED_NAMES:
                continue
            occurrences[name].append((project, value))

    duplicates = {
        name: projects
        for name, projects in occurrences.items()
        if len({p for p, _ in projects}) > 1
    }

    print(f"Scanned {len(iop_h_files)} projects:")
    for path in iop_h_files:
        print(f"  - {project_name(path)}")
    print()

    if not duplicates:
        print("No duplicate object names found across projects.")
        return

    print(f"Found {len(duplicates)} object name(s) used in more than one project:\n")
    for name in sorted(duplicates):
        projects = duplicates[name]
        print(f"  {name}")
        for project, value in projects:
            print(f"      {project:<20} = {value}")


if __name__ == "__main__":
    main()
