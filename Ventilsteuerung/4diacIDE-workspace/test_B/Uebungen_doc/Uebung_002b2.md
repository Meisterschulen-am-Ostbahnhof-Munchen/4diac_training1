# Uebung_002b2: Kombinatorische Logik (AND/OR mit F_MOVE)

```{index} single: Uebung_002b2: Kombinatorische Logik (AND/OR mit F_MOVE)
```

[Uebung_002b2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_002b2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_002b2`. In dieser Übung wird eine kombinatorische Logikschaltung implementiert, die zwei Grundoperationen (UND und ODER) miteinander verknüpft, wobei ein `F_MOVE`-Baustein zur expliziten Datenweiterleitung genutzt wird.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Schalterlogik verstehen: So funktioniert ein Toggle Flip-Flop mit logiBUS® – einfache Steuerung in der Landtechnik](https://podcasters.spotify.com/pod/show/logibus/episodes/Schalterlogik-verstehen-So-funktioniert-ein-Toggle-Flip-Flop-mit-logiBUS--einfache-Steuerung-in-der-Landtechnik-e36vjo1)
* [Digitale Logik Flip-Flops und Datentypen](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Digitale-Logik-Flip-Flops-und-Datentypen-e3dic6t)
* [Wie simple Schalter "denken": Die Grundlagen der Digitaltechnik – Gatter, Logik und die Macht von 1 und 0](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Wie-simple-Schalter-denken-Die-Grundlagen-der-Digitaltechnik--Gatter--Logik-und-die-Macht-von-1-und-0-e3ae98g)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_002b2.png)


## Ziel der Übung

Das Hauptziel dieser Übung ist die hierarchische Verknüpfung von Logikbausteinen. Es wird gezeigt, wie Teilergebnisse einer Operation als Eingangsgröße für eine weitere Operation dienen können. Zusätzlich wird der Baustein `F_MOVE` eingeführt, der dazu dient, Datenwerte explizit in einem eigenen Ereignisschritt weiterzureichen.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_002b2.SUB` realisiert die logische Funktion `Q1 = (I1 AND I2) OR I3` unter Verwendung von Standard-Logikbausteinen[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1` bis `I3`**: Drei Instanzen des Typs `logiBUS_IX`. [cite_start]Sie liefern die Eingangssignale für die Logikkette[cite: 1].
  * **`AND_2`**: Eine Instanz des Typs `AND_2`. [cite_start]Verknüpft die Eingänge `I1` und `I2`[cite: 1].
  * **`F_MOVE`**: Ein Datentransfer-Baustein. [cite_start]Er nimmt den Wert am Eingang `IN` entgegen und gibt ihn beim Ereignis `REQ` unverändert am Ausgang `OUT` wieder aus[cite: 1]. Er dient hier als Puffer zwischen den Logikstufen.
  * **`OR_2`**: Eine Instanz des Typs `OR_2`. [cite_start]Verknüpft das (gepufferte) Ergebnis des UND-Bausteins mit dem dritten Eingang `I3`[cite: 1].
  * **`DigitalOutput_Q1`**: Gibt das Endergebnis der Logik an den Hardware-Ausgang aus.

-----

## Funktionsweise

Die hierarchische Struktur der Logik wird durch die Verschaltung der Ereigniskette in `Uebung_002b2.SUB` deutlich:

```xml
<EventConnections>
    <Connection Source="DigitalInput_I1.IND" Destination="AND_2.REQ"/>
    <Connection Source="DigitalInput_I2.IND" Destination="AND_2.REQ"/>
    <Connection Source="AND_2.CNF" Destination="F_MOVE.REQ"/>
    <Connection Source="F_MOVE.CNF" Destination="OR_2.REQ"/>
    <Connection Source="DigitalInput_I3.IND" Destination="OR_2.REQ"/>
    <Connection Source="OR_2.CNF" Destination="DigitalOutput_Q1.REQ"/>
</EventConnections>
<DataConnections>
    <Connection Source="DigitalInput_I1.IN" Destination="AND_2.IN1"/>
    <Connection Source="DigitalInput_I2.IN" Destination="AND_2.IN2"/>
    <Connection Source="AND_2.OUT" Destination="F_MOVE.IN"/>
    <Connection Source="F_MOVE.OUT" Destination="OR_2.IN1"/>
    <Connection Source="DigitalInput_I3.IN" Destination="OR_2.IN2"/>
    <Connection Source="OR_2.OUT" Destination="DigitalOutput_Q1.OUT"/>
</DataConnections>
```

[cite_start][cite: 1]

Der funktionale Ablauf:
1.  Ändert sich `I1` oder `I2`, berechnet `AND_2` das Teilergebnis.
2.  Das Fertigstellungs-Event (`CNF`) von `AND_2` triggert den `F_MOVE`.
3.  `F_MOVE` schiebt das Teilergebnis weiter zum ODER-Baustein und triggert diesen wiederum an (`CNF -> REQ`).
4.  Der ODER-Baustein verarbeitet das gepufferte Ergebnis zusammen mit dem Signal von `I3`.
5.  Der Ausgang `Q1` wird aktiviert, wenn entweder beide ersten Eingänge aktiv sind ODER wenn der dritte Eingang aktiv ist.

-----

## Anwendungsbeispiel

**Anlagenfreigabe mit Überbrückung**:
Ein Motor (`Q1`) soll normalerweise nur laufen, wenn zwei Sensoren (`I1` und `I2`) gleichzeitig grünes Licht geben (z.B. Druck ok UND Temperatur ok). Für Wartungszwecke soll der Motor jedoch auch dann gestartet werden können, wenn ein manueller Taster (`I3`) gedrückt wird, der die Automatiklogik überbrückt.