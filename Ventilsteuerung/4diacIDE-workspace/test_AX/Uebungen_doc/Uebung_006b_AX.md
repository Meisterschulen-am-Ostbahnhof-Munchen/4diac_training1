# Uebung_006b_AX: RS-Flip-Flop (Rücksetzen dominant)

```{index} single: Uebung_006b_AX: RS-Flip-Flop (Rücksetzen dominant)
```

[Uebung_006b_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006b_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006b_AX`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_006b_AX.png)


## Ziel der Übung

Unterschied zwischen SR (Set Priority) und RS (Reset Priority) verstehen.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006b_AX.SUB` nutzt einen `AX_RS` Baustein[cite: 1].

### Funktionsbausteine (FBs)

  * **`AX_RS`**: Ein RS-Flip-Flop.

-----

## Funktionsweise

Funktional sehr ähnlich zu `AX_SR`. Der Unterschied liegt im Verhalten, wenn **gleichzeitig** (im selben SPS-Zyklus) ein Set- und ein Reset-Event eintreffen (oder wenn beide Eingänge TRUE sind bei pegelgesteuerten Bausteinen).
*   **SR**: Setzen hat Vorrang -> Ausgang wird TRUE.
*   **RS**: Rücksetzen hat Vorrang -> Ausgang wird FALSE.

In der IEC 61499 mit Event-Verarbeitung ist "Gleichzeitigkeit" subtiler, da Events oft sequenziell abgearbeitet werden. Wenn jedoch z.B. durch einen `E_SPLIT` beide Events im selben "Step" ankommen, entscheidet die interne Logik des Bausteins. Beim `AX_RS` gewinnt im Zweifel das Reset.

-----

## Anwendungsbeispiel

**Sicherheitskritische Abschaltung**: Wenn jemand "Start" drückt, während "Not-Aus" gedrückt ist, darf die Maschine **nicht** anlaufen. Daher Reset-Dominanz (RS).