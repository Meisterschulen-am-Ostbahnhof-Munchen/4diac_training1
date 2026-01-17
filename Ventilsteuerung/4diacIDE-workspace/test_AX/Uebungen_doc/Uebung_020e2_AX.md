# Uebung_020e2_AX: AX_FB_TOF mit Takteingang

[Uebung_020e2_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020e2_AX.html)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020e2_AX`. Hier wird der adapterbasierte IEC 61131-3 Timer-Baustein `AX_FB_TOF` verwendet, der eine regelmäßige Triggerung (Takt) benötigt.

----

![](Uebung_020e2_AX.png)

## Ziel der Übung

Realisierung einer Ausschaltverzögerung, die auch während der Nachlaufzeit ihren Status (`ET`) aktualisiert.

-----

## Beschreibung und Komponenten

Die Subapplikation `Uebung_020e2_AX.SUB` nutzt einen `E_CYCLE` Baustein für die Taktung.

### Funktionsbausteine (FBs)

  * **`AX_FB_TOF`**: Der Ausschaltverzögerungs-Timer.
  * **`E_CYCLE`**: Liefert den Takt (500ms) für den Timer.
  * **`AX_SWITCH_I1`**: Startet den Takt bei Aktivierung des Eingangs.
  * **`AX_SWITCH_Q1`**: Stoppt den Takt erst dann, wenn auch der Ausgang des Timers wieder abgefallen ist (Nachlauf beendet).

-----

## Funktionsweise

1.  **Aktivierung**: Bei `I1 = TRUE` wird der Ausgang sofort aktiv und der Taktgeber startet.
2.  **Nachlauf**: Fällt `I1` ab, läuft der Timer weiter. Der `E_CYCLE` bleibt aktiv, da der Ausgang `Q` noch `TRUE` ist.
3.  **Abschluss**: Sobald die 5 Sekunden abgelaufen sind, fällt `Q` ab und der `E_CYCLE` wird gestoppt.

-----

## Fazit

Die Übung zeigt die komplexe Ansteuerung eines Ausschaltverzögerers, bei dem der Taktgeber über die gesamte Dauer (Einschaltzeit + Nachlaufzeit) aktiv bleiben muss.
