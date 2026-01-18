# Uebung_056: Mehrkanal-Statusüberwachung

```{index} single: Uebung_056: Mehrkanal-Statusüberwachung
```

[Uebung_056](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_056.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_056`. Hier wird das Quarter-Konzept auf eine vierkanalige Struktur erweitert.

## 📺 Video

* [2025-01-29 09-27-56 Windows Defender exclusion check in der Eclipse 4diac™ IDE](https://www.youtube.com/watch?v=8k8-QnbTPxk)
* [2025-02-02 18-56-54 DI_LONG_PRESS_HOLD (Teil 1)](https://www.youtube.com/watch?v=8pkKq_8HAIQ)

----

![](Uebung_056.png)

## Übersicht

[cite_start]Die Subapplikation `Uebung_056.SUB` zeigt eine vollständige Diagnose-Pipeline[cite: 1]:
1.  **Eingabe**: Vier Taster (`I1`-`I4`) werden in Quartale gewandelt.
2.  **Bündelung**: Vier Quartale (4 x 2 Bit = 8 Bit) werden über den Baustein `ASSEMBLE_BYTE_FROM_QUARTERS` zu einem einzigen Byte zusammengefasst.
3.  **Transport**: Das Byte wird als Paket übertragen.
4.  **Zerlegung**: `SPLIT_BYTE_INTO_QUARTERS` gewinnt die Information zurück.
5.  **Ausgabe & Diagnose**: Die Signale steuern vier Lampen, während parallel für **jeden** Kanal ein Klartext-Status für das Terminal generiert wird.

Dies ist das Standard-Verfahren für die Übertragung von Sektions-Zuständen (z.B. bei einer Feldspritze) im logiBUS-System.