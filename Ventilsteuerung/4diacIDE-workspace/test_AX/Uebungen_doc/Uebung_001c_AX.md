# Uebung_001c_AX: DigitalInput_I1 auf DigitalOutput_Q1 --&gt; Eingang abfragen bei Boot.

* * * * * * * * * *
## Einleitung
Diese Übung demonstriert eine grundlegende Funktion der SPS-Programmierung mit 4diac: das Lesen eines digitalen Eingangs (`Input_I1`) und das Steuern eines digitalen Ausgangs (`Output_Q1`). Die besondere Herausforderung dieser Übung besteht darin, den Zustand des Eingangs direkt beim Booten des Systems abzufragen und auf den Ausgang zu übertragen. Dies ist eine elementare Aufgabe in der Automatisierungstechnik, um Sensordaten zu verarbeiten und Aktoren anzusteuern.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: Uebung_001c_AX
- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **Bausteinname**: DigitalInput_I1
        - **Typ**: `logiBUS::io::DI::logiBUS_IXA` (Importiert aus `logiBUS::io::DI::logiBUS_DI::Input_I1`)
        - **Parameter**:
            - `QI = TRUE` (Quality Input – Der Baustein ist aktiviert.)
            - `Input = Input_I1` (Der physische digitale Eingang, der abgefragt wird.)
        - **Ereignisausgang/-eingang**:
            - Ereignisausgang: `INITO` (Initialisation Output – Wird ausgelöst, nachdem der Baustein initialisiert wurde.)
            - Ereigniseingang: `REQ` (Request – Fordert den Baustein auf, den Eingangswert zu lesen.)
        - **Datenausgang/-eingang**:
            - Datenausgang: `IN` (Trägt den aktuell gelesenen Zustand des digitalen Eingangs.)
    - **Bausteinname**: DigitalOutput_Q1
        - **Typ**: `logiBUS::io::DQ::logiBUS_QXA` (Importiert aus `logiBUS::io::DQ::logiBUS_DO::Output_Q1`)
        - **Parameter**:
            - `QI = TRUE` (Quality Input – Der Baustein ist aktiviert.)
            - `Output = Output_Q1` (Der physische digitale Ausgang, der gesteuert wird.)
        - **Ereignisausgang/-eingang**: (Keine direkten Ereignisverbindungen als Quelle oder Ziel für diesen Baustein im Netzwerk vorhanden.)
        - **Datenausgang/-eingang**:
            - Dateneingang: `OUT` (Nimmt den booleschen Wert entgegen, der den Zustand des digitalen Ausgangs setzt.)
- **Funktionsweise**: Dieser Sub-Baustein (`Uebung_001c_AX`) ist so konfiguriert, dass er nach dem Start des 4diac-Applikationssystems den Zustand eines digitalen Eingangs (Input_I1) einmalig liest und diesen Zustand direkt auf einen digitalen Ausgang (Output_Q1) überträgt.

## Programmablauf und Verbindungen
Die Übung `Uebung_001c_AX` implementiert eine einfache, aber effektive Logik zur I/O-Steuerung:

**Ereignisverbindungen:**
*   **`DigitalInput_I1.INITO` nach `DigitalInput_I1.REQ`**: Diese Verbindung ist ein Selbst-Trigger. Nach der Initialisierung des Funktionsbausteins `DigitalInput_I1` (z.B. beim Start der 4diac-Laufzeitumgebung) sendet dieser ein `INITO`-Ereignis an seinen eigenen `REQ`-Eingang. Dies veranlasst den Baustein, den physischen Eingang `Input_I1` einmalig abzufragen und dessen Wert bereitzustellen.

**Daten- und Adapterverbindungen:**
*   **`DigitalInput_I1.IN` nach `DigitalOutput_Q1.OUT`**: Der vom `DigitalInput_I1`-Baustein gelesene boolesche Zustand (Datenausgang `IN`) wird direkt mit dem Dateneingang `OUT` des `DigitalOutput_Q1`-Bausteins verbunden. Das bedeutet, dass der Zustand von `Input_I1` unmittelbar auf den digitalen Ausgang `Output_Q1` übertragen wird.

**Gesamtfunktionalität:**
Die Übung sorgt dafür, dass der digitale Ausgang `Output_Q1` den gleichen Zustand annimmt wie der digitale Eingang `Input_I1`, und zwar zum Zeitpunkt des Systemstarts. Ist `Input_I1` zu diesem Zeitpunkt auf `TRUE` (hoch), wird auch `Output_Q1` auf `TRUE` gesetzt. Ist `Input_I1` auf `FALSE` (niedrig), wird `Output_Q1` auf `FALSE` gesetzt.

**Lernziele:**
*   Verständnis der Grundprinzipien der digitalen Eingangs- und Ausgangssteuerung.
*   Kennenlernen der Funktionsweise von Standard-I/O-Funktionsbausteinen in 4diac (z.B. `logiBUS_IXA` und `logiBUS_QXA`).
*   Erkennen der Bedeutung von Ereignisverbindungen zur Steuerung des Programmflusses, insbesondere des `INITO`-Events.
*   Implementierung einfacher Datenflüsse zwischen Funktionsbausteinen.

**Schwierigkeitsgrad:** Leicht

**Benötigte Vorkenntnisse:**
*   Grundlagen der digitalen Elektronik (HIGH/LOW-Zustände).
*   Grundkenntnisse der 4diac-IDE und des Konzepts von Funktionsbausteinen.

**Starten der Übung:**
1.  Importieren Sie die bereitgestellte `.fbt`- oder `.xml`-Datei in Ihre 4diac-IDE.
2.  Erstellen Sie eine Anwendung, die diesen `Uebung_001c_AX`-SubAppType verwendet.
3.  Konfigurieren Sie die entsprechende 4diac-Laufzeitumgebung auf einem geeigneten Gerät (z.B. Raspberry Pi mit logiBUS-Erweiterung), das physische digitale Eingänge und Ausgänge bereitstellt, die als `Input_I1` und `Output_Q1` gemappt sind.
4.  Laden Sie die Anwendung auf die Laufzeitumgebung herunter und starten Sie diese.
5.  Beobachten Sie das Verhalten von `Output_Q1` in Abhängigkeit von `Input_I1` direkt nach dem Start des Systems.

## Zusammenfassung
`Uebung_001c_AX` ist eine Einführung in die direkte digitale I/O-Steuerung mit 4diac. Sie zeigt, wie ein digitaler Eingang gelesen und sein Zustand auf einen digitalen Ausgang übertragen wird, wobei der Abfragevorgang durch das Initialisierungsereignis des Eingangsmessbausteins ausgelöst wird. Dies ist eine grundlegende Fähigkeit für die Entwicklung von Automatisierungsanwendungen.