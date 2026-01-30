# Uebung_004c4_AX: Gedrückt halten (Wiederholung)

```{index} single: Uebung_004c4_AX: Gedrückt halten (Wiederholung)
```

[Uebung_004c4_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004c4_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004c4_AX`.

----

![](Uebung_004c4_AX.png)

## Ziel der Übung

Nutzung des Ereignisses `BUTTON_LONG_PRESS_HOLD`.

-----

## Funktionsweise

[cite_start]Der Baustein `DigitalInput_CLK_I1` in `Uebung_004c4_AX.SUB` ist auf `BUTTON_LONG_PRESS_HOLD` konfiguriert[cite: 1].

Dieses Event wird *periodisch* gefeuert, solange der Taster nach Erkennung des langen Drucks weiterhin gehalten wird.

-----

## Anwendungsbeispiel

**Lautstärke ändern / Scrollen**: Solange man die Taste gedrückt hält, wird die Lautstärke schrittweise erhöht oder durch ein Menü gescrollt. Das Toggle-FF würde hier sehr schnell an und aus gehen (Flackern), was zeigt, dass dieses Event eher für Inkrement-Funktionen als für Toggles gedacht ist.