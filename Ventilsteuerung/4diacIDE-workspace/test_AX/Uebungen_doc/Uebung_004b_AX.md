# Uebung_004b_AX: Komplexes Event-Switching (Anti-Pattern?)

```{index} single: Uebung_004b_AX: Komplexes Event-Switching (Anti-Pattern?)
```

[Uebung_004b_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004b_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004b_AX`. Diese Übung zeigt eine alternative Implementierung eines Stromstoßschalters unter Verwendung von Daten-zu-Event-Konvertierung und Weichen.

> **Hinweis:** Diese Lösung gilt als "nicht empfohlen" (siehe Kommentar im Code), da sie unnötig komplex ist. Sie dient hier als Lehrbeispiel für die Bausteine `AX_SWITCH`, `AX_BOOL_TO_X` und `AX_X_TO_BOOL`.


## 📺 Video

* [D-Flip-Flop: E_D_FF aus der IEC 61499 (Übung 002c) als "Eventbremse"](https://www.youtube.com/watch?v=yGSx_0ggveE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [E_TOF vs. FB_TOF: Der Event-Timer, der nicht zyklisch tickt – Revolution für Automatisierungssysteme?](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_TOF-vs--FB_TOF-Der-Event-Timer--der-nicht-zyklisch-tickt--Revolution-fr-Automatisierungssysteme-e3673qk)
* [EventFBs nach IEC 61499: Legosteine der Automatisierung – So funktionieren Ereignis-Funktionsbausteine](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/EventFBs-nach-IEC-61499-Legosteine-der-Automatisierung--So-funktionieren-Ereignis-Funktionsbausteine-e375gjm)
* [IEC 61499: Revolution der Automatisierung – Event-gesteuerte FBs und verteilte Systeme erklärt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Revolution-der-Automatisierung--Event-gesteuerte-FBs-und-verteilte-Systeme-erklrt-e3671vb)
* [E_REND: Event Synchronization in IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/E_REND-Event-Synchronization-in-IEC-61499-e368cv2)
* [The Unstoppable Counter: Why IEC 61499's ECTU Guarantees Safe, Event-Driven Control (and Never Overflows)](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/The-Unstoppable-Counter-Why-IEC-61499s-ECTU-Guarantees-Safe--Event-Driven-Control-and-Never-Overflows-e3a9qsh)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004b_AX.png)


## Ziel der Übung

Verständnis der Interaktion zwischen booleschen Daten und Event-Fluss-Steuerung.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004b_AX.SUB` baut einen Toggle-Mechanismus diskret auf[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1`**: Liefert ein Event bei Klick.
  * **`AX_BOOL_TO_X`**: Wandelt einen booleschen Wert in ein Adapter-Signal (Daten + Event) um. Hier genutzt, um den aktuellen Zustand des Flip-Flops in ein Steuersignal für den Switch zu wandeln.
  * **`AX_SWITCH`**: Eine Weiche. Je nach Wert am Eingang `G` leitet sie ein Event entweder an `EO0` oder `EO1`.
  * **`E_SR`**: Set/Reset Flip-Flop (Ereignisbasiert).
  * **`AX_SPLIT_2`**: Verteilt den Ausgang des Flip-Flops (einmal zur Lampe, einmal zur Rückkopplung).
  * **`AX_X_TO_BOOL`**: Extrahiert den booleschen Zustand aus dem Adapter-Signal für die Rückkopplung.

-----

## Funktionsweise

Der Grundgedanke ist:
1.  Ein Klick-Event kommt an.
2.  Wohin soll es gehen? -> Zum "Einschalten" (`S`) oder zum "Ausschalten" (`R`)?
3.  Das entscheidet der `AX_SWITCH` basierend auf dem *aktuellen* Zustand.
    *   Ist die Lampe aus (`G=0`), geht das Event zu `EO0` -> `E_SR.S` (Setzen).
    *   Ist die Lampe an (`G=1`), geht das Event zu `EO1` -> `E_SR.R` (Rücksetzen).

Diese Rückkopplungsschleife (Feedback Loop) macht aus dem SR-Flip-Flop effektiv ein Toggle-Flip-Flop.

-----

## Bewertung

Warum ist das "schlecht"?
*   Hoher Baustein-Aufwand für eine simple Funktion.
*   Rückkopplungsschleifen können in ereignisbasierten Systemen zu "Race Conditions" oder unendlichen Loops führen, wenn man nicht aufpasst (hier durch die Trennung von Event und Datenpfad zwar funktional, aber schwer lesbar).
*   Ein einfaches `AX_T_FF` (wie in Übung 004a) erledigt dasselbe in einem Baustein.