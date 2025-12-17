Hier ist die Dokumentationsseite basierend auf den bereitgestellten XML-Inhalten.

# Uebung_010b2_AX

![Uebung_010b2_AX](Uebung_010b2_AX.png)

* * * * * * * * * *

## Einleitung
Die Übung **Uebung_010b2_AX** implementiert eine Toggle-Flip-Flop-Logik (T-Flip-Flop), die durch das Loslassen (Release) einer SoftKey-Taste ausgelöst wird. Das Ziel ist es, den digitalen Ausgang Q1 bei jedem Loslassen der Taste F1 umzuschalten (an/aus). Besonderheit hierbei ist die Verwendung von Adapter-Verbindungen für die Ausgangssteuerung und Input-Events für die Tastenabfrage.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden folgende Funktionsbausteine verwendet, um die Logik abzubilden:

### Sub-Bausteine:

#### **SoftKey_UP_F1**
- **Typ**: `isobus::UT::io::Softkey::Softkey_IE`
- **Beschreibung**: Dieser Baustein dient als Eingabestelle für ISOBUS Softkeys. Er ist spezifisch konfiguriert, um auf ein Ereignis zu reagieren, wenn die Taste losgelassen wird.
- **Parameter**:
    - `QI` = `TRUE` (Baustein aktiviert)
    - `u16ObjId` = `SoftKey_F1` (Zugeordneter SoftKey)
    - `InputEvent` = `SK_RELEASED` (Auslöser: Taste losgelassen)
- **Ereignisausgang**:
    - `IND`: Feuert, wenn das konfigurierte Ereignis (Taste F1 losgelassen) eintritt.

#### **E_T_FF**
- **Typ**: `adapter::events::unidirectional::AX_T_FF`
- **Beschreibung**: Ein Toggle-Flip-Flop, das über Adapter-Technologie realisiert ist. Es wechselt seinen internen Zustand bei jedem Signal am Takteingang.
- **Ereigniseingang**:
    - `CLK`: Takteingang (Clock), der das Umschalten auslöst.
- **Adapterausgang**:
    - `Q`: Der Ausgangszustand, der über eine Adapterverbindung weitergeleitet wird.

#### **DigitalOutput_Q1**
- **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
- **Beschreibung**: Repräsentiert einen digitalen Ausgang im logiBUS-System, der über Adapter gesteuert wird.
- **Parameter**:
    - `QI` = `TRUE`
    - `Output` = `Output_Q1` (Hardware-Zuordnung auf Ausgang Q1)
- **Adaptereingang**:
    - `OUT`: Empfängt den Zustand vom Flip-Flop.

## Programmablauf und Verbindungen

Der Ablauf der Schaltung gestaltet sich wie folgt:

1.  **Eingabe (SoftKey):**
    Der Benutzer interagiert mit dem SoftKey **F1**. Der Baustein `SoftKey_UP_F1` überwacht diesen SoftKey. Konkret ist er so eingestellt (`SK_RELEASED`), dass er erst reagiert, wenn die Taste **losgelassen** wird.
    
2.  **Signalverarbeitung (Trigger):**
    Sobald F1 losgelassen wird, sendet `SoftKey_UP_F1` ein Signal über den Event-Ausgang `IND`. Dieses Signal ist mit dem Eingang `CLK` des Bausteins `E_T_FF` verbunden.

3.  **Logik (Flip-Flop):**
    Der Baustein `E_T_FF` fungiert als T-Flip-Flop. Bei jedem empfangenen Event am `CLK`-Eingang wechselt er seinen Zustand (von EIN zu AUS oder von AUS zu EIN).

4.  **Ausgabe (Digital Output):**
    Der Zustand des Flip-Flops wird über den Adapter-Anschluss `Q` direkt an den Adapter-Eingang `OUT` des `DigitalOutput_Q1` übertragen. Dies schaltet den physischen Ausgang Q1 entsprechend um.

**Wichtige Verbindungen:**
- **Event-Verbindung**: `SoftKey_UP_F1.IND` $\rightarrow$ `E_T_FF.CLK`
- **Adapter-Verbindung**: `E_T_FF.Q` $\rightarrow$ `DigitalOutput_Q1.OUT`

**Lernziele:**
- Umgang mit ISOBUS Softkey Events (speziell `SK_RELEASED`).
- Nutzung von Adapter-basierten Flip-Flops (`AX_T_FF`).
- Verknüpfung von Logik und Hardware-Ausgängen über Adapter-Verbindungen.

## Zusammenfassung
Die Übung `Uebung_010b2_AX` stellt eine klassische Stromstoßschaltung dar, die über einen SoftKey bedient wird. Durch die Konfiguration auf "Release" wird ein präzises Schaltverhalten beim Loslassen der Taste F1 erreicht, welches den Ausgang Q1 alternierend ein- und ausschaltet.