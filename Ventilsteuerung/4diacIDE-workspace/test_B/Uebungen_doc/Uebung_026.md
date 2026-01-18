# Uebung_026: Strukturierte Sequenz-Ausgabe

```{index} single: Uebung_026: Strukturierte Sequenz-Ausgabe
```

[Uebung_026](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_026.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_026`.

## 📺 Video

* [2025 11 15 12 52 26 Montage Hutschienenmoped logiBUS® -- Teil 4 -- Aufbauten](https://www.youtube.com/watch?v=WeowCxZW70Y)
* [2026-01-13 12-14-50 logiBUS® Eclipse 4diac™ Subapplications](https://www.youtube.com/watch?v=J-UYbZDwhZw)

----

![](Uebung_026.png)

## Übersicht

[cite_start]In dieser Übung wird die komplexe Ablauflogik aus Übung 025 beibehalten, jedoch wird die Ansteuerung der Hardware-Ausgänge in eine typisierte Sub-Applikation `Uebung_026_sub` ausgelagert[cite: 1].
Jede Instanz dieser Sub-App (`Q1` bis `Q4`) kapselt einen SR-Speicher und den Hardware-Ausgangsbaustein. Das Hauptdiagramm wird dadurch wesentlich übersichtlicher, da nur noch die Ereigniskette zwischen den Phasen (Rendezvous und Delays) sichtbar ist, während die "Leistungsebene" im Hintergrund arbeitet.