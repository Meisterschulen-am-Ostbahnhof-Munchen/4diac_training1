#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Findet .SUB-Dateien im Projekt, die VT-Pool-Konstanten (Uebungen::const::UT::...)
aus MEHREREN VERSCHIEDENEN Pools importieren.

Entstanden aus einem konkreten Bug: InputOutputTesterButton_AI_Calibrate_3P_OPC_UA.SUB
importierte teils aus dem 2-Punkt-Pool (DefaultPool_AIC_Numeric) und teils aus dem
3-Punkt-Pool (DefaultPool_AIC_3P_Numeric) - ein Copy-Paste-Rest, der erst auffiel,
als die generierte GCF-Datei geloescht und ehrlich neu erzeugt wurde.

Namespace-Konvention (aus echten Beispielen abgeleitet):
    Uebungen::const::UT::<Kuerzel>::<GCF-Basisname>::<Konstante>
    oder (kein Kuerzel-Unterordner, GCF direkt unter UT/):
    Uebungen::const::UT::<GCF-Basisname>::<Konstante>

D.h. unabhaengig von der Tiefe: das VORLETZTE "::"-Segment ist immer der
GCF-Basisname (z.B. "DefaultPool_AIC_3P_Numeric"), das LETZTE Segment ist
immer der Konstantenname.

Pool-"Kernbezeichnung" (normalisierter Poolname) = GCF-Basisname MINUS ein
optionales, exakt am Ende stehendes "_Numeric"-Suffix. Beispiele (verifiziert
gegen Uebungen/const/UT/AIC/*.gcf):
    DefaultPool_AIC_Numeric     -> DefaultPool_AIC
    DefaultPool_AIC_3P_Numeric  -> DefaultPool_AIC_3P
    DefaultPool_AIC             -> DefaultPool_AIC   (unveraendert)
    DefaultPool_AIC_3P          -> DefaultPool_AIC_3P (unveraendert)
Andere Suffixe wie "_3P" werden NICHT abgeschnitten, weil sie tatsaechlich
unterschiedliche Uebungen/Pools kennzeichnen (DefaultPool_AIC vs.
DefaultPool_AIC_3P sind unterschiedliche "Kernbezeichnungen").

Zwei Signale werden berechnet:

  Signal A (breit): Kommen in EINER .SUB-Datei mehrere verschiedene
      normalisierte Poolnamen vor? ACHTUNG: das ist by-design haeufig, weil
      Varianten-Uebungen (z.B. "_3P") ueblicherweise weiterhin gemeinsame/
      Basis-Konstanten (RAW-Werte, Digitalausgaenge) aus dem Basispool
      importieren und nur die variantenspezifischen Objekte aus dem
      Varianten-Pool. Das ist meistens KEIN Bug, sondern Architektur.

  Signal B (eng, hohe Praezision): Kommen unter den *_Numeric-Importen EINER
      Datei zwei verschiedene *_Numeric-Rohpoolnamen vor? Das ist untypisch,
      weil numerische Objektpool-Konstanten (ID/Scale/Offset) innerhalb einer
      Uebung normalerweise konsistent aus EINEM Numeric-Pool kommen sollten.

Bekannte Einschraenkung (von Franz explizit vorgegeben, nicht loesbar mit
diesem Ansatz): Dieses Skript kann NUR erkennen, wenn eine Datei INTERN
inkonsistent ist (mehrere Pools gemischt). Wenn eine Uebung DURCHGAENGIG und
konsistent den falschen Pool importiert (z.B. eine 3P-Uebung nutzt
ausschliesslich einen 2P-Pool, ohne jede Mischung), sieht das Skript nichts
Auffaelliges - die Importliste wirkt intern "sauber". Das muss spaeter manuell
geprueft werden, z.B. indem man pro Uebungsverzeichnis den Namen der Uebung
mit dem Namen des tatsaechlich importierten Pools abgleicht.
"""

import re
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SEARCH_ROOT = PROJECT_ROOT / "Ventilsteuerung" / "4diacIDE-workspace"

IMPORT_RE = re.compile(r'<Import\s+declaration="([^"]+)"\s*/>')
# Matches the VT-pool constant convention: ...::const::UT::...::<Pool>::<Const>
UT_CONST_RE = re.compile(r'^(.*?)::const::UT::(.+)$')


def parse_import(decl):
    """
    Returns (kuerzel_path, pool_basename, constant_name) for a declaration
    string that follows the Uebungen::const::UT::... convention, or None if
    it doesn't match that convention at all.
    """
    m = UT_CONST_RE.match(decl)
    if not m:
        return None
    tail = m.group(2)  # everything after "::const::UT::"
    parts = tail.split("::")
    if len(parts) < 2:
        # Not enough segments to have both a pool basename and a constant
        return None
    pool_basename = parts[-2]
    constant_name = parts[-1]
    kuerzel_path = "::".join(parts[:-2])  # may be "" if no Kuerzel subfolder
    return kuerzel_path, pool_basename, constant_name


def normalize_pool(pool_basename):
    """Strip a single trailing '_Numeric' suffix to get the core pool name."""
    if pool_basename.endswith("_Numeric"):
        return pool_basename[: -len("_Numeric")]
    return pool_basename


def analyze_file(path):
    """
    Returns a dict with analysis results for one .SUB file, or None if the
    file has no Uebungen::const::UT::... imports at all.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"WARN: could not read {path}: {e}", file=sys.stderr)
        return None

    records = []  # list of (decl, kuerzel, pool_basename, normalized_pool, const_name)
    other_const_decls = []  # declarations containing '::const::' but not '::const::UT::'

    for m in IMPORT_RE.finditer(text):
        decl = m.group(1)
        parsed = parse_import(decl)
        if parsed is None:
            if "::const::" in decl:
                other_const_decls.append(decl)
            continue
        kuerzel_path, pool_basename, const_name = parsed
        norm_pool = normalize_pool(pool_basename)
        records.append((decl, kuerzel_path, pool_basename, norm_pool, const_name))

    if not records:
        return None

    norm_pool_counts = Counter(r[3] for r in records)
    raw_numeric_pool_counts = Counter(r[2] for r in records if r[2].endswith("_Numeric"))

    signal_a = len(norm_pool_counts) > 1
    signal_b = len(raw_numeric_pool_counts) > 1

    return {
        "path": path,
        "records": records,
        "other_const_decls": other_const_decls,
        "norm_pool_counts": norm_pool_counts,
        "raw_numeric_pool_counts": raw_numeric_pool_counts,
        "signal_a": signal_a,
        "signal_b": signal_b,
    }


def print_hit(result):
    path = result["path"]
    try:
        rel = path.relative_to(PROJECT_ROOT)
    except ValueError:
        rel = path
    print("=" * 100)
    print(f"DATEI: {rel}")
    print(f"  Normalisierte Pool-Namen (Signal A): {dict(result['norm_pool_counts'])}")
    if result["signal_b"]:
        print(f"  ACHTUNG Signal B (gemischte *_Numeric-Rohpools): "
              f"{dict(result['raw_numeric_pool_counts'])}")

    majority_pool, _ = result["norm_pool_counts"].most_common(1)[0]
    print(f"  Mehrheits-Pool (normalisiert): {majority_pool}")
    print("  Abweichende Import-Zeilen (nicht der Mehrheits-Pool):")
    for decl, kuerzel, pool_basename, norm_pool, const_name in result["records"]:
        if norm_pool != majority_pool:
            print(f"    - [{norm_pool}] {const_name}  <=  {decl}")

    if result["signal_b"]:
        minority_numeric_pools = [
            p for p, c in result["raw_numeric_pool_counts"].items()
            if c != result["raw_numeric_pool_counts"].most_common(1)[0][1]
        ]
        if not minority_numeric_pools:
            minority_numeric_pools = list(result["raw_numeric_pool_counts"].keys())[1:]
        print("  Konkrete *_Numeric-Konflikt-Zeilen:")
        for decl, kuerzel, pool_basename, norm_pool, const_name in result["records"]:
            if pool_basename in minority_numeric_pools:
                print(f"    - [{pool_basename}] {const_name}  <=  {decl}")
    print()


def main():
    if not SEARCH_ROOT.exists():
        print(f"FEHLER: {SEARCH_ROOT} existiert nicht.", file=sys.stderr)
        sys.exit(1)

    sub_files = sorted(SEARCH_ROOT.rglob("*.SUB"))
    print(f"Gefundene .SUB-Dateien insgesamt: {len(sub_files)}\n")

    signal_a_hits = []
    signal_b_hits = []
    files_with_ut_imports = 0

    for path in sub_files:
        result = analyze_file(path)
        if result is None:
            continue
        files_with_ut_imports += 1
        if result["signal_a"]:
            signal_a_hits.append(result)
        if result["signal_b"]:
            signal_b_hits.append(result)

    print(f"Dateien mit Uebungen::const::UT::-Importen: {files_with_ut_imports}")
    print(f"Signal A (>=2 verschiedene normalisierte Pools) Treffer: {len(signal_a_hits)}")
    print(f"Signal B (>=2 verschiedene *_Numeric-Rohpools) Treffer: {len(signal_b_hits)}")
    print()

    print("=" * 100)
    print("HIGH-CONFIDENCE TREFFER (Signal B: gemischte *_Numeric-Pools)")
    print("=" * 100)
    for r in signal_b_hits:
        print_hit(r)

    print("=" * 100)
    print("ALLE SIGNAL-A-TREFFER (breiter, inkl. vermutlich beabsichtigter Basis+Varianten-Mischungen)")
    print("=" * 100)
    for r in signal_a_hits:
        print_hit(r)

    print("=" * 100)
    print("EINSCHRAENKUNG: Dieses Skript findet nur INTERN gemischte Pool-Importe.")
    print("Eine Uebung, die DURCHGAENGIG und konsistent den falschen Pool importiert,")
    print("wird hier NICHT erkannt - das muss manuell geprueft werden (Uebungsname")
    print("gegen tatsaechlich importierten Pool abgleichen).")
    print("=" * 100)


if __name__ == "__main__":
    main()
