# Uebung_034b: Dynamische PWM-Tastung (Hold)

```{index} single: Uebung_034b: Dynamische PWM-Tastung (Hold)
```

[Uebung_034b](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_034b.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_034b`. Hier wird die PWM-Leistung über Taster-Interaktionen ("Gas geben") gesteuert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [ISOBUS Object Pointer: Das Geheimnis dynamischer Displays und effizienter Fehlerdiagnose](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Object-Pointer-Das-Geheimnis-dynamischer-Displays-und-effizienter-Fehlerdiagnose-e36bp75)
* [ISOBUS Output Meter: Dynamische Anzeigen meistern – vom Zeiger bis zur Visualisierung auf dem VT](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Output-Meter-Dynamische-Anzeigen-meistern--vom-Zeiger-bis-zur-Visualisierung-auf-dem-VT-e36t2tp)
* [ISOBUS-Container: Dynamische Bedienfelder für klare Sicht und mehr Effizienz](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Container-Dynamische-Bedienfelder-fr-klare-Sicht-und-mehr-Effizienz-e36alr9)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_034b.png)


## Ziel der Übung

Kombination von repetierenden Ereignissen (`HOLD`) und Zählern zur Steuerung einer PWM-Stufe. Der Nutzer kann die Leistung durch Festhalten eines Tasters stufenweise erhöhen oder verringern.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_034b.SUB` wird ein Up/Down-Zähler als digitaler Integrator genutzt[cite: 1].

### Funktionsbausteine (FBs)

  * **`IE_SPEED_UP`**: Sendet alle 200ms ein Event, solange Taster **I1** gehalten wird.
  * **`IE_SPEED_DOWN`**: Sendet alle 200ms ein Event, solange Taster **I2** gehalten wird.
  * **`E_CTUD_UDINT`**: Speichert den aktuellen "Leistungs-Zählerstand".
  * **`F_MUL`**: Skaliert den Zählerstand (hier Faktor 8) auf den Zielbereich für den PWM-Baustein.
  * **`PWMOutput_Q1`**: Der Leistungsausgang.

-----

## Funktionsweise

1.  **Steigern**: Der Bediener hält **I1** gedrückt. Der Zähler zählt alle 200ms einen Schritt hoch. Die Lampe an `Q1` wird stufenweise heller.
2.  **Senken**: Der Bediener hält **I2** gedrückt. Die Lampe wird stufenweise dunkler.
3.  **Schnell-Wahl**: Taster **I3** (Stopp) setzt den Wert sofort auf 0. Taster **I4** (Full) lädt den Zähler sofort auf das Maximum.

Dies ermöglicht eine sehr feinfühlige Steuerung von Antrieben oder Beleuchtungen über einfache digitale Taster.