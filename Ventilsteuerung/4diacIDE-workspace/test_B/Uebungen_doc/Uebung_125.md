Hier ist die Dokumentation für die Übung 125 basierend auf den bereitgestellten XML-Daten.

# Uebung_125

![Uebung_125](Uebung_125.png)

* * * * * * * * * *

## Einleitung
Diese Übung behandelt die ISOBUS-Kommunikation, spezifisch das Senden einer Nachricht auf Anfrage (Send Message on Request) unter Verwendung eines Callback-Mechanismus (CB). Das Ziel ist es, einen spezifischen Teilnehmer im Netzwerk zu identifizieren und eine Übertragungsressource (Transmit-FB) einzurichten, die ihre Daten dynamisch über einen Adapter von einem Sub-Baustein bezieht.

## Verwendete Funktionsbausteine (FBs)

### Hauptnetzwerk
Im Hauptnetzwerk werden folgende Funktionsbausteine verwendet:

*   **NmGetCfInfo_1** (`isobus::pgn::NmGetCfInfo`)
    *   Dient zur Ermittlung von Informationen über eine Control Function (CF) im ISOBUS-Netzwerk. Er filtert nach bestimmten Teilnehmern.
    *   **Parameter**:
        *   `u8CanIdx`: NODE1 (CAN-Knoten)
        *   `member`: network
        *   `address`: PEAK_ADD (Filter-Adresse)
        *   `mask`: PEAK_FLT (Filter-Maske)
*   **STRUCT_DEMUX_3, _4, _5** (`eclipse4diac::convert::STRUCT_DEMUX`)
    *   Dienen zum Aufschlüsseln (Demultiplexen) von komplexen Datentypen in ihre Einzelteile zur besseren Analyse oder Weiterverarbeitung.
    *   **Typen**:
        *   `NAMEFIELD_T` (Name Field des ISOBUS Namens)
        *   `CF_INFO_T` (Control Function Informationen)
        *   `ISONETEVENT_T` (Netzwerk-Ereignisse)
*   **AlPgnTxNew8B_REQ** (`isobus::pgn::tx::AlPgnTxNew8B_REQ`)
    *   Ein Sendebaustein für eine neue 8-Byte PGN-Nachricht. Dieser Baustein nutzt einen Request/Callback-Mechanismus.
    *   **Parameter**:
        *   `u32Pgn`: 61184 (Die zu sendende Parameter Group Number)
        *   `u16DaSize`: 8 (Datenlänge in Bytes)
        *   `u8Priority`: 3 (Priorität der Nachricht)

### Sub-Bausteine: DataSupply

Dieser Sub-Baustein kapselt die Logik zur Bereitstellung der Nutzdaten.

*   **Name der Datei**: `Uebung_12x_sub`
*   **Typ**: SubApp
*   **Funktionsweise**:
    *   Der Baustein `DataSupply` ist über einen Adapter (`PLUG1`) mit dem Sendebaustein `AlPgnTxNew8B_REQ` verbunden.
    *   Anstatt dass Daten statisch am Eingang des Sendebausteins anliegen, fordert der Sendebaustein über die Adapter-Verbindung (`CB` für Callback) die Daten von diesem Sub-Baustein an, wenn gesendet werden soll.

## Programmablauf und Verbindungen

1.  **Netzwerk-Scan und Identifikation**:
    *   Der Baustein `NmGetCfInfo_1` überwacht das Netzwerk (`NODE1`) auf Teilnehmer, die den Filterkriterien (`PEAK_ADD`, `PEAK_FLT`) entsprechen.
    *   Sobald ein entsprechender Teilnehmer gefunden wird oder ein Ereignis auftritt, feuert der Event-Ausgang `IND`.

2.  **Datenanalyse (Optional/Debug)**:
    *   Parallel zum Hauptablauf werden die vom Netzwerkbaustein gelieferten Strukturdaten (`sNameField`, `sCfInfo`, `sNetEv`) an die drei `STRUCT_DEMUX` Bausteine geleitet. Dies ermöglicht die detaillierte Betrachtung der Namensfelder, CF-Informationen und Netzwerkereignisse im Monitoring.

3.  **Installation der Sende-Ressource**:
    *   Das `IND`-Event von `NmGetCfInfo_1` triggert den Eingang `install` am Sendebaustein `AlPgnTxNew8B_REQ`.
    *   Gleichzeitig wird die Netzwerkinformation (`sNetEv`) an den Eingang `NmDestin` des Sendebausteins übergeben. Damit weiß der Sendebaustein, an welches Ziel im Netzwerk die PGN 61184 gesendet werden soll (oder ob es sich um einen Broadcast handelt, abhängig von der PGN-Definition).

4.  **Datenbereitstellung via Callback**:
    *   Der Baustein `AlPgnTxNew8B_REQ` besitzt keine direkten Dateneingänge für den Payload. Stattdessen ist der Adapter-Anschluss `CB` mit `DataSupply.PLUG1` verbunden.
    *   Die tatsächlichen 8 Byte Daten werden durch die Logik innerhalb der SubApp `DataSupply` generiert und über den Adapter bereitgestellt.

## Zusammenfassung
Diese Übung demonstriert eine fortgeschrittene Methode der ISOBUS-Programmierung in 4diac. Es wird gezeigt, wie man dynamisch auf Netzwerkteilnehmer reagiert und eine Kommunikationsverbindung aufbaut. Ein zentraler Lerninhalt ist die Trennung von Kommunikationsmanagement (in der Hauptanwendung) und Datenbereitstellung (gekapselt in einer SubApp via Adapter-Pattern). Dies erhöht die Modularität und Wiederverwendbarkeit des Codes.