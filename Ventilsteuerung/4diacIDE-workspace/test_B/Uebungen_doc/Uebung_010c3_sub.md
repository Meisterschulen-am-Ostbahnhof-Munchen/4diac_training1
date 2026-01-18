# Uebung_010c3_sub: Softkey mit Feedback (SubApp)

```{index} single: Uebung_010c3_sub: Softkey mit Feedback (SubApp)
```

[Uebung_010c3_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010c3_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

## Übersicht

[cite_start]Dieser Sub-App-Typ kombiniert eine Softkey-Eingabe mit einem automatischen visuellen Feedback auf dem Terminal[cite: 1].
Er bündelt die Bausteine `Softkey_IX`, `GreenWhiteBackground` und `DigitalOutput_QX`. Der Anwender muss lediglich die `u16ObjId` des Softkeys und den physischen `Output` angeben. Der Baustein stellt sicher, dass bei jeder Betätigung sowohl der Hardware-Ausgang geschaltet als auch der Hintergrund des Softkeys am Terminal farblich (Grün/Weiß) angepasst wird. Dies reduziert den Projektierungsaufwand bei komplexen Bedienoberflächen erheblich.