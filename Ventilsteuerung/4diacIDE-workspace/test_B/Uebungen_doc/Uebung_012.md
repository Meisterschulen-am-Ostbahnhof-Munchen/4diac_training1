# Uebung_012: Daten dauerhaft speichern (NVS)

```{index} single: Uebung_012: Daten dauerhaft speichern (NVS)
```

[Uebung_012](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_012.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_012`. Hier wird gezeigt, wie numerische Werte nicht nur angezeigt, sondern auch stromausfallsicher in der Steuerung (NVS - Non Volatile Storage) gespeichert werden.

## 📺 Video

* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [2025 11 15 12 35 11 Montage Hutschienenmoped logiBUS® -- Teil 3 -- Gehäuse](https://www.youtube.com/watch?v=MPm4vLmD5RE)
* [2025 11 15 12 52 26 Montage Hutschienenmoped logiBUS® -- Teil 4 -- Aufbauten](https://www.youtube.com/watch?v=WeowCxZW70Y)
* [2025-07-20 21-12-23  Fusion 360 Schematic SPICE Simulation deutsch](https://www.youtube.com/watch?v=jHT9nZIXxGU)
* [2025-11-04 16-12-16 LogiBUS® on the way to Eclipse 4diac™ 3.0 - Content Assist](https://www.youtube.com/watch?v=HXOzyEPKhrU)

## 🎧 Podcast

* [Amazon Pizza-Regel bis IKEA-Effekt: 12 verblüffend einfache Ideen hinter riesigem Geschäftserfolg](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Amazon-Pizza-Regel-bis-IKEA-Effekt-12-verblffend-einfache-Ideen-hinter-riesigem-Geschftserfolg-e39kmmc)

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