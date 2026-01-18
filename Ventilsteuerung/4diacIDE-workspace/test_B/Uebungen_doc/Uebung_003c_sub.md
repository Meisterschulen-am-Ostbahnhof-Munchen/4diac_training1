# Uebung_003c_sub: ISOBUS AUX-Kanal (SubApp)

```{index} single: Uebung_003c_sub: ISOBUS AUX-Kanal (SubApp)
```

[Uebung_003c_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003c_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt den Sub-App-Typ `Uebung_003c_sub`. Dieser Baustein dient als Brücke zwischen lokaler Hardware und dem ISOBUS-Hilfseingangssystem (Auxiliary).


## 📺 Video

* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-04-06 19-43-11 Slurry Tanker und Subapps und Groups erklärt](https://www.youtube.com/watch?v=EYsZXyRwfps)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [Das Working Set Objekt: Das Gehirn der ISOBUS-Bedienoberfläche verstehen – Von der Norm zur Praxis im ISO-Designer](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/Das-Working-Set-Objekt-Das-Gehirn-der-ISOBUS-Bedienoberflche-verstehen--Von-der-Norm-zur-Praxis-im-ISO-Designer-e36cl5v)
* [ISOBUS Button: Mehr als nur ein Klick – Die Standardisierung der Landtechnik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Button-Mehr-als-nur-ein-Klick--Die-Standardisierung-der-Landtechnik-e3673rb)
* [ISOBUS Object Pointer: Das Geheimnis dynamischer Displays und effizienter Fehlerdiagnose](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Object-Pointer-Das-Geheimnis-dynamischer-Displays-und-effizienter-Fehlerdiagnose-e36bp75)
* [ISOBUS Output Meter: Dynamische Anzeigen meistern – vom Zeiger bis zur Visualisierung auf dem VT](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Output-Meter-Dynamische-Anzeigen-meistern--vom-Zeiger-bis-zur-Visualisierung-auf-dem-VT-e36t2tp)
* [ISOBUS Skalierung: Wenn der Ackerschlepper-Bildschirm nicht passt – Eine Einführung in ISO 11783-6](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Skalierung-Wenn-der-Ackerschlepper-Bildschirm-nicht-passt--Eine-Einfhrung-in-ISO-11783-6-e36a8q6)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



## Ziel der Übung

Kapselung der ISOBUS-Kommunikation. Der Baustein verbirgt die Details des ISOBUS-Protokolls und stellt eine einfache Schnittstelle zur Zuordnung von physischen Tastern zu logischen AUX-Nummern bereit.

-----

## Beschreibung und Komponenten

[cite_start]Der Typ `Uebung_003c_sub` enthält einen lokalen Eingangs-Baustein und einen ISOBUS-Ausgangs-Baustein[cite: 1].

### Interne Funktionsbausteine (FBs)

  * **`IX`**: Typ `logiBUS_IX`. Liest den lokalen Hardware-Pin (`Input`) ein.
  * **`QX`**: Typ `Aux_QX`. Sendet den Zustand als ISOBUS-Nachricht für die gewählte Funktionsnummer (`iInpNr`).

-----

## Schnittstellen

[cite_start]Der Baustein wird über zwei Parameter konfiguriert[cite: 1]:
*   **`Input`**: Der physische Taster an der Steuerung.
*   **`iInpNr`**: Die fortlaufende Nummer (Index) im ISOBUS-Auxiliary-Pool.

Jede Änderung am lokalen Taster führt sofort zu einer entsprechenden Status-Meldung im ISOBUS-Netzwerk, wodurch der Taster für andere Geräte (z.B. Task Controller) sichtbar wird.