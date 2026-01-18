# Uebung_034a1_Q1: PWM-Wert vom Terminal (Kanal 1)

```{index} single: Uebung_034a1_Q1: PWM-Wert vom Terminal (Kanal 1)
```

[Uebung_034a1_Q1](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_034a1_Q1.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

## Übersicht

[cite_start]In dieser Übung wird ein numerischer Wert direkt vom ISOBUS-Terminal eingelesen, um die Tastrate eines PWM-Ausgangs (`Q1`) zu steuern[cite: 1].
Über das Objekt `InputNumber_PWM_Value` kann der Bediener am Bildschirm eine Zahl eingeben. Erst nach der Bestätigung mit "OK" wird das Ereignis `IND` gefeuert und der neue Wert an die PWM-Hardware übertragen. Dies ermöglicht die präzise manuelle Vorgabe von Leistungen (z.B. Lüfterdrehzahl oder Lampenhelligkeit) direkt über das Display.
