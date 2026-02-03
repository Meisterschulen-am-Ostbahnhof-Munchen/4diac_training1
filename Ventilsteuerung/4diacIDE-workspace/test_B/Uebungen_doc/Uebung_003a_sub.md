# Uebung_003a_sub: IX auf QX (generisch)

```{index} single: Uebung_003a_sub: Universal-Kanal (SubApp)
```

[Uebung_003a_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003a_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt den Sub-App-Typ `Uebung_003a_sub`. Dieser Baustein dient als wiederverwendbare Vorlage für die 1:1 Verbindung eines digitalen Eingangs mit einem digitalen Ausgang.

----

## Ziel der Übung

Kapselung der logiBUS I/O-Logik. Durch die Erstellung eines eigenen Typs wird die Komplexität der Einzelverbindungen nach außen hin verborgen. Der Anwender muss nur noch die Hardware-IDs zuweisen.

-----

## Beschreibung und Komponenten

[cite_start]Der Typ `Uebung_003a_sub` bündelt einen Eingangs- und einen Ausgangsbaustein[cite: 1].

### Interne Funktionsbausteine (FBs)

  * **`IX`**: Typ `logiBUS_IX`. Liest den über den Parameter `Input` zugewiesenen Hardware-Pin ein.
  * **`QX`**: Typ `logiBUS_QX`. Schaltet den über den Parameter `Output` zugewiesenen Hardware-Pin.

-----

## Schnittstellen

[cite_start]Der Baustein verfügt über zwei Konfigurations-Eingänge[cite: 1]:
*   **`Input`**: Erwartet eine Konstante vom Typ `logiBUS_DI_S` (z.B. `Input_I1`).
*   **`Output`**: Erwartet eine Konstante vom Typ `logiBUS_DO_S` (z.B. `Output_Q1`).

Intern sind die Ereignis-Ports (`IND -> REQ`) und die Daten-Ports (`IN -> OUT`) fest miteinander verbunden. Sobald dieser Typ in einem Projekt platziert wird, arbeitet er völlig autark für den zugewiesenen Hardware-Kanal.



## 🛠️ Zugehörige Übungen

* [Uebung_003a](Uebung_003a.md)

