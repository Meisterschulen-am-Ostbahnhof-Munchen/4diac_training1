Hier ist die Dokumentationsseite für die Übung 132 basierend auf den bereitgestellten Daten.

# Uebung_132

![Uebung_132](Uebung_132.png)

* * * * * * * * * *

## Einleitung
Diese Übung (SubApplication) befasst sich mit der Verarbeitung und Anforderung von **ISOBUS Request Messages**. Das Hauptziel ist es, Netzwerkinformationen einer bestimmten Steuereinheit (Control Function) zu ermitteln, diese zu zerlegen und anschließend eine spezifische PGN-Anforderung (PGN 61184) durch ein Hardware-Ereignis (Tastendruck) auszulösen.

## Verwendete Funktionsbausteine (FBs)

In dieser SubApp werden verschiedene spezialisierte Bausteine für ISOBUS-Kommunikation und Hardware-Interaktion verwendet.

### Sub-Bausteine:

#### **NmGetCfInfo_1**
- **Typ**: `isobus::pgn::NmGetCfInfo`
- **Beschreibung**: Dieser Baustein ruft Informationen über eine Control Function (CF) aus dem Netzwerkmanagement ab.
- **Konfiguration**:
    - `u8CanIdx`: `NODE1` (CAN-Knoten)
    - `member`: `network`
    - `address`: `PEAK_ADD` (Zieladresse, definiert in Konstanten)
    - `mask`: `PEAK_FLT` (Filtermaske, definiert in Konstanten)

#### **STRUCT_DEMUX (3x)**
- **Typ**: `eclipse4diac::convert::STRUCT_DEMUX`
- **Beschreibung**: Dient dazu, komplexe strukturierte Datentypen in ihre Einzelteile zu zerlegen, um diese sichtbar oder weiterverarbeitbar zu machen.
- **Instanzen**:
    1. **STRUCT_DEMUX_3**: Zerlegt `isobus::pgn::NAMEFIELD_T`.
    2. **STRUCT_DEMUX_4**: Zerlegt `isobus::pgn::CF_INFO_T`.
    3. **STRUCT_DEMUX_5**: Zerlegt `isobus::pgn::ISONETEVENT_T`.

#### **AlPgnRxNew8B_REQ**
- **Typ**: `isobus::pgn::rx::AlPgnRxNew8B_REQ`
- **Beschreibung**: Dieser Baustein ist für die Handhabung des Empfangs oder der Anforderung einer neuen 8-Byte PGN zuständig.
- **Konfiguration**:
    - `u32Pgn`: `61184` (Proprietary A / Herstellerspezifisch)
    - `u16DaSize`: `8` (Datengröße)
    - `u8Priority`: `3` (Priorität)

#### **DigitalInput_CLK_I1**
- **Typ**: `logiBUS::io::DI::logiBUS_IE`
- **Beschreibung**: Stellt die Schnittstelle zu einem physischen digitalen Eingang dar.
- **Konfiguration**:
    - `Input`: `Input_I1` (Physischer Eingang 1)
    - `InputEvent`: `BUTTON_SINGLE_CLICK` (Reagiert auf einfachen Klick)
    - `QI`: `TRUE` (Eingang aktiviert)

## Programmablauf und Verbindungen

Der Ablauf der Übung lässt sich in zwei Hauptstränge unterteilen: **Netzwerk-Initialisierung** und **Benutzerinteraktion**.

1.  **Erfassung der Netzwerkinformationen**:
    *   Der Baustein `NmGetCfInfo_1` überwacht das Netzwerk (`NODE1`) basierend auf den Filterkriterien (`PEAK_ADD`, `PEAK_FLT`).
    *   Sobald Informationen verfügbar sind, feuert das Ereignis `IND`.
    *   **Datenfluss**: Die Ausgänge `sNameField`, `sCfInfo` und `sNetEv` werden an die jeweiligen `STRUCT_DEMUX`-Bausteine weitergeleitet, um die internen Strukturen (Name Field, CF Info, Network Event) aufzuschlüsseln.

2.  **Installation und Request**:
    *   Das Ereignis `IND` von `NmGetCfInfo_1` ist auch mit dem Eingang `install` des Bausteins `AlPgnRxNew8B_REQ` verbunden. Gleichzeitig wird das Netzwerk-Event (`sNetEv`) an den Eingang `NmSource` übergeben. Dies initialisiert den Handler für die PGN 61184.

3.  **Auslösung durch Hardware**:
    *   Der Baustein `DigitalInput_CLK_I1` überwacht den Taster an Eingang `I1`.
    *   Bei einem einfachen Klick (`BUTTON_SINGLE_CLICK`) wird das Ereignis `IND` ausgelöst.
    *   Dieses Ereignis triggert den Eingang `REQ` am Baustein `AlPgnRxNew8B_REQ`, wodurch die eigentliche Verarbeitung oder Anforderung der PGN 61184 ausgeführt wird.

## Zusammenfassung
Diese Übung demonstriert die Kopplung von Netzwerkmanagement-Logik mit Benutzerinteraktion. Sie zeigt, wie man basierend auf dynamisch ermittelten Netzwerkteilnehmern (via `NmGetCfInfo`) eine Kommunikationsschnittstelle für eine spezifische PGN (hier 61184) einrichtet und diese gezielt durch einen externen Hardware-Trigger (Taster) aktiviert.