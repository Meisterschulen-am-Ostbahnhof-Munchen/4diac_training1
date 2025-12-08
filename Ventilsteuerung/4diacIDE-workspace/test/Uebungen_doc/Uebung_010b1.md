# Uebung_010b1: AuxFunction2_X1 auf DigitalOutput_Q1

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verbindung zwischen einem Hilfsfunktionsbaustein und einem digitalen Ausgang. Die Anwendung zeigt, wie ein Auxiliary-Funktionsbaustein mit einem logiBUS-Ausgabemodul kommuniziert.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: AuxFunction2_X1
- **Typ**: Aux_IX
- **Verwendete interne FBs**: Keine internen FBs
- **Funktionsweise**: Der Baustein dient als Hilfsfunktion mit einem Indikator-Ausgang (IND) und einem Datenausgang (IN). Bei Aktivierung sendet er ein Ereignis und die entsprechenden Daten an den verbundenen Ausgangsbaustein.

### Sub-Bausteine: DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Verwendete interne FBs**: Keine internen FBs
- **Funktionsweise**: Dieser Baustein steuert einen physischen digitalen Ausgang des logiBUS-Systems. Er empfängt Anforderungen (REQ) und Daten (OUT) von vorgeschalteten Bausteinen und setzt diese auf den konfigurierten Ausgang um.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- AuxFunction2_X1.IND → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- AuxFunction2_X1.IN → DigitalOutput_Q1.OUT

**Parameterkonfiguration:**
- DigitalOutput_Q1:
  - QI = TRUE (Qualified Input aktiviert)
  - Output = logiBUS_DO::Output_Q1 (Zielausgang definiert)
- AuxFunction2_X1:
  - QI = TRUE (Qualified Input aktiviert)
  - u16ObjId = DefaultPool::AuxFunction2_X1 (Objekt-ID für die Hilfsfunktion)

**Lernziele:**
- Grundlegende Verbindung von Funktionsbausteinen in 4diac-IDE
- Konfiguration von logiBUS-Ausgabemodulen
- Verständnis der Ereignis- und Datenflusssteuerung
- Arbeit mit Hilfsfunktionsbausteinen (Auxiliary Functions)

**Schwierigkeitsgrad:** Einsteiger

**Benötigte Vorkenntnisse:**
- Grundkenntnisse der 4diac-IDE Oberfläche
- Verständnis von Ereignisgesteuerten Funktionsbausteinen (FB) nach IEC 61499
- Basiswissen über logiBUS-Systeme

**Starten der Übung:**
Die Übung kann direkt in der 4diac-IDE geladen und auf einem kompatiblen logiBUS-System ausgeführt werden. Die Parameter sind bereits vorkonfiguriert.

## Zusammenfassung
Diese einfache Übung vermittelt die grundlegenden Prinzipien der Verbindung von Funktionsbausteinen in 4diac-IDE. Sie zeigt, wie ein Hilfsfunktionsbaustein mit einem physischen Ausgabemodul interagiert und demonstriert den standardmäßigen Daten- und Ereignisfluss zwischen Bausteinen. Die Übung bildet eine wichtige Basis für komplexere Automatisierungsanwendungen.