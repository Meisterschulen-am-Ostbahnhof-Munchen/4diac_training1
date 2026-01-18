# Uebung_003c_AX: Mapping auf ISOBUS AUX

```{index} single: Uebung_003c_AX: Mapping auf ISOBUS AUX
```

[Uebung_003c_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003c_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_003c_AX`. Diese Übung demonstriert die Anbindung von lokalen digitalen Eingängen an das ISOBUS-System als "Auxiliary Inputs". Dies ermöglicht die Nutzung lokaler Schalter zur Steuerung von ISOBUS-Geräten.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-08-17 14-05-25 Vorstellung logiBUS® neues IO System ohne Mapping](https://www.youtube.com/watch?v=5YnRsE5zVBk)
* [2025-08-17 14-39-09 logiBUS® Umwandeln eines Projektes mit Mapping in eines ohne Mapping.](https://www.youtube.com/watch?v=w8nTLn8fQxQ)

## Podcast
* [Das Working Set Objekt: Das Gehirn der ISOBUS-Bedienoberfläche verstehen – Von der Norm zur Praxis im ISO-Designer](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/Das-Working-Set-Objekt-Das-Gehirn-der-ISOBUS-Bedienoberflche-verstehen--Von-der-Norm-zur-Praxis-im-ISO-Designer-e36cl5v)
* [ISOBUS Button: Mehr als nur ein Klick – Die Standardisierung der Landtechnik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Button-Mehr-als-nur-ein-Klick--Die-Standardisierung-der-Landtechnik-e3673rb)
* [ISOBUS Object Pointer: Das Geheimnis dynamischer Displays und effizienter Fehlerdiagnose](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Object-Pointer-Das-Geheimnis-dynamischer-Displays-und-effizienter-Fehlerdiagnose-e36bp75)
* [ISOBUS Output Meter: Dynamische Anzeigen meistern – vom Zeiger bis zur Visualisierung auf dem VT](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Output-Meter-Dynamische-Anzeigen-meistern--vom-Zeiger-bis-zur-Visualisierung-auf-dem-VT-e36t2tp)
* [ISOBUS Skalierung: Wenn der Ackerschlepper-Bildschirm nicht passt – Eine Einführung in ISO 11783-6](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Skalierung-Wenn-der-Ackerschlepper-Bildschirm-nicht-passt--Eine-Einfhrung-in-ISO-11783-6-e36a8q6)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_003c_AX.png)


## Ziel der Übung

Das Ziel ist es, lokale Hardware-Eingänge (`I1` bis `I4`) für das ISOBUS-Netzwerk verfügbar zu machen. In der ISOBUS-Welt können Eingabegeräte (Joysticks, Schalterfelder) als "Auxiliary Inputs" definiert werden, die dann vom Benutzer flexibel auf Maschinenfunktionen gemappt werden können.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_003c_AX.SUB` nutzt untypisierte (bzw. wiederverwendete typisierte) Sub-Applikationen, um vier Kanäle zu definieren[cite: 1].

### Sub-Komponente: `Uebung_003c_sub_AX`

[cite_start]Dieser Sub-Baustein verbindet einen lokalen digitalen Eingang mit einem ISOBUS-Auxiliary-Ausgangsbaustein[cite: 2].
  * **Eingang**: `logiBUS_IXA` (Liest den lokalen Pin)
  * **Ausgang**: `Aux_QXA` (Sendet den Status als ISOBUS AUX Nachricht)
  * **Parameter**:
    * `Input`: Der lokale Eingang (z.B. `Input_I1`).
    * `iInpNr`: Die Nummer des AUX-Inputs im ISOBUS-Pool (Index 0 bis n).

### Konfiguration

Die Übung mappt vier Eingänge:
*   `F1`: `Input_I1` -> AUX Index 0
*   `F2`: `Input_I2` -> AUX Index 1 (implizit, Parameter-Mapping in der .SUB prüfen)
*   `F3`: `Input_I3` -> AUX Index 2
*   `F4`: `Input_I4` -> AUX Index 3

(Hinweis: In der bereitgestellten .SUB-Datei sind die Parameter `Input` und `iInpNr` nicht explizit bei den Instanzen `F1`...`F4` sichtbar, was typisch für untypisierte SubApps ist, wo die Werte im Inneren gesetzt sind. Bei einer sauberen typisierten Lösung wären diese Werte wie in `Uebung_003b3_AX` sichtbar.)

-----

## Funktionsweise

1.  Der Bediener betätigt Schalter `I1`.
2.  Der `logiBUS_IXA`-Baustein erfasst das Signal.
3.  Das Signal wird via Adapter an den `Aux_QXA`-Baustein weitergeleitet.
4.  Der `Aux_QXA`-Baustein generiert die entsprechende ISOBUS-Nachricht, dass der "Auxiliary Input 0" betätigt wurde.
5.  Ein angeschlossenes ISOBUS-Gerät (z.B. eine Feldspritze) empfängt dies und führt die Funktion aus, die der Benutzer diesem Schalter zugewiesen hat.

-----

## Anwendungsbeispiel

Ein **Nachrüst-Joystick**:

Ein älterer Traktor hat keinen ISOBUS-Joystick. Man installiert vier einfache Taster am Armaturenbrett und verbindet sie mit der Steuerung. Durch diese Software-Logik tauchen diese vier Taster plötzlich als vollwertige ISOBUS-Bedienelemente auf dem Terminal auf und können genutzt werden, um modernste Anbaugeräte zu steuern.