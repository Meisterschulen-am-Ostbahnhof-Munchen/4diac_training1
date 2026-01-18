# Uebung_025: Synchronisierte Sequenz (Rendezvous)

```{index} single: Uebung_025: Synchronisierte Sequenz (Rendezvous)
```

[Uebung_025](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_025.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_025`. Hier wird die Ablaufsteuerung durch Rendezvous-Bausteine abgesichert.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_025.png)


## Ziel der Übung

Verwendung von `E_REND` zur Absicherung von Übergängen. Es soll sichergestellt werden, dass ein Folgeschritt nur dann ausgelöst wird, wenn sowohl das Hardware-Feedback (Endlage) als auch das logische Software-Event (Bereitschaft) vorliegen.

-----

## Funktionsweise

[cite_start]Die Übung nutzt für jeden Übergang einen `E_REND` Baustein[cite: 1].
Zusätzlich werden `E_SWITCH` Bausteine zur Plausibilitätsprüfung eingesetzt. Ein Ereignis wird nur dann als gültige Endlage akzeptiert, wenn der zugehörige Ausgang (`Q`) der Steuerung zu diesem Zeitpunkt auch tatsächlich aktiv ist (Rückkopplung der Daten an das Gate der Weiche). Dies verhindert Fehlsteuerungen durch defekte oder hängende Sensoren.
