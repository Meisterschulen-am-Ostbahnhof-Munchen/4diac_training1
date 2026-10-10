#!/usr/bin/env python3
"""Gemeinsame Konfiguration/Hilfsfunktion zum Finden der lokalen
4diac_training1-Deploy-Dateien (fboot) - genutzt von
make_4diac_training1_deploy.py (Upload) UND make_libs_manifest.py (lokale
Manifest-Erzeugung, kein Upload). Python-Portierung von deploy_common.sh.

IP-Zuordnung: NUR AX ist aktuell bekannt (192.168.178.55, von Franz genannt
2026-10-09). B-Station-IP ist noch nicht bekannt - sobald Franz sie nennt,
hier ergaenzen.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

VENTILSTEUERUNG_DIR = Path(__file__).resolve().parent.parent

NODE_BASES: dict[str, list[str]] = {
    "192.168.178.55": ["test_AX_FORTE_PC_AX.fboot"],
    # "<B-IP-noch-unbekannt>": ["test_B_FORTE_PC_B.fboot"],
}

REPO_PATHS: dict[str, str] = {
    "test_AX_FORTE_PC_AX.fboot": "boot-files/test_AX_FORTE_PC_AX.fboot",
    "test_B_FORTE_PC_B.fboot": "boot-files/test_B_FORTE_PC_B.fboot",
}

NODE_ORDER: list[str] = ["192.168.178.55"]


def resolve_local_path(base: str) -> Optional[Path]:
    """Liefert den tatsaechlichen lokalen Pfad zu einer Basisdatei: zuerst
    gestempelte Variante im Ventilsteuerung-Wurzelverzeichnis, dann
    unbestempelte Variante dort, dann Repo-Fallback-Pfad. None, wenn nichts
    gefunden (entspricht resolve_local_path() in deploy_common.sh)."""
    name, _, ext = base.rpartition(".")
    stamped = sorted(VENTILSTEUERUNG_DIR.glob(f"{name}_*.{ext}"))
    if stamped:
        return stamped[0]
    plain = VENTILSTEUERUNG_DIR / base
    if plain.is_file():
        return plain
    repo_rel = REPO_PATHS.get(base)
    if repo_rel:
        repo = VENTILSTEUERUNG_DIR / repo_rel
        if repo.is_file():
            return repo
    return None
