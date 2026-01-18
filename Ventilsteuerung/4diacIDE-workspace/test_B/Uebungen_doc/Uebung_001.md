# Uebung_001: Direkte Signalweiterleitung (Event & Daten)

```{index} single: Uebung_001: Direkte Signalweiterleitung (Event & Daten)
```

[Uebung_001](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_001.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die grundlegende logiBUS®-Übung `Uebung_001`. Hier wird das fundamentale Prinzip der IEC 61499 demonstriert: Die explizite Trennung von Datenfluss und Ereignisfluss.


## 📺 Video

* [D-Flip-Flop: E_D_FF aus der IEC 61499 (Übung 002c) als "Eventbremse"](https://www.youtube.com/watch?v=yGSx_0ggveE)
* [Zusätzlich: Uebung_083: Aufwärts/Abwärts zählen: E_CTUD_UDINT Datentyp UDINT; mit Anzeige am VT.](https://www.youtube.com/watch?v=oTPDtsw5eAw)
* ["Store Version" – Dein Schlüssel zur Verwaltung von Objektdatenpools im nichtflüchtigen VT-Speich...](https://www.youtube.com/watch?v=eVseHOOO9qM)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)

## Podcast
* [Analyse der Novellierung der Meisterprüfungsverordnung im Land- und Baumaschinenmechatroniker-Handwerk: Ein Detaillierter Vergleich der Verordnungen von 2024 und 2001](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Analyse-der-Novellierung-der-Meisterprfungsverordnung-im-Land--und-Baumaschinenmechatroniker-Handwerk-Ein-Detaillierter-Vergleich-der-Verordnungen-von-2024-und-2001-e37aejv)
* [logiBUS® verstehen: Direkte Signalweiterleitung – Das "Hallo Welt" der Automatisierung](https://podcasters.spotify.com/pod/show/logibus/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg)
* [Datenkommunikation in der Automatisierung: Die Geheimnisse der IEC 61499 Datentypen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Datenkommunikation-in-der-Automatisierung-Die-Geheimnisse-der-IEC-61499-Datentypen-e3672lj)
* [Datentypen der IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Datentypen-der-IEC-61499-e3672jf)
* [E_TOF vs. FB_TOF: Der Event-Timer, der nicht zyklisch tickt – Revolution für Automatisierungssysteme?](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_TOF-vs--FB_TOF-Der-Event-Timer--der-nicht-zyklisch-tickt--Revolution-fr-Automatisierungssysteme-e3673qk)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_001_Gemini.jpg)

![](Uebung_001.png)


## Ziel der Übung

Das Ziel dieser Einstiegsübung ist es, ein Signal von einem physischen digitalen Eingang zu einem digitalen Ausgang zu leiten. Dabei lernen die Anwender, dass in der IEC 61499 eine reine Datenverbindung (die "Leitung") nicht ausreicht – es muss auch ein Ereignis (der "Trigger") übertragen werden, damit der Zielbaustein die Daten verarbeitet.

-----

## Beschreibung und Komponenten

[cite_start]Die Übung besteht aus einer Subapplikation (`Uebung_001.SUB`), die einen Eingangsbaustein und einen Ausgangsbaustein über zwei separate Verbindungstypen verknüpft[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1`**: Eine Instanz des Typs `logiBUS_IX`. [cite_start]Dieser Baustein repräsentiert den physischen Eingang `Input_I1`[cite: 1]. Er stellt sowohl den logischen Zustand (`IN`) als auch ein Benachrichtigungs-Ereignis (`IND`) zur Verfügung.
  * **`DigitalOutput_Q1`**: Eine Instanz des Typs `logiBUS_QX`. [cite_start]Dieser Baustein steuert den physischen Ausgang `Output_Q1`[cite: 1]. Er benötigt einen Datenwert (`OUT`) und einen Auslöse-Befehl (`REQ`).

-----

## Funktionsweise

Die Logik wird durch zwei parallele Verbindungen realisiert. Der Aufbau in `Uebung_001.SUB` verdeutlicht dies:

```xml
<EventConnections>
    <Connection Source="DigitalInput_I1.IND" Destination="DigitalOutput_Q1.REQ"/>
</EventConnections>
<DataConnections>
    <Connection Source="DigitalInput_I1.IN" Destination="DigitalOutput_Q1.OUT"/>
</DataConnections>
```

[cite_start][cite: 1]

Der Prozess läuft wie folgt ab:
1.  Der Baustein `DigitalInput_I1` erkennt eine Änderung am Hardware-Eingang `I1`.
2.  Er aktualisiert seinen Daten-Ausgang `IN` mit dem neuen Wert (TRUE oder FALSE).
3.  Zeitgleich feuert er ein Ereignis am Port `IND` (Indication) ab.
4.  Dieses Ereignis wandert über die **Event Connection** zum Port `REQ` (Request) des Bausteins `DigitalOutput_Q1`.
5.  Erst durch den Empfang des Ereignisses liest `DigitalOutput_Q1` den Wert, der an seinem Port `OUT` über die **Data Connection** anliegt, und schaltet den Hardware-Ausgang entsprechend.

-----

## Anwendungsbeispiel

Ein **Lichtschalter im Haus**:
Der Schalter an der Wand ist der Eingang `I1`, die Glühbirne an der Decke ist der Ausgang `Q1`. Das Kabel überträgt den Strom (Daten), aber erst das Umlegen des Schalters (Ereignis) sorgt dafür, dass die Information "An" oder "Aus" verarbeitet und umgesetzt wird.