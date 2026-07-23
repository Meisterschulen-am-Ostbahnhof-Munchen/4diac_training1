# Übung 061: Reine Zeitsteuerung 4-Kanal

## Thema: Ablaufsteuerungen in der Landtechnik

### Situationsbeschreibung
Für ein System in der landwirtschaftlichen Automatisierung (z.B. eine Fassreinigung, eine Klappvorrichtung oder ein Gebläse) soll eine Ablaufsteuerung implementiert werden.
Es werden 4 Stufen oder Aktoren nacheinander geschaltet. 

Die Steuerung soll über den Baustein `sequence_T_04_AX` realisiert werden.

### Funktionsbeschreibung der Ablaufsteuerung
- **Start:** Durch Betätigen des Tasters `I1` (`START_S1`).
- **Phasen:** 4 aufeinanderfolgende Ausgangsschritte (Ausgänge `Q1` bis `Q4`).
- **Übergänge:** Die Schrittübergänge laufen rein zeitgesteuert ab (jeder Schritt dauert 1 Sekunde).
- **Reset:** Zu jedem Zeitpunkt kann die Schrittkette über einen Reset (z.B. Taster `I4` oder Softkey) in den Ausgangszustand (Schritt 0) zurückgesetzt werden.

### Arbeitsauftrag
1. Öffnen Sie das 4diac-Projekt und legen Sie die SubApp `Uebung_061_AX` bzw. `Uebung_061` an.
2. Platzieren Sie den Sequenzer-Baustein `sequence_T_04_AX` und konfigurieren Sie die Parameter.
3. Verbinden Sie den Start-Taster `I1` und den Reset-Taster `I4` mit den entsprechenden Eingängen.
4. Schalten Sie die 4 Ausgänge auf die physischen Ausgänge `Output_Q1` bis `Output_Q4`.
5. Zur Visualisierung soll die Zustandsnummer `STATE_NR` auf dem ISOBUS Virtual Terminal-Ausgang `OutputNumber_N1` angezeigt werden.
