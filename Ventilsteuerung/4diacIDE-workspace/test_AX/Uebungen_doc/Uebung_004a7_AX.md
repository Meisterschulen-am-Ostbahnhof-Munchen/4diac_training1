Hier ist die Dokumentation für die Übung `Uebung_004a7_AX` basierend auf den bereitgestellten Informationen.

# Uebung_004a7_AX

![Uebung_004a7_AX](Uebung_004a7_AX.png)

* * * * * * * * * *

## Einleitung

Diese Übung demonstriert die Verwendung eines **Rendezvous-Bausteins (`E_REND`)** in Kombination mit einem **T-Flip-Flop (`AX_T_FF_SR`)**. Ziel der Schaltung ist es, zwei unabhängige Eingangsereignisse zu synchronisieren. Ein Ausgangssignal wird nur dann umgeschaltet (getoggelt), wenn zuvor beide Eingangssignale (Taster I1 und Taster I2) betätigt wurden. Ein dritter Taster dient als globaler Reset für die Synchronisation und den Speicherzustand.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden verschiedene Funktionsbausteine verschaltet, um die logische Verknüpfung der Eingänge und die Steuerung des Ausgangs zu realisieren.

### Sub-Bausteine: DigitalInput_CLK_I1 / I2 / I3
- **Typ**: `logiBUS::io::DI::logiBUS_IE`
- **Verwendete Parameter**:
    - `QI`: TRUE
    - `Input`: `Input_I1` / `Input_I2` / `Input_I3`
    - `InputEvent`: `BUTTON_SINGLE_CLICK`
- **Funktionsweise**: Diese Bausteine erfassen Einzelklicks der Taster. Sie wandeln das physische Signal in ein Ereignis (`IND`) um, das im Netzwerk weiterverarbeitet wird.

### Sub-Bausteine: E_REND
- **Typ**: `iec61499::events::E_REND`
- **Ereigniseingänge**: `EI1`, `EI2`, `R`
- **Ereignisausgänge**: `EO`
- **Funktionsweise**: Der `E_REND` (Event Rendezvous) Baustein dient der Synchronisation.
    - Er wartet darauf, dass sowohl an `EI1` als auch an `EI2` ein Ereignis eintrifft. Die Reihenfolge spielt dabei keine Rolle.
    - Erst wenn **beide** Ereignisse eingetroffen sind, feuert der Ausgang `EO`.
    - Der Eingang `R` setzt den internen Speicher des Bausteins zurück (löscht bereits eingetroffene Teil-Ereignisse).

### Sub-Bausteine: AX_T_FF_SR
- **Typ**: `adapter::events::unidirectional::AX_T_FF_SR`
- **Anschlüsse**:
    - `CLK`: Takteingang (Clock)
    - `R`: Reset-Eingang
    - `Q`: Datenausgang (über Adapterverbindung)
- **Funktionsweise**: Dies ist ein T-Flip-Flop (Toggle Flip-Flop) mit Set/Reset-Funktionalität, das über Adapter kommuniziert.
    - Bei jedem Ereignis am `CLK`-Eingang wechselt der Zustand des Ausgangs (von TRUE auf FALSE oder umgekehrt).
    - Ein Ereignis am `R`-Eingang setzt den Zustand sofort zurück.

### Sub-Bausteine: DigitalOutput_Q1
- **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
- **Verwendete Parameter**:
    - `QI`: TRUE
    - `Output`: `Output_Q1`
- **Funktionsweise**: Dieser Baustein steuert den physischen Ausgang an, basierend auf dem Signal, das er über die Adapterverbindung erhält.

## Programmablauf und Verbindungen

Der Ablauf der Schaltung lässt sich wie folgt beschreiben:

1.  **Eingangserfassung**:
    - **Taster I1** (`DigitalInput_CLK_I1`) sendet ein Ereignis an den Eingang `EI1` des `E_REND`-Bausteins.
    - **Taster I2** (`DigitalInput_CLK_I2`) sendet ein Ereignis an den Eingang `EI2` des `E_REND`-Bausteins.

2.  **Synchronisation (Rendezvous)**:
    - Der Baustein `E_REND` stellt sicher, dass der nachfolgende Prozess erst gestartet wird, wenn I1 **und** I2 betätigt wurden. Es ist egal, ob man erst I1 und dann I2 drückt oder umgekehrt.
    - Sobald das zweite benötigte Ereignis eintrifft, wird am Ausgang `EO` ein Signal ausgegeben.

3.  **Zustandswechsel (Toggle)**:
    - Das Ausgangssignal `EO` des Rendezvous-Bausteins ist mit dem Takteingang `CLK` des `AX_T_FF_SR` verbunden.
    - Das Flip-Flop wechselt seinen Zustand (Toggles). Das Ergebnis wird über eine Adapterverbindung an `DigitalOutput_Q1` gesendet, wodurch die Lampe/der Aktor an Q1 seinen Zustand ändert (An/Aus).

4.  **Reset-Funktion**:
    - **Taster I3** (`DigitalInput_CLK_I3`) fungiert als zentraler Reset.
    - Sein Ereignis ist mit dem `R`-Eingang des `E_REND`-Bausteins verbunden (setzt wartende Ereignisse zurück).
    - Gleichzeitig ist es mit dem `R`-Eingang des `AX_T_FF_SR` verbunden (setzt das Flip-Flop und damit den Ausgang Q1 zurück).

**Lernziele:**
- Verständnis des `E_REND`-Bausteins zur Ereignissynchronisation.
- Verwendung von T-Flip-Flops zur Zustandssteuerung.
- Implementierung einer globalen Reset-Logik für mehrere Bausteine gleichzeitig.

## Zusammenfassung

Die Übung `Uebung_004a7_AX` zeigt eine robuste Methode, um sicherzustellen, dass zwei Bedingungen (Tasterklicks) erfüllt sein müssen, um eine Aktion auszulösen. Durch die Kombination von `E_REND` und einem T-Flip-Flop entsteht eine Schaltung, bei der man beide Eingabetaster betätigen muss, um den Ausgangszustand zu wechseln, während ein dritter Taster jederzeit einen definierten Ausgangszustand (Reset) wiederherstellen kann.