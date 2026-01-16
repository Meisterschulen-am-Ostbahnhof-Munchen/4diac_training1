# Uebung_010a2: ISOBUS Button (Datenmaske)

[Uebung_010a2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010a2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010a2`. Neben den Softkeys am Rand gibt es im ISOBUS auch "Buttons", die sich direkt innerhalb der Arbeitsmaske befinden.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010a2.png)


## Ziel der Übung

Verwendung eines `Button_IX` Bausteins.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_010a2.SUB` nutzt einen Button anstelle eines Softkeys zur Steuerung eines Ausgangs[cite: 1].

### Funktionsbausteine (FBs)

  * **`Button_A1`**: Typ `isobus::UT::io::Button::Button_IX`. Referenziert das Objekt `Button_A1` im Pool.

-----

## Funktionsweise

Die Logik ist identisch zum Softkey: Solange die Schaltfläche auf dem Bildschirm berührt wird, liefert der Baustein `TRUE`. Der wesentliche Unterschied ist die visuelle Platzierung und Gestaltungsmöglichkeit innerhalb der grafischen Benutzeroberfläche des Terminals.
