# Uebung_019b: Alarm-Logik mit Hardware-Ausgang

```{index} single: Uebung_019b: Alarm-Logik mit Hardware-Ausgang
```

[Uebung_019b](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_019b.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_019b`. Hier wird der virtuelle Alarm am Terminal mit einem physischen Alarm-Ausgang synchronisiert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Automatisierung 4.0: Warum Software die Hardware überholt und was das für deine Skills bedeutet](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Automatisierung-4-0-Warum-Software-die-Hardware-berholt-und-was-das-fr-deine-Skills-bedeutet-e375eqs)
* [SPS: Das Unsichtbare Gehirn der Industrie – Von robuster Hardware zur IT/OT-Konvergenz](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/SPS-Das-Unsichtbare-Gehirn-der-Industrie--Von-robuster-Hardware-zur-ITOT-Konvergenz-e375g1f)
* [Universal Automation: So entkoppeln Sie Software und Hardware für die Zukunft der Industrie](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Universal-Automation-So-entkoppeln-Sie-Software-und-Hardware-fr-die-Zukunft-der-Industrie-e36849a)
* [Das Alarm Mask Objekt: Dein standardisierter Wachposten für Warnungen auf Landmaschinen](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/Das-Alarm-Mask-Objekt-Dein-standardisierter-Wachposten-fr-Warnungen-auf-Landmaschinen-e36e6c3)
* [Schalterlogik verstehen: So funktioniert ein Toggle Flip-Flop mit logiBUS® – einfache Steuerung in der Landtechnik](https://podcasters.spotify.com/pod/show/logibus/episodes/Schalterlogik-verstehen-So-funktioniert-ein-Toggle-Flip-Flop-mit-logiBUS--einfache-Steuerung-in-der-Landtechnik-e36vjo1)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_019b.png)


## Ziel der Übung

Verknüpfung von UI-Zuständen mit Hardware-Speichern. Es soll sichergestellt werden, dass ein Alarmzustand in der Steuerung erhalten bleibt, bis er am Terminal gelöscht wird.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_019b.SUB` wird zusätzlich zur Maskenumschaltung ein SR-Flip-Flop für den Alarm-Status verwendet[cite: 1].

### Funktionsbausteine (FBs)

  * **`E_SR`**: Der Alarm-Speicher.
  * **`Alarmausgang`**: Schaltet eine physische Hupe oder Warnlampe (`Q1`).

-----

## Funktionsweise

*   **Alarm auslösen**: Taster `I3` triggert den Alarm. Das Terminal springt auf die Alarmmaske **UND** der Speicher `E_SR` wird gesetzt ➡️ Die physische Hupe geht an.
*   **Quittieren**: Der Nutzer drückt **ACK** am Terminal. Die Steuerung wechselt zurück zur normalen Maske **UND** löscht den Speicher `E_SR.R` ➡️ Die Hupe verstummt.
*   Interessant: Auch das Wechseln zu einer anderen normalen Maske (`I1`, `I2`) löscht in dieser Implementierung den Alarm-Speicher (Reset-Zweig am `E_SR`).

-----

## Anwendungsbeispiel

**Zentrale Störmelde-Zentrale**:
Ein kritischer Fehler (z.B. Öldruckverlust) löst sowohl die Anzeige am Bildschirm als auch eine externe Sirene aus. Der Techniker muss zum Terminal gehen, um zu sehen, was los ist, und durch die Quittierung sowohl das Display aufräumen als auch den Lärm abstellen.