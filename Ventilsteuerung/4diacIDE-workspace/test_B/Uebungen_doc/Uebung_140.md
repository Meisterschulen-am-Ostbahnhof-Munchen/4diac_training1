Hier ist die Dokumentationsseite für die Übung 140 basierend auf den bereitgestellten Daten.

# Uebung_140

![Uebung_140](Uebung_140.png)

* * * * * * * * * *

## Einleitung
Diese Übung befasst sich mit der Zeiterfassung in Steuerungssystemen. Konkret wird der Funktionsbaustein `SYS_ONTIME` implementiert, welcher als Betriebsstundenzähler dient. Ziel ist es, zu verstehen, wie Laufzeiten von Systemen oder Aggregaten gemessen und für weitere Logik (z.B. Wartungsintervalle) bereitgestellt werden können.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Application wird der folgende Funktionsbaustein verwendet:

### Sub-Bausteine: SYS_ONTIME
- **Typ**: `logiBUS::signalprocessing::measurement::SYS_ONTIME`
- **Verwendete interne FBs**:
    - *Keine weiteren internen FBs im bereitgestellten Ausschnitt definiert (Bibliotheksbaustein).*
- **Funktionsweise**:
    Der Baustein `SYS_ONTIME` dient der Messung der kumulierten Einschaltzeit. Er zählt die Zeit, solange ein entsprechendes Eingangssignal aktiv ist, und gibt die summierte Dauer aus. Dies ist essenziell für die Realisierung von Betriebsstundenzählern.

## Programmablauf und Verbindungen

Die Übung besteht aus einem Netzwerk innerhalb einer Sub-Application, in dem eine Instanz des `SYS_ONTIME` Bausteins platziert wurde.

*   **Lernziele**:
    *   Kennenlernen von Bibliotheksbausteinen zur Zeitmessung.
    *   Verständnis für die Erfassung von Betriebsdauern.
*   **Schwierigkeitsgrad**: Einsteiger.
*   **Voraussetzungen**: Grundlegendes Verständnis der IEC 61499 und der Handhabung von Funktionsbausteinen in der 4diac IDE.
*   **Ablauf**:
    *   Der Baustein befindet sich an der Position (x=-1400, y=-400).
    *   In dieser Basis-Konfiguration sind noch keine expliziten Verbindungen zu Eingangs- oder Ausgangssignalen definiert. Um die Übung zu vervollständigen, müssen die Eingänge des `SYS_ONTIME` Bausteins mit einer Logik (z.B. einem "Motor Ein"-Signal) verbunden werden, um die Zählung zu aktivieren.

## Zusammenfassung
Die "Uebung_140" legt den Grundstein für die Implementierung von Wartungs- und Überwachungsfunktionen in Steuerungsapplikationen. Durch die Nutzung des `SYS_ONTIME` Bausteins wird eine präzise Erfassung der Betriebszeiten ermöglicht.