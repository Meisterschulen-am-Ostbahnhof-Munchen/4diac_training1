# Uebung_010a4: SoftKey_F1 auf DigitalOutput_Q1 (Datapanel)

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verknüpfung zwischen einem Softkey-Eingang und einem digitalen Ausgang in der 4diac-IDE. Die Anwendung zeigt, wie ein Tastendruck auf einer virtuellen Softkey-Taste direkt einen digitalen Ausgang steuert.

## Verwendete Funktionsbausteine (FBs)

### SoftKey_F1
- **Typ**: Softkey_IX
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - u16ObjId = DefaultPool::SoftKey_F1 (Objekt-ID für Softkey F1)
- **Ereignisausgang**: IND (Indication - zeigt Tastendruck an)
- **Dateneingang**: IN (Eingangsdaten)

### DigitalOutput_Q1
- **Typ**: DataPanel_MI_QX
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - u8SAMember = MI::MI_00 (SA-Mitgliedsnummer)
  - Output = DataPanel_MI_DO::DigitalOutput_1A (Ausgangskonfiguration)
- **Ereigniseingang**: REQ (Request - Auslöser für Ausgangsaktivierung)
- **Datenausgang**: OUT (Ausgangsdaten)

## Programmablauf und Verbindungen

**Ereignisverbindung:**
- SoftKey_F1.IND → DigitalOutput_Q1.REQ

**Datenverbindung:**
- SoftKey_F1.IN → DigitalOutput_Q1.OUT

**Ablauf:**
1. Beim Drücken der Softkey-Taste F1 wird das IND-Ereignis ausgelöst
2. Das IND-Ereignis aktiviert über REQ den digitalen Ausgang Q1
3. Gleichzeitig werden die Daten von SoftKey_F1.IN an DigitalOutput_Q1.OUT übertragen
4. Der digitale Ausgang Q1 wird entsprechend dem empfangenen Signal geschaltet

**Schwierigkeitsgrad:** Einfach (Anfängerübung)
**Benötigte Vorkenntnisse:** Grundlagen der 4diac-IDE, Verständnis von Ereignis- und Datenverbindungen
**Start der Übung:** Die Übung wird durch Drücken der F1-Taste im DataPanel gestartet

## Zusammenfassung
Diese Übung vermittelt die grundlegende Funktionsweise von Ereignis- und Datenverbindungen in 4diac-IDE. Sie zeigt, wie einfache Steuerungsaufgaben durch Verknüpfung von Eingangs- und Ausgangsbausteinen realisiert werden können. Die Übung dient als Basis für komplexere Steuerungsanwendungen und demonstriert das Prinzip der ereignisgesteuerten Automatisierung.