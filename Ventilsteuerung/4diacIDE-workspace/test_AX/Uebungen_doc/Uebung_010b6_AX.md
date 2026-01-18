# Uebung_010b6_AX: Softkey Event (SK_PRESSED)

```{index} single: Uebung_010b6_AX: Softkey Event (SK_PRESSED)
```

[Uebung_010b6_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b6_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010b6_AX`.

## 🎧 Podcast

* [ISO 11783-6: Softkeys und das Virtual Terminal verstehen – Dein Schlüssel zur Landmaschinen-Mechatronik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISO-11783-6-Softkeys-und-das-Virtual-Terminal-verstehen--Dein-Schlssel-zur-Landmaschinen-Mechatronik-e36a8b0)

----

![](Uebung_010b6_AX.png)

## Ziel der Übung

Reaktion beim Drücken.

-----

## Beschreibung

[cite_start]Verwendet das Event `SK_PRESSED`[cite: 1].

-----

## Funktionsweise

Das Flip-Flop schaltet bereits im Moment des Berührens ("Touch Down") um, nicht erst beim Loslassen. Das fühlt sich "schneller" an, ist aber untypisch für Touch-Bedienoberflächen (wo man meist noch wegziehen kann, um abzubrechen).