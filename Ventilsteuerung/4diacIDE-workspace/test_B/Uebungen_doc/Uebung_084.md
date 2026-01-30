# Uebung_084: Automatischer Zähler (Takt & Zählung)

```{index} single: Uebung_084: Automatischer Zähler (Takt & Zählung)
```

[Uebung_084](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_084.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_084`. Hier wird der Zähler nicht manuell, sondern durch einen Taktgeber gesteuert.

----

![](Uebung_084.png)

## Ziel der Übung

Kombination von Zeitbasis (`E_CYCLE`) und Ereignis-Zähler (`E_CTU`).

-----

## Funktionsweise

[cite_start]In `Uebung_084.SUB` wird der Zähler automatisch jede Sekunde inkrementiert[cite: 1].
*   Taster **I1** startet den Taktgeber.
*   Jedes Sekunde-Event vom `E_CYCLE` erreicht den `CU`-Eingang des Zählers.
*   Nach 5 Sekunden erreicht der Zähler den Wert 5 und die Lampe `Q1` geht an.
*   Taster **I2** stoppt den Taktgeber (Pause).
*   Taster **I3** setzt den Zähler auf Null zurück.

Dies ist die Basis für die Implementierung von Zeit-Grenzwerten oder verzögerten Abschaltungen über längere Zeiträume.