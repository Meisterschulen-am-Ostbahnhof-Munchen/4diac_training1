# Uebung_010bA3: Toggle Flip-Flop mit IE AuxFunction2_X1 AuxHeld

```{index} single: Uebung_010bA3: AUX-Repetier-Event (Held)
```

[Uebung_010bA3](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010bA3.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010bA3`.

----

![](Uebung_010bA3.png)

## Funktionsweise

[cite_start]Nutzt `AuxFunction2_X1` mit `AuxHeld`[cite: 1]. Bei einem tastenden Bedienelement führt dieses Ereignis zu einer kontinuierlichen Event-Folge, solange die Taste am Joystick gehalten wird. In Kombination mit einem Toggle-Flip-Flop entsteht so ein Blink-Effekt am Ausgang.