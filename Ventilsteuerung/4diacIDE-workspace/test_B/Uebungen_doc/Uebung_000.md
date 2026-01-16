# Uebung_000: Arithmetische Grundfunktionen (ADD)

[Uebung_000](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_000.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_000`. Dies ist das absolute Einstiegsbeispiel für die mathematische Datenverarbeitung.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_000.png)


## Ziel der Übung

Verwendung eines Standard-Mathematikbausteins (`ADD_2`). Es wird gezeigt, wie konstante Werte an die Eingänge eines Bausteins angelegt werden, um eine einfache Berechnung auszuführen.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_000.SUB` wird ein Additions-Baustein zur Berechnung einer Summe genutzt[cite: 1].

### Funktionsbausteine (FBs)

  * **`ADD_2`**: Ein Baustein aus der IEC 61131-Bibliothek (Arithmetik).
  * **Parameter**:
    * `IN1`: Festwert 5 (`INT#5`).
    * `IN2`: Festwert 3 (`INT#3`).

-----

## Funktionsweise

Der Baustein nimmt die beiden Eingangswerte und addiert sie intern. Da in diesem minimalistischen Beispiel keine Ereignisverbindungen definiert sind, handelt es sich um eine rein statische Berechnung des Datenflusses. Das mathematische Ergebnis am Ausgang `OUT` ist 8.

-----

## Lernziel

Diese Übung dient dazu, sich mit der 4diac-Oberfläche vertraut zu machen:
1.  Bausteine aus der Bibliothek ziehen.
2.  Eigenschaften (Parameter) von Bausteinen im Properties-Fenster editieren.
3.  Den Unterschied zwischen variablen Eingängen und Konstanten verstehen.
