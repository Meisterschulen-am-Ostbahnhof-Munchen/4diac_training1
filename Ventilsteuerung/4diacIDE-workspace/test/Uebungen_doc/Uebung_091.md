# Uebung_091: Beispiel für E_TRAIN

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_TRAIN-Funktionsbausteins zur Erzeugung einer Ereignisfolge. Das System erzeugt nach einem Tasterdruck eine definierte Anzahl von Ereignissen mit festgelegten Zeitintervallen.

## Verwendete Funktionsbausteine (FBs)

### E_TRAIN
- **Typ**: E_TRAIN
- **Parameter**: 
  - DT = T#1s (Zeitintervall von 1 Sekunde)
  - N = 8 (Anzahl der Ereignisse)

### E_T_FF
- **Typ**: E_T_FF (Toggle-Flipflop)

### logiBUS_IE
- **Typ**: logiBUS_IE (Digitaler Eingang)
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### logiBUS_QX
- **Typ**: logiBUS_QX (Digitaler Ausgang)
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_TRAIN.START
- E_TRAIN.EO → E_T_FF.CLK
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Ein Tastendruck auf Input_I1 löst über den DigitalInput_CLK_I1-Baustein ein IND-Ereignis aus
2. Dieses Ereignis startet den E_TRAIN-Baustein
3. E_TRAIN generiert 8 Ereignisse im Abstand von je 1 Sekunde
4. Jedes E_TRAIN-Ausgangsereignis (EO) triggert den E_T_FF-Baustein
5. E_T_FF toggelt seinen Ausgang Q bei jedem Ereignis
6. Der Ausgangswert wird über DigitalOutput_Q1 an die physische Ausgabe Q1 gesendet

**Lernziele:**
- Verständnis des E_TRAIN-Bausteins und seiner Parameter
- Umgang mit zeitgesteuerten Ereignisfolgen
- Kombination von E_TRAIN mit einem Toggle-Flipflop
- Ansteuerung digitaler Ein- und Ausgänge

**Schwierigkeitsgrad**: Einfach bis mittel

**Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Ereignis- und Datenverbindungen

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung des E_TRAIN-Bausteins zur Erzeugung einer zeitlich gesteuerten Ereignisfolge. Nach einem Tasterdruck werden 8 Ereignisse im Sekundentakt generiert, die einen Ausgangstoggle steuern. Die Übung vermittelt wichtige Konzepte der Ereignisverarbeitung und Zeitsteuerung in IEC 61499-Systemen.