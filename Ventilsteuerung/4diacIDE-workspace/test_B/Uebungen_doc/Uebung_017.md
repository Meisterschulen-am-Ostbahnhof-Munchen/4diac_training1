# Uebung_017: Akustische Signale (Beep)

```{index} single: Uebung_017: Akustische Signale (Beep)
```

[Uebung_017](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_017.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_017`. In dieser Übung wird gezeigt, wie man den internen Summer des ISOBUS-Terminals anspricht, um akustische Rückmeldungen zu geben.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Das tödliche Dilemma des Relais: Warum Silberkontakte bei Kleinsignalen versagen und Gold bei Last schmilzt – Der Freibrenn-Effekt erklärt](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Das-tdliche-Dilemma-des-Relais-Warum-Silberkontakte-bei-Kleinsignalen-versagen-und-Gold-bei-Last-schmilzt--Der-Freibrenn-Effekt-erklrt-e3a9lhv)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_017.png)


## Ziel der Übung

Verwendung des Bausteins `Q_CtrlAudioSignal`. Es wird demonstriert, wie ein Ereignis (hier ein Softkey-Klick) eine Audio-Ausgabe am Terminal mit spezifischer Frequenz und Dauer auslöst.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_017.SUB` löst bei Betätigung eines Softkeys ein Tonsignal aus[cite: 1].

### Funktionsbausteine (FBs)

  * **`SoftKey_UP_F1`**: Der Auslöser.
  * **`Q_CtrlAudioSignal`**: Der ISOBUS-Ausgangsbaustein für Audio.
  * **Parameter**:
    * `u16Frequency`: Tonhöhe in Hertz (hier 440 Hz = Kammerton A).
    * `u16OnTimeMs`: Dauer des Tons (150 ms).
    * `u8NumOfRepit`: Anzahl der Wiederholungen (1).

-----

## Funktionsweise

Die Kette ist rein ereignisbasiert:
Ein Klick (und Loslassen) von Softkey **F1** feuert ein `IND`-Event. Dieses geht direkt an den `REQ`-Eingang des Audio-Bausteins. Das Terminal erhält daraufhin den Befehl, einmalig für 150ms mit 440 Hz zu piepsen.

-----

## Anwendungsbeispiel

**Tastenton-Quittierung**:
Jeder Tastendruck am Terminal soll durch einen kurzen, dezenten Piepston bestätigt werden. Dies gibt dem Bediener eine akustische Rückmeldung über die erfolgreiche Eingabe, auch wenn er nicht direkt auf den Bildschirm schaut.