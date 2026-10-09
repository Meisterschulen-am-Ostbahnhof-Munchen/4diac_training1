#!/usr/bin/env bash
# Erzeugt <programm>.libs.json fuer jede Station, die ausgelagerte ELF-Libs
# (OSCAT/OSCAT_adapter) benoetigt, und legt sie direkt in boot-files/ ab.
#
# Reine lokale Dateierzeugung - KEIN Netzwerkzugriff, laeuft unabhaengig davon
# ob irgendeine Steuerung erreichbar ist. make_4diac_training1_deploy.sh ist
# das Upload-/Kopier-Skript (braucht erreichbare Knoten); dieses Skript hier
# ist nur fuer das Erzeugen der JSON-Datei zustaendig.
#
# Baut selbst keine ELFs - die liegen schon unter
# 4diacIDE-workspace/.lib/<Lib>/elf/<arch>/ (von make_elf_libs.sh im Repo
# LOGIBUS_integration_datapanel gebaut). Fehlt ein benoetigtes ELF lokal, wird
# fuer die betroffene Station einfach kein Manifest geschrieben (siehe
# build_libs_manifest() in elf_libs_manifest_lib.sh) - kein Fehlerabbruch.
set -uo pipefail

# Skript wird meist per Doppelklick gestartet (Windows/Git-Bash-Fenster) - ohne
# diese Pause schliesst sich das Fenster sofort und Warnungen/Fehlermeldungen
# sind nie zu sehen. Greift bei JEDEM Ausstiegspunkt (auch bei frueher Abbruch).
pause_on_exit() {
    echo ""
    read -r -p "Fertig - Enter druecken zum Schliessen..." _
}
trap pause_on_exit EXIT

cd "$(dirname "$0")"
source "deploy_common.sh"
source "elf_libs_manifest_lib.sh"

WRITTEN=()
SKIPPED=()

for ip in "${NODE_ORDER[@]}"; do
    fboot_base=""
    for base in ${NODE_BASES[$ip]}; do
        [[ "$base" == *.fboot ]] && fboot_base="$base"
    done
    [ -z "$fboot_base" ] && continue

    fboot_path="$(resolve_local_path "$fboot_base")"
    if [ -z "$fboot_path" ]; then
        echo "WARNUNG: ${fboot_base} (${ip}) nicht gefunden - uebersprungen."
        SKIPPED+=("$fboot_base")
        continue
    fi

    arch="${NODE_ARCH[$ip]:-}"
    if [ -z "$arch" ]; then
        echo "WARNUNG: Keine Architektur fuer ${ip} in NODE_ARCH hinterlegt - ${fboot_base} uebersprungen."
        SKIPPED+=("$fboot_base")
        continue
    fi

    mapfile -t required_libs < <(resolve_required_libs "$fboot_path")
    if [ "${#required_libs[@]}" -eq 0 ]; then
        echo "${fboot_base} (${ip}): keine bekannten ausgelagerten Libs referenziert - kein Manifest noetig."
        continue
    fi

    node_files=()
    for base in ${NODE_BASES[$ip]}; do
        f="$(resolve_local_path "$base")"
        [ -n "$f" ] && node_files+=("$f")
    done

    out_path="boot-files/$(basename "$fboot_path" .fboot).libs.json"
    echo "${fboot_base} (${ip}, ${arch}): benoetigt ${required_libs[*]}"
    if build_libs_manifest "$arch" node_files "$out_path" required_libs; then
        echo "  Geschrieben: ${out_path}"
        WRITTEN+=("$out_path")
    else
        SKIPPED+=("$fboot_base")
    fi
done

echo "----------------------------------------------------------------------------"
echo "ZUSAMMENFASSUNG: ${#WRITTEN[@]} Manifest(e) geschrieben, ${#SKIPPED[@]} uebersprungen."
for p in "${WRITTEN[@]}"; do
    echo "  OK: ${p}"
done
for b in "${SKIPPED[@]}"; do
    echo "  UEBERSPRUNGEN: ${b} (siehe Warnung/Hinweis oben)"
done
