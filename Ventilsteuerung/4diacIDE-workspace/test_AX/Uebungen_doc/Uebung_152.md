# Uebung_152: PI-Regelung (Drehzahlregelung)

```{index} single: Uebung_152: PI-Regelung (Drehzahlregelung)
```

[Uebung_152](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_152.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_152`. Hier wird eine geschlossene Regelschleife (Closed Loop) implementiert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_152.png)


## Ziel der Übung

Implementierung eines PI-Reglers zur Konstanthaltung einer physikalischen Größe.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_152.SUB` verbindet Sensorik, Regelung und Aktorik[cite: 1].

### Regelkreis-Komponenten

  * **Sensor (Ist-Wert)**: Impulszähler `logiBUS_PI_ID` + Ableitung `FT_DERIV` (berechnet z.B. die aktuelle Drehzahl).
  * **Regler**: `CTRL_PI` (OSCAT). Er vergleicht den Sollwert (`SET = 16.0`) mit dem Ist-Wert.
  * **Aktor (Stellgröße)**: `logiBUS_QD_PWM`. Ein pulsweitenmodulierter Ausgang, der z.B. einen Motor oder ein Ventil ansteuert.
  * **Bedienung**: Taster `I2` (Start) und `I3` (Stop) steuern den Zyklus. Taster `I1` schaltet zwischen Hand- und Automatikbetrieb um (`MAN` Eingang am Regler).

-----

## Funktionsweise

Der Regler versucht ständig, die Stellgröße am PWM-Ausgang so anzupassen, dass die gemessene Impulsrate dem Sollwert entspricht.
*   Wird das System belastet (Drehzahl sinkt), erhöht der Regler das PWM-Verhältnis.
*   Wird es zu schnell, drosselt er.

-----

## Anwendungsbeispiel

**Tempomat** oder **Konstanthaltung der Ausbringmenge**: Egal ob der Traktor bergauf oder bergab fährt, die Drehzahl der Säwelle soll exakt gleich bleiben.