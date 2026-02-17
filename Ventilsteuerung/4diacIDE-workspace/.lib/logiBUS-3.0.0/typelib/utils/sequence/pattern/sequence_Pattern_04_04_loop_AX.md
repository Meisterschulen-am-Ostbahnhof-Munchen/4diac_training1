# ⚙️ sequence_Pattern_04_04_loop_AX

**Pattern Sequence 4 Steps 4 Outputs (Cam Sequencer), AX Adapter**

Dieser Baustein realisiert eine zyklische Schrittkette mit 4 Schritten, bei der in jedem Schritt ein individuelles Bitmuster (Pattern) an 4 AX-Adapter-Ausgänge ausgegeben wird.

## 🔌 Schnittstelle

### 📥 Eingänge (Events)

| Name | Beschreibung |
| :--- | :--- |
| **START_S1** | Startet die Sequenz (Übergang von START zu Schritt 1). |
| **S1_S2** | Manueller Übergang von Schritt 1 zu Schritt 2. |
| **S2_S3** | Manueller Übergang von Schritt 2 zu Schritt 3. |
| **S3_S4** | Manueller Übergang von Schritt 3 zu Schritt 4. |
| **S4_S1** | Manueller Übergang von Schritt 4 zurück zu Schritt 1. |
| **RESET** | Setzt die Sequenz sofort auf den Initialzustand (START) zurück. |

### 📤 Ausgänge (Events)

| Name | Beschreibung |
| :--- | :--- |
| **CNF** | Bestätigungsevent bei jedem Zustandswechsel. |

### 📥 Eingänge (Daten)

| Name | Typ | Initialwert | Beschreibung |
| :--- | :--- | :--- | :--- |
| **DT_S1_S2** | TIME | `NO_TIME` | Zeitdauer für Schritt 1. |
| **DT_S2_S3** | TIME | `NO_TIME` | Zeitdauer für Schritt 2. |
| **DT_S3_S4** | TIME | `NO_TIME` | Zeitdauer für Schritt 3. |
| **DT_S4_S1** | TIME | `NO_TIME` | Zeitdauer für Schritt 4. |
| **P_S1** | BYTE | `1` | Bitmuster für Schritt 1 (Bit 0 -> Q1, Bit 1 -> Q2 ...). |
| **P_S2** | BYTE | `2` | Bitmuster für Schritt 2. |
| **P_S3** | BYTE | `4` | Bitmuster für Schritt 3. |
| **P_S4** | BYTE | `8` | Bitmuster für Schritt 4. |

### 📤 Ausgänge (Daten)

| Name | Typ | Beschreibung |
| :--- | :--- | :--- |
| **STATE_NR** | SINT | Aktuelle Schrittnummer (0=START, 1..4=Schritt). |

### 🔌 Adapter (Plugs)

| Name | Typ | Beschreibung |
| :--- | :--- | :--- |
| **Q1** | AX | Adapter-Ausgang 1 (Bit 0 des Patterns). |
| **Q2** | AX | Adapter-Ausgang 2 (Bit 1 des Patterns). |
| **Q3** | AX | Adapter-Ausgang 3 (Bit 2 des Patterns). |
| **Q4** | AX | Adapter-Ausgang 4 (Bit 3 des Patterns). |
| **timeOut** | ATimeOut | Schnittstelle für Zeitüberwachung. |

## ⚙️ Funktionsweise

Beim Eintritt in einen Schritt wird das entsprechende Bitmuster (`P_S1` bis `P_S4`) auf die Ausgänge `Q1` bis `Q4` verteilt:
- Bit 0 -> Q1.D1
- Bit 1 -> Q2.D1
- Bit 2 -> Q3.D1
- Bit 3 -> Q4.D1

Ein Weiterschalten erfolgt entweder durch das entsprechende Event (z.B. `S1_S2`) oder automatisch nach Ablauf der Zeit (z.B. `DT_S1_S2`).

## 🛠️ Zugehörige Übungen

- [Uebung_035a1_AX](../../../../test_AX/Uebungen_doc/Uebung_035a1_AX.md)

---

**Autor:** Franz Höpfinger  
**Version:** 1.0 (2026-02-01)  
**Copyright:** (c) 2026 HR Agrartechnik GmbH  
**Lizenz:** EPL-2.0
