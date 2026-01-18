# Uebung_004c4_AX: Gedrückt halten (Wiederholung)

```{index} single: Uebung_004c4_AX: Gedrückt halten (Wiederholung)
```

[Uebung_004c4_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004c4_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004c4_AX`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Der E_T_FF_SR-Baustein: Herzstück der IEC 61499 – Speichern, Umschalten, Reagieren](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_T_FF_SR-Baustein-Herzstck-der-IEC-61499--Speichern--Umschalten--Reagieren-e3682dm)
* [Reihenschaltung von Widerständen: Grundlagen und Verhalten](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Reihenschaltung-von-Widerstnden-Grundlagen-und-Verhalten-e368ie0)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004c4_AX.png)


## Ziel der Übung

Nutzung des Ereignisses `BUTTON_LONG_PRESS_HOLD`.

-----

## Funktionsweise

[cite_start]Der Baustein `DigitalInput_CLK_I1` in `Uebung_004c4_AX.SUB` ist auf `BUTTON_LONG_PRESS_HOLD` konfiguriert[cite: 1].

Dieses Event wird *periodisch* gefeuert, solange der Taster nach Erkennung des langen Drucks weiterhin gehalten wird.

-----

## Anwendungsbeispiel

**Lautstärke ändern / Scrollen**: Solange man die Taste gedrückt hält, wird die Lautstärke schrittweise erhöht oder durch ein Menü gescrollt. Das Toggle-FF würde hier sehr schnell an und aus gehen (Flackern), was zeigt, dass dieses Event eher für Inkrement-Funktionen als für Toggles gedacht ist.