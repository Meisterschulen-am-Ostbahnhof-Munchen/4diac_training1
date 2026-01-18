# Uebung_004c1_AX: Doppelklick-Auswertung

```{index} single: Uebung_004c1_AX: Doppelklick-Auswertung
```

[Uebung_004c1_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004c1_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004c1_AX`. Ab hier widmen wir uns den erweiterten Fähigkeiten des `logiBUS_IE` Bausteins, der komplexe Taster-Muster erkennen kann.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004c1_AX.png)


## Ziel der Übung

Nutzung des Ereignisses `BUTTON_DOUBLE_CLICK`.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004c1_AX.SUB` schaltet eine Lampe nur bei einem Doppelklick um[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1`**: Konfiguriert mit `InputEvent = BUTTON_DOUBLE_CLICK`.

-----

## Funktionsweise

Der Baustein überwacht den Eingang `I1`.
1.  Drückt man einmal: Nichts passiert am Ausgang `IND`.
2.  Drückt man zweimal kurz hintereinander (innerhalb einer definierten Zeitspanne): Der Baustein feuert *ein* `IND` Event.
3.  Das Flip-Flop toggelt.

-----

## Anwendungsbeispiel

**Vermeidung von Fehlbedienung**: Kritische Funktionen (z.B. "Alle Löschen") auf einen Doppelklick legen, damit sie nicht versehentlich ausgelöst werden.
