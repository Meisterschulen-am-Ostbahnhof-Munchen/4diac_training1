# Uebung_080: Beispiel für E_CTU

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_CTU-Funktionsbausteins (Up-Counter) in einem 4diac-IDE Programm. Das Beispiel zeigt einen einfachen Aufwärtszähler, der bei Erreichen eines vordefinierten Wertes eine Ausgabe aktiviert.

## Verwendete Funktionsbausteine (FBs)

### E_CTU
- **Typ**: E_CTU (Event-Driven Up Counter)
- **Parameter**: 
  - PV = UINT#5 (Preset Value = 5)
- **Ereigniseingänge**: 
  - CU (Count Up)
  - R (Reset)
- **Ereignisausgänge**: 
  - CUO (Count Up Output)
  - RO (Reset Output)
- **Datenausgänge**: 
  - Q (Counter Output Value)
  - CV (Current Counter Value)

### logiBUS_IE (Digital Input)
- **Typ**: logiBUS_IE (logiBUS Input Event)
- **Parameter**:
  - QI = TRUE (Qualified Input enabled)
  - Input = logiBUS_DI::Input_I1 / Input_I2
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Ereignisausgänge**: 
  - IND (Input Event Detected)

### logiBUS_QX (Digital Output)
- **Typ**: logiBUS_QX (logiBUS Output)
- **Parameter**:
  - QI = TRUE (Qualified Input enabled)
  - Output = logiBUS_DO::Output_Q1
- **Ereigniseingänge**: 
  - REQ (Request Output)
- **Dateneingänge**: 
  - OUT (Output Value)

## Programmablauf und Verbindungen

Das Programm implementiert einen einfachen Zähler mit folgenden Funktionen:

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_CTU.CU (Zähler erhöht sich bei Tastendruck I1)
- DigitalInput_CLK_I2.IND → E_CTU.R (Zähler-Reset bei Tastendruck I2)
- E_CTU.CUO → DigitalOutput_Q1.REQ (Ausgabe bei Erreichen des Preset-Wertes)
- E_CTU.RO → DigitalOutput_Q1.REQ (Ausgabe bei Reset)

**Datenverbindungen:**
- E_CTU.Q → DigitalOutput_Q1.OUT (Übergabe des Zählerstatus an Ausgabe)

**Funktionsweise:**
- Bei jedem Tastendruck auf I1 wird der Zähler um 1 erhöht
- Bei Erreichen des Preset-Wertes 5 wird die Ausgabe Q1 aktiviert
- Ein Tastendruck auf I2 setzt den Zähler zurück auf 0
- Die Ausgabe Q1 zeigt den aktuellen Zählerstatus an

**Lernziele:**
- Verständnis des E_CTU-Funktionsbausteins
- Implementierung eines einfachen Zählers
- Verwendung von Ereignis- und Datenverbindungen
- Arbeit mit digitalen Ein- und Ausgängen im logiBUS-System

**Schwierigkeitsgrad**: Einfach

## Zusammenfassung
Diese Übung bietet eine grundlegende Einführung in die Verwendung des E_CTU-Zählbausteins in 4diac-IDE. Sie zeigt die wesentlichen Konzepte der Ereignissteuerung und Datenverarbeitung in IEC 61499-basierten Steuerungssystemen und bildet eine gute Basis für komplexere Zähleranwendungen.