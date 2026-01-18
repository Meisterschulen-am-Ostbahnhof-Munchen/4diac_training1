# Uebung_020c: Einschaltverzögerung (E_TON)

```{index} single: Uebung_020c: Einschaltverzögerung (E_TON)
```

[Uebung_020c](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020c.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020c`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020c.png)


## Ziel der Übung

Nutzung des standardisierten Timer-Bausteins `E_TON`.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_020c.SUB` nutzt den `E_TON` Baustein aus der Event-Timer-Bibliothek[cite: 1].

### Funktionsbausteine (FBs)

  * **`E_TON`**: Timer ON-Delay (Ereignisbasiert).
  * **Parameter `PT`**: Preset Time (hier 5 Sekunden).

-----

## Funktionsweise

Der Baustein vereinfacht den Aufbau aus Übung 020b erheblich:
*   Eingang `I1` wird TRUE ➡️ Timer startet.
*   Nach 5s wird der Ausgang `Q` TRUE.
*   Eingang `I1` wird FALSE ➡️ Timer bricht ab, Ausgang wird sofort FALSE.

Dies ist der Standardweg, um Verzögerungen in 4diac zu realisieren.