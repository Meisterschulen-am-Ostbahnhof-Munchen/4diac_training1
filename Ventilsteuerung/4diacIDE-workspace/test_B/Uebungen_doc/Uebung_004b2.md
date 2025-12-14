# Uebung_004b2: Toggle Flip-Flop mit IE / Split / doppelt

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Implementierung eines Toggle Flip-Flop-Verhaltens mit doppelter Ausführung unter Verwendung von IEC 61499-Funktionsbausteinen. Die Anwendung nutzt Eingabeereignisse von Tastern und steuert digitale Ausgänge basierend auf einem Set-Reset-Verhalten.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

- **DigitalInput_CLK_I1** und **DigitalInput_CLK_I2** (Typ: logiBUS_IE)
  - Parameter: QI = TRUE, Input = logiBUS_DI::Input_I1/Input_I2, InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
  - Funktion: Erfassen von Tastereignissen (Einzelklick) an den Eingängen I1 und I2

- **E_SWITCH_I1** und **E_SWITCH_I2** (Typ: E_SWITCH)
  - Funktion: Ereignisverteiler basierend auf dem Steuersignal G

- **E_SR_I1** und **E_SR_I2** (Typ: E_SR)
  - Funktion: Set-Reset-Flipflop zur Zustandsspeicherung

- **DigitalOutput_Q1** und **DigitalOutput_Q2** (Typ: logiBUS_QX)
  - Parameter: QI = TRUE, Output = logiBUS_DO::Output_Q1/Output_Q2
  - Funktion: Ansteuerung der digitalen Ausgänge Q1 und Q2

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- Tasterereignisse (IND) werden an die E_SWITCH-Bausteine weitergeleitet
- E_SWITCH verteilt Ereignisse an Set(S) oder Reset(R) der E_SR-Bausteine
- E_SR-Ausgangsereignisse (EO) triggern die Ausgabebausteine (REQ)

### Datenverbindungen:
- Der Q-Ausgang der E_SR-Bausteine wird sowohl an die Ausgabebausteine (OUT) als auch an die Steuereingänge (G) der E_SWITCH-Bausteine geführt
- Dies erzeugt ein Rückkopplungssystem für das Toggle-Verhalten

### Funktionsweise:
Bei jedem Tastendruck an I1 oder I2:
1. Das Eingabeereignis wird an E_SWITCH weitergeleitet
2. E_SWITCH leitet das Ereignis an S oder R von E_SR weiter, abhängig vom aktuellen Q-Zustand
3. E_SR ändert seinen Zustand und gibt ein Ausgabeereignis aus
4. Der digitale Ausgang (Q1/Q2) wird entsprechend geschaltet
5. Der neue Zustand wird an E_SWITCH zurückgeführt, um den nächsten Toggle-Zyklus vorzubereiten

**Schwierigkeitsgrad**: Mittel  
**Benötigte Vorkenntnisse**: Grundverständnis von Flipflops, Ereignisverarbeitung in IEC 61499  
**Lernziele**: Verständnis von Toggle-Flipflop-Implementierung, Ereignisverteilung, Rückkopplungsschaltungen

## Zusammenfassung
Diese Übung zeigt eine elegante Implementierung eines Toggle Flip-Flops mit doppelter Ausführung unter Verwendung standardisierter IEC 61499-Bausteine. Die parallele Struktur für zwei unabhängige Kanäle demonstriert die Wiederverwendbarkeit und Skalierbarkeit des Konzepts. Die Verwendung von Ereignis-switchen mit Rückkopplung ermöglicht ein robustes Toggle-Verhalten ohne zusätzliche Zähler oder Timer.