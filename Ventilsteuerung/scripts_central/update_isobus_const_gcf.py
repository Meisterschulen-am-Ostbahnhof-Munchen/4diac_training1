#!/usr/bin/env python3
# Copyright (c) 2026 Meisterschulen am Ostbahnhof
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0
"""Konstanten-GCFs von isobus_pgn aus dem isobus.net-Export aktualisieren.

Eingabe ist der CSV-Export von https://www.isobus.net/isobus/ ("Export" ->
CSV, ein Ordner mit "Manufacturer IDs.csv", "SPNs and PGNs.csv" usw.).

Vorgehen, damit bestehende Netze nicht brechen:
  * Name und Wert vorhandener Konstanten bleiben immer unveraendert,
  * der Kommentar wird aus dem Export neu geschrieben (XML und <OriginalSource>-
    Spiegel, eine kurze Zeile; von der IDE umgebrochene Zeilen fallen weg),
  * fehlende Werte werden als neue Konstante eingefuegt, in Wert-Reihenfolge,
  * umbenannte Eintraege werden gemeldet, mit Vorschlag fuer einen neuen Namen,
  * Werte, die im Export fehlen (gestrichen), werden gemeldet, bleiben aber,
  * Global_Source_Addresses.gcf wird neu angelegt, falls sie fehlt.

Ohne --apply laeuft nur ein Trockenlauf mit Bericht.

Aufruf:
  python update_isobus_const_gcf.py --csv "C:/Users/.../isoExport_csv" [--apply]
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
DEFAULT_CONST = HERE.parent / "4diacIDE-workspace/.lib/isobus_pgn-3.0.0/typelib/pgn/const"
COMMENT_MAX = 100 # kurz halten: lange Kommentare bricht die IDE um und liest sie falsch zurueck

LEGAL_SUFFIXES = {"INC", "LLC", "LTD", "CO", "CORP", "CORPORATION", "GMBH", "KG", "PTY"}


def clean(text: str) -> str:
    # _x000D_ = Zeilenumbruch aus dem Excel-Ursprung des Exports
    return " ".join(text.replace("_x000D_", " ").split()).rstrip(" -")


def short(text: str, limit: int = COMMENT_MAX) -> str:
    text = clean(text)  # leere Notes ergeben sonst ein "-" am Ende
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(" ,;-")


def ident(text: str) -> str:
    text = text.replace("&", " AND ")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9]+", "_", text.upper()).strip("_")


def manufacturer_ident(name: str) -> str:
    name = re.sub(r"\(.*?\)", " ", name)
    name = name.split(",")[0]
    parts = ident(name).split("_")
    while len(parts) > 1 and parts[-1] in LEGAL_SUFFIXES:
        parts.pop()
    return "_".join(parts)


@dataclass
class Entry:
    value: int
    name: str
    comment: str
    text: str  # Vergleichstext fuer "geaendert?"
    group: str = ""  # nur IG-Funktionen: Vehicle System, Funktionsnummern ab 128 gelten je System
    full: str = ""  # ungekuerzter Kommentar, fuer den Vergleich mit dem vorhandenen

    def __post_init__(self):
        self.full, self.comment = clean(self.comment), short(self.comment)


@dataclass
class Table:
    gcf: str
    csv: str
    typ: str
    entries: Callable[[list[dict]], list[Entry]]
    literal: Callable[[int], str] = str
    title: str = ""


def rows(csv_dir: Path, name: str) -> list[dict]:
    with open(csv_dir / f"{name}.csv", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def date10(r: dict, key: str) -> str:
    return (r.get(key) or "")[:10]


def e_manufacturer(rs):
    out = []
    for r in rs:
        loc = " ".join(r["location"].split())
        c = f"Manufacturer: {r['manufacturer']}" + (f" | Location: {loc}" if loc else "")
        c += f" - {date10(r, 'date_created_or_last_modified')}"
        out.append(Entry(int(r["value"]), "M_" + manufacturer_ident(r["manufacturer"]), c, r["manufacturer"]))
    return out


def e_pgn(rs):
    seen, out = set(), []
    for r in rs:
        if not r["pgn"].strip().isdigit() or int(r["pgn"]) in seen:
            continue
        p = int(r["pgn"])
        seen.add(p)
        c = f"< {p:05d} - {r['acronym'].strip() or r['parameter_group_label'].strip()}".rstrip(" -")
        out.append(Entry(p, "PGN_" + ident(r["parameter_group_label"]), c, r["acronym"].strip() or str(p)))
    return out


def e_global_function(rs):
    out = []
    for r in rs:
        if not r["function_description"].strip():
            continue  # leere Zeilen im Export (z. B. 95)
        c = f"Function: {r['function_description']} - {r['notes']}"
        out.append(Entry(int(r["function_id"]), "F_" + ident(r["function_description"]), c, r["function_description"]))
    return out


def e_ig_function(ig):
    def f(rs):
        out = []
        for r in rs:
            if r["industry_group_id"] != str(ig) or r["function_id"] == "255":
                continue  # 255 = not available, steht schon in Global_NAME_Functions
            system = r["vehicle_system_description"].split(" - ")[0].strip()
            c = f"Sys: {system}, Func: {r['function_description']} - {r['notes']}"
            name = "F_" + ident(system + " " + r["function_description"])
            out.append(Entry(int(r["function_id"]), name, c, r["function_description"], system.lower()))
        return out
    return f


def e_device_class(ig):
    def f(rs):
        out, seen = [], set()
        for r in rs:
            if r["industry_group_id"] != str(ig) or r["vehicle_system_id"] in seen:
                continue
            seen.add(r["vehicle_system_id"])
            desc = r["vehicle_system_description"]
            c = f"Device Class / Vehicle System: {desc}"
            out.append(Entry(int(r["vehicle_system_id"]), "DC_" + ident(desc.split(" - ")[0]), c,
                             desc.split(" - ")[0]))
        return out
    return f


def e_source_address(rs):
    out = []
    for r in rs:
        if not r["source_address_id"].strip().isdigit():
            continue
        c = f"Source Address: {r['name']} - {r['notes']}"
        sa = int(r["source_address_id"])
        # "thru 127 are reserved ..." = Beginn eines reservierten Bereichs, Namensmuster wie IG1/IG2
        low = r["name"].strip().lower()
        if low.startswith("thru"):
            kind = "RESERVED" if "reserved" in low + r["notes"].lower() else (
                "DYNAMIC" if "dynamic" in low + r["notes"].lower() else "RANGE")
            name = f"SA_{kind}_{sa}"
        else:
            name = "SA_" + ident(r["name"])
        out.append(Entry(sa, name, c, r["name"]))
    return out


TABLES = [
    Table("Manufacturer_IDs", "Manufacturer IDs", "UINT", e_manufacturer),
    Table("PgnDef", "SPNs and PGNs", "UDINT", e_pgn, lambda v: f"UDINT#16#{v:04X}"),
    Table("Global_NAME_Functions", "Global NAME Functions", "BYTE", e_global_function),
    *[Table(f"IG{i}_NAME_Functions", "IG Specific NAME Function", "BYTE", e_ig_function(i)) for i in range(1, 6)],
    *[Table(f"IG{i}_Device_Classes", "IG Specific NAME Function", "BYTE", e_device_class(i)) for i in range(1, 6)],
    *[Table(f"IG{i}_Source_Addresses", f"IG{i} Source Addresses", "BYTE", e_source_address) for i in range(1, 6)],
    Table("Global_Source_Addresses", "Global Source Addresses", "BYTE", e_source_address,
          title="Global source addresses (all industry groups)"),
]


def group_of(comment: str) -> str:
    m = re.match(r"Sys: (.*?)(?:, Func:| - |$)", comment)
    return m.group(1).strip().lower() if m else ""


def existing(path: Path):
    """Schluessel (Wert, Vehicle System) -> vorhandene VarDeclarations."""
    root = ET.parse(path).getroot()
    vals: dict[tuple[int, str], list[ET.Element]] = {}
    for v in root.iter("VarDeclaration"):
        iv = v.attrib.get("InitialValue", "")
        m = re.search(r"16#([0-9A-Fa-f]+)", iv)
        num = int(m.group(1), 16) if m else (int(iv) if iv.isdigit() else None)
        if num is not None:
            vals.setdefault((num, group_of(v.attrib.get("Comment", ""))), []).append(v)
    return vals


def same_comment(old: str, e: Entry) -> bool:
    """Gleich, wenn der vorhandene Kommentar nur anders gekuerzt ist als der Export-Text."""
    old, full = clean(old).lower(), clean(e.full or e.comment).lower()
    return old == e.comment.lower() or bool(old) and full.startswith(old.rstrip(" ,;-."))


def unique(name: str, value: int, taken: set[str]) -> str:
    if name in taken:
        name = f"{name}_{value}"
    taken.add(name)
    return name


def insert_sorted(lines: list[str], new_lines: dict[int, str], value_of: Callable[[str], int | None],
                  block: tuple[int, int], group: str = "") -> None:
    """Fuegt new_lines (Wert -> Zeile) nach der letzten Zeile mit kleinerem Wert ein
    (bei IG-Funktionen nur innerhalb desselben Vehicle Systems)."""
    start, end = block
    for value in sorted(new_lines, reverse=True):
        pos = start
        for i in range(start, end):
            v = value_of(lines[i])
            low = lines[i].lower()
            in_group = not group or f"sys: {group}," in low or f"sys: {group} -" in low
            if v is not None and v < value and in_group:
                pos = i + 1
                # Fortsetzungszeilen eines umgebrochenen Kommentars mitnehmen
                while pos < end and lines[pos].lstrip().startswith("//") and value_of(lines[pos]) is None:
                    pos += 1
        lines.insert(pos, new_lines[value])
        end += 1


def val_from(line: str) -> int | None:
    m = re.search(r'InitialValue="(?:UDINT#)?(16#)?([0-9A-Fa-f]+)"', line)
    if m:
        return int(m.group(2), 16 if m.group(1) else 10)
    m = re.search(r":\s*\w+\s*:=\s*(?:UDINT#)?(16#)?([0-9A-Fa-f]+);", line)
    if m:
        return int(m.group(2), 16 if m.group(1) else 10)
    return None


def update(t: Table, csv_dir: Path, const_dir: Path, apply: bool, report: list[str]) -> None:
    path = const_dir / f"{t.gcf}.gcf"
    want: dict[tuple[int, str], Entry] = {}
    for e in t.entries(rows(csv_dir, t.csv)):
        want.setdefault((e.value, e.group), e)
    if not path.exists():
        report.append(f"{t.gcf}: Datei fehlt, wird neu angelegt ({len(want)} Konstanten)")
        if apply:
            write_new(path, t, sorted(want.values(), key=lambda e: (e.group, e.value)))
        return
    have = existing(path)
    taken = {v.attrib["Name"] for vs in have.values() for v in vs}
    missing = [want[k] for k in sorted(set(want) - set(have))]
    def norm(x: str) -> str:
        return " ".join(x.split()).lower()
    def renamed(e: Entry, x: ET.Element) -> bool:
        # alter Name steht als "(formerly ...)" im Export: bleibt auch nach dem Kommentar-Update erkennbar
        core = x.attrib["Name"].split("_", 1)[-1]
        old = [manufacturer_ident(s) for s in re.findall(r"formerly ([^,;)]+)", e.text, re.I)]
        return core in old and core not in ident(e.text.split(" (")[0])
    changed = [want[k] for k in sorted(set(want) & set(have))
               if not any(norm(want[k].text.split(" (")[0])[:30] in norm(x.attrib.get("Comment", ""))
                          or ident(want[k].text) in x.attrib["Name"] for x in have[k])
               or any(renamed(want[k], x) for x in have[k])]
    # 255 = "not available" steht nicht (mehr) als Funktion im Export, ist aber gueltig
    removed = sorted(k for k in set(have) - set(want) if not (t.gcf.endswith("NAME_Functions") and k[0] == 255))
    recomment = [(v, want[k].comment) for k in sorted(set(want) & set(have)) for v in have[k]
                 if not same_comment(v.attrib.get("Comment", ""), want[k])]
    report.append(f"{t.gcf}: {len(have)} vorhanden, {len(missing)} fehlen, {len(changed)} umbenannt, "
                  f"{len(removed)} im Export gestrichen, {len(recomment)} Kommentare neu")
    for e in missing:
        e.name = unique(e.name, e.value, taken)
        report.append(f"   + {e.value}: {e.name}  ({e.text[:60]})")
    for e in changed:
        old = have[(e.value, e.group)][0]
        report.append(f"   ~ {e.value}: {old.attrib['Name']} -> laut Export jetzt '{' '.join(e.text.split())[:60]}'"
                      f", Vorschlag: {unique(e.name, e.value, set(taken))} (Name nicht geaendert)")
    for k in removed:
        names = ", ".join(v.attrib["Name"] for v in have[k])
        report.append(f"   - {k[0]}: {names}  (nicht mehr im Export, bleibt erhalten)")
    if not apply or not (missing or recomment):
        return
    lines = path.read_text(encoding="utf-8").split("\n")
    for v, c in recomment:
        set_comment(lines, v.attrib["Name"], c)
    for e in missing:
        xs = next(i for i, l in enumerate(lines) if l.strip() == "<GlobalConstants>") + 1
        xe = next(i for i, l in enumerate(lines) if l.strip() == "</GlobalConstants>")
        insert_sorted(lines, {e.value: xml_line(t, e)}, val_from, (xs, xe), e.group)
        ss = next(i for i, l in enumerate(lines) if "VAR_GLOBAL CONSTANT" in l) + 1
        # einige GCFs haben mehrere VAR_GLOBAL-Bloecke (je Vehicle System): bis zum letzten END_VAR
        se = max(i for i, l in enumerate(lines) if l.strip() == "END_VAR")
        insert_sorted(lines, {e.value: src_line(t, e)}, val_from, (ss, se), e.group)
    path.write_text("\n".join(lines), encoding="utf-8", newline="")
    ET.parse(path)


def attr(text: str) -> str:
    return '"' + escape(text, {'"': "&quot;"}) + '"'


def set_comment(lines: list[str], name: str, comment: str) -> None:
    """Kommentar einer vorhandenen Konstante ersetzen, im XML und im Quelltext-Spiegel.
    Fortsetzungszeilen eines von der IDE umgebrochenen Kommentars werden entfernt."""
    xml_re = re.compile(rf'(<VarDeclaration Name="{re.escape(name)}" [^>]*?Comment=)("[^"]*")')
    src_re = re.compile(rf"^(\s*{re.escape(name)}\s*:\s*\w+\s*:=[^;]*;)\s*(//.*)?$")
    for i, line in enumerate(lines):
        if xml_re.search(line):
            lines[i] = xml_re.sub(lambda m: m.group(1) + attr(comment), line, count=1)
            continue
        m = src_re.match(line)
        if not m:
            continue
        col = line.find("//")
        lines[i] = f"{m.group(1)} // {comment}"
        while col >= 0 and i + 1 < len(lines) and lines[i + 1].find("//") == col \
                and not lines[i + 1][:col].strip():
            del lines[i + 1]
        return


def xml_line(t: Table, e: Entry) -> str:
    return (f'\t\t<VarDeclaration Name="{e.name}" Type="{t.typ}" Comment={attr(e.comment)} '
            f'InitialValue="{t.literal(e.value)}"/>')


def src_line(t: Table, e: Entry) -> str:
    return f"\t\t{e.name} : {t.typ} := {t.literal(e.value)}; // {e.comment}"


def write_new(path: Path, t: Table, entries: list[Entry]) -> None:
    taken: set[str] = set()
    for e in entries:
        e.name = unique(e.name, e.value, taken)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           f'<GlobalConstants Name="{t.gcf}" Comment={attr(t.title)}>',
           '\t<Identification Standard="61499-1">', "\t</Identification>",
           '\t<VersionInfo Organization="Meisterschulen am Ostbahnhof" Version="1.0" Author="Franz Höpfinger" '
           'Date="2026-11-14" Remarks="erzeugt mit scripts_central/update_isobus_const_gcf.py">',
           "\t</VersionInfo>",
           '\t<CompilerInfo packageName="isobus::pgn::const">', "\t</CompilerInfo>", "\t<GlobalConstants>"]
    out += [xml_line(t, e) for e in entries]
    out += ["\t</GlobalConstants>", "\t<OriginalSource><![CDATA[PACKAGE isobus::pgn::const;", "",
            f"// {escape(t.title)}", f"GLOBALCONSTANTS {t.gcf}", "\tVAR_GLOBAL CONSTANT"]
    out += [src_line(t, e) for e in entries]
    out += ["\tEND_VAR", "END_GLOBALCONSTANTS", "]]></OriginalSource>",
            "\t<Attribute Name=\"eclipse4diac::core::TypeHash\" Value=\"''\"/>", "</GlobalConstants>", ""]
    path.write_text("\n".join(out), encoding="utf-8", newline="")
    ET.parse(path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", required=True, type=Path, help="Ordner mit dem CSV-Export von isobus.net")
    ap.add_argument("--const", type=Path, default=DEFAULT_CONST, help="Ordner pgn/const der Bibliothek isobus_pgn")
    ap.add_argument("--apply", action="store_true", help="GCFs schreiben (sonst nur Bericht)")
    a = ap.parse_args()
    report: list[str] = []
    for t in TABLES:
        update(t, a.csv, a.const, a.apply, report)
    print("\n".join(report))
    print("\n(Trockenlauf, nichts geschrieben)" if not a.apply else "\nGCFs geschrieben.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
