# Uebung_020f: DigitalInput_I1 auf DigitalOutput_Q1; E_TP; Impulsformend

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung eines Zeitgeber-Funktionsbausteins (E_TP) zur Steuerung eines digitalen Ausgangs basierend auf einem digitalen Eingangssignal. Der Baustein E_TP erzeugt einen zeitlich begrenzten Impuls, wenn ein Ereignis am Eingang detektiert wird.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktionsweise**: Liest den Zustand des digitalen Eingangs I1 ein und gibt diesen über den Datenausgang IN weiter.

### E_TP
- **Typ**: E_TP
- **Parameter**:
  - PT = T#5s (Zeitbasis: 5 Sekunden)
- **Funktionsweise**: Bei einem Ereignis am REQ-Eingang wird der am IN-Eingang anliegende Wert für die eingestellte Zeitdauer (5 Sekunden) am Q-Ausgang ausgegeben.

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Setzt den digitalen Ausgang Q1 entsprechend dem Wert am OUT-Eingang.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → E_TP.REQ
- E_TP.CNF → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → E_TP.IN
- E_TP.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Bei einer Zustandsänderung am digitalen Eingang I1 wird ein IND-Ereignis ausgelöst
2. Dieses Ereignis triggert den E_TP-Baustein über REQ
3. Der E_TP-Baustein gibt den Eingangswert für genau 5 Sekunden am Q-Ausgang aus
4. Nach Ablauf der Zeit oder bei neuem Trigger-Ereignis wird ein CNF-Ereignis generiert
5. Das CNF-Ereignis aktiviert den DigitalOutput_Q1 Baustein, der den Ausgang Q1 entsprechend setzt

**Lernziele:**
- Verwendung des E_TP Zeitgeber-Bausteins
- Verknüpfung von digitalen Ein- und Ausgängen
- Impulsformung und Zeitsteuerung
- Ereignisgesteuerte Programmabläufe

**Schwierigkeitsgrad**: Einfach
**Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Ereignis- und Datenverbindungen

## Zusammenfassung
Diese Übung zeigt eine grundlegende Anwendung des E_TP-Funktionsbausteins zur Erzeugung zeitlich begrenzter Impulse. Der Baustein wandelt ein Eingangssignal in einen 5-Sekunden-Impuls um, der dann einen digitalen Ausgang steuert. Dieses Muster ist typisch für viele Steuerungsaufgaben, bei denen Signale für eine bestimmte Zeitdauer aktiv sein müssen.