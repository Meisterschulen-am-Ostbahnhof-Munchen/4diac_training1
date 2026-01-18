# Uebung_004b3: Gegenseitig verriegelte Toggle-Logik

```{index} single: Uebung_004b3: Gegenseitig verriegelte Toggle-Logik
```

[Uebung_004b3](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004b3.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004b3`. Diese Übung erweitert das zweikanalige System um eine gegenseitige Verriegelung: Es kann immer nur maximal eine Lampe gleichzeitig leuchten.


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



![](Uebung_004b3.png)


## Ziel der Übung

Implementierung einer exklusiven Auswahl-Logik. Das Einschalten eines Kanals muss zwangsläufig das Ausschalten des anderen Kanals zur Folge haben. Dies ist eine Standardanforderung bei der Auswahl von Betriebsmodi oder Fahrtrichtungen.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004b3.SUB` basiert auf dem Aufbau von 004b2, führt jedoch zusätzliche Ereignisverbindungen zur Verriegelung ein[cite: 1].

### Funktionsbausteine (FBs)

  * Identisch zu 004b2: Taster `I1`/`I2`, Weichen `E_SWITCH_I1`/`I2`, Speicher `E_SR_I1`/`I2`.

-----

## Funktionsweise

Die Besonderheit liegt in der "Über-Kreuz-Verbindung" der Setz-Ereignisse:

```xml
<EventConnections>
    <!-- Normale Toggle-Logik Kanal 1 -->
    <Connection Source="E_SWITCH_I1.EO0" Destination="E_SR_I1.S"/>
    <Connection Source="E_SWITCH_I1.EO1" Destination="E_SR_I1.R"/>
    
    <!-- Verriegelung: Wenn Kanal 1 einschaltet (EO0), schalte Kanal 2 aus! -->
    <Connection Source="E_SWITCH_I1.EO0" Destination="E_SR_I2.R"/>
    
    <!-- Verriegelung: Wenn Kanal 2 einschaltet (EO0), schalte Kanal 1 aus! -->
    <Connection Source="E_SWITCH_I2.EO0" Destination="E_SR_I1.R"/>
</EventConnections>
```

[cite_start][cite: 1]

Der funktionale Ablauf:
1.  Lampe 1 ist an, Lampe 2 ist aus.
2.  Nutzer drückt Taster 2 (`I2`).
3.  Die Weiche von Kanal 2 erkennt "Lampe 2 ist aus" und feuert das Ereignis zum Einschalten (`EO0`).
4.  Dieses Ereignis geht einerseits an den Speicher von Kanal 2 (`Setzen`) ➡️ Lampe 2 geht an.
5.  Gleichzeitig geht das selbe Ereignis an den Reset-Eingang von Kanal 1 ➡️ Lampe 1 geht sofort aus.

Ergebnis: Durch das Einschalten einer Funktion wird die andere automatisch deaktiviert.

-----

## Anwendungsbeispiel

**Betriebsarten-Wahl**: Eine Anlage kann entweder im Modus "Automatik" (`Q1`) oder im Modus "Handbetrieb" (`Q2`) laufen. Sobald der Bediener auf Handbetrieb umschaltet, muss die Automatik aus Sicherheitsgründen sofort gestoppt werden.