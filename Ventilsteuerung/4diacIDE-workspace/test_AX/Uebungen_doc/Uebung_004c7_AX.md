# Uebung_004c7_AX: Parametrierter Langer Druck

```{index} single: Uebung_004c7_AX: Parametrierter Langer Druck
```

[Uebung_004c7_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004c7_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004c7_AX`. Auch hier wird `logiBUS_IE2` genutzt, um die Zeitdauer für einen "langen Druck" anzupassen.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Das Kleingedruckte der Würth Klemmleiste entschlüsselt!](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Das-Kleingedruckte-der-Wrth-Klemmleiste-entschlsselt-e3aujai)
* [Druckbegrenzungsventile: Lebensversicherung der Hydraulik – Arten, Funktion und Systemintegration](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Druckbegrenzungsventile-Lebensversicherung-der-Hydraulik--Arten--Funktion-und-Systemintegration-e373nal)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004c7_AX.png)


## Ziel der Übung

Definition einer spezifischen Haltezeit.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004c7_AX.SUB` nutzt `logiBUS_IE2` mit `InputEvent = BUTTON_LONG_PRESS_START` und `arg = 3000` (ms)[cite: 1].

-----

## Funktionsweise

Das Event feuert erst, wenn der Taster für **3 Sekunden** (3000ms) gedrückt gehalten wird. Dies überschreibt den Standardwert (der meist bei 500ms oder 1s liegt).

-----

## Anwendungsbeispiel

**Werkseinstellungen laden**: Eine sehr destruktive Aktion, die extrem gut gegen versehentliches Auslösen geschützt sein muss. Der Nutzer muss bewusst lange drücken.