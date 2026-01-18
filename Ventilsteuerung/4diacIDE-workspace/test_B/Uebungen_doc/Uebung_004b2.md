# Uebung_004b2: Doppelte manuelle Toggle-Logik

```{index} single: Uebung_004b2: Doppelte manuelle Toggle-Logik
```

[Uebung_004b2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004b2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004b2`. Hier wird die manuelle Toggle-Logik aus Übung 004b auf zwei unabhängige Kanäle erweitert.


## 📺 Video

* [Schalterlogik verstehen: So funktioniert ein Toggle Flip-Flop mit logiBUS® – einfache Steuerung i...](https://www.youtube.com/watch?v=s7ZQ4tSk3f0)
* [Toggle-Flip-Flop Baustein E_T_FF aus der IEC 61499 (Übung 004a)](https://www.youtube.com/watch?v=XZqsqNy_g_g)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)

## Podcast
* [Schalterlogik verstehen: So funktioniert ein Toggle Flip-Flop mit logiBUS® – einfache Steuerung in der Landtechnik](https://podcasters.spotify.com/pod/show/logibus/episodes/Schalterlogik-verstehen-So-funktioniert-ein-Toggle-Flip-Flop-mit-logiBUS--einfache-Steuerung-in-der-Landtechnik-e36vjo1)
* [Unpacking E_T_FF_SR: The Secret Toggle Switch of Industrial Control Systems](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/Unpacking-E_T_FF_SR-The-Secret-Toggle-Switch-of-Industrial-Control-Systems-e367ntv)
* [Digitale Logik Flip-Flops und Datentypen](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Digitale-Logik-Flip-Flops-und-Datentypen-e3dic6t)
* [Wie simple Schalter "denken": Die Grundlagen der Digitaltechnik – Gatter, Logik und die Macht von 1 und 0](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Wie-simple-Schalter-denken-Die-Grundlagen-der-Digitaltechnik--Gatter--Logik-und-die-Macht-von-1-und-0-e3ae98g)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004b2.png)


## Ziel der Übung

Vertiefung des Verständnisses für parallele, rückgekoppelte Logikstrukturen. Jeder Kanal muss seinen eigenen Zustand korrekt verwalten, um unabhängig schaltbar zu sein.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_004b2.SUB` sind zwei identische Logik-Stränge (Switch + Speicher) nebeneinander aufgebaut[cite: 1].

### Funktionsbausteine (FBs)

  * **Kanal 1**: Taster `I1`, Weiche `E_SWITCH_I1`, Speicher `E_SR_I1`, Ausgang `Q1`.
  * **Kanal 2**: Taster `I2`, Weiche `E_SWITCH_I2`, Speicher `E_SR_I2`, Ausgang `Q2`.

-----

## Funktionsweise

Die beiden Kanäle arbeiten nach dem gleichen Prinzip wie in Übung 004b: Der Ausgangszustand (`Q`) steuert über den Gate-Eingang (`G`) der Weiche, ob der nächste Tastendruck ein Setz- oder Rücksetz-Ereignis auslöst.

```xml
<!-- Beispiel Kanal 1 -->
<Connection Source="DigitalInput_CLK_I1.IND" Destination="E_SWITCH_I1.EI"/>
<Connection Source="E_SWITCH_I1.EO0" Destination="E_SR_I1.S"/>
<Connection Source="E_SWITCH_I1.EO1" Destination="E_SR_I1.R"/>
<Connection Source="E_SR_I1.Q" Destination="E_SWITCH_I1.G"/>
```

[cite_start][cite: 1]

Da keine Querverbindungen zwischen den Strängen existieren, beeinflusst die Bedienung von Taster 1 niemals den Zustand von Lampe 2 und umgekehrt.