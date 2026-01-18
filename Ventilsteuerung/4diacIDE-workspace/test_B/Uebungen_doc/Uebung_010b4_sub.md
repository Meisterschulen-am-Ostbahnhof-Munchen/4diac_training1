# Uebung_010b4_sub: Softkey-Mapping-Einheit (SubApp)

```{index} single: Uebung_010b4_sub: Softkey-Mapping-Einheit (SubApp)
```

[Uebung_010b4_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b4_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

## Übersicht

[cite_start]Dieser Sub-App-Typ dient der strukturierten Anbindung von ISOBUS-Softkeys an Hardware-Ausgänge[cite: 1].
Er bündelt eine `Softkey_IX` Instanz und einen `DigitalOutput_QX` Baustein. Über die Parameter `u16ObjId` und `Output` kann die Zuordnung zwischen virtuellem Button und physischer Lampe/Ventil direkt an der Sub-App vorgenommen werden. Dies ermöglicht den Aufbau von großen Bedien-Matrizen (wie in Übung 010b4 gezeigt) mit minimalem Verdrahtungsaufwand im Hauptdiagramm.