# 🚜 4diac Training: Ventilsteuerung & ISOBUS Automation

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)
[![4diac](https://img.shields.io/badge/Eclipse-4diac-purple)](https://www.eclipse.org/4diac/)
[![Standard](https://img.shields.io/badge/Standard-IEC%2061131--3-green)](https://en.wikipedia.org/wiki/IEC_61131-3)
[![Protocol](https://img.shields.io/badge/Protocol-ISOBUS%20%2F%20J1939-orange)]()

Dieses Repository bietet eine umfassende Sammlung von Trainingsmaterialien, Beispielprojekten und Implementierungen für die **Ventilsteuerung** unter Verwendung von **Eclipse 4diac**. Der Fokus liegt auf der mobilen Automation, insbesondere der Integration von **ISOBUS (ISO 11783)** Technologien.

Es eignet sich hervorragend für Schulungszwecke, Meisterkurse und Entwickler, die sich in die IEC 61131-3 Programmierung mit verteilten Steuerungssystemen einarbeiten möchten.

---

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

* **IDE:** [Eclipse 4diac IDE](https://www.eclipse.org/4diac/) (IEC 61131-3 Standard)
* **Laufzeitumgebung:** Eclipse FORTE (4diac RTE)
* **HMI Design:** Jetter ISO-Designer (für ISOBUS VT)
* **Kommunikation:** CAN-Bus, SAE J1939, ISO 11783 (ISOBUS)
* **Hardware-Ziele:** ESP32, PC (Soft-SPLC), Mobile Controller

---

## 📂 Ordnerstruktur

Ein kurzer Überblick über die wichtigsten Verzeichnisse:

```text
4diac_training1/
├── Ventilsteuerung/
│   ├── 4diacIDE-workspace/       # Haupt-Arbeitsbereich für 4diac Projekte
│   │   ├── test_AX/              # Übungsprojekte Serie A
│   │   ├── test_B/               # Übungsprojekte Serie B
│   │   └── .lib/                 # Bibliotheken (logiBUS, isobus, iec61131)
│   ├── ISO-DesignerProjects/     # HMI/VT Designs
│   │   ├── Workspace_Joystick/   # Joystick-Integration
│   │   ├── Workspace_PWM/        # PWM-Visualisierung
│   │   └── Workspace_TECU/       # Tractor ECU Simulation
│   ├── TaskController-SC/        # Section Control Konfigurationen
│   └── scripts/                  # Python & Batch Hilfsskripte
└── README.md




Übungen AX
Doku: https://meisterschulen-am-ostbahnhof-munchen-docs.readthedocs.io/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test_AX/Uebungen_doc/Uebungen.html

Übungen (ohne AX)
Doku: https://meisterschulen-am-ostbahnhof-munchen-docs.readthedocs.io/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test_B/Uebungen_doc/Uebungen.html

Übungen (VV Verteilte Verarbeitung)
Doku: TODO,
kommt hier hin: https://meisterschulen-am-ostbahnhof-munchen-docs.readthedocs.io/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test_VV/Uebungen_doc/Uebungen.html

















