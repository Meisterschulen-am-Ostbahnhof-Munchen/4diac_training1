# Uebung_080b: Frequenzverdopplung von Events

```{index} single: Uebung_080b: Frequenzverdopplung von Events
```

[Uebung_080b](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_080b.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_080b`. Hier wird gezeigt, wie man die Anzahl der eintreffenden Ereignisse künstlich verdoppelt.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Taster & Events: GPIO-Grundlagen für Land- und Baumaschinen Mechatroniker](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Taster--Events-GPIO-Grundlagen-fr-Land--und-Baumaschinen-Mechatroniker-e36aaen)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_080b.png)


## Ziel der Übung

Manipulation von Ereignisströmen unter Verwendung von `E_SPLIT`.

-----

## Funktionsweise

[cite_start]In `Uebung_080b.SUB` wird ein Ereignis-Splitter vor den Zähler geschaltet[cite: 1].
Jeder einzelne Klick auf Taster **I1** erreicht den Eingang `E_SPLIT.EI`. Der Splitter feuert daraufhin **zwei** Ereignisse (`EO1` und `EO2`) nacheinander ab. Da beide Ausgänge wieder auf den `CU`-Eingang des Zählers gemerged (zusammengeführt) werden, erhält der Zähler pro Tastendruck zwei Impulse.

**Ergebnis**: Die Lampe `Q1` (Schwelle 5) leuchtet bereits nach dem 3. Tastendruck auf (Zählerstand ist dann bereits auf 6 gesprungen).

-----

## Anwendungsbeispiel

Anpassung von Sensor-Impulsen: Ein Getriebesensor liefert einen Impuls pro Radumdrehung, die Logik benötigt aber zwei Impulse pro Umdrehung zur genaueren Berechnung. Der Splitter verdoppelt die eintreffende Frequenz rein softwareseitig.