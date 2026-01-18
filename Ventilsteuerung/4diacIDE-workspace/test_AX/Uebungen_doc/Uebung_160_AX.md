# Uebung_160_AX: Motor-Logik mit Statusmeldung

```{index} single: Uebung_160_AX: Motor-Logik mit Statusmeldung
```

[Uebung_160_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_160_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_160_AX`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Eclipse 4diac: Innovationsmotor Forschung vs. Nutzerbedürfnisse – Was treibt die Entwicklung wirklich voran?](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/Eclipse-4diac-Innovationsmotor-Forschung-vs--Nutzerbedrfnisse--Was-treibt-die-Entwicklung-wirklich-voran-e38cke4)
* [Schalterlogik verstehen: So funktioniert ein Toggle Flip-Flop mit logiBUS® – einfache Steuerung in der Landtechnik](https://podcasters.spotify.com/pod/show/logibus/episodes/Schalterlogik-verstehen-So-funktioniert-ein-Toggle-Flip-Flop-mit-logiBUS--einfache-Steuerung-in-der-Landtechnik-e36vjo1)
* [Der Niedergang des Traktoren-Kults: Vom genialen Schwenkkammer-Motor zum teuren Ende der Motorenfabrik Anton Schlüter](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Der-Niedergang-des-Traktoren-Kults-Vom-genialen-Schwenkkammer-Motor-zum-teuren-Ende-der-Motorenfabrik-Anton-Schlter-e3aea7o)
* [Diesels radikale Vision: Warum der Erfinder alle Motoren seiner Zeit für „prinzipiell falsch“ hielt – Der Weg zum Dieselmotor](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Diesels-radikale-Vision-Warum-der-Erfinder-alle-Motoren-seiner-Zeit-fr-prinzipiell-falsch-hielt--Der-Weg-zum-Dieselmotor-e399mvg)
* [Digitale Logik Flip-Flops und Datentypen](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Digitale-Logik-Flip-Flops-und-Datentypen-e3dic6t)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_160_AX.png)


## Ziel der Übung

Kombination von Einzelausgängen und einer Sammelmeldung.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_160_AX.SUB` steuert zwei Drehrichtungen und einen gemeinsamen Status-Ausgang[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1`**: Taster für Links (`Q5`).
  * **`I2`**: Taster für Rechts (`Q6`).
  * **`AX_OR_2`**: Verknüpft beide Signale.
  * **`Q56`**: Ein dritter Ausgang.

-----

## Funktionsweise

1.  Drückt man `I1`, geht `Q5` an.
2.  Drückt man `I2`, geht `Q6` an.
3.  Der Baustein `AX_OR_2` sorgt dafür, dass `Q56` immer dann an ist, wenn **entweder** `Q5` **oder** `Q6` (oder beide) aktiv sind.

-----

## Anwendungsbeispiel

**Hauptschütz-Ansteuerung**: In einer Motorsteuerung sind `Q5` und `Q6` die Richtungsschütze. `Q56` steuert das Hauptschütz an, das in beiden Fällen angezogen sein muss, um den Leistungsteil mit Strom zu versorgen.