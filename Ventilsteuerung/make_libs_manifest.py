#!/usr/bin/env python3
"""Python-Portierung von make_libs_manifest.sh, als PARALLELE Implementierung
zum Bash-Original zum Vergleich (Franz: Ergebnisse abwechselnd laufen lassen
und auf Gleichheit pruefen). Erzeugt <programm>.libs.json rein lokal, kein
Netzwerkzugriff.

Schreibt standardmaessig NICHT nach boot-files/test_AX_FORTE_PC_AX.libs.json
(das wuerde die von der Bash-Version erzeugte Datei ueberschreiben), sondern
nach boot-files/test_AX_FORTE_PC_AX.libs.python.json - mit --out <Pfad>
konfigurierbar.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from elf_libs_manifest_lib import NODE_ARCH, build_libs_manifest, resolve_required_libs

VENTILSTEUERUNG_DIR = Path(__file__).resolve().parent

# 1:1 aus deploy_common.sh uebernommen (nur die Daten, nicht das Bash-
# resolve_local_path()-Stempel-Verhalten - fuer den Side-by-Side-Vergleich
# reicht der einfache Repo-Pfad, da im Testbetrieb keine gestempelten
# Varianten im Wurzelverzeichnis liegen).
NODE_BASES = {
    "192.168.178.55": ["test_AX_FORTE_PC_AX.fboot"],
    # "<B-IP-noch-unbekannt>": ["test_B_FORTE_PC_B.fboot"],
}
REPO_PATHS = {
    "test_AX_FORTE_PC_AX.fboot": "boot-files/test_AX_FORTE_PC_AX.fboot",
    "test_B_FORTE_PC_B.fboot": "boot-files/test_B_FORTE_PC_B.fboot",
}
NODE_ORDER = ["192.168.178.55"]


def resolve_local_path(base: str) -> Path | None:
    """Analog zu resolve_local_path() in deploy_common.sh: zuerst gestempelte
    Variante im Ventilsteuerung-Wurzelverzeichnis, dann unbestempelte
    Variante dort, dann Repo-Fallback-Pfad."""
    name, _, ext = base.rpartition(".")
    stamped = sorted(VENTILSTEUERUNG_DIR.glob(f"{name}_*.{ext}"))
    if stamped:
        return stamped[0]
    plain = VENTILSTEUERUNG_DIR / base
    if plain.is_file():
        return plain
    repo = VENTILSTEUERUNG_DIR / REPO_PATHS.get(base, "")
    if REPO_PATHS.get(base) and repo.is_file():
        return repo
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default=None,
        help=(
            "Zielpfad fuer das Manifest (Default: boot-files/<fboot-name>.libs.python.json, "
            "um die von der Bash-Version erzeugte Datei nicht zu ueberschreiben)."
        ),
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
            out_path = VENTILSTEUERUNG_DIR / "boot-files" / f"{fboot_path.stem}.libs.python.json"

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
