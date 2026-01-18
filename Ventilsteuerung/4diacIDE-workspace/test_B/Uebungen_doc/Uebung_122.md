# Uebung_122: Netzwerk-Scan (16 Teilnehmer)

```{index} single: Uebung_122: Netzwerk-Scan (16 Teilnehmer)
```

[Uebung_122](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_122.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_122`.

----

![](Uebung_122.png)

## Übersicht

[cite_start]Diese Übung demonstriert die Erfassung einer größeren Anzahl von Bus-Teilnehmern[cite: 1].
Unter Verwendung des Bausteins `LOG_16` werden die Namen von bis zu 16 verschiedenen Control Functions im Netzwerk gleichzeitig gepuffert und analysiert. Für jeden Teilnehmer wird über eine Kette von `NmSetNameField` Bausteinen eine detaillierte Analyse der Identität durchgeführt. Dies ist ein Werkzeug für komplexe Diagnosesysteme, die den gesamten Geräteverbund eines Gespanns überwachen müssen.