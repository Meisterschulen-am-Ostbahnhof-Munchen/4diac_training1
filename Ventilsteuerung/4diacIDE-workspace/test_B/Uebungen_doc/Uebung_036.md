# Uebung_036: Event-gesteuerte Schrittkette

```{index} single: Uebung_036: Event-gesteuerte Schrittkette
```

[Uebung_036](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_036.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_036`. Im Gegensatz zu Übung 035 liegt hier der Fokus auf der manuellen Weiterschaltung durch Ereignisse.

## 📺 Video

* [2025-01-28 20-01-36 logiBUS® Projektupdate und EInit (jetzt mit Ton)](https://www.youtube.com/watch?v=h-tzDyRtiHo)
* [2025-02-23 11-18-57 Einstieg in Autodesk Fusion 360 - Mechanisches Design MCAD](https://www.youtube.com/watch?v=3bmFKBpIpZY)
* [2025-02-23 11-43-44 Fusion 360 Übersicht Tutorials](https://www.youtube.com/watch?v=djM9ndIfp-0)
* [2025-02-23 11-47-07 Fusion 360 Elektronik Einführung](https://www.youtube.com/watch?v=uZb-U6FArGw)
* [2025-02-23 13-20-15 Fusion 360 Elektronik Stückliste Exportieren](https://www.youtube.com/watch?v=Z5RllKgpOfc)

----

![](Uebung_036.png)

## Ziel der Übung

Realisierung einer Schrittkette ohne automatische Zeitübergänge.

-----

## Funktionsweise

[cite_start]In `Uebung_036.SUB` sind die Zeitparameter `DT_S1_S2` und `DT_S2_S3` auf den Wert `NO_TIME` gesetzt[cite: 1].
Das bedeutet: Der Sequenzer bleibt in Schritt 1 stehen, bis er ein explizites Ereignis am Eingang `S1_S2` erhält. In dieser Übung wird dies durch den Taster **I2** ausgelöst. Analog schaltet Taster **I3** von Schritt 2 zu 3 weiter. Erst die letzten Schritte nutzen wieder die Zeitautomatik (2s).

-----

## Anwendungsbeispiel

**Manueller Bestückungsprozess**:
Ein Mitarbeiter legt ein Teil ein und drückt "Fertig" (`I2`). Die Maschine führt den ersten Bearbeitungsschritt aus. Danach wartet sie wieder auf die Freigabe des Mitarbeiters (`I3`), bevor sie weitermacht. Die Schrittkette passt sich so dem Arbeitstempo des Menschen an.