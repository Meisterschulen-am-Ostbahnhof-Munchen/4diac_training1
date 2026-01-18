# Uebung_011a: Dynamische Anzeige (Repeat Done)

```{index} single: Uebung_011a: Dynamische Anzeige (Repeat Done)
```

[Uebung_011a](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_011a.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_011a`. Hier wird die Interaktion zwischen Taster-Ereignissen und numerischen Anzeigen auf dem Terminal vertieft.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [Zusätzlich: Uebung_083: Aufwärts/Abwärts zählen: E_CTUD_UDINT Datentyp UDINT; mit Anzeige am VT.](https://www.youtube.com/watch?v=oTPDtsw5eAw)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [ISOBUS Output Meter: Dynamische Anzeigen meistern – vom Zeiger bis zur Visualisierung auf dem VT](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Output-Meter-Dynamische-Anzeigen-meistern--vom-Zeiger-bis-zur-Visualisierung-auf-dem-VT-e36t2tp)
* [ISOBUS Object Pointer: Das Geheimnis dynamischer Displays und effizienter Fehlerdiagnose](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Object-Pointer-Das-Geheimnis-dynamischer-Displays-und-effizienter-Fehlerdiagnose-e36bp75)
* [ISOBUS-Bedienoberflächen: Wenn Tasten und Hauptanzeige unterschiedlich skalieren – ISO 11783-6 entschlüsselt](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Bedienoberflchen-Wenn-Tasten-und-Hauptanzeige-unterschiedlich-skalieren--ISO-11783-6-entschlsselt-e36a8n8)
* [ISOBUS-Container: Dynamische Bedienfelder für klare Sicht und mehr Effizienz](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Container-Dynamische-Bedienfelder-fr-klare-Sicht-und-mehr-Effizienz-e36alr9)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_011a.png)


## Ziel der Übung

Nutzung des `BUTTON_PRESS_REPEAT_DONE` Ereignisses zur Aktualisierung eines Anzeige-Objekts.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_011a.SUB` wird ein Byte-Wert von einem Taster eingelesen und an eine numerische Anzeige am Terminal gesendet[cite: 1].

### Funktionsbausteine (FBs)

  * **`logiBUS_IB`**: Eingangsbaustein für Byte-Werte. Er ist auf das Event `BUTTON_PRESS_REPEAT_DONE` konfiguriert.
  * **`Q_NumericValue`**: Ausgangsbaustein zur Anzeige einer Zahl auf dem Terminal.

-----

## Funktionsweise

Das Besondere ist die Wahl des Eingangs-Ereignisses:
*   **`BUTTON_PRESS_REPEAT`**: Würde während des Drückens ständig Ereignisse senden (Blinker-Effekt).
*   **`BUTTON_PRESS_REPEAT_DONE`**: Feuert nur **ein einziges Mal**, nämlich dann, wenn der Nutzer den Taster nach einer (eventuell wiederholten) Betätigung endgültig loslässt.

Die Logik sorgt dafür, dass der aktuelle Byte-Wert des Tasters (z.B. eine ID oder ein Zählerstand) erst am Ende der Interaktion an das Terminal übertragen wird.

-----

## Anwendungsbeispiel

**Zähler-Übertragung**:
Ein Bediener hält einen Taster gedrückt, um einen Wert intern hochzuzählen. Damit der CAN-Bus nicht durch ständige Display-Updates belastet wird, erfolgt die Aktualisierung der Anzeige auf dem Terminal erst dann, wenn der Finger weggenommen wird (`REPEAT_DONE`).