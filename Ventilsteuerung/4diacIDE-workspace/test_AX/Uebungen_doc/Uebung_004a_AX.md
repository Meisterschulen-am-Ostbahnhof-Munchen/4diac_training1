# Uebung_004a_AX: Stromstoßschalter (Toggle Flip-Flop)

```{index} single: Uebung_004a_AX: Stromstoßschalter (Toggle Flip-Flop)
```

[Uebung_004a_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004a_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004a_AX`. In dieser Übung verlassen wir die reine Datenweiterleitung und nutzen Ereignisse (Events), um eine Speicherfunktion zu realisieren: einen klassischen Stromstoßschalter.


## 📺 Video

* [Toggle-Flip-Flop Baustein E_T_FF aus der IEC 61499 (Übung 004a)](https://www.youtube.com/watch?v=XZqsqNy_g_g)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [Unpacking E_T_FF_SR: The Secret Toggle Switch of Industrial Control Systems](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/Unpacking-E_T_FF_SR-The-Secret-Toggle-Switch-of-Industrial-Control-Systems-e367ntv)
* [Schalterlogik verstehen: So funktioniert ein Toggle Flip-Flop mit logiBUS® – einfache Steuerung in der Landtechnik](https://podcasters.spotify.com/pod/show/logibus/episodes/Schalterlogik-verstehen-So-funktioniert-ein-Toggle-Flip-Flop-mit-logiBUS--einfache-Steuerung-in-der-Landtechnik-e36vjo1)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004a_AX.png)


## Ziel der Übung

Das Ziel ist es, den Unterschied zwischen zustandsorientierter (Pegel) und ereignisorientierter (Flanke) Programmierung zu verstehen. Während ein einfacher Taster nur solange "Ein" ist, wie er gedrückt wird, soll hier jeder Tastendruck den Zustand des Ausgangs wechseln (Umschalten: Aus -> Ein -> Aus -> ...).

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004a_AX.SUB` verwendet einen speziellen Eingangsbaustein, der Klick-Ereignisse generiert, und ein Toggle-Flip-Flop[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1`**: Typ `logiBUS_IE` (Input Event). [cite_start]Im Gegensatz zum `IXA` (Input Extended Adapter) liefert dieser Baustein kein kontinuierliches `BOOL`-Signal, sondern feuert ein einzelnes Ereignis (`IND`), wenn eine bestimmte Bedingung erfüllt ist. Hier ist er auf `BUTTON_SINGLE_CLICK` konfiguriert[cite: 1].
  * **`E_T_FF`**: Typ `AX_T_FF` (Adapter Toggle Flip-Flop). [cite_start]Dieser Baustein hat einen Takteingang (`CLK`). Bei jedem empfangenen Ereignis wechselt er seinen internen Zustand und gibt diesen über den Adapter-Ausgang `Q` aus[cite: 1].
  * **`DigitalOutput_Q1`**: Typ `logiBUS_QXA`. [cite_start]Schaltet den physischen Ausgang `Q1` basierend auf dem Zustand des Flip-Flops[cite: 1].

-----

## Funktionsweise

1.  Der Benutzer drückt den Taster an `I1` kurz ("Klick").
2.  Der `DigitalInput_CLK_I1` erkennt das Muster "Einzelklick" und sendet ein `IND`-Ereignis.
3.  Das Ereignis erreicht den `CLK`-Eingang des `E_T_FF`.
4.  Das Flip-Flop kippt seinen Zustand (z.B. von FALSE auf TRUE).
5.  Der neue Zustand wird über den Adapter-Ausgang `Q` an `DigitalOutput_Q1` gesendet.
6.  Die Lampe an `Q1` geht an und bleibt an, auch wenn der Taster losgelassen wird.
7.  Beim nächsten Klick wiederholt sich der Vorgang, das Flip-Flop kippt zurück auf FALSE, die Lampe geht aus.

-----

## Anwendungsbeispiel

Die klassische **Flurbeleuchtung** oder **Treppenhauslicht** (ohne Zeitglied): Ein Tasterdruck schaltet das Licht ein, der nächste schaltet es wieder aus. Dies ist mit einem rein elektrischen Schalter (der zurückfedert) nicht möglich, man benötigt ein Speicherelement (Stromstoßrelais in der Elektrotechnik, Flip-Flop in der Software).