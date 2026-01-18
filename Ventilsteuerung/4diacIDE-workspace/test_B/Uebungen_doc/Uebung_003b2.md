# Uebung_003b2: Massenmapping (Funk auf DataPanel)

```{index} single: Uebung_003b2: Massenmapping (Funk auf DataPanel)
```

[Uebung_003b2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003b2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_003b2`. In dieser Übung wird die Skalierbarkeit des Systems demonstriert, indem 15 Tasten einer Funkfernbedienung auf 15 digitale Ausgänge eines DataPanels gemappt werden.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_003b2.png)


## Ziel der Übung

Das Ziel dieser Übung ist die effiziente Verwaltung einer großen Anzahl von Hardware-Schnittstellen. Durch den Einsatz von typisierten Sub-Applikationen mit exponierten Parametern kann die komplette Zuordnung (Mapping) zwischen Funk-Eingängen und CAN-Bus-Ausgängen zentral in der Hauptanwendung vorgenommen werden, ohne die interne Logik verändern zu müssen.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_003b2.SUB` instanziiert 15 mal den spezialisierten Sub-Typ `Uebung_003b2_sub` (benannt `F1` bis `F15`)[cite: 1].

### Typisierte Sub-Applikation: `Uebung_003b2_sub`

[cite_start]Dieser Baustein dient als universeller "Kanal-Treiber" für die Funk-zu-CAN-Kommunikation[cite: 2]. Er verfügt über folgende Parameter:
  * **`Input`**: Der Name der Funk-Taste (z.B. `Key_01`, `START`, `STOP`).
  * **`u8SAMember`**: Die CAN-Adresse des DataPanels (hier fest auf `MI_00` gesetzt).
  * **`Output`**: Der Name des physischen Ausgangs am DataPanel (z.B. `DigitalOutput_1A`).

Intern enthält der Baustein einen `Funk_IX` zum Empfangen der Funksignale und einen `DataPanel_MI_QX` zum Senden der CAN-Nachrichten.

### Konfiguration der Kanäle

In `Uebung_003b2` sind die Zuweisungen klar definiert:
*   `F1`: `STOP` ➡️ `Output_1A`
*   `F2`: `START` ➡️ `Output_1B`
*   `F3` bis `F15`: `Key_01` bis `Key_13` ➡️ `Output_2A` bis `Output_8A`

-----

## Funktionsweise

Der Signalweg verläuft ereignisbasiert über die CAN-Bus-Infrastruktur:
1.  Der Nutzer drückt eine Taste auf der Funkfernbedienung.
2.  Die Instanz des Typs `Funk_IX` im Inneren der entsprechenden Sub-Applikation erkennt den Tastendruck und feuert ein `IND`-Event.
3.  Dieses Ereignis wird direkt an den `REQ`-Eingang des `DataPanel_MI_QX` Bausteins geleitet.
4.  Der Ausgangs-Baustein generiert daraufhin eine CAN-Nachricht für das DataPanel, um den zugeordneten physischen Ausgang ein- oder auszuschalten.

Da alle 15 Instanzen parallel und unabhängig arbeiten, können beliebig viele Tasten gleichzeitig bedient werden.

-----

## Anwendungsbeispiel

**Nachrüstung einer Funkfernsteuerung**:
Eine bestehende Maschine soll mit einer Funkfernbedienung für 15 verschiedene Hydraulikfunktionen ausgestattet werden. Anstatt die gesamte Logik neu zu programmieren, nutzt man das DataPanel als IO-Knoten und mappt die Funktasten rein parametrisch auf die Ventilausgänge. Dies ermöglicht eine extrem schnelle Inbetriebnahme und einfache Anpassung an Kundenwünsche (z.B. Tastenbelegung ändern).