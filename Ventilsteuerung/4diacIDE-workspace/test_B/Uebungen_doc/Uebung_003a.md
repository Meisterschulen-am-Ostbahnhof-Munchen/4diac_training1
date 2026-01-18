# Uebung_003a: Modulare Parallelsteuerung (Typed SubApp)

```{index} single: Uebung_003a: Modulare Parallelsteuerung (Typed SubApp)
```

[Uebung_003a](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003a.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_003a`. Hier wird ein fortgeschrittener Ansatz zur Strukturierung von IEC 61499-Anwendungen demonstriert: Die Kapselung von Logik in wiederverwendbare, typisierte Sub-Applikationen ("Typed SubApps").


## 📺 Video

* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-04-06 19-43-11 Slurry Tanker und Subapps und Groups erklärt](https://www.youtube.com/watch?v=EYsZXyRwfps)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [Der E_T_FF in IEC 61499: Modulares Kippen für die Industrie 4.0](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_T_FF-in-IEC-61499-Modulares-Kippen-fr-die-Industrie-4-0-e3674m7)
* [DIN EN 61499-1 Entschlüsselt: Der Bauplan für modulare, verteilte Steuerungssysteme](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Entschlsselt-Der-Bauplan-fr-modulare--verteilte-Steuerungssysteme-e367nmj)
* [DIN EN 61499-1: Revolution in der Steuerungstechnik – Modulare, ereignisgesteuerte Systeme verstehen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Revolution-in-der-Steuerungstechnik--Modulare--ereignisgesteuerte-Systeme-verstehen-e367nse)
* [ISOBUS nachrüsten: Kabelsalat war gestern – Die modulare Lösung für Ihre Agrartechnik](https://podcasters.spotify.com/pod/show/logibus/episodes/ISOBUS-nachrsten-Kabelsalat-war-gestern--Die-modulare-Lsung-fr-Ihre-Agrartechnik-e3767p4)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_003a.png)


## Ziel der Übung

Das Hauptziel ist die Vermeidung von redundantem Code. Anstatt für jeden Kanal die gleichen Bausteine und Verbindungen manuell zu zeichnen, wird einmalig ein generischer "Kanal-Typ" definiert. Dieser kann dann beliebig oft instanziiert und individuell konfiguriert werden. Dies erhöht die Übersichtlichkeit und reduziert Fehler bei der Programmierung großer Anlagen.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_003a.SUB` verwendet zwei Instanzen eines selbst definierten Sub-App-Typs, um zwei Signalpfade zu realisieren[cite: 1].

### Typisierte Sub-Applikation: `Uebung_003a_sub`

[cite_start]Dieser Baustein kapselt die grundlegende Logik der Signalweiterleitung[cite: 2]. Er besitzt zwei Parameter zur Hardware-Zuordnung:
  * **`Input`**: Bestimmt den physischen Eingang (z.B. `Input_I1`).
  * **`Output`**: Bestimmt den physischen Ausgang (z.B. `Output_Q1`).

Im Inneren des Typs befinden sich ein `logiBUS_IX` und ein `logiBUS_QX` Baustein, die über eine Event- und eine Data-Connection fest miteinander verbunden sind.

### Instanzen in der Hauptanwendung

In `Uebung_003a` werden zwei Instanzen dieses Typs platziert:
  * **`F1`**: [cite_start]Parametriert für den Pfad `I1` zu `Q1`[cite: 1].
  * **`F2`**: [cite_start]Parametriert für den Pfad `I2` zu `Q2`[cite: 1].

-----

## Funktionsweise

Die Komplexität der Einzelverbindungen ist im Inneren der Sub-Applikation verborgen ("Information Hiding"). Die Hauptanwendung definiert lediglich die Zuweisung der physischen Adressen. Der Aufbau in `Uebung_003a.SUB` ist daher extrem kompakt:

```xml
<SubApp Name="F1" Type="Uebungen::Uebung_003a_sub">
    <Parameter Name="Input" Value="Input_I1"/>
    <Parameter Name="Output" Value="Output_Q1"/>
</SubApp>
<SubApp Name="F2" Type="Uebungen::Uebung_003a_sub">
    <Parameter Name="Input" Value="Input_I2"/>
    <Parameter Name="Output" Value="Output_Q2"/>
</SubApp>
```

[cite_start][cite: 1]

Funktional verhält sich die Anwendung exakt wie die flache Struktur in Übung 003. Jede Instanz arbeitet als eigenständiger Block, der auf Ereignisse an seinem zugewiesenen Hardware-Eingang reagiert und den Hardware-Ausgang aktualisiert.

-----

## Anwendungsbeispiel

**Objektorientierte Anlagensteuerung**:
Stellen Sie sich eine Förderbandanlage mit 20 identischen Sektionen vor. Anstatt 20 mal die gleiche Logik zu zeichnen, erstellt man einen Typ "Sektion". In der Hauptanwendung platziert man 20 Instanzen und gibt ihnen nur die Start-Adressen der jeweiligen Hardware-IOs. Muss später die Logik geändert werden (z.B. eine zusätzliche Zeitverzögerung), ändert man dies nur an einer einzigen Stelle (im Typ), und alle 20 Sektionen übernehmen die Änderung sofort.