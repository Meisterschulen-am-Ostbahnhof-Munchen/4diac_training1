# Uebung_003c: Mapping auf ISOBUS AUX (Standard-Pins)

```{index} single: Uebung_003c: Mapping auf ISOBUS AUX (Standard-Pins)
```

[Uebung_003c](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003c.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_003c`. Hier wird demonstriert, wie lokale Hardware-Eingänge an das ISOBUS-System als "Auxiliary Inputs" angebunden werden, wobei eine typisierte Sub-Applikation zur Strukturierung verwendet wird.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-08-17 14-05-25 Vorstellung logiBUS® neues IO System ohne Mapping](https://www.youtube.com/watch?v=5YnRsE5zVBk)
* [2025-08-17 14-39-09 logiBUS® Umwandeln eines Projektes mit Mapping in eines ohne Mapping.](https://www.youtube.com/watch?v=w8nTLn8fQxQ)

## Podcast
* [ISOBUS Button: Mehr als nur ein Klick – Die Standardisierung der Landtechnik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Button-Mehr-als-nur-ein-Klick--Die-Standardisierung-der-Landtechnik-e3673rb)
* [4diac IDE: Wie der IEC 61499 Standard die Industrieautomatisierung revolutioniert](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/4diac-IDE-Wie-der-IEC-61499-Standard-die-Industrieautomatisierung-revolutioniert-e36756a)
* [IEC 61499 vs. 61131: Brauchen wir einen neuen Standard für IIoT? Analyse einer hitzigen Debatte um Verteilte Intelligenz](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-vs--61131-Brauchen-wir-einen-neuen-Standard-fr-IIoT--Analyse-einer-hitzigen-Debatte-um-Verteilte-Intelligenz-e3ahc2r)
* [IEC 61499: Befreit der neue Standard die Industrieautomation? Ein Vergleich mit 61131 und die Brücke zwischen OT & IT.](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Befreit-der-neue-Standard-die-Industrieautomation--Ein-Vergleich-mit-61131-und-die-Brcke-zwischen-OT--IT-e368446)
* [IEC 61499: Revolution der Industrieautomation – Warum der neue Standard Ihre Systeme fit für die Zukunft macht](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Revolution-der-Industrieautomation--Warum-der-neue-Standard-Ihre-Systeme-fit-fr-die-Zukunft-macht-e375evm)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_003c.png)


## Ziel der Übung

Das Ziel ist es, lokale physische Schalter (`I1` bis `I4`) für das ISOBUS-Netzwerk verfügbar zu machen. In der ISOBUS-Welt können diese Eingänge als "Auxiliary Inputs" (Hilfseingänge) definiert werden. Der Endbenutzer kann diese dann am Terminal flexibel auf verschiedene Maschinenfunktionen mappen (z.B. "Taster 1 steuert Klappe auf/zu").

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_003c.SUB` nutzt vier Instanzen des Typs `Uebung_003c_sub`, um vier Kanäle für das ISOBUS-Mapping bereitzustellen[cite: 1].

### Typisierte Sub-Applikation: `Uebung_003c_sub`

[cite_start]Dieser Baustein verbindet einen Standard-Digitaleingang mit einem ISOBUS-Auxiliary-Ausgang[cite: 2]. Er verfügt über folgende Parameter:
  * **`Input`**: Auswahl des lokalen Hardware-Pins (z.B. `Input_I1`).
  * **`iInpNr`**: Die fortlaufende Nummer des AUX-Eingangs im Objekt-Pool (Index 0 bis n).

Intern werden die Ereignisse (`IND -> REQ`) und Daten (`IN -> OUT`) vom `logiBUS_IX` zum `Aux_QX` Baustein durchgereicht.

### Konfiguration der Kanäle

In `Uebung_003c` erfolgt das Mapping wie folgt:
*   `F1`: `Input_I1` ➡️ AUX Index 0
*   `F2`: `Input_I2` ➡️ AUX Index 1
*   `F3`: `Input_I3` ➡️ AUX Index 2
*   `F4`: `Input_I4` ➡️ AUX Index 3

-----

## Funktionsweise

1.  Der Bediener betätigt einen der physischen Schalter (z.B. `I1`).
2.  Die entsprechende Instanz (z.B. `F1`) erkennt die Pegeländerung.
3.  Ein `IND`-Event wird ausgelöst und triggert den `REQ`-Port des `Aux_QX` Bausteins.
4.  Der `Aux_QX` Baustein sendet eine standardisierte ISOBUS-Nachricht in das CAN-Netzwerk, die den Status des "Auxiliary Input N" mitteilt.
5.  Das verbundene ISOBUS-Anbaugerät empfängt diese Nachricht und führt die vom Nutzer zugewiesene Aktion aus.

-----

## Anwendungsbeispiel

**Nachrüstung von Bedienelementen**:
Ein Traktor verfügt über keine originalen ISOBUS-Joystick-Tasten. Man installiert eine kleine Konsole mit vier Standard-Tastern in der Kabine und verbindet diese mit der logiBUS-Steuerung. Dank dieser Software-Logik erscheinen die Taster für alle ISOBUS-Geräte (z.B. Feldspritze, Düngerstreuer) als vollwertige, frei belegbare Bedienelemente auf dem Terminal.