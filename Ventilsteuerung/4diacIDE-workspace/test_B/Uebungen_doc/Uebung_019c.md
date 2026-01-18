# Uebung_019c: Interaktive Alarm-Verriegelung

```{index} single: Uebung_019c: Interaktive Alarm-Verriegelung
```

[Uebung_019c](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_019c.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_019c`. Dies ist die komplexeste Navigations-Logik, bei der die Maskenumschaltung aktiv vom Hardware-Zustand blockiert werden kann.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Das Alarm Mask Objekt: Dein standardisierter Wachposten für Warnungen auf Landmaschinen](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/Das-Alarm-Mask-Objekt-Dein-standardisierter-Wachposten-fr-Warnungen-auf-Landmaschinen-e36e6c3)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_019c.png)


## Ziel der Übung

Implementierung einer bedingten Navigationssteuerung. Der Wechsel der Bildschirmseiten soll unterbunden werden, solange ein aktiver Alarm anliegt.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_019c.SUB` nutzt mehrere `E_SWITCH` Bausteine als "Türsteher" für die Ereignisse[cite: 1].

### Funktionsbausteine (FBs)

  * **`Alarmeingang`**: Ein physischer Sensor (`I3`). Solange dieser `TRUE` ist, herrscht Alarmzustand.
  * **`E_SWITCH` (diverse)**: Prüfen vor jeder Aktion, ob der Alarmeingang aktiv ist.
  * **`ACK`**: Ein physischer Quittier-Taster (`I4`) anstelle eines Softkeys.

-----

## Funktionsweise

Die Weichen blockieren die normalen Navigations-Befehle:
1.  Drückt der Nutzer `I1` (Maske 1), geht das Event zuerst an einen `E_SWITCH`.
2.  Die Weiche prüft den `Alarmeingang`.
    *   Ist **kein** Alarm vorhanden (`G=FALSE`), wird das Event zu `EO0` ➡️ `F_SEL_E_4` durchgelassen. Die Seite wechselt.
    *   Ist ein Alarm aktiv (`G=TRUE`), landet das Event bei `EO1` (nicht verbunden). Der Seitenwechsel wird **ignoriert**.
3.  Tritt ein Alarm ein, schaltet das System sofort auf die Alarmmaske und aktiviert die Hupe.
4.  Erst wenn der Alarm-Sensor (`I3`) wieder FALSE ist **UND** der Nutzer den Quittier-Taster (`I4`) drückt, wird der Speicher zurückgesetzt und die Navigation wieder freigegeben.

-----

## Anwendungsbeispiel

**Zwingende Störungsbehebung**:
Bei einem kritischen Hardware-Fehler (z.B. Not-Aus betätigt) darf der Bediener das Terminal nicht weiter zur normalen Maschinensteuerung nutzen. Er wird auf der Alarmseite "festgehalten", bis der Not-Aus entriegelt und die Störung quittiert wurde. Dies erzwingt die Aufmerksamkeit für das vorrangige Sicherheitsproblem.