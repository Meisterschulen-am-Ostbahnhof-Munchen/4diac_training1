# Uebung_020f3_AX: Blinker (AX_BLINK)

```{index} single: Uebung_020f3_AX: Blinker (AX_BLINK)
```

[Uebung_020f3_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020f3_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020f3_AX`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [4diac IDE: Dein "Hello World" der Automatisierung – Das Blinking Tutorial Lokal](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/4diac-IDE-Dein-Hello-World-der-Automatisierung--Das-Blinking-Tutorial-Lokal-e36971r)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020f3_AX.png)


## Ziel der Übung

Verwendung des `AX_BLINK` Bausteins für asymmetrisches Blinken.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_020f3_AX.SUB` nutzt einen spezialisierten Blinker-Baustein[cite: 1].

### Funktionsbausteine (FBs)

  * **`AX_BLINK`**: Erzeugt ein Blinksignal.
  * **Parameter `TIMELOW`**: Zeit für "Aus" (1s).
  * **Parameter `TIMEHIGH`**: Zeit für "An" (1.2s).

-----

## Funktionsweise

Ein Event am Eingang `START` (hier vom Taster `I1` geliefert) startet den Blinker. Er läuft dann mit den parametrierten Zeiten. Der Baustein integriert im Grunde die Logik von zwei Timern und einem Flip-Flop.

-----

## Anwendungsbeispiel

**Fehlercode**: Eine LED blinkt in einem bestimmten Muster (kurz an, lang aus), um einen Fehlercode zu signalisieren.