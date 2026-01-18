# Uebung_020e_AX: Ausschaltverzögerung (TOF)

```{index} single: Uebung_020e_AX: Ausschaltverzögerung (TOF)
```

[Uebung_020e_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020e_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020e_AX`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020e_AX.png)


## Ziel der Übung

Kennenlernen des Timer-Bausteins `AX_TOF`.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_020e_AX.SUB` verzögert das Ausschaltsignal[cite: 1].

### Funktionsbausteine (FBs)

  * **`AX_TOF`**: Timer Off-Delay.
  * **Parameter `PT`**: Preset Time (hier 5 Sekunden).

-----

## Funktionsweise

1.  Eingang `I1` wird TRUE -> Lampe geht **sofort** an.
2.  Eingang `I1` wird FALSE -> Timer startet.
3.  Nach 5 Sekunden wird der Ausgang `Q` FALSE -> Lampe geht aus.

-----

## Anwendungsbeispiel

**Nachlauf**: Ein Lüfter im Bad läuft noch 5 Minuten nach, nachdem das Licht ausgeschaltet wurde.