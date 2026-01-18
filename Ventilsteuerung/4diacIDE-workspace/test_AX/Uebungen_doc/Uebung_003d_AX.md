# Uebung_003d_AX: Wiederholung Parallelsteuerung

```{index} single: Uebung_003d_AX: Wiederholung Parallelsteuerung
```

[Uebung_003d_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003d_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_003d_AX`. Diese Übung ist strukturell nahezu identisch mit `Uebung_003_AX` und dient der Festigung des Verständnisses für parallele Signalpfade.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_003d_AX.png)


## Ziel der Übung

Das Ziel ist die Wiederholung der direkten I/O-Verknüpfung mittels Adapter-Technologie. Es wird sichergestellt, dass das Konzept der unabhängigen Datenflüsse verstanden wurde.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_003d_AX.SUB` verbindet zwei Eingänge mit zwei Ausgängen[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1`** -> **`DigitalOutput_Q1`**
  * **`DigitalInput_I2`** -> **`DigitalOutput_Q2`**

Die Bausteintypen sind `logiBUS_IXA` und `logiBUS_QXA`, verbunden über den Adapter `AX`.

-----

## Funktionsweise

Siehe `Uebung_003_AX`. Die Signale werden 1:1 und latenzarm von den Eingängen auf die Ausgänge durchgeschleift.

-----

## Anwendungsbeispiel

Diese Übung kann als Template für **einfache Verdrahtungstests** genutzt werden. Wenn man eine neue Steuerung in Betrieb nimmt, lädt man oft so ein "dummes" Programm hoch, um zu prüfen, ob physikalisch alles korrekt angeschlossen ist (Schalter betätigen -> LED geht an).