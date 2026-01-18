# Uebung_004a9: Dreifach Event-Splitter (E_SPLIT_3)

```{index} single: Uebung_004a9: Dreifach Event-Splitter (E_SPLIT_3)
```

[Uebung_004a9](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004a9.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004a9`. Hier wird das Konzept des sequenziellen Event-Splittings auf drei Ziele erweitert.


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
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004a9.png)


## Ziel der Übung

Demonstration der Skalierbarkeit von Ereignis-Verteilern. Mit `E_SPLIT_3` können drei Prozesse mit einem einzigen Auslöser sequenziell angestoßen werden.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004a9.SUB` verteilt das Signal eines Tasters auf drei separate Toggle-Flip-Flops und somit auf drei Ausgänge[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1`**: Der zentrale Auslöser (Taster).
  * **`E_SPLIT_3`**: Verteilt den Eingang `EI` nacheinander auf `EO1`, `EO2` und `EO3`.
  * **`E_T_FF_Q1`, `Q2`, `Q3`**: Drei unabhängige Flip-Flops.
  * **`DigitalOutput_Q1`, `Q2`, `Q3`**: Drei physische Lampen.

-----

## Funktionsweise

Ein einziger Klick auf den Taster löst eine definierte Ereigniskette aus:
1.  `EO1` feuert ➡️ `Q1` toggelt.
2.  `EO2` feuert ➡️ `Q2` toggelt.
3.  `EO3` feuert ➡️ `Q3` toggelt.

Die Abarbeitung erfolgt in der Steuerung so schnell, dass die Lampen für den Betrachter gleichzeitig umschalten, jedoch ist die interne Reihenfolge strikt vorgegeben.

-----

## Anwendungsbeispiel

**Szenen-Schaltung im Gebäude**:
Ein Taster an der Wohnungstür schaltet gleichzeitig die Beleuchtung im Flur (`Q1`), in der Küche (`Q2`) und im Außenbereich (`Q3`) um. Durch den Splitter wird sichergestellt, dass alle Funktionsblöcke den Trigger erhalten.