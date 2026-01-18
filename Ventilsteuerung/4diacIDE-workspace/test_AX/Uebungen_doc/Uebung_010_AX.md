# Uebung_010_AX: ISOBUS Softkey (Direkt)

```{index} single: Uebung_010_AX: ISOBUS Softkey (Direkt)
```

[Uebung_010_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010_AX`. Hier betreten wir die Welt des ISOBUS (ISO 11783). Anstelle von physischen Eingängen nutzen wir virtuelle Tasten auf einem Terminal (Universal Terminal, UT).


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010_AX.png)


## Ziel der Übung

Verwendung eines `Softkey`-Bausteins zur Steuerung eines Ausgangs.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_010_AX.SUB` verbindet eine Softkey-Instanz mit einem digitalen Ausgang[cite: 1].

### Funktionsbausteine (FBs)

  * **`SoftKey_F1`**: Typ `isobus::UT::io::Softkey::Softkey_IXA`. Dieser Baustein repräsentiert die Taste "F1" auf dem Bildschirm des ISOBUS-Terminals.
  * **`DigitalOutput_Q1`**: Der physische Ausgang.

### Parameter

*   `u16ObjId`: Verweist auf die Objekt-ID des Softkeys im Objekt-Pool (hier `SoftKey_F1`).

-----

## Funktionsweise

Die Funktionsweise ist identisch zu einem physischen Taster. Solange der Nutzer den Finger auf dem Touchscreen (oder die Taste am Rand) hält, liefert der Baustein `TRUE`. Lässt er los, wird `FALSE` gesendet.

-----

## Anwendungsbeispiel

**Maschinenfunktion einschalten**: Der Fahrer drückt auf dem Bildschirm das Symbol für "Arbeitsscheinwerfer", und das Licht geht an (solange er drückt).
