# Uebung_094a_AX: Deaktivieren von Bausteinen (QI)

```{index} single: Uebung_094a_AX: Deaktivieren von Bausteinen (QI)
```

[Uebung_094a_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_094a_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_094a_AX`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [DIN EN 61499: Industrielle Steuerungen modular und ereignisbasiert mit Funktionsbausteinen meistern – Der ESR-Schalter im Fokus](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-Industrielle-Steuerungen-modular-und-ereignisbasiert-mit-Funktionsbausteinen-meistern--Der-ESR-Schalter-im-Fokus-e367nra)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_094a_AX.png)


## Ziel der Übung

Nutzung des `QI` (Qualifier Input) Parameters zur Laufzeit-Steuerung von Funktionsbausteinen.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_094a_AX.SUB` schaltet einen Eingangspfad aktiv oder inaktiv[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I2`**: Toggelt über ein Flip-Flop den Zustand "Aktiv/Inaktiv".
  * **`DigitalInput_I1`**: Der eigentliche Signaleingang. Sein `QI` Parameter ist variabel beschaltet.
  * **`DigitalOutput_Q1`**: Hängt an `I1`.
  * **`DigitalOutput_Q2`**: Zeigt den Status "Ist Aktiv" an.

-----

## Funktionsweise

1.  Drückt man `I2`, schaltet `Q2` ein (System aktiviert).
2.  Gleichzeitig wird `QI` von `DigitalInput_I1` auf TRUE gesetzt.
3.  Jetzt funktioniert `I1`: Wenn man `I1` drückt, schaltet `Q1`.
4.  Drückt man `I2` erneut, schaltet `Q2` aus (System deaktiviert).
5.  `QI` von `I1` wird FALSE.
6.  Der Baustein `I1` stellt seine Arbeit ein. Änderungen am physischen Eingang `I1` werden nicht mehr an `Q1` weitergeleitet.

-----

## Anwendungsbeispiel

**Wartungsmodus**: Teile der Sensorik werden softwareseitig "abgeklemmt", damit bei Arbeiten an der Maschine keine Fehlalarme ausgelöst werden.