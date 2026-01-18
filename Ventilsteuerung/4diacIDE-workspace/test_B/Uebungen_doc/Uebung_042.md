# Uebung_042: Signal-Skalierung (SCALE)

```{index} single: Uebung_042: Signal-Skalierung (SCALE)
```

[Uebung_042](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_042.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_042`. Hier wird die mathematische Umrechnung von Wertebereichen demonstriert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [R_TRIG & F_TRIG: So erkennen SPS-Steuerungen Signalflanken zuverlässig – ohne Doppelbehandlung](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/R_TRIG--F_TRIG-So-erkennen-SPS-Steuerungen-Signalflanken-zuverlssig--ohne-Doppelbehandlung-e370kqh)
* [ISOBUS Skalierung: Wenn der Ackerschlepper-Bildschirm nicht passt – Eine Einführung in ISO 11783-6](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Skalierung-Wenn-der-Ackerschlepper-Bildschirm-nicht-passt--Eine-Einfhrung-in-ISO-11783-6-e36a8q6)
* [Code-Renovierung mit AX-Adaptern: Wie Eclipse 4diac™ durch Signal-Bündelung Komplexität besiegt](https://podcasters.spotify.com/pod/show/logibus/episodes/Code-Renovierung-mit-AX-Adaptern-Wie-Eclipse-4diac-durch-Signal-Bndelung-Komplexitt-besiegt-e3ahcd1)
* [logiBUS® verstehen: Direkte Signalweiterleitung – Das "Hallo Welt" der Automatisierung](https://podcasters.spotify.com/pod/show/logibus/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg)
* [Das tödliche Dilemma des Relais: Warum Silberkontakte bei Kleinsignalen versagen und Gold bei Last schmilzt – Der Freibrenn-Effekt erklärt](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Das-tdliche-Dilemma-des-Relais-Warum-Silberkontakte-bei-Kleinsignalen-versagen-und-Gold-bei-Last-schmilzt--Der-Freibrenn-Effekt-erklrt-e3a9lhv)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_042.png)


## Ziel der Übung

Verwendung des Bausteins `SCALE`. In der Automatisierungstechnik müssen Rohwerte (z.B. 4-20 mA) oft in physikalische Größen (z.B. 0-10 Bar) umgerechnet werden. Der Scale-Baustein übernimmt diese lineare Abbildung.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_042.SUB` wird ein Test-Szenario für den Skalierungs-Baustein aufgebaut[cite: 1].

### Funktionsbausteine (FBs)

  * **`SCALE`**: Der Umrechnungs-Baustein.
  * **Parameter**:
    * `MIN_IN` / `MAX_IN`: Der Quell-Bereich (hier 4.0 bis 20.0).
    * `MIN_OUT` / `MAX_OUT`: Der Ziel-Bereich (hier 0.0 bis 100.0).
    * `IN`: Der aktuelle Eingangswert (hier fest auf 10.0 gesetzt).

-----

## Funktionsweise

Sobald das Ereignis `REQ` (hier durch Taster **I1** ausgelöst) eintrifft, berechnet der Baustein die Position des Eingangswerts im Quell-Bereich und bildet diese proportional auf den Ziel-Bereich ab.
Bei `IN = 10.0` (genau in der Mitte zwischen 4 und 20 ist es nicht ganz, aber mathematisch definiert) liefert der Baustein das entsprechende Ergebnis am Ausgang.

-----

## Anwendungsbeispiel

**Sensorkalibrierung**:
Ein Drucksensor liefert Werte zwischen 400 (Vakuum) und 2000 (Maximaldruck). Für die Anzeige am Terminal soll dies als 0% bis 100% dargestellt werden. Der `SCALE`-Baustein übernimmt diese Aufgabe, sodass die Logik immer mit intuitiven Prozentwerten arbeiten kann.