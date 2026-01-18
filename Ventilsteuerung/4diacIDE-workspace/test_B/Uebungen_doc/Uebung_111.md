# Uebung_111: Überlauf-Vermeidung durch Typwandlung

```{index} single: Uebung_111: Überlauf-Vermeidung durch Typwandlung
```

[Uebung_111](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_111.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_111`. Hier wird gezeigt, wie man durch rechtzeitige Konvertierung in größere Datentypen Rechenfehler verhindert.


## 📺 Video

* [2025-03-15 16-27-21 Arithmetischer Überlauf führt zu Division durch 0.](https://www.youtube.com/watch?v=7CyOJPYJVz0)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-15 15-57-14 Arithmetischer Überlauf](https://www.youtube.com/watch?v=TLanGc-c9Ww)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)

## Podcast
* [DIN EN 61131-3 vs. 61499-1: Dein Wegweiser durch die Normen der Industrieautomatisierung](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61131-3-vs--61499-1-Dein-Wegweiser-durch-die-Normen-der-Industrieautomatisierung-e36c6nc)
* [Industrielle Automation verstehen: SPS, PLS, SCADA, MES und ERP entschlüsselt – Eine Reise durch die Smart Factory](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Industrielle-Automation-verstehen-SPS--PLS--SCADA--MES-und-ERP-entschlsselt--Eine-Reise-durch-die-Smart-Factory-e3671qn)
* [Code-Renovierung mit AX-Adaptern: Wie Eclipse 4diac™ durch Signal-Bündelung Komplexität besiegt](https://podcasters.spotify.com/pod/show/logibus/episodes/Code-Renovierung-mit-AX-Adaptern-Wie-Eclipse-4diac-durch-Signal-Bndelung-Komplexitt-besiegt-e3ahcd1)
* [Als Landtechnik-Spezialist durch die Hölle: Wie Lanz-Wery Krieg, Besatzung und Hyperinflation überlebte – Einblicke in Original-Geschäftsberichte 1915-1922](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Als-Landtechnik-Spezialist-durch-die-Hlle-Wie-Lanz-Wery-Krieg--Besatzung-und-Hyperinflation-berlebte--Einblicke-in-Original-Geschftsberichte-1915-1922-e39athj)
* [Altbayerisch für Einsteiger: Von Gratler-Schnupfen und Stadthodern – Eine Laute-Reise durch Lektion 3C](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Altbayerisch-fr-Einsteiger-Von-Gratler-Schnupfen-und-Stadthodern--Eine-Laute-Reise-durch-Lektion-3C-e376jh4)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_111.png)


## Übersicht

[cite_start]In `Uebung_111.SUB` wird das Überlauf-Problem aus Übung 110 gelöst[cite: 1].
Bevor die kritische Berechnung oder der Vergleich stattfindet, wird der kleine Datentyp `USINT` über den Baustein `F_USINT_TO_UDINT` in einen großen 32-Bit-Typ gewandelt. Dadurch steht genügend "Platz" für das Ergebnis zur Verfügung, und der anschließende Vergleich liefert das mathematisch korrekte Ergebnis. Dies demonstriert den sauberen Umgang mit verschiedenen numerischen Genauigkeiten im Programmablauf.