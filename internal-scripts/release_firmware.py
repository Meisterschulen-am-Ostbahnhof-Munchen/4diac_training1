#!/usr/bin/env python3
"""Firmware als Assets an ein 4diac_training1-Release hängen (für den TrainingsInstaller).

Pro Target kommen Application_<T>.bin und merged-flash_<T>.bin ans Release,
dazu firmware.json mit Build, forte_abi, arch und SHA256 je Datei.
Die SHA256 kommen vom Build selbst (SHA256SUMS im Build-Ordner, erzeugt beim
Compilieren); das Skript prüft die Dateien auf dem Drive dagegen. Liegt eine
build.json daneben, kommen forte_abi, Commits und Targets daraus.
Vorher wird geprüft, ob alle genutzten ELFs im Tag (laut LIB_VERSIONS) dieselbe
forte_abi haben (ELFLIB-String "ELFLIB:<lib>:<version>:<abi>:<arch>").

Schritt im Release-Ablauf: nach "gh release create" aufrufen.

Aufruf:
    python internal-scripts/release_firmware.py --tag v0.28l \
        --build v0.27-alpha-b-179-g24534469 --forte-abi 6            (nur prüfen;
                                                       --forte-abi nur ohne build.json)
    ... --upload                                                      (hochladen, --clobber)

Der Build-Ordner liegt auf dem Team-Drive (gdrive_team:Public/Visuelle-Programmierung/
Flash_Controller/logiBUS/<Build>), lokal z. B. unter G:\\Geteilte Ablagen\\Classroom\\...
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

DRIVE_DEFAULT = r'G:\Geteilte Ablagen\Classroom\Public\Visuelle-Programmierung\Flash_Controller\logiBUS'

# Target -> Architektur (Liste laut ELFMASTER, 2026-11-25)
TARGETS = {
    'ESP32P4_NodeISO20': 'riscv32',
    'ESP32P4_NodeISO20_V3': 'riscv32',
    'ESP32S31_Trainer20': 'riscv32',
    'ESP32S3_deca_out': 'xtensa',
    'ESP32S3_dual_can': 'xtensa',
    'ESP32S3_dual_io': 'xtensa',
    'ESP32S3_dual_out': 'xtensa',
    'ESP32S3_octa_out': 'xtensa',
    'HutschienenmopedXL': 'xtensa',
    'HutschienenmopedXL26': 'xtensa',
    'HutschienenmopedXL_1ETH': 'xtensa',
    'HutschienenmopedXL_2ETH': 'xtensa',
    'M5_CoreS3_1ETH': 'xtensa',
    'lilygo_T_Connect_Pro': 'xtensa',
}

ELFLIB = re.compile(rb'ELFLIB:([\w.-]+):([\w.-]+):(\d+):(\w+)')


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str, binary: bool = False):
    r = subprocess.run(['git', *args], capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode('utf-8')


LIBVER_FILE = 'Ventilsteuerung/scripts_central/elf_libs_manifest_lib.py'


def lib_versions(tag: str) -> dict[str, str]:
    """LIB_VERSIONS aus elf_libs_manifest_lib.py im Tag lesen (welche ELF-Version genutzt wird)."""
    src = git('show', f'{tag}:{LIBVER_FILE}')
    block = src[src.index('LIB_VERSIONS = {'):]
    block = block[:block.index('}')]
    return dict(re.findall(r'"([\w]+)":\s*"([\d.]+)"', block))


def check_elf_abi(tag: str, abi: int) -> int:
    """Genutzte ELFs (laut LIB_VERSIONS) im Tag prüfen: ELFLIB mit forte_abi == abi.
    Ältere, nicht genutzte ELF-Versionen werden nur gemeldet."""
    used = lib_versions(tag)
    paths = [p for p in git('ls-tree', '-r', '--name-only', tag).splitlines() if p.endswith('.elf')]
    if not paths:
        sys.exit(f'Keine ELFs im Tag {tag}')
    bad, n, unused = [], 0, []
    for p in paths:
        name = p.rsplit('/', 1)[1][:-4]          # <lib>-<ver>-<arch>
        lib, ver, _arch = name.rsplit('-', 2)
        if used.get(lib) != ver:
            unused.append(p)
            continue
        n += 1
        m = ELFLIB.search(git('show', f'{tag}:{p}', binary=True))
        if not m or int(m.group(3)) != abi:
            bad.append((p, m.group(0).decode() if m else 'kein ELFLIB'))
    missing = sorted(set(used) - {p.rsplit('/', 1)[1].rsplit('-', 2)[0] for p in paths})
    for p in unused:
        print(f'  nicht genutzt (alte Version): {p}')
    if missing:
        sys.exit(f'ELF fehlt im Tag für: {", ".join(missing)}')
    if bad:
        for p, s in bad:
            print(f'  forte_abi passt nicht: {p}: {s}', file=sys.stderr)
        sys.exit(f'{len(bad)} von {n} genutzten ELFs haben nicht forte_abi {abi}')
    return n


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--tag', required=True, help='training1-Release, z. B. v0.28l')
    ap.add_argument('--build', required=True, help='LOGIBUS-Build, z. B. v0.27-alpha-b-179-g24534469')
    ap.add_argument('--forte-abi', type=int, help='nur nötig, wenn der Build keine build.json hat')
    ap.add_argument('--drive', default=DRIVE_DEFAULT, help='Ordner mit den Build-Ordnern')
    ap.add_argument('--sums', help='SHA256SUMS vom Build (Default: <Build-Ordner>/SHA256SUMS)')
    ap.add_argument('--forte-commit', help='forte-Commit des Builds (optional)')
    ap.add_argument('--upload', action='store_true', help='per gh release upload --clobber hochladen')
    a = ap.parse_args()

    src = Path(a.drive) / a.build
    if not src.is_dir():
        sys.exit(f'Build-Ordner fehlt: {src}')

    targets_arch = TARGETS
    bj = src / 'build.json'
    if bj.is_file():
        info = json.loads(bj.read_text(encoding='utf-8'))
        if info.get('version') != a.build:
            sys.exit(f'build.json gehört zu {info.get("version")}, nicht zu {a.build}')
        if a.forte_abi is not None and a.forte_abi != info['forte_abi']:
            sys.exit(f'--forte-abi {a.forte_abi} widerspricht build.json ({info["forte_abi"]})')
        a.forte_abi = info['forte_abi']
        a.forte_commit = info.get('forte_commit') or a.forte_commit
        logibus_commit = info.get('logibus_commit')
        targets_arch = info['targets']
        print(f'build.json: forte_abi {a.forte_abi}, {len(targets_arch)} Targets')
    else:
        if a.forte_abi is None:
            sys.exit('Keine build.json im Build-Ordner: --forte-abi angeben')
        g = re.search(r'-g([0-9a-f]{7,})$', a.build)
        logibus_commit = g.group(1) if g else None
    sums_path = Path(a.sums) if a.sums else src / 'SHA256SUMS'
    if not sums_path.is_file():
        sys.exit(f'SHA256SUMS vom Build fehlt: {sums_path} (wird beim Compilieren erzeugt)')
    sums = {}
    for line in sums_path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            h, name = line.split(maxsplit=1)
            sums[name.lstrip('*')] = h.lower()

    n = check_elf_abi(a.tag, a.forte_abi)
    print(f'Genutzte ELFs im Tag {a.tag}: {n}, alle forte_abi {a.forte_abi}')

    files: list[Path] = []
    targets = {}
    for t, arch in targets_arch.items():
        entry = {'arch': arch}
        for key, name in (('application', f'Application_{t}.bin'), ('merged_flash', f'merged-flash_{t}.bin')):
            p = src / name
            if not p.is_file():
                sys.exit(f'Datei fehlt: {p}')
            h = sha256(p)
            if sums.get(name) != h:
                sys.exit(f'SHA256 passt nicht zum Build: {name} (Drive {h}, Build {sums.get(name)})')
            entry[key] = {'file': name, 'size': p.stat().st_size, 'sha256': h}
            files.append(p)
        targets[t] = entry
        print(f'  {t:26} {arch:8} ok')

    manifest = {'build': a.build, 'logibus_commit': logibus_commit,
                'forte_commit': a.forte_commit,
                'training1': a.tag, 'forte_abi': a.forte_abi, 'targets': targets}
    out = Path(tempfile.mkdtemp(prefix='fw_')) / 'firmware.json'
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'firmware.json: {out}')

    if not a.upload:
        print('Nur geprüft. Zum Hochladen --upload angeben.')
        return
    # in Paketen hochladen, damit die Kommandozeile kurz bleibt
    allf = [str(p) for p in files] + [str(out)]
    sums_out = out.with_name('SHA256SUMS')
    sums_out.write_bytes(sums_path.read_bytes())
    allf.append(str(sums_out))
    for i in range(0, len(allf), 8):
        subprocess.run(['gh', 'release', 'upload', a.tag, *allf[i:i + 8], '--clobber'], check=True)
    print(f'Hochgeladen: {len(allf)} Dateien an {a.tag}')


if __name__ == '__main__':
    main()
