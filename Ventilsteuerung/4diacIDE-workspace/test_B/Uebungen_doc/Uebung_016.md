# Uebung_016: Dynamische Hintergrundfarben

```{index} single: Uebung_016: Dynamische Hintergrundfarben
```

[Uebung_016](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_016.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_016`. Hier wird gezeigt, wie man die Hintergrundfarbe von Objekten (z.B. Softkeys) zur Laufzeit ändert, um Zustände zu visualisieren.

## 📺 Video

* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-03-11 16-08-47 Erzeugen von Dokumentation zur IEC 61499 mittels deepseek](https://www.youtube.com/watch?v=Ce__kP5iFc0)
* [2025-03-11 16-53-43 Watch über App, nicht über Ressource](https://www.youtube.com/watch?v=bGwFMVQBj3k)
* [2025-03-15 16-27-21 Arithmetischer Überlauf führt zu Division durch 0.](https://www.youtube.com/watch?v=7CyOJPYJVz0)

## 🎧 Podcast

* [ESP32-S3-DevKitC-1 Doku-Analyse: Das Speicher-Monster (32MB Flash/16MB PSRAM) und die Macht der Dual-USB-Ports](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/ESP32-S3-DevKitC-1-Doku-Analyse-Das-Speicher-Monster-32MB-Flash16MB-PSRAM-und-die-Macht-der-Dual-USB-Ports-e39hamt)

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