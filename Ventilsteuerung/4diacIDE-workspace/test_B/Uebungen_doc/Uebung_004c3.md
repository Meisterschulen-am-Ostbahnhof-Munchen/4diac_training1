# Uebung_004c3: Langer Tastendruck (Release-Event)

```{index} single: Uebung_004c3: Langer Tastendruck (Release-Event)
```

[Uebung_004c3](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004c3.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004c3`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004c3.png)


## Ziel der Übung

Nutzung des Ereignisses `BUTTON_LONG_PRESS_UP`.

-----

## Funktionsweise

[cite_start]Der Baustein `DigitalInput_CLK_I1` in `Uebung_004c3.SUB` erkennt das Ende eines langen Drucks[cite: 1].

Im Gegensatz zum `START`-Event feuert `LONG_PRESS_UP` erst dann, wenn der Nutzer den Taster **wieder loslässt**, sofern dieser vorher lange genug gedrückt wurde. Dies ermöglicht es, Aktionen genau am Ende einer Interaktion auszulösen.

-----

## Anwendungsbeispiel

**Bestätigungs-Dialog**: Der Nutzer muss eine Taste lange gedrückt halten, um sicherzugehen, dass er die Aktion will. Die Ausführung (z.B. "Motor starten") erfolgt erst beim Loslassen als finale Bestätigung.
