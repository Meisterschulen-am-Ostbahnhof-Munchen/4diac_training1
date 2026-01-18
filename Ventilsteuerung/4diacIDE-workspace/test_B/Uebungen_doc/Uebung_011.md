# Uebung_011: Numerische Eingabe (Universal Terminal)

```{index} single: Uebung_011: Numerische Eingabe (Universal Terminal)
```

[Uebung_011](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_011.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_011`. Hier wird demonstriert, wie Zahlenwerte (Daten) von einem ISOBUS-Terminal eingelesen werden.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_011.png)


## Ziel der Übung

Erlernen der Verarbeitung von numerischen Variablen im ISOBUS-Kontext. Es wird gezeigt, wie ein Nutzer am Terminal eine Zahl eingeben kann und wie diese Information als Daten-Ereignis-Kombination in der Steuerung ankommt.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_011.SUB` nutzt einen Eingabe-Baustein für numerische Werte[cite: 1].

### Funktionsbausteine (FBs)

  * **`InputNumber_I1`**: Typ `NumericValue_ID`. [cite_start]Dieser Baustein repräsentiert ein numerisches Eingabefeld (Data Mask Object) auf dem ISOBUS-Terminal[cite: 1]. Sobald der Nutzer die Eingabe bestätigt, sendet der Baustein den neuen Wert am Port `IN` (DWORD) und feuert ein `IND`-Ereignis.
  * **`F_DWORD_TO_UDINT`**: Ein Konvertierungs-Baustein, der den rohen 32-Bit-Wert vom Terminal in einen vorzeichenlosen Ganzzahlwert (UDINT) für die weitere Logik umwandelt.

-----

## Funktionsweise

Die Logik wartet auf die Bestätigung der Eingabe am Terminal:

```xml
<EventConnections>
    <Connection Source="InputNumber_I1.IND" Destination="F_DWORD_TO_UDINT.REQ"/>
</EventConnections>
<DataConnections>
    <Connection Source="InputNumber_I1.IN" Destination="F_DWORD_TO_UDINT.IN"/>
</DataConnections>
```

[cite_start][cite: 1]

1.  Der Nutzer tippt am Terminal auf das Zahlenfeld `I1`, gibt z.B. "42" ein und drückt "Enter".
2.  Das Terminal sendet den Wert über den CAN-Bus an die Steuerung.
3.  Der Baustein `InputNumber_I1` empfängt den Wert und löst das Ereignis `IND` aus.
4.  Der Konvertierungs-Baustein übernimmt den Wert und stellt ihn der restlichen Applikation als Standard-Datentyp zur Verfügung.

-----

## Anwendungsbeispiel

**Einstellung von Sollwerten**:
Der Landwirt gibt am Terminal die gewünschte Ausbringmenge für Saatgut (in kg/ha) oder die Zieltemperatur für die Getreidetrocknung ein. Die Software verarbeitet diesen numerischen Wert sofort weiter.
