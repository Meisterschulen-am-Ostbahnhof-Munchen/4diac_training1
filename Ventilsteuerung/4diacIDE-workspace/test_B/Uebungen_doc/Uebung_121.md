# Uebung_121: Eigener ISOBUS Name

```{index} single: Uebung_121: Eigener ISOBUS Name
```

[Uebung_121](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_121.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_121`.

----

![](Uebung_121.png)

## Übersicht

[cite_start]In dieser Übung wird das Gegenstück zu 120 gezeigt: Das Auslesen der eigenen Identität[cite: 1].
Über den Parameter `member = thisMember` am Baustein `NmGetCfInfo` liefert die Steuerung ihren eigenen 64-Bit Namen zurück. Mit dem Baustein `NmSetName` können zudem die einzelnen Felder der eigenen Identität (z.B. die Funktions-Instanz) zur Laufzeit dynamisch angepasst werden, bevor sie über den Bus kommuniziert werden.