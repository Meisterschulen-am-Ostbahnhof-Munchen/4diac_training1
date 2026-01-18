# Uebung_006a2: Globaler Reset für mehrere Kanäle

```{index} single: Uebung_006a2: Globaler Reset für mehrere Kanäle
```

[Uebung_006a2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006a2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006a2`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_006a2.png)


## Ziel der Übung

Realisierung einer "Zentral-Aus" Funktion für mehrere unabhängige Speicherglieder.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006a2.SUB` steuert zwei separate Lampen (`Q1`, `Q2`) über zwei Taster (`I1`, `I2`), die durch einen dritten Taster (`I3`) gemeinsam zurückgesetzt werden können[cite: 1].

### Funktionsbausteine (FBs)

  * **2x `E_T_FF_SR`**: Einer für jeden Lichtkanal.
  * **`I1` & `I2`**: Tasten zum individuellen Umschalten der Kanäle.
  * **`I3`**: Gemeinsamer Reset-Taster.

-----

## Funktionsweise

Die Logik nutzt das Fan-Out Prinzip für Ereignisse:
*   `I1` ist mit `CLK` von Flip-Flop 1 verbunden.
*   `I2` ist mit `CLK` von Flip-Flop 2 verbunden.
*   `I3` (Reset) ist mit den `R`-Eingängen **beider** Flip-Flops verbunden.

Ein Druck auf `I3` schaltet sofort alle Lampen im System aus, unabhängig davon, in welchem Zustand sie sich vorher befanden.

-----

## Anwendungsbeispiel

**Werkstatt-Beleuchtung**: Jede Maschine hat ihr eigenes Arbeitslicht. Am Ende des Arbeitstages kann der Werkstattleiter über einen zentralen Schalter an der Tür alle Lichter gleichzeitig löschen.