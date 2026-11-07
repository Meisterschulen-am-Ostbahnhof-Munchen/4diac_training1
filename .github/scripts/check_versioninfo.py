#!/usr/bin/env python3
# Copyright (c) 2026 Meisterschulen am Ostbahnhof
# SPDX-License-Identifier: EPL-2.0
"""Prueft die <VersionInfo>-Eintraege in IEC-61499-Typdateien.

Fehler:   Eintraege nicht nach Datum absteigend (neuester muss oben stehen),
          Datei nicht lesbar oder ausserhalb des Arbeitsverzeichnisses.
Warnung:  dieselbe Versionsnummer mehrfach in einer Datei
          (mit --strict ebenfalls Fehler), VersionInfo ohne Version.

Aufruf: check_versioninfo.py [--strict] [Datei ...]
Ohne Dateien werden alle per git ls-files gefundenen Typdateien geprueft.
"""
import re
import subprocess
import sys
from pathlib import Path

EXT = ('*.fbt', '*.FBT', '*.sub', '*.SUB', '*.adp', '*.ADP', '*.dtp', '*.DTP', '*.atp', '*.ATP')
VI = re.compile(r'<VersionInfo\b[^>]*>')
VERSION = re.compile(r'\bVersion="([^"]*)"')
DATE = re.compile(r'\bDate="([^"]*)"')
ROOT = Path.cwd().resolve()


def files_from_git():
    out = subprocess.check_output(['git', 'ls-files', '-z', '--', *EXT])
    return [f for f in out.decode('utf-8').split('\0') if f]


def attr(rx, tag):
    m = rx.search(tag)
    return m.group(1) if m else ''


def read(path):
    """Liest eine Datei innerhalb des Arbeitsverzeichnisses, sonst None."""
    p = (ROOT / path).resolve()
    if not p.is_relative_to(ROOT):
        print(f'::error file={path}::ausserhalb des Arbeitsverzeichnisses')
        return None
    try:
        return p.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as exc:
        print(f'::error file={path}::nicht lesbar: {exc}')
        return None


def entries_of(text):
    return [(attr(VERSION, m.group(0)), attr(DATE, m.group(0)), text.count('\n', 0, m.start()) + 1)
            for m in VI.finditer(text)]


def check_order(path, entries):
    errors = 0
    for (v1, d1, _), (v2, d2, l2) in zip(entries, entries[1:]):
        if d1 and d2 and d2 > d1:
            print(f'::error file={path},line={l2}::VersionInfo {v2} ({d2}) steht unter {v1} ({d1}) - neuester Eintrag muss oben stehen')
            errors += 1
    return errors


def check_duplicates(path, entries, strict):
    errors = 0
    level = 'error' if strict else 'warning'
    seen = {}
    for v, _, ln in entries:
        if not v:
            print(f'::warning file={path},line={ln}::VersionInfo ohne Versionsnummer')
        elif v in seen:
            print(f'::{level} file={path},line={ln}::Version {v} doppelt (auch Zeile {seen[v]})')
            errors += int(strict)
        else:
            seen[v] = ln
    return errors


def check(path, strict):
    text = read(path)
    if text is None:
        return 1
    entries = entries_of(text)
    return check_order(path, entries) + check_duplicates(path, entries, strict)


def main(argv):
    strict = '--strict' in argv
    files = [a for a in argv if a != '--strict'] or files_from_git()
    errors = sum(check(f, strict) for f in files)
    print(f'{len(files)} Dateien geprueft, {errors} Fehler')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
