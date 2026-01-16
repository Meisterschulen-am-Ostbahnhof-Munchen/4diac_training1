# Uebung_020c3: Zyklische Timer-Aktualisierung (FB_TON)

[Uebung_020c3](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020c3.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020c3`. Hier wird gezeigt, wie man Timer-Bausteine nutzt, die dem klassischen SPS-Standard (IEC 61131-3) entsprechen.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020c3.png)


## Ziel der Übung

Verwendung von `FB_TON` (Function Block TON). Im Gegensatz zum ereignisbasierten `E_TON` benötigt dieser Baustein einen regelmäßigen Trigger (Abtastung), um seine interne Zeitrechnung und die Ausgänge zu aktualisieren.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_020c3.SUB` wird ein Taktgeber verwendet, um den klassischen Timer anzutreiben[cite: 1].

### Funktionsbausteine (FBs)

  * **`FB_TON`**: Der klassische TON-Baustein.
  * **`E_CYCLE`**: Ein Zeitgeber, der alle 500ms ein Ereignis an den `REQ`-Eingang des Timers sendet.

-----

## Funktionsweise

Damit der `FB_TON` korrekt funktioniert, muss er "befragt" werden.
1.  Der Nutzer drückt Taster `I1`. Das Signal liegt am Dateneingang `IN` des Timers an.
2.  Gleichzeitig startet der Taster über eine Weiche den `E_CYCLE`.
3.  Alle 500ms fordert der Cycle den Timer zur Berechnung auf (`REQ`).
4.  Erst bei diesen Abfragen prüft der Timer, wie viel Zeit vergangen ist.
5.  Sobald die 5 Sekunden erreicht sind, wechselt der Ausgang `Q` auf TRUE.

Diese Methode ist notwendig, wenn man Bausteine aus der 61131-Welt in die 61499-Event-Welt integriert.
