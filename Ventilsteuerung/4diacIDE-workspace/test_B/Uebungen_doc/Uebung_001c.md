# Uebung_001c: Eingang abfragen bei Boot (Standard-Pins)

```{index} single: Uebung_001c: Eingang abfragen bei Boot (Standard-Pins)
```

[Uebung_001c](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_001c.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_001c`. Hier wird demonstriert, wie ein digitaler Eingang unmittelbar nach dem Systemstart (Boot-Vorgang) abgefragt wird, um den initialen Zustand an einen digitalen Ausgang zu übertragen, unter Verwendung von Standard-Ereignis- und Datenverbindungen.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [4diac IDE: Wie der IEC 61499 Standard die Industrieautomatisierung revolutioniert](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/4diac-IDE-Wie-der-IEC-61499-Standard-die-Industrieautomatisierung-revolutioniert-e36756a)
* [IEC 61499 vs. 61131: Brauchen wir einen neuen Standard für IIoT? Analyse einer hitzigen Debatte um Verteilte Intelligenz](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-vs--61131-Brauchen-wir-einen-neuen-Standard-fr-IIoT--Analyse-einer-hitzigen-Debatte-um-Verteilte-Intelligenz-e3ahc2r)
* [IEC 61499: Befreit der neue Standard die Industrieautomation? Ein Vergleich mit 61131 und die Brücke zwischen OT & IT.](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Befreit-der-neue-Standard-die-Industrieautomation--Ein-Vergleich-mit-61131-und-die-Brcke-zwischen-OT--IT-e368446)
* [IEC 61499: Revolution der Industrieautomation – Warum der neue Standard Ihre Systeme fit für die Zukunft macht](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Revolution-der-Industrieautomation--Warum-der-neue-Standard-Ihre-Systeme-fit-fr-die-Zukunft-macht-e375evm)
* [Das Alarm Mask Objekt: Dein standardisierter Wachposten für Warnungen auf Landmaschinen](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/Das-Alarm-Mask-Objekt-Dein-standardisierter-Wachposten-fr-Warnungen-auf-Landmaschinen-e36e6c3)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_001c.png)


## Ziel der Übung

Das Hauptziel dieser Übung ist das Verständnis des Initialisierungsvorgangs in der IEC 61499. Es soll sichergestellt werden, dass der Ausgang bereits beim Hochfahren der Steuerung den korrekten Ist-Zustand des Hardware-Eingangs übernimmt, auch wenn zu diesem Zeitpunkt noch keine Zustandsänderung (Flanke) stattgefunden hat.

-----

## Beschreibung und Komponenten

[cite_start]Die Übung nutzt die Subapplikation `Uebung_001c.SUB`, um eine Verbindung zwischen einem digitalen Eingang und einem Ausgang herzustellen, ergänzt um eine Selbst-Triggerung für den Systemstart[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1`**: Eine Instanz des Typs `logiBUS_IX`. [cite_start]Dieser Baustein liefert das Ereignis `IND` bei Änderungen und reagiert auf den Befehl `REQ`, um den aktuellen Wert manuell auszulesen[cite: 1].
  * **`DigitalOutput_Q1`**: Eine Instanz des Typs `logiBUS_QX`. [cite_start]Dieser Baustein setzt den Hardware-Ausgang `Output_Q1` bei jedem eintreffenden `REQ`-Ereignis[cite: 1].

-----

## Funktionsweise

Die Logik kombiniert die normale Signalweiterleitung mit einer Initialisierungsschleife. Der Aufbau in `Uebung_001c.SUB` ist wie folgt definiert:

```xml
<EventConnections>
    <Connection Source="DigitalInput_I1.IND" Destination="DigitalOutput_Q1.REQ"/>
    <Connection Source="DigitalInput_I1.INITO" Destination="DigitalInput_I1.REQ"/>
    <Connection Source="DigitalInput_I1.CNF" Destination="DigitalOutput_Q1.REQ"/>
</EventConnections>
<DataConnections>
    <Connection Source="DigitalInput_I1.IN" Destination="DigitalOutput_Q1.OUT"/>
</DataConnections>
```

[cite_start][cite: 1]

Der Ablauf gliedert sich in zwei Phasen:

1.  **Initialisierungsphase (Boot)**:
    *   Beim Systemstart wird der Baustein `DigitalInput_I1` initialisiert und sendet ein `INITO`-Ereignis.
    *   Dieses Ereignis wird auf den eigenen `REQ`-Eingang zurückgeführt.
    *   Dadurch liest der Baustein sofort den physischen Zustand ein und quittiert dies mit einem `CNF`-Ereignis.
    *   Das `CNF`-Ereignis triggert schließlich `DigitalOutput_Q1.REQ`, wodurch der Ausgang bereits beim Start den korrekten Wert erhält.

2.  **Betriebsphase (Laufzeit)**:
    *   Jede spätere Änderung am Eingang triggert über `IND -> REQ` direkt den Ausgang, wie in Übung 001.

-----

## Anwendungsbeispiel

Ein **Zustands-Display**:
Stellen Sie sich vor, der Ausgang `Q1` steuert eine Kontrollleuchte, die anzeigt, ob ein Sicherheitsschalter (`I1`) geschlossen ist. Wenn die Anlage nach einem Stromausfall neu startet, muss die Lampe sofort korrekt leuchten – nicht erst, wenn jemand den Sicherheitsschalter erneut betätigt. Die Boot-Abfrage garantiert diese sofortige Korrektheit der Anzeige.