# Uebung_016: Dynamische Hintergrundfarben

[Uebung_016](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_016.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_016`. Hier wird gezeigt, wie man die Hintergrundfarbe von Objekten (z.B. Softkeys) zur Laufzeit ändert, um Zustände zu visualisieren.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_016.png)


## Ziel der Übung

Verwendung des Bausteins `Q_BackgroundColour`. Dies ist eine Alternative zum Farbumschlag in Sub-Applikationen (wie in Übung 010c) und erlaubt die explizite Wahl von Farben aus der ISOBUS-Palette.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_016.SUB` schaltet die Farbe des Softkeys `F7` basierend auf der Auswahl über `F1` und `F2` um[cite: 1].

### Funktionsbausteine (FBs)

  * **`F_SEL`**: Wählt zwischen zwei Farb-Konstanten aus.
  * **`Q_BackgroundColour`**: Der Ausgangsbaustein. [cite_start]Er setzt die Hintergrundfarbe für das Objekt `SoftKey_F7`[cite: 1].

-----

## Funktionsweise

*   Wird der Speicher durch **F1** gesetzt, liefert `F_SEL` den Wert `COLOR_GREEN`.
*   Wird er durch **F2** gelöscht, liefert `F_SEL` den Wert `COLOR_WHITE`.
*   Das Ergebnis wird an `Q_BackgroundColour` gesendet, welches das entsprechende ISOBUS-Kommando ("Change Background Colour") an das Terminal absetzt.

Der Softkey `F7` (der in dieser Übung keine eigene Logik hat, sondern nur als Anzeige dient) wechselt nun zwischen Grün und Weiß.

-----

## Anwendungsbeispiel

**Status-Ampel**:
Ein Sensor überwacht einen Füllstand. Ist alles im grünen Bereich, leuchtet eine Anzeige am Terminal grün. Erreicht der Stand eine kritische Marke, schaltet die Anzeige auf Gelb oder Rot um, um den Bediener visuell zu warnen.
