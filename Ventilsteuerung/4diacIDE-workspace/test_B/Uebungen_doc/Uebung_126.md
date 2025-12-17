Hier ist die Dokumentation für die Übung 126, basierend auf den bereitgestellten XML-Daten.

# Uebung_126

![Uebung_126](Uebung_126.png)

* * * * * * * * * *

## Einleitung
Diese Übung behandelt das zyklische Senden von ISOBUS-Nachrichten unter Verwendung eines Callback-Mechanismus (`CB`). Der Fokus liegt auf der Initialisierung einer Übertragung, sobald ein Netzwerkteilnehmer erkannt wird, und der Bereitstellung der Nutzdaten über eine Adapterverbindung aus einer Sub-Applikation.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung werden folgende Hauptkomponenten verwendet:

*   **NmGetCfInfo** (`isobus::pgn::NmGetCfInfo`): Dient der Überwachung des ISOBUS-Netzwerks auf spezifische Teilnehmer (Control Functions).
*   **STRUCT_DEMUX** (`eclipse4diac::convert::STRUCT_DEMUX`): Wird mehrfach verwendet, um komplexe strukturierte Datentypen (`NAMEFIELD_T`, `CF_INFO_T`, `ISONETEVENT_T`) in ihre Einzelteile zu zerlegen.
*   **AlPgnTxNew8Bcycl_REQ** (`isobus::pgn::tx::AlPgnTxNew8Bcycl_REQ`): Ein Baustein zum zyklischen Senden einer neuen 8-Byte PGN-Nachricht. Er verfügt über einen `CB` (Callback) Eingang für Adapter.
*   **DataSupply** (`Uebungen::Uebung_12x_sub`): Eine Sub-Applikation, die als Datenquelle dient.

### Sub-Bausteine: DataSupply

*   **Typ**: `Uebungen::Uebung_12x_sub`
*   **Verwendete interne FBs**:
    *   *Hinweis: Die internen Details dieser Sub-Applikation sind in den bereitgestellten Daten nicht enthalten. Basierend auf der Verschaltung dient sie der Datenerzeugung.*
*   **Funktionsweise**:
    *   Dieser Baustein stellt über den Adapter-Ausgang `PLUG1` die notwendige Logik oder Daten bereit, die vom Sendebaustein benötigt werden. Er fungiert als "Data Supply" (Datenversorgung) für den zyklischen Sender.

## Programmablauf und Verbindungen

Der Ablauf der Übung wird durch das Netzwerkmanagement gesteuert:

1.  **Netzwerkerkennung**:
    Der Baustein `NmGetCfInfo_1` überwacht den Bus auf dem Kanal `NODE1`. Er filtert nach einer spezifischen Adresse (`PEAK_ADD`) und Maske (`PEAK_FLT`).

2.  **Informationsverarbeitung**:
    Sobald der `NmGetCfInfo_1` ein Ereignis (`IND`) auslöst, werden die empfangenen Strukturdaten (`sNameField`, `sCfInfo`, `sNetEv`) an drei verschiedene `STRUCT_DEMUX` Bausteine weitergeleitet. Dies dient der Aufschlüsselung und Analyse der Netzwerkteilnehmer-Informationen.

3.  **Installation der Übertragung**:
    Das `IND`-Ereignis triggert gleichzeitig den Eingang `install` des Bausteins `AlPgnTxNew8Bcycl_REQ`. Damit wird der Sendevorgang eingerichtet.
    *   **Parameter**:
        *   `u32Pgn` = 61184 (Die zu sendende Parameter Group Number).
        *   `u16DaSize` = 8 (Datenlänge: 8 Byte).
        *   `u8Priority` = 3 (Priorität der Nachricht).
        *   `u16DefRepRate` = 500 (Wiederholrate: 500 ms).

4.  **Datenbereitstellung via Callback**:
    Im Gegensatz zu statischen Dateneingängen nutzt der Sendebaustein `AlPgnTxNew8Bcycl_REQ` einen Adapter-Eingang `CB` (Callback). Dieser ist mit dem Adapter `PLUG1` der Sub-Applikation `DataSupply` verbunden. Das bedeutet, dass die `DataSupply`-Sub-Applikation alle 500 ms (entsprechend der `DefRepRate`) die aktuellen Nutzdaten für die Nachricht bereitstellt.

## Zusammenfassung
Die Übung 126 demonstriert, wie man eine zyklische ISOBUS-Nachricht (PGN 61184) konfiguriert, die automatisch startet, sobald ein relevanter Netzwerkteilnehmer erkannt wird. Eine Besonderheit ist die Trennung von Sendekonfiguration und Datenerzeugung: Während `AlPgnTxNew8Bcycl_REQ` das Timing und Protokoll übernimmt, werden die eigentlichen Nutzdaten dynamisch über eine Adapter-Verbindung aus der `DataSupply` Sub-Applikation bezogen.