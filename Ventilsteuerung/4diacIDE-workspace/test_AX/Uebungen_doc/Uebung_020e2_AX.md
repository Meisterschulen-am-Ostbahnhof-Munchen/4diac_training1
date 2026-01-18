# Uebung_020e2_AX: AX_FB_TOF mit Takteingang

```{index} single: Uebung_020e2_AX: AX_FB_TOF mit Takteingang
```

[Uebung_020e2_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020e2_AX.html)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020e2_AX`. Hier wird der adapterbasierte IEC 61131-3 Timer-Baustein `AX_FB_TOF` verwendet, der eine regelmäßige Triggerung (Takt) benötigt.

## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

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