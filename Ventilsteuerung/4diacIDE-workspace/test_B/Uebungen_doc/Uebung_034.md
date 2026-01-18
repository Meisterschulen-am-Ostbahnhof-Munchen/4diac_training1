# Uebung_034: Leistungsregelung (Analog zu PWM)

```{index} single: Uebung_034: Leistungsregelung (Analog zu PWM)
```

[Uebung_034](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_034.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_034`. Hier wird ein analoger Messwert genutzt, um die Leistung eines Aktors stufenlos zu regeln.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_034.png)


## Ziel der Übung

Verbindung eines Analog-Eingangs (`logiBUS_AI`) mit einem PWM-Ausgang (`logiBUS_QD_PWM`). Es wird demonstriert, wie Datenwerte skaliert werden, um den Stellbereich eines Sensors auf den Leistungsbereich eines Aktors abzubilden.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_034.SUB` liest ein Potentiometer ein und steuert damit die Helligkeit einer Lampe oder die Drehzahl eines Motors[cite: 1].

### Funktionsbausteine (FBs)

  * **`AnalogInput_I7`**: Liest die Spannung am Eingang ein.
  * **`F_SHL`**: Ein Schieberegister-Baustein (Shift Left). [cite_start]Er wird hier zur Skalierung genutzt, indem er den Eingangswert um ein Bit nach links verschiebt (entspricht einer Multiplikation mit 2)[cite: 1].
  * **`PWMOutput_Q4`**: Ein pulsweitenmodulierter Ausgang zur Leistungsstellung.

-----

## Funktionsweise

1.  Jede Änderung am analogen Eingang `I7` löst ein `IND`-Event aus.
2.  Der Wert wird im `F_SHL` angepasst, um den gewünschten Zielbereich zu erreichen.
3.  Das Ergebnis wird an den `OUT`-Port des PWM-Bausteins gesendet und über `REQ` aktiviert.
4.  Der Aktor an `Q4` reagiert sofort auf die neue Vorgabe.

-----

## Anwendungsbeispiel

**Licht-Dimmer oder Lüfter-Steuerung**:
Durch Drehen an einem physischen Potentiometer (`I7`) kann der Bediener die Helligkeit der Kabinenbeleuchtung oder die Stärke eines Gebläses (`Q4`) stufenlos regeln. Die Software sorgt für die latenzfreie Übertragung der Steuerbefehle.