# Uebung_023: Kompletter Zyklus (Aus- und Einfahren)

```{index} single: Uebung_023: Kompletter Zyklus (Aus- und Einfahren)
```

[Uebung_023](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_023.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_023`. Hier wird ein vollständiger Hin- und Rückweg für zwei Zylinder implementiert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_023.png)


## Übersicht

[cite_start]Diese Übung erweitert die Logik auf insgesamt vier Phasen unter Verwendung von sechs Softkeys[cite: 1]:
1.  **Ausfahren**: `F1` (Start) ➡️ `Q1` an. Endlage erreicht über `F2`.
2.  **Folgeschritt**: `F2` stoppt `Q1` und startet `Q2`. Endlage erreicht über `F3`.
3.  **Einfahren**: Über separate Taster (`F7`, `F8`) wird die Rückhol-Sequenz eingeleitet (`Q3`, `Q4`).

Dies zeigt die Handhabung von komplexen, richtungsabhängigen Abläufen in einer flachen Ereignisstruktur.