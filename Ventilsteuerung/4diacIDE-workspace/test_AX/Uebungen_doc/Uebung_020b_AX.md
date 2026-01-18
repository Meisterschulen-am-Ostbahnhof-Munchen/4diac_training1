# Uebung_020b_AX: Einschaltverzögerung (aufgelöst)

```{index} single: Uebung_020b_AX: Einschaltverzögerung (aufgelöst)
```

[Uebung_020b_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020b_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020b_AX`. Hier wird eine Einschaltverzögerung (TON) nicht als fertiger Baustein verwendet, sondern aus diskreten Ereignis- und Speicherbausteinen aufgebaut.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_020b_AX.png)


## Ziel der Übung

Das Ziel dieser Übung ist es, das Verständnis für die zeitliche Steuerung von Ereignissen zu vertiefen. Anstatt den fertigen `AX_TON` Baustein (siehe `Uebung_020c_AX`) zu nutzen, wird hier demonstriert, wie ein `E_DELAY` Baustein in eine Logikschleife eingebunden werden kann, um eine identische Funktionalität zu erreichen.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_020b_AX.SUB` kombiniert eine Ereignis-Weiche, eine Zeitverzögerung und einen RS-Speicher[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1`**: Typ `logiBUS_IXA`. Signaleingang.
  * **`AX_SWITCH`**: [cite_start]Leitet das Ereignis bei steigender Flanke an `EO1` und bei fallender Flanke an `EO0` weiter[cite: 1].
  * **`E_DELAY`**: [cite_start]Verzögert ein am `START`-Eingang eintreffendes Ereignis um die Zeit `DT` (hier 2 Sekunden)[cite: 1].
  * **`AX_RS`**: Der Ergebnisspeicher.
  * **`DigitalOutput_Q1`**: Typ `logiBUS_QXA`. Signalausgang.

-----

## Funktionsweise

Die Logik arbeitet in drei Phasen:

1.  **Einschalten (Start der Verzögerung)**:
    Wird `I1` gedrückt, sendet die Weiche ein Event an `E_DELAY.START`. Die Zeit läuft.
2.  **Ablauf der Zeit (Durchschalten)**:
    Nach 2 Sekunden feuert `E_DELAY` an seinem Ausgang `EO`. Dieses Event setzt den Speicher `AX_RS.S` -> `Q1` geht an.
3.  **Ausschalten (Sofort-Stopp)**:
    Wird `I1` losgelassen, sendet die Weiche ein Event an `EO0`. Dieses Event stoppt sofort eine eventuell laufende Zeitmessung (`E_DELAY.STOP`) und setzt gleichzeitig den Speicher zurück (`AX_RS.R`) -> `Q1` geht sofort aus.

Im Ergebnis leuchtet die Lampe nur, wenn der Taster mindestens 2 Sekunden lang gehalten wird. Wird er vorher losgelassen, passiert nichts.

-----

## Anwendungsbeispiel

**Schutz gegen Fehlbedienung**: Ein Taster zum Öffnen eines schweren Tors oder zum Starten einer Maschine muss 2 Sekunden lang gehalten werden, um eine versehentliche Betätigung auszuschließen.