# Uebung_006: Speicherglied (SR-Flip-Flop)

```{index} single: Uebung_006: Speicherglied (SR-Flip-Flop)
```

[Uebung_006](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006`. Hier wird ein klassischer Selbsthaltespeicher mit getrennten Tastern für Ein und Aus implementiert.

## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [RS-Flip-Flop Baustein E_RS aus der IEC 61499 (Übung 006b)](https://www.youtube.com/watch?v=GXOe8K7Jgr0)
* [SR&T-Flip-Flop Übung 006a](https://www.youtube.com/watch?v=lfumU4WoIGs)
* [SR-Flip-Flop Baustein E_SR aus der IEC 61499 (Übung 006)](https://www.youtube.com/watch?v=6nGmGX7gwAE)

----

![](Uebung_006.png)

## Ziel der Übung

Realisierung einer Schaltung mit getrennter Setz- und Rücksetz-Logik unter Verwendung von Ereignis-Bausteinen.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006.SUB` nutzt zwei ereignisbasierte Eingänge und einen SR-Speicher[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` (Set)**: Taster zum Einschalten (konfiguriert auf Einzelklick).
  * **`I2` (Reset)**: Taster zum Ausschalten (konfiguriert auf Einzelklick).
  * **`E_SR`**: Ein ereignisbasierter Speicherbaustein. [cite_start]Ein Event am Eingang `S` (Set) setzt den Ausgang `Q` auf TRUE, ein Event am Eingang `R` (Reset) setzt ihn auf FALSE[cite: 1].

-----

## Funktionsweise

```xml
<EventConnections>
    <Connection Source="DigitalInput_CLK_I1.IND" Destination="E_SR.S"/>
    <Connection Source="DigitalInput_CLK_I2.IND" Destination="E_SR.R"/>
    <Connection Source="E_SR.EO" Destination="DigitalOutput_Q1.REQ"/>
</EventConnections>
```

[cite_start][cite: 1]

*   Ein Klick auf Taster 1 ➡️ Speicher wird gesetzt ➡️ Lampe geht an.
*   Ein Klick auf Taster 2 ➡️ Speicher wird gelöscht ➡️ Lampe geht aus.
*   Erneutes Drücken von Taster 1, wenn das Licht bereits an ist, hat keine Auswirkung.

-----

## Anwendungsbeispiel

**Industrielle Start/Stopp-Steuerung**: Ein grüner Taster startet eine Maschine, ein roter Taster stoppt sie. Dies ist sicherer als ein einzelner Toggle-Taster, da der Bediener immer einen definierten Befehl ("Ich will aus") geben kann, unabhängig vom aktuellen Zustand.