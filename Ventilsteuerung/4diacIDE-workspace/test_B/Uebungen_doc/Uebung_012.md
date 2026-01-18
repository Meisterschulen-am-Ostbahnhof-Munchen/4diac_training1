# Uebung_012: Daten dauerhaft speichern (NVS)

```{index} single: Uebung_012: Daten dauerhaft speichern (NVS)
```

[Uebung_012](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_012.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_012`. Hier wird gezeigt, wie numerische Werte nicht nur angezeigt, sondern auch stromausfallsicher in der Steuerung (NVS - Non Volatile Storage) gespeichert werden.


## 📺 Video

* [Zusätzlich: Uebung_083: Aufwärts/Abwärts zählen: E_CTUD_UDINT Datentyp UDINT; mit Anzeige am VT.](https://www.youtube.com/watch?v=oTPDtsw5eAw)
* ["Store Version" – Dein Schlüssel zur Verwaltung von Objektdatenpools im nichtflüchtigen VT-Speich...](https://www.youtube.com/watch?v=eVseHOOO9qM)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)

## Podcast
* [Datenkommunikation in der Automatisierung: Die Geheimnisse der IEC 61499 Datentypen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Datenkommunikation-in-der-Automatisierung-Die-Geheimnisse-der-IEC-61499-Datentypen-e3672lj)
* [Datentypen der IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Datentypen-der-IEC-61499-e3672jf)
* [Der E_T_FF_SR-Baustein: Herzstück der IEC 61499 – Speichern, Umschalten, Reagieren](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_T_FF_SR-Baustein-Herzstck-der-IEC-61499--Speichern--Umschalten--Reagieren-e3682dm)
* [IEC 61499: Revolution der Automatisierung – Ereignisgesteuerte Systeme und intelligente Datenflüsse entschlüsselt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Revolution-der-Automatisierung--Ereignisgesteuerte-Systeme-und-intelligente-Datenflsse-entschlsselt-e375ghe)
* [SINT, INT, DINT: Warum die Wahl des Datentyps über Effizienz und Fehler entscheidet](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/SINT--INT--DINT-Warum-die-Wahl-des-Datentyps-ber-Effizienz-und-Fehler-entscheidet-e3673b8)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_012.png)


## Ziel der Übung

Erlernen der persistenten Datenspeicherung. Es wird demonstriert, wie ein am Terminal eingegebener Wert im internen Flash-Speicher der Steuerung abgelegt und beim Neustart automatisch wieder geladen und angezeigt wird.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_012.SUB` verbindet Eingabe, Speicherung und Anzeige zu einem geschlossenen Kreislauf[cite: 1].

### Funktionsbausteine (FBs)

  * **`InputNumber_I1`**: Numerisches Eingabefeld am Terminal.
  * **`NVS`**: Typ `logiBUS::storage::esp32_nvs::NVS`. [cite_start]Dieser Baustein verwaltet den Zugriff auf den nicht-flüchtigen Speicher. Er speichert Werte unter einem eindeutigen `KEY` ab[cite: 1].
  * **`CbVtStatus`**: Ein Statusbaustein des Terminals. [cite_start]Er feuert ein Ereignis (`IND`), wenn das Terminal neu startet oder die Verbindung wiederhergestellt wird[cite: 1].
  * **`Q_NumericValue`**: Die numerische Anzeige am Terminal.

-----

## Funktionsweise

Der Prozess deckt drei Szenarien ab:

1.  **Speichern**: Gibt der Nutzer einen Wert ein (`IND`), wird dieser konvertiert und per `NVS.SET` dauerhaft gespeichert.
2.  **Laden beim Start**: Nach dem Booten sendet der Speicherbaustein ein `INITO`-Event, welches sofort einen Lese-Vorgang (`GET`) auslöst. Der gespeicherte Wert wird geladen und an die Anzeige gesendet.
3.  **Refresh bei Verbindung**: Falls das Terminal während des Betriebs kurzzeitig getrennt wird, sorgt `CbVtStatus.IND` dafür, dass der aktuelle Wert erneut an das Terminal gesendet wird, sobald es wieder online ist.

-----

## Anwendungsbeispiel

**Konfigurations-Parameter**:
Ein Landwirt stellt die Arbeitsbreite seines Gerätes einmalig am Terminal ein. Dank NVS-Speicherung muss er diesen Wert nicht bei jedem morgendlichen Start der Maschine neu eingeben; die Steuerung "erinnert" sich an die letzte Einstellung.