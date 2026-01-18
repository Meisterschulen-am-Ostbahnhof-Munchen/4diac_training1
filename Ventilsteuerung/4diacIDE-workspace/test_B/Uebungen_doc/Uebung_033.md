# Uebung_033: Modulare RGB-Ansteuerung

```{index} single: Uebung_033: Modulare RGB-Ansteuerung
```

[Uebung_033](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_033.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_033`.

## 📺 Video

* [2025-11-15 12-19-33 Montage Hutschienenmoped logiBUS® -- Teil 2 -- Einführung und Löten](https://www.youtube.com/watch?v=nohE36SZY9M)
* [logiBUS® ESP32 installer   Google Chrome 2022 10 18 17 38 33](https://www.youtube.com/watch?v=pQ53R2zChlc)

----

![](Uebung_033.png)

## Übersicht

[cite_start]Dies ist die modulare Variante der Übung 032[cite: 1]. Die Logik für einen farbigen LED-Kanal wurde in eine typisierte Sub-Applikation `Uebung_033_sub` ausgelagert. Das Hauptprogramm instanziiert diesen Typ viermal und weist ihm die Taster `I1` bis `I4` sowie die Zielfarben zu. Dies zeigt erneut die Vorteile der Wiederverwendbarkeit bei komplexen Hardware-Komponenten wie LED-Controllern.