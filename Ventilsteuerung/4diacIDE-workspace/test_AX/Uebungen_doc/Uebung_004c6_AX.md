# Uebung_004c6_AX: Mehrfach-Klick (3-fach)

```{index} single: Uebung_004c6_AX: Mehrfach-Klick (3-fach)
```

[Uebung_004c6_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004c6_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004c6_AX`. Hier wird der erweiterte `logiBUS_IE2` Baustein genutzt, der Argumente akzeptiert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Von klickenden Relais zum intelligenten Code: Wie Software die Industriesteuerung revolutionierte](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Von-klickenden-Relais-zum-intelligenten-Code-Wie-Software-die-Industriesteuerung-revolutionierte-e375en3)
* [ISOBUS Button: Mehr als nur ein Klick – Die Standardisierung der Landtechnik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Button-Mehr-als-nur-ein-Klick--Die-Standardisierung-der-Landtechnik-e3673rb)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004c6_AX.png)


## Ziel der Übung

Konfiguration eines n-fach Klicks.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004c6_AX.SUB` nutzt `logiBUS_IE2` mit `InputEvent = BUTTON_MULTIPLE_CLICK` und `arg = 3`[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1`**: Typ `logiBUS_IE2`. Dieser Typ hat den zusätzlichen Eingang `arg`.

-----

## Funktionsweise

Das Event feuert nur, wenn der Benutzer exakt dreimal kurz hintereinander klickt (Triple-Click).

-----

## Anwendungsbeispiel

**Versteckte Service-Menüs**: Zugriff auf Experten-Einstellungen, die ein normaler Nutzer nicht versehentlich aktivieren soll.