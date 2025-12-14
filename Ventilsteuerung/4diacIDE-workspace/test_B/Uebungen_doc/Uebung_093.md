# Uebung_093: Beispiel für E_TABLE

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_TABLE-Funktionsbausteins zur zeitgesteuerten Ereignisausgabe. Das System erzeugt nach einem Tastendruck eine Sequenz von vier Ereignissen zu definierten Zeitpunkten.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Funktionsweise**: Liest den digitalen Eingang I1 ein und erkennt einen einfachen Tastendruck (BUTTON_SINGLE_CLICK)

### E_TABLE
- **Typ**: E_TABLE
- **Parameter**: 
  - DT = [T#0s, T#2s, T#3s, T#4s]
  - N = 4
- **Funktionsweise**: Gibt nach START-Event vier Ereignisse zu den definierten Zeitpunkten aus (sofort, nach 2s, 3s und 4s)

### E_T_FF
- **Typ**: E_T_FF
- **Funktionsweise**: T-Flipflop, der bei jedem CLK-Event seinen Ausgangszustand toggelt

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Steuert den digitalen Ausgang Q1 an

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_TABLE.START
- E_TABLE.EO → E_T_FF.CLK
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Ablauf:**
1. Ein Tastendruck auf I1 löst das IND-Event aus
2. E_TABLE startet und gibt vier Ereignisse aus:
   - Sofort nach dem Klick
   - 2 Sekunden nach dem Klick
   - 3 Sekunden nach dem Klick
   - 4 Sekunden nach dem Klick
3. Jedes EO-Event von E_TABLE toggelt den E_T_FF
4. Der E_T_FF steuert den Digitalausgang Q1
5. Insgesamt wird Q1 viermal getoggelt

**Lernziele:**
- Verständnis des E_TABLE-Bausteins
- Zeitgesteuerte Ereignissequenzen
- Kombination von Event- und Datenverbindungen
- Toggle-Flipflop Funktionalität

**Schwierigkeitsgrad**: Einfach bis Mittel

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung des E_TABLE-Funktionsbausteins zur Erzeugung zeitlich gestaffelter Ereignisse. Nach einem initialen Tastendruck werden vier Events zu genau definierten Zeitpunkten ausgelöst, die einen Ausgangstoggle steuern. Die Gesamtsequenz dauert 9 Sekunden und demonstriert effektiv die Zeitsteuerungsfähigkeiten von 4diac.