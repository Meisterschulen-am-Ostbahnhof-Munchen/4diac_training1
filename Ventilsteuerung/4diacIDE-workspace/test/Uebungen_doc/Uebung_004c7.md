# Uebung_004c7: Toggle Flip-Flop mit IE mit BUTTON_PRESS_END

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle-Flip-Flops mit einem speziellen Eingabeereignis. Das System erkennt einen langen Tastendruck und schaltet einen Ausgang bei jedem Erkennen dieses Ereignisses um.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE2
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Input = logiBUS_DI::Input_I1 (verwendet Eingang I1)
  - InputEvent = logiBUS_DI_Events::BUTTON_LONG_PRESS_START (erkennt langen Tastendruck)
  - arg = 3000 (3 Sekunden Schwellwert)

### E_T_FF
- **Typ**: E_T_FF (Toggle-Flip-Flop)
- **Funktionsweise**: Schaltet den Ausgang Q bei jedem eingehenden Takt-Ereignis um

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (steuert Ausgang Q1)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_T_FF.CLK (Takt-Ereignis)
- E_T_FF.EO → DigitalOutput_Q1.REQ (Ausgabeanforderung)

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT (Ausgangswert)

**Ablauf:**
1. Ein langer Tastendruck (3 Sekunden) auf Eingang I1 wird erkannt
2. Das Ereignis BUTTON_LONG_PRESS_START löst den Toggle-Flip-Flop aus
3. Der Ausgang Q1 schaltet bei jedem Ereignis seinen Zustand um
4. Der Kommentar "3s drücken" weist auf die benötigte Druckdauer hin

**Lernziele:**
- Verständnis von Toggle-Flip-Flop-Funktionalität
- Umgang mit speziellen Eingabeereignissen (BUTTON_LONG_PRESS_START)
- Parametrierung von Zeitverzögerungen in Eingabebausteinen
- Ereignisgesteuerte Programmabläufe

**Schwierigkeitsgrad**: Einfach bis mittel

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Ereignisverbindungen

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung eines Toggle-Flip-Flops mit ereignisgesteuerter Auslösung. Durch die Verwendung des BUTTON_LONG_PRESS_START-Ereignisses wird ein zuverlässiges Umschalten des Ausgangs bei langem Tastendruck erreicht. Die Übung vermittelt wichtige Konzepte der ereignisbasierten Steuerung und parametrierbarer Eingabebausteine.