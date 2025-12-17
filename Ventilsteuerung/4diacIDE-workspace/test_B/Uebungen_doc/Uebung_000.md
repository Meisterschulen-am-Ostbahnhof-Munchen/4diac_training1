Hier ist die Dokumentationsseite für die Übung `Uebung_000` basierend auf den bereitgestellten Daten.

# Uebung_000

![Uebung_000](Uebung_000.png)

* * * * * * * * * *

## Einleitung

Die Sub-Applikation **Uebung_000** dient als einfaches Einstiegsbeispiel in die Verwendung von arithmetischen Grundfunktionen innerhalb der 4diac IDE. Der Zweck dieser Übung ist die Demonstration einer Addition zweier Integer-Konstanten mithilfe eines Standard-IEC-61131-3-Bausteins. Es handelt sich um eine grundlegende Konfiguration ohne externe Schnittstellen.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung wird im internen Netzwerk der Sub-Applikation ein zentraler Funktionsbaustein verwendet, um die Berechnungslogik auszuführen.

### Sub-Bausteine: Uebung_000 Netzwerk

- **Typ**: SubAppType (Sub-Applikation)
- **Verwendete interne FBs**:
    - **Bausteinname**: ADD_2
        - **Typ**: iec61131::arithmetic::ADD_2
        - **Parameter**: 
            - IN1 = INT#5
            - IN2 = INT#3
        - **Ereignisausgang/-eingang**: *Keine expliziten Ereignisverbindungen in diesem Snippet definiert (Datenfluss-Logik).*
        - **Datenausgang/-eingang**: 
            - IN1 (Eingang): Integer-Wert 5
            - IN2 (Eingang): Integer-Wert 3
            - OUT (Ausgang): Ergebnis der Addition (implizit)
- **Funktionsweise**: 
    Der Baustein `ADD_2` führt eine mathematische Addition durch. Er nimmt die an den Eingängen `IN1` und `IN2` definierten Werte entgegen und summiert diese.

## Programmablauf und Verbindungen

Der Programmablauf in dieser Übung ist statisch und dient primär der Veranschaulichung der Parameterisierung von Bausteinen.

1.  **Initialisierung**: Die Übung verwendet fest kodierte Parameterwerte direkt am Baustein.
2.  **Verarbeitung**: Der Funktionsbaustein `ADD_2` erhält den Wert `5` am Eingang `IN1` und den Wert `3` am Eingang `IN2`.
3.  **Ergebnis**: Der Baustein addiert diese beiden Ganzzahlen. Das mathematische Ergebnis dieser Operation ist `8`.

Da keine externen Ein- oder Ausgänge in der `SubAppInterfaceList` definiert sind, ist diese Logik in sich geschlossen. Es werden keine Verbindungen (Connections) zu anderen Bausteinen gezogen; die Werte werden direkt über die Parametereingänge des Bausteins injiziert.

**Lernziele:**
- Einfügen eines Funktionsbausteins aus der Bibliothek.
- Setzen von festen Werten (Konstanten) an Bausteineingängen.
- Verständnis des `ADD` Bausteins.

## Zusammenfassung

Die `Uebung_000` ist eine minimalistische Darstellung einer Additionsaufgabe. Sie zeigt, wie der Baustein `ADD_2` konfiguriert wird, um die Festwerte 5 und 3 zu addieren. Dies bildet die Grundlage für komplexere arithmetische Operationen und Datenverarbeitungen in 4diac.