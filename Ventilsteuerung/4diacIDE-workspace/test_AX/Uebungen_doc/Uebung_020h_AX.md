# Uebung_020h_AX: Ereignisgesteuerter Impuls (AX_PULSE)

```{index} single: Uebung_020h_AX: Ereignisgesteuerter Impuls (AX_PULSE)
```

[Uebung_020h_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020h_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020h_AX`. Hier wird der Baustein `AX_PULSE` verwendet, der im Gegensatz zum `AX_TP` rein ereignisbasiert arbeitet.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [E_CTD: Ereignisgesteuerter Abwärtszähler nach IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_CTD-Ereignisgesteuerter-Abwrtszhler-nach-IEC-61499-e368lli)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_020h_AX.png)


## Ziel der Übung

Das Ziel ist es, ein einzelnes, kurzes Ereignis (z.B. einen Mausklick oder Taster-Impuls) in eine länger anhaltende Aktion zu verwandeln. Der Fokus liegt hierbei auf der rein ereignisorientierten Schnittstelle des Bausteins.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_020h_AX.SUB` kombiniert einen Event-Eingang mit einem Adapter-Puls-Baustein[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1`**: Typ `logiBUS_IE`. Liefert ein Ereignis bei einem Einfachklick (`BUTTON_SINGLE_CLICK`).
  * **`AX_PULSE`**: [cite_start]Startet einen Timer bei Eintreffen eines Ereignisses am `REQ`-Eingang. Der Ausgang `Q` bleibt für die Zeit `PT` (5 Sekunden) auf TRUE[cite: 1].
  * **`DigitalOutput_Q1`**: Typ `logiBUS_QXA`.

-----

## Funktionsweise

1.  **Ereignis**: Der Nutzer klickt kurz auf den Taster `I1`.
2.  **Trigger**: Der Eingangsbaustein sendet ein `IND`-Event an den `REQ`-Eingang von `AX_PULSE`.
3.  **Aktion**: Der Timer startet sofort. Der Adapter-Ausgang `Q` wird `TRUE` und schaltet die Lampe `Q1` ein.
4.  **Autarkie**: Da der Baustein ereignisbasiert ist, muss der Eingang nicht gehalten werden. Er "merkt" sich den Startimpuls.
5.  **Ende**: Nach 5 Sekunden schaltet der Ausgang automatisch wieder auf `FALSE`.

-----

## Anwendungsbeispiel

**Türöffner**: Ein kurzer Tastendruck an der Gegensprechanlage löst einen elektrischen Türöffner für genau 5 Sekunden aus, damit der Besucher eintreten kann.