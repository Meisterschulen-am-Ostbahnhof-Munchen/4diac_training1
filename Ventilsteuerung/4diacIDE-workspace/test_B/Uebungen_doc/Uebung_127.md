# Uebung_127: Zyklisches Senden (Statische Daten)

```{index} single: Uebung_127: Zyklisches Senden (Statische Daten)
```

[Uebung_127](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_127.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_127`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_127.png)


## Übersicht

[cite_start]Variante des zyklischen Sendens unter Verwendung von `AlPgnTxNew8Bcycl` ohne Callback[cite: 1].
In dieser Übung werden die zu sendenden Daten fest als Parameter am Baustein hinterlegt. Ein Ereignis am Eingang `UPD` (Update) ermöglicht es der Applikation jedoch, den Inhalt der Nachricht bei Bedarf zu ändern. Dies ist eine einfachere Alternative zum Callback, wenn sich die Daten nicht in jedem Zyklus ändern.
