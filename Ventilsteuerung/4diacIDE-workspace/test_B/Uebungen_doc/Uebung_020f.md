# Uebung_020f: Impulsgeber (E_TP)

```{index} single: Uebung_020f: Impulsgeber (E_TP)
```

[Uebung_020f](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020f.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020f`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

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