# Uebung_094: Ereignis-Freigabe (PERMIT)

```{index} single: Uebung_094: Ereignis-Freigabe (PERMIT)
```

[Uebung_094](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_094.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_094`. Hier wird eine Schutzfunktion für Ereignisströme implementiert.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_094.png)


## Ziel der Übung

Verwendung des Bausteins `E_PERMIT`. Ziel ist es, die Ausführung einer Aktion (Ereignis) von einer Bedingung (Datenwert) abhängig zu machen.

-----

## Funktionsweise

[cite_start]Die Subapplikation `Uebung_094.SUB` nutzt einen Schalter als Freigabe für einen Taster[cite: 1].
*   Taster **I2** liefert den Auslöse-Impuls.
*   Schalter **I1** liefert die Freigabe (`PERMIT`).
*   Nur wenn **I1** auf `TRUE` steht, leitet der Baustein den Klick von **I2** an das Flip-Flop weiter. Ist der Schalter aus, verpufft das Ereignis wirkungslos.

Dies ist eine einfache, aber effektive Methode zur Realisierung von Verriegelungen.
