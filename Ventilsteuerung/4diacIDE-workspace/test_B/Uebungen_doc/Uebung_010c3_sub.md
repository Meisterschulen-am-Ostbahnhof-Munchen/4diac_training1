Hier ist die Dokumentation für die Übung `Uebung_010c3_sub` basierend auf den bereitgestellten Daten.

# Uebung_010c3_sub

![Uebung_010c3_sub](Uebung_010c3_sub.png)

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine sogenannte "Typed SubApp" (typisierte Unteranwendung), die eine gekapselte Logik für die Steuerung eines digitalen Ausgangs über einen SoftKey (F1) bereitstellt. Zusätzlich wird ein visuelles Feedback über einen Hintergrund (GreenWhiteBackground) gegeben. Der Baustein ist so konzipiert, dass er wiederverwendbar ist, indem er die Objekt-ID und den spezifischen Ausgang als Eingabeparameter akzeptiert.

## Verwendete Funktionsbausteine (FBs)

In diesem Netzwerk werden spezifische Funktionsbausteine und eine weitere Sub-Anwendung kombiniert, um die gewünschte Funktionalität zu erreichen.

### Sub-Bausteine: GreenWhiteBackground
- **Typ**: `MyLib::sys::GreenWhiteBackground`
- **Beschreibung**: Dieser Baustein wird verwendet, um den Hintergrundstatus basierend auf der Eingabe zu ändern (vermutlich Wechsel zwischen Grün und Weiß).
- **Verbindungen**:
    - Erhält Ereignisse vom SoftKey (`IND` -> `REQ`).
    - Erhält Daten vom SoftKey (`IN` -> `DI1`) und die Objekt-ID (`u16ObjId`).

### Verwendete interne FBs

Hier werden die direkt im Netzwerk instanziierten Funktionsbausteine beschrieben:

- **SoftKey_F1**: `isobus::UT::io::Softkey::Softkey_IX`
    - **Parameter**: 
        - `QI` = `TRUE`
    - **Ereignisausgang**: `IND` (Indication - Signalisiert eine Zustandsänderung des SoftKeys).
    - **Datenausgang**: `IN` (Der aktuelle Wert/Status des SoftKeys).
    - **Dateneingang**: `u16ObjId` (Wird von der SubApp-Schnittstelle durchgereicht).
    - **Funktionsweise**: Dieser Baustein repräsentiert die Eingabelogik für die SoftKey-Taste F1 auf dem ISO-BUS Terminal.

- **DigitalOutput_Q1**: `logiBUS::io::DQ::logiBUS_QX`
    - **Parameter**: 
        - `QI` = `TRUE`
        - `PARAMS` = "" (Sichtbarkeit: false)
    - **Ereigniseingang**: `REQ` (Trigger zum Aktualisieren des Ausgangs).
    - **Dateneingang**: 
        - `OUT`: Empfängt den Status vom SoftKey.
        - `Output`: Wählt den physischen Ausgang (Q1..Q8) basierend auf der SubApp-Schnittstelle.
    - **Funktionsweise**: Dieser Baustein steuert den physischen digitalen Ausgang des Systems.

## Programmablauf und Verbindungen

Der Ablauf innerhalb dieser SubApp wird durch Ereignis- und Datenflüsse gesteuert, die von außen parametrisiert werden:

1.  **Initialisierung & Parameterübergabe**:
    - Die SubApp verfügt über zwei Eingänge: `u16ObjId` (Objekt-ID) und `Output` (Ausgangszuweisung).
    - `u16ObjId` wird direkt an den SoftKey `SoftKey_F1` und den Hintergrundbaustein `GreenWhiteBackground` weitergeleitet (Hidden Connections).
    - `Output` wird an den Baustein `DigitalOutput_Q1` geleitet, um festzulegen, welcher Hardware-Ausgang geschaltet werden soll.

2.  **Verarbeitung der Benutzereingabe**:
    - Wenn der SoftKey F1 betätigt wird, löst der Baustein `SoftKey_F1` das Ereignis `IND` aus.
    - Dieses Ereignis triggert parallel zwei Aktionen:
        - Es aktiviert den `DigitalOutput_Q1` (Eingang `REQ`).
        - Es aktiviert den `GreenWhiteBackground` (Eingang `REQ`).

3.  **Datenfluss**:
    - Der Status des SoftKeys (`IN` am Baustein `SoftKey_F1`) wird ausgelesen.
    - Dieser Wert wird an den Eingang `OUT` des `DigitalOutput_Q1` gesendet, wodurch der physische Ausgang entsprechend dem Tastendruck geschaltet wird.
    - Gleichzeitig wird der Wert an `DI1` des `GreenWhiteBackground` gesendet, um die visuelle Darstellung anzupassen.

Diese Struktur ermöglicht es, die Logik "Taste drückt Ausgang + Visuelles Feedback" mehrfach im Hauptprogramm zu verwenden, indem einfach verschiedene Ausgänge und Objekt-IDs an Instanzen dieser SubApp übergeben werden.

## Zusammenfassung
Die `Uebung_010c3_sub` ist ein wiederverwendbares Modul zur Kopplung einer SoftKey-Eingabe an einen konfigurierbaren digitalen Ausgang. Sie demonstriert die Kapselung von Logik, die Verwendung von Schnittstellenvariablen (`u16ObjId`, `Output`) zur Konfiguration interner Bausteine und die parallele Verarbeitung von visueller Rückmeldung und Hardware-Aktorik.