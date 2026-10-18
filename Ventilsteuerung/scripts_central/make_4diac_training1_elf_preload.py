#!/usr/bin/env python3
"""Spielt die ELF-Grundausstattung (deploy_common.PRELOAD_LIBS + requires)
OHNE Bootfile und OHNE Manifest nach /data/elf-libs/ auf die Trainings-
Knoten. Danach laedt make_4diac_training1_deploy.py pro Uebung praktisch nur
noch Bootfile + Manifest hoch: bereits vorhandene ELFs werden per Hash
uebersprungen, und die Grundausstattung wird beim Aufraeumen nicht mehr
geloescht, auch wenn das aktuelle Manifest sie nicht auflistet.

Aufruf:
    python make_4diac_training1_elf_preload.py            (alle Knoten aus NODE_ORDER)
    python make_4diac_training1_elf_preload.py 192.168.178.55 192.168.178.56

Laedt nur hoch, loescht nichts (auch keine alten Versionen derselben Lib -
das aktive Manifest auf dem Knoten koennte sie noch referenzieren; das
Aufraeumen macht das naechste normale Deploy). Kein Neustart noetig: der
Loader nutzt die ELFs erst, wenn ein Manifest sie auflistet.
"""

from __future__ import annotations

import sys

from deploy_common import NODE_ORDER, preload_libs_with_requires
from elf_libs_manifest_lib import LIB_VERSIONS, NODE_ARCH, resolve_elf_path, sha256_of
from make_4diac_training1_deploy import (
    http_reachable,
    http_remote_sha256_listing,
    http_upload_file,
    http_warmup,
)

# Ohne bekannte Architektur (NODE_ARCH) fuer eine frei angegebene IP wird
# diese angenommen - das Board "Trainer" ist riscv32.
DEFAULT_ARCH = "riscv32"


def preload_node(ip: str, libs: list[str]) -> bool:
    arch = NODE_ARCH.get(ip, DEFAULT_ARCH)
    http_warmup(ip)
    if not http_reachable(ip):
        print(f"WARNUNG: {ip} nicht erreichbar - uebersprungen.")
        return False

    remote_hashes = http_remote_sha256_listing(ip)
    sha256_capable = remote_hashes is not None
    if remote_hashes is None:
        remote_hashes = {}

    ok = True
    for lib in libs:
        elf_path = resolve_elf_path(lib, LIB_VERSIONS[lib], arch)
        if elf_path is None:
            print(f"  WARNUNG: ELF fuer {lib}-{LIB_VERSIONS[lib]}-{arch} nicht gefunden.")
            ok = False
            continue
        remote_path = f"elf-libs/{elf_path.name}"
        http_code = http_upload_file(
            ip, elf_path, remote_path, 60,
            sha256_of(elf_path), remote_hashes, sha256_capable,
        )
        if http_code == "SKIP":
            print(f"  {remote_path}: unveraendert (Hash stimmt), uebersprungen")
        elif http_code == "303":
            print(f"  {remote_path}: OK (HTTP 303)")
        elif http_code == "RECOVERED":
            print(f"  {remote_path}: OK (Antwort verloren, Datei laut Hash aber vollstaendig angekommen)")
        elif http_code == "VERIFY_FAILED":
            print(f"  FEHLER: {remote_path}: mit HTTP 303 quittiert, Datei laut Geraet aber nicht/falsch gespeichert!")
            ok = False
        else:
            print(f"  WARNUNG: {remote_path}: Upload fehlgeschlagen (HTTP {http_code})")
            ok = False
    return ok


def main(argv: list[str]) -> int:
    ips = argv or NODE_ORDER
    libs = preload_libs_with_requires()
    print(f"Grundausstattung ({len(libs)} Libs): {' '.join(libs)}")

    failed: list[str] = []
    for ip in ips:
        print("-" * 78)
        print(f"Knoten {ip}")
        if not preload_node(ip, libs):
            failed.append(ip)

    print("-" * 78)
    print(f"ZUSAMMENFASSUNG ({len(ips) - len(failed)}/{len(ips)} Knoten erfolgreich):")
    for ip in ips:
        print(f"  - {ip}: {'FEHLER (siehe oben)' if ip in failed else 'OK'}")
    if failed:
        print("Fehlgeschlagene Knoten einfach erneut aufrufen - vorhandene ELFs werden per Hash uebersprungen.")
    print("Kein Neustart noetig: die ELFs werden erst mit dem naechsten Deploy (Manifest) genutzt.")
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, ValueError):
        pass
    sys.exit(main(sys.argv[1:]))
