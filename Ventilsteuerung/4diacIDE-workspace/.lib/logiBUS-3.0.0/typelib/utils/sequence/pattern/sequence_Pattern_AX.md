# ⚙️ Pattern-Sequenzer (AX Adapter)

Dieses Dokument beschreibt die Pattern-Sequenzer (Nockenschaltwerke) der logiBUS®-Bibliothek, die für die Verwendung mit dem **AX Adapter** optimiert sind.

## ℹ️ Allgemeines

Die Pattern-Sequenzer (`sequence_Pattern_xx_AX`) ermöglichen es, für jeden Schritt ein individuelles Bitmuster (Pattern) für die Ausgänge zu definieren. Dies ist ideal für Anwendungen, bei denen in einem Schritt mehrere Aktoren gleichzeitig in bestimmten Mustern geschaltet werden müssen (z. B. eine Nockenwellensteuerung).

Die hier beschriebenen Bausteine sind zyklisch (**loop**), d.h. nach dem letzten Schritt erfolgt automatisch (oder per Event) der Übergang zurück zum ersten Schritt.

---

## 📦 Verfügbare Typen

| Baustein | Schritte | Ausgänge | Beschreibung |
| :--- | :---: | :---: | :--- |
| `sequence_Pattern_04_04_loop_AX` | 4 | 4 | 4 Schritte mit 4 AX-Ausgängen. |
| `sequence_Pattern_08_08_loop_AX` | 8 | 8 | 8 Schritte mit 8 AX-Ausgängen. |

---

## 🔌 Schnittstellenbeschreibung

### 📥 Eingänge (Events)

| Anschluss | Typ | Beschreibung |
| :--- | :--- | :--- |
| **START_S1** | `Event` | Startet die Sequenz und springt vom Initialzustand in **Schritt 1**. |
| **S1_S2** ... **Sx_S1** | `Event` | Manuelles Weiterschalten zum nächsten Schritt. |
| **RESET** | `Event` | Setzt die Sequenz sofort auf den Initialzustand (START) zurück und schaltet alle Ausgänge ab. |

### 📥 Eingänge (Daten)

| Anschluss | Typ | Initialwert | Beschreibung |
| :--- | :--- | :--- | :--- |
| **DT_S1_S2** ... | `TIME` | `NO_TIME` | Zeitdauer für den jeweiligen Schritt. Wenn `NO_TIME`, erfolgt kein automatisches Weiterschalten. |
| **P_S1** ... **P_Sx** | `BYTE` | (variiert) | Bitmuster für den jeweiligen Schritt. |

### 📤 Ausgänge (Daten)

| Anschluss | Typ | Beschreibung |
| :--- | :--- | :--- |
| **STATE_NR** | `SINT` | Aktuelle Schrittnummer (0 = START, 1 = Schritt 1, ...). |

### 🔌 Adapter (Plugs)

| Anschluss | Typ | Beschreibung |
| :--- | :--- | :--- |
| **Q1** ... **Qx** | `AX` | AX-Adapter-Ausgänge. Gesteuert durch die Bits des Patterns. |
| **timeOut** | `ATimeOut` | Adapter zur Anbindung eines Time-Out-Bausteins für die Zeitsteuerung. |

---

## ⚙️ Funktionsweise

### Pattern-Mapping
Jeder Zustand `S1` bis `Sx` hat einen zugehörigen Eingang `P_S1` bis `P_Sx` vom Typ `BYTE`. Die einzelnen Bits dieses Bytes steuern die Adapter-Ausgänge `Q1` bis `Qx`:
- **Bit 0** -> Ausgang **Q1**
- **Bit 1** -> Ausgang **Q2**
- **Bit 2** -> Ausgang **Q3**
- **Bit 3** -> Ausgang **Q4**
- ...
- **Bit 7** -> Ausgang **Q8** (nur bei der 8-Kanal Version)

### Schrittwechsel
Ein Wechsel zum nächsten Schritt erfolgt durch:
1. Das Eintreffen des entsprechenden **Weiterschalt-Events** (z.B. `S1_S2`).
2. Das Eintreffen eines `timeOut.TimeOut` Events, sofern am entsprechenden `DT`-Eingang eine Zeit ungleich `NO_TIME` konfiguriert wurde.

Beim Eintritt in einen neuen Zustand wird:
- Das zugehörige Bitmuster an die AX-Adapter angelegt.
- Ein `E1`-Event an allen betroffenen AX-Adaptern ausgelöst.
- Der `timeOut` Timer mit der neuen Zeit gestartet.
- Der Ausgang `STATE_NR` aktualisiert und das Event `CNF` gefeuert.

---

## 🛠️ Zugehörige Übungen

Die Verwendung der Pattern-Sequenzer wird in folgenden Übungen demonstriert:
- [Uebung_035a1_AX](../../../../test_AX/Uebungen_doc/Uebung_035a1_AX.md)

---

**Autor:** Franz Höpfinger  
**Version:** 1.0 (2026-02-01)  
**Copyright:** (c) 2026 HR Agrartechnik GmbH  
**Lizenz:** EPL-2.0
