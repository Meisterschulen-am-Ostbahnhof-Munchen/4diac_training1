#!/usr/bin/env python3
"""Überträgt den .lib-Stand (samt elf/) von 4diac_training1 in ein anderes 4diac-Projekt.

Ablauf: training1@<tag> lesen -> <ws>/.lib im Ziel komplett ersetzen (alte
Lib-Versionen fallen weg) -> optional das Minimum aus scripts_central und den
Release-Workflow dazu -> Referenz-Check des Projekts mit alter und neuer .lib
-> Diff gegen Ziel-HEAD -> (optional) schreiben. Regeln: lib_sync.toml.

Projektinhalte (.SUB, .sys, ...) werden nie verändert. Was mit der neuen .lib
nicht mehr auflösbar ist oder doppelt vorkommt, steht nur im Report.

  python sync_lib.py --source <training1> --target <ziel-klon> --repo 4diac_empty1 --ref v0.28m [--apply]

Ohne --apply: reiner Trockenlauf, nichts wird geschrieben.
"""
import argparse
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "lib_sync.toml"
REPORT = Path("report.md")   # fest, im Arbeitsverzeichnis
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "sync_empty"))
from refcheck import refs, resolves, type_index  # noqa: E402
from sync_empty import blob_ids, check_ref, hash_blob, inside, read_tree  # noqa: E402


def repo_cfg(cfg, name):
    for r in cfg["repo"]:
        if r["name"] == name:
            return r
    raise SystemExit(f"Repo {name!r} steht nicht in lib_sync.toml")


def build_result(src, tgt, cfg, rc):
    """Zielbaum nach dem Sync: .lib aus training1, optional Skripte und Workflow."""
    s_lib = cfg["source"]["workspace"].rstrip("/") + "/.lib/"
    t_lib = rc["workspace"].rstrip("/") + "/.lib/"
    res = {p: c for p, c in tgt.items() if not p.startswith(t_lib)}
    for p, c in src.items():
        if p.startswith(s_lib):
            res[t_lib + p[len(s_lib):]] = c
    if rc.get("scripts"):
        d = cfg["scripts"]["dir"].rstrip("/") + "/"
        for f in cfg["scripts"]["files"]:
            if d + f not in src:
                raise SystemExit(f"Skript fehlt in training1: {d + f}")
            res[d + f] = src[d + f]
    wf = cfg["target_workflow"]   # gehört zum Werkzeug, nicht zum Tag: aus diesem Checkout
    res[wf["to"]] = (HERE.parent.parent / wf["from"]).read_bytes()
    return res, t_lib


def project_check(tgt, res, t_lib):
    """Referenzen des Projekts (ohne .lib) mit alter und neuer .lib prüfen."""
    in_lib = lambda p: p.startswith(t_lib)  # noqa: E731
    ws = t_lib[:-len(".lib/")]
    proj_refs = refs({p: c for p, c in res.items() if p.startswith(ws)}, skip=in_lib)
    ot, oc = type_index({p: c for p, c in tgt.items() if p.startswith(ws)})
    nt, nc = type_index({p: c for p, c in res.items() if p.startswith(ws)})
    broken_old = {r for r in proj_refs if not resolves(r, ot, oc)}
    broken_new = {r for r in proj_refs if not resolves(r, nt, nc)}
    own = type_index({p: c for p, c in res.items() if p.startswith(ws) and not in_lib(p)})[0]
    lib_types = type_index({p: c for p, c in res.items() if in_lib(p)})[0]
    return {
        "neu kaputt": {r: proj_refs[r] for r in sorted(broken_new - broken_old)},
        "schon vorher fehlend": {r: proj_refs[r] for r in sorted(broken_new & broken_old)},
        "durch neue .lib aufgelöst": {r: proj_refs[r] for r in sorted(broken_old - broken_new)},
        "doppelt (Projekt und .lib)": {t: {own[t]} for t in sorted(own.keys() & lib_types.keys())},
    }


def report(name, ref, tids, res, checks):
    added = sorted(p for p in res if p not in tids)
    deleted = sorted(p for p in tids if p not in res)
    changed = sorted(p for p in res if p in tids and hash_blob(res[p]) != tids[p])
    rep = [f"# .lib-Sync training1@{ref} -> {name}", "",
           f"neu: {len(added)}  geändert: {len(changed)}  gelöscht: {len(deleted)}", ""]
    for title, items in checks.items():
        rep.append(f"## {title} ({len(items)})")
        rep += [f"  {r}  <- {len(ps)}x, z. B. {min(ps)}" for r, ps in items.items()]
        rep.append("")
    if checks["neu kaputt"] or checks["doppelt (Projekt und .lib)"]:
        rep.append("**Hinweis:** Die Stellen oben bitte von Hand in der IDE prüfen. Der Sync repariert nichts im Projekt.")
    return "\n".join(rep), added, changed, deleted


def write(target, res, added, changed, deleted):
    root = Path(target).resolve()
    for p in deleted:
        inside(root, p).unlink(missing_ok=True)
    for d in sorted({inside(root, p).parent for p in deleted}, key=lambda x: -len(x.parts)):
        while d != root and d.is_dir() and not any(d.iterdir()):
            d.rmdir()
            d = d.parent
    for p in added + changed:
        f = inside(root, p)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(res[p])
    print(f"\n{len(added) + len(changed)} geschrieben, {len(deleted)} gelöscht in {root}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="4diac_training1-Klon")
    ap.add_argument("--target", required=True, help="Klon des Ziel-Repos")
    ap.add_argument("--repo", required=True, help="Name wie in lib_sync.toml")
    ap.add_argument("--ref", required=True, help="Tag in training1, z. B. v0.28m")
    ap.add_argument("--apply", action="store_true", help="Ergebnis in den Ziel-Worktree schreiben")
    ap.add_argument("--report", action="store_true", help=f"Report zusätzlich nach {REPORT} schreiben")
    a = ap.parse_args()
    cfg = tomllib.loads(CONFIG.read_text(encoding="utf-8"))
    rc = repo_cfg(cfg, a.repo)
    ref = check_ref(a.ref)
    base = check_ref(rc.get("base", "main"))

    src = read_tree(a.source, ref)
    tgt = read_tree(a.target, base)
    res, t_lib = build_result(src, tgt, cfg, rc)
    checks = project_check(tgt, res, t_lib)
    text, added, changed, deleted = report(a.repo, ref, blob_ids(a.target, base), res, checks)
    print(text)
    if a.report:
        REPORT.write_text(text + "\n", encoding="utf-8")
    if a.apply:
        write(a.target, res, added, changed, deleted)
    return 0


if __name__ == "__main__":
    sys.exit(main())
