# Gemeinsame Konfiguration/Hilfsfunktion zum Finden der lokalen
# 4diac_training1-Deploy-Dateien (fboot) - genutzt von
# make_4diac_training1_deploy.sh (Upload) UND make_libs_manifest.sh (lokale
# Manifest-Erzeugung, kein Upload). Nur per "source" einzubinden.
#
# IP-Zuordnung: NUR AX ist aktuell bekannt (192.168.178.55, von Franz genannt
# 2026-10-09). B-Station-IP ist noch nicht bekannt - sobald Franz sie nennt,
# hier ergaenzen (Zeile unten einkommentieren/anpassen).
declare -A NODE_BASES=(
    ["192.168.178.55"]="test_AX_FORTE_PC_AX.fboot"
    # ["<B-IP-noch-unbekannt>"]="test_B_FORTE_PC_B.fboot"
)

declare -A REPO_PATHS=(
    ["test_AX_FORTE_PC_AX.fboot"]="boot-files/test_AX_FORTE_PC_AX.fboot"
    ["test_B_FORTE_PC_B.fboot"]="boot-files/test_B_FORTE_PC_B.fboot"
)

NODE_ORDER=("192.168.178.55")

# Liefert den tatsaechlichen lokalen Pfad zu einer Basisdatei: zuerst gestempelte
# Variante im aktuellen Verzeichnis, dann unbestempelte Variante im aktuellen
# Verzeichnis, dann Repo-Fallback-Pfad. Leer, wenn nichts gefunden.
resolve_local_path() {
    local base="$1" name ext stamped_matches
    name="${base%.*}"
    ext="${base##*.}"
    stamped_matches=("${name}_"*".${ext}")
    if [ -f "${stamped_matches[0]:-}" ]; then
        echo "${stamped_matches[0]}"
    elif [ -f "$base" ]; then
        echo "$base"
    elif [ -f "${REPO_PATHS[$base]}" ]; then
        echo "${REPO_PATHS[$base]}"
    else
        echo ""
    fi
}
