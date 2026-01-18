# Uebung_020f3: Integrierter Blinker (E_BLINK)

```{index} single: Uebung_020f3: Integrierter Blinker (E_BLINK)
```

[Uebung_020f3](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020f3.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020f3`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020f3.png)


## Übersicht

[cite_start]Verwendung des spezialisierten Blinker-Bausteins `E_BLINK`[cite: 1]. Dieser Baustein fasst die gesamte Logik der Übung 007a3 zusammen.
Über getrennte Parameter für `TIMELOW` und `TIMEHIGH` können asymmetrische Blinkmuster (z.B. kurzes Blitzen) einfach realisiert werden. Ein Ereignis am Eingang `START` setzt den Blinker in Gang.
