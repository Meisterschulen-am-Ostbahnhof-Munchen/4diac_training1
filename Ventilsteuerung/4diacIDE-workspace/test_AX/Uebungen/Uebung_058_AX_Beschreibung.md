# Übung 058: Reine Event-Schrittkette 5-Kanal ENDLOS

## Thema: Ablaufsteuerungen in der Landtechnik

### Situationsbeschreibung
Für ein System in der landwirtschaftlichen Automatisierung (z.B. eine Fassreinigung, eine Klappvorrichtung oder ein Gebläse) soll eine Ablaufsteuerung implementiert werden.
Es werden 5 Stufen oder Aktoren nacheinander geschaltet. 

Die Steuerung soll über den Baustein `sequence_E_05_loop_AX` realisiert werden.

### Funktionsbeschreibung der Ablaufsteuerung
- **Start:** Durch Betätigen des Tasters `I1` (`START_S1`).
- **Phasen:** 5 aufeinanderfolgende Ausgangsschritte (Ausgänge `Q1` bis `Q5`).
- **Übergänge:** Die Schrittübergänge laufen rein ereignisgesteuert ab (Taster I2, I3 etc.).
- **Reset:** Zu jedem Zeitpunkt kann die Schrittkette über einen Reset (z.B. Taster `I4` oder Softkey) in den Ausgangszustand (Schritt 0) zurückgesetzt werden.

### Arbeitsauftrag
1. Öffnen Sie das 4diac-Projekt und legen Sie die SubApp `Uebung_058_AX` bzw. `Uebung_058` an.
2. Platzieren Sie den Sequenzer-Baustein `sequence_E_05_loop_AX` und konfigurieren Sie die Parameter.
3. Verbinden Sie den Start-Taster `I1` und den Reset-Taster `I4` mit den entsprechenden Eingängen.
4. Schalten Sie die 5 Ausgänge auf die physischen Ausgänge `Output_Q1` bis `Output_Q5`.
5. Zur Visualisierung soll die Zustandsnummer `STATE_NR` auf dem ISOBUS Virtual Terminal-Ausgang `OutputNumber_N1` angezeigt werden.
