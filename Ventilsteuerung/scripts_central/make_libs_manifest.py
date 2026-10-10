#!/usr/bin/env python3
"""Erzeugt <programm>.libs.json rein lokal, kein Netzwerkzugriff -
make_4diac_training1_deploy.py ist das Upload-Skript (braucht erreichbare
Knoten). Ersetzt das fruehere make_libs_manifest.sh (Bash-Original entfernt,
siehe Git-Historie Branch feature/elf-loader).

Schreibt standardmaessig nach boot-files/<fboot-name>.libs.json - mit --out
<Pfad> konfigurierbar (z.B. fuer einen Testlauf ohne die echte Datei zu
ueberschreiben).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from deploy_common import NODE_BASES, NODE_ORDER, VENTILSTEUERUNG_DIR, resolve_local_path
from elf_libs_manifest_lib import NODE_ARCH, build_libs_manifest, resolve_required_libs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default=None,
        help="Zielpfad fuer das Manifest (Default: boot-files/<fboot-name>.libs.json).",
    )
    args = parser.parse_args()

    written: list[str] = []
    skipped: list[str] = []

    for ip in NODE_ORDER:
        fboot_base = next((b for b in NODE_BASES.get(ip, []) if b.endswith(".fboot")), None)
        if fboot_base is None:
            continue

        fboot_path = resolve_local_path(fboot_base)
        if fboot_path is None:
            print(f"WARNUNG: {fboot_base} ({ip}) nicht gefunden - uebersprungen.")
            skipped.append(fboot_base)
            continue

        arch = NODE_ARCH.get(ip)
        if not arch:
            print(f"WARNUNG: Keine Architektur fuer {ip} in NODE_ARCH hinterlegt - {fboot_base} uebersprungen.")
            skipped.append(fboot_base)
            continue

        required_libs = resolve_required_libs(fboot_path)
        if not required_libs:
            print(f"{fboot_base} ({ip}): keine bekannten ausgelagerten Libs referenziert - kein Manifest noetig.")
            continue

        node_files = [p for base in NODE_BASES.get(ip, []) if (p := resolve_local_path(base)) is not None]

        if args.out:
            out_path = Path(args.out)
        else:
            out_path = VENTILSTEUERUNG_DIR / "boot-files" / f"{fboot_path.stem}.libs.json"

        print(f"{fboot_base} ({ip}, {arch}): benoetigt {' '.join(required_libs)}")
        result = build_libs_manifest(arch, node_files, out_path, required_libs)
        if result.ok:
            print(f"  Geschrieben: {out_path.relative_to(VENTILSTEUERUNG_DIR)}")
            written.append(str(out_path))
        else:
            skipped.append(fboot_base)

    print("-" * 78)
    print(f"ZUSAMMENFASSUNG: {len(written)} Manifest(e) geschrieben, {len(skipped)} uebersprungen.")
    for p in written:
        print(f"  OK: {p}")
    for b in skipped:
        print(f"  UEBERSPRUNGEN: {b} (siehe Warnung/Hinweis oben)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
