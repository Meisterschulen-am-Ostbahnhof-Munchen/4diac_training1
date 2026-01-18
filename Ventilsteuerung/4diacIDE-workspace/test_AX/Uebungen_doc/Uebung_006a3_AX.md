# Uebung_006a3_AX: Motorsteuerung (Links/Rechts) mit Verriegelung

```{index} single: Uebung_006a3_AX: Motorsteuerung (Links/Rechts) mit Verriegelung
```

[Uebung_006a3_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006a3_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006a3_AX`. Dies ist eine komplexere Anwendung zur Ansteuerung eines Motors mit zwei Drehrichtungen.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_006a3_AX.png)


## Ziel der Übung

Realisierung einer Wende-Schütz-Steuerung mit Software-Verriegelung. Es darf niemals gleichzeitig "Links" und "Rechts" angesteuert werden, da dies einen Kurzschluss im Leistungskreis verursachen würde.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006a3_AX.SUB` nutzt eine Kombination aus Flip-Flop, Splitter und einer custom Sub-App (`Uebung_006a3_sub_AX`)[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` (Set)**: Einschalten (in die zuletzt gewählte Richtung oder Default).
  * **`I2` (Reset)**: Ausschalten.
  * **`I3` (Toggle)**: Start/Stopp.
  * **`AX_T_FF_SR`**: Der Hauptspeicher "Motor Ein/Aus".
  * **`AX_SPLIT_3`**: Verteilt das "Motor ist an"-Signal.
  * **`AX_LinksRechts_T_FF` (SubApp)**: Speichert die aktuelle *Richtung* (Links oder Rechts).
  * **2x `AX_AND_2`**: Verriegelungsgatter.

-----

## Funktionsweise

1.  Das `AX_T_FF_SR` bestimmt, ob der Motor überhaupt laufen soll.
2.  Die SubApp `AX_LinksRechts_T_FF` ist ein Richtungs-Speicher (Toggle). Jedes Mal, wenn der Motor eingeschaltet wird (Event von `SPLIT_3.OUT1`), toggelt diese SubApp die Richtung für den *nächsten* oder *aktuellen* Lauf (abhängig von der genauen internen Verschaltung).
3.  Die UND-Gatter verknüpfen "Motor Ein" (`SPLIT_3`) mit "Richtung Links" bzw. "Richtung Rechts".
4.  Dadurch ist sichergestellt, dass immer nur ein Ausgang (`Q1` oder `Q2`) aktiv ist.

*Hinweis: Die genaue Logik des Richtungwechsels (bei jedem Start? oder durch extra Taste?) hängt von der `Uebung_006a3_sub_AX` ab.*

-----

## Anwendungsbeispiel

**Waschmaschine** oder **Rührwerk**: Der Motor soll abwechselnd links und rechts laufen, aber natürlich nie gleichzeitig.