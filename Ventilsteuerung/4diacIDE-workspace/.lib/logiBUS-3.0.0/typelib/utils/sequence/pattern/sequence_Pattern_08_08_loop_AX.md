# ⚙️ sequence_Pattern_08_08_loop_AX

**Pattern Sequence 8 Steps 8 Outputs (Cam Sequencer), AX Adapter**

Dieser Baustein realisiert eine zyklische Schrittkette mit 8 Schritten, bei der in jedem Schritt ein individuelles Bitmuster (Pattern) an 8 AX-Adapter-Ausgänge ausgegeben wird.

## 🔌 Schnittstelle

### 📥 Eingänge (Events)

| Name | Beschreibung |
| :--- | :--- |
| **START_S1** | Startet die Sequenz (Übergang von START zu Schritt 1). |
| **S1_S2** ... **S7_S8** | Manueller Übergang zum nächsten Schritt. |
| **S8_S1** | Manueller Übergang von Schritt 8 zurück zu Schritt 1. |
| **RESET** | Setzt die Sequenz sofort auf den Initialzustand (START) zurück. |

### 📤 Ausgänge (Events)

| Name | Beschreibung |
| :--- | :--- |
| **CNF** | Bestätigungsevent bei jedem Zustandswechsel. |

### 📥 Eingänge (Daten)

| Name | Typ | Initialwert | Beschreibung |
| :--- | :--- | :--- | :--- |
| **DT_S1_S2** ... | TIME | `NO_TIME` | Zeitdauer für den jeweiligen Schritt. |
| **P_S1** | BYTE | `1` | Bitmuster für Schritt 1 (Bit 0 -> Q1 ... Bit 7 -> Q8). |
| **P_S2** | BYTE | `2` | Bitmuster für Schritt 2. |
| **P_S3** | BYTE | `4` | Bitmuster für Schritt 3. |
| **P_S4** | BYTE | `8` | Bitmuster für Schritt 4. |
| **P_S5** | BYTE | `16` | Bitmuster für Schritt 5. |
| **P_S6** | BYTE | `32` | Bitmuster für Schritt 6. |
| **P_S7** | BYTE | `64` | Bitmuster für Schritt 7. |
| **P_S8** | BYTE | `128` | Bitmuster für Schritt 8. |

### 📤 Ausgänge (Daten)

| Name | Typ | Beschreibung |
| :--- | :--- | :--- |
| **STATE_NR** | SINT | Aktuelle Schrittnummer (0=START, 1..8=Schritt). |

### 🔌 Adapter (Plugs)

| Name | Typ | Beschreibung |
| :--- | :--- | :--- |
| **Q1** ... **Q8** | AX | Adapter-Ausgänge 1 bis 8. |
| **timeOut** | ATimeOut | Schnittstelle für Zeitüberwachung. |

## ⚙️ Funktionsweise

Beim Eintritt in einen Schritt wird das entsprechende Bitmuster (`P_S1` bis `P_S8`) auf die Ausgänge `Q1` bis `Q8` verteilt. Jedes Bit entspricht dabei einem Ausgang (Bit 0 -> Q1, Bit 7 -> Q8).

Ein Weiterschalten erfolgt entweder durch ein externes Event oder automatisch nach Ablauf der konfigurierten Zeit am entsprechenden `DT`-Eingang.

---

**Autor:** Franz Höpfinger  
**Version:** 1.0 (2026-02-01)  
**Copyright:** (c) 2026 HR Agrartechnik GmbH  
**Lizenz:** EPL-2.0
