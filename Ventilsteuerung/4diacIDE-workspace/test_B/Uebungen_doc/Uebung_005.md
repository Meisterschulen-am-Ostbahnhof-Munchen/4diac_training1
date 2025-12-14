# Uebung_005: Toggle Flip-Flop mit IX

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle-Flip-Flops unter Verwendung von IX-Eingängen. Das System realisiert eine Schaltung, bei der ein digitaler Eingang über einen Schalterbaustein den Takt für ein Flip-Flop bereitstellt, dessen Ausgangszustand bei jedem Taktwechsel toggelt.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktionsweise**: Liest den digitalen Eingang I1 vom logiBUS-System ein

### E_SWITCH
- **Typ**: E_SWITCH
- **Funktionsweise**: Dient als Schalter, der Ereignisse basierend auf dem G-Eingang weiterleitet

### E_T_FF
- **Typ**: E_T_FF
- **Funktionsweise**: Toggle-Flip-Flop, das bei jedem Taktimpuls am CLK-Eingang seinen Ausgangszustand wechselt

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Schreibt den Ausgangswert auf den digitalen Ausgang Q1 des logiBUS-Systems

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → E_SWITCH.EI
- E_SWITCH.EO1 → E_T_FF.CLK
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → E_SWITCH.G
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Der digitale Eingang I1 wird kontinuierlich eingelesen
2. Bei Änderung des Eingangssignals wird ein Ereignis an E_SWITCH gesendet
3. E_SWITCH leitet das Ereignis an E_T_FF weiter, wenn G=TRUE
4. E_T_FF toggelt seinen Ausgang Q bei jedem Taktimpuls
5. Der Ausgangswert wird an den digitalen Ausgang Q1 geschrieben

**Lernziele:**
- Verständnis von Toggle-Flip-Flop-Schaltungen
- Umgang mit digitalen Ein- und Ausgängen über logiBUS
- Ereignisgesteuerte Programmierung mit Schalterbausteinen
- Signalverarbeitung in IEC 61499-Systemen

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der IEC 61499, digitale Schaltungen

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung eines Toggle-Flip-Flops mit IX-Eingängen. Der Aufbau demonstriert die Verknüpfung von digitalen Ein-/Ausgängen mit ereignisgesteuerten Funktionsbausteinen. Das System ermöglicht das experimentelle Erleben der Flip-Flop-Funktionalität und vermittelt grundlegende Konzepte der ereignisbasierten Steuerung in 4diac-Systemen.