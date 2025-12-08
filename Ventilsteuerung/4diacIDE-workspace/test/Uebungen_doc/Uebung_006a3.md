# Uebung_006a3: SR und T-Flip-Flop mit 3x IE

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines SR-Flip-Flops und T-Flip-Flops in Kombination mit drei Eingabeelementen. Das System steuert eine Links-/Rechtslauf-Steuerung basierend auf den Eingabesignalen.

## Verwendete Funktionsbausteine (FBs)

### Hauptbausteine:
- **DigitalInput_CLK_I1**, **DigitalInput_CLK_I2**, **DigitalInput_CLK_I3** (Typ: logiBUS_IE)
  - Parameter: QI = TRUE, Input = logiBUS_DI::Input_I1/I2/I3, InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **E_T_FF_SR** (Typ: E_T_FF_SR) - Kombinierter T- und SR-Flip-Flop
- **AND_LINKS**, **AND_RECHTS** (Typ: AND_2_BOOL) - Logische UND-Verknüpfungen
- **Linkslauf**, **Rechtslauf** (Typ: logiBUS_QX) - Ausgabeelemente für Links- und Rechtslauf
  - Parameter: QI = TRUE, Output = logiBUS_DO::Output_Q1/Q2

### Sub-Bausteine: LinksRechts_T_FF (Typ: Uebung_006a3_sub)

**Verwendete interne FBs:**
- **E_T_FF** (Typ: E_T_FF) - T-Flip-Flop
- **E_SWITCH** (Typ: E_SWITCH) - Ereignis-Schalter
- **F_NOT** (Typ: F_NOT) - Logischer NOT-Operator

**Funktionsweise:**
Der Sub-Baustein verarbeitet das Eingangssignal DI und steuert die Links-/Rechts-Ausgänge. Der E_SWITCH leitet Ereignisse basierend auf dem DI-Signal an den T-Flip-Flop weiter. Der Ausgang Q des T-Flip-Flops wird direkt als "Rechts"-Signal ausgegeben und durch einen NOT-Operator invertiert als "Links"-Signal.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- Die drei DigitalInputs (I1, I2, I3) lösen Ereignisse für S, R und CLK des E_T_FF_SR aus
- Der E_T_FF_SR-Ausgang EO triggert sowohl den Sub-Baustein als auch die AND-Gatter
- Der Sub-Baustein-Ausgang EO aktiviert die AND-Gatter
- Die AND-Gatter steuern die Ausgabeelemente Linkslauf und Rechtslauf

**Datenverbindungen:**
- Der Q-Ausgang des E_T_FF_SR wird an beide AND-Gatter und den Sub-Baustein weitergeleitet
- Der Sub-Baustein generiert Links- und Rechts-Signale für die AND-Gatter
- Die AND-Gatter-Ausgänge steuern die physischen Ausgänge Q1 und Q2

**Lernziele:**
- Verständnis von Flip-Flop-Schaltungen (SR und T-Flip-Flop)
- Kombination logischer Verknüpfungen mit Speicherelementen
- Ereignisgesteuerte Programmabläufe in 4diac
- Verwendung von Sub-Applikationen zur Strukturierung

**Schwierigkeitsgrad:** Mittel
**Benötigte Vorkenntnisse:** Grundlagen logischer Schaltungen, Flip-Flop-Funktionalität, 4diac-Bedienung

**Starten der Übung:** Nach dem Laden der Applikation können die drei Eingänge I1, I2, I3 über Taster bedient werden, um das Verhalten der Links-/Rechts-Steuerung zu beobachten.

## Zusammenfassung
Diese Übung verdeutlicht die praktische Anwendung von Flip-Flop-Schaltungen in einer Steuerungsapplikation. Durch die Kombination von SR- und T-Flip-Flops mit logischen Verknüpfungen entsteht ein komplexes Steuerungssystem für eine Links-/Rechtslauf-Steuerung. Die Verwendung von Sub-Applikationen zeigt zudem Methoden zur strukturierten Programmierung in 4diac.