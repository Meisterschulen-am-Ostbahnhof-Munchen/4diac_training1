# Uebung_008_AX: Autonomer Blinker-Baustein

```{index} single: Uebung_008_AX: Autonomer Blinker-Baustein
```

[Uebung_008_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_008_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_008_AX`.


## 📺 Video

* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)
* [Aufwärts/Abwärts zählen Baustein E_CTUD aus der IEC 61499 (Übung 82)](https://www.youtube.com/watch?v=H_MRtaMiaU8)
* [Herunterzählen Baustein E_CTD aus der IEC 61499 (Übung 81)](https://www.youtube.com/watch?v=NgLWcVhgRqk)
* [RS-Flip-Flop Baustein E_RS aus der IEC 61499 (Übung 006b)](https://www.youtube.com/watch?v=GXOe8K7Jgr0)
* [SR-Flip-Flop Baustein E_SR aus der IEC 61499 (Übung 006)](https://www.youtube.com/watch?v=6nGmGX7gwAE)

## Podcast
* [Der E_CTU-Baustein: Ereignisgesteuertes Hochzählen in der Industrie nach IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_CTU-Baustein-Ereignisgesteuertes-Hochzhlen-in-der-Industrie-nach-IEC-61499-e36846t)
* [Der E_PERMIT-Baustein: Der "Türsteher" für Ereignisse in IEC 61499-Systemen entschlüsselt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_PERMIT-Baustein-Der-Trsteher-fr-Ereignisse-in-IEC-61499-Systemen-entschlsselt-e3681m5)
* [Der E_T_FF_SR-Baustein: Herzstück der IEC 61499 – Speichern, Umschalten, Reagieren](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_T_FF_SR-Baustein-Herzstck-der-IEC-61499--Speichern--Umschalten--Reagieren-e3682dm)
* [DIN EN 61499-1 Entmystifiziert: Funktionsbausteine, Objektorientierung und verteilte Systeme](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Entmystifiziert-Funktionsbausteine--Objektorientierung-und-verteilte-Systeme-e37229b)
* [DIN EN 61499-1: Bauklötze für die Industrie 4.0 – So revolutionieren Funktionsbausteine die Automatisierung](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Baukltze-fr-die-Industrie-4-0--So-revolutionieren-Funktionsbausteine-die-Automatisierung-e3681j7)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_008_AX.png)


## Ziel der Übung

Implementierung eines dauerhaft laufenden Blinkers als Basis-Baustein.

-----

## Beschreibung und Komponenten

## Beschreibung und Komponenten

Die Subapplikation `Uebung_008_AX.SUB` ist eine Variante, die den `AX_AE_MERGE` Baustein nutzt, um die Ereignisse korrekt zusammenzuführen.

Der `AE_CYCLE` läuft dauerhaft (oder wird einmalig initialisiert). Der `AX_AE_MERGE` führt das Taktsignal (`AE_CYCLE.EO`) mit dem Rückkopplungssignal (`AX_SR.Q`) zusammen. Die Logik mit `E_SWITCH` und `AX_SR` sorgt für das Toggeln. Da keine externen Eingriffe vorgesehen sind, blinkt dieser Ausgang permanent, solange die Steuerung läuft.

-----

## Anwendungsbeispiel

**Lebenszeichen (Heartbeat)**: Eine LED, die auf der Platine oder am Schaltschrank blinkt, um anzuzeigen: "Die CPU lebt noch und das Programm läuft".