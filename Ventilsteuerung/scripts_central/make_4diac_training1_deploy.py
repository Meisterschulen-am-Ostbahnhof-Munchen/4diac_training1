#!/usr/bin/env python3
"""Verteilt die aktuellen 4diac_training1-Boot-Dateien per HTTP auf die
Trainings-Knoten (file_server-Baustein aus LOGIBUS_integration_datapanel/
Application/components/file_server, POST /upload/<datei> mit rohem
Binaerinhalt nach /data/<datei>) - gleicher Mechanismus wie bei Krauternter
(Ventilsteuerung/make_krauternter_deploy.sh), ANNAHME: die Trainings-Station
laeuft auf derselben Firmware (LOGIBUS_integration_datapanel).

Python-Portierung von make_4diac_training1_deploy.sh, reine Stdlib
(http.client) - keine externe Abhaengigkeit (kein requests), damit
`python make_4diac_training1_deploy.py` ohne pip-Installation laeuft und
kein Git Bash mehr noetig ist.

Laedt nur hoch, rebootet NICHT automatisch - FORTE liest *.fboot nur beim
Booten neu ein, ein Neustart des Knotens muss also manuell ausgeloest werden
(z.B. ueber den "Reboot"-Button auf der Knoten-Weboberflaeche http://<ip>/).

Baut selbst nichts - Boot-Files (4diac-IDE-Export) muessen vorher aktuell
exportiert sein.
"""

from __future__ import annotations

import http.client
import re
import sys
import tempfile
from pathlib import Path
from typing import Optional

from deploy_common import NODE_BASES, NODE_ORDER, REPO_PATHS, resolve_local_path
from elf_libs_manifest_lib import NODE_ARCH, build_libs_manifest, resolve_required_libs

# Generell eingeschaltet - siehe elf_libs_manifest_lib.py/.sh fuer das
# Firmware-Verhalten bei fehlendem/ungueltigem Manifest (existiert eine
# *.libs.json und ist sie nicht ladbar, startet FORTE NICHT, Netzwerk/
# Dateiserver bleiben aktiv).
ENABLE_ELF_LIBS = True

_FBOOT_HREF_RE = re.compile(r'href="/([^"]*\.fboot)"')
_ELF_OR_MANIFEST_HREF_RE = re.compile(r'href="/([^"]*\.(?:elf|libs\.json))"')


def _http(ip: str, method: str, path: str, timeout: float, body: Optional[bytes] = None) -> tuple[int, bytes]:
    conn = http.client.HTTPConnection(ip, timeout=timeout)
    try:
        conn.request(method, path, body=body)
        resp = conn.getresponse()
        return resp.status, resp.read()
    finally:
        conn.close()


def http_warmup(ip: str) -> None:
    """Manche Knoten-Webserver antworten auf den allerersten Request nach dem
    Booten nicht zuverlaessig - ein Aufwaerm-Request VOR der eigentlichen
    Erreichbarkeitspruefung behebt das. Ergebnis wird bewusst ignoriert."""
    try:
        _http(ip, "GET", "/", 5)
    except OSError:
        pass


def http_reachable(ip: str) -> bool:
    """Wie curl -m 5 -o /dev/null ...: jede empfangene HTTP-Antwort (auch
    4xx/5xx) zaehlt als erreichbar, nur ein Verbindungsfehler/Timeout als
    nicht erreichbar."""
    try:
        _http(ip, "GET", "/application/", 5)
        return True
    except OSError:
        return False


def http_listing(ip: str, timeout: float = 5) -> str:
    """GET "/" als Text fuer die href-Listing-Regexe, leer bei
    Verbindungsfehler (wie curl -s: leere stdout statt Absturz)."""
    try:
        _status, data = _http(ip, "GET", "/", timeout)
        return data.decode("utf-8", errors="replace")
    except OSError:
        return ""


def http_delete(ip: str, name: str, timeout: float = 10) -> None:
    """POST /delete/<name>, Ergebnis bewusst ignoriert (best effort, wie im
    Original mit -o /dev/null)."""
    try:
        _http(ip, "POST", f"/delete/{name}", timeout)
    except OSError:
        pass


def http_upload_file(ip: str, local_path: Path, remote_name: str, timeout: float) -> str:
    """POST /upload/<remote_name> mit dem rohen Binaerinhalt von local_path,
    OHNE Redirects zu folgen (http.client folgt nie automatisch, wie curl
    ohne -L). Gibt den HTTP-Status als String zurueck ("303" = Erfolg, der
    Upload-Handler antwortet damit statt mit "200"), "000" bei jedem Fehler
    (Datei nicht lesbar, Verbindungsfehler, Timeout - wie curl ... || echo
    "000" im Original)."""
    try:
        data = local_path.read_bytes()
        status, _body = _http(ip, "POST", f"/upload/{remote_name}", timeout, body=data)
        return str(status)
    except OSError:
        return "000"


def main() -> int:
    missing = False
    for ip in NODE_ORDER:
        for base in NODE_BASES.get(ip, []):
            if resolve_local_path(base) is None:
                print(f"FEHLER: Deploy-Datei fehlt: {base} (weder gestempelt noch unter {REPO_PATHS.get(base)})")
                missing = True
    if missing:
        print("Abbruch: Fehlende Dateien zuerst neu bauen/exportieren (4diac-IDE-Export).")
        return 1

    reboot_needed: list[str] = []
    unreachable: list[str] = []
    upload_failed: list[str] = []

    for ip in NODE_ORDER:
        print("-" * 78)
        print(f"Knoten {ip}")

        http_warmup(ip)

        if not http_reachable(ip):
            print(f"WARNUNG: {ip} nicht erreichbar - uebersprungen.")
            unreachable.append(ip)
            continue

        node_ok = True
        node_local_files: list[Path] = []
        node_fboot_file: Optional[Path] = None

        for base in NODE_BASES.get(ip, []):
            local_file = resolve_local_path(base)
            assert local_file is not None  # durch die MISSING-Pruefung oben ausgeschlossen
            node_local_files.append(local_file)
            if base.endswith(".fboot"):
                node_fboot_file = local_file

            remote_name = local_file.name

            # Bei .fboot-Dateien anders benannte alte Bootfiles vorher
            # entfernen, sonst entscheidet FORTE beim Booten per
            # alphabetischer Sortierung ueber mehrere *.fboot-Kandidaten.
            if remote_name.endswith(".fboot"):
                for existing in _FBOOT_HREF_RE.findall(http_listing(ip)):
                    if existing != remote_name:
                        print(f"  Entferne alten Bootfile-Kandidaten: {existing}")
                        http_delete(ip, existing)

            print(f"  Lade {local_file} -> http://{ip}/upload/{remote_name}")
            http_code = http_upload_file(ip, local_file, remote_name, 30)
            if http_code == "303":
                print(f"  OK (HTTP {http_code})")
            else:
                print(f"  WARNUNG: Upload fehlgeschlagen (HTTP {http_code})")
                node_ok = False

        # ENTWURF/EXPERIMENTAL (Standard AN): ELFs + Libs-Manifest zusaetzlich
        # zum fboot hochladen. Fehlt lokal auch nur ein benoetigtes ELF, wird
        # dieser Teil fuer den Knoten uebersprungen - der normale fboot-
        # Upload oben ist davon unberuehrt.
        if node_ok and ENABLE_ELF_LIBS and node_fboot_file is not None:
            arch = NODE_ARCH.get(ip)
            if not arch:
                print(f"  WARNUNG: Keine Architektur fuer {ip} in NODE_ARCH hinterlegt - ELF-Manifest uebersprungen.")
            else:
                required_libs = resolve_required_libs(node_fboot_file)
                if not required_libs:
                    print("  Keine bekannten ausgelagerten Libs in diesem .fboot referenziert - kein Libs-Manifest noetig.")
                else:
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        manifest_tmp = Path(tmp_dir) / "manifest.json"
                        result = build_libs_manifest(arch, node_local_files, manifest_tmp, required_libs)
                        if result.ok:
                            manifest_name = f"{node_fboot_file.stem}.libs.json"

                            keep_names = {p.name for p in result.elf_paths}
                            for existing in _ELF_OR_MANIFEST_HREF_RE.findall(http_listing(ip)):
                                if existing != manifest_name and existing not in keep_names:
                                    print(f"  Entferne alten Lib-Kandidaten: {existing}")
                                    http_delete(ip, existing)

                            elf_ok = True
                            for elf_path in result.elf_paths:
                                elf_name = elf_path.name
                                print(f"  Lade {elf_path} -> http://{ip}/upload/{elf_name}")
                                http_code = http_upload_file(ip, elf_path, elf_name, 60)
                                if http_code == "303":
                                    print(f"  OK (HTTP {http_code})")
                                else:
                                    print(f"  WARNUNG: ELF-Upload fehlgeschlagen (HTTP {http_code})")
                                    elf_ok = False

                            # Manifest bewusst ZULETZT hochladen: fehlt es,
                            # laedt die Firmware keine Lib - ein
                            # abgebrochener Upload ist so erkennbar.
                            if elf_ok:
                                print(f"  Lade {manifest_tmp} -> http://{ip}/upload/{manifest_name}")
                                http_code = http_upload_file(ip, manifest_tmp, manifest_name, 30)
                                if http_code == "303":
                                    print(f"  OK (HTTP {http_code})")
                                else:
                                    print(
                                        f"  WARNUNG: Manifest-Upload fehlgeschlagen (HTTP {http_code}) - "
                                        "Libs auf dem Knoten sind damit unvollstaendig/inkonsistent.",
                                    )
                                    node_ok = False
                            else:
                                print("  WARNUNG: Mindestens ein ELF-Upload fehlgeschlagen - Manifest wird bewusst NICHT hochgeladen.")
                                node_ok = False

        if node_ok:
            reboot_needed.append(ip)
        else:
            upload_failed.append(ip)

    print("-" * 78)
    print(f"ZUSAMMENFASSUNG ({len(reboot_needed)}/{len(NODE_ORDER)} Knoten erfolgreich):")
    if len(reboot_needed) == len(NODE_ORDER):
        print(f"  ALLE {len(NODE_ORDER)} KNOTEN ERFOLGREICH HOCHGELADEN:")
        for ip in reboot_needed:
            print(f"  - {ip}: OK")
    else:
        for ip in NODE_ORDER:
            if ip in reboot_needed:
                print(f"  - {ip}: OK")
            elif ip in upload_failed:
                print(f"  - {ip}: FEHLER (Upload fehlgeschlagen, siehe Warnungen oben)")
            elif ip in unreachable:
                print(f"  - {ip}: NICHT ERREICHBAR (uebersprungen)")

    if reboot_needed:
        print()
        print("Neue Dateien werden erst nach einem Neustart aktiv.")
        print('Manuell neu starten (z.B. "Reboot"-Button auf http://<ip>/):')
        for ip in reboot_needed:
            print(f"  - {ip}")

    return 0 if len(reboot_needed) == len(NODE_ORDER) else 1


if __name__ == "__main__":
    # Skript wird meist per Doppelklick gestartet (Windows-Konsolenfenster) -
    # ohne diese Pause schliesst sich das Fenster sofort und Warnungen/
    # Fehlermeldungen sind nie zu sehen. Greift bei JEDEM Ausstiegspunkt
    # (auch bei frueher Abbruch/Exception), analog zum Bash-"trap ... EXIT".
    exit_code = 1
    try:
        exit_code = main()
    finally:
        input("\nFertig - Enter druecken zum Schliessen...")
    sys.exit(exit_code)
