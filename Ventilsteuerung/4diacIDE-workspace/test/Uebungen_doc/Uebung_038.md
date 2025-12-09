# Uebung_038: Lauflicht 8 reine Zeitsteuerung

* * * * * * * * * *

## Einleitung
Diese Übung implementiert ein 8-Kanal-Lauflicht mit reiner Zeitsteuerung. Das System ermöglicht die sequentielle Aktivierung von acht Ausgängen mit unterschiedlichen Zeitintervallen zwischen den Zustandsübergängen.

## Verwendete Funktionsbausteine (FBs)

### Hauptbausteine:
- **DigitalOutput_Q1 bis Q8** (Typ: logiBUS_QX) - Digitale Ausgänge für die Lauflicht-Kanäle
- **DigitalInput_CLK_I1** (Typ: logiBUS_IE) - Start-Eingang mit Tasterfunktion
- **DigitalInput_CLK_I4** (Typ: logiBUS_IE) - Reset-Eingang mit Tasterfunktion  
- **E_TimeOut** (Typ: E_TimeOut) - Zeitsteuerungsbaustein
- **F_SINT_TO_UINT** (Typ: F_SINT_TO_UINT) - Datentyp-Konvertierung
- **Q_NumericValue** (Typ: Q_NumericValue) - Numerische Wertausgabe

### Sub-Bausteine: sequence_T_08_loop
- **Typ**: sequence_T_08_loop
- **Verwendete interne FBs**: E_TimeOut (Adapterverbindung)
- **Funktionsweise**: Steuert die sequentielle Abfolge der 8 Lauflicht-Zustände mit konfigurierbaren Zeitintervallen zwischen den Zustandsübergängen. Verfügt über START_S1 und RESET Ereigniseingänge sowie EO_S1 bis EO_S8 Ereignisausgänge und entsprechende Datenausgänge DO_S1 bis DO_S8.

## Programmablauf und Verbindungen

**Start und Steuerung:**
- I1-Button: Startet die Sequenz ab Zustand S1
- I4-Button: Reset der gesamten Sequenz

**Zeitsteuerung:**
- S1→S2: 200ms
- S2→S3: 100ms  
- S3→S4: 200ms
- S4→S5: 100ms
- S5→S6: 200ms
- S6→S7: 100ms
- S7→S8: 200ms
- S8→S1: 100ms

**Signalfluss:**
- Die Sequenz steuert über EO/DO-Ausgänge direkt die digitalen Ausgänge Q1-Q8
- Der aktuelle Zustand wird über STATE_NR an F_SINT_TO_UINT weitergeleitet
- Der konvertierte Wert wird an Q_NumericValue zur Anzeige übergeben

**Hardware-Anbindung:**
- Alle DigitalOutput-FBs sind mit logiBUS_DO-Schnittstellen verbunden
- Die DigitalInput-FBs nutzen BUTTON_SINGLE_CLICK Ereignisse

## Zusammenfassung
Diese Übung demonstriert eine reine Zeitsteuerung für ein 8-Kanal-Lauflicht mit variablen Zeitintervallen. Sie zeigt die Anwendung von Sequenzsteuerungen, Zeitgebern und der Integration von Ein-/Ausgabebausteinen in einem logiBUS-System. Die unterschiedlichen Zeitintervalle zwischen den Zustandsübergängen ermöglichen komplexere Lauflicht-Muster als einfache gleichmäßige Sequenzen.