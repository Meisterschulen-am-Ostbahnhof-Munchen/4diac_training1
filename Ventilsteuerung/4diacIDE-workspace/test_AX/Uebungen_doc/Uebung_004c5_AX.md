# Uebung_004c5_AX: Loslassen (Generell)

```{index} single: Uebung_004c5_AX: Loslassen (Generell)
```

[Uebung_004c5_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004c5_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004c5_AX`.

----

![](Uebung_004c5_AX.png)

## Ziel der Übung

Nutzung des Ereignisses `BUTTON_PRESS_END`.

-----

## Funktionsweise

[cite_start]Der Baustein `DigitalInput_CLK_I1` in `Uebung_004c5_AX.SUB` ist auf `BUTTON_PRESS_END` konfiguriert[cite: 1].

Dieses Event feuert *immer*, wenn der Taster losgelassen wird, egal ob kurz oder lang gedrückt wurde.

-----

## Anwendungsbeispiel

**Totmannschalter**: Eine Funktion ist aktiv, solange gedrückt wird (Start beim Pegel-Wechsel auf HIGH), und muss sicher stoppen, wenn losgelassen wird (`PRESS_END`).