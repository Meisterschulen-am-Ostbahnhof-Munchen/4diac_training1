# Uebung_010bA4: Einmaliges AUX-Halte-Event

```{index} single: Uebung_010bA4: Einmaliges AUX-Halte-Event
```

[Uebung_010bA4](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010bA4.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010bA4`.

----

![](Uebung_010bA4.png)

## Funktionsweise

[cite_start]Nutzt `AuxFunction2_X1` mit `AuxHeld_START`[cite: 1]. Unabhängig vom Typ des Bedienelements wird dieses Ereignis nur **einmal** beim Erreichen der Zeitschwelle gesendet. Es ist die bevorzugte Wahl für Long-Press-Funktionen an ISOBUS-Joysticks.