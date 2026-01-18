# Uebung_003: Parallele Signalwege (Standard-Pins)

```{index} single: Uebung_003: Parallele Signalwege (Standard-Pins)
```

[Uebung_003](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_003`. In dieser Übung werden zwei voneinander unabhängige Signalpfade realisiert, wobei jeder digitale Eingang direkt einen zugeordneten digitalen Ausgang steuert.


## 📺 Video

* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
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



![](Uebung_003.png)


## Ziel der Übung

Das Hauptziel dieser Übung ist es, die parallele Verarbeitung von Signalen in der IEC 61499 zu demonstrieren. Da Funktionsbausteine in 4diac ereignisbasiert arbeiten, können mehrere Steuerungsaufgaben völlig unabhängig voneinander in einem Netzwerk existieren, ohne sich gegenseitig in der Ausführung zu blockieren.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_003.SUB` definiert zwei separate Signalwege ("Kanäle"), die parallel verarbeitet werden[cite: 1].

### Funktionsbausteine (FBs)

Es werden zwei Paare von Ein- und Ausgangsbausteinen verwendet:

  * **`DigitalInput_I1` & `DigitalOutput_Q1`**: Das erste Paar (Kanal 1). [cite_start]Verbindet Hardware-Eingang `I1` mit Hardware-Ausgang `Q1`[cite: 1].
  * **`DigitalInput_I2` & `DigitalOutput_Q2`**: Das zweite Paar (Kanal 2). [cite_start]Verbindet Hardware-Eingang `I2` mit Hardware-Ausgang `Q2`[cite: 1].

-----

## Funktionsweise

Die Unabhängigkeit der beiden Kanäle wird durch die getrennten Ereignis- und Datenverbindungen in der Subapplikation `Uebung_003.SUB` sichergestellt:

```xml
<EventConnections>
    <Connection Source="DigitalInput_I1.IND" Destination="DigitalOutput_Q1.REQ"/>
    <Connection Source="DigitalInput_I2.IND" Destination="DigitalOutput_Q2.REQ"/>
</EventConnections>
<DataConnections>
    <Connection Source="DigitalInput_I1.IN" Destination="DigitalOutput_Q1.OUT"/>
    <Connection Source="DigitalInput_I2.IN" Destination="DigitalOutput_Q2.OUT"/>
</DataConnections>
```

[cite_start][cite: 1]

Der funktionale Ablauf:
1.  Ändert sich der Zustand von `I1`, feuert der erste Baustein ein `IND`-Event, welches `Q1` zur Aktualisierung auffordert.
2.  Ändert sich der Zustand von `I2`, feuert der zweite Baustein ein `IND`-Event, welches `Q2` zur Aktualisierung auffordert.

Beide Prozesse laufen asynchron ab. Eine schnelle Schaltfolge auf Kanal 1 beeinflusst die Reaktionszeit von Kanal 2 in keiner Weise.

-----

## Anwendungsbeispiel

**Unabhängige Aggregate**:
In einer landwirtschaftlichen Maschine werden zwei unabhängige Elektromotoren gesteuert. Schalter 1 (`I1`) schaltet den Motor für die Förderschnecke (`Q1`) ein, und Schalter 2 (`I2`) schaltet das Gebläse (`Q2`) ein. Obwohl beide Logiken im selben Steuerungsprogramm definiert sind, operieren sie als getrennte "Software-Schaltkreise".