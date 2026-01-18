# Uebung_010b6_AX: Softkey Event (SK_PRESSED)

```{index} single: Uebung_010b6_AX: Softkey Event (SK_PRESSED)
```

[Uebung_010b6_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b6_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010b6_AX`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

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
