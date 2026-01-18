# Uebung_053: Bit-Manipulation (Assemble/Split)

```{index} single: Uebung_053: Bit-Manipulation (Assemble/Split)
```

[Uebung_053](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_053.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_053`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

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