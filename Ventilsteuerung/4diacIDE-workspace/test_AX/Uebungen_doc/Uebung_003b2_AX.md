# Uebung_003b2_AX: Massenverarbeitung mit untypisierten Sub-Applikationen

```{index} single: Uebung_003b2_AX: Massenverarbeitung mit untypisierten Sub-Applikationen
```

[Uebung_003b2_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003b2_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_003b2_AX`. Diese Übung zeigt die Skalierbarkeit des Systems am Beispiel der Verknüpfung von 15 Funktasten mit 15 digitalen Ausgängen, realisiert durch untypisierte Sub-Applikationen (bzw. wiederverwendete typisierte Sub-Applikationen, die hier manuell platziert wurden).


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_003b2_AX.png)


## Ziel der Übung

Das Ziel dieser Übung ist es, eine große Anzahl von gleichartigen Verbindungen effizient zu verwalten. Anstatt 15 Mal die gleichen Funktionsbausteine und Verbindungen in der Hauptansicht zu zeichnen, wird die Logik in modulare Blöcke (Sub-Applikationen) verpackt. Dies demonstriert, wie IEC 61499 für umfangreiche I/O-Mappings eingesetzt wird.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_003b2_AX.SUB` instanziiert 15 mal den Sub-Typ `Uebung_003b2_sub_AX` (hier als `F1` bis `F15` benannt)[cite: 1].

### Sub-Komponente: `Uebung_003b2_sub_AX`

[cite_start]Dieser Sub-Baustein verbindet einen Funkeingang (`Funk_IXA`) mit einem DataPanel-Ausgang (`DataPanel_MI_QXA`)[cite: 2]. Er verfügt über Parameter zur Konfiguration:
  * **`Input`**: Der Funk-Taster (z.B. `DigitalInput_Key_START`).
  * **`Output`**: Der physische Ausgang (z.B. `DigitalOutput_1B`).
  * **`u8SAMember`**: Die Adresse des DataPanels.

### Mapping

Die Übung mappt folgende Signale:
*   `STOP` -> (nicht belegt/intern)
*   `START` -> `F2`
*   `Key_01` bis `Key_13` -> `F3` bis `F15`

(Hinweis: Die genaue Zuordnung der Parameter ist in der `.SUB`-Datei für `Uebung_003b2_AX` im Gegensatz zu `Uebung_003b3_AX` nicht explizit sichtbar, da hier untypisierte oder eingebettete SubApps verwendet wurden, bei denen die Parameter im Inneren gesetzt sind oder Default-Werte nutzen. In `Uebung_003b3_AX` sind die Parameter explizit nach außen geführt.)

-----

## Funktionsweise

Jede Instanz `F1` bis `F15` arbeitet unabhängig:
1.  Der `Funk_IXA`-Baustein empfängt das Signal der entsprechenden Taste von der Funkfernbedienung.
2.  Das Signal wird über eine Adapter-Verbindung an den `DataPanel_MI_QXA`-Baustein weitergeleitet.
3.  Der Ausgang am DataPanel schaltet entsprechend.

Da alle 15 Kanäle parallel arbeiten, können mehrere Tasten gleichzeitig gedrückt werden, und die entsprechenden Ausgänge reagieren simultan.

-----

## Anwendungsbeispiel

Ein Anwendungsbeispiel ist ein **Bedienfeld für einen Ladekran**:

Der Kranführer hat eine Funkfernbedienung mit vielen Tasten (Heben, Senken, Drehen, Teleskopieren, etc.). Jede Taste muss ein spezifisches Hydraulikventil ansteuern. Durch die Verwendung von Sub-Applikationen bleibt der Schaltplan übersichtlich ("Eine Kiste pro Funktion"), obwohl im Hintergrund 30 oder mehr Bausteine aktiv sind.