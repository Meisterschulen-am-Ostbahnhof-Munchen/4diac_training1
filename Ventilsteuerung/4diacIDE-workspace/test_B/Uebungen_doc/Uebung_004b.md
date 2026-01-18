# Uebung_004b: Manueller Stromstoßschalter (Switch & Speicher)

```{index} single: Uebung_004b: Manueller Stromstoßschalter (Switch & Speicher)
```

[Uebung_004b](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004b.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004b`. Hier wird gezeigt, wie die Funktion eines Toggle-Flip-Flops manuell aus Grundbausteinen (Weiche und Speicher) aufgebaut werden kann.


## 📺 Video

* [Ereignisschalter E_SWITCH aus der IEC 61499 (Übung 86)](https://www.youtube.com/watch?v=Gev-kGR4-Tc)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [Der E_T_FF_SR-Baustein: Herzstück der IEC 61499 – Speichern, Umschalten, Reagieren](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_T_FF_SR-Baustein-Herzstck-der-IEC-61499--Speichern--Umschalten--Reagieren-e3682dm)
* [E_SWITCH: Die Weiche der Automatisierung – Warum Einfachheit IEC 61499 revolutioniert](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_SWITCH-Die-Weiche-der-Automatisierung--Warum-Einfachheit-IEC-61499-revolutioniert-e3681fl)
* [E_SWITCH: The Unsung Hero of Industrial Automation's Modular Design](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/E_SWITCH-The-Unsung-Hero-of-Industrial-Automations-Modular-Design-e367npq)
* [Unpacking E_T_FF_SR: The Secret Toggle Switch of Industrial Control Systems](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/Unpacking-E_T_FF_SR-The-Secret-Toggle-Switch-of-Industrial-Control-Systems-e367ntv)
* ["Store Version" – Dein Schlüssel zur Verwaltung von Objektdatenpools im nichtflüchtigen VT-Speicher (ISO 11783-6)](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/Store-Version--Dein-Schlssel-zur-Verwaltung-von-Objektdatenpools-im-nichtflchtigen-VT-Speicher-ISO-11783-6-e36vfh0)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004b.png)


## Ziel der Übung

Verständnis der inneren Logik eines Speicherbausteins. Anstatt den fertigen `E_T_FF` Baustein zu nutzen, wird hier eine Rückkopplungsschleife konstruiert, die den aktuellen Zustand nutzt, um das nächste Ereignis an den richtigen Eingang (`Setzen` oder `Rücksetzen`) zu leiten.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004b.SUB` realisiert die Toggle-Funktion durch die Kombination einer Ereignis-Weiche und eines SR-Speichers[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1`**: Liefert ein Ereignis bei jedem Tastendruck.
  * **`E_SWITCH`**: Eine Ereignis-Weiche. [cite_start]Je nach Zustand am Dateneingang `G` leitet sie das Ereignis `EI` entweder an `EO0` (wenn FALSE) oder an `EO1` (wenn TRUE) weiter[cite: 1].
  * **`E_SR`**: Ein ereignisbasierter SR-Speicher (Set/Reset).
  * **`DigitalOutput_Q1`**: Der Hardware-Ausgang.

-----

## Funktionsweise

Der Schlüssel liegt in der Rückführung des Ausgangszustands zum Eingang der Weiche:

```xml
<EventConnections>
    <Connection Source="DigitalInput_CLK_I1.IND" Destination="E_SWITCH.EI"/>
    <Connection Source="E_SWITCH.EO0" Destination="E_SR.S"/>
    <Connection Source="E_SWITCH.EO1" Destination="E_SR.R"/>
    <Connection Source="E_SR.EO" Destination="DigitalOutput_Q1.REQ"/>
</EventConnections>
<DataConnections>
    <Connection Source="E_SR.Q" Destination="DigitalOutput_Q1.OUT"/>
    <Connection Source="E_SR.Q" Destination="E_SWITCH.G"/>
</DataConnections>
```

[cite_start][cite: 1]

Der funktionale Ablauf:
1.  **Zustand AUS**: `E_SR.Q` ist FALSE, damit ist auch `E_SWITCH.G` auf FALSE.
2.  Ein Tastendruck feuert `EI`. Die Weiche leitet es an `EO0` ➡️ `E_SR.S`. Der Speicher wird gesetzt, die Lampe geht an.
3.  **Zustand AN**: Da die Lampe nun an ist, liegt an `E_SWITCH.G` eine TRUE an.
4.  Der nächste Tastendruck feuert wieder `EI`. Diesmal leitet die Weiche das Event an `EO1` ➡️ `E_SR.R`. Der Speicher wird zurückgesetzt, die Lampe geht aus.

-----

## Bewertung

Dieser Aufbau ist lehrreich, um die Konzepte von Ereignissteuerung und Datenrückkopplung zu verstehen. In realen Projekten sollte jedoch immer der spezialisierte Baustein `E_T_FF` bevorzugt werden, da dieser übersichtlicher ist und weniger Ressourcen verbraucht.