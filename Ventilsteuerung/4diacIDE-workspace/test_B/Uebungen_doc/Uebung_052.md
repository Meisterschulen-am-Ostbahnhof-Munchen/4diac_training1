# Uebung_052: DigitalInput_I1-_I4 auf DigitalOutput_Q1-_Q4

```{index} single: Uebung_052: Gezielter Zugriff auf Strukturen
```

[Uebung_052](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_052.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_052`.

----

![](Uebung_052.png)

## Übersicht

[cite_start]In dieser Variante wird gezeigt, wie man ein einzelnes Signal aus einer Struktur extrahiert, ohne alle Kanäle auspacken zu müssen[cite: 1].
Über den Baustein `GET_STRUCT_VALUE` und den Parameter `member = 'X_00'` wird gezielt nur der erste Kanal aus dem Datenpaket der Übung 051 abgegriffen und auf den Ausgang `Q4` gelegt. Dies ist nützlich, wenn in einem Modul nur eine bestimmte Information aus einem großen Datenbündel benötigt wird.