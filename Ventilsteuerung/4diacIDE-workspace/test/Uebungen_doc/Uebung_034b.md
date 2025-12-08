# Uebung_034b: LONG_PRESS_HOLD-Eingang auf PWM Ausgang

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung von LONG_PRESS_HOLD-Eingängen zur Steuerung eines PWM-Ausgangs. Das Programm ermöglicht die Geschwindigkeitsregelung über Taster mit unterschiedlichen Betriebsmodi.

## Verwendete Funktionsbausteine (FBs)

### logiBUS_IE (Input Event)
- **Typ**: Eingangsbaustein für logiBUS
- **Verwendete Instanzen**:
  - **IE_SPEED_UP**: Konfiguriert für Input_I1 mit BUTTON_LONG_PRESS_HOLD
  - **IE_SPEED_DOWN**: Konfiguriert für Input_I2 mit BUTTON_LONG_PRESS_HOLD  
  - **IE_STOP**: Konfiguriert für Input_I3 mit BUTTON_SINGLE_CLICK
  - **IE_FULL**: Konfiguriert für Input_I4 mit BUTTON_SINGLE_CLICK

### E_CTUD_UDINT
- **Typ**: Hoch-/Runterzähler mit Vorwärts- und Rückwärtszählung
- **Parameter**: PV = 1023 (Endwert)
- **Funktionsweise**: Zählt bei CU-Ereignis hoch, bei CD-Ereignis runter, mit Reset- und Load-Funktionen

### F_MUL
- **Typ**: Multiplikationsbaustein
- **Parameter**: IN2 = UDINT#8 (konstanter Multiplikator)
- **Funktionsweise**: Multipliziert den Eingangswert mit 8

### F_UDINT_TO_DWORD
- **Typ**: Datentyp-Konverter
- **Funktionsweise**: Wandelt UDINT-Werte in DWORD-Werte um

### logiBUS_QD_PWM
- **Typ**: PWM-Ausgangsbaustein für logiBUS
- **Verwendete Instanzen**:
  - **PWMOutput_Q1**: Konfiguriert für Output_Q1
  - **Parameter**: QI = TRUE (aktiviert)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- IE_SPEED_UP.IND → E_CTUD.CU (Hochzählen)
- IE_SPEED_DOWN.IND → E_CTUD.CD (Runterzählen)  
- IE_STOP.IND → E_CTUD.R (Reset)
- IE_FULL.IND → E_CTUD.LD (Laden auf Maximalwert)
- E_CTUD.CO/RO/LDO → F_MUL.REQ
- F_MUL.CNF → F_UDINT_TO_DWORD.REQ
- F_UDINT_TO_DWORD.CNF → PWMOutput_Q1.REQ

**Datenverbindungen:**
- E_CTUD.CV → F_MUL.IN1 (Zählerwert zur Multiplikation)
- F_MUL.OUT → F_UDINT_TO_DWORD.IN (multiplizierter Wert zur Konvertierung)
- F_UDINT_TO_DWORD.OUT → PWMOutput_Q1.OUT (PWM-Steuerwert)

**Bedienung:**
- I1 (LONG_PRESS_HOLD): Erhöht die Geschwindigkeit
- I2 (LONG_PRESS_HOLD): Verringert die Geschwindigkeit  
- I3 (SINGLE_CLICK): Stoppt (Reset auf 0)
- I4 (SINGLE_CLICK): Volle Geschwindigkeit (Maximalwert)

## Zusammenfassung
Diese Übung zeigt die Kombination von verschiedenen Eingangsereignissen (LONG_PRESS_HOLD und SINGLE_CLICK) mit einem Zählbaustein zur Erzeugung eines PWM-Signals. Der Zählerwert wird mit 8 multipliziert und als PWM-Wert ausgegeben, was eine fein abgestufte Geschwindigkeitsregelung ermöglicht.