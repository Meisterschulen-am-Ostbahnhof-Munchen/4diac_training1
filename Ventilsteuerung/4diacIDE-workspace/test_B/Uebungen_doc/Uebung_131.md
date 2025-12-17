Hier ist die Dokumentation für die Übung `Uebung_131` basierend auf den bereitgestellten XML-Daten.

# Uebung_131

![Uebung_131 Übersicht](Uebung_131.png)

* * * * * * * * * *

## Einleitung
Die Übung `Uebung_131` behandelt den zyklischen Empfang von ISOBUS-Nachrichten. Der Fokus liegt darauf, zunächst über das Netzwerkmanagement Informationen über einen Teilnehmer zu erhalten und anschließend einen Empfänger für eine spezifische Parameter Group Number (PGN) zu installieren. Dabei werden komplexe Datentypen aufgeschlüsselt, um detaillierte Informationen über das Netzwerk und die empfangenen Daten bereitzustellen.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden spezifische ISOBUS-Bausteine sowie Konvertierungsbausteine verwendet, um die Datenkommunikation und -verarbeitung zu realisieren.

### Sub-Bausteine: NmGetCfInfo_1
Dieser Baustein ist für das Abrufen von Informationen über eine "Control Function" (CF) im ISOBUS-Netzwerk zuständig.

- **Typ**: `isobus::pgn::NmGetCfInfo`
- **Verwendete interne FBs**:
    - **NmGetCfInfo_1**: `isobus::pgn::NmGetCfInfo`
        - Parameter: `u8CanIdx` = `NODE1` (CAN-Knoten Index)
        - Parameter: `member` = `network`
        - Parameter: `address` = `PEAK_ADD` (Zieladresse, importierte Konstante)
        - Parameter: `mask` = `PEAK_FLT` (Filtermaske, importierte Konstante)
        - Ereignisausgang: `IND` (Indication - signalisiert neue Informationen)
        - Datenausgang: `sNameField`, `sNetEv`, `sCfInfo` (Strukturierte Ausgänge)
- **Funktionsweise**: Der Baustein überwacht das Netzwerk auf Basis der angegebenen Adresse und Maske. Wenn der entsprechende Teilnehmer identifiziert wird, stellt er dessen Namensfeld, Netzwerkereignis-Daten und CF-Informationen zur Verfügung.

### Sub-Bausteine: AlPgnRxNew8Bcylc
Dieser Baustein realisiert den eigentlichen Empfang der zyklischen Nachricht.

- **Typ**: `isobus::pgn::rx::AlPgnRxNew8Bcylc`
- **Verwendete interne FBs**:
    - **AlPgnRxNew8Bcylc**: `isobus::pgn::rx::AlPgnRxNew8Bcylc`
        - Parameter: `u32Pgn` = `61184` (Zu empfangende PGN)
        - Parameter: `u16DaSize` = `8` (Datengröße in Bytes)
        - Parameter: `u8Priority` = `3` (Priorität der Nachricht)
        - Parameter: `u16CtrlTime` = `1500` (Überwachungszeit in ms)
        - Dateneingang: `NmSource` (Quelle aus dem Netzwerkmanagement)
        - Datenausgang: `Data` (Empfangene Nachricht)
- **Funktionsweise**: Er wird konfiguriert, um zyklisch eine 8-Byte große Nachricht mit der PGN 61184 zu empfangen. Er benötigt die Netzwerkinformationen (`NmSource`) vom `NmGetCfInfo`-Baustein, um korrekt zu arbeiten.

### Sub-Bausteine: STRUCT_DEMUX (Mehrfachverwendung)
Diese Bausteine dienen dazu, komplexe strukturierte Datentypen in ihre Einzelbestandteile zu zerlegen, um sie lesbar oder weiterverarbeitbar zu machen.

- **Typ**: `eclipse4diac::convert::STRUCT_DEMUX`
- **Verwendete Instanzen**:
    - **STRUCT_DEMUX_3**: Zerlegt `isobus::pgn::NAMEFIELD_T` (Informationen zum Namensfeld).
    - **STRUCT_DEMUX_4**: Zerlegt `isobus::pgn::CF_INFO_T` (Informationen zur Control Function).
    - **STRUCT_DEMUX_5**: Zerlegt `isobus::pgn::ISONETEVENT_T` (Netzwerkereignisse).
    - **STRUCT_DEMUX**: Zerlegt `isobus::pgn::CAN_MSG` (Die eigentliche CAN-Nachricht).

## Programmablauf und Verbindungen

Der Ablauf der Übung wird durch die Initialisierung und Ereignisse im Netzwerk gesteuert:

1.  **Netzwerk-Identifikation**:
    Der Baustein `NmGetCfInfo_1` sucht auf dem Bus (`NODE1`) nach einem Teilnehmer, der dem Filter `PEAK_FLT` und der Adresse `PEAK_ADD` entspricht.
    
2.  **Verarbeitung der Identifikation**:
    Sobald Informationen verfügbar sind (`IND`-Event von `NmGetCfInfo_1`), werden drei parallele Aktionen ausgelöst:
    *   Die Strukturdaten `sNameField`, `sCfInfo` und `sNetEv` werden an die jeweiligen Demultiplexer (`STRUCT_DEMUX_3`, `_4`, `_5`) übergeben, um die Details des gefundenen Teilnehmers offenzulegen.
    *   Das Ereignis triggert den Eingang `install` am Baustein `AlPgnRxNew8Bcylc`.

3.  **Installation des Empfängers**:
    Der Baustein `AlPgnRxNew8Bcylc` nutzt die `sNetEv`-Daten von `NmGetCfInfo_1` am Eingang `NmSource`. Damit wird der Empfangskanal für die PGN 61184 (Proprietary B) eingerichtet. Die Zyklusüberwachung ist auf 1500 ms eingestellt.

4.  **Nachrichtenempfang**:
    Wenn die Nachricht mit PGN 61184 empfangen wird, feuert `AlPgnRxNew8Bcylc` das `IND`-Event. Die empfangenen Daten (`Data`) werden an den letzten `STRUCT_DEMUX` übergeben, der die `CAN_MSG`-Struktur aufschlüsselt (z.B. CAN-ID, DLC, Daten-Bytes).

## Zusammenfassung
Die Übung 131 demonstriert die Kopplung von Netzwerkmanagement und Nachrichtenempfang im ISOBUS-Umfeld. Sie zeigt, wie man dynamisch auf basierend auf Netzwerkinformationen einen zyklischen Empfänger für spezifische PGNs instanziiert und wie die komplexen ISOBUS-Datenstrukturen in 4diac zur Analyse zerlegt werden.