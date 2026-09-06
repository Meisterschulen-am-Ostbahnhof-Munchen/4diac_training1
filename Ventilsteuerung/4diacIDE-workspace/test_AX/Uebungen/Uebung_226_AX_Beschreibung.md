# Übung 226: Split-Bargraph

## Thema: Virtual-Terminal-Bargraphen (ISO 11783-6 Annex B.11.3) — vorzeichenbehafteter Ausschlag über zwei Balken

### Situationsbeschreibung
Im ISO-Designer-Pool `Workspace_Dreieck` liegen zwei Linear-Bargraphen (`Bargraph_Split_links`,
`Bargraph_Split_rechts`, VT-Objekte 18001/18002) unmittelbar nebeneinander — eine
Darstellungsvariante, wie sie in echten Produktions-Pools für Signalgrößen mit Nulllage in der Mitte
verwendet wird (dort mit anderen, kundenspezifischen Objektnamen; siehe `iso-designer-jop`-Skill zur
allgemeinen Bargraph-Konfiguration). Jeder Balken zeigt `Min=0`/`Max=42` an. Zusammen bilden sie einen
gemeinsamen, vorzeichenbehafteten Balken von **-42 bis +42**: bei positivem Wert füllt sich der rechte
Balken von der Mitte nach außen, bei negativem Wert der linke, der jeweils andere bleibt bei 0. Der
Bediener gibt über `InputNumber_Sollwert` (VT-Objekt 9000) einen Wert zwischen -42 und +42 ein.

### Funktionsbeschreibung
- **Sollwert lesen:** Ändert der Bediener `InputNumber_Sollwert`, liefert das VT den physikalischen
  Wert als `REAL`.
- **Split-Bargraph ansteuern:** übernimmt der wiederverwendbare Baustein `BargraphSplitFS`
  (`isobus::UT::Q`) — er klammert den positiven Anteil des Werts auf `[0, r32MaxMagnitude]` und
  schreibt ihn auf den rechten Balken; parallel negiert er den Wert (`F_MUL` mit `-1.0`), klammert
  das Ergebnis genauso und schreibt es auf den linken Balken. Ist der Sollwert positiv, bleibt der
  linke Balken bei 0 (geklammert), und umgekehrt — das ist der normale Ruhezustand der jeweils
  inaktiven Seite, keine Fehlerbedingung. Beide Seiten schreiben direkt auf ihre Bargraph-Objekt-ID
  per **Command Numeric Value** (ISO 11783-6 Annex F.22, wie `Q_NumericValue_PHYS` es bereits für
  einzelne Zahlenfelder tut) — ohne gebundene `NumberVariable`. Balken-IDs und der gemeinsame
  Magnitudenbereich kommen gebündelt aus **einer** Konstante (`Bargraph_Split_BargraphSplit`, Typ
  `BargraphSplit_S`), die `GcfScript.py` automatisch aus der `.jop`-Geometrie erzeugt (zwei
  Bargraph-Objektnamen mit gemeinsamem Präfix, endend auf `_links`/`_rechts`).
- **Wichtig:** `xOverRight`/`xOverLeft` melden nur, wenn der Betrag des Sollwerts
  `r32MaxMagnitude` (42) tatsächlich überschreitet — es gibt bewusst **keine** `xUnder`-Ausgänge,
  da "Betrag unterhalb 0" auf der gerade inaktiven Seite im Normalbetrieb ständig zutrifft und damit
  keine Diagnoseinformation wäre (anders als bei `PositionMarkerFS`, wo Rand-Werte selten sind).

### Arbeitsauftrag
1. Legen Sie die SubApp `Uebung_226_AX` an (bereits als Referenzlösung vorhanden).
2. Lesen Sie `InputNumber_Sollwert` (VT-Objekt 9000) mit einer `NumericValue_PHYS`-Instanz
   (`stObj := NumberVariable_Sollwert_N` aus `DefaultPool_Dreieck_Numeric.gcf`) — das VT meldet
   Wertänderungen eines an eine `NumberVariable` gebundenen Eingabefelds unter der Objekt-ID der
   Variable (hier `NumberVariable_Sollwert`, 21000), nicht unter der ID des Eingabefelds selbst
   (9000).
3. Steuern Sie den Split-Bargraph mit einer `BargraphSplitFS`-Instanz
   (`stObj := Bargraph_Split_BargraphSplit` aus `DefaultPool_Dreieck_BargraphSplit.gcf`, `rValue :=`
   der physikalische Sollwert aus Schritt 2).
4. Am echten Terminal testen: Sollwert positiv → rechter Balken füllt sich, linker bleibt leer;
   Sollwert negativ → umgekehrt; `xOverRight`/`xOverLeft` bleiben `FALSE` solange `|Sollwert| <= 42`.

### Referenzlösung
`Uebung_226_AX.SUB` — validiert gegen `subapptype.xsd` (siehe `iec61499-creator`-Skill). Der
wiederverwendbare Baustein liegt in
`Ventilsteuerung\4diacIDE-workspace\.lib\isobus-3.0.0\typelib\UT\Q\BargraphSplitFS.fbt`
(Struct `isobus::utils::bargraph::BargraphSplit_S`, Klammer-Hilfsbaustein
`logiBUS::signalprocessing::clamp::F_ClampReal`).
