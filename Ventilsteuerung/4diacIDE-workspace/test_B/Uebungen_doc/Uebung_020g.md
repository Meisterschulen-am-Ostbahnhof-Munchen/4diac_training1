# Uebung_020g: Kombinierte Verzögerung (E_TONOF)

```{index} single: Uebung_020g: Kombinierte Verzögerung (E_TONOF)
```

[Uebung_020g](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020g.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020g`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020g.png)


## Ziel der Übung

Verwendung des Bausteins `E_TONOF`, der sowohl eine Einschalt- als auch eine Ausschaltverzögerung in einem Gehäuse bietet.

-----

## Funktionsweise

[cite_start]Der Baustein reagiert auf den Pegel am Eingang `IN`[cite: 1]:
*   Wechsel zu `TRUE`: Der Ausgang wird erst nach Ablauf von `PT_ON` (5s) aktiv.
*   Wechsel zu `FALSE`: Der Ausgang bleibt noch für die Zeit `PT_OFF` (5s) aktiv.

Dies filtert kurze Impulse (Störungen) am Eingang komplett heraus und sorgt gleichzeitig für einen definierten Nachlauf.
