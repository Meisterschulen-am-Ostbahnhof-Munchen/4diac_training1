# Uebung_024: Sequenz mit Wartezeit (Delay)

```{index} single: Uebung_024: Sequenz mit Wartezeit (Delay)
```

[Uebung_024](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_024.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_024`. Hier wird eine zeitliche Pause in den automatischen Ablauf integriert.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_024.png)


## Ziel der Übung

Integration von Zeitgliedern (`E_DELAY`) in eine Ereigniskette.

-----

## Funktionsweise

[cite_start]Im Vergleich zu Übung 023 wird zwischen zwei Schritten ein Verzögerungs-Baustein eingefügt[cite: 1].
Wenn Zylinder 2 seine Endlage erreicht (`F3`), wird nicht sofort der nächste Schritt ausgelöst, sondern der Eingang `E_DELAY.START` getriggert. Erst nach Ablauf der Zeit `DT` (hier 2 Sekunden) feuert das `EO`-Event und setzt die Sequenz fort (z.B. Start des Einfahrens).

-----

## Anwendungsbeispiel

**Pressvorgang**:
Ein Zylinder fährt aus und drückt zwei Bauteile zusammen. Sobald die Endlage erreicht ist, muss der Druck für 2 Sekunden gehalten werden (Wartezeit), bevor der Zylinder wieder einfährt und das Werkstück freigibt.
