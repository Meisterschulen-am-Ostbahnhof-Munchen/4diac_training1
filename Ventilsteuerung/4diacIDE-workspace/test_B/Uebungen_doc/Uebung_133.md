Hier ist die Dokumentation für die Übung 133, basierend auf den bereitgestellten XML-Daten.

# Uebung_133

*(Bild der Übung, falls vorhanden)*

* * * * * * * * * *

## Einleitung

Diese Übung beschäftigt sich mit der ISOBUS-Kommunikation, genauer gesagt mit der Einrichtung eines zyklischen Nachrichtenempfangs basierend auf einer Anfrage (Request Message Cyclic). Ziel ist es, einen spezifischen Teilnehmer am Bus zu identifizieren und anschließend einen Empfangs-Handler für eine spezifische PGN (Parameter Group Number) zu installieren, der Daten von diesem Teilnehmer erwartet.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung werden verschiedene Funktionsbausteine aus der `isobus`-Bibliothek sowie Konvertierungsbausteine verwendet.

### Haupt-Bausteine

#### `NmGetCfInfo_1` (isobus::pgn::NmGetCfInfo)
Dieser Baustein dient dazu, Informationen über eine "Control Function" (CF) im ISOBUS-Netzwerk zu erhalten. Er filtert den Busverkehr nach bestimmten Kriterien.

*   **Parameter:**
    *   `u8CanIdx` = `NODE1` (Der verwendete CAN-Knoten).
    *   `member` = `network` (Netzwerk-Mitgliedschaft).
    *   `address` = `PEAK_ADD` (Filteradresse).
    *   `mask` = `PEAK_FLT` (Filtermaske).
*   **Funktion:** Er überwacht den Bus und liefert bei Übereinstimmung (Event `IND`) detaillierte Informationen über den gefundenen Teilnehmer (Name, Netzwerk-Event-Daten, CF-Info).

#### `AlPgnRxNew8Bcylc_REQ` (isobus::pgn::rx::AlPgnRxNew8Bcylc_REQ)
Dieser Baustein ist für die Einrichtung (Installation) eines neuen Empfangs-Handlers zuständig. Er ist spezifisch für den zyklischen Empfang von 8-Byte-Daten konfiguriert, der wahrscheinlich über eine Request-Nachricht initiiert wird.

*   **Parameter:**
    *   `u32Pgn` = `61184` (Die zu empfangende PGN).
    *   `u16DaSize` = `8` (Datenlänge in Bytes).
    *   `u8Priority` = `3` (Priorität der Nachricht).
    *   `u16DefRepRate` = `500` (Standard-Wiederholrate in ms, hier 500ms).
    *   `u16CtrlTime` = `1500` (Kontrollzeit/Timeout in ms).
*   **Dateneingang:**
    *   `NmSource`: Erhält die Netzwerkinformation (`sNetEv`) vom `NmGetCfInfo_1`, um zu wissen, von welchem Gerät die Daten empfangen werden sollen.

#### `STRUCT_DEMUX` (eclipse4diac::convert::STRUCT_DEMUX)
Es werden mehrere Instanzen dieses Bausteins verwendet, um komplexe Datentypen in ihre Einzelteile zu zerlegen, meist zu Diagnosezwecken.

*   **Instanz `STRUCT_DEMUX_3`**: Zerlegt den Typ `isobus::pgn::NAMEFIELD_T`.
*   **Instanz `STRUCT_DEMUX_4`**: Zerlegt den Typ `isobus::pgn::CF_INFO_T`.
*   **Instanz `STRUCT_DEMUX_5`**: Zerlegt den Typ `isobus::pgn::ISONETEVENT_T`.
*   **Instanz `STRUCT_DEMUX`**: Zerlegt den Typ `isobus::pgn::CAN_MSG` (die eigentliche empfangene CAN-Nachricht).

## Programmablauf und Verbindungen

Der Ablauf der Übung lässt sich in folgende Schritte unterteilen:

1.  **Netzwerk-Scanning und Identifikation**:
    Der Baustein `NmGetCfInfo_1` sucht auf dem CAN-Bus (`NODE1`) nach einem Teilnehmer, der den Filterkriterien (`PEAK_ADD`, `PEAK_FLT`) entspricht.

2.  **Bereitstellung der Teilnehmer-Informationen**:
    Sobald der Teilnehmer identifiziert wurde, löst `NmGetCfInfo_1` das Event `IND` aus. Gleichzeitig werden drei Datenstrukturen ausgegeben:
    *   `sNameField` (NAME-Feld des Teilnehmers) -> geht an `STRUCT_DEMUX_3`.
    *   `sCfInfo` (Control Function Info) -> geht an `STRUCT_DEMUX_4`.
    *   `sNetEv` (Netzwerk Event) -> geht an `STRUCT_DEMUX_5` und an den Empfangsbaustein.
    Die Demultiplexer dienen hier primär der Visualisierung der gefundenen Daten.

3.  **Installation des Nachrichten-Empfangs**:
    Das `IND`-Event von `NmGetCfInfo_1` triggert den Eingang `install` am Baustein `AlPgnRxNew8Bcylc_REQ`.
    Wichtig ist hierbei die Datenverbindung: Der Ausgang `sNetEv` des Filterbausteins ist mit dem Eingang `NmSource` des Empfangsbausteins verbunden. Damit wird der Empfänger instruiert, zyklische Nachrichten der PGN 61184 *spezifisch* von diesem gefundenen Teilnehmer zu akzeptieren und zu überwachen (mit einer Zykluszeit von 500ms).

4.  **Datenempfang**:
    Wenn die PGN 61184 empfangen wird, feuert `AlPgnRxNew8Bcylc_REQ` das Event `IND`. Die empfangenen Rohdaten (`Data`) werden an den `STRUCT_DEMUX` übergeben, der die `CAN_MSG` Struktur aufschlüsselt.

## Zusammenfassung

Diese Übung demonstriert die dynamische Kopplung von Netzmanagement und Nachrichtenempfang im ISOBUS. Zuerst wird ein spezifischer Kommunikationspartner über Netzmanagement-Funktionen identifiziert (`NmGetCfInfo`). Dessen Identität wird anschließend verwendet, um einen gezielten, zyklischen Empfangskanal (`AlPgnRxNew8Bcylc_REQ`) für eine proprietäre PGN (61184) einzurichten. Dies ist ein typisches Muster für ISOBUS-Anwendungen, bei denen man erst zur Laufzeit weiß, mit welchem genauen Gerät (basierend auf NAME oder Funktion) kommuniziert werden soll.