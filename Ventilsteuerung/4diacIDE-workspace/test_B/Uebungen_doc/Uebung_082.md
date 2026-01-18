# Uebung_082: Vorwärts-Rückwärts-Zähler (Up/Down)

```{index} single: Uebung_082: Vorwärts-Rückwärts-Zähler (Up/Down)
```

[Uebung_082](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_082.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_082`. Hier werden beide Zählrichtungen in einem Baustein kombiniert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [E_CTD: Ereignisgesteuerter Abwärtszähler nach IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_CTD-Ereignisgesteuerter-Abwrtszhler-nach-IEC-61499-e368lli)
* [E_CTUD: Bidirektionaler Zähler in IEC 61499 Systemen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_CTUD-Bidirektionaler-Zhler-in-IEC-61499-Systemen-e368lmb)
* [Meisterwissen 61499: Der Ereignisgesteuerte Aufwärtszähler (E_CTU) – Robustes Zählen in Landmaschinen-Steuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Meisterwissen-61499-Der-Ereignisgesteuerte-Aufwrtszhler-E_CTU--Robustes-Zhlen-in-Landmaschinen-Steuerungen-e3a9q5n)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_082.png)


## Ziel der Übung

Verwendung des Bausteins `E_CTUD` (Event Count Up/Down). Es wird gezeigt, wie man den Füllstand eines Speichers verwaltet, der sowohl Zu- als auch Abflüsse hat.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_082.SUB` nutzt vier Taster zur vollständigen Kontrolle des Zählers[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` (CU)**: Zählt aufwärts.
  * **`I2` (CD)**: Zählt abwärts.
  * **`I3` (R)**: Setzt den Zähler auf Null.
  * **`I4` (LD)**: Lädt den Zähler mit dem Wert 5 (`PV`).
  * **`Q1` (Upper Limit)**: Leuchtet, wenn der Zählerstand >= 5 ist.
  * **`Q2` (Lower Limit)**: Leuchtet, wenn der Zählerstand <= 0 ist.

-----

## Funktionsweise

Der Baustein überwacht zwei Schwellwerte gleichzeitig:
*   Der Ausgang `QU` reagiert auf die Obergrenze (`PV`).
*   Der Ausgang `QD` reagiert auf die Untergrenze (Null).

Dies ermöglicht eine lückenlose Überwachung von Beständen oder Positionen innerhalb eines definierten Arbeitsbereichs.