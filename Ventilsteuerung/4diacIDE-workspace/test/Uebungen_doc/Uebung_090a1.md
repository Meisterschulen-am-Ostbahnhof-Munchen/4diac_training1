# Uebung_090a1: Beispiel für F_MUX_2

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des Multiplexer-Funktionsbausteins F_MUX_2 in einer 4diac-IDE Anwendung. Das Programm zeigt, wie ein Multiplexer zur Auswahl zwischen verschiedenen Eingangssignalen verwendet werden kann.

## Verwendete Funktionsbausteine (FBs)

### F_MUX_2
- **Typ**: Multiplexer-Funktionsbaustein mit 2 Eingängen
- **Funktionsweise**: Wählt zwischen zwei Eingangssignalen (IN1 und IN2) basierend auf dem Steuersignal K aus

### logiBUS_IX (DigitalInput)
- **Typ**: Digitaler Eingangsbaustein für logiBUS
- **Parameter**: 
  - QI = TRUE (aktiviert den Baustein)
  - Input = logiBUS_DI::Input_Ix (konfiguriert den spezifischen Eingangskanal)

### F_BOOL_TO_UINT
- **Typ**: Typkonvertierungsbaustein
- **Funktionsweise**: Wandelt einen BOOL-Wert in einen UINT-Wert um

### logiBUS_QX (DigitalOutput)
- **Typ**: Digitaler Ausgangsbaustein für logiBUS
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (konfiguriert den spezifischen Ausgangskanal)

## Programmablauf und Verbindungen

Das Programm verwendet drei digitale Eingänge (I1, I2, I4) und einen digitalen Ausgang (Q1). Der Ablauf ist wie folgt:

1. **Ereignisverbindungen**:
   - DigitalInput_I4.IND → F_BOOL_TO_UINT_I4.REQ
   - F_MUX_2.CNF → DigitalOutput_Q1.REQ
   - DigitalInput_I1.IND → F_MUX_2.REQ
   - DigitalInput_I2.IND → F_MUX_2.REQ

2. **Datenverbindungen**:
   - DigitalInput_I4.IN → F_BOOL_TO_UINT_I4.IN
   - F_BOOL_TO_UINT_I4.OUT → F_MUX_2.K (Steuersignal)
   - DigitalInput_I1.IN → F_MUX_2.IN1 (Eingang 1)
   - DigitalInput_I2.IN → F_MUX_2.IN2 (Eingang 2)
   - F_MUX_2.OUT → DigitalOutput_Q1.OUT

**Funktionsweise**: 
- Eingang I4 steuert über den Typkonverter F_BOOL_TO_UINT die Auswahl des Multiplexers
- Je nach Wert von I4 wird entweder der Wert von I1 oder I2 an den Ausgang Q1 weitergeleitet
- Die Eingänge I1 und I2 liefern die alternativen Signale für den Multiplexer

**Lernziele**:
- Verständnis des Multiplexer-Prinzips
- Umgang mit Typkonvertierungen (BOOL zu UINT)
- Aufbau von Steuerungslogik mit Multiplexern
- Verwendung von logiBUS-Ein-/Ausgängen

**Schwierigkeitsgrad**: Einfach
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Datenfluss

## Zusammenfassung
Diese Übung vermittelt grundlegende Kenntnisse im Umgang mit Multiplexern in der 4diac-IDE. Der F_MUX_2 Baustein ermöglicht die Auswahl zwischen verschiedenen Eingangssignalen basierend auf einem Steuersignal. Die Übung zeigt zudem die praktische Anwendung von Typkonvertierungen und die Integration mit logiBUS-Ein-/Ausgängen.