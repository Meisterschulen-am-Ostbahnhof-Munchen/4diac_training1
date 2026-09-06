# Übung 225b: Dreieck-Sollwertmarker mit PositionMarkerFS

## Thema: Virtual-Terminal-Objektpositionierung (ISO 11783-6 Annex F.16) — wiederverwendbarer Baustein

Variante von [Übung 225](Uebung_225_AX_Beschreibung.md): dieselbe Aufgabe, aber statt die drei
Bausteine `F_ADD_Center`/`F_REAL_TO_INT_Pos`/`Q_ChildPosition_Dreieck` einzeln zu verdrahten, wird
der neue wiederverwendbare Baustein `PositionMarkerFS` (`isobus::UT::Q`) eingesetzt. Übung 225 selbst
bleibt unverändert als eigenständige Referenz stehen.

### Situationsbeschreibung
Im ISO-Designer-Pool `Workspace_Dreieck` zeigt ein kleines Dreieck (`Polygon_Bargraph_Mittelmarker`)
innerhalb eines 96×14 px großen Containers (`Container_Sollwertmarker`) eine Sollposition an —
analog zum Mittelmarker, wie er in der echten Krauternter-Anwendung für Achslenkung/Hangausgleich
verwendet wird. Der Bediener gibt über das Eingabefeld `InputNumber_Sollwert` (VT-Objekt 9000) einen
Wert zwischen **-42 und +42** ein (0 = Mitte, ISO-Designer wendet den Offset -42 bereits objektseitig
an). Das Dreieck soll dieser Eingabe sofort folgen, und der eingestellte Wert soll zusätzlich als
Istwert (`NumberVariable_Istwert`, treibt sowohl `InputNumber_Istwert` als auch den Bargraph-Zeiger)
zurückgemeldet werden.

### Funktionsbeschreibung
- **Sollwert lesen:** Ändert der Bediener `InputNumber_Sollwert`, liefert das VT den physikalischen
  Wert (bereits skaliert/versetzt gemäß Offset -42) als `REAL`.
- **Dreieck bewegen:** übernimmt der wiederverwendbare Baustein `PositionMarkerFS`
  (`isobus::UT::Q`) — er addiert intern den Center-Offset, klammert das Ergebnis auf den gültigen
  Bewegungsbereich (mit `xOver`/`xUnder`-Rückmeldung), rechnet `REAL`→`INT` um und schreibt die
  Position per **Change Child Position** (ISO 11783-6 Annex F.16) auf das Polygon-Objekt. Kind-Objekt
  ist das Dreieck (`Polygon_Bargraph_Mittelmarker`, ID 16000, gültig als Kind: TypPolygon
  16000–16999), Parent-Objekt ist der Container (`Container_Sollwertmarker`, ID 3000, gültig als
  Parent: Container, Annex B.4). Y bleibt konstant 0. Kind-ID, Parent-ID, Bewegungsbereich und
  Center-Offset kommen gebündelt aus **einer** Konstante (`Container_PositionMarker`, Typ
  `PositionMarker_S`), die `GcfScript.py` automatisch aus der `.jop`-Geometrie erzeugt (Container
  ObjectName endet auf `_Sollwertmarker`) — analog zu `ScrollObjectPool_S` beim Scroll-Baustein.
- **Istwert zurückschreiben:** Derselbe physikalische Sollwert wird unverändert (gleicher Offset,
  keine weitere Umrechnung nötig) auf `NumberVariable_Istwert` geschrieben — dadurch aktualisieren
  sich sowohl `InputNumber_Istwert` als auch der Bargraph-Positionszeiger gleichzeitig.
- **Wichtig:** der Sollwert-Eingang von `PositionMarkerFS` (`rValue`) ist ein generischer `REAL`-Wert
  — er muss nicht zwingend von `NumericValue_PHYS` kommen, sondern kann z. B. auch direkt von einem
  Sensor gespeist werden. Deshalb bleibt `NumericValue_PHYS` bewusst außerhalb des Bausteins.

### Arbeitsauftrag
1. Legen Sie die SubApp `Uebung_225b_AX` an (bereits als Referenzlösung vorhanden).
2. Lesen Sie `InputNumber_Sollwert` (VT-Objekt 9000) mit einer `NumericValue_PHYS`-Instanz
   (`stObj := NumberVariable_Sollwert_N` aus `DefaultPool_Dreieck_Numeric.gcf`) — das VT meldet
   Wertänderungen eines an eine `NumberVariable` gebundenen Eingabefelds unter der Objekt-ID der
   Variable (hier `NumberVariable_Sollwert`, 21000), nicht unter der ID des Eingabefelds selbst
   (9000).
3. Bewegen Sie das Dreieck mit einer `PositionMarkerFS`-Instanz (`stObj := Container_PositionMarker`
   aus `DefaultPool_Dreieck_PositionMarker.gcf`, `rValue :=` der physikalische Sollwert aus Schritt 2).
4. Schreiben Sie parallel denselben physikalischen Sollwert mit `Q_NumericValue_PHYS`
   (`stObj := NumberVariable_Istwert_N`) als Istwert zurück.
5. Am echten Terminal testen: Sollwert ändern → Dreieck folgt sofort, Istwert-Feld und
   Bargraph-Zeiger zeigen denselben Wert, `xOver`/`xUnder` bleiben `FALSE` solange der Sollwert im
   gültigen Bereich liegt.

### Referenzlösung
`Uebung_225b_AX.SUB` — validiert gegen `subapptype.xsd` (siehe `iec61499-creator`-Skill). Der
wiederverwendbare Baustein liegt in
`Ventilsteuerung\4diacIDE-workspace\.lib\isobus-3.0.0\typelib\UT\Q\PositionMarkerFS.fbt`
(Struct `isobus::utils::childposition::PositionMarker_S`, Klammer-Hilfsbaustein
`isobus::UT::Q::helpers::F_ClampReal`).
