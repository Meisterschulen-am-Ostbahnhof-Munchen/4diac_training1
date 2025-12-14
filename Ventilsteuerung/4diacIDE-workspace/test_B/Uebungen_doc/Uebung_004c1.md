# Uebung_004c1: Toggle Flip-Flop mit IE mit BUTTON_DOUBLE_CLICK

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Implementierung eines Toggle Flip-Flops mit spezieller Ereignisauslösung. Der Schwerpunkt liegt auf der Verwendung eines Doppelklick-Ereignisses als Taktgeber für den Flip-Flop.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_DOUBLE_CLICK
- **Funktionsweise**: Überwacht den digitalen Eingang I1 und erkennt speziell Doppelklick-Ereignisse

### E_T_FF
- **Typ**: E_T_FF (Toggle Flip-Flop)
- **Funktionsweise**: Schaltet seinen Ausgangszustand bei jedem eingehenden Taktimpuls um

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Steuert den digitalen Ausgang Q1 basierend auf dem Eingangssignal

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_T_FF.CLK
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Ein Doppelklick auf den physischen Button an Eingang I1 löst ein IND-Ereignis aus
2. Dieses Ereignis dient als Takt (CLK) für den Toggle Flip-Flop
3. Der E_T_FF wechselt seinen Zustand (Q) bei jedem Taktimpuls
4. Das Ausgangssignal wird über EO an den Digitalausgang Q1 gesendet
5. Der Ausgang Q1 schaltet bei jedem Doppelklick-Ereignis um

**Lernziele:**
- Verständnis von Toggle Flip-Flops
- Umgang mit speziellen Eingabeereignissen (Doppelklick)
- Verbindung von Eingabe-, Verarbeitungs- und Ausgabebausteinen
- Ereignisgesteuerte Programmierung

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis digitaler Ein- und Ausgänge

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung eines Toggle Flip-Flops, der durch Doppelklick-Ereignisse gesteuert wird. Die Kombination aus ereignisbasierter Eingabeverarbeitung und zustandsgesteuerter Logik demonstriert grundlegende Prinzipien der Automatisierungstechnik. Die Übung eignet sich ideal zum Einstieg in die ereignisgesteuerte Programmierung mit 4diac.