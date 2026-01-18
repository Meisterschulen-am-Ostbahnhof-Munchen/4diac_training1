# Uebung_006a4_AX: Motorsteuerung mit Bibliotheksbaustein

```{index} single: Uebung_006a4_AX: Motorsteuerung mit Bibliotheksbaustein
```

[Uebung_006a4_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006a4_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006a4_AX`. Sie ist eine Optimierung von `Uebung_006a3_AX` durch Verwendung eines vorgefertigten Bausteins.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_006a4_AX.png)


## Ziel der Übung

Nutzung von Bibliotheken ("Don't reinvent the wheel").

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006a4_AX.SUB` ersetzt das komplexe Netzwerk aus Gatter und SubApp der vorherigen Übung durch den Baustein `LinksRechts_AX`[cite: 1].

### Funktionsbausteine (FBs)

  * **`LinksRechts`**: Typ `logiBUS::utils::sequence::verteiler::LinksRechts_AX`. Dieser Baustein kapselt die komplette Logik für die Richtungssteuerung und Verriegelung.
  * **`AX_T_FF_SR`**: Liefert weiterhin das "Ein/Aus" Signal an den Eingang `EIN` des Verteilers.

-----

## Funktionsweise

Die Logik ist gekapselt. Der Baustein `LinksRechts_AX` kümmert sich intern darum, das Eingangssignal abwechselnd auf den Ausgang `Links` und `Rechts` zu leiten.

-----

## Vorteil

Der Code ist wesentlich aufgeräumter, lesbarer und weniger fehleranfällig.