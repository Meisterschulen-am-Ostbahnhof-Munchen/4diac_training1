Hier ist die Dokumentationsseite basierend auf den bereitgestellten Informationen:

# Uebung_006a3_sub

![Uebung_006a3_sub](Uebung_006a3_sub.png)

* * * * * * * * * *

## Einleitung
Diese Dokumentation beschreibt die Sub-Applikation `Uebung_006a3_sub`. Dieser Baustein implementiert eine Umschaltlogik (Toggle), die über ein Freigabesignal gesteuert wird. Er sorgt dafür, dass zwei Ausgänge (`Rechts` und `Links`) stets entgegengesetzte Zustände haben und bei Aktivierung ihren Zustand wechseln.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden verschiedene Standard-Bibliotheksbausteine zu einer Logikeinheit verschaltet.

### Sub-Bausteine: Uebung_006a3_sub
- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **E_SWITCH**: `iec61499::events::E_SWITCH`
        - **Beschreibung**: Dient als Ereignisweiche basierend auf einem booleschen Dateneingang.
        - **Dateneingang**: G = DI (Externer Eingang)
        - **Ereigniseingang**: EI (Externer Eingang)
    - **E_T_FF**: `iec61499::events::E_T_FF`
        - **Beschreibung**: Ein Toggle-Flip-Flop, das seinen Ausgangszustand bei jedem Ereignis am CLK-Eingang wechselt.
        - **Ereigniseingang**: CLK (verbunden mit E_SWITCH.EO1)
        - **Datenausgang**: Q (verbunden mit Ausgang `Rechts` und F_NOT)
    - **F_NOT**: `iec61131::bitwiseOperators::F_NOT`
        - **Beschreibung**: Führt eine bitweise Negation durch (Invertierung).
        - **Dateneingang**: IN (verbunden mit E_T_FF.Q)
        - **Datenausgang**: OUT (verbunden mit Ausgang `Links`)

- **Funktionsweise**:
    Der Baustein empfängt ein Ereignis `EI` und einen Datenwert `DI`. Ist `DI` aktiv (TRUE), wird das Ereignis an das Flip-Flop weitergeleitet, welches den Zustand von `Rechts` umschaltet. Gleichzeitig wird dieses Signal invertiert an `Links` ausgegeben, sodass `Rechts` und `Links` immer komplementär sind.

## Programmablauf und Verbindungen

Der interne Ablauf der Sub-Applikation gestaltet sich wie folgt:

1.  **Eingangsverarbeitung (E_SWITCH)**:
    *   Das externe Ereignis `EI` triggert den Baustein `E_SWITCH`.
    *   Dieser prüft den externen Dateneingang `DI`.
    *   Nur wenn `DI` den Wert `TRUE` hat, wird das Ereignis über den Ausgang `EO1` weitergeleitet. Dies fungiert als "Enable"- oder Freigabe-Schaltung.

2.  **Zustandswechsel (E_T_FF)**:
    *   Das Signal von `E_SWITCH.EO1` erreicht den Takteingang (`CLK`) des Toggle-Flip-Flops `E_T_FF`.
    *   Bei jedem Impuls wechselt der Ausgang `Q` seinen Zustand (von TRUE auf FALSE oder umgekehrt).
    *   Der Wert von `Q` wird direkt auf den externen Ausgang `Rechts` geschrieben.

3.  **Invertierung (F_NOT)**:
    *   Das Ereignis `EO` des Flip-Flops triggert den Invertierer `F_NOT`.
    *   Der Zustand von `Q` (vom Flip-Flop) liegt am Eingang `IN` an.
    *   Der Baustein negiert diesen Wert (aus TRUE wird FALSE, aus FALSE wird TRUE) und gibt ihn am Ausgang `OUT` aus.
    *   Dieser invertierte Wert wird auf den externen Ausgang `Links` geschrieben.

4.  **Abschluss**:
    *   Nachdem die Invertierung abgeschlossen ist, sendet `F_NOT` ein Bestätigungsereignis (`CNF`), welches als externes Ereignis `EO` der Sub-Applikation ausgegeben wird.

**Zusammenfassung der Schnittstellen:**
*   **Eingänge**: `EI` (Event), `DI` (Data/Bool - Freigabe).
*   **Ausgänge**: `EO` (Event), `Rechts` (Data/Bool), `Links` (Data/Bool - invertiert zu Rechts).

## Zusammenfassung
Die Sub-Applikation `Uebung_006a3_sub` stellt eine verriegelte Wechselschaltung dar. Sie eignet sich für Steuerungsaufgaben, bei denen zwischen zwei exklusiven Zuständen (z.B. Motordrehrichtung Rechts/Links) gewechselt werden soll, jedoch nur, wenn ein explizites Freigabesignal (`DI`) vorliegt.