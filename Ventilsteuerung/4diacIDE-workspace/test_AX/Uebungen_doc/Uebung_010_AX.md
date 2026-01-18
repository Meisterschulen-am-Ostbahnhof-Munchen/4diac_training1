# Uebung_010_AX: ISOBUS Softkey (Direkt)

```{index} single: Uebung_010_AX: ISOBUS Softkey (Direkt)
```

[Uebung_010_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010_AX`. Hier betreten wir die Welt des ISOBUS (ISO 11783). Anstelle von physischen Eingängen nutzen wir virtuelle Tasten auf einem Terminal (Universal Terminal, UT).


## 📺 Video

* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [E_CTUD: Bidirektionaler Zähler in IEC 61499 Systemen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_CTUD-Bidirektionaler-Zhler-in-IEC-61499-Systemen-e368lmb)
* [Das Working Set Objekt: Das Gehirn der ISOBUS-Bedienoberfläche verstehen – Von der Norm zur Praxis im ISO-Designer](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/Das-Working-Set-Objekt-Das-Gehirn-der-ISOBUS-Bedienoberflche-verstehen--Von-der-Norm-zur-Praxis-im-ISO-Designer-e36cl5v)
* [ISO 11783-6: Softkeys und das Virtual Terminal verstehen – Dein Schlüssel zur Landmaschinen-Mechatronik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISO-11783-6-Softkeys-und-das-Virtual-Terminal-verstehen--Dein-Schlssel-zur-Landmaschinen-Mechatronik-e36a8b0)
* [ISOBUS Button: Mehr als nur ein Klick – Die Standardisierung der Landtechnik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Button-Mehr-als-nur-ein-Klick--Die-Standardisierung-der-Landtechnik-e3673rb)
* [ISOBUS Object Pointer: Das Geheimnis dynamischer Displays und effizienter Fehlerdiagnose](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Object-Pointer-Das-Geheimnis-dynamischer-Displays-und-effizienter-Fehlerdiagnose-e36bp75)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010_AX.png)


## Ziel der Übung

Verwendung eines `Softkey`-Bausteins zur Steuerung eines Ausgangs.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_010_AX.SUB` verbindet eine Softkey-Instanz mit einem digitalen Ausgang[cite: 1].

### Funktionsbausteine (FBs)

  * **`SoftKey_F1`**: Typ `isobus::UT::io::Softkey::Softkey_IXA`. Dieser Baustein repräsentiert die Taste "F1" auf dem Bildschirm des ISOBUS-Terminals.
  * **`DigitalOutput_Q1`**: Der physische Ausgang.

### Parameter

*   `u16ObjId`: Verweist auf die Objekt-ID des Softkeys im Objekt-Pool (hier `SoftKey_F1`).

-----

## Funktionsweise

Die Funktionsweise ist identisch zu einem physischen Taster. Solange der Nutzer den Finger auf dem Touchscreen (oder die Taste am Rand) hält, liefert der Baustein `TRUE`. Lässt er los, wird `FALSE` gesendet.

-----

## Anwendungsbeispiel

**Maschinenfunktion einschalten**: Der Fahrer drückt auf dem Bildschirm das Symbol für "Arbeitsscheinwerfer", und das Licht geht an (solange er drückt).