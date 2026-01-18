# Uebung_004a9_AX: Event-Splitter 3-fach (E_SPLIT_3)

```{index} single: Uebung_004a9_AX: Event-Splitter 3-fach (E_SPLIT_3)
```

[Uebung_004a9_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004a9_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004a9_AX`. Hier wird das Konzept des Event-Splittings auf drei Ziele erweitert.


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



![](Uebung_004a9_AX.png)


## Ziel der Übung

Demonstration der Skalierbarkeit von Event-Verteilern. Mit `E_SPLIT_3` können drei Prozesse sequenziell angestoßen werden.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004a9_AX.SUB` verteilt das Signal eines Tasters auf drei separate Toggle-Flip-Flops und somit auf drei Ausgänge[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1`**: Taster.
  * **`E_SPLIT_3`**: Verteilt Eingang `EI` sequenziell auf `EO1`, `EO2` und `EO3`.
  * **`AX_T_FF_Q1`, `Q2`, `Q3`**: Drei Flip-Flops.
  * **`DigitalOutput_Q1`, `Q2`, `Q3`**: Drei Lampen.

-----

## Funktionsweise

```xml
<EventConnections>
    <Connection Source="DigitalInput_CLK_I1.IND" Destination="E_SPLIT_3.EI"/>
    <Connection Source="E_SPLIT_3.EO1" Destination="AX_T_FF_Q1.CLK"/>
    <Connection Source="E_SPLIT_3.EO2" Destination="AX_T_FF_Q2.CLK"/>
    <Connection Source="E_SPLIT_3.EO3" Destination="AX_T_FF_Q3.CLK"/>
</EventConnections>
```

[cite_start][cite: 1]

Ein einzelner Klick auf den Taster löst eine Kaskade aus:
1.  `EO1` feuert -> `Q1` toggelt.
2.  `EO2` feuert -> `Q2` toggelt.
3.  `EO3` feuert -> `Q3` toggelt.

Dies geschieht in der SPS-Zykluszeit so schnell, dass es für das menschliche Auge simultan wirkt, aber steuerungstechnisch ist es eine definierte Sequenz.

-----

## Anwendungsbeispiel

**Zentral-Schalter für eine Etage**: Ein Taster an der Wohnungstür schaltet Licht im Flur (`Q1`), Küche (`Q2`) und Wohnzimmer (`Q3`) gleichzeitig aus (oder um).