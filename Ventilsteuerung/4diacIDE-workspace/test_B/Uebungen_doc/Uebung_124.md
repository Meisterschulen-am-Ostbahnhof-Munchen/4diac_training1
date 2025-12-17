Hier ist die Dokumentation für die Übung 124, basierend auf den bereitgestellten Daten.

# Uebung_124

*(Hier Platzhalter für ein Bild der Übung einfügen, falls vorhanden)*

* * * * * * * * * *

## Einleitung
Diese Übung befasst sich mit dem Senden von ISOBUS-Nachrichten (`ISOBUS Send Message`). Ziel ist es, einen spezifischen Netzwerkknoten (hier vermutlich ein Virtual Terminal) mittels Filterkriterien zu identifizieren und anschließend auf Tastendruck ein definiertes Datenpaket an diesen Knoten zu senden.

## Verwendete Funktionsbausteine (FBs)

In dieser SubApplikation werden verschiedene Funktionsbausteine kombiniert, um die Netzwerkverwaltung und das Senden von Nachrichten zu realisieren.

### Haupt-Bausteine:

### **NmGetCfInfo_1**
- **Typ**: `isobus::pgn::NmGetCfInfo`
- **Funktionsweise**: Dieser Baustein dient dazu, Informationen über eine Steuerfunktion (Control Function - CF) im ISOBUS-Netzwerk zu erhalten. Er filtert den Netzwerkverkehr basierend auf einer Adresse und einer Maske.
- **Konfiguration**:
    - **Parameter**:
        - `u8CanIdx` = `NODE1` (Der verwendete CAN-Knoten)
        - `member` = `network`
        - `address` = `VT_ADD` (Zieladresse, importiert aus Konstanten)
        - `mask` = `VT_FLT` (Filtermaske, importiert aus Konstanten)
    - **Ausgänge**:
        - Liefert `sNameField`, `sCfInfo` und `sNetEv` (Netzwerkevent mit Adressinformationen).

### **AlPgnTxNew8B**
- **Typ**: `isobus::pgn::tx::AlPgnTxNew8B`
- **Funktionsweise**: Dieser Baustein ist für das Senden einer neuen PGN-Nachricht mit einer Länge von 8 Bytes zuständig.
- **Konfiguration**:
    - **Parameter**:
        - `u32Pgn` = `61184` (Die zu sendende Parameter Group Number)
        - `u16DaSize` = `8` (Datengröße)
        - `u8Priority` = `3` (Priorität der Nachricht)
        - `Data` = `[16#FA, 16#FB, 16#FC, 16#FD, 16#FE, 16#FF, 16#F1, 16#F2]` (Das statische Daten-Array, das gesendet wird)
    - **Eingänge**:
        - `install`: Initialisiert den Sender mit dem Ziel (getriggert durch `NmGetCfInfo`).
        - `REQ`: Fordert das Senden der Nachricht an (getriggert durch den Taster).
        - `NmDestin`: Empfängt das Ziel aus dem `sNetEv` des `NmGetCfInfo`.

### **DigitalInput_CLK_I1**
- **Typ**: `logiBUS::io::DI::logiBUS_IE`
- **Funktionsweise**: Stellt die Schnittstelle zu einem physischen digitalen Eingang dar und generiert Events.
- **Konfiguration**:
    - **Parameter**:
        - `QI` = `TRUE`
        - `Input` = `Input_I1`
        - `InputEvent` = `BUTTON_SINGLE_CLICK` (Reagiert auf einen einfachen Klick).

### **STRUCT_DEMUX (3, 4, 5)**
- **Typ**: `eclipse4diac::convert::STRUCT_DEMUX`
- **Funktionsweise**: Diese Bausteine werden verwendet, um komplexe Datentypen (Strukturen) in ihre Einzelteile zu zerlegen, vermutlich zu Debugging- oder Analysezwecken.
- **Verwendete Typen**:
    - `isobus::pgn::NAMEFIELD_T`
    - `isobus::pgn::CF_INFO_T`
    - `isobus::pgn::ISONETEVENT_T`

## Programmablauf und Verbindungen

Der Ablauf der Übung lässt sich in zwei Phasen unterteilen: **Initialisierung/Suche** und **Senden**.

1.  **Netzwerksuche (Identifikation):**
    *   Der Baustein `NmGetCfInfo_1` überwacht das Netzwerk `NODE1`.
    *   Sobald ein Teilnehmer gefunden wird, der den Filterkriterien (`VT_ADD`, `VT_FLT`) entspricht, wird das Event `IND` ausgelöst.
    *   Gleichzeitig werden die Strukturdaten (`sNameField`, `sNetEv`, `sCfInfo`) ausgegeben. Diese werden zur Analyse an die `STRUCT_DEMUX` Bausteine geleitet.

2.  **Installation des Senders:**
    *   Das `IND`-Event von `NmGetCfInfo_1` ist mit dem `install`-Eingang des Senders `AlPgnTxNew8B` verbunden.
    *   Wichtig hierbei ist die Datenverbindung von `NmGetCfInfo_1.sNetEv` zu `AlPgnTxNew8B.NmDestin`. Damit "lernt" der Sender, an welche Adresse (Destination) die PGN 61184 gesendet werden soll.

3.  **Senden der Nachricht:**
    *   Der Baustein `DigitalInput_CLK_I1` überwacht den Eingang `Input_I1`.
    *   Bei einem einfachen Klick (`BUTTON_SINGLE_CLICK`) wird das Event `IND` ausgelöst.
    *   Dieses Event triggert den Eingang `REQ` am `AlPgnTxNew8B`.
    *   Daraufhin sendet der Baustein die definierten 8 Bytes (beginnend mit `0xFA`) an die zuvor installierte Zieladresse.

## Zusammenfassung
Die `Uebung_124` demonstriert einen typischen Anwendungsfall im ISOBUS-Umfeld: Das dynamische Finden eines Kommunikationspartners (z.B. ein Virtual Terminal) und das anschließende Senden von gerichtetem Datenverkehr (Destination Specific) ausgelöst durch eine Benutzerinteraktion (Taster). Die Verwendung der `DEMUX`-Bausteine deutet darauf hin, dass die empfangenen Netzwerkinformationen auch im Detail betrachtet werden können.