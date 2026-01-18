# Uebung_083: Präzisions-Zähler (UDINT)

```{index} single: Uebung_083: Präzisions-Zähler (UDINT)
```

[Uebung_083](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_083.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_083`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_083.png)


## Übersicht

[cite_start]Diese Übung verwendet den Baustein `E_CTUD_UDINT`[cite: 1]. Im Gegensatz zum Standard-Zähler (der meist nur bis 65.535 zählt) nutzt dieser Typ den Datentyp `UDINT` (Unsigned Double Integer). Damit können Ereignisse bis zu einem Wert von über 4 Milliarden gezählt werden.
Zusätzlich zur Ansteuerung der Lampen `Q1` und `Q2` wird der aktuelle Zählerstand (`CV`) direkt an eine numerische Anzeige am ISOBUS-Terminal gesendet. Dies ermöglicht eine genaue Beobachtung des Zählvorgangs in Echtzeit.
