# Uebung_072b: GBSD auf UT ausgeben, mit Impulsen.

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung von Geschwindigkeits- und Distanzdaten mit Impulsausgaben basierend auf zurückgelegten Distanzen. Das System verarbeitet sowohl bodenbasierte als auch radbasierte Maschinengeschwindigkeiten und erzeugt digitale Ausgangssignale in Abhängigkeit von bestimmten Distanzbereichen.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

- **I_GBSD**: Bodengeschwindigkeitssensor-Interface
- **I_WBSD**: Radgeschwindigkeitssensor-Interface  
- **Q_NumericValue_GBSD**: Ausgabe der bodenbasierten Maschinengeschwindigkeit
- **Q_NumericValue_WBSD**: Ausgabe der radbasierten Maschinengeschwindigkeit
- **Q_NumberVariable_Wheel_based_machine_distance**: Ausgabe der radbasierten Maschinendistanz
- **RangeBasedPulse_Q1-Q4**: Distanzbasierte Impulserzeugung für vier verschiedene Bereiche
- **E_D_FF_Q1-Q4**: D-Flipflops zur Signalverarbeitung
- **DigitalOutput_Q1-Q4**: Digitale Ausgänge für die Impulssignale

### Sub-Bausteine: RangeBasedPulse
- **Typ**: signalprocessing::distance::RangeBasedPulse
- **Parameter**:
  - DIST_OFF: Startdistanz für Impulsaktivierung (0, 1000, 2000, 3000)
  - DIST_HIGH: Impulsdauer bei hohem Pegel (5000)
  - DIST_LOW: Impulsdauer bei niedrigem Pegel (5000)
- **Ereigniseingang**: REQ
- **Ereignisausgang**: CNF
- **Dateneingang**: DIST_IN
- **Datenausgang**: Q
- **Funktionsweise**: Erzeugt Impulse basierend auf eingehenden Distanzwerten. Der Ausgang Q wird aktiviert, wenn die Eingangsdistanz den DIST_OFF-Wert erreicht und für die konfigurierte Dauer aktiv bleibt.

## Programmablauf und Verbindungen

Das Programm verarbeitet zwei unabhängige Geschwindigkeitsquellen:
1. **Bodenbasierte Geschwindigkeit (GBSD)** über I_GBSD
2. **Radbasierte Geschwindigkeit (WBSD)** über I_WBSD

**Datenfluss:**
- Die IND-Ereignisse von I_GBSD triggern gleichzeitig die Ausgabe der Geschwindigkeitswerte und die Distanzverarbeitung
- Die bodenbasierte Distanz (GROUNDBASEDMACHINEDISTANCE) wird an alle vier RangeBasedPulse-Bausteine verteilt
- Jeder RangeBasedPulse ist für einen spezifischen Distanzbereich konfiguriert:
  - Q1: ab 0 Einheiten
  - Q2: ab 1000 Einheiten  
  - Q3: ab 2000 Einheiten
  - Q4: ab 3000 Einheiten

**Signalverarbeitung:**
- Die RangeBasedPulse-Bausteine erzeugen Impulse bei Erreichen ihrer jeweiligen Schwellwerte
- Diese Impulse werden an D-Flipflops (E_D_FF) weitergeleitet
- Die Flipflops stabilisieren die Signale und geben sie an die digitalen Ausgänge weiter

**Lernziele:**
- Verarbeitung von Sensordaten aus verschiedenen Quellen
- Distanzbasierte Steuerung mit konfigurierbaren Schwellwerten
- Verwendung von Flipflops zur Signalstabilisierung
- Parallele Verarbeitung mehrerer Distanzbereiche

**Schwierigkeitsgrad**: Mittel
**Benötigte Vorkenntnisse**: Grundlagen der IEC 61499, Sensor-Datenverarbeitung, digitale Schaltungen

## Zusammenfassung
Diese Übung zeigt ein komplexes System zur Verarbeitung von Geschwindigkeits- und Distanzdaten mit distanzabhängiger Impulserzeugung. Durch die parallele Verarbeitung mehrerer Distanzbereiche und die Verwendung von Flipflops zur Signalstabilisierung werden grundlegende Konzepte der industriellen Automatisierungstechnik praktisch umgesetzt.