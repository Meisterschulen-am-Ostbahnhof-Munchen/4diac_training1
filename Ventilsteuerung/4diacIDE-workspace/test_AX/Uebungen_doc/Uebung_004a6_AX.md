# Uebung_004a6_AX: Event-Rendezvous (Synchronisation)

```{index} single: Uebung_004a6_AX: Event-Rendezvous (Synchronisation)
```

[Uebung_004a6_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004a6_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004a6_AX`. Hier wird ein komplexeres Event-Handling-Muster vorgestellt: Das Rendezvous. Ein Ereignis wird erst dann weitergegeben, wenn zwei Bedingungen (Events) eingetreten sind.


## 📺 Video

* [D-Flip-Flop: E_D_FF aus der IEC 61499 (Übung 002c) als "Eventbremse"](https://www.youtube.com/watch?v=yGSx_0ggveE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [E_REND: Ereignissynchronisation in IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_REND-Ereignissynchronisation-in-IEC-61499-e368co9)
* [E_TOF vs. FB_TOF: Der Event-Timer, der nicht zyklisch tickt – Revolution für Automatisierungssysteme?](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_TOF-vs--FB_TOF-Der-Event-Timer--der-nicht-zyklisch-tickt--Revolution-fr-Automatisierungssysteme-e3673qk)
* [EventFBs nach IEC 61499: Legosteine der Automatisierung – So funktionieren Ereignis-Funktionsbausteine](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/EventFBs-nach-IEC-61499-Legosteine-der-Automatisierung--So-funktionieren-Ereignis-Funktionsbausteine-e375gjm)
* [IEC 61499: Revolution der Automatisierung – Event-gesteuerte FBs und verteilte Systeme erklärt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Revolution-der-Automatisierung--Event-gesteuerte-FBs-und-verteilte-Systeme-erklrt-e3671vb)
* [E_REND: Event Synchronization in IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/E_REND-Event-Synchronization-in-IEC-61499-e368cv2)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004a6_AX.png)


## Ziel der Übung

Verständnis des `E_REND` Bausteins. Dieser Baustein fungiert wie ein "UND" für Ereignisse. Er merkt sich, welche Eingänge bereits gefeuert haben, und feuert erst am Ausgang, wenn *alle* erforderlichen Eingänge mindestens einmal aktiv waren. Danach setzt er sich zurück.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004a6_AX.SUB` nutzt `E_REND`, um sicherzustellen, dass zwei Taster gedrückt wurden, bevor das Licht umschaltet[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1` & `I2`**: Die beiden Bestätigungs-Taster.
  * **`DigitalInput_CLK_I3`**: Ein Reset-Taster.
  * **`E_REND`**: Der Rendezvous-Baustein mit Eingängen `EI1`, `EI2` und einem Reset `R`.
  * **`E_T_FF`**: Das Flip-Flop.
  * **`DigitalOutput_Q1`**: Die Lampe.

-----

## Funktionsweise

```xml
<EventConnections>
    <Connection Source="DigitalInput_CLK_I1.IND" Destination="E_REND.EI1"/>
    <Connection Source="DigitalInput_CLK_I2.IND" Destination="E_REND.EI2"/>
    <Connection Source="E_REND.EO" Destination="E_T_FF.CLK"/>
    <Connection Source="DigitalInput_CLK_I3.IND" Destination="E_REND.R"/>
</EventConnections>
```

[cite_start][cite: 1]

1.  Drückt man nur Taster 1 (`I1`), passiert nichts am Ausgang. `E_REND` merkt sich intern "EI1 war da".
2.  Drückt man danach Taster 2 (`I2`), ist die Bedingung komplett (beide waren da). `E_REND` feuert `EO`.
3.  Das Flip-Flop schaltet um, die Lampe ändert ihren Zustand.
4.  `E_REND` vergisst den Status und wartet erneut auf beide Events.

*   Der Reset-Taster (`I3`) kann genutzt werden, um den internen Merker des `E_REND` zu löschen, falls man z.B. nur Taster 1 gedrückt hat und den Vorgang abbrechen will.

-----

## Anwendungsbeispiel

**Zweihand-Auslösung (Sequenziell)**: Ein Prozess soll erst starten, wenn Bediener A "Freigabe" drückt UND Bediener B "Start" drückt (Reihenfolge egal, aber beide müssen einmal gedrückt haben).