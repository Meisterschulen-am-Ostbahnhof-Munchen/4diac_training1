#!/usr/bin/env python3
"""Erzeugt den Inhalt von 4diac_training1_empty aus 4diac_training1.

Ablauf: Quellbaum (git ref) lesen -> exclude/keep -> preserve aus Ziel ->
Transformationen (DefaultPool*.gcf aus Workspace_Empty per GcfScript.py,
Skript-Pfade, Control in den .sys) -> Referenz-Check -> Diff gegen
Ziel-HEAD -> (optional) schreiben. Die Regeln stehen in empty_sync.toml.

Exit-Code 1, wenn im Ergebnis Typen oder Konstanten fehlen, die in
training1 noch aufloesbar sind.

  python sync_empty.py --source C:/git/ms-docs/4diac_training1 --target <empty-klon> [--apply]

Ohne --apply: reiner Trockenlauf, nichts wird geschrieben.
"""
import argparse, collections, io, re, subprocess, sys, tarfile, tempfile, tomllib
from pathlib import Path


# ---------------------------------------------------------------- git helpers
def git(repo, *args, binary=False):
    out = subprocess.run(["git", "-C", str(repo), *args], check=True,
                         capture_output=True).stdout
    return out if binary else out.decode("utf-8")


def read_tree(repo, ref):
    """{path: bytes} fuer alle Dateien von repo@ref (via git archive)."""
    data = git(repo, "archive", "--format=tar", ref, binary=True)
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        for m in tf:
            if m.isfile():
                files[m.name] = tf.extractfile(m).read()
    return files


def blob_ids(repo, ref):
    out = git(repo, "-c", "core.quotepath=off", "ls-tree", "-r", "-z", "--format=%(objectname) %(path)", ref)
    return {l.split(" ", 1)[1]: l.split(" ", 1)[0] for l in out.split("\0") if l}


def hash_blob(content):
    import hashlib
    return hashlib.sha1(b"blob %d\0" % len(content) + content).hexdigest()


# ---------------------------------------------------------------- globbing
def glob_re(pat):
    i, out = 0, ""
    while i < len(pat):
        c = pat[i]
        if pat.startswith("**/", i):
            out += "(?:.*/)?"; i += 3; continue
        if pat.startswith("**", i):
            out += ".*"; i += 2; continue
        if c == "*": out += "[^/]*"
        elif c == "?": out += "[^/]"
        elif c == "{":
            j = pat.index("}", i)
            out += "(?:" + "|".join(re.escape(x) for x in pat[i + 1:j].split(",")) + ")"
            i = j
        else: out += re.escape(c)
        i += 1
    return re.compile(out + r"\Z")


class Matcher:
    def __init__(self, pats):
        self.pats = [(p, glob_re(p)) for p in pats]

    def hit(self, path):
        for p, r in self.pats:
            if r.match(path):
                return p
        return None


# ---------------------------------------------------------------- transforms
def t_sys_control(files, rules, log):
    for rule in rules:
        m = Matcher([rule["glob"]])
        pat = re.compile(r'(<SubApp Name="%s" Type=")([^"]+)(")' % re.escape(rule["subapp"]))
        for p in list(files):
            if m.hit(p):
                txt = files[p].decode("utf-8")
                new, n = pat.subn(lambda mo: mo.group(1) + rule["type"] + mo.group(3), txt)
                if n and new != txt:
                    old = pat.search(txt).group(2)
                    log.append(f"sys_control: {p}: {old} -> {rule['type']}")
                    files[p] = new.encode("utf-8")


def t_script_prune(files, removed, cfg, log):
    removed_names = {Path(p).name for p in removed}
    m = Matcher(cfg["globs"])
    for p in list(files):
        if not m.hit(p):
            continue
        lines = files[p].decode("utf-8").splitlines(keepends=True)
        out, drop_next_if = [], False
        for ln in lines:
            if drop_next_if and re.match(r"\s*if errorlevel", ln, re.I):
                drop_next_if = False; continue
            drop_next_if = False
            toks = set(re.findall(r"[\w.\-]+\.(?:bat|sh)", ln))
            if toks & removed_names and re.search(r"\b(call|bash|sh|\./|start)\b|^\s*[\w.\-]+\.(bat|sh)", ln):
                log.append(f"script_prune: {p}: - {ln.strip()}")
                drop_next_if = True; continue
            out.append(ln)
        files[p] = "".join(out).encode("utf-8")


def t_replace(files, rules, log):
    """Text ersetzen, z. B. Pool-Pfade in Build-Skripten."""
    for rule in rules:
        m = Matcher(rule["globs"])
        for p in list(files):
            if not m.hit(p):
                continue
            txt = files[p].decode("utf-8", errors="surrogateescape")
            new = txt
            for old, repl in rule["pairs"]:
                new = new.replace(old, repl)
            if new != txt:
                log.append(f"replace: {p}")
                files[p] = new.encode("utf-8", errors="surrogateescape")


def t_gcf(files, src, rules, log):
    """DefaultPool*.gcf mit GcfScript.py aus dem Pool der Quelle neu erzeugen."""
    for rule in rules:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            pool_pre = rule["pool"].rstrip("/") + "/"
            if not any(p.startswith(pool_pre) for p in src):
                raise SystemExit(f"Pool {rule['pool']} fehlt in der Quelle (Tag zu alt?)")
            for p, c in src.items():
                if p.startswith(pool_pre) or p.startswith(rule["scripts"].rstrip("/") + "/"):
                    f = tmp / "src" / p
                    f.parent.mkdir(parents=True, exist_ok=True)
                    f.write_bytes(c)
            pool = tmp / "src" / rule["pool"]
            out = tmp / "out"
            out.mkdir()
            cmd = [sys.executable, "-I", str(tmp / "src" / rule["scripts"] / "GcfScript.py"),
                   "--oldfile", str(pool / "Output" / (rule["newfile"] + ".iop.h")),
                   "--newfolder", str(out) + "/", "--newfile", rule["newfile"],
                   "--package", rule["package"], "--jopfile", str(pool / (rule["newfile"] + ".jop"))]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode:
                raise SystemExit("GcfScript fehlgeschlagen:\n" + r.stdout + "\n" + r.stderr)
            gen = sorted(out.glob("*.gcf"))
            if not gen:
                raise SystemExit("GcfScript hat keine .gcf erzeugt")
            for g in gen:
                for d in rule["to"]:
                    dst = d.rstrip("/") + "/" + g.name
                    content = g.read_bytes()
                    if files.get(dst) != content:
                        log.append(f"gcf: {g.name} -> {dst}")
                    files[dst] = content


# ---------------------------------------------------------------- reference check
TYPE_EXT = re.compile(r"\.(fbt|sub|adp|dtp|fct|gcf|atp)$", re.I)
RE_PKG = re.compile(rb'<CompilerInfo[^>]*packageName="([^"]*)"')
RE_NAME = re.compile(rb'<(?:FBType|SubAppType|AdapterType|DataType|GlobalConstants|FunctionType|AttributeDeclaration)\b[^>]*\bName="([^"]+)"')
RE_REF = re.compile(rb'\bType="([A-Za-z_][\w]*(?:::[\w]+)+)"')
RE_IMP = re.compile(rb'<Import declaration="([^"]+)"')
RE_CONST = re.compile(rb'<VarDeclaration\b[^>]*\bName="([^"]+)"')


def type_index(files):
    types, consts = {}, {}
    for p, c in files.items():
        if not TYPE_EXT.search(p):
            continue
        n = RE_NAME.search(c)
        if not n:
            continue
        pk = RE_PKG.search(c)
        fq = ((pk.group(1) + b"::") if pk and pk.group(1) else b"") + n.group(1)
        types[fq.decode()] = p
        if p.lower().endswith(".gcf"):
            consts[fq.decode()] = {x.decode() for x in RE_CONST.findall(c)}
    return types, consts


def resolves(ref, types, consts):
    if ref in types:
        return True
    if ref.endswith("::*"):
        pre = ref[:-1]
        return any(t.startswith(pre) for t in types)
    head, _, last = ref.rpartition("::")
    return head in consts and last in consts[head]


def check_refs(src, res):
    """Referenzen, die im Quellbaum aufloesbar sind, im Ergebnis aber nicht mehr."""
    st, sc = type_index(src)
    rt, rc = type_index(res)
    broken = collections.defaultdict(set)
    for p, c in res.items():
        if not re.search(r"\.(fbt|sub|sys|adp|fct)$", p, re.I):
            continue
        for r in set(RE_REF.findall(c)) | set(RE_IMP.findall(c)):
            r = r.decode()
            if not resolves(r, rt, rc) and resolves(r, st, sc):
                broken[r].add(p)
    return broken


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--config", default=str(Path(__file__).with_name("empty_sync.toml")))
    ap.add_argument("--ref")
    ap.add_argument("--apply", action="store_true", help="Ergebnis in Ziel-Worktree schreiben")
    ap.add_argument("--report", help="Report-Datei (Markdown)")
    a = ap.parse_args()
    cfg = tomllib.loads(Path(a.config).read_text(encoding="utf-8"))
    ref = a.ref or cfg["source"]["ref"]
    if ref == "latest-tag":   # neuester Release-Tag von training1
        ref = git(a.source, "tag", "--sort=-creatordate").split()[0]
        print(f"Quelle: neuester Tag {ref}")
    tgt_ref = cfg["target"]["branch"]

    src = read_tree(a.source, ref)
    tgt = read_tree(a.target, tgt_ref)
    log = []

    exc, keep = Matcher(cfg["filter"]["exclude"]), Matcher(cfg["filter"]["keep"])
    pres = Matcher(cfg.get("preserve", {}).get("paths", []) + cfg.get("preserve", {}).get("owned", []))
    res, removed, why = {}, set(), collections.Counter()
    for p, c in src.items():
        if pres.hit(p):
            continue
        hit = exc.hit(p)
        if hit and not keep.hit(p):
            removed.add(p); why[hit] += 1
            continue
        res[p] = c
    for p, c in tgt.items():           # empty-eigene Dateien
        if pres.hit(p):
            res[p] = c
    owned = Matcher(cfg.get("preserve", {}).get("owned", []))   # ganz dem empty-Repo: kein Fallback
    for p, c in src.items():           # preserve-Pfad im Ziel (noch) nicht vorhanden -> aus Quelle
        if pres.hit(p) and not owned.hit(p) and p not in res and not (exc.hit(p) and not keep.hit(p)):
            res[p] = c
            log.append(f"preserve-fallback (aus training1, im empty noch nicht vorhanden): {p}")
    for rule in cfg.get("transform", {}).get("copy", []):
        content = res.get(rule["from"], src.get(rule["from"]))   # auch aus ausgeschlossenen Quellen
        if content is None:
            raise SystemExit(f"copy: {rule['from']} fehlt in der Quelle")
        for to in rule["to"]:
            if res.get(to) != content:
                log.append(f"copy: {rule['from']} -> {to}")
            res[to] = content

    t_gcf(res, src, cfg.get("transform", {}).get("gcf", []), log)
    t_replace(res, cfg.get("transform", {}).get("replace", []), log)
    t_sys_control(res, cfg.get("transform", {}).get("sys_control", []), log)
    if "script_prune" in cfg.get("transform", {}):
        t_script_prune(res, removed, cfg["transform"]["script_prune"], log)

    broken = check_refs(src, res)

    # Diff gegen Ziel
    tids = blob_ids(a.target, tgt_ref)
    added = sorted(p for p in res if p not in tids)
    deleted = sorted(p for p in tids if p not in res)
    changed = sorted(p for p in res if p in tids and hash_blob(res[p]) != tids[p])
    same = len(res) - len(added) - len(changed)

    def grp(paths, depth=4):
        c = collections.Counter("/".join(p.split("/")[:depth]) for p in paths)
        return "\n".join(f"  {v:5}  {k}" for k, v in sorted(c.items(), key=lambda x: -x[1]))

    rep = [f"# Trockenlauf training1@{ref} -> empty@{tgt_ref}", "",
           f"Quelle: {len(src)} Dateien, ausgeschlossen: {len(removed)}, Ergebnis: {len(res)}",
           f"Ziel heute: {len(tids)} Dateien", "",
           f"identisch: {same}  neu: {len(added)}  geaendert: {len(changed)}  geloescht: {len(deleted)}", "",
           "## Ausschluss je Regel", *[f"  {v:5}  {k}" for k, v in why.most_common()], "",
           "## Transformationen", *["  " + l for l in log], "",
           "## Neu (nach Ordner)", grp(added), "", "## Geaendert (nach Ordner)", grp(changed), "",
           "## Geloescht (nach Ordner)", grp(deleted), "",
           f"## Durch Filter kaputte Referenzen ({len(broken)})"]
    for r, ps in sorted(broken.items()):
        rep.append(f"  {r}  <- {len(ps)}x, z.B. {sorted(ps)[0]}")
    text = "\n".join(rep)
    print(text)
    if a.report:
        Path(a.report).write_text(text + "\n\n## Alle Loeschungen\n" + "\n".join(deleted)
                                  + "\n\n## Alle geaenderten\n" + "\n".join(changed), encoding="utf-8")

    if a.apply:
        root = Path(a.target)
        for p in deleted:
            (root / p).unlink(missing_ok=True)
        # leer gewordene Ordner entfernen (Git kennt keine Ordner, die IDE schon)
        for d in sorted({(root / p).parent for p in deleted}, key=lambda x: -len(x.parts)):
            while d != root and d.is_dir() and not any(d.iterdir()):
                d.rmdir()
                d = d.parent
        for p in added + changed:
            f = root / p
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(res[p])
        print(f"\n{len(added) + len(changed)} geschrieben, {len(deleted)} geloescht in {root}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
