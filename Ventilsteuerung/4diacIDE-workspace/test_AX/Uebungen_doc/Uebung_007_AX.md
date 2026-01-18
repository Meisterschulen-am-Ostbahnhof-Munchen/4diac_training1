# Uebung_007_AX: Einfacher Blinker (Taktgeber)

```{index} single: Uebung_007_AX: Einfacher Blinker (Taktgeber)
```

[Uebung_007_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_007_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_007_AX`. Hier wird gezeigt, wie man zeitgesteuerte Ereignisse erzeugt.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [logiBUS®: Revolutioniert die Agrarmechatronik – ISOBUS einfacher, offener, smarter](https://podcasters.spotify.com/pod/show/logibus/episodes/logiBUS-Revolutioniert-die-Agrarmechatronik--ISOBUS-einfacher--offener--smarter-e38b4kp)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_007_AX.png)


## Ziel der Übung

Erzeugung eines periodischen Blinksignals.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_007_AX.SUB` nutzt einen `E_CYCLE` Baustein in Kombination mit einem Flip-Flop[cite: 1].

### Funktionsbausteine (FBs)

  * **`E_CYCLE`**: Ein Ereignis-Generator. Er sendet periodisch Events am Ausgang `EO`. Der Parameter `DT` bestimmt die Periodendauer (hier `T#1s`).
  * **`AX_T_FF`**: Das Toggle-Flip-Flop.
  * **`DigitalOutput_Q1`**: Die Lampe.

-----

## Funktionsweise

1.  Der `E_CYCLE` Baustein feuert jede Sekunde ein Event.
2.  Das Event erreicht das Flip-Flop (`AX_T_FF.CLK`).
3.  Das Flip-Flop schaltet um (An -> Aus -> An ...).
4.  Die Lampe blinkt mit einer Frequenz von 0,5 Hz (1 Sekunde an, 1 Sekunde aus).

-----

## Anwendungsbeispiel

**Warnleuchte**: Eine Signallampe soll blinken, um Aufmerksamkeit zu erregen.