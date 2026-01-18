# Uebung_023: Kompletter Zyklus (Aus- und Einfahren)

```{index} single: Uebung_023: Kompletter Zyklus (Aus- und Einfahren)
```

[Uebung_023](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_023.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_023`. Hier wird ein vollständiger Hin- und Rückweg für zwei Zylinder implementiert.

## 📺 Video

* [2025-02-21 15-23-28 logiBUS® mit Eclipse 4diac™ neues IO Konzept für alle Controller](https://www.youtube.com/watch?v=YUCodIng1UA)
* [2025-02-23 11-18-57 Einstieg in Autodesk Fusion 360 - Mechanisches Design MCAD](https://www.youtube.com/watch?v=3bmFKBpIpZY)
* [2025-02-23 11-43-44 Fusion 360 Übersicht Tutorials](https://www.youtube.com/watch?v=djM9ndIfp-0)
* [2025-02-23 11-47-07 Fusion 360 Elektronik Einführung](https://www.youtube.com/watch?v=uZb-U6FArGw)
* [2025-02-23 13-20-15 Fusion 360 Elektronik Stückliste Exportieren](https://www.youtube.com/watch?v=Z5RllKgpOfc)

----

![](Uebung_023.png)

## Übersicht

[cite_start]Diese Übung erweitert die Logik auf insgesamt vier Phasen unter Verwendung von sechs Softkeys[cite: 1]:
1.  **Ausfahren**: `F1` (Start) ➡️ `Q1` an. Endlage erreicht über `F2`.
2.  **Folgeschritt**: `F2` stoppt `Q1` und startet `Q2`. Endlage erreicht über `F3`.
3.  **Einfahren**: Über separate Taster (`F7`, `F8`) wird die Rückhol-Sequenz eingeleitet (`Q3`, `Q4`).

Dies zeigt die Handhabung von komplexen, richtungsabhängigen Abläufen in einer flachen Ereignisstruktur.