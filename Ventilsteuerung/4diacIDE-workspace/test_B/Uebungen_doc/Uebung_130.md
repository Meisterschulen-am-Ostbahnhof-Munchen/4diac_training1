Hier ist die Dokumentation für die Übung 130 basierend auf den bereitgestellten XML-Daten.

# Uebung_130

![Uebung_130](Uebung_130.png)

* * * * * * * * * *

## Einleitung
Diese Übung (Uebung_130) befasst sich mit dem Empfang von ISOBUS-Nachrichten auf der Anwendungsebene (Application Layer). Der Schwerpunkt liegt auf der Verknüpfung von Netzwerkmanagement-Informationen (Network Management - NM) mit einem Empfangsbaustein. Ziel ist es, eine spezifische Parameter Group Number (PGN) von einem durch Filterkriterien definierten Teilnehmer am Bus zu empfangen und die Datenstruktur aufzulösen.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Application werden Bausteine aus der `isobus` Bibliothek sowie Standard-Konvertierungsbausteine von 4diac verwendet. Die Hauptlogik besteht darin, zunächst Informationen über einen Teilnehmer zu ermitteln und diese Informationen zu nutzen, um einen Nachrichten-Empfänger zu konfigurieren.

### Sub-Bausteine: NmGetCfInfo_1
Dieser Baustein ist für das Netzwerkmanagement zuständig. Er filtert den Bus nach spezifischen Teilnehmern.

- **Typ**: `isobus::pgn::NmGetCfInfo`
- **Verwendete interne Parameter**:
    - **u8CanIdx**: `NODE1` (Der CAN-Knoten, auf dem gelauscht wird).
    - **member**: `network` (Bezieht sich auf die Netzwerkschicht).
    - **address**: `PEAK_ADD` (Filter-Adresse, importiert aus Konstanten).
    - **mask**: `PEAK_FLT` (Filter-Maske, importiert aus Konstanten).
- **Funktionsweise**: 
  Der Baustein überwacht das Netzwerk auf Nachrichten, die den Filterkriterien (Adresse und Maske) entsprechen. Wenn ein entsprechender Teilnehmer (Control Function) gefunden wird, stellt der Baustein detaillierte Informationen über dessen Namen (`sNameField`), Netzwerkevents (`sNetEv`) und CF-Infos (`sCfInfo`) zur Verfügung.

### Sub-Bausteine: AlPgnRxNew8B
Dieser Baustein empfängt eine spezifische 8-Byte PGN von einem definierten Sender.

- **Typ**: `isobus::pgn::rx::AlPgnRxNew8B`
- **Verwendete interne Parameter**:
    - **u32Pgn**: `61184` (Die zu empfangende PGN, hier im Proprietary B Bereich).
    - **u16DaSize**: `8` (Größe des Datenfeldes in Bytes).
    - **u8Priority**: `3` (Priorität der Nachricht).
- **Dateneingang**:
    - **NmSource**: Verbunden mit `NmGetCfInfo_1.sNetEv`. Dies teilt dem Empfänger mit, von welchem logischen Gerät die Nachricht erwartet wird.
- **Ereigniseingang**:
    - **install**: Wird getriggert durch `NmGetCfInfo_1.IND`, um den Empfänger zu registrieren.
- **Funktionsweise**: 
  Sobald der Baustein durch das `install`-Event und die entsprechende `NmSource` konfiguriert ist, lauscht er auf die PGN 61184. Wenn diese empfangen wird, gibt er die Rohdaten am `Data`-Ausgang aus und triggert das `IND`-Event.

### Sub-Bausteine: STRUCT_DEMUX (Mehrfachverwendung)
Diese Bausteine dienen der Visualisierung und Aufschlüsselung komplexer Datentypen.

- **Typ**: `eclipse4diac::convert::STRUCT_DEMUX`
- **Instanzen und Attribute**:
    - **STRUCT_DEMUX_3**: `StructuredType` = `isobus::pgn::NAMEFIELD_T` (Schlüsselt das ISO-NAME-Feld auf).
    - **STRUCT_DEMUX_4**: `StructuredType` = `isobus::pgn::CF_INFO_T` (Schlüsselt Informationen zur Control Function auf).
    - **STRUCT_DEMUX_5**: `StructuredType` = `isobus::pgn::ISONETEVENT_T` (Schlüsselt das Netzwerk-Event auf).
    - **STRUCT_DEMUX**: `StructuredType` = `isobus::pgn::CAN_MSG` (Schlüsselt die empfangene CAN-Nachricht auf).
- **Funktionsweise**: 
  Sie zerlegen die eingehenden strukturierten Datentypen in ihre Einzelkomponenten, was für das Debugging und die Weiterverarbeitung der Daten essenziell ist.

## Programmablauf und Verbindungen

Der Ablauf der Übung gestaltet sich wie folgt:

1.  **Initialisierung & Suche**: Der Baustein `NmGetCfInfo_1` sucht auf dem CAN-Knoten `NODE1` nach einem Teilnehmer, der durch die Konstanten `PEAK_ADD` und `PEAK_FLT` definiert ist.
2.  **Erkennung**: Sobald dieser Teilnehmer erkannt wird oder Informationen sendet, feuert `NmGetCfInfo_1` das Event `IND`.
3.  **Informationsverteilung**:
    *   Die detaillierten Informationen (`sNameField`, `sCfInfo`, `sNetEv`) werden an die `STRUCT_DEMUX`-Bausteine weitergeleitet, um die Struktur des gefundenen Teilnehmers sichtbar zu machen.
    *   Wichtig: Die Netzwerkinformation (`sNetEv`) wird direkt an den Eingang `NmSource` des Empfangsbausteins `AlPgnRxNew8B` geleitet.
4.  **Installation des Listeners**: Das `IND`-Event von `NmGetCfInfo_1` löst gleichzeitig das `install`-Event am `AlPgnRxNew8B` aus. Damit weiß der Empfänger nun, von welchem Quellgerät er Nachrichten erwarten soll.
5.  **Nachrichtenempfang**: Der Baustein `AlPgnRxNew8B` wartet nun spezifisch auf die PGN `61184` (Proprietary B) von der zuvor identifizierten Quelle.
6.  **Ausgabe**: Wenn die PGN empfangen wird, wird das `IND`-Event am `AlPgnRxNew8B` ausgelöst. Die empfangenen Daten (`Data`) werden an einen weiteren `STRUCT_DEMUX` übergeben, der die `CAN_MSG` Struktur (ID, DLC, Data Payload) aufschlüsselt.

## Zusammenfassung
Die Übung 130 demonstriert exemplarisch das Zusammenspiel zwischen Netzwerkmanagement und Datenaustausch im ISOBUS-Umfeld. Sie zeigt, wie man dynamisch auf einen Netzwerkteilnehmer reagiert, dessen Identität verifiziert und anschließend einen Kommunikationskanal für eine spezifische PGN zu diesem Teilnehmer aufbaut. Die Verwendung von Demultiplexern ermöglicht dabei einen tiefen Einblick in die übertragenen Datenstrukturen.