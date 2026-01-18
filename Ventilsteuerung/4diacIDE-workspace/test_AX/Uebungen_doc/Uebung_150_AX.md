# Uebung_150_AX: Impulszähler (Monitoring)

```{index} single: Uebung_150_AX: Impulszähler (Monitoring)
```

[Uebung_150_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_150_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_150_AX`. Hier nutzen wir den schnellen Zählereingang der Steuerung.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_150_AX.png)


## Ziel der Übung

Erfassung von schnellen Impulsen (z.B. Drehzahl, Durchfluss).

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_150_AX.SUB` kombiniert eine Standard-Beleuchtungslogik mit einem Impulszähler-Baustein[cite: 1].

### Funktionsbausteine (FBs)

  * **`logiBUS_PI_ID`**: Typ `PulseInput_ID`. Erfasst Impulse am Hardware-Eingang `I8`.
  * **`DigitalInput_I1`**: Taster für die Lampe.
  * **`AX_T_FF`**: Toggle für die Lampe.

-----

## Funktionsweise

Der Baustein `logiBUS_PI_ID` arbeitet im Hintergrund. Er zählt die Impulse am Eingang `I8`.
*   `ImpulseDelta = 100`: Der Baustein meldet sich (sendet ein Event), wenn 100 neue Impulse gezählt wurden.
*   `TimeDelta = 50000` (µs): Oder wenn 50ms vergangen sind.

Dies ermöglicht die Erfassung von Hochgeschwindigkeitssignalen, die für normale digitale Eingänge zu schnell wären. Die restliche Schaltung (`I1` auf `Q1`) läuft völlig unabhängig davon weiter.

-----

## Anwendungsbeispiel

**Radarsensor / Geschwindigkeitsmessung**: Ein Sensor am Rad liefert Impulse. Die Steuerung zählt diese, um die Fahrgeschwindigkeit des Traktors zu berechnen.