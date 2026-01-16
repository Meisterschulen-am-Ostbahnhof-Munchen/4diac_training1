# Uebung_091: Ereignis-Salve (E_TRAIN)

[Uebung_091](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_091.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_091`. Hier wird die automatische Erzeugung einer festen Anzahl von Ereignissen demonstriert.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_091.png)


## Ziel der Übung

Verwendung des Bausteins `E_TRAIN`. Ziel ist es, nach einem einzelnen Start-Impuls eine definierte Folge von Ereignissen auszulösen.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_091.SUB` wird ein Ereignis-Zug (Train) zur Steuerung eines Flip-Flops genutzt[cite: 1].

### Funktionsweise

1.  Der Nutzer klickt einmal auf Taster **I1**.
2.  Der Baustein `E_TRAIN` startet seine Arbeit.
3.  Laut Parameter `N=8` und `DT=1s` sendet der Baustein nun exakt **8 Ereignisse** im Abstand von jeweils einer Sekunde aus.
4.  Diese Ereignisse gelangen an das Toggle-Flip-Flop.
5.  Die Lampe an `Q1` blinkt daraufhin genau viermal (4 x An, 4 x Aus) und bleibt dann in der letzten Position stehen.

-----

## Anwendungsbeispiel

**Automatisches Abkippen**:
Ein Hydraulikzylinder soll zum Lockern von Material dreimal kurz ruckeln. Ein Tastendruck löst die Salve von 6 Steuerbefehlen (Ausfahren-Einfahren x 3) aus, woraufhin die Steuerung den Vorgang selbstständig beendet.
