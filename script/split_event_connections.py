#!/usr/bin/env python3
"""
Split multi-target EventConnections in 4diac .SUB files by inserting
E_SPLIT_N blocks. Fixes 4diac validation warnings of type
"Multiple output connections on event may lead to undefined execution order".

Strategy:
  - Parse <SubAppType> files
  - For every <EventConnections> block, group <Connection> elements by
    (Source, source-event-port) and identify sources that fan-out to > 1
    destination events.
  - For each such source, insert a single E_SPLIT_N FB (N = fan-out count,
    capped at available 2..4 by chaining) and rewire the destinations to
    E_SPLIT_N.EO1..EON.
  - Preserve indentation, dx1/dx2, and source-side connections.
  - Do NOT touch DataConnections / AdapterConnections.
  - Skip connections whose source is a SubAppEventOutput (e.g. "CNF_1")
    when used at top-level -- they cannot be redirected through an FB
    port. These are reported only.
  - Idempotent: if a source already feeds an E_SPLIT_N, leave it alone.

Usage:
    python script/split_event_connections.py [--apply] [--root PATH]

Default is dry-run (prints planned changes, writes nothing). Use --apply
to overwrite files.
"""
from __future__ import annotations

import argparse
import collections
import os
import re
import sys
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple

NS_4DIAC = "iec61499::events"
MAX_SPLIT = 4  # E_SPLIT_2 .. E_SPLIT_4 available; >4 chains E_SPLIT_4

# ---------------- IO helpers ----------------

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_text(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)

# Indent: 4diac uses tabs for top-level and 2 spaces for nested. We use
# string-level rewriting instead of ET serialization to keep formatting.
INDENT_FB = "\t\t"      # <FB ...> inside <SubAppNetwork>
INDENT_CONN = "\t\t\t"  # <Connection ...> inside <EventConnections>

# ---------------- Analysis ----------------

def find_subapp_blocks(text: str) -> List[Tuple[int, int, str]]:
    """Return (start, end, name) of every <SubAppType ...>...</SubAppType>."""
    out = []
    for m in re.finditer(r"<SubAppType\b[^>]*>", text):
        start = m.start()
        # match closing tag with possible whitespace/newline
        end_m = re.search(r"</SubAppType\s*>", text[m.end():])
        if not end_m:
            continue
        end = m.end() + end_m.end()
        name_m = re.search(r'Name="([^"]+)"', text[m.start():m.end()])
        out.append((start, end, name_m.group(1) if name_m else "?"))
    return out

def find_event_connections_block(text: str, start: int, end: int):
    """Return (block_start, block_end, inner_connections) for the first
    <EventConnections>...</EventConnections> within text[start:end]."""
    m = re.search(r"<EventConnections\b[^>]*>", text[start:end])
    if not m:
        return None
    bs = start + m.start()
    be_m = re.search(r"</EventConnections\s*>", text[start + m.end():])
    if not be_m:
        return None
    be = start + m.end() + be_m.end()
    return bs, be, text[start + m.end():start + m.end() + be_m.start()]

CONN_RE = re.compile(
    r'<Connection\s+Source="([^"]+)"\s+Destination="([^"]+)"([^/>]*)/?>'
)

def split_source_dest(source: str) -> Tuple[str, str]:
    if "." in source:
        a, b = source.rsplit(".", 1)
        return a, b
    return source, ""

def parse_event_conns(inner: str) -> List[Tuple[str, str, str, str]]:
    """Return list of (source, dest, attrs, raw_line) tuples preserving
    original ordering and per-connection attribute strings (dx1 etc.)."""
    out = []
    # include the line indent too so we can preserve it
    for m in re.finditer(r"(?P<lead>^[ \t]*)<Connection\s+Source=\"(?P<s>[^\"]+)\"\s+Destination=\"(?P<d>[^\"]+)\"(?P<attrs>[^/>]*)/?>",
                         inner, flags=re.MULTILINE):
        out.append((m.group("s"), m.group("d"), m.group("attrs").strip(), m.group(0)))
    return out

def detect_top_level_subapp_outputs(text: str) -> set:
    """SubAppEventOutputs declared in <SubAppInterfaceList> are top-level
    events. Their names appear as Sources in EventConnections; they cannot
    be rewired through a child FB port. Return set of those names."""
    names = set()
    m = re.search(r"<SubAppEventOutputs\b[^>]*>(.*?)</SubAppEventOutputs\s*>",
                  text, flags=re.DOTALL)
    if m:
        for em in re.finditer(r'<SubAppEvent\s+Name="([^"]+)"', m.group(1)):
            names.add(em.group(1))
    return names

# ---------------- Re-write ----------------

def group_by_source(conns) -> Dict[Tuple[str, str], List[int]]:
    g = collections.defaultdict(list)
    for i, (s, _d, _a, _raw) in enumerate(conns):
        g[split_source_dest(s)].append(i)
    return g

def build_split_chain(existing_fb_names: set, n: int) -> Tuple[List[Tuple[str, str, int, int]], int]:
    """Build a list of E_SPLIT blocks whose combined fan-out == n.
    Each entry: (instance_name, type, fan_out_of_this_block, x)."""
    blocks = []
    remaining = n
    x = -7600
    while remaining > 1:
        k = min(remaining, MAX_SPLIT)
        bname_base = "E_SPLIT_2" if k == 2 else f"E_SPLIT_{k}"
        bname = bname_base
        suffix = 1
        while bname in existing_fb_names:
            suffix += 1
            bname = f"{bname_base}_{suffix}"
        btype = f"{NS_4DIAC}::{bname_base}"
        existing_fb_names.add(bname)
        blocks.append((bname, btype, k, x))
        x += 1000
        remaining -= (k - 1)  # EI absorbs 1 input; we still need remaining-1 outputs
    return blocks, remaining

def process_subapp_text(subapp_text: str) -> Tuple[str, int]:
    """Return (new_subapp_text, num_splits_inserted)."""
    subapp_outputs = detect_top_level_subapp_outputs(subapp_text)
    m = re.search(r"<EventConnections\b[^>]*>", subapp_text)
    if not m:
        return subapp_text, 0
    block_start = m.start()
    inner_start = m.end()
    end_m = re.search(r"</EventConnections\s*>", subapp_text[inner_start:])
    if not end_m:
        return subapp_text, 0
    # block_end points just AFTER the closing '>' of </EventConnections>
    block_end = inner_start + end_m.end()
    inner = subapp_text[inner_start:inner_start + end_m.start()]

    conns = parse_event_conns(inner)
    if not conns:
        return subapp_text, 0

    # Existing FB instance names in subapp
    fb_names = set(re.findall(r'<FB\s+Name="([^"]+)"', subapp_text))

    by_src = group_by_source(conns)
    plan: List[dict] = []
    # plan entry: { "src": (fb, port), "dests": [orig_conn_indices...],
    #               "chain": [(bname, btype, k, x), ...] }

    for (fbname, port), idxs in by_src.items():
        if len(idxs) <= 1:
            continue
        if fbname in subapp_outputs:
            print(f"  ! skip: source '{fbname}' is SubAppEventOutput")
            continue
        # If the source already feeds an existing E_SPLIT_N, skip
        targets = [conns[i][1] for i in idxs]
        if any(t.endswith(".EI") and t.split(".")[0].startswith("E_SPLIT") for t in targets):
            continue
        chain, leftover = build_split_chain(fb_names, len(idxs))
        plan.append({"src": (fbname, port), "idxs": idxs, "chain": chain})

    if not plan:
        return subapp_text, 0

    # Mutate conns in-place: build new ordered list
    new_conns: List[Tuple[str, str, str, str]] = []
    # Track which original indices we've consumed
    consumed: set = set()
    for p in plan:
        idxs = p["idxs"]
        chain = p["chain"]
        # The first connection's *source* feeds the chain's input. All
        # idxs (including idxs[0]) are rewritten to originate from chain
        # EOs so the original destinations remain connected.
        first_idx = idxs[0]
        orig_src, _dst, attrs, raw = conns[first_idx]
        new_conns.append((orig_src, f"{chain[0][0]}.EI", attrs, raw))
        # Build flat list of available EOs from the chain
        flat_eos: List[str] = []
        for (bname, _btype, k, _bx) in chain:
            for n in range(1, k + 1):
                flat_eos.append(f"{bname}.EO{n}")
        # We need len(idxs) outputs in the chain. flat_eos has sum(k)
        # entries which is >= len(idxs). Use the first len(idxs) EOs.
        eo_iter = iter(flat_eos[:len(idxs)])
        for ci in idxs:
            s, d, attrs2, raw2 = conns[ci]
            try:
                eo = next(eo_iter)
            except StopIteration:
                eo = f"{chain[-1][0]}.EO{chain[-1][2]}"
            new_conns.append((eo, d, attrs2, raw2))
            consumed.add(ci)
        # Internal chain connections (chain[j].EO_last -> chain[j+1].EI)
        for j in range(1, len(chain)):
            prev = chain[j - 1]
            cur = chain[j]
            new_conns.append((f"{prev[0]}.EO{prev[2]}", f"{cur[0]}.EI", "", ""))

    # Add unchanged conns
    for i, c in enumerate(conns):
        if i not in consumed:
            new_conns.append(c)

    # Re-render inner
    rendered = []
    for (s, d, attrs, _raw) in new_conns:
        attr_str = (" " + attrs) if attrs else ""
        rendered.append(f'{INDENT_CONN}<Connection Source="{s}" Destination="{d}"{attr_str}/>')
    new_inner = "\n" + "\n".join(rendered) + "\n\t\t"

    # Build FB insertion text: insert new FBs right before <EventConnections>.
    # Match the 4diac style where the closing tag sits on its own line at
    # the same indent level as the opening tag.
    fb_lines = []
    for p in plan:
        for (bname, btype, k, bx) in p["chain"]:
            fb_lines.append(
                f'{INDENT_FB}<FB Name="{bname}" Type="{btype}" x="{bx}" y="700">'
            )
            fb_lines.append(f'{INDENT_FB}</FB>')
    fb_block = ("\n" + "\n".join(fb_lines)) if fb_lines else ""

    # Reassemble: keep everything before the opening <EventConnections> tag,
    # prepend any newly inserted FB instances, then place the rendered
    # <EventConnections> block (open tag + new_inner + close tag) and
    # finally the rest of the subapp.
    open_tag = subapp_text[block_start:inner_start]
    rest = subapp_text[inner_start + end_m.start():]   # from '<' of </EventConnections> onwards
    new_subapp = (subapp_text[:block_start]
                  + fb_block
                  + open_tag
                  + new_inner
                  + rest)

    # Add import for E_SPLIT types
    ci_m = re.search(r"<CompilerInfo\b[^>]*>", new_subapp)
    if ci_m and "iec61499::events::E_SPLIT" not in new_subapp:
        ci_end = new_subapp.find("</CompilerInfo", ci_m.end())
        insertion = '\n\t\t<Import declaration="iec61499::events::E_SPLIT_2"/>'
        # Add E_SPLIT_3/4 imports only if used
        used_kinds = set()
        for p in plan:
            for (_n, _t, k, _x) in p["chain"]:
                if k >= 3:
                    used_kinds.add(k)
        for k in sorted(used_kinds):
            insertion += f'\n\t\t<Import declaration="iec61499::events::E_SPLIT_{k}"/>'
        new_subapp = new_subapp[:ci_end] + insertion + new_subapp[ci_end:]

    return new_subapp, sum(len(p["chain"]) for p in plan)


def process_file(path: str, apply: bool) -> int:
    text = read_text(path)
    blocks = find_subapp_blocks(text)
    if not blocks:
        return 0
    total = 0
    # Process in reverse order to keep offsets valid
    new_text = text
    for start, end, name in reversed(blocks):
        sub = new_text[start:end]
        new_sub, n = process_subapp_text(sub)
        if n:
            print(f"  {os.path.basename(path)} :: {name}: +{n} E_SPLIT block(s)")
            new_text = new_text[:start] + new_sub + new_text[end:]
            total += n
    if apply and total:
        write_text(path, new_text)
    return total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Write changes to disk")
    ap.add_argument("--root", default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "Ventilsteuerung", "4diacIDE-workspace"))
    args = ap.parse_args()

    root = args.root
    if not os.path.isdir(root):
        print(f"workspace not found: {root}", file=sys.stderr)
        return 1

    files = []
    for dirpath, _dirs, fnames in os.walk(root):
        for fn in fnames:
            if fn.lower().endswith(".sub"):
                files.append(os.path.join(dirpath, fn))
    files.sort()

    grand_total = 0
    files_changed = 0
    for f in files:
        n = process_file(f, apply=args.apply)
        if n:
            grand_total += n
            files_changed += 1

    mode = "APPLIED" if args.apply else "DRY-RUN"
    print(f"\n[{mode}] {grand_total} E_SPLIT block(s) inserted across {files_changed} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
