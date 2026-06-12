# 🚜 4diac Training: Ventilsteuerung & ISOBUS Automation



[![License](https://img.shields.io/badge/License-EPL%202.0-red.svg)](LICENSE.md)
[![4diac](https://img.shields.io/badge/Eclipse-4diac-purple)](https://www.eclipse.org/4diac/)
[![Standard](https://img.shields.io/badge/Standard-IEC%2061131--3-green)](https://en.wikipedia.org/wiki/IEC_61131-3)
[![Standard](https://img.shields.io/badge/Standard-DIN%20EN%2061131--3-green)](https://de.wikipedia.org/wiki/EN_61131-3)
[![Standard](https://img.shields.io/badge/Standard-IEC%2061499-green)](https://en.wikipedia.org/wiki/IEC_61499)
[![Standard](https://img.shields.io/badge/Standard-DIN%20EN%2061499-green)](https://de.wikipedia.org/wiki/EN_61499)
[![Protocol](https://img.shields.io/badge/Protocol-ISOBUS%20%2F%20J1939-orange)]()

Dieses Repository bietet eine umfassende Sammlung von Trainingsmaterialien, Beispielprojekten und Implementierungen für die **Ventilsteuerung** unter Verwendung von **Eclipse 4diac™**. Der Fokus liegt auf der mobilen Automation, insbesondere der Integration von **ISOBUS (ISO 11783)** Technologien.

Es eignet sich hervorragend für Schulungszwecke, Meisterkurse und Entwickler, die sich in die IEC 61131-3 / IEC 61499 Programmierung mit verteilten aber auch lokalen Steuerungssystemen einarbeiten möchten.

logiBUS® <https://www.logibus.tech/> 

## 📋 Inhaltsverzeichnis

- [Über das Projekt](#über-das-projekt)
- [Hauptkomponenten](#hauptkomponenten)
- [Verwendete Technologien](#verwendete-technologien)
- [Ordnerstruktur](#ordnerstruktur)
- [Voraussetzungen](#voraussetzungen)
- [Erste Schritte](#erste-schritte)
- [SEO & Schlagwörter](#seo--schlagwörter)

---

## 📖 Über das Projekt

Das Hauptziel dieses Repositories ist die Demonstration einer **SPS-basierten Ventilsteuerung** im Kontext landwirtschaftlicher Anwendungen. Es verbindet die Logik-Programmierung (Funktionsbausteine) mit modernen HMI-Schnittstellen über ISOBUS Virtual Terminals (VT).

Enthalten sind zahlreiche Übungen (`Uebung_001` bis `Uebung_160`), die schrittweise von einfachen Logikgattern bis hin zu komplexen Sequenzsteuerungen und Kommunikationsprotokollen führen.

---

## ⚙️ Hauptkomponenten

### 1. Ventilsteuerung (Logic)
Implementierung der Steuerungslogik für Hydraulikventile.
- **Funktionen:** Zeitgesteuerte Abläufe, Verriegelungen, PWM-Ansteuerung.
- **Sicherheit:** Not-Halt-Routinen und Fehlerbehandlung.

### 2. ISOBUS Integration (HMI)
Vollständige Design-Projekte für **Virtual Terminals (VT)**.
- **ISO-Designer Projekte:** Enthalten Masken, Softkeys und Alarmmeldungen.
- **Pool-Dateien:** `.jop`, `.jvi` und Bildressourcen für verschiedene Auflösungen (Monochrom & Farbe).
- **Task Controller (TC-SC):** Beispiele für Section Control (`.dvc` Dateien).

### 3. Trainingsübungen
Eine strukturierte Reihe von Lernmodulen:
- Grundlagen der digitalen Logik (AND, OR, XOR).
- Zeitglieder (TON, TOF, TP).
- Zustandsautomaten und Sequenzen.
- Datenkonvertierung und Arrays.

---

## 🛠 Verwendete Technologien

* **IDE:** [Eclipse 4diac IDE](https://www.eclipse.org/4diac/) (IEC 61131-3 / IEC 61499 Standard)
* **Laufzeitumgebung:** Eclipse FORTE (4diac RTE)
* **HMI Design:** Jetter / Bucher ISO-Designer (für ISOBUS VT)
* **Kommunikation:** CAN-Bus, SAE J1939, ISO 11783 (ISOBUS)
* **Hardware-Ziele:** ESP32, PC (Soft-SPLC), Mobile Controller

---

## 📂 Ordnerstruktur

Ein kurzer Überblick über die wichtigsten Verzeichnisse:

```text
4diac_training1/
├── Ventilsteuerung/
│   ├── 4diacIDE-workspace/       # Haupt-Arbeitsbereich für 4diac Projekte
│   │   ├── test_AX/              # Übungsprojekte Serie AX (mit AX Adapter)
│   │   ├── test_B/               # Übungsprojekte Serie B (ohne AX Adapter)
│   │   ├── test_VV/              # Übungsprojekte Serie VV (Verteile Verarbeitung)
│   │   └── .lib/                 # Bibliotheken (logiBUS®, isobus, iec61131, iec61499)
│   ├── ISO-DesignerProjects/     # HMI/VT Designs
│   │   ├── Workspace/            # Basis Pool für die meisten Übungen
│   │   ├── Workspace_Joystick/   # Joystick-Integration
│   │   ├── Workspace_PWM/        # PWM-Visualisierung
│   │   └── Workspace_TECU/       # Tractor ECU auslesen
│   ├── TaskController-SC/        # Section Control Konfigurationen
│   └── scripts/                  # Python & Batch Hilfsskripte
└── README.md
```

## 🚀 Erste Schritte

### 1. Projekt beschaffen
Sie haben zwei Möglichkeiten, die Dateien zu erhalten:

* **Option A: ZIP-Download (Einfach & Schnell)** Sie können den aktuellen Stand direkt als ZIP-Datei herunterladen. Dafür ist **kein Git-Client** notwendig.  
    📦 [**Hier geht es zu den Downloads / Releases**](https://github.com/Meisterschulen-am-Ostbahnhof-Munchen/4diac_training1/releases)

* **Option B: Repository klonen (Für Entwickler)** Nutzen Sie diese Methode, wenn Sie Versionskontrolle verwenden möchten:
    ```bash
    git clone [https://github.com/Meisterschulen-am-Ostbahnhof-Munchen/4diac_training1.git](https://github.com/Meisterschulen-am-Ostbahnhof-Munchen/4diac_training1.git)
    ```

### 2. 4diac IDE starten
Wähle den Ordner `Ventilsteuerung/4diacIDE-workspace` aus dem heruntergeladenen Paket als deinen Workspace.

### 3. Bibliotheken importieren
Stelle sicher, dass die `isobus`, `logiBUS` und `iec61131` Bibliotheken korrekt im Pfad eingebunden sind.

### 4. Deploy
Nutze die `.launch` Dateien im Ordner `Launches`, um die Applikation auf dein Zielgerät (oder FORTE PC) zu laden.
2.  **4diac IDE starten:**
    Wähle `Ventilsteuerung/4diacIDE-workspace` als deinen Workspace.
3.  **Bibliotheken importieren:**
    Stelle sicher, dass die `isobus`, `logiBUS` und `iec61131` Bibliotheken korrekt im Pfad eingebunden sind.
4.  **Deploy:**
    Nutze die `.launch` Dateien im Ordner `Launches`, um die Applikation auf dein Zielgerät (oder FORTE PC) zu laden.

-----

## 📚 Dokumentation & Übungsreihen

Detaillierte Anleitungen und Beschreibungen zu den einzelnen Übungspaketen finden Sie in unserer ReadTheDocs-Dokumentation.

| Bereich | Beschreibung | Dokumentation |
| :--- | :--- | :--- |
| **Übungen AX** | Grundlagen der Ventilsteuerung (Serie AX) | [📘 Zur Dokumentation](https://meisterschulen-am-ostbahnhof-munchen-docs.readthedocs.io/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test_AX/Uebungen_doc/Uebungen.html) |
| **Übungen B** | Erweiterte Übungen ohne AX-Präfix | [📙 Zur Dokumentation](https://meisterschulen-am-ostbahnhof-munchen-docs.readthedocs.io/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test_B/Uebungen_doc/Uebungen.html) |
| **Übungen VV** | Verteilte Verarbeitung & Kommunikation | [🚀 Zur Dokumentation](https://meisterschulen-am-ostbahnhof-munchen-docs.readthedocs.io/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test_VV/Uebungen_doc/Uebungen.html) |

## 🔍 SEO & Schlagwörter

**Themengebiete:**
`Automatisierungstechnik`, `Mobile Automation`, `Landtechnik`, `SPS Programmierung`, `Embedded Systems`

**Technologien:**
`Eclipse 4diac`, `FORTE`, `IEC 61131-3`, `IEC 61499`, `Function Block Diagram (FBD)`, `Structured Text (ST)`, `ESP32`

**Protokolle & Standards:**
`ISOBUS`, `ISO 11783`, `SAE J1939`, `CAN Bus`, `Virtual Terminal (VT)`, `Task Controller (TC)`

**Spezifisch:**
`Ventilsteuerung`, `Hydraulik`, `Meisterschule Projekt`, `Open Source PLC`

-----

**Hinweis:** Dieses Projekt dient primär Bildungszwecken im Rahmen der Meisterschulen am Ostbahnhof München.

<https://www.ms-muc-docs.de/>

<https://www.ms-muc.de/>