# Uebung_004a4_AX: Event-Splitter (E_SPLIT)

```{index} single: Uebung_004a4_AX: Event-Splitter (E_SPLIT)
```

[Uebung_004a4_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004a4_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004a4_AX`. Hier wird gezeigt, wie ein einzelnes Ereignis genutzt werden kann, um mehrere unabhängige Prozesse anzustoßen, indem man einen `E_SPLIT` Baustein verwendet.


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



![](Uebung_004a4_AX.png)


## Ziel der Übung

Das Ziel ist das Verständnis der sequenziellen Event-Verarbeitung. In IEC 61499 kann ein Event-Ausgang oft nur mit einem Event-Eingang verbunden sein (Fan-Out = 1), oder man möchte explizit die Reihenfolge der Abarbeitung steuern. Der `E_SPLIT` Baustein nimmt ein Eingangs-Event und feuert nacheinander Ausgänge ab.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004a4_AX.SUB` verwendet einen Taster, um zwei separate Toggle-Flip-Flops zu schalten[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1`**: Der Event-Generator (Taster).
  * **`E_SPLIT`**: Ein Event-Verteiler. Er hat einen Eingang `EI` und zwei Ausgänge `EO1` und `EO2`.
  * **`E_T_FF_Q1` & `Q2`**: Zwei unabhängige Flip-Flops.
  * **`DigitalOutput_Q1` & `Q2`**: Zwei Lampen.

-----

## Funktionsweise

```xml
<EventConnections>
    <Connection Source="DigitalInput_CLK_I1.IND" Destination="E_SPLIT.EI"/>
    <Connection Source="E_SPLIT.EO1" Destination="E_T_FF_Q1.CLK"/>
    <Connection Source="E_SPLIT.EO2" Destination="E_T_FF_Q2.CLK"/>
</EventConnections>
```

[cite_start][cite: 1]

1.  Ein Klick auf Taster 1 sendet ein Event an `E_SPLIT`.
2.  `E_SPLIT` sendet **zuerst** ein Event an `EO1` -> `E_T_FF_Q1` schaltet um.
3.  Danach (quasi zeitgleich, aber logisch danach) sendet `E_SPLIT` ein Event an `EO2` -> `E_T_FF_Q2` schaltet um.

Beide Lampen schalten somit synchron um, gesteuert durch einen Taster.

*(Hinweis im Code: "hier 2x T_FF zu verwenden ist sinnlos, das soll nur zeigen wie man E_SPLIT verwenden kann." - Das stimmt, man hätte auch beide Ausgänge an ein FF hängen können. Hier geht es rein um die Demonstration des Event-Splittings.)*

-----

## Anwendungsbeispiel

**Szenen-Steuerung**: Ein Taster "Feierabend" betätigt gleichzeitig (bzw. nacheinander) mehrere Aktionen: Licht ausschalten (`Q1`) und Alarmanlage scharfschalten (`Q2`). Durch den Splitter wird sichergestellt, dass beide Funktionsketten angestoßen werden.