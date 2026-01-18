# Uebung_038: Zeitgesteuertes Lauflicht (8-fach)

```{index} single: Uebung_038: Zeitgesteuertes Lauflicht (8-fach)
```

[Uebung_038](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_038.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_038`. Hier wird eine umfangreichere Schrittkette mit 8 Phasen realisiert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_038.png)


## Übersicht

[cite_start]Unter Verwendung des Bausteins `sequence_T_08_loop` wird ein automatisches Lauflicht über 8 Ausgänge (`Q1` bis `Q8`) erzeugt[cite: 1].
Die Übergangszeiten zwischen den Lampen sind individuell einstellbar (z.B. 200ms für die ungeraden, 100ms für die geraden Schritte). Das Programm demonstriert die Handhabung vieler paralleler Ausgänge und die numerische Rückmeldung des aktuellen Systemzustands an das Terminal.