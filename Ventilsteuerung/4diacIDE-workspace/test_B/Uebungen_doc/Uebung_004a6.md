# Uebung_004a6: Event-Rendezvous (Synchronisation)

```{index} single: Uebung_004a6: Event-Rendezvous (Synchronisation)
```

[Uebung_004a6](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004a6.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004a6`. Hier wird ein fortgeschrittenes Ereignis-Muster vorgestellt: Das Rendezvous. Ein Ereignis wird erst dann weitergegeben, wenn mehrere unterschiedliche Bedingungen zeitunabhängig eingetroffen sind.


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
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004a6.png)


## Ziel der Übung

Erlernen des Umgangs mit dem `E_REND` Baustein. Dieser fungiert wie ein "Gedächtnis-UND" für Ereignisse. Er feuert erst am Ausgang, wenn an *allen* konfigurierten Eingängen mindestens einmal ein Ereignis registriert wurde. Dies dient der Synchronisation von asynchronen Prozessen.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004a6.SUB` nutzt `E_REND`, um sicherzustellen, dass zwei Taster gedrückt wurden, bevor der Ausgang umschaltet[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1` & `I2`**: Die beiden Taster für die Synchronisation.
  * **`DigitalInput_CLK_I3`**: Ein Reset-Taster zum Löschen der Vorbedingungen.
  * **`E_REND`**: Der Rendezvous-Baustein mit Eingängen `EI1`, `EI2` und einem Reset-Eingang `R`.
  * **`E_T_FF`**: Das Flip-Flop zur Zustandsspeicherung.

-----

## Funktionsweise

Die Logik verlangt die Bestätigung beider Quellen:

```xml
<EventConnections>
    <Connection Source="DigitalInput_CLK_I1.IND" Destination="E_REND.EI1"/>
    <Connection Source="DigitalInput_CLK_I2.IND" Destination="E_REND.EI2"/>
    <Connection Source="E_REND.EO" Destination="E_T_FF.CLK"/>
    <Connection Source="DigitalInput_CLK_I3.IND" Destination="E_REND.R"/>
</EventConnections>
```

[cite_start][cite: 1]

Der funktionale Ablauf:
1.  Drückt man nur Taster 1 (`I1`), passiert am Ausgang nichts. `E_REND` speichert intern: "EI1 ist erledigt".
2.  Drückt man irgendwann später Taster 2 (`I2`), ist die Bedingung erfüllt (beide waren da). `E_REND` feuert nun das Event an `EO`.
3.  Das Flip-Flop toggelt den Ausgangszustand.
4.  Danach setzt sich `E_REND` automatisch zurück und wartet erneut auf beide Eingänge.

*   Der Reset-Taster (`I3`) kann jederzeit genutzt werden, um die internen Merker von `E_REND` zu löschen (Abbruch der Sequenz).

-----

## Anwendungsbeispiel

**Sequenzielle Freigabe**:
In einer Montagehalle muss ein Monteur den Zusammenbau bestätigen (`I1`) und ein Qualitätskontrolleur die Prüfung abnehmen (`I2`). Erst wenn beide (unabhängig voneinander und in beliebiger Reihenfolge) ihre Quittierung gegeben haben, darf das Förderband zum nächsten Schritt weiterschalten (`EO`).