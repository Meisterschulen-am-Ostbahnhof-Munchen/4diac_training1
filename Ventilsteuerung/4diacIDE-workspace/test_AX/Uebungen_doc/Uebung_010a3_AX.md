# Uebung_010a3_AX: Latching Button (Rastend)

```{index} single: Uebung_010a3_AX: Latching Button (Rastend)
```

[Uebung_010a3_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010a3_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010a3_AX`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [ISOBUS Button: Mehr als nur ein Klick – Die Standardisierung der Landtechnik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Button-Mehr-als-nur-ein-Klick--Die-Standardisierung-der-Landtechnik-e3673rb)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010a3_AX.png)


## Ziel der Übung

Umgang mit rastenden Tasten (Latching Buttons).

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_010a3_AX.SUB` verwendet `Button_L1`[cite: 1].

### Funktionsbausteine (FBs)

  * **`Button_L1`**: Ein Button, der im ISOBUS-Pool als "Latching" definiert ist.

-----

## Funktionsweise

Wie im Code kommentiert: *"Latching Button 'rastet ein', kein T_FF nötig!"*.
Wenn der Nutzer diesen Button drückt, wechselt er seinen Zustand (Visuell z.B. eingedrückt) und sendet dauerhaft `TRUE`. Beim nächsten Druck wechselt er auf `FALSE`. Das Speicherverhalten liegt hier also im **Terminal**, nicht in der SPS-Logik.