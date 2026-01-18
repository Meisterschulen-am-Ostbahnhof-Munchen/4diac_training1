# Uebung_003a0: Strukturierung durch untypisierte Sub-Applikationen

```{index} single: Uebung_003a0: Strukturierung durch untypisierte Sub-Applikationen
```

[Uebung_003a0](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003a0.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_003a0`. Im Gegensatz zur Verwendung von Typen (wie in `Uebung_003a`) wird hier gezeigt, wie man Logik visuell gruppieren kann, ohne separate Typ-Definitionen in der Bibliothek anzulegen. Dies geschieht durch sogenannte "Untyped SubApps".


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-15 16-27-21 Arithmetischer Überlauf führt zu Division durch 0.](https://www.youtube.com/watch?v=7CyOJPYJVz0)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [DIN EN 61131-3 vs. 61499-1: Dein Wegweiser durch die Normen der Industrieautomatisierung](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61131-3-vs--61499-1-Dein-Wegweiser-durch-die-Normen-der-Industrieautomatisierung-e36c6nc)
* [Industrielle Automation verstehen: SPS, PLS, SCADA, MES und ERP entschlüsselt – Eine Reise durch die Smart Factory](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Industrielle-Automation-verstehen-SPS--PLS--SCADA--MES-und-ERP-entschlsselt--Eine-Reise-durch-die-Smart-Factory-e3671qn)
* [Code-Renovierung mit AX-Adaptern: Wie Eclipse 4diac™ durch Signal-Bündelung Komplexität besiegt](https://podcasters.spotify.com/pod/show/logibus/episodes/Code-Renovierung-mit-AX-Adaptern-Wie-Eclipse-4diac-durch-Signal-Bndelung-Komplexitt-besiegt-e3ahcd1)
* [Als Landtechnik-Spezialist durch die Hölle: Wie Lanz-Wery Krieg, Besatzung und Hyperinflation überlebte – Einblicke in Original-Geschäftsberichte 1915-1922](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Als-Landtechnik-Spezialist-durch-die-Hlle-Wie-Lanz-Wery-Krieg--Besatzung-und-Hyperinflation-berlebte--Einblicke-in-Original-Geschftsberichte-1915-1922-e39athj)
* [Altbayerisch für Einsteiger: Von Gratler-Schnupfen und Stadthodern – Eine Laute-Reise durch Lektion 3C](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Altbayerisch-fr-Einsteiger-Von-Gratler-Schnupfen-und-Stadthodern--Eine-Laute-Reise-durch-Lektion-3C-e376jh4)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_003a0.png)


## Ziel der Übung

Das Hauptziel dieser Übung ist es, Möglichkeiten zur rein visuellen Strukturierung von Anwendungen aufzuzeigen. Untypisierte Sub-Applikationen dienen als "Container" oder Ordner innerhalb eines Netzwerks, um zusammengehörige Funktionen zu kapseln. Sie helfen, komplexe Diagramme aufzuräumen ("Aufräumen durch Einklappen"), ohne dass man sich Gedanken über Wiederverwendbarkeit oder Schnittstellen-Definitionen machen muss.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_003a0.SUB` enthält zwei eingebettete Sub-Applikationen (`SubApp` und `SubApp_1`), die jeweils einen eigenen Signalpfad beinhalten[cite: 1].

### Untypisierte Sub-Applikationen

Anders als bei typisierten SubApps, die auf einer externen Definition basieren, existiert die Logik dieser Container nur innerhalb dieser spezifischen Instanz. Sie haben keine externen Ein- oder Ausgänge im Interface (in diesem Beispiel), sondern greifen direkt auf die Hardware zu.

1.  **Container `SubApp`**:
    *   Beinhaltet die Logik für Kanal 2.
    *   Intern: [cite_start]`DigitalInput_I2` verbunden mit `DigitalOutput_Q2`[cite: 1].

2.  **Container `SubApp_1`**:
    *   Beinhaltet die Logik für Kanal 1.
    *   Intern: [cite_start]`DigitalInput_I1` verbunden mit `DigitalOutput_Q1`[cite: 1].

### Funktionsbausteine (FBs)

Innerhalb der Container werden die bekannten Standard-Bausteine verwendet:
  * **`logiBUS_IX`**: Zum ereignisbasierten Einlesen der Signale.
  * **`logiBUS_QX`**: Zum ereignisbasierten Ausgeben der Signale.

-----

## Funktionsweise

Die Logik ist identisch zur parallelen Steuerung, jedoch ist die Ansicht hierarchisch gegliedert. Der Aufbau in `Uebung_003a0.SUB` zeigt die Verschachtelung:

```xml
<SubAppNetwork>
    <SubApp Name="SubApp">
        <SubAppNetwork>
            <FB Name="DigitalInput_I2" ... />
            <FB Name="DigitalOutput_Q2" ... />
            <EventConnections> ... </EventConnections>
            <DataConnections> ... </DataConnections>
        </SubAppNetwork>
    </SubApp>
    
    <SubApp Name="SubApp_1">
        <SubAppNetwork>
            <FB Name="DigitalInput_I1" ... />
            <FB Name="DigitalOutput_Q1" ... />
            <EventConnections> ... </EventConnections>
            <DataConnections> ... </DataConnections>
        </SubAppNetwork>
    </SubApp>
</SubAppNetwork>
```

[cite_start][cite: 1]

Der funktionale Ablauf:
Die Kapselung hat keinen Einfluss auf die Laufzeit-Ausführung. Die Bausteine verhalten sich exakt so, als wären sie alle auf der obersten Ebene platziert.
1.  `SubApp_1` verarbeitet das Signal von `I1` zu `Q1`.
2.  `SubApp` verarbeitet das Signal von `I2` zu `Q2`.

-----

## Anwendungsbeispiel

**Visuelle Gruppierung von Funktionsbereichen**:
In einer großen Anlage könnte man untypisierte SubApps nutzen, um die Logik thematisch zu sortieren, z.B. einen Container "Temperaturregelung", einen "Antriebssteuerung" und einen "Sicherheitsüberwachung". Wenn man die Hauptansicht öffnet, sieht man nur diese drei Blöcke und nicht hunderte von einzelnen Gattern und Verbindungen. Dies erleichtert die Navigation ("Zoom-In"-Effekt), ist aber nicht für die Wiederverwendung über mehrere Projekte hinweg gedacht (dafür nutzt man typisierte SubApps).