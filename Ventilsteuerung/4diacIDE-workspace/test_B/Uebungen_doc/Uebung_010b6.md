# Uebung_010b6: Toggle Flip-Flop mit IE SoftKey_F1 SK_PRESSED

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops (T-FF) in Verbindung mit einer Softkey-Eingabe. Der Schaltungsaufbau zeigt, wie ein Tastendruck auf die F1-Taste den Zustand eines digitalen Ausgangs umschaltet.

## Verwendete Funktionsbausteine (FBs)

### SoftKey_UP_F1
- **Typ**: Softkey_IE
- **Parameter**:
  - QI = TRUE (Aktivierung)
  - u16ObjId = DefaultPool::SoftKey_F1 (Softkey-Objekt)
  - InputEvent = SoftKeyActivationCode::SK_PRESSED (Ereignis bei Tastendruck)

### E_T_FF
- **Typ**: E_T_FF (Toggle Flip-Flop mit Ereignissteuerung)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (Aktivierung)
  - Output = logiBUS_DO::Output_Q1 (Ausgangskanal)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- SoftKey_UP_F1.IND → E_T_FF.CLK (Tastendruck löst Toggle-Flip-Flop aus)
- E_T_FF.EO → DigitalOutput_Q1.REQ (Flip-Flop-Ausgang triggert Ausgangsanforderung)

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT (Flip-Flop-Zustand wird an digitalen Ausgang übertragen)

**Funktionsweise:**
1. Beim Drücken der F1-Taste wird das IND-Ereignis des Softkey-Bausteins ausgelöst
2. Dieses Ereignis aktiviert den Takt-Eingang (CLK) des Toggle Flip-Flops
3. Der Flip-Flop ändert seinen Ausgangszustand (Q) bei jedem Tastendruck
4. Das EO-Ereignis des Flip-Flops fordert die Aktualisierung des digitalen Ausgangs an
5. Der aktuelle Zustand (Q) wird an den Ausgang Q1 weitergeleitet

**Lernziele:**
- Verständnis von Toggle Flip-Flop Funktionalität
- Umgang mit Softkey-Eingaben in 4diac
- Ereignisgesteuerte Programmabläufe
- Daten- und Ereignisverbindungen zwischen Funktionsbausteinen

**Schwierigkeitsgrad**: Einfach  
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Basiswissen Funktionsbausteine

**Starten der Übung**: Die Übung wird in der 4diac-IDE geladen und auf ein kompatibles Steuerungssystem deployed. Der Ausgang Q1 kann durch Betätigen der F1-Taste getoggelt werden.

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung eines Toggle Flip-Flops, der durch Softkey-Eingaben gesteuert wird. Die Schaltung demonstriert grundlegende Prinzipien der ereignisgesteuerten Programmierung und die Verknüpfung von Eingabeereignissen mit logischen Schaltfunktionen in 4diac.