# Uebung_010b1: ISOBUS AUX-N (Joystick-Tasten)

```{index} single: Uebung_010b1: ISOBUS AUX-N (Joystick-Tasten)
```

[Uebung_010b1](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b1.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010b1`. Hier wird die dritte Säule der ISOBUS-Bedienung eingeführt: Auxiliary Functions (AUX-N).


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010b1.png)


## Ziel der Übung

Anbindung von AUX-Eingabegeräten (z.B. ISOBUS-Joystick).

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_010b1.SUB` wird eine Auxiliary Function genutzt, um einen Ausgang zu schalten[cite: 1].

### Funktionsbausteine (FBs)

  * **`AuxFunction2_X1`**: Typ `isobus::UT::io::Auxiliary::IN::Aux_IX`. Dieser Baustein lauscht auf AUX-Nachrichten der "Funktion 2".

-----

## Funktionsweise

Im Gegensatz zu Softkeys, die ein festes Bildschirmelement sind, ist eine AUX-Funktion ein logisches Objekt. Der Bediener muss am Terminal (über das AUX-Menü) einmalig festlegen, welche physische Taste seines Joysticks er dieser "Funktion 2" zuweisen möchte. Sobald dieses "Teaching" abgeschlossen ist, triggert jeder Druck auf die Joystick-Taste den Baustein in 4diac.
