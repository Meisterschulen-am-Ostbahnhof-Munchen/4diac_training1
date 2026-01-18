# Uebung_002a5b: ODER-Verknüpfung mit Signalverteilung

```{index} single: Uebung_002a5b: ODER-Verknüpfung mit Signalverteilung
```

[Uebung_002a5b](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_002a5b.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_002a5b`. In dieser Übung werden zwei Konzepte kombiniert: Eine logische ODER-Verknüpfung (OR) mit drei Eingängen und die gleichzeitige Verteilung (Fan-Out) des Ergebnisses auf drei digitale Ausgänge.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-03-30 16-59-57 Verknüpfung von Object ID und Objektname](https://www.youtube.com/watch?v=FuZTizT48JU)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vagb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_002a5b.png)


## Ziel der Übung

Das Ziel ist es, eine komplexe E/A-Struktur abzubilden. Es wird gezeigt, wie Informationen von mehreren Sensoren gesammelt, logisch bewertet und das Ergebnis an eine Gruppe von Aktoren verteilt wird. Dabei wird die Skalierbarkeit von Ereignisverbindungen sowohl auf der Eingangsseite (Fan-In) als auch auf der Ausgangsseite (Fan-Out) verdeutlicht.

-----

## Beschreibung und Komponenten

[cite_start]In der Subapplikation `Uebung_002a5b.SUB` werden drei Eingangsbausteine über ein ODER-Gatter mit drei Ausgangsbausteinen verknüpft[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1` bis `I3`**: Drei Instanzen des Typs `logiBUS_IX`. [cite_start]Sie überwachen die Hardware-Eingänge `Input_I1`, `Input_I2` und `Input_I3`[cite: 1].
  * **`OR_3_BOOL`**: Eine Instanz des Typs `OR_3_BOOL` (aus der IEC 61131-Bibliothek). [cite_start]Dieser Baustein führt eine ODER-Operation für drei boolesche Eingänge aus[cite: 1]. Er reagiert auf `REQ` und quittiert mit `CNF`.
  * **`DigitalOutput_Q1` bis `Q3`**: Drei Instanzen des Typs `logiBUS_QX`. [cite_start]Sie steuern die physischen Ausgänge `Output_Q1`, `Output_Q2` und `Output_Q3`[cite: 1].

-----

## Funktionsweise

Die Schaltung nutzt ein zentrales Logik-Element als Knotenpunkt für alle Signale. Der Aufbau in `Uebung_002a5b.SUB` ist wie folgt definiert:

```xml
<EventConnections>
    <Connection Source="DigitalInput_I1.IND" Destination="OR_3_BOOL.REQ"/>
    <Connection Source="DigitalInput_I2.IND" Destination="OR_3_BOOL.REQ"/>
    <Connection Source="DigitalInput_I3.IND" Destination="OR_3_BOOL.REQ"/>
    <Connection Source="OR_3_BOOL.CNF" Destination="DigitalOutput_Q1.REQ"/>
    <Connection Source="OR_3_BOOL.CNF" Destination="DigitalOutput_Q2.REQ"/>
    <Connection Source="OR_3_BOOL.CNF" Destination="DigitalOutput_Q3.REQ"/>
</EventConnections>
<DataConnections>
    <Connection Source="DigitalInput_I1.IN" Destination="OR_3_BOOL.IN1"/>
    <Connection Source="DigitalInput_I2.IN" Destination="OR_3_BOOL.IN2"/>
    <Connection Source="DigitalInput_I3.IN" Destination="OR_3_BOOL.IN3"/>
    <Connection Source="OR_3_BOOL.OUT" Destination="DigitalOutput_Q1.OUT"/>
    <Connection Source="OR_3_BOOL.OUT" Destination="DigitalOutput_Q2.OUT"/>
    <Connection Source="OR_3_BOOL.OUT" Destination="DigitalOutput_Q3.OUT"/>
</DataConnections>
```

[cite_start][cite: 1]

Der funktionale Ablauf:
1.  **Eingangs-Trigger**: Jede Änderung an einem der drei Taster (`I1`, `I2`, `I3`) löst eine Neuberechnung der Logik aus.
2.  **Berechnung**: Der Baustein `OR_3_BOOL` setzt sein Ergebnis auf `TRUE`, wenn mindestens ein Eingang aktiv ist.
3.  **Massen-Update**: Das resultierende Signal wird zeitgleich an alle drei Lampen (`Q1`, `Q2`, `Q3`) gesendet. Sobald die Logik fertig ist (`CNF`), werden alle drei Hardware-Ausgänge synchron aktualisiert.

-----

## Anwendungsbeispiel

**Zentrale Warnanlage**:
In einer Werkshalle gibt es drei Not-Halt-Taster (`I1`, `I2`, `I3`). Sobald einer dieser Taster gedrückt wird, müssen an drei verschiedenen Stellen der Halle Warnlampen (`Q1`, `Q2`, `Q3`) aufleuchten. Die ODER-Logik sammelt die Alarme ein, und der Fan-Out sorgt für die weitreichende Signalisierung.