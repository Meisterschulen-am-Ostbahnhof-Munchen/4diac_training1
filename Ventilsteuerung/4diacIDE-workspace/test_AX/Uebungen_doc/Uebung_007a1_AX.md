# Uebung_007a1_AX: Schaltbarer Blinker (Problembehaftet)

```{index} single: Uebung_007a1_AX: Schaltbarer Blinker (Problembehaftet)
```

[Uebung_007a1_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_007a1_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_007a1_AX`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_007a1_AX.png)


## Ziel der Übung

Starten und Stoppen des Blinkers.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_007a1_AX.SUB` nutzt die Eingänge `START` und `STOP` des `E_CYCLE` Bausteins[cite: 1].

### Funktionsbausteine (FBs)

  * **`START` (I1)**: Startet den Zyklus.
  * **`STOP` (I2)**: Stoppt den Zyklus.
  * **`E_CYCLE`**: Generiert Events nur, wenn er gestartet ist.

-----

## Problem

Wie im Kommentar der Subapplikation vermerkt ("dieser Blinker bleibt zufällig auf AN oder AUS stehen"):
Wenn man `STOP` drückt, hört der `E_CYCLE` auf, Events zu senden. Das Flip-Flop `AX_T_FF` behält aber seinen *letzten* Zustand bei. War die Lampe gerade an, bleibt sie dauerhaft an. Das ist meistens nicht gewünscht (eine gestoppte Warnleuchte sollte aus sein).

-----

## Anwendungsbeispiel

Zeigt, warum man beim Design von Zustandsautomaten den "Stopp-Zustand" definieren muss.