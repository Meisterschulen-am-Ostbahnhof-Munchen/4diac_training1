# Übung 225 AXA: Dreieck-Sollwertmarker mit AR-Adapter (manuelle Kette)

## Thema: Virtual-Terminal-Objektpositionierung — AR-Adapter-Variante

Adapter-Variante von [Übung 225](Uebung_225_AX_Beschreibung.md): identische Funktion, aber Sollwert-
Lesen und Istwert-Schreiben laufen über die AR-Adapter-Bausteine (`NumericValue_PHYSA`/
`Q_NumericValue_PHYSA`) statt über plain `REQ`/`IND`-Events. Die eigentliche Dreieck-Bewegung
verwendet weiterhin die "manuelle" Kette (kein Klammern) — passend zu Übung 225, nicht zu 225b.

### Warum ein neuer Baustein nötig war
`Q_ChildPosition` hat keine AR-Adapter-Schnittstelle, und ein Adapter-Plug/Socket-Teilsignal
(`.E1`/`.D1`) lässt sich nur **innerhalb** des Bausteins ansprechen, der es selbst deklariert — nicht
von außen aus einer dritten SubApp heraus. Deshalb gibt es jetzt `ChildPositionValueA`
(`isobus::UT::Q`): ein neuer, kleiner AR-Socket-Wrapper, der intern exakt die gleiche
`F_ADD`→`F_REAL_TO_INT`→`Q_ChildPosition`-Kette aufbaut wie Übung 225 selbst — bewusst **ohne**
Klammern/`xOver`/`xUnder`, um zu Übung 225 (die das auch nicht hat) passend zu bleiben. Die
bestehenden Bausteine `NumericValue_PHYSA`/`Q_NumericValue_PHYSA` wurden dafür **nicht** verändert.

### Verdrahtung
- `Sollwert_N` (`NumericValue_PHYSA`) liest `InputNumber_Sollwert`, liefert den Wert als AR-Plug `rPhys`.
- `Split` (`AR_SPLIT_2`) verteilt diesen einen AR-Wert sauber auf zwei Verbraucher (ein Adapter darf
  nicht direkt auf mehrere Ziele zeigen — siehe `iec61499-creator`-Skill, Regel 8).
- `Move_Dreieck` (`ChildPositionValueA`) bewegt das Dreieck.
- `Istwert_N` (`Q_NumericValue_PHYSA`) schreibt denselben Wert als Istwert zurück.
- Alles ausschließlich über `<AdapterConnections>` verdrahtet — keine einzige plain Event-/
  DataConnection nötig, genau wie bei `Uebung_011b1_PHYSA`.

### Referenzlösung
`Uebung_225_AXA.SUB` — validiert gegen `subapptype.xsd`. Neuer Baustein:
`Ventilsteuerung\4diacIDE-workspace\.lib\isobus-3.0.0\typelib\UT\Q\ChildPositionValueA.fbt`.
