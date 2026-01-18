# Uebung_007a3: Sicherer Blinker (Definierter AUS-Zustand)

```{index} single: Uebung_007a3: Sicherer Blinker (Definierter AUS-Zustand)
```

[Uebung_007a3](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_007a3.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_007a3`. Hier wird die "saubere" Lösung für einen schaltbaren Blinker präsentiert, der beim Ausschalten garantiert in den Zustand "AUS" geht.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_007a3.png)


## Ziel der Übung

Realisierung eines Blinkers mit definiertem Stopp-Verhalten. Es wird demonstriert, wie Ereignispfade verknüpft werden müssen, um sowohl die Takterzeugung zu stoppen als auch den Zustandsspeicher zu löschen.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_007a3.SUB` wird die Blinklogik manuell aus Weiche und Speicher aufgebaut, um die volle Kontrolle über den Reset-Vorgang zu haben[cite: 1].

### Funktionsbausteine (FBs)

  * **`E_CYCLE`**: Der Taktgeber.
  * **`E_SWITCH`**: Die Ereignis-Weiche zur Realisierung der Toggle-Funktion.
  * **`E_SR`**: Der Speicherbaustein (Reset-dominant verschaltet).
  * **`START` & `STOP`**: Die Bedien-Taster.

-----

## Funktionsweise

Die Sicherheit wird durch eine doppelte Belegung des Stopp-Signals erreicht:

```xml
<EventConnections>
    <Connection Source="START.IND" Destination="E_CYCLE.START"/>
    <Connection Source="STOP.IND" Destination="E_CYCLE.STOP"/>
    <Connection Source="E_CYCLE.EO" Destination="E_SWITCH.EI"/>
    <Connection Source="E_SWITCH.EO0" Destination="E_SR.S"/>
    <Connection Source="E_SWITCH.EO1" Destination="E_SR.R"/>
    <!-- Die entscheidende Verbindung für die Sicherheit: -->
    <Connection Source="STOP.IND" Destination="E_SR.R"/>
</EventConnections>
```

[cite_start][cite: 1]

1.  **Blinkbetrieb**: Der `E_CYCLE` triggert die `E_SWITCH/E_SR` Kombination, was zum periodischen Umschalten führt.
2.  **Ausschalten**: Wenn der Nutzer `STOP` drückt, passieren zwei Dinge gleichzeitig:
    *   Der `E_CYCLE` wird angehalten (keine neuen Takte mehr).
    *   Der Speicher `E_SR` erhält einen **direkten Reset-Befehl**. Damit wird der Ausgang sofort auf `FALSE` gezwungen, egal ob das Flip-Flop gerade im "An"- oder "Aus"-Zustand war.

-----

## Anwendungsbeispiel

**Professionelle Warnsignalisierung**:
Ein akustischer Alarm oder eine Blitzleuchte an einer Maschine muss bei Quittierung sofort und zuverlässig verstummen. Ein "Hängenbleiben" im eingeschalteten Zustand wäre irreführend und störend. Diese Schaltung garantiert, dass der Alarm nach dem Ausschalten immer inaktiv ist.