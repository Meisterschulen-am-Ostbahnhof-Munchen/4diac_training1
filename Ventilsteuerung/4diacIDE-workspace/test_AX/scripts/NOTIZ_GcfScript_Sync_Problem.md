# Notiz: `RunSkript_Workspace_DIDO_AX.bat` aktualisiert per Skript hinzugefügte Objekte nicht

Schmierzettel, damit das nicht vergessen wird. Betrifft potenziell auch Krauternter
(`G:\Geteilte Ablagen\Büngener Schuder GmbH\Krauternter Steuerung 2026`), wo dieselbe
Art von Tooling (`iop_to_xml.py`/`xml_to_iop.py`) benutzt wurde.

## Problem

`RunSkript_Workspace_DIDO_AX.bat` → `GcfScript.py` liest **nicht** aus `.iop`/`.xml`,
sondern aus:

- `DefaultPool.iop.h` (C-Header, `#define NAME WERT`-Zeilen)
- optional `DefaultPool.jop` (das eigentliche IsoDesigner/JetViewERS-Projekt, XML)

Beide werden normalerweise vom **echten** ISO-Designer-Tool (GUI) erzeugt, wenn dort
im Designer etwas hinzugefügt/gebaut wird.

Das Roundtrip-Tooling `iop_to_xml.py`/`xml_to_iop.py` kennt dagegen **nur** die
kompilierte Binärebene (`.iop`). Wird darüber ein neues Objekt hinzugefügt (Beispiel:
`OutputNumber_Tick`, ID 12020, für den System-Tick-Zähler), landet es zwar korrekt in
der `.iop`-Binärdatei, aber:

- **`.iop.h`** kennt das neue Objekt nicht (kein `#define ..._12020`).
- **`.jop`** (die eigentliche Projektquelle) kennt es ebenfalls nicht.

## Konsequenzen

1. Führt man `RunSkript_Workspace_DIDO_AX.bat` erneut aus, baut `GcfScript.py`
   `DefaultPool_DIDO.gcf` komplett neu aus `.iop.h` – die per Hand ergänzte
   Konstante (`OutputNumber_Tick`) geht dabei **stillschweigend wieder verloren**.
2. Öffnet man das Projekt im echten ISO-Designer-GUI, taucht das neue Objekt dort
   **nicht auf** – unsichtbar für die eigentliche Projektquelle.
3. Dasselbe Risiko besteht für jedes Objekt, das per Skript statt über die GUI in
   einen ISOBUS-Pool eingefügt wurde – auch bei Krauternter.

## Aktueller Stand (Stopgap)

Für `OutputNumber_Tick` wurde die Konstante direkt in
`Uebungen/const/UT/DIDO/DefaultPool_DIDO.gcf` ergänzt (nicht über `GcfScript.py`
generiert). Das reicht fürs Erste zum Weiterarbeiten, ist aber nicht dauerhaft
robust gegen einen erneuten Skriptlauf.

## Noch zu klären / offen

- Wie gehen wir mit künftigen per Skript hinzugefügten Objekten um, damit sie nicht
  beim nächsten `GcfScript.py`-Lauf verschwinden bzw. im GUI unsichtbar bleiben?
  Optionen (noch nicht entschieden):
  - `.iop.h` (und ggf. `.jop`) manuell mitpatchen (schneller Workaround, `.jop`
    bleibt aber weiterhin die GUI-Quelle-der-Wahrheit und ist dann inkonsistent).
  - Neue VT-Objekte künftig nur noch über den echten ISO-Designer anlegen, Skripte
    nur noch zum Lesen/Vergleichen/Diffen benutzen.
