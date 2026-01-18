# Uebung_010b3_AX: AUX Event (AuxDisabled_START)

```{index} single: Uebung_010b3_AX: AUX Event (AuxDisabled_START)
```

[Uebung_010b3_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b3_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010b3_AX`.


## 📺 Video

* [D-Flip-Flop: E_D_FF aus der IEC 61499 (Übung 002c) als "Eventbremse"](https://www.youtube.com/watch?v=yGSx_0ggveE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [E_TOF vs. FB_TOF: Der Event-Timer, der nicht zyklisch tickt – Revolution für Automatisierungssysteme?](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_TOF-vs--FB_TOF-Der-Event-Timer--der-nicht-zyklisch-tickt--Revolution-fr-Automatisierungssysteme-e3673qk)
* [Ereignisse und IEC 61499: Der Startschuss für intelligente Systeme](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Ereignisse-und-IEC-61499-Der-Startschuss-fr-intelligente-Systeme-e368461)
* [EventFBs nach IEC 61499: Legosteine der Automatisierung – So funktionieren Ereignis-Funktionsbausteine](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/EventFBs-nach-IEC-61499-Legosteine-der-Automatisierung--So-funktionieren-Ereignis-Funktionsbausteine-e375gjm)
* [IEC 61499: Revolution der Automatisierung – Event-gesteuerte FBs und verteilte Systeme erklärt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Revolution-der-Automatisierung--Event-gesteuerte-FBs-und-verteilte-Systeme-erklrt-e3671vb)
* [E_REND: Event Synchronization in IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/E_REND-Event-Synchronization-in-IEC-61499-e368cv2)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010b3_AX.png)


## Ziel der Übung

Verwendung von `Aux_IE` (Event).

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_010b3_AX.SUB` toggelt ein Flip-Flop über AUX[cite: 1].

### Funktionsbausteine (FBs)

  * **`AuxFunction2_X1_UP`**: Typ `isobus::UT::io::Auxiliary::IN::Aux_IE`.
  * **InputEvent**: `AuxDisabled_START`.

-----

## Funktionsweise

Das Event-Namensschema bei AUX ist etwas speziell:
*   `AuxDisabled`: Bedeutet, der Schalter ist "Aus" (Offen).
*   `AuxEnabled`: Bedeutet, der Schalter ist "Ein" (Geschlossen).
*   `_START`: Bedeutet Flanke (Übergang in diesen Zustand).

`AuxDisabled_START` bedeutet also: Der Übergang von "Enabled" zu "Disabled". Das entspricht dem **Loslassen** eines Tasters (`Falling Edge`). Das Flip-Flop schaltet also beim Loslassen der Joystick-Taste um.