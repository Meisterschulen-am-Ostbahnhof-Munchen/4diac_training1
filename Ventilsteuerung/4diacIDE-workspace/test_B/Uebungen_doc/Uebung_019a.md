# Uebung_019a: Alarmmasken und Quittierung

```{index} single: Uebung_019a: Alarmmasken und Quittierung
```

[Uebung_019a](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_019a.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_019a`. Hier wird die Maskenumschaltung um eine Sicherheitsfunktion erweitert: Den Alarm.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_019a.png)


## Ziel der Übung

Erlernen des Umgangs mit Alarm-Masken. Im ISOBUS-Standard haben Alarme Vorrang vor normalen Datenmasken und können oft nur durch eine explizite Quittierung (ACK) verlassen werden.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_019a.SUB` wird ein vierstufiger Selektor (`F_SEL_E_4`) zur Maskenwahl genutzt[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` & `I2`**: Normale Maskenwahl (M1, M2).
  * **`I3`**: Auslöser für den Alarm.
  * **`ACK`**: Ein Softkey am Terminal zum Quittieren des Alarms.
  * **`AlarmMask_A2_medium`**: Eine spezielle Alarm-Maske aus dem Pool.

-----

## Funktionsweise

1.  Durch `I1` und `I2` kann der Nutzer wie gewohnt navigieren.
2.  Tritt ein Fehler ein (`I3`), erzwingt die Steuerung die Anzeige der `AlarmMask_A2`. Das Terminal überlagert nun die aktuelle Ansicht mit der Alarmmeldung.
3.  Die Navigation über `I1/I2` ist nun wirkungslos oder wird vom Alarm überdeckt (je nach Terminal-Implementierung).
4.  Erst wenn der Nutzer am Terminal den Softkey **ACK** drückt, schaltet die Steuerung wieder auf die normale Arbeitsmaske (`M1`) zurück.

-----

## Anwendungsbeispiel

**Überlastwarnung**:
Ein Sensor meldet eine drohende Überlastung der Maschine. Die Steuerung unterbricht die normale Anzeige und blendet großformatig die Warnung "Überlast!" ein. Der Fahrer muss den Fehler bewusst wahrnehmen und am Terminal quittieren, bevor er die normalen Anzeigen wieder nutzen kann.