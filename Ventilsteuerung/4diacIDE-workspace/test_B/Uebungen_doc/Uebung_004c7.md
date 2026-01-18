# Uebung_004c7: Parametrierter langer Tastendruck

```{index} single: Uebung_004c7: Parametrierter langer Tastendruck
```

[Uebung_004c7](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004c7.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004c7`. Auch hier wird der Baustein `logiBUS_IE2` genutzt, um die Haltezeit für ein Ereignis individuell anzupassen.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004c7.png)


## Ziel der Übung

Festlegung einer spezifischen Zeitdauer für einen langen Tastendruck.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004c7.SUB` nutzt `logiBUS_IE2` mit `BUTTON_LONG_PRESS_START` und dem Argument `arg = 3000`[cite: 1].

-----

## Funktionsweise

Die Einheit des Arguments `arg` sind Millisekunden. Das bedeutet: Das Ereignis `IND` wird erst dann gefeuert, wenn der Taster für **mindestens 3 Sekunden** (3000ms) ununterbrochen gedrückt wurde. Dies überschreibt den im System hinterlegten Standardwert für "Long Press".

-----

## Anwendungsbeispiel

**Werkseinstellungen laden (Factory Reset)**: Eine kritische Aktion, die eine sehr bewusste und lange Interaktion des Nutzers erfordert, um versehentliche Datenverluste absolut sicher auszuschließen.
