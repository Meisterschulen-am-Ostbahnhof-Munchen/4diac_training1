# Uebung_020f: Impulsgeber (E_TP)

```{index} single: Uebung_020f: Impulsgeber (E_TP)
```

[Uebung_020f](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020f.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020f`.

----

![](Uebung_020f.png)

## Ziel der Übung

Nutzung des impulsformenden Timers `E_TP` (Timer Pulse).

-----

## Funktionsweise

[cite_start]Sobald der Eingang `IN` auf `TRUE` wechselt, schaltet der Ausgang `Q` für exakt die Zeit `PT` (hier 5 Sekunden) ein[cite: 1].
Das Besondere: Der Ausgang bleibt für die volle Zeit aktiv, auch wenn der Eingang `IN` zwischendurch wieder abfällt oder mehrfach gedrückt wird (nicht re-triggerbar).

-----

## Anwendungsbeispiel

**Türöffner**: Ein kurzer Druck auf den Taster lässt den elektrischen Türöffner für 5 Sekunden summen, damit der Gast eintreten kann. Die Zeit läuft unabhängig davon ab, wie lange der Bewohner den Taster tatsächlich gedrückt hält.