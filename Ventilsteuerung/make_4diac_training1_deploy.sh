#!/usr/bin/env bash
# Verteilt die aktuellen 4diac_training1-Boot-Dateien per HTTP auf die
# Trainings-Knoten (file_server-Baustein aus LOGIBUS_integration_datapanel/
# Application/components/file_server, POST /upload/<datei> mit rohem
# Binaerinhalt nach /data/<datei>) - gleicher Mechanismus wie bei Krauternter
# (Ventilsteuerung/make_krauternter_deploy.sh), ANNAHME: die Trainings-Station
# laeuft auf derselben Firmware (LOGIBUS_integration_datapanel), noch nicht
# live verifiziert.
#
# IP-Zuordnung: NUR AX ist bekannt (192.168.178.55, von Franz genannt
# 2026-10-09) - siehe deploy_common.sh. B-Station-IP fehlt noch.
#
# Laedt nur hoch, rebootet NICHT automatisch - FORTE liest *.fboot nur beim
# Booten neu ein, ein Neustart des Knotens muss also manuell ausgeloest werden
# (z.B. ueber den "Reboot"-Button auf der Knoten-Weboberflaeche http://<ip>/).
#
# Baut selbst nichts - Boot-Files (4diac-IDE-Export) muessen vorher aktuell
# exportiert sein.
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

# Von Franz 2026-10-09 bewusst eingeschaltet - Uebung_011f_ROUND_AR_AX braucht
# OSCAT_adapter/OSCAT als ELF auf dem Geraet, ohne Manifest startet FORTE
# diesen fboot nicht (siehe elf_libs_manifest_lib.sh fuer Firmware-Verhalten).
ENABLE_ELF_LIBS=1

MISSING=0
for ip in "${NODE_ORDER[@]}"; do
    for base in ${NODE_BASES[$ip]}; do
        if [ -z "$(resolve_local_path "$base")" ]; then
            echo "FEHLER: Deploy-Datei fehlt: ${base} (weder gestempelt noch unter ${REPO_PATHS[$base]})"
            MISSING=1
        fi
    done
done
if [ "$MISSING" = 1 ]; then
    echo "Abbruch: Fehlende Dateien zuerst neu bauen/exportieren (4diac-IDE-Export)."
    exit 1
fi

REBOOT_NEEDED=()
UNREACHABLE=()
UPLOAD_FAILED=()

for ip in "${NODE_ORDER[@]}"; do
    echo "----------------------------------------------------------------------------"
    echo "Knoten ${ip}"

    # Manche Knoten-Webserver antworten auf den allerersten Request nach dem
    # Booten nicht zuverlaessig - ein Aufwaerm-Request auf die Startseite VOR
    # der eigentlichen Erreichbarkeitspruefung behebt das (siehe Krauternter-
    # Deploy-Skript). Ergebnis wird bewusst ignoriert.
    curl -s -m 5 -o /dev/null "http://${ip}/" 2>/dev/null

    if ! curl -s -m 5 -o /dev/null "http://${ip}/application/"; then
        echo "WARNUNG: ${ip} nicht erreichbar - uebersprungen."
        UNREACHABLE+=("$ip")
        continue
    fi

    NODE_OK=1
    NODE_LOCAL_FILES=()
    NODE_FBOOT_FILE=""

    for base in ${NODE_BASES[$ip]}; do
        local_file="$(resolve_local_path "$base")"
        NODE_LOCAL_FILES+=("$local_file")
        if [[ "$base" == *.fboot ]]; then
            NODE_FBOOT_FILE="$local_file"
        fi

        remote_name="$(basename "$local_file")"

        # Bei .fboot-Dateien anders benannte alte Bootfiles vorher entfernen,
        # sonst entscheidet FORTE beim Booten per alphabetischer Sortierung
        # ueber mehrere *.fboot-Kandidaten im Verzeichnis.
        if [[ "$remote_name" == *.fboot ]]; then
            existing_fboots="$(curl -s -m 5 "http://${ip}/" | grep -oE 'href="/[^"]*\.fboot"' | sed -E 's/href="\/(.*)"/\1/')"
            for existing in $existing_fboots; do
                if [ "$existing" != "$remote_name" ]; then
                    echo "  Entferne alten Bootfile-Kandidaten: ${existing}"
                    curl -s -m 10 -X POST "http://${ip}/delete/${existing}" -o /dev/null
                fi
            done
        fi

        echo "  Lade ${local_file} -> http://${ip}/upload/${remote_name}"
        HTTP_CODE="$(curl -s -o /dev/null -w "%{http_code}" -m 30 \
            -X POST "http://${ip}/upload/${remote_name}" \
            --data-binary @"${local_file}" \
            || echo "000")"

        # Der Upload-Handler antwortet bei Erfolg mit "303 See Other" (Redirect
        # auf "/", fuer die Browser-Oberflaeche gedacht), nicht mit "200".
        if [ "$HTTP_CODE" = "303" ]; then
            echo "  OK (HTTP ${HTTP_CODE})"
        else
            echo "  WARNUNG: Upload fehlgeschlagen (HTTP ${HTTP_CODE})"
            NODE_OK=0
        fi
    done

    # ENTWURF/EXPERIMENTAL (Standard AUS): ELFs + Libs-Manifest zusaetzlich zum
    # fboot hochladen. Fehlt lokal auch nur ein benoetigtes ELF, wird dieser
    # Teil fuer den Knoten uebersprungen - der normale fboot-Upload oben ist
    # davon unberuehrt.
    if [ "$NODE_OK" = 1 ] && [ "$ENABLE_ELF_LIBS" = 1 ] && [ -n "$NODE_FBOOT_FILE" ]; then
        arch="${NODE_ARCH[$ip]:-}"
        if [ -z "$arch" ]; then
            echo "  WARNUNG: Keine Architektur fuer ${ip} in NODE_ARCH hinterlegt - ELF-Manifest uebersprungen."
        else
            mapfile -t required_libs < <(resolve_required_libs "$NODE_FBOOT_FILE")
            if [ "${#required_libs[@]}" -eq 0 ]; then
                echo "  Keine bekannten ausgelagerten Libs in diesem .fboot referenziert - kein Libs-Manifest noetig."
            else
                manifest_tmp="$(mktemp)"
                if build_libs_manifest "$arch" NODE_LOCAL_FILES "$manifest_tmp" required_libs; then
                    manifest_name="$(basename "$NODE_FBOOT_FILE" .fboot).libs.json"

                    existing_extra="$(curl -s -m 5 "http://${ip}/" | grep -oE 'href="/[^"]*\.(elf|libs\.json)"' | sed -E 's/href="\/(.*)"/\1/')"
                    for existing in $existing_extra; do
                        if [ "$existing" != "$manifest_name" ]; then
                            keep=0
                            for elf_path in "${MANIFEST_ELF_PATHS[@]}"; do
                                [ "$existing" = "$(basename "$elf_path")" ] && keep=1
                            done
                            if [ "$keep" = 0 ]; then
                                echo "  Entferne alten Lib-Kandidaten: ${existing}"
                                curl -s -m 10 -X POST "http://${ip}/delete/${existing}" -o /dev/null
                            fi
                        fi
                    done

                    ELF_OK=1
                    for elf_path in "${MANIFEST_ELF_PATHS[@]}"; do
                        elf_name="$(basename "$elf_path")"
                        echo "  Lade ${elf_path} -> http://${ip}/upload/${elf_name}"
                        HTTP_CODE="$(curl -s -o /dev/null -w "%{http_code}" -m 60 \
                            -X POST "http://${ip}/upload/${elf_name}" \
                            --data-binary @"${elf_path}" \
                            || echo "000")"
                        if [ "$HTTP_CODE" = "303" ]; then
                            echo "  OK (HTTP ${HTTP_CODE})"
                        else
                            echo "  WARNUNG: ELF-Upload fehlgeschlagen (HTTP ${HTTP_CODE})"
                            ELF_OK=0
                        fi
                    done

                    # Manifest bewusst ZULETZT hochladen: fehlt es, laedt die
                    # Firmware keine Lib - ein abgebrochener Upload ist so
                    # erkennbar.
                    if [ "$ELF_OK" = 1 ]; then
                        echo "  Lade ${manifest_tmp} -> http://${ip}/upload/${manifest_name}"
                        HTTP_CODE="$(curl -s -o /dev/null -w "%{http_code}" -m 30 \
                            -X POST "http://${ip}/upload/${manifest_name}" \
                            --data-binary @"${manifest_tmp}" \
                            || echo "000")"
                        if [ "$HTTP_CODE" = "303" ]; then
                            echo "  OK (HTTP ${HTTP_CODE})"
                        else
                            echo "  WARNUNG: Manifest-Upload fehlgeschlagen (HTTP ${HTTP_CODE}) - Libs auf dem Knoten sind damit unvollstaendig/inkonsistent."
                            NODE_OK=0
                        fi
                    else
                        echo "  WARNUNG: Mindestens ein ELF-Upload fehlgeschlagen - Manifest wird bewusst NICHT hochgeladen."
                        NODE_OK=0
                    fi
                fi
                rm -f "$manifest_tmp"
            fi
        fi
    fi

    if [ "$NODE_OK" = 1 ]; then
        REBOOT_NEEDED+=("$ip")
    else
        UPLOAD_FAILED+=("$ip")
    fi
done

echo "----------------------------------------------------------------------------"
echo "ZUSAMMENFASSUNG (${#REBOOT_NEEDED[@]}/${#NODE_ORDER[@]} Knoten erfolgreich):"
if [ "${#REBOOT_NEEDED[@]}" -eq "${#NODE_ORDER[@]}" ]; then
    echo "  ALLE ${#NODE_ORDER[@]} KNOTEN ERFOLGREICH HOCHGELADEN:"
    for ip in "${REBOOT_NEEDED[@]}"; do
        echo "  - ${ip}: OK"
    done
else
    for ip in "${NODE_ORDER[@]}"; do
        if [[ " ${REBOOT_NEEDED[*]:-} " == *" ${ip} "* ]]; then
            echo "  - ${ip}: OK"
        elif [[ " ${UPLOAD_FAILED[*]:-} " == *" ${ip} "* ]]; then
            echo "  - ${ip}: FEHLER (Upload fehlgeschlagen, siehe Warnungen oben)"
        elif [[ " ${UNREACHABLE[*]:-} " == *" ${ip} "* ]]; then
            echo "  - ${ip}: NICHT ERREICHBAR (uebersprungen)"
        fi
    done
fi

if [ "${#REBOOT_NEEDED[@]}" -gt 0 ]; then
    echo ""
    echo "Neue Dateien werden erst nach einem Neustart aktiv."
    echo "Manuell neu starten (z.B. \"Reboot\"-Button auf http://<ip>/):"
    for ip in "${REBOOT_NEEDED[@]}"; do
        echo "  - ${ip}"
    done
fi

if [ "${#REBOOT_NEEDED[@]}" -ne "${#NODE_ORDER[@]}" ]; then
    exit 1
fi
