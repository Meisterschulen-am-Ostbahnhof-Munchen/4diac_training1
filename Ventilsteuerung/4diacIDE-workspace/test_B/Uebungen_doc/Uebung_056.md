# Uebung_056: Mehrkanal-Statusüberwachung

```{index} single: Uebung_056: Mehrkanal-Statusüberwachung
```

[Uebung_056](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_056.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_056`. Hier wird das Quarter-Konzept auf eine vierkanalige Struktur erweitert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

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