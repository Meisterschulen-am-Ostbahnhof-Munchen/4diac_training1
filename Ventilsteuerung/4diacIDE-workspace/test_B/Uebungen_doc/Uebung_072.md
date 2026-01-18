# Uebung_072: Rad- vs. Radargeschwindigkeit

```{index} single: Uebung_072: Rad- vs. Radargeschwindigkeit
```

[Uebung_072](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_072.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_072`. In der Landtechnik gibt es verschiedene Quellen für die Geschwindigkeit; hier werden die zwei wichtigsten verglichen.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_072.png)


## Ziel der Übung

Gleichzeitige Verarbeitung von radbasierter (WBSD) und grundbasierter (GBSD) Geschwindigkeit.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_072.SUB` werden zwei verschiedene TECU-Eingangsbausteine genutzt und deren Werte auf dem Terminal angezeigt[cite: 1].

### Funktionsbausteine (FBs)

  * **`I_WBSD`**: Radbasierte Geschwindigkeit (Wheel Based). Sie stammt meist vom Getriebe-Sensor.
  * **`I_GBSD`**: Grundbasierte Geschwindigkeit (Ground Based). Sie wird meist über einen Radar-Sensor oder GPS-Empfänger ermittelt.

-----

## Hintergrund: Warum zwei Werte?

Auf losem Untergrund (z.B. nasser Acker) haben die Räder oft Schlupf. Die radbasierte Geschwindigkeit ist dann höher als die tatsächliche Vorwärtsbewegung. Die grundbasierte Geschwindigkeit (Radar) ist in diesem Fall genauer. Durch den Vergleich beider Werte im Programm kann die Steuerung den **Schlupf** berechnen und die Arbeitsprozesse entsprechend anpassen.