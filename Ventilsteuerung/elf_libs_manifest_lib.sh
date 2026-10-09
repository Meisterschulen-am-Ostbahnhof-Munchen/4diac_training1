# ELF-Libs-Manifest-Logik (OSCAT/OSCAT_adapter), uebertragen aus
# Krauternter/Ventilsteuerung/elf_libs_manifest_lib.sh. Format/Kanonisierung
# sind seit 2026-10-09 durch den Firmware-Code (elf_libs_loader,
# LOGIBUS_integration_datapanel feature/elf-loader) festgelegt - siehe dortige
# Datei fuer die ausfuehrliche Begruendung/Firmware-Verhalten.
#
# Genutzt von make_libs_manifest.sh (rein lokal, kein Netzwerk) und
# make_4diac_training1_deploy.sh (laedt bei ENABLE_ELF_LIBS=1 zusaetzlich ELFs
# + Manifest hoch).
#
# Firmware-Verhalten (SO IMPLEMENTIERT in main.c, von Franz NICHT ausdruecklich
# bestaetigt): existiert eine *.libs.json und ist sie nicht ladbar, startet
# FORTE NICHT, Netzwerk/Dateiserver bleiben aktiv. 192.168.178.55 (AX) wurde
# 2026-10-09 live erfolgreich mit riscv32-ELFs + Manifest getestet - das ist
# also bestaetigt ein S31 mit dieser Firmware. Fuer jeden weiteren Knoten (z.B.
# B) erst SoC + Firmware-Branch mit Franz klaeren, bevor ENABLE_ELF_LIBS dafuer
# eingeschaltet wird - auf S3 fehlt noch die Host-Symboltabelle
# (elf_libs/host/elf_host_symbols_xtensa.cpp), auf P4 sind die riscv32-ELFs
# ungetestet.

# Architektur je Knoten - UNBESTAETIGTER PLATZHALTER (ausser 192.168.178.55,
# siehe oben), muss vor dem ersten echten Einsatz mit Franz gegen die reale
# Hardware abgeglichen werden.
declare -A NODE_ARCH=(
    ["192.168.178.55"]="riscv32"
)

# forte_abi: von Hand erhoehte Nummer, wenn sich FORTE-Basisklassen aendern.
# Quelle: Datei elf_libs/FORTE_ABI im Repo LOGIBUS_integration_datapanel.
FORTE_ABI=3

# Namensraum-Praefix (erstes Segment vor "::" in einem Type="...") -> Lib-Name.
declare -A PREFIX_TO_LIB=(
    ["OSCAT"]="OSCAT"
    ["OSCAT_adapter"]="OSCAT_adapter"
)

# Lib-Version, die aktuell als ELF gebaut/erwartet wird. Quelle: die echten
# MANIFEST.MF unter 4diacIDE-workspace/.lib/<Lib>*/MANIFEST.MF.
declare -A LIB_VERSIONS=(
    ["OSCAT"]="0.1.0"
    ["OSCAT_adapter"]="3.0.0"
)

# Abhaengigkeiten je Lib ("Name:Range", Leerzeichen-getrennt). Range-Format
# seit 2026-10-09 durch die Firmware festgelegt: "^MAJOR.MINOR[.PATCH]" (gleiche
# Major, bei Major 0 zusaetzlich gleiche Minor), ">=X.Y.Z" oder exakt "X.Y.Z".
# "adapter" bleibt bewusst fest in die Firmware gelinkt (noch nicht
# ausgelagert, wie bei Krauternter), daher kein eigener Eintrag dafuer.
declare -A LIB_REQUIRES=(
    ["OSCAT_adapter"]="OSCAT:^0.1"
)

# Lib-Ordnername unter 4diacIDE-workspace/.lib/ (nicht einheitlich).
declare -A LIB_DIR_NAME=(
    ["OSCAT"]="OSCAT"
    ["OSCAT_adapter"]="OSCAT_adapter-3.0.0"
)

ELF_DIR="elf-libs"

sha256_of() {
    local f="$1"
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$f" | awk '{print $1}'
    else
        shasum -a 256 "$f" | awk '{print $1}'
    fi
}

sha256_stdin() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum | awk '{print $1}'
    else
        shasum -a 256 | awk '{print $1}'
    fi
}

# Liest die benoetigten Lib-Namen aus einem .fboot: Type="PRAEFIX::..."
# sammeln, ueber PREFIX_TO_LIB mappen, transitiv per LIB_REQUIRES erweitern.
resolve_required_libs() {
    local fboot_file="$1" prefix lib req name
    declare -A seen=()
    local -a queue=()

    while IFS= read -r prefix; do
        lib="${PREFIX_TO_LIB[$prefix]:-}"
        if [ -n "$lib" ] && [ -z "${seen[$lib]:-}" ]; then
            seen[$lib]=1
            queue+=("$lib")
        fi
    done < <(grep -oE 'Type="[A-Za-z0-9_]+::' "$fboot_file" | sed -E 's/Type="([A-Za-z0-9_]+)::/\1/' | sort -u)

    local i=0
    while [ "$i" -lt "${#queue[@]}" ]; do
        lib="${queue[$i]}"
        i=$((i + 1))
        for req in ${LIB_REQUIRES[$lib]:-}; do
            name="${req%%:*}"
            if [ -z "${seen[$name]:-}" ]; then
                seen[$name]=1
                queue+=("$name")
            fi
        done
    done

    # "${queue[@]}" bei leerem Array nicht einfach an printf uebergeben: ohne
    # Argumente gibt printf trotzdem EINE Leerzeile aus, mapfile liest das als
    # ein Element "" statt eines leeren Arrays.
    if [ "${#queue[@]}" -gt 0 ]; then
        printf '%s\n' "${queue[@]}"
    fi
}

# Liest die in der echten MANIFEST.MF deklarierte Lib-Version
# (Product/VersionInfo/@Version unter 4diacIDE-workspace/.lib/<LibVerzeichnis>/
# MANIFEST.MF). Leer, wenn die Datei fehlt oder nicht geparst werden kann -
# dann wird NICHT geprueft (siehe Aufrufer), statt faelschlich abzubrechen.
mf_version_of() {
    local lib="$1" dir mf
    dir="${LIB_DIR_NAME[$lib]:-$lib}"
    mf="4diacIDE-workspace/.lib/${dir}/MANIFEST.MF"
    [ -f "$mf" ] || { echo ""; return; }
    grep -A1 '<Product ' "$mf" | grep -oE 'Version="[^"]+"' | tail -1 | sed -E 's/Version="([^"]+)"/\1/'
}

# Findet den lokalen Pfad eines Lib-ELFs: ELF_DIR flach, sonst Repo-Pfad
# 4diacIDE-workspace/.lib/<LibVerzeichnis>/elf/<arch>/<Name>-<Version>-<arch>.elf.
resolve_elf_path() {
    local lib="$1" version="$2" arch="$3" fname dir repo_path
    fname="${lib}-${version}-${arch}.elf"
    if [ -f "${ELF_DIR}/${fname}" ]; then
        echo "${ELF_DIR}/${fname}"
        return
    fi
    dir="${LIB_DIR_NAME[$lib]:-$lib}"
    repo_path="4diacIDE-workspace/.lib/${dir}/elf/${arch}/${fname}"
    if [ -f "$repo_path" ]; then
        echo "$repo_path"
        return
    fi
    echo ""
}

# Baut <programm>.libs.json (Pfad in $3) fuer einen Knoten: $1=Arch,
# $2=Array-Name (nameref) der lokalen "files"-Pfade, $4=Array-Name (nameref)
# der benoetigten Lib-Namen. 0 bei Erfolg (setzt MANIFEST_ELF_PATHS), 1
# (nichts geschrieben) wenn ein ELF fehlt oder ein Firmware-Limit verletzt
# wuerde.
build_libs_manifest() {
    local arch="$1" files_ref="$2" out_path="$3" libs_ref="$4"
    local -n _files="$files_ref"
    local -n _libs="$libs_ref"
    local lib version elf_path missing=0
    declare -A elf_path_of=()

    if [ "${#_libs[@]}" -gt 16 ]; then
        echo "  WARNUNG: ${#_libs[@]} Libs benoetigt, Firmware erlaubt max. 16 - uebersprungen."
        return 1
    fi
    if [ $(( ${#_libs[@]} + ${#_files[@]} )) -gt 64 ]; then
        echo "  WARNUNG: ${#_libs[@]} Libs + ${#_files[@]} Dateien > 64 Eintraege (Firmware-Limit) - uebersprungen."
        return 1
    fi

    local mf_ver
    for lib in "${_libs[@]}"; do
        version="${LIB_VERSIONS[$lib]:-}"
        if [ -z "$version" ]; then
            echo "  WARNUNG: Keine Version fuer Lib '${lib}' in LIB_VERSIONS hinterlegt - uebersprungen."
            return 1
        fi
        mf_ver="$(mf_version_of "$lib")"
        if [ -n "$mf_ver" ] && [ "$mf_ver" != "$version" ]; then
            echo "  WARNUNG: LIB_VERSIONS[${lib}]=${version} stimmt nicht mit MANIFEST.MF (${mf_ver}) ueberein - LIB_VERSIONS aktualisieren. Uebersprungen."
            return 1
        fi
        elf_path="$(resolve_elf_path "$lib" "$version" "$arch")"
        if [ -z "$elf_path" ]; then
            echo "  Hinweis: ELF fehlt lokal (${lib}-${version}-${arch}.elf, weder in ${ELF_DIR}/ noch unter 4diacIDE-workspace/.lib/${LIB_DIR_NAME[$lib]:-$lib}/elf/${arch}/) - uebersprungen."
            missing=1
            continue
        fi
        elf_path_of[$lib]="$elf_path"
    done
    if [ "$missing" = 1 ]; then
        return 1
    fi

    local -a canon_lines=()
    local -a lib_json_entries=()
    for lib in "${_libs[@]}"; do
        elf_path="${elf_path_of[$lib]}"
        version="${LIB_VERSIONS[$lib]}"
        local fname size sha requires_json="[]" req name range first=1
        fname="$(basename "$elf_path")"
        size="$(wc -c < "$elf_path" | tr -d ' ')"
        sha="$(sha256_of "$elf_path")"
        canon_lines+=("${fname}:${sha}")

        requires_json="["
        for req in ${LIB_REQUIRES[$lib]:-}; do
            name="${req%%:*}"
            range="${req#*:}"
            if [ "$first" = 1 ]; then first=0; else requires_json+=","; fi
            requires_json+="{\"name\":\"${name}\",\"range\":\"${range}\"}"
        done
        requires_json+="]"

        lib_json_entries+=("{\"name\":\"${lib}\",\"version\":\"${version}\",\"file\":\"${fname}\",\"size\":${size},\"sha256\":\"${sha}\",\"requires\":${requires_json}}")
    done

    local -a file_json_entries=()
    local f fname size sha
    for f in "${_files[@]}"; do
        fname="$(basename "$f")"
        size="$(wc -c < "$f" | tr -d ' ')"
        sha="$(sha256_of "$f")"
        canon_lines+=("${fname}:${sha}")
        file_json_entries+=("{\"file\":\"${fname}\",\"size\":${size},\"sha256\":\"${sha}\"}")
    done

    local dup_check
    dup_check="$(printf '%s\n' "${canon_lines[@]%%:*}" | sort | uniq -d)"
    if [ -n "$dup_check" ]; then
        echo "  WARNUNG: Doppelte Dateinamen zwischen libs[] und files[] (${dup_check}) - uebersprungen."
        return 1
    fi

    # -t: -k1,1: nach dem Dateiname-Feld sortieren (vor dem ersten ":"), nicht
    # nach der ganzen Zeile - muss exakt der Sortierung in cmp_hashed()
    # (elf_libs_loader.c, sortiert nur ueber .name) entsprechen.
    local manifest_sha
    manifest_sha="$(printf '%s\n' "${canon_lines[@]}" | LC_ALL=C sort -t: -k1,1 | sha256_stdin)"

    {
        printf '{\n'
        printf '  "format": 1,\n'
        printf '  "forte_abi": %s,\n' "$FORTE_ABI"
        printf '  "arch": "%s",\n' "$arch"
        printf '  "libs": [%s],\n' "$(IFS=,; echo "${lib_json_entries[*]}")"
        printf '  "files": [%s],\n' "$(IFS=,; echo "${file_json_entries[*]}")"
        printf '  "manifest_sha256": "%s",\n' "$manifest_sha"
        printf '  "signature": null\n'
        printf '}\n'
    } > "$out_path"

    local manifest_size
    manifest_size="$(wc -c < "$out_path" | tr -d ' ')"
    if [ "$manifest_size" -gt 65536 ]; then
        echo "  WARNUNG: Manifest ${manifest_size} Bytes > 64 KB (Firmware-Limit) - uebersprungen."
        rm -f "$out_path"
        return 1
    fi

    MANIFEST_ELF_PATHS=()
    for lib in "${_libs[@]}"; do
        MANIFEST_ELF_PATHS+=("${elf_path_of[$lib]}")
    done
    return 0
}
