# Uebung_151_AX: Geschwindigkeitsberechnung (Ableitung)

```{index} single: Uebung_151_AX: Geschwindigkeitsberechnung (Ableitung)
```

[Uebung_151_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_151_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_151_AX`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_151_AX.png)


## Ziel der Übung

Berechnung einer zeitlichen Änderung (Differenzialquotient) aus Impulswerten.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_151_AX.SUB` erweitert den Impulszähler um mathematische Funktionen[cite: 1].

### Funktionsbausteine (FBs)

  * **`logiBUS_PI_ID`**: Liefert den aktuellen Zählerstand.
  * **`FT_DERIV`**: Ein Baustein aus der **OSCAT** Bibliothek zur Berechnung der Ableitung (Änderungsrate).

-----

## Funktionsweise

1.  Der Zählerstand (DWORD) wird in eine Fließkommazahl (REAL) gewandelt.
2.  Der `FT_DERIV` Baustein berechnet, wie schnell sich dieser Wert über die Zeit ändert.
3.  Das Ergebnis ist direkt proportional zur Frequenz der Eingangsimpulse (z.B. km/h oder U/min).

-----

## Anwendungsbeispiel

**Drehzahlüberwachung**: Ein Sensor am Lüfterrad liefert Impulse. Steigt oder fällt die Änderung pro Sekunde unter einen Schwellwert, kann ein Alarm ausgelöst werden.
