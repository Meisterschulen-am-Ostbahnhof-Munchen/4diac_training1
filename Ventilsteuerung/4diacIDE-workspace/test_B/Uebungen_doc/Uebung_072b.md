# Uebung_072b: Versetzte Wegimpulse (Phasenschieber)

```{index} single: Uebung_072b: Versetzte Wegimpulse (Phasenschieber)
```

[Uebung_072b](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_072b.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_072b`. Hier wird eine komplexe wegabhängige Steuerung für mehrere Ausgänge realisiert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_072b.png)


## Ziel der Übung

Erzeugung von zeitversetzten Impulsen basierend auf dem GBSD-Distanzwert.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_072b.SUB` steuern vier `RangeBasedPulse` Bausteine vier Ausgänge (`Q1` bis `Q4`) an[cite: 1].

### Funktionsweise

Alle Bausteine reagieren auf den gleichen Distanzwert vom Radar (`I_GBSD`). Sie unterscheiden sich jedoch im Parameter **`DIST_OFF`** (Offset):
*   `Q1`: Offset 0 mm.
*   `Q2`: Offset 1000 mm.
*   `Q3`: Offset 2000 mm.
*   `Q4`: Offset 3000 mm.

Dies bewirkt ein "Wander-Muster": Wenn die Maschine fährt, schalten die Ausgänge nacheinander ein und aus, jeweils um einen Meter versetzt zur gefahrenen Strecke.

-----

## Anwendungsbeispiel

**Reihen-Steuerung bei Sämaschinen**:
Die Sähaggregate sind mechanisch versetzt am Rahmen montiert. Um exakt auf einer Linie quer zur Fahrtrichtung mit der Ablage zu beginnen, müssen die Aggregate je nach Fahrgeschwindigkeit und Position zeitversetzt angesteuert werden. Die Offset-Logik sorgt dafür, dass jedes Aggregat genau an der richtigen Stelle im Feld aktiv wird.