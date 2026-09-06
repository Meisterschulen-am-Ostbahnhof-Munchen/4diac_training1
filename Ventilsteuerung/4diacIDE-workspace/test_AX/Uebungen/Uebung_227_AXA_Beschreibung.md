# Übung 227: Kombinierte Übung — Dreieck-Sollwertmarker + Split-Bargraph (AR-Adapter)

## Thema: mehrere VT-Anzeigen aus einer Sollwertquelle — durchgängig über AR-Adapter

Kombiniert [Übung 225b](Uebung_225b_AX_Beschreibung.md) (Dreieck-Sollwertmarker) und
[Übung 226b](Uebung_226b_AX_Beschreibung.md) (Split-Bargraph): **ein** Sollwert treibt **beide**
Anzeigen gleichzeitig. Anders als die beiden Einzelübungen läuft hier alles konsequent über
AR-Adapter-Bausteine (wie `225b_AXA`), da `226b_AX` seinen Sollwert bereits nur über den
AR-Adapter (`NumericValue_PHYSA`) liest — für eine gemeinsame Quelle müssen beide Verbraucher
denselben Verdrahtungsstil (Adapter) verwenden.

### Situationsbeschreibung
Derselbe Sollwert (`InputNumber_Sollwert`, VT-Objekt 9000, Bereich -42…+42) steuert gleichzeitig:
- das Dreieck (`Polygon_Bargraph_Mittelmarker`) im Container `Container_Sollwertmarker`,
- den Split-Bargraph (`Bargraph_Split_links`/`_rechts`),
- und schreibt wie bisher den Istwert (`NumberVariable_Istwert`) zurück.

### Funktionsbeschreibung
- **Sollwert lesen:** `Sollwert_N` (`NumericValue_PHYSA`) liest `NumberVariable_Sollwert_N`
  (VT-Objekt 21000 — die an `InputNumber_Sollwert` gebundene Variable, siehe
  [Übung 225 Beschreibung](Uebung_225_AX_Beschreibung.md) zur Begründung) und liefert den Wert als
  AR-Plug `rPhys`.
- **Verteilen:** `Split` (`AR_SPLIT_3`) verteilt diesen einen AR-Wert sauber auf drei Verbraucher
  (ein Adapter darf nicht direkt auf mehrere Ziele zeigen — siehe `iec61499-creator`-Skill,
  Regel 8).
- **Dreieck bewegen:** `Marker_Dreieck` (`PositionMarkerFSA`, `xScale := TRUE`) — mit Klammerung
  und `xOver`/`xUnder` als AX-Plugs.
- **Split-Bargraph ansteuern:** `SplitBar` (`BargraphSplitFS_AR`) — mit Klammerung und
  `xOverRight`/`xOverLeft` als AX-Plugs.
- **Istwert zurückschreiben:** `Istwert_N` (`Q_NumericValue_PHYSA`) schreibt denselben Wert auf
  `NumberVariable_Istwert` zurück (treibt `InputNumber_Istwert` und den bestehenden
  Einzel-Bargraph-Zeiger).
- Alles ausschließlich über `<AdapterConnections>` verdrahtet — keine einzige plain Event-/
  DataConnection nötig.

### Arbeitsauftrag
1. Legen Sie die SubApp `Uebung_227_AXA` an (bereits als Referenzlösung vorhanden).
2. Lesen Sie `NumberVariable_Sollwert_N` mit `NumericValue_PHYSA`.
3. Verteilen Sie den Wert mit `AR_SPLIT_3` auf drei Ziele.
4. Bewegen Sie das Dreieck mit `PositionMarkerFSA` (`stObj := Container_PositionMarker`,
   `xScale := TRUE`).
5. Steuern Sie den Split-Bargraph mit `BargraphSplitFS_AR`
   (`stObj := Bargraph_Split_BargraphSplit`).
6. Schreiben Sie den Istwert mit `Q_NumericValue_PHYSA` (`stObj := NumberVariable_Istwert_N`)
   zurück.
7. Am echten Terminal testen: Sollwert ändern → Dreieck folgt, Split-Bargraph füllt die passende
   Seite, Istwert-Feld und der bestehende Einzel-Bargraph-Zeiger zeigen denselben Wert.

### Referenzlösung
`Uebung_227_AXA.SUB` — validiert gegen `subapptype.xsd`. Verwendet ausschließlich bereits
bestehende Bausteine (`PositionMarkerFSA`, `BargraphSplitFS_AR`, `AR_SPLIT_3`) — keine neuen
Typen für diese Übung nötig.
