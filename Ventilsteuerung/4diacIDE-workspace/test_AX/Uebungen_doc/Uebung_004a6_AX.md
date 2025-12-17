Hier ist die Dokumentation für die Übung **Uebung_004a6_AX** basierend auf den bereitgestellten Daten.

# Uebung_004a6_AX

![Uebung_004a6_AX](Uebung_004a6_AX.png)

* * * * * * * * * *

## Einleitung

Diese Übung demonstriert die Steuerung eines Toggle-Flip-Flops (T-Flip-Flop) unter Verwendung eines **Rendezvous-Bausteins (`E_REND`)**. Ziel ist es, ein Ereignis (das Umschalten des Ausgangs) erst dann auszulösen, wenn zwei separate Eingangsereignisse eingetreten sind. Zusätzlich wird eine Reset-Funktion für das Rendezvous implementiert. Die Ansteuerung der Ein- und Ausgänge erfolgt über das logiBUS-System.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden folgende Funktionsbausteine verwendet, um die Logik zu realisieren:

### Sub-Bausteine:

#### **DigitalInput_CLK_I1** (und I2, I3)
- **Typ**: `logiBUS::io::DI::logiBUS_IE`
- **Beschreibung**: Dieser Baustein dient als Ereignisquelle (Event Input). Er generiert ein Ereignis (`IND`), wenn der physische Eingang betätigt wird.
- **Parameter**:
    - `QI` = `TRUE` (Baustein aktiviert)
    - `Input` = `Input_I1` (bzw. I2, I3)
    - `InputEvent` = `BUTTON_SINGLE_CLICK` (Reagiert auf einfachen Klick)

#### **E_REND**
- **Typ**: `iec61499::events::E_REND`
- **Beschreibung**: Der Rendezvous-Baustein synchronisiert zwei Ereignisse. Er gibt erst dann ein Ausgangsereignis (`EO`) aus, wenn an beiden Eingängen (`EI1` und `EI2`) ein Ereignis empfangen wurde.
- **Eingänge**: `EI1`, `EI2`, `R` (Reset)
- **Ausgänge**: `EO`

#### **E_T_FF**
- **Typ**: `adapter::events::unidirectional::AX_T_FF`
- **Beschreibung**: Ein Toggle-Flip-Flop, das seinen Zustand bei jedem Eingangsimpuls (`CLK`) wechselt (von Ein zu Aus und umgekehrt). Diese spezielle Variante verwendet Adapter-Verbindungen für den Signalausgang.
- **Eingänge**: `CLK`

#### **DigitalOutput_Q1**
- **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
- **Beschreibung**: Dieser Baustein steuert den physischen Ausgang an. Er empfängt den Zustand über eine Adapter-Verbindung.
- **Parameter**:
    - `QI` = `TRUE`
    - `Output` = `Output_Q1`

## Programmablauf und Verbindungen

Die Logik verknüpft drei Taster (I1, I2, I3) mit einem Ausgang (Q1) über eine Synchronisationslogik.

1.  **Eingangssignale**:
    *   Der Taster **I1** (`DigitalInput_CLK_I1`) sendet ein Signal an den Eingang `EI1` des `E_REND`-Bausteins.
    *   Der Taster **I2** (`DigitalInput_CLK_I2`) sendet ein Signal an den Eingang `EI2` des `E_REND`-Bausteins.
    *   Der Taster **I3** (`DigitalInput_CLK_I3`) ist mit dem Reset-Eingang `R` des `E_REND`-Bausteins verbunden.

2.  **Rendezvous-Logik (`E_REND`)**:
    *   Der Baustein wartet darauf, dass sowohl `EI1` (durch Taster I1) als auch `EI2` (durch Taster I2) aktiviert wurden. Die Reihenfolge spielt dabei keine Rolle.
    *   Erst wenn **beide** Ereignisse eingetreten sind, feuert der Ausgang `EO`.
    *   Wird Taster I3 gedrückt, wird der interne Speicher des Rendezvous-Bausteins zurückgesetzt (ein eventuell bereits eingegangenes Einzelsignal verfällt).

3.  **Toggle-Funktion (`E_T_FF`)**:
    *   Das Ausgangssignal `EO` des Rendezvous-Bausteins ist mit dem Takteingang `CLK` des Toggle-Flip-Flops verbunden.
    *   Sobald das Rendezvous erfolgreich war (beide Taster gedrückt), schaltet das Flip-Flop seinen Zustand um.

4.  **Ausgabe**:
    *   Der Zustand des Flip-Flops (`Q`) wird über eine Adapter-Verbindung an den Ausgangsbaustein `DigitalOutput_Q1` weitergegeben, welcher die Lampe Q1 entsprechend ein- oder ausschaltet.

**Lernziele:**
*   Verständnis der Ereignissynchronisation (Rendezvous-Pattern).
*   Verwendung von Event-gesteuerten Flip-Flops.
*   Umgang mit logiBUS Ein- und Ausgabebausteinen.

## Zusammenfassung

Die Übung `Uebung_004a6_AX` zeigt eine Schaltung, bei der eine Aktion (Umschalten von Q1) nur dann ausgeführt wird, wenn zwei Bedingungen (Taster I1 und Taster I2) erfüllt wurden. Ein dritter Taster (I3) ermöglicht das Zurücksetzen des Vorgangs. Dies simuliert eine Zweihand-Sicherheitssteuerung oder eine einfache UND-Verknüpfung auf Ereignisebene.