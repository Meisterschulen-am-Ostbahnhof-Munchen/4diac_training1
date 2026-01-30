# Uebung_128: Globaler Rundruf (Broadcast)

```{index} single: Uebung_128: Globaler Rundruf (Broadcast)
```

[Uebung_128](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_128.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_128`.

----

![](Uebung_128.png)

## Übersicht

[cite_start]In dieser Übung wird eine Nachricht an alle Teilnehmer im Netzwerk gleichzeitig gesendet (Broadcast)[cite: 1].
Dazu wird der Baustein `NetEv2NetEv` mit dem speziellen Handle `GLOBAL_A` (Adresse 255) genutzt. Die resultierende Netzwerk-Identität wird als Ziel (`NmDestin`) für den Sende-Baustein verwendet. Eine so gesendete Nachricht wird von jedem Gerät am ISOBUS empfangen und kann für allgemeine Informationen oder Synchronisations-Signale genutzt werden.