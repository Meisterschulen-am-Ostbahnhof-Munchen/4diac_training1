# Uebung_000_AX: Einfache Addition

[Uebung_000_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_000_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_000_AX`, das absolute Basisbeispiel für Berechnungen.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_000_AX.png)


## Ziel der Übung

Das Ziel ist die Platzierung und Parametrierung eines Standard-Bausteins der IEC 61131-Bibliothek innerhalb eines IEC 61499 Netzwerks.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_000_AX.SUB` enthält lediglich einen Rechenbaustein[cite: 1].

### Funktionsbausteine (FBs)

  * **`ADD_2`**: Typ `iec61131::arithmetic::ADD_2`. [cite_start]Addiert zwei Ganzzahlen (`IN1` und `IN2`)[cite: 1].

-----

## Funktionsweise

Der Baustein ist fest mit den Werten 5 und 3 beschaltet. Das Ergebnis (8) liegt am Ausgang `OUT` an. Da es sich um einen reinen Datenbaustein ohne Event-Eingang handelt (Simple FB), wird das Ergebnis berechnet, sobald sich die Eingangsdaten ändern.

-----

## Anwendungsbeispiel

Grundlage für jede Form von **Zählern, Offsets oder Skalierungen** in einer Steuerung.
