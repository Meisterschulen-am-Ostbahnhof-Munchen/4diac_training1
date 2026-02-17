# Uebung_004c7_AX: Toggle Flip-Flop mit IE mit BUTTON_PRESS_END

```{index} single: Uebung_004c7_AX: Parametrierter Langer Druck
```

[Uebung_004c7_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004c7_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004c7_AX`. Auch hier wird `logiBUS_IE2` genutzt, um die Zeitdauer für einen "langen Druck" anzupassen.

----

![](Uebung_004c7_AX.png)

## Ziel der Übung

Definition einer spezifischen Haltezeit.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004c7_AX.SUB` nutzt `logiBUS_IE2` mit `InputEvent = BUTTON_LONG_PRESS_START` und `arg = 3000` (ms)[cite: 1].

-----

## Funktionsweise

Das Event feuert erst, wenn der Taster für **3 Sekunden** (3000ms) gedrückt gehalten wird. Dies überschreibt den Standardwert (der meist bei 500ms oder 1s liegt).

-----

## Anwendungsbeispiel

**Werkseinstellungen laden**: Eine sehr destruktive Aktion, die extrem gut gegen versehentliches Auslösen geschützt sein muss. Der Nutzer muss bewusst lange drücken.