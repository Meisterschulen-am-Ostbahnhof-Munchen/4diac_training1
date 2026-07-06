# Übung 036: Kombinierte 4-Kanal-Schrittkette (Event & Zeit) mit sequence_ET_04_AX

## Thema: Ablaufsteuerungen in der Landtechnik

### Situationsbeschreibung
Ein Landwirt möchte die Reinigungsprozedur seiner Feldspritze teil-automatisieren, um Wasser zu sparen und den Spülvorgang zu beschleunigen. Das Spülsystem besitzt vier Ventile für verschiedene Spülstufen (Vorspülen, Hauptspülen, Klarspülen, Ausblasen). 

Die ersten beiden Phasen (Vorspülen, Hauptspülen) sollen manuell durch den Bediener per Knopfdruck weitergeschaltet werden, da diese je nach Verschmutzung unterschiedlich lange dauern. Die letzten beiden Phasen (Klarspülen, Ausblasen) sollen vollautomatisch für jeweils 2 Sekunden laufen.

### Funktionsbeschreibung der Ablaufsteuerung
Die Logik soll mit dem Funktionsbaustein [sequence_ET_04_AX.fbt](../../.lib/logiBUS-3.0.0/typelib/utils/sequence/combi/sequence_ET_04_AX.fbt) realisiert werden.

#### Phasen des Spülprozesses:
1. **Zustand 0 (Bereit / Idle):** Das System wartet auf den Start. Kein Ventil ist aktiv (`STATE_NR = 0`).
2. **Schritt 1 (Vorspülen):** Ventil 1 öffnet (`DO_S1` wird aktiv). Die Phase läuft unbegrenzt (`DT_S1_S2 = NO_TIME`). Erst ein Impuls auf Taster `I2` (`S1_S2`) schaltet in Schritt 2.
3. **Schritt 2 (Hauptspülen):** Ventil 2 öffnet (`DO_S2` wird aktiv). Die Phase läuft unbegrenzt (`DT_S2_S3 = NO_TIME`). Erst ein Impuls auf Taster `I3` (`S2_S3`) schaltet in Schritt 3.
4. **Schritt 3 (Klarspülen):** Ventil 3 öffnet (`DO_S3` wird aktiv). Die Phase dauert genau **2 Sekunden** (`DT_S3_S4 = T#2s`) und schaltet danach automatisch weiter.
5. **Schritt 4 (Ausblasen/Abtropfen):** Ventil 4 öffnet (`DO_S4` wird aktiv). Die Phase dauert genau **2 Sekunden** (`DT_S4_START = T#2s`) und schaltet danach automatisch wieder in den Zustand 0 (Bereit).
6. **Reset:** Zu jedem Zeitpunkt kann das System durch Betätigen von Taster `I4` (`RESET`) sofort in den Zustand 0 (Bereit) zurückgesetzt werden.

### Arbeitsauftrag
1. Öffnen Sie das 4diac-Projekt und legen Sie die SubApp `Uebung_036_AX` an (eine Vorlage befindet sich bereits im Ordner `Uebungen`).
2. Platzieren Sie den Sequenzer-Baustein `sequence_ET_04_AX` und konfigurieren Sie die Zeitparameter (`DT_S1_S2` bis `DT_S4_START`) entsprechend den Vorgaben.
3. Verbinden Sie den Start-Taster `I1` (über das Event `BUTTON_SINGLE_CLICK` von `DigitalInput_CLK_I1`) mit dem Eingang `START_S1` des Sequenzers.
4. Verbinden Sie die Taster `I2` und `I3` mit den Weiterschalt-Ereignissen (`S1_S2`, `S2_S3`).
5. Verbinden Sie den Reset-Taster `I4` mit dem Eingang `RESET` des Sequenzers.
6. Schalten Sie die vier Ausgänge `DO_S1` bis `DO_S4` auf die digitalen Ausgänge `Output_Q1` bis `Output_Q4` der Ventilsteuerung.
7. Zur Visualisierung des aktuellen Schrittes soll die Zustandsnummer `STATE_NR` in einen `UINT` konvertiert und an den ISOBUS Virtual Terminal-Ausgang `OutputNumber_N1` gesendet werden.
8. Testen Sie das Verhalten der Ablaufsteuerung in der Simulation (FORTE) oder auf der realen Hardware.
