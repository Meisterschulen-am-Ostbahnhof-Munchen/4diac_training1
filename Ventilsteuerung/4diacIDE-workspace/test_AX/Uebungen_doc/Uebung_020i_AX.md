# Uebung_020i_AX: Teach-In Puls (Stoppuhr)

```{index} single: Uebung_020i_AX: Teach-In Puls (Stoppuhr)
```

[Uebung_020i_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020i_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020i_AX`. Diese Übung kombiniert Zeitmessung und Zeitsteuerung zu einer lernfähigen Puls-Funktion.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_020i_AX.png)


## Ziel der Übung

Das Ziel ist die Implementierung eines Teach-In-Verfahrens. Anstatt die Zeit `PT` fest im Programm zu hinterlegen, kann der Bediener die gewünschte Dauer durch Halten eines Tasters vorgeben. Die Steuerung speichert diese Zeit und wendet sie bei zukünftigen Impulsen an.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_020i_AX.SUB` nutzt eine Stoppuhr, um die Zeitvorgabe für einen Puls-Baustein dynamisch zu ändern[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I2` (Teach-Taste)**: Typ `logiBUS_IXA`. Misst, wie lange der Taster gedrückt wird.
  * **`AX_SWITCH`**: Wandelt das Drücken/Loslassen von `I2` in Start/Stopp-Signale für die Stoppuhr um.
  * **`E_STOPWATCH`**: [cite_start]Misst die Zeit zwischen `START` und `STOP` und gibt die Dauer am Ausgang `TD` aus[cite: 1].
  * **`AX_PULSE`**: Der Impuls-Baustein. Sein Zeitparameter `PT` ist mit dem gemessenen Wert `TD` der Stoppuhr verbunden.
  * **`DigitalInput_CLK_I1` (Start-Taste)**: Typ `logiBUS_IE`. Löst den Puls aus.
  * **`DigitalOutput_Q1`**: Typ `logiBUS_QXA`. Signalausgang.

-----

## Funktionsweise

Die Anwendung erfolgt in zwei Schritten:

1.  **Anlernen (Teach-In)**:
    Der Nutzer hält Taster `I2` für die gewünschte Dauer gedrückt (z.B. 3,5 Sekunden).
    *   Beim Drücken startet `E_STOPWATCH`.
    *   Beim Loslassen stoppt die Messung. Der Wert (3,5s) liegt nun am Eingang `PT` von `AX_PULSE` an.
2.  **Ausführen**:
    Der Nutzer klickt kurz auf Taster `I1`.
    *   `AX_PULSE` wird getriggert und schaltet die Lampe `Q1` für exakt die zuvor gelernten 3,5 Sekunden ein.

Jedes neue Anlernen über `I2` überschreibt die gespeicherte Zeit für den nächsten Puls.

-----

## Anwendungsbeispiel

**Dosiersteuerung**: Ein Landwirt möchte die Ausbringmenge eines Zusatzstoffs manuell kalibrieren. Er hält den Befüllknopf so lange, bis die gewünschte Testmenge erreicht ist. Die Steuerung merkt sich diese Zeit und kann den Dosiervorgang ab nun per einfachem Tastendruck exakt wiederholen.