# Uebung_094a: Beispiel für QI anstelle Permit

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung eines T-Flip-Flops (E_T_FF) in Kombination mit digitalen Ein- und Ausgängen. Das Programm zeigt ein Beispiel für Aufwärtszählvorgänge und illustriert die Verwendung des QI-Parameters als Alternative zu Permit-Signalen. Die Übung ist Teil des UAO Curriculum Module 3 zum IEC 61499 Standard.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**: Input = logiBUS_DI::Input_I1
- **Ereignisausgänge**: IND
- **Dateneingänge**: QI
- **Datenausgänge**: IN

### DigitalInput_CLK_I2
- **Typ**: logiBUS_IE
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I2
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Ereignisausgänge**: IND

### E_T_FF
- **Typ**: E_T_FF
- **Ereigniseingänge**: CLK
- **Ereignisausgänge**: EO
- **Datenausgänge**: Q

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**: 
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Ereigniseingänge**: REQ
- **Dateneingänge**: OUT

## Programmablauf und Verbindungen

Das Programm verwendet einen T-Flip-Flop (E_T_FF) als zentrales Element. Der DigitalInput_CLK_I2 Baustein erzeugt Taktsignale bei Betätigung des Tasters I2 und triggert damit den CLK-Eingang des T-Flip-Flops.

**Ereignisverbindungen:**
- DigitalInput_CLK_I2.IND → E_T_FF.CLK (Taktsignal)
- DigitalInput_I1.IND → DigitalOutput_Q1.REQ (Ausgabeanforderung)
- E_T_FF.EO → DigitalInput_I1.INIT (Initialisierung)

**Datenverbindungen:**
- DigitalInput_I1.IN → DigitalOutput_Q1.OUT (Direkte Signalübertragung)
- E_T_FF.Q → DigitalInput_I1.QI (QI-Steuerung)

Der T-Flip-Flop ändert seinen Ausgangszustand bei jedem Taktimpuls und steuert über den Q-Ausgang das QI-Signal des DigitalInput_I1 Bausteins. Dies ermöglicht eine bedingte Verarbeitung der Eingangssignale.

## Zusammenfassung
Diese Übung veranschaulicht die grundlegende Funktionsweise eines T-Flip-Flops in einer IEC 61499-basierten Steuerung. Sie zeigt die praktische Anwendung von QI-Parametern zur Steuerung von Funktionsbausteinen und demonstriert die Verknüpfung von digitalen Ein- und Ausgängen mit logischen Verarbeitungseinheiten. Die Übung eignet sich ideal zum Verständnis von Zählvorgängen und Flip-Flop-Schaltungen in verteilten Automatisierungssystemen.