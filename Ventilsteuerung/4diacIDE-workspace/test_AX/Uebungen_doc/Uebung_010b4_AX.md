# Uebung_010b4_AX: Softkey Massenmapping (8-fach)

```{index} single: Uebung_010b4_AX: Softkey Massenmapping (8-fach)
```

[Uebung_010b4_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b4_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010b4_AX`.

## 🎧 Podcast

* [ISO 11783-6: Softkeys und das Virtual Terminal verstehen – Dein Schlüssel zur Landmaschinen-Mechatronik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISO-11783-6-Softkeys-und-das-Virtual-Terminal-verstehen--Dein-Schlssel-zur-Landmaschinen-Mechatronik-e36a8b0)

----

![](Uebung_010b4_AX.png)

## Ziel der Übung

Effiziente Verbindung vieler Softkeys.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_010b4_AX.SUB` nutzt untypisierte Sub-Applikationen (`Uebung_010b4_sub_AX`), um 8 Softkeys auf 8 Ausgänge zu mappen[cite: 1].

Die Struktur ist analog zu `Uebung_003b2_AX`, nur mit ISOBUS-Softkeys als Quelle.

-----

## Funktionsweise

Jede SubApp kapselt die Verbindung `Softkey -> Ausgang`. Dies hält das Hauptdiagramm sauber.