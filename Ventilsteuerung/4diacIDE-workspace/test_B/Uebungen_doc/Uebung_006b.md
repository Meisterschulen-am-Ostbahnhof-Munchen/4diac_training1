# Uebung_006b: Speicherglied (RS-Flip-Flop)

```{index} single: Uebung_006b: Speicherglied (RS-Flip-Flop)
```

[Uebung_006b](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006b.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006b`.

----

![](Uebung_006b.png)

## Ziel der Übung

Verständnis der Reset-Priorität.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006b.SUB` nutzt einen `E_RS` Baustein[cite: 1].

### Funktionsbausteine (FBs)

  * **`E_RS`**: Ein ereignisbasiertes RS-Flip-Flop (Reset dominant).

-----

## Funktionsweise

Funktional sehr ähnlich zum SR-Speicher (Übung 006). Der entscheidende Unterschied liegt im Verhalten bei "Gleichzeitigkeit": Sollten im exakt gleichen Moment sowohl ein Setz- als auch ein Rücksetz-Ereignis eintreffen, gewinnt beim `E_RS` das **Rücksetzen**. Der Ausgang wird also sicher auf `FALSE` geschaltet.

-----

## Anwendungsbeispiel

**Gefahrenabschaltung**: Bei einer Maschine hat der Stopp-Befehl immer Vorrang. Wenn ein Fehlerzustand den Stopp auslöst, darf ein gleichzeitiger Startversuch des Bedieners die Abschaltung nicht verhindern. Hier ist ein RS-Glied zwingend erforderlich.