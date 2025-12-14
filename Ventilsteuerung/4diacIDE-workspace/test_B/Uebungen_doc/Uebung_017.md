# Uebung_017: Control Audio Signal

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Steuerung eines Audiosignals über eine Softkey-Eingabe. Bei Betätigung der definierten Taste wird ein Tonsignal mit spezifischen Parametern ausgelöst.

## Verwendete Funktionsbausteine (FBs)

### SoftKey_UP_F1
- **Typ**: Softkey_IE
- **Parameter**:
  - QI = TRUE
  - u16ObjId = DefaultPool::SoftKey_F1
  - InputEvent = SoftKeyActivationCode::SK_RELEASED

### Q_CtrlAudioSignal
- **Typ**: Q_CtrlAudioSignal
- **Parameter**:
  - u8NumOfRepit = 1 (Anzahl der Wiederholungen)
  - u16Frequency = 440 (Frequenz in Hz)
  - u16OnTimeMs = 150 (Einschaltdauer in Millisekunden)
  - u16OffTimeMs = 0 (Ausschaltdauer in Millisekunden)

## Programmablauf und Verbindungen

Die Übung verwendet folgende Verbindungen:

- **Ereignisverbindung**: SoftKey_UP_F1.IND → Q_CtrlAudioSignal.REQ

**Programmablauf**:
1. Beim Loslassen der F1-Taste (SoftKey_F1) wird das IND-Ereignis des SoftKey_IE-Bausteins ausgelöst
2. Dieses Ereignis triggert den Q_CtrlAudioSignal-Baustein über dessen REQ-Eingang
3. Der Audio-Controller erzeugt ein Tonsignal mit 440 Hz für 150 Millisekunden
4. Das Signal wird einmalig abgespielt (keine Wiederholungen)

**Lernziele**:
- Verwendung von Softkey-Input-Bausteinen
- Konfiguration von Audio-Signal-Steuerung
- Ereignisgesteuerte Programmabläufe
- Parameterkonfiguration für Tonerzeugung

**Schwierigkeitsgrad**: Einfach

**Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Ereignisverbindungen

## Zusammenfassung
Diese Übung zeigt eine einfache Implementierung zur Steuerung eines Audiosignals durch Tastendruck. Sie vermittelt grundlegende Konzepte der ereignisgesteuerten Programmierung und der Parameterkonfiguration für spezifische Hardware-Funktionalitäten in 4diac.