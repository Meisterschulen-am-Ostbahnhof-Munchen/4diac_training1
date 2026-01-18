# Uebung_038_AX: Lauflicht (Zeitgesteuert)

```{index} single: Uebung_038_AX: Lauflicht (Zeitgesteuert)
```

[Uebung_038_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_038_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_038_AX`. Wir bauen eine klassische Schrittkette (Sequencer).


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_038_AX.png)


## Ziel der Übung

Realisierung einer automatischen Abfolge von 8 Schritten.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_038_AX.SUB` verwendet einen Sequenzer-Baustein, um 8 Ausgänge nacheinander zu schalten[cite: 1].

### Funktionsbausteine (FBs)

  * **`sequence_T_08_loop_AX`**: Ein komplexer Baustein, der 8 Zustände (`S1` bis `S8`) verwaltet. Der Übergang zwischen den Zuständen erfolgt zeitgesteuert.
  * **Parameter `DT_S1_S2` etc.**: Definieren die Verweildauer in jedem Schritt (z.B. 200ms oder 100ms).
  * **`Q_NumericValue`**: Zeigt die aktuelle Schrittnummer auf dem ISOBUS-Terminal an.
  * **`E_TimeOut`**: Überwacht die Sequenz (Watchdog).

-----

## Funktionsweise

1.  Start durch Taster `I1` -> Sequenz springt zu `S1`.
2.  Ausgang `DO_S1` wird aktiv -> `Q1` leuchtet.
3.  Nach `T#200ms` wechselt die Sequenz automatisch zu `S2`.
4.  `DO_S1` geht aus, `DO_S2` geht an -> `Q2` leuchtet.
5.  ... das geht so weiter bis `S8`.
6.  Nach `S8` springt sie wieder zu `S1` (Loop).
7.  Reset durch Taster `I4` -> Alles aus.

-----

## Anwendungsbeispiel

**Werbe-Beleuchtung** oder **Prozess-Steuerung**: Zuerst Wasser einlassen, dann heizen, dann waschen, dann abpumpen.