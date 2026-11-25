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
    ... --notes                                (Runtime-Kopf der Notes auf die Assets umstellen)

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
LIBVER_FILE = 'Ventilsteuerung/scripts_central/elf_libs_manifest_lib.py'

# Target -> Architektur, nur für Builds ohne build.json (Liste laut ELFMASTER, 2026-11-25)
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

# Erlaubte Eingaben: keine Pfadtrenner, kein führendes "-"
RE_TAG = re.compile(r'v\d+\.\d+[a-z]?')
RE_BUILD = re.compile(r'v\d[\w.]*-alpha-b-\d+-g[0-9a-f]{7,40}')
RE_TARGET = re.compile(r'\w+', re.ASCII)
RE_ARCH = re.compile(r'riscv32|xtensa')
RE_BIN = re.compile(r'(Application|merged-flash)_\w+\.bin', re.ASCII)
RE_SHA = re.compile(r'[0-9a-f]{64}')
RE_COMMIT = re.compile(r'[0-9a-f]{7,40}')
ELFLIB = re.compile(rb'ELFLIB:([\w.-]+):([\w.-]+):(\d+):(\w+)')


def fail(msg: str) -> None:
    sys.exit(msg)


def check(rx: re.Pattern, value, what: str) -> str:
    if not isinstance(value, str) or not rx.fullmatch(value):
        fail(f'Ungültig ({what}): {value!r}')
    return value


def entries(base: Path) -> dict[str, Path]:
    """Einträge eines Ordners nach Name. Die Pfade kommen so aus dem Dateisystem
    und werden nie aus Eingaben zusammengesetzt (kein Path Traversal)."""
    return {e.name: e for e in base.iterdir()}


def pick_tag(name: str) -> str:
    """Tag aus "git tag --list" nehmen (nicht die Eingabe selbst)."""
    tags = {t: t for t in git('tag', '--list').split()}
    tag = tags.get(name)
    if tag is None:
        fail(f'Tag fehlt im Repo: {name} (vorher git fetch --tags)')
    return tag


def pick(found: dict[str, Path], name: str, what: str) -> Path:
    p = found.get(name)
    if p is None:
        fail(f'{what} fehlt: {name}')
    return p


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str, binary: bool = False):
    r = subprocess.run(['git', *args], capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode('utf-8')


def lib_versions(tag: str) -> dict[str, str]:
    """LIB_VERSIONS aus elf_libs_manifest_lib.py im Tag lesen (welche ELF-Version genutzt wird)."""
    src = git('show', f'{tag}:{LIBVER_FILE}')
    block = src[src.index('LIB_VERSIONS = {'):]
    block = block[:block.index('}')]
    return dict(re.findall(r'"(\w+)":\s*"([\d.]+)"', block))


def elf_name(path: str) -> tuple[str, str]:
    """'.../<lib>-<ver>-<arch>.elf' -> (lib, ver)"""
    lib, ver, _arch = path.rsplit('/', 1)[1][:-4].rsplit('-', 2)
    return lib, ver


def check_elf_abi(tag: str, abi: int) -> int:
    """Genutzte ELFs (laut LIB_VERSIONS) im Tag prüfen: ELFLIB mit forte_abi == abi.
    Ältere, nicht genutzte ELF-Versionen werden nur gemeldet."""
    used = lib_versions(tag)
    paths = [p for p in git('ls-tree', '-r', '--name-only', tag).splitlines() if p.endswith('.elf')]
    if not paths:
        fail(f'Keine ELFs im Tag {tag}')
    missing = sorted(set(used) - {elf_name(p)[0] for p in paths})
    if missing:
        fail(f'ELF fehlt im Tag für: {", ".join(missing)}')
    bad, n = [], 0
    for p in paths:
        lib, ver = elf_name(p)
        if used.get(lib) != ver:
            print(f'  nicht genutzt (alte Version): {p}')
            continue
        n += 1
        m = ELFLIB.search(git('show', f'{tag}:{p}', binary=True))
        if not m or int(m.group(3)) != abi:
            bad.append(f'{p}: {m.group(0).decode() if m else "kein ELFLIB"}')
    if bad:
        print('\n'.join(f'  forte_abi passt nicht: {b}' for b in bad), file=sys.stderr)
        fail(f'{len(bad)} von {n} genutzten ELFs haben nicht forte_abi {abi}')
    return n


def info_from_args(build: str, forte_abi: int | None, forte_commit: str | None) -> dict:
    """Ohne build.json: Werte aus der Kommandozeile."""
    if forte_abi is None:
        fail('Keine build.json im Build-Ordner: --forte-abi angeben')
    return {'logibus_commit': build.rsplit('-g', 1)[1], 'forte_commit': forte_commit,
            'forte_abi': forte_abi, 'targets': TARGETS}


def load_build_info(src: Path, build: str, forte_abi: int | None, forte_commit: str | None) -> dict:
    """build.json lesen und prüfen, falls vorhanden."""
    bj = src / 'build.json'
    if not bj.is_file():
        return info_from_args(build, forte_abi, forte_commit)
    info = json.loads(bj.read_text(encoding='utf-8'))
    if info.get('version') != build:
        fail(f'build.json gehört zu {info.get("version")!r}, nicht zu {build}')
    abi = info.get('forte_abi')
    if not isinstance(abi, int) or (forte_abi is not None and forte_abi != abi):
        fail(f'forte_abi in build.json ({abi!r}) fehlt oder widerspricht --forte-abi')
    targets = info.get('targets')
    if not isinstance(targets, dict) or not targets:
        fail('build.json: targets fehlt')
    for t, arch in targets.items():
        check(RE_TARGET, t, 'Target in build.json')
        check(RE_ARCH, arch, f'arch von {t}')
    commits = {k: info.get(k) for k in ('logibus_commit', 'forte_commit')}
    for k, v in commits.items():
        if v is not None:
            check(RE_COMMIT, v, k)
    print(f'build.json: forte_abi {abi}, {len(targets)} Targets')
    return {**commits, 'forte_abi': abi, 'targets': targets}


def read_sums(path: Path) -> dict[str, str]:
    """SHA256SUMS (sha256sum-Format) lesen; nur gültige .bin-Namen."""
    sums = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        h, name = line.split(maxsplit=1)
        name = check(RE_BIN, name.lstrip('*'), 'Dateiname in SHA256SUMS')
        sums[name] = check(RE_SHA, h.lower(), f'SHA256 von {name}')
    return sums


def check_file(found: dict[str, Path], name: str, sums: dict[str, str]) -> tuple[Path, dict]:
    """Datei muss im Build-Ordner liegen und zur SHA256SUMS des Builds passen."""
    p = pick(found, check(RE_BIN, name, 'Dateiname'), 'Datei im Build-Ordner')
    if not p.is_file():
        fail(f'Keine Datei: {p}')
    h = sha256(p)
    if sums.get(name) != h:
        fail(f'SHA256 passt nicht zum Build: {name} (Drive {h}, Build {sums.get(name)})')
    return p, {'file': name, 'size': p.stat().st_size, 'sha256': h}


def check_targets(src: Path, targets: dict[str, str], sums: dict[str, str]) -> tuple[dict, list[Path]]:
    found = entries(src)
    out, files = {}, []
    for t, arch in targets.items():
        pa, app = check_file(found, f'Application_{t}.bin', sums)
        pm, merged = check_file(found, f'merged-flash_{t}.bin', sums)
        out[t] = {'arch': arch, 'application': app, 'merged_flash': merged}
        files += [pa, pm]
        print(f'  {t:26} {arch:8} ok')
    return out, files


def runtime_head(lines: list[str]) -> tuple[int | None, int]:
    """Zeilenbereich [start, end) des Runtime-Kopfs: ab "## Runtime:" bis vor
    "Neu in der Runtime:" oder die nächste "## "-Überschrift."""
    start = next((i for i, line in enumerate(lines) if line.startswith('## Runtime:')), None)
    if start is None:
        return None, 0
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith(('Neu in der Runtime:', '## '))), len(lines))
    return start, end

RE_PREV = re.compile(r'\(neu, vorher ([^)\s]+)\)')
DRIVE_REMOTE = 'gdrive_team:Public/Visuelle-Programmierung/Flash_Controller/logiBUS'


def runtime_block(build: str, prev: str | None) -> str:
    """Kopf des Abschnitts "## Runtime:" (Verweis auf die Assets); "Neu in der Runtime" bleibt."""
    vorher = f' (neu, vorher {prev})' if prev else ''
    return (f'## Runtime:\n{build}{vorher}\n\n'
            'Download: unten unter **Assets**\n'
            '- Update im Browser (OTA): `Application_<Board>.bin`\n'
            '- Erst-Flashen per USB (esptool, ab 0x0): `merged-flash_<Board>.bin`\n'
            '- Prüfsummen: `SHA256SUMS`, für den Installer: `firmware.json`\n\n'
            f'Google Drive (Trainer): `{DRIVE_REMOTE}/{build}`\n\n')


def update_notes(tag: str, build: str, prev: str | None) -> None:
    """Runtime-Kopf der Release-Notes ersetzen (alte Notes werden vorher gesichert)."""
    body = subprocess.run(['gh', 'release', 'view', tag, '--json', 'body', '-q', '.body'],
                          capture_output=True, check=True, encoding='utf-8').stdout.rstrip('\n')
    lines = body.split('\n')
    start, end = runtime_head(lines)
    if start is None:
        fail(f'Kein Abschnitt "## Runtime:" in den Notes von {tag}')
    if prev is None:
        pm = RE_PREV.search('\n'.join(lines[start:end]))
        prev = pm.group(1) if pm else None
    new = '\n'.join(lines[:start]) + ('\n' if start else '') + runtime_block(build, prev) + '\n'.join(lines[end:])
    tmp = Path(tempfile.mkdtemp(prefix='notes_'))
    (tmp / 'notes_alt.md').write_text(body, encoding='utf-8', newline='\n')
    (tmp / 'notes_neu.md').write_text(new, encoding='utf-8', newline='\n')
    if new == body:
        print('Release-Notes schon aktuell')
        return
    subprocess.run(['gh', 'release', 'edit', tag, '--notes-file', str(tmp / 'notes_neu.md')], check=True)
    print(f'Release-Notes: Runtime-Kopf ersetzt (alt/neu in {tmp})')


def upload(tag: str, files: list[Path]) -> None:
    """In Paketen hochladen; Dateien erst nach '--'."""
    names = [str(p) for p in files]
    for i in range(0, len(names), 8):
        subprocess.run(['gh', 'release', 'upload', '--clobber', tag, '--', *names[i:i + 8]], check=True)
    print(f'Hochgeladen: {len(names)} Dateien an {tag}')


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--tag', required=True, help='training1-Release, z. B. v0.28l')
    ap.add_argument('--build', required=True, help='LOGIBUS-Build, z. B. v0.27-alpha-b-179-g24534469')
    ap.add_argument('--forte-abi', type=int, help='nur nötig, wenn der Build keine build.json hat')
    ap.add_argument('--forte-commit', help='forte-Commit, nur ohne build.json')
    ap.add_argument('--upload', action='store_true', help='per gh release upload --clobber hochladen')
    ap.add_argument('--notes', action='store_true', help='Runtime-Kopf der Release-Notes auf die Assets umstellen')
    ap.add_argument('--prev-build', help='Vorgänger-Build für "(neu, vorher …)"; sonst aus den Notes')
    a = ap.parse_args()
    check(RE_TAG, a.tag, '--tag')
    check(RE_BUILD, a.build, '--build')
    if a.forte_commit is not None:
        check(RE_COMMIT, a.forte_commit, '--forte-commit')
    if a.prev_build is not None:
        check(re.compile(r'[\w.-]+'), a.prev_build, '--prev-build')
    return a


def main() -> None:
    a = parse_args()
    src = pick(entries(Path(DRIVE_DEFAULT)), a.build, 'Build-Ordner im Drive')
    if not src.is_dir():
        fail(f'Kein Ordner: {src}')
    # Ab hier nur noch Werte aus Dateisystem bzw. git, nicht die Eingaben selbst
    build = src.name
    tag = pick_tag(a.tag)
    sums_path = pick(entries(src), 'SHA256SUMS', 'SHA256SUMS vom Build (entsteht beim Compilieren)')

    info = load_build_info(src, build, a.forte_abi, a.forte_commit)
    sums = read_sums(sums_path)
    n = check_elf_abi(tag, info['forte_abi'])
    print(f'Genutzte ELFs im Tag {tag}: {n}, alle forte_abi {info["forte_abi"]}')
    targets, files = check_targets(src, info['targets'], sums)

    manifest = {'build': build, 'logibus_commit': info['logibus_commit'],
                'forte_commit': info['forte_commit'], 'training1': tag,
                'forte_abi': info['forte_abi'], 'targets': targets}
    tmp = Path(tempfile.mkdtemp(prefix='fw_'))
    out = tmp / 'firmware.json'
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    # SHA256SUMS fürs Release aus den geprüften Werten neu schreiben, nicht die Drive-Datei kopieren
    sums_out = tmp / 'SHA256SUMS'
    lines = [f'{f["sha256"]}  {f["file"]}' for t in targets.values() for f in (t['application'], t['merged_flash'])]
    sums_out.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    print(f'firmware.json: {out}')

    if a.upload:
        upload(tag, [*files, out, sums_out])
    if a.notes:
        update_notes(tag, build, a.prev_build)
    if not (a.upload or a.notes):
        print('Nur geprüft. Zum Hochladen --upload, für die Notes --notes angeben.')


if __name__ == '__main__':
    main()
