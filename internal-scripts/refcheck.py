"""Referenz-Check für 4diac-Typen, gemeinsam für sync_empty und sync_lib.

Ein Dateibaum ist ein dict {Pfad: Inhalt (bytes)}. type_index sammelt die
Typen (Paket::Name) und die Konstanten der .gcf; resolves prüft eine
Referenz (Type="..." oder <Import declaration="...">) dagegen.
"""
import collections
import re

TYPE_EXT = re.compile(r"\.(fbt|sub|adp|dtp|fct|gcf|atp)$", re.I)
REF_EXT = re.compile(r"\.(fbt|sub|sys|adp|fct)$", re.I)
RE_PKG = re.compile(rb'<CompilerInfo[^>]*packageName="([^"]*)"')
RE_NAME = re.compile(rb'<(?:FBType|SubAppType|AdapterType|DataType|GlobalConstants|FunctionType|AttributeDeclaration)\b[^>]*\bName="([^"]+)"')
RE_REF = re.compile(rb'\bType="([A-Za-z_]\w*(?:::\w+)+)"')
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


def refs(files, skip=lambda p: False):
    """Alle Referenzen -> Menge der Dateien, die sie enthalten."""
    out = collections.defaultdict(set)
    for p, c in files.items():
        if REF_EXT.search(p) and not skip(p):
            for r in set(RE_REF.findall(c)) | set(RE_IMP.findall(c)):
                out[r.decode()].add(p)
    return out


def check_refs(src, res):
    """Referenzen, die im Quellbaum auflösbar sind, im Ergebnis aber nicht mehr."""
    st, sc = type_index(src)
    rt, rc = type_index(res)
    broken = collections.defaultdict(set)
    for r, ps in refs(res).items():
        if not resolves(r, rt, rc) and resolves(r, st, sc):
            broken[r] |= ps
    return broken
