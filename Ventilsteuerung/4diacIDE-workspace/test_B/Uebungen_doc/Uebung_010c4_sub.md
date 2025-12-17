Hier ist die Dokumentation für die Übung `Uebung_010c4_sub`, basierend auf den bereitgestellten XML-Daten.

# Uebung_010c4_sub

![Uebung_010c4_sub](Uebung_010c4_sub.png)

* * * * * * * * * *

## Einleitung
Bei dieser Übung handelt es sich um einen **Typed SubApp** (typisierten Unterbaustein), der als wiederverwendbares Modul konzipiert ist. Die Hauptaufgabe dieses Bausteins besteht darin, eine Verbindung zwischen einem SoftKey auf einem ISOBUS-Terminal (UT) und einem physikalischen digitalen Ausgang herzustellen. Zusätzlich wird eine visuelle Rückmeldung (Hintergrundfarbe) für den SoftKey gesteuert.

Der Baustein kapselt die Logik für einen einzelnen SoftKey (F1) und dessen zugehörigen Ausgang (Q1) sowie die visuelle Darstellung (Grün/Weiß) und ermöglicht durch seine Schnittstellen (`u16ObjId`, `Output`) eine flexible Zuweisung in übergeordneten Anwendungen.

## Verwendete Funktionsbausteine (FBs)

Innerhalb dieses SubApp-Netzwerks werden folgende interne Bausteine und Sub-Bausteine verwendet, um die Funktionalität zu realisieren:

### Sub-Bausteine: GreenWhiteBackground
Dieser Baustein ist als `SubApp` innerhalb des Netzwerks integriert.
- **Typ**: `MyLib::sys::GreenWhiteBackground`
- **Funktionsweise**: Dieser Baustein ist für die visuelle Rückmeldung zuständig. Er empfängt den Status des Softkeys und ändert vermutlich die Hintergrundfarbe des entsprechenden Objekts auf dem Terminal (z.B. Wechsel zwischen Grün und Weiß basierend auf dem Aktivierungsstatus).
- **Verbindungen**:
    - Erhält Ereignisse (`REQ`) vom SoftKey.
    - Erhält Daten (`DI1`) vom SoftKey-Status.
    - Erhält die Objekt-ID (`u16ObjId`) von der SubApp-Schnittstelle.

### Interne Funktionsbausteine

#### SoftKey_F1
- **Typ**: `isobus::UT::io::Softkey::Softkey_IX`
- **Verwendete Parameter**:
    - `QI` = `TRUE`
- **Ereignisausgang**: `IND` (Indication - Zeigt eine Statusänderung an)
- **Datenausgang**: `IN` (Aktueller Status des SoftKeys)
- **Dateneingang**: `u16ObjId` (Die ID des zu überwachenden UI-Objekts)
- **Funktionsweise**: Dieser Baustein stellt die Schnittstelle zum ISOBUS Universal Terminal dar. Er überwacht den gedrückten Zustand des Softkeys mit der übergebenen Objekt-ID.

#### DigitalOutput_Q1
- **Typ**: `logiBUS::io::DQ::logiBUS_QX`
- **Verwendete Parameter**:
    - `QI` = `TRUE`
    - `PARAMS` (Visible = false)
- **Ereigniseingang**: `REQ` (Trigger zum Schreiben des Ausgangs)
- **Dateneingang**:
    - `OUT`: Der zu schreibende Wert (True/False).
    - `Output`: Die Adresse/Identifikation des physikalischen Ausgangs (von der SubApp-Schnittstelle).
- **Funktionsweise**: Dieser Baustein steuert den physikalischen digitalen Ausgang der Hardware an.

## Programmablauf und Verbindungen

Der Ablauf innerhalb dieses SubApps wird durch die Interaktion zwischen dem Benutzereingang (SoftKey) und den Ausgängen (Physikalisch & Visuell) bestimmt:

1.  **Initialisierung & Konfiguration**:
    - Über die Schnittstelle der SubApp werden die `u16ObjId` (Objekt-ID des Softkeys) und der `Output` (Hardware-Ausgangskonfiguration) in das System eingespeist.
    - Die `u16ObjId` wird an `SoftKey_F1` und `GreenWhiteBackground` verteilt.
    - Die `Output`-Konfiguration wird an `DigitalOutput_Q1` geleitet.

2.  **Signalverarbeitung**:
    - Sobald der SoftKey auf dem Terminal betätigt wird oder sich sein Status ändert, löst der Baustein **SoftKey_F1** das Ereignis `IND` aus.
    - Dieses Ereignis triggert gleichzeitig:
        - Die visuelle Aktualisierung im Baustein **GreenWhiteBackground** (`REQ`).
        - Das Schreiben des physikalischen Ausgangs im Baustein **DigitalOutput_Q1** (`REQ`).

3.  **Datenfluss**:
    - Der Statuswert (`IN`) von **SoftKey_F1** wird direkt an den Eingang `DI1` von **GreenWhiteBackground** weitergegeben, um die Farbe zu steuern.
    - Derselbe Statuswert (`IN`) wird an den Eingang `OUT` von **DigitalOutput_Q1** gesendet, um den physikalischen Ausgang entsprechend zu schalten (An/Aus).

Dieser Aufbau stellt sicher, dass der physikalische Ausgang und die visuelle Darstellung auf dem Terminal stets synchron zum Status des Softkeys sind.

## Zusammenfassung
Die `Uebung_010c4_sub` ist ein modularer Baustein zur Kopplung eines ISOBUS-Softkeys mit einem digitalen Hardware-Ausgang. Durch die Verwendung als "Typed SubApp" kann dieser Baustein mehrfach instanziiert werden, um verschiedene Tasten-Ausgangs-Paare zu steuern, wobei die Logik für die visuelle Rückmeldung (Green/White) und die Hardwareansteuerung zentral gekapselt ist.