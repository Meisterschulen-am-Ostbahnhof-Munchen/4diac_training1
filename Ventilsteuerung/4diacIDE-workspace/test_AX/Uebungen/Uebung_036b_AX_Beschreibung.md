# Übung 036b: Kombinierte 4-Kanal-Schrittkette (Event & Zeit) mit sequence_ET_04_AX

## Thema: Ablaufsteuerungen in der Landtechnik

### Situationsbeschreibung
Ein Landwirt möchte die Reinigungsprozedur seiner Feldspritze teil-automatisieren, um Wasser zu sparen und den Spülvorgang zu beschleunigen. Das Spülsystem besitzt vier Ventile für verschiedene Spülstufen (Vorspülen, Hauptspülen, Klarspülen, Ausblasen). 
Die Reinigung soll in vier aufeinanderfolgenden Phasen ablaufen. Jede Phase soll eine maximale Dauer haben (Zeitsteuerung), kann jedoch vom Bediener in der Traktorkabine bei Bedarf vorzeitig per Tastendruck auf die nächste Stufe geschaltet werden (Eventsteuerung).

### Funktionsbeschreibung der Ablaufsteuerung
Die Logik soll mit dem Funktionsbaustein [sequence_ET_04_AX.fbt](file:///C:/git/ms/4diac_training1/Ventilsteuerung/4diacIDE-workspace/.lib/logiBUS-3.0.0/typelib/utils/sequence/combi/sequence_ET_04_AX.fbt) realisiert werden.

#### Phasen des Spülprozesses:
1. **Zustand 0 (Bereit / Idle):** Das System wartet auf den Start. Kein Ventil ist aktiv (`STATE_NR = 0`).
2. **Schritt 1 (Vorspülen):** Ventil 1 öffnet (`DO_S1` wird aktiv). Maximale Dauer: **5 Sekunden** (`DT_S1_S2 = T#5s`). Ein Impuls auf Taster `I2` (`S1_S2`) schaltet vorzeitig in Schritt 2.
3. **Schritt 2 (Hauptspülen):** Ventil 2 öffnet (`DO_S2` wird aktiv). Maximale Dauer: **10 Sekunden** (`DT_S2_S3 = T#10s`). Ein Impuls auf Taster `I3` (`S2_S3`) schaltet vorzeitig in Schritt 3.
4. **Schritt 3 (Klarspülen):** Ventil 3 öffnet (`DO_S3` wird aktiv). Maximale Dauer: **5 Sekunden** (`DT_S3_S4 = T#5s`). Ein Impuls auf Taster `I4` (`S3_S4`) schaltet vorzeitig in Schritt 4.
5. **Schritt 4 (Ausblasen/Abtropfen):** Ventil 4 öffnet (`DO_S4` wird aktiv). Maximale Dauer: **3 Sekunden** (`DT_S4_START = T#3s`). Nach Ablauf dieser Zeit wechselt das System automatisch wieder in den Zustand 0 (Bereit).

### Arbeitsauftrag
1. Öffnen Sie das 4diac-Projekt und legen Sie die SubApp `Uebung_037_AX` an (eine Vorlage befindet sich bereits im Ordner `Uebungen`).
2. Platzieren Sie den Sequenzer-Baustein `sequence_ET_04_AX` und konfigurieren Sie die Zeitparameter (`DT_S1_S2` bis `DT_S4_START`) entsprechend den Vorgaben.
3. Verbinden Sie den Start-Taster `I1` (über das Event `BUTTON_SINGLE_CLICK` von `DigitalInput_CLK_I1`) mit dem Eingang `START_S1` des Sequenzers.
4. Verbinden Sie die Taster `I2`, `I3` und `I4` mit den entsprechenden Weiterschalt-Ereignissen (`S1_S2`, `S2_S3`, `S3_S4`).
5. Schalten Sie die vier Ausgänge `DO_S1` bis `DO_S4` auf die digitalen Ausgänge `Output_Q1` bis `Output_Q4` der Ventilsteuerung.
6. Zur Visualisierung des aktuellen Schrittes soll die Zustandsnummer `STATE_NR` in einen `UINT` konvertiert und an den ISOBUS Virtual Terminal-Ausgang `OutputNumber_N1` gesendet werden.
7. Testen Sie das Verhalten der Ablaufsteuerung in der Simulation (FORTE) oder auf der realen Hardware:
   - Läuft die Kette ohne Benutzereingriff vollautomatisch durch?
   - Lässt sich die Kette durch Tastendrücke beschleunigen?
