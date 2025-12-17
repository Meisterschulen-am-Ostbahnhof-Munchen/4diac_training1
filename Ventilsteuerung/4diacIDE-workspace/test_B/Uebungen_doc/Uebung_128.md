Hier ist die Dokumentation für die Übung 128 basierend auf den bereitgestellten XML-Daten.

# Übung 128: ISOBUS Send Message GLOBAL

*(Hier Bild der Übung einfügen, falls vorhanden)*

* * * * * * * * * *

## Einleitung
Diese Übung befasst sich mit dem Senden einer ISOBUS-Nachricht an eine globale Adresse (Broadcast). Ziel ist es, eine proprietäre PGN (Parameter Group Number) über den CAN-Bus zu senden, sobald ein Hardware-Taster betätigt wird. Dabei wird die Nachricht nicht an einen spezifischen Teilnehmer, sondern an alle Teilnehmer im Netzwerk (`GLOBAL_A`) adressiert.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung werden verschiedene Funktionsbausteine aus den Bibliotheken `isobus`, `logiBUS` und `eclipse4diac` verwendet. Im Folgenden werden die wichtigsten Instanzen im Detail beschrieben.

### Sub-Bausteine: NmGetCfInfo_1
Dieser Baustein ist für das Abrufen von Informationen über die Control Function (CF) im Netzwerkmanagementsystem zuständig.
- **Typ**: `isobus::pgn::NmGetCfInfo`
- **Verwendete Parameter**:
    - `u8CanIdx` = `NODE1` (Verwendeter CAN-Knoten)
    - `member` = `thisMember` (Bezieht sich auf den eigenen Teilnehmer)
    - `address` = `FLT_ALL_PASS` (Filter für Adressen)
    - `mask` = `FLT_ALL_PASS` (Maske für Filter)
- **Funktionsweise**: Er stellt Informationen über den aktuellen Netzwerkstatus und Events bereit, die für die Konfiguration des Senders benötigt werden. Seine Ausgänge werden zudem zur Analyse mittels Demultiplexer aufgesplittet.

### Sub-Bausteine: AlPgnTxNew8B
Dies ist der eigentliche Sende-Baustein für die ISOBUS-Nachricht.
- **Typ**: `isobus::pgn::tx::AlPgnTxNew8B`
- **Verwendete Parameter**:
    - `u32Pgn` = `61184` (Die zu sendende PGN)
    - `u16DaSize` = `8` (Größe des Datenfelds in Bytes)
    - `u8Priority` = `3` (Priorität der Nachricht)
    - `Data` = `[16#FA, 16#FB, 16#FC, 16#FD, 16#FE, 16#FF, 16#F1, 16#F2]` (Fest definierte Nutzdaten)
- **Funktionsweise**: Sendet bei einem Trigger-Event (`REQ`) die konfigurierten 8 Bytes auf den Bus. Der Baustein muss zuvor über den Eingang `install` und `NmDestin` konfiguriert werden.

### Sub-Bausteine: DigitalInput_CLK_I1
Stellt die Verbindung zur physischen Hardware her (Taster).
- **Typ**: `logiBUS::io::DI::logiBUS_IE`
- **Verwendete Parameter**:
    - `QI` = `TRUE`
    - `Input` = `Input_I1` (Erster digitaler Eingang)
    - `InputEvent` = `BUTTON_SINGLE_CLICK` (Reagiert auf einfachen Klick)
- **Funktionsweise**: Erzeugt ein Event (`IND`), wenn der Taster einfach geklickt wird. Dieses Event löst das Senden der Nachricht aus.

### Sub-Bausteine: NetEv2NetEv
Dient der Anpassung des Netzwerk-Events für die Zieladressierung.
- **Typ**: `isobus::pgn::NetEv2NetEv`
- **Verwendete Parameter**:
    - `s16Handle` = `GLOBAL_A` (Zieladresse Global / Broadcast)
- **Funktionsweise**: Nimmt das Netzwerk-Event entgegen und leitet es so weiter, dass der Sender (`AlPgnTxNew8B`) weiß, dass die Nachricht global versendet werden soll.

### Weitere Hilfsbausteine
- **STRUCT_DEMUX (3, 4, 5)**: Diese Bausteine (`eclipse4diac::convert::STRUCT_DEMUX`) werden verwendet, um komplexe Datentypen (`NAMEFIELD_T`, `CF_INFO_T`, `ISONETEVENT_T`) in ihre Einzelteile zu zerlegen. Dies dient primär der Diagnose und Sichtbarmachung der internen Datenstrukturen, die vom `NmGetCfInfo_1` Baustein geliefert werden.

## Programmablauf und Verbindungen

Der Ablauf der Übung lässt sich in zwei Phasen unterteilen: Initialisierung/Konfiguration und Ausführung.

1.  **Netzwerk-Konfiguration**:
    *   Der Baustein `NmGetCfInfo_1` liefert Informationen über das Netzwerkmanagement.
    *   Das Ausgangssignal `sNetEv` (Netzwerk Event) und das Event `IND` werden an `NetEv2NetEv` geleitet.
    *   Der Baustein `NetEv2NetEv` ist mit dem Handle `GLOBAL_A` konfiguriert. Dies sorgt dafür, dass die Zielinformation auf "Global" (Broadcast) gesetzt wird.
    *   Das Ergebnis von `NetEv2NetEv` (Event `CNF` und Daten) wird an den Eingang `install` bzw. `NmDestin` des Sende-Bausteins `AlPgnTxNew8B` weitergegeben. Damit ist der Sender bereit, Nachrichten an alle Teilnehmer zu schicken.

2.  **Senden der Nachricht**:
    *   Der Baustein `DigitalInput_CLK_I1` überwacht den Eingang `Input_I1`.
    *   Sobald ein einfacher Klick (`BUTTON_SINGLE_CLICK`) erkannt wird, wird das `IND`-Event ausgelöst.
    *   Dieses Event ist mit dem `REQ`-Eingang des `AlPgnTxNew8B` verbunden.
    *   Daraufhin sendet der Baustein die PGN `61184` mit der Priorität 3 und dem festen Datenarray `FA FB FC FD FE FF F1 F2` auf den CAN-Bus (`NODE1`).

3.  **Diagnose**:
    *   Parallel dazu werden die Ausgänge des `NmGetCfInfo_1` (`sNameField`, `sCfInfo`, `sNetEv`) permanent über die `STRUCT_DEMUX`-Bausteine aufgeschlüsselt, um den Zustand des Netzwerkmanagements im Monitoring beobachten zu können.

## Zusammenfassung
In dieser Übung wird gelernt, wie man eine Broadcast-Nachricht im ISOBUS-Netzwerk initiiert. Es wird gezeigt, wie Netzwerk-Events verarbeitet werden, um die Zieladresse (`GLOBAL_A`) für einen Sende-Baustein (`AlPgnTxNew8B`) festzulegen, und wie ein Hardware-Eingang (Taster) genutzt wird, um das Senden der Datenpakete manuell auszulösen.