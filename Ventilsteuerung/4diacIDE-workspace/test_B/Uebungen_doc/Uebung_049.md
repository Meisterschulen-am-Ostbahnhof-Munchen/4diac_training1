# Uebung_049: Mehrkanal-Mapping (Standard)

```{index} single: Uebung_049: Mehrkanal-Mapping (Standard)
```

[Uebung_049](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_049.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_049`. Diese Übung dient der Übung von umfangreichen Punkt-zu-Punkt-Verbindungen.

## 📺 Video

* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)
* [Aufwärts/Abwärts zählen Baustein E_CTUD aus der IEC 61499 (Übung 82)](https://www.youtube.com/watch?v=H_MRtaMiaU8)
* [D-Flip-Flop: E_D_FF aus der IEC 61499 (Übung 002c) als "Eventbremse"](https://www.youtube.com/watch?v=yGSx_0ggveE)
* [D-Flip-Flop: E_D_FF aus der IEC 61499 (Übung 85)](https://www.youtube.com/watch?v=VNaTUOE5izc)
* [E_CYCLE aus der IEC 61499 (Übung 84)](https://www.youtube.com/watch?v=PWJHijOPpFc)

## 🎧 Podcast

* [4diac IDE: Wie der IEC 61499 Standard die Industrieautomatisierung revolutioniert](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/4diac-IDE-Wie-der-IEC-61499-Standard-die-Industrieautomatisierung-revolutioniert-e36756a)
* [IEC 61499 vs. 61131: Brauchen wir einen neuen Standard für IIoT? Analyse einer hitzigen Debatte um Verteilte Intelligenz](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-vs--61131-Brauchen-wir-einen-neuen-Standard-fr-IIoT--Analyse-einer-hitzigen-Debatte-um-Verteilte-Intelligenz-e3ahc2r)
* [IEC 61499: Befreit der neue Standard die Industrieautomation? Ein Vergleich mit 61131 und die Brücke zwischen OT & IT.](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Befreit-der-neue-Standard-die-Industrieautomation--Ein-Vergleich-mit-61131-und-die-Brcke-zwischen-OT--IT-e368446)
* [IEC 61499: Revolution der Industrieautomation – Warum der neue Standard Ihre Systeme fit für die Zukunft macht](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Revolution-der-Industrieautomation--Warum-der-neue-Standard-Ihre-Systeme-fit-fr-die-Zukunft-macht-e375evm)
* [4diac IDE: Dein Open-Source-Werkzeugkasten für verteilte Industrieautomatisierung nach IEC 61499](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/4diac-IDE-Dein-Open-Source-Werkzeugkasten-fr-verteilte-Industrieautomatisierung-nach-IEC-61499-e36821e)

----

![](Uebung_049.png)

## Übersicht

[cite_start]In `Uebung_049.SUB` werden vier digitale Eingänge (`I1` bis `I4`) direkt auf vier digitale Ausgänge (`Q1` bis `Q4`) gemappt[cite: 1]. Dies ist die Basisform der Signalweiterleitung ohne Logik oder Strukturierung, bei der jeder Kanal über eigene Event- und Data-Connections verfügt. Es dient primär dem Training der manuellen Verdrahtung in der 4diac-IDE.