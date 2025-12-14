# Uebung_079: alle TECU FBs

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung verschiedener TECU-Funktionsbausteine in einer 4diac-IDE Anwendung. Die Übung zeigt die Integration von Sensor- und Aktorbausteinen in einem Steuerungssystem.

## Verwendete Funktionsbausteine (FBs)

Die Übung verwendet folgende Funktionsbausteine:

- **I_GBSD** - Greifer-Basis-Sensordiagnose
- **I_VDS** - Vertikal-Dreh-Sensor
- **I_WBSD** - Werkstück-Basis-Sensordiagnose  
- **I_MSS** - Material-Sortier-Sensor
- **I_FHS** - Förderband-Horizontal-Steuerung
- **I_FPTO** - Förderband-Positionier-Tor-Steuerung
- **I_RHS** - Roboter-Hand-Steuerung
- **I_RPTO** - Roboter-Positionier-Tor-Steuerung
- **COGSOGRapidUpdate** - COGS-OG Rapid Update Baustein

## Programmablauf und Verbindungen

Alle Funktionsbausteine sind mit dem Parameter **QI = TRUE** initialisiert, was eine sofortige Aktivierung der Bausteine beim Programmstart gewährleistet. Die Bausteine sind in einer typischen industriellen Automatisierungsstruktur angeordnet:

- **Sensorbausteine** (I_GBSD, I_VDS, I_WBSD, I_MSS) sind auf der linken Seite positioniert
- **Aktorbausteine** (I_FHS, I_FPTO, I_RHS, I_RPTO) befinden sich in der mittleren Position
- **Steuerungsbaustein** (COGSOGRapidUpdate) ist auf der rechten Seite platziert

Die räumliche Anordnung spiegelt den typischen Signalfluss von Sensoren über die Steuerung zu den Aktoren wider.

## Zusammenfassung
Diese Übung vermittelt grundlegende Kenntnisse in der Integration verschiedener TECU-Funktionsbausteine in einem 4diac-System. Sie zeigt die typische Struktur einer Automatisierungsanwendung mit Sensorik, Aktorik und Steuerungskomponenten und demonstriert die Initialisierung von Bausteinen mit Aktivierungsparametern.