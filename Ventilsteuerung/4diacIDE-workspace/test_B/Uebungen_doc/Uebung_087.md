# Uebung_087: Bedingte Ereignisverteilung (E_DEMUX)

```{index} single: Uebung_087: Bedingte Ereignisverteilung (E_DEMUX)
```

[Uebung_087](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_087.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_087`. Hier wird die Auswahl eines Ereignispfads durch eine Kombination von Logikwerten demonstriert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_087.png)


## Ziel der Übung

Verwendung des `E_DEMUX` (Event Demultiplexer). Es wird gezeigt, wie ein zentrales "Ausführ-Ereignis" (Klick auf Taster 1) an verschiedene Aktoren geleitet wird, wobei die Auswahl über die Kombination anderer Taster getroffen wird.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_087.SUB` nutzt eine Additions-Logik, um den Selektor-Eingang des Demultiplexers zu steuern[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` (Trigger)**: Das Ereignis, das verteilt werden soll.
  * **`I2`, `I3`, `I4` (Selector)**: Bestimmen das Ziel.
  * **`ADD_3`**: Summiert die Zustände der Taster 2, 3 und 4 auf.
  * **`E_DEMUX`**: Leitet das Event von `I1` an den Ausgang weiter, dessen Nummer der berechneten Summe entspricht.

-----

## Funktionsweise

Die Anzahl der gedrückten "Wahl-Taster" bestimmt, welche Lampe beim Klick auf **I1** toggelt:
*   Kein Wahl-Taster gedrückt ➡️ Summe = 0 ➡️ Klick auf I1 toggelt **Q1**.
*   Ein Wahl-Taster gedrückt ➡️ Summe = 1 ➡️ Klick auf I1 toggelt **Q2**.
*   Zwei Wahl-Taster gedrückt ➡️ Summe = 2 ➡️ Klick auf I1 toggelt **Q3**.
*   Alle drei Wahl-Taster gedrückt ➡️ Summe = 3 ➡️ Klick auf I1 toggelt **Q4**.

-----

## Anwendungsbeispiel

**Indirekte Adressierung**:
Ein Bediener wählt über Kippschalter an seinem Bedienpult eine Gruppe von Düsen aus. Erst wenn er den zentralen Fußtaster (`I1`) betätigt, wird der Befehl an die gewählte Gruppe gesendet.