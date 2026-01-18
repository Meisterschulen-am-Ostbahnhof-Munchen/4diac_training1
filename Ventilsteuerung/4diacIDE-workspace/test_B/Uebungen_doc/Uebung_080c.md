# Uebung_080c: Frequenzhalbierung von Events

```{index} single: Uebung_080c: Frequenzhalbierung von Events
```

[Uebung_080c](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_080c.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_080c`. Hier wird das Gegenteil der vorherigen Übung gezeigt: Die Reduzierung der Ereignisanzahl um die Hälfte.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Taster & Events: GPIO-Grundlagen für Land- und Baumaschinen Mechatroniker](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Taster--Events-GPIO-Grundlagen-fr-Land--und-Baumaschinen-Mechatroniker-e36aaen)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_080c.png)


## Ziel der Übung

Manipulation von Ereignisströmen unter Verwendung von `E_T_FF` und `E_PERMIT`.

-----

## Funktionsweise

[cite_start]In `Uebung_080c.SUB` wird ein Toggle-Flip-Flop als Gate-Wächter genutzt[cite: 1].
1.  Jeder Klick auf **I1** toggelt das Flip-Flop. Der Zustand wechselt also: TRUE, FALSE, TRUE, FALSE...
2.  Das `E_PERMIT` lässt Ereignisse nur durch, wenn der `PERMIT` Eingang auf TRUE steht.
3.  Daher wird nur bei jedem zweiten Klick (wenn das Flip-Flop gerade auf TRUE steht) ein Ereignis an den Zähler weitergereicht.

**Ergebnis**: Um die Lampe `Q1` (Schwelle 5) zum Leuchten zu bringen, muss der Nutzer nun 10 mal auf den Taster klicken.

-----

## Anwendungsbeispiel

Unterdrückung von Prell-Effekten oder grobe Skalierung von schnellen Sensorsignalen, um die Rechenlast der nachfolgenden Logik zu verringern.