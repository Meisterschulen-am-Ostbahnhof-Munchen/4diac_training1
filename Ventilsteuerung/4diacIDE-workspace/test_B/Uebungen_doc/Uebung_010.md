# Uebung_010: SoftKey_F1 auf DigitalOutput_Q1

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verknüpfung zwischen einer Softkey-Eingabe und einem digitalen Ausgang. Die Übung zeigt, wie ein Tastendruck auf eine virtuelle Taste (SoftKey_F1) direkt einen digitalen Ausgang (DigitalOutput_Q1) steuert.

## Verwendete Funktionsbausteine (FBs)

### SoftKey_F1
- **Typ**: Softkey_IX
- **Parameter**:
  - QI = TRUE (Qualified Input - Aktivierung)
  - u16ObjId = DefaultPool::SoftKey_F1 (Objekt-ID für Softkey)
- **Ereignisausgang**: IND (Indication - Signalisiert Tastendruck)
- **Dateneingang**: IN (Eingangsdaten)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (Qualified Input - Aktivierung)
  - Output = logiBUS_DO::Output_Q1 (Zugewiesener physikalischer Ausgang)
- **Ereigniseingang**: REQ (Request - Anforderung zur Ausgabe)
- **Datenausgang**: OUT (Ausgangsdaten)

## Programmablauf und Verbindungen

**Ereignisverbindung:**
- SoftKey_F1.IND → DigitalOutput_Q1.REQ

**Datenverbindung:**
- SoftKey_F1.IN → DigitalOutput_Q1.OUT

**Ablauf:**
1. Beim Drücken der Softkey-F1-Taste wird das IND-Ereignis ausgelöst
2. Das IND-Ereignis triggert über die Ereignisverbindung den REQ-Eingang des Digitalausgangs
3. Gleichzeitig wird der Datenwert von SoftKey_F1.IN an DigitalOutput_Q1.OUT übertragen
4. Der digitale Ausgang Q1 schaltet entsprechend dem empfangenen Signal

**Lernziele:**
- Grundlegende Event- und Datenverbindungen zwischen FBs
- Steuerung digitaler Ausgänge durch Softkey-Eingaben
- Verständnis der Parameterkonfiguration für Ein- und Ausgänge

**Schwierigkeitsgrad**: Einfach (Anfängerübung)

**Benötigte Vorkenntnisse:**
- Grundlagen der 4diac-IDE
- Verständnis von Funktionsbausteinen und deren Verbindungen

## Zusammenfassung
Diese Übung vermittelt die grundlegenden Prinzipien der Signalverarbeitung in 4diac. Sie zeigt anschaulich, wie eine Benutzereingabe (Softkey) direkt mit einer Aktorik (digitaler Ausgang) verbunden werden kann. Die einfache Struktur mit nur zwei Funktionsbausteinen und klaren Verbindungen macht diese Übung ideal für den Einstieg in die Automatisierungsprogrammierung mit IEC 61499.