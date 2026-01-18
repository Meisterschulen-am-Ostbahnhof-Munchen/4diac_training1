# Uebung_053: Bit-Manipulation (Assemble/Split)

```{index} single: Uebung_053: Bit-Manipulation (Assemble/Split)
```

[Uebung_053](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_053.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_053`.

## 📺 Video

* [2025-03-11 16-53-43 Watch über App, nicht über Ressource](https://www.youtube.com/watch?v=bGwFMVQBj3k)
* [2025-12-14 19-53-53 Installation Eclipse 4diac™ IDE 3.0.0 und Import des Training1 Projektes](https://www.youtube.com/watch?v=O3S1o_NUyvc)

----

![](Uebung_053.png)

## Ziel der Übung

Kombination von Bits zu einem Byte. Dies ist eine hardwarenahe Form der Bündelung, wie sie oft bei der Kommunikation mit Feldbus-Teilnehmern (z.B. CAN-Bus Nachrichten) vorkommt.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_053.SUB` nutzt Konvertierungs-Bausteine für den Datentyp `BYTE`[cite: 1].

### Funktionsbausteine (FBs)

  * **`ASSEMBLE_BYTE_FROM_BOOLS`**: Wandelt 8 Einzelbits (hier werden 4 genutzt) in einen 8-Bit Ganzzahlwert (BYTE) um.
  * **`SPLIT_BYTE_INTO_BOOLS`**: Zerlegt das Byte wieder in seine einzelnen Bits.

-----

## Funktionsweise

Das Prinzip entspricht Übung 051, jedoch wird anstelle einer Software-Struktur ein standardisierter numerischer Datentyp (`BYTE`) als Container genutzt. Dies ist die effizienteste Form der Datenübertragung, da sie den Speicherverbrauch im Netzwerk minimiert.