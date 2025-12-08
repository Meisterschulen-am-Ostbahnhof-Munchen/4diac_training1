# Uebung_094: Beispiel für E_PERMIT

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_PERMIT-Funktionsbausteins in Kombination mit einem E_T_FF-Baustein. Das Programm realisiert eine Toggle-Funktion, die nur bei aktivierter Freigabe durch einen Eingangssignal zählt.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktion**: Digitaler Eingang für das Freigabesignal

### DigitalInput_CLK_I2
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I2
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktion**: Digitaler Eingang mit Tasterereignis für den Takt

### E_PERMIT
- **Typ**: E_PERMIT
- **Funktion**: Erlaubnisbaustein, der Ereignisse nur bei aktiviertem PERMIT-Signal durchlässt

### E_T_FF
- **Typ**: E_T_FF
- **Funktion**: Toggle-Flipflop, der bei jedem Taktimpuls seinen Ausgangszustand wechselt

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktion**: Digitaler Ausgang zur Anzeige des Toggle-Zustands

## Programmablauf und Verbindungen

Das Programm arbeitet nach folgendem Prinzip:

1. **Ereignisfluss**: 
   - Ein Tasterklick an I2 (BUTTON_SINGLE_CLICK) löst das IND-Ereignis aus
   - Dieses Ereignis wird an E_PERMIT.EI weitergeleitet
   - E_PERMIT leitet das Ereignis nur an E_T_FF.CLK weiter, wenn PERMIT aktiv ist
   - E_T_FF wechselt bei jedem empfangenen Takt seinen Ausgangszustand
   - Das EO-Ereignis von E_T_FF aktiviert den Digitalausgang Q1

2. **Datenfluss**:
   - Der digitale Eingang I1 liefert das PERMIT-Signal für E_PERMIT
   - Der Q-Ausgang von E_T_FF steuert den digitalen Ausgang Q1

**Lernziele**:
- Verständnis des E_PERMIT-Bausteins und seiner Anwendung
- Kombination von Ereignis- und Datenfluss in IEC 61499
- Implementierung einer Freigabefunktion für Ereignisse
- Arbeit mit Toggle-Flipflops

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**: Grundlagen der IEC 61499, Verständnis von Ereignisbausteinen

**Starten der Übung**: Das Programm wird auf einem logiBUS-kompatiblen System ausgeführt. Der Taster an I2 muss gedrückt werden, während I1 aktiv ist, um den Ausgang Q1 zu toggeln.

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung des E_PERMIT-Bausteins zur Steuerung von Ereignisflüssen. Durch die Kombination mit einem Toggle-Flipflop wird demonstriert, wie Ereignisse nur unter bestimmten Bedingungen (hier: aktivierter PERMIT-Eingang) weiterverarbeitet werden können. Die Übung vermittelt grundlegende Konzepte der ereignisgesteuerten Automatisierung nach IEC 61499.