# Uebung_010bA: Einmaliger langer Tastendruck

```{index} single: Uebung_010bA: Einmaliger langer Tastendruck
```

[Uebung_010bA](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010bA.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010bA`.

----

![](Uebung_010bA.png)

## Funktionsweise

[cite_start]Nutzt `Button_A1` mit `BT_STILL_HELD_START`[cite: 1]. Im Gegensatz zum einfachen `STILL_HELD` wird dieses Ereignis **nicht wiederholt**. Es feuert exakt einmal, sobald die Haltezeit überschritten wurde. Dies entspricht einer sauberen "Long Press" Auswertung.