# Uebung_010b6: Softkey-Pressed als Auslöser

```{index} single: Uebung_010b6: Softkey-Pressed als Auslöser
```

[Uebung_010b6](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b6.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010b6`.

----

![](Uebung_010b6.png)

## Ziel der Übung

Reaktion zum frühestmöglichen Zeitpunkt der Interaktion.

-----

## Funktionsweise

[cite_start]Verwendet das Event `SK_PRESSED`[cite: 1]. Das Flip-Flop am Ausgang toggelt bereits in dem Moment, in dem der Nutzer den Touchscreen berührt. Dies minimiert die gefühlte Latenz, verhindert aber ein nachträgliches Abbrechen durch Wegziehen des Fingers.