#!/usr/bin/env python3
# Copyright (c) 2026 Meisterschulen am Ostbahnhof
# SPDX-License-Identifier: EPL-2.0
"""Prueft die <VersionInfo>-Eintraege in IEC-61499-Typdateien.

Fehler:   Eintraege nicht nach Datum absteigend (neuester muss oben stehen).
Warnung:  dieselbe Versionsnummer mehrfach in einer Datei
          (mit --strict ebenfalls Fehler).

Aufruf: check_versioninfo.py [--strict] [Datei ...]
Ohne Dateien werden alle per git ls-files gefundenen Typdateien geprueft.
"""
import re
import subprocess
import sys

EXT = ('*.fbt', '*.FBT', '*.sub', '*.SUB', '*.adp', '*.ADP', '*.dtp', '*.DTP', '*.atp', '*.ATP')
VI = re.compile(r'<VersionInfo\b([^>]*)>')
ATTR = re.compile(r'(\w+)="([^"]*)"')


def files_from_git():
    out = subprocess.check_output(['git', 'ls-files', '-z', '--', *EXT])
    return [f for f in out.decode('utf-8').split('\0') if f]


def line_of(text, pos):
    return text.count('\n', 0, pos) + 1


def check(path, strict):
    try:
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        print(f'::warning file={path}::nicht lesbar: {exc}')
        return 0
    entries = []
    for m in VI.finditer(text):
        a = dict(ATTR.findall(m.group(1)))
        entries.append((a.get('Version', ''), a.get('Date', ''), line_of(text, m.start())))
    errors = 0
    for (v1, d1, l1), (v2, d2, l2) in zip(entries, entries[1:]):
        if d1 and d2 and d2 > d1:
            print(f'::error file={path},line={l2}::VersionInfo {v2} ({d2}) steht unter {v1} ({d1}) - neuester Eintrag muss oben stehen')
            errors += 1
    seen = {}
    for v, d, ln in entries:
        if v in seen:
            level = 'error' if strict else 'warning'
            print(f'::{level} file={path},line={ln}::Version {v} doppelt (auch Zeile {seen[v]})')
            if strict:
                errors += 1
        else:
            seen[v] = ln
    return errors


def main(argv):
    strict = '--strict' in argv
    files = [a for a in argv if a != '--strict'] or files_from_git()
    errors = sum(check(f, strict) for f in files)
    print(f'{len(files)} Dateien geprueft, {errors} Fehler')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
