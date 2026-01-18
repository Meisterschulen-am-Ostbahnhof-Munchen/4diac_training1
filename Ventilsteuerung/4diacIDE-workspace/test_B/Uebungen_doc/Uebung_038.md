# Uebung_038: Zeitgesteuertes Lauflicht (8-fach)

```{index} single: Uebung_038: Zeitgesteuertes Lauflicht (8-fach)
```

[Uebung_038](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_038.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_038`. Hier wird eine umfangreichere Schrittkette mit 8 Phasen realisiert.

## 📺 Video

* [Geräte Manager 2022 10 18 17 38 10](https://www.youtube.com/watch?v=l9kIRm3Wtas)
* [logiBUS® ESP32 installer   Google Chrome 2022 10 18 17 38 33](https://www.youtube.com/watch?v=pQ53R2zChlc)

----

![](Uebung_038.png)

## Übersicht

[cite_start]Unter Verwendung des Bausteins `sequence_T_08_loop` wird ein automatisches Lauflicht über 8 Ausgänge (`Q1` bis `Q8`) erzeugt[cite: 1].
Die Übergangszeiten zwischen den Lampen sind individuell einstellbar (z.B. 200ms für die ungeraden, 100ms für die geraden Schritte). Das Programm demonstriert die Handhabung vieler paralleler Ausgänge und die numerische Rückmeldung des aktuellen Systemzustands an das Terminal.