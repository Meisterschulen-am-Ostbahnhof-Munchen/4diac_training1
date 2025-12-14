# Uebung_020a: DigitalInput_I1 auf DigitalOutput_Q1

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verarbeitung eines digitalen Eingangssignals und dessen Ausgabe auf einen digitalen Ausgang. Es werden Ereignis- und Datenverbindungen zwischen verschiedenen Funktionsbausteinen realisiert, um ein einfaches Schaltsystem zu implementieren.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktion**: Liest den digitalen Eingang I1 des logiBUS Systems aus

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktion**: Schreibt auf den digitalen Ausgang Q1 des logiBUS Systems

### E_SWITCH
- **Typ**: E_SWITCH
- **Funktion**: Schaltbaustein, der je nach Eingangswert zwischen zwei Ereignisausgängen umschaltet

### E_RS
- **Typ**: E_RS
- **Funktion**: RS-Flipflop zur Speicherung des Schaltzustands

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → E_SWITCH.EI
- E_SWITCH.EO0 → E_RS.R (Reset)
- E_SWITCH.EO1 → E_RS.S (Set)
- E_RS.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → E_SWITCH.G (Steuerung)
- E_RS.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Der DigitalInput_I1 Baustein liest den Zustand des physischen Eingangs I1
2. Bei einer Zustandsänderung wird ein IND-Ereignis an E_SWITCH gesendet
3. E_SWITCH wertet den Datenwert aus und leitet das Ereignis entweder an EO0 (Reset) oder EO1 (Set) weiter
4. E_RS speichert den Zustand und gibt bei Änderung ein EO-Ereignis aus
5. DigitalOutput_Q1 setzt den Ausgang Q1 entsprechend dem gespeicherten Zustand

**Lernziele:**
- Grundlegende Verwendung von digitalen Ein- und Ausgängen
- Ereignisgesteuerte Programmierung
- Umschaltung zwischen verschiedenen Ereignispfaden
- Zustandsspeicherung mit RS-Flipflop

**Schwierigkeitsgrad**: Einfach
**Vorkenntnisse**: Grundlagen der 4diac-IDE und Funktionsbausteine

## Zusammenfassung
Diese Übung vermittelt die grundlegenden Prinzipien der ereignisgesteuerten Automatisierung mit 4diac. Sie zeigt, wie ein digitaler Eingang verarbeitet, über einen Schaltbaustein gesteuert und der resultierende Zustand auf einem digitalen Ausgang ausgegeben wird. Die Verwendung des RS-Flipflops ermöglicht dabei eine Zustandsspeicherung zwischen den Ereignissen.