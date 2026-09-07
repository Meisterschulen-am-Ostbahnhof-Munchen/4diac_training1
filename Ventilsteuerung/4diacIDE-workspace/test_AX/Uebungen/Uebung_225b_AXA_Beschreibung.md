# Übung 225b AXA: Dreieck-Sollwertmarker mit AR-Adapter (PositionMarkerFS)

## Thema: Virtual-Terminal-Objektpositionierung — AR-Adapter-Variante

Adapter-Variante von [Übung 225b](Uebung_225b_AX_Beschreibung.md): identische Funktion, aber Sollwert-
Lesen und Istwert-Schreiben laufen über die AR-Adapter-Bausteine (`NumericValue_PHYSA`/
`Q_NumericValue_PHYSA`) statt über plain `REQ`/`IND`-Events. Die Dreieck-Bewegung nutzt weiterhin den
wiederverwendbaren `PositionMarkerFS` — inklusive Klammern und `xOver`/`xUnder` — passend zu 225b.

### Warum ein neuer Baustein nötig war
`PositionMarkerFS` hat keine AR-Adapter-Schnittstelle. Genau wie bei `Q_NumericValue_PHYSA`, das
`Q_NumericValue_PHYS` um einen AR-Socket herum verpackt, gibt es jetzt `PositionMarkerFSA`
(`isobus::UT::Q`): ein neuer, kleiner Wrapper, der **intern eine einzige Instanz von
`PositionMarkerFS` aufruft** (keine Duplizierung der Klammer-Logik) und `xOver`/`xUnder` als
AX-Adapter-Plugs nach außen reicht — exakt dieselbe Baustein-Form wie `Q_NumericValue_PHYSA`. Die
bestehenden Bausteine `NumericValue_PHYSA`/`Q_NumericValue_PHYSA`/`PositionMarkerFS` wurden dafür
**nicht** verändert.

### Verdrahtung
- `Sollwert_N` (`NumericValue_PHYSA`) liest `InputNumber_Sollwert`, liefert den Wert als AR-Plug `rPhys`.
- `Split` (`AR_SPLIT_2`) verteilt diesen einen AR-Wert sauber auf zwei Verbraucher (ein Adapter darf
  nicht direkt auf mehrere Ziele zeigen — siehe `iec61499-creator`-Skill, Regel 8).
- `Marker_Dreieck` (`PositionMarkerFSA`) bewegt das Dreieck, mit Klammerung und `xOver`/`xUnder`.
- `Istwert_N` (`Q_NumericValue_PHYSA`) schreibt denselben Wert als Istwert zurück.
- Alles ausschließlich über `<AdapterConnections>` verdrahtet — keine einzige plain Event-/
  DataConnection nötig, genau wie bei `Uebung_011b1_PHYSA`.

### Referenzlösung
`Uebung_225b_AXA.SUB` — validiert gegen `subapptype.xsd`. Neuer Baustein:
`Ventilsteuerung\4diacIDE-workspace\.lib\isobus-3.0.0\typelib\UT\Q\PositionMarkerFSA.fbt`.
