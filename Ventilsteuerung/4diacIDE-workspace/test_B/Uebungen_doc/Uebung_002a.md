# Uebung_002a: Logische UND-Verknüpfung (AND)

```{index} single: Uebung_002a: Logische UND-Verknüpfung (AND)
```

[Uebung_002a](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_002a.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_002a`. In dieser Übung wird eine klassische UND-Verknüpfung (AND) realisiert, bei der ein digitaler Ausgang nur dann aktiviert wird, wenn zwei digitale Eingänge gleichzeitig den Zustand "Wahr" (HIGH) führen.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-03-30 16-59-57 Verknüpfung von Object ID und Objektname](https://www.youtube.com/watch?v=FuZTizT48JU)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_002a.png)


## Ziel der Übung

Das Hauptziel dieser Übung ist die Implementierung einer grundlegenden logischen Entscheidungsstruktur. Es wird gezeigt, wie Signale von mehreren Sensoren (Eingängen) kombiniert werden können, um eine Aktion an einem Aktor (Ausgang) auszulösen. Dies ist ein fundamentaler Baustein jeder Steuerungsprogrammierung.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_002a.SUB` verknüpft zwei digitale Eingänge über einen Logik-Baustein mit einem digitalen Ausgang[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1` & `DigitalInput_I2`**: Instanzen des Typs `logiBUS_IX`. [cite_start]Diese repräsentieren die beiden Hardware-Eingänge, die überwacht werden[cite: 1].
  * **`AND_2`**: Eine Instanz des Typs `AND_2` (aus der IEC 61131-Bibliothek). [cite_start]Dieser Baustein führt die logische UND-Operation aus. Er besitzt zwei Dateneingänge (`IN1`, `IN2`) und einen Datenausgang (`OUT`)[cite: 1]. Zur Steuerung benötigt er ein Ereignis am Port `REQ` und quittiert die Berechnung am Port `CNF`.
  * **`DigitalOutput_Q1`**: Eine Instanz des Typs `logiBUS_QX`. [cite_start]Dieser Baustein steuert den Hardware-Ausgang `Output_Q1` basierend auf dem Ergebnis der Logik[cite: 1].

-----

## Funktionsweise

Die Logik wird durch die Verschaltung von Ereignis- und Datenverbindungen festgelegt. Der Aufbau in `Uebung_002a.SUB` ist wie folgt definiert:

```xml
<EventConnections>
    <Connection Source="DigitalInput_I1.IND" Destination="AND_2.REQ"/>
    <Connection Source="DigitalInput_I2.IND" Destination="AND_2.REQ"/>
    <Connection Source="AND_2.CNF" Destination="DigitalOutput_Q1.REQ"/>
</EventConnections>
<DataConnections>
    <Connection Source="DigitalInput_I1.IN" Destination="AND_2.IN1"/>
    <Connection Source="DigitalInput_I2.IN" Destination="AND_2.IN2"/>
    <Connection Source="AND_2.OUT" Destination="DigitalOutput_Q1.OUT"/>
</DataConnections>
```

[cite_start][cite: 1]

Der Prozess folgt dieser Logik:
1.  Ändert sich einer der beiden Eingänge (`I1` oder `I2`), sendet der jeweilige Baustein ein `IND`-Ereignis an den `REQ`-Port des `AND_2`-Bausteins.
2.  Der `AND_2`-Baustein liest daraufhin beide Daten-Eingänge (`IN1` und `IN2`) und berechnet das Ergebnis (`IN1 AND IN2`).
3.  Nach Abschluss der Berechnung feuert der Logik-Baustein ein `CNF`-Ereignis (Confirmation) ab.
4.  Dieses `CNF`-Ereignis erreicht den `REQ`-Port von `DigitalOutput_Q1`, welcher daraufhin das Ergebnis übernimmt und den physischen Ausgang schaltet.

-----

## Anwendungsbeispiel

Ein klassisches Anwendungsbeispiel ist die **Sicherheits-Freigabe**:
Ein Motor (`Q1`) soll nur starten, wenn sowohl die Schutztür geschlossen ist (`I1`) als auch der Bediener den Start-Taster drückt (`I2`). Nur wenn beide Bedingungen gleichzeitig erfüllt sind (`TRUE`), liefert das UND-Gatter ein Signal zum Einschalten des Motors.