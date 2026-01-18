# Uebung_010b3: AUX-Ereignis-Steuerung

```{index} single: Uebung_010b3: AUX-Ereignis-Steuerung
```

[Uebung_010b3](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b3.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010b3`.


## 📺 Video

* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [DIN EN 61499: Industrielle Steuerungen modular und ereignisbasiert mit Funktionsbausteinen meiste...](https://www.youtube.com/watch?v=fD6yS9dQVLY)
* [Ereignisschalter E_SWITCH aus der IEC 61499 (Übung 86)](https://www.youtube.com/watch?v=Gev-kGR4-Tc)
* [Gesteuerte Verbreitung eines Ereignisses E_PERMIT aus der IEC 61499 (Übung 94)](https://www.youtube.com/watch?v=ry5LTRd9H3M)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)

## Podcast
* [DIN EN 61499-1: Die Lego-Steine für flexible und ereignisgesteuerte Industriesteuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Die-Lego-Steine-fr-flexible-und-ereignisgesteuerte-Industriesteuerungen-e3681o1)
* [DIN EN 61499-1: Revolution in der Steuerungstechnik – Modulare, ereignisgesteuerte Systeme verstehen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Revolution-in-der-Steuerungstechnik--Modulare--ereignisgesteuerte-Systeme-verstehen-e367nse)
* [DIN EN 61499: Industrielle Steuerungen modular und ereignisbasiert mit Funktionsbausteinen meistern – Der ESR-Schalter im Fokus](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-Industrielle-Steuerungen-modular-und-ereignisbasiert-mit-Funktionsbausteinen-meistern--Der-ESR-Schalter-im-Fokus-e367nra)
* [IEC 61499: Der E_SR-Baustein entschlüsselt – Einfachheit trifft Ereignissteuerung](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Der-E_SR-Baustein-entschlsselt--Einfachheit-trifft-Ereignissteuerung-e3682bo)
* [Meisterwissen 61499: Der Ereignisgesteuerte Aufwärtszähler (E_CTU) – Robustes Zählen in Landmaschinen-Steuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Meisterwissen-61499-Der-Ereignisgesteuerte-Aufwrtszhler-E_CTU--Robustes-Zhlen-in-Landmaschinen-Steuerungen-e3a9q5n)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010b3.png)


## Ziel der Übung

Verwendung von `Aux_IE` (Event) zur Steuerung von Speichern.

-----

## Beschreibung

[cite_start]In `Uebung_010b3.SUB` wird eine AUX-Funktion genutzt, um ein Flip-Flop zu toggeln[cite: 1].

### Funktionsweise

Es wird das Event `AuxDisabled_START` verwendet. In der ISOBUS-Terminologie bedeutet dies den Übergang in den Zustand "Deaktiviert". Das entspricht dem **Loslassen** einer Joystick-Taste. Das Flip-Flop wechselt also beim Loslassen der Taste seinen Zustand.