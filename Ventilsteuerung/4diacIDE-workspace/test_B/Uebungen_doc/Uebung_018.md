# Uebung_018: Control Audio Signal und Delay

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Steuerung von Audiosignalen mit Verzögerung. Es werden zwei verschiedene Audiosignale nacheinander abgespielt, wobei das zweite Signal nach einer definierten Verzögerung nach dem ersten Signal aktiviert wird.

## Verwendete Funktionsbausteine (FBs)

### SoftKey_UP_F1
- **Typ**: Softkey_IE
- **Parameter**:
  - QI = TRUE
  - u16ObjId = DefaultPool::SoftKey_F1
  - InputEvent = SoftKeyActivationCode::SK_RELEASED

### Q_CtrlAudioSignal_0
- **Typ**: Q_CtrlAudioSignal
- **Parameter**:
  - u8NumOfRepit = 1
  - u16Frequency = 440
  - u16OnTimeMs = 150
  - u16OffTimeMs = 0

### Q_CtrlAudioSignal_1
- **Typ**: Q_CtrlAudioSignal
- **Parameter**:
  - u8NumOfRepit = 1
  - u16Frequency = 880
  - u16OnTimeMs = 150
  - u16OffTimeMs = 0

### E_DELAY
- **Typ**: E_DELAY
- **Parameter**:
  - DT = T#250ms

## Programmablauf und Verbindungen

Der Programmablauf beginnt mit der Betätigung der Softtaste F1 (SoftKey_UP_F1). Beim Loslassen der Taste (SK_RELEASED) wird ein Ereignis an Q_CtrlAudioSignal_0 gesendet, welches ein Audiosignal mit 440 Hz Frequenz für 150 ms abspielt.

Nach Abschluss des ersten Audiosignals (CNF-Ausgang) wird der Verzögerungsbaustein E_DELAY gestartet, der eine 250 ms Verzögerung einfügt. Nach Ablauf dieser Verzögerung wird das zweite Audiosignal Q_CtrlAudioSignal_1 aktiviert, welches ein Signal mit 880 Hz Frequenz für 150 ms abspielt.

**Ereignisverbindungen:**
- SoftKey_UP_F1.IND → Q_CtrlAudioSignal_0.REQ
- Q_CtrlAudioSignal_0.CNF → E_DELAY.START
- E_DELAY.EO → Q_CtrlAudioSignal_1.REQ

**Lernziele:**
- Verwendung von Softkey-Inputs
- Steuerung von Audiosignalen
- Implementierung von Zeitverzögerungen
- Ereignisgesteuerte Programmabläufe

**Schwierigkeitsgrad**: Einfach bis Mittel

**Vorkenntnisse**: Grundkenntnisse in 4diac IDE und Funktionsbausteinen

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung zur sequenziellen Steuerung von Audiosignalen mit integrierter Zeitverzögerung. Die Kombination aus Benutzereingabe, Signalgenerierung und Zeitsteuerung demonstriert grundlegende Konzepte der ereignisgesteuerten Automatisierungstechnik.