# 🚜 4diac Training: Valve Control & ISOBUS Automation



[![License](https://img.shields.io/badge/License-EPL%202.0-red.svg)](LICENSE.md)
[![4diac](https://img.shields.io/badge/Eclipse-4diac-purple)](https://www.eclipse.org/4diac/)
[![Standard](https://img.shields.io/badge/Standard-IEC%2061131--3-green)](https://en.wikipedia.org/wiki/IEC_61131-3)
[![Standard](https://img.shields.io/badge/Standard-DIN%20EN%2061131--3-green)](https://de.wikipedia.org/wiki/EN_61131-3)
[![Standard](https://img.shields.io/badge/Standard-IEC%2061499-green)](https://en.wikipedia.org/wiki/IEC_61499)
[![Standard](https://img.shields.io/badge/Standard-DIN%20EN%2061499-green)](https://de.wikipedia.org/wiki/EN_61499)
[![Protocol](https://img.shields.io/badge/Protocol-ISOBUS%20%2F%20J1939-orange)]()

🇩🇪 [Deutsch](README.md) | 🇬🇧 English

This repository provides a comprehensive collection of training materials, sample projects, and implementations for **valve control** using **Eclipse 4diac™**. The focus is on mobile automation, in particular the integration of **ISOBUS (ISO 11783)** technologies.

It is ideally suited for training purposes, master craftsman courses, and developers who want to get into IEC 61131-3 / IEC 61499 programming with distributed as well as local control systems.

logiBUS® <https://www.logibus.tech/>

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Main Components](#main-components)
- [Technologies Used](#technologies-used)
- [Folder Structure](#folder-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Documentation & Exercise Series](#documentation--exercise-series)
- [SEO & Keywords](#seo--keywords)

---

## 📖 About the Project

The main goal of this repository is to demonstrate **PLC-based valve control** in the context of agricultural applications. It combines logic programming (function blocks) with modern HMI interfaces via ISOBUS Virtual Terminals (VT).

It includes numerous exercises (`Uebung_001` through `Uebung_160`) that lead step by step from simple logic gates to complex sequence controls and communication protocols.

---

## ⚙️ Main Components

### 1. Valve Control (Logic)
Implementation of control logic for hydraulic valves.
- **Functions:** Time-controlled sequences, interlocks, PWM actuation.
- **Safety:** Emergency-stop routines and error handling.

### 2. ISOBUS Integration (HMI)
Complete design projects for **Virtual Terminals (VT)**.
- **ISO-Designer projects:** Contain masks, softkeys, and alarm messages (`Workspace`, `Workspace_Joystick`, `Workspace_PWM`, `Workspace_TECU`, `Workspace_TC_SC`, `Workspace_Horse`, `Workspace_Scroll`, `Workspace_Tester`).
- **Pool files:** `.jop`, `.jvi`, and image resources for various resolutions (monochrome & color).
- **Task Controller (TC-SC):** Section Control examples (`.dvc` files).

### 3. APIXON I/O Client (OPC UA)
A browser-based test client (`apixon-io-client/`) for I/O access via **OPC UA**.
- **Technologies:** Vue 3, TypeScript, Vite (single-file build), Vitest for unit/coverage tests.
- **Purpose:** Manually setting/observing inputs/outputs of a FORTE application directly in the browser, without additional tools.

### 4. Training Exercises
A structured series of learning modules:
- Fundamentals of digital logic (AND, OR, XOR).
- Timers (TON, TOF, TP).
- State machines and sequences.
- Data conversion and arrays.

---

## 🛠 Technologies Used

* **IDE:** [Eclipse 4diac IDE](https://www.eclipse.org/4diac/) (IEC 61131-3 / IEC 61499 Standard)
* **Runtime:** Eclipse FORTE (4diac RTE)
* **HMI Design:** Jetter / Bucher ISO-Designer (for ISOBUS VT)
* **Communication:** CAN bus, SAE J1939, ISO 11783 (ISOBUS)
* **Hardware targets:** ESP32, PC (soft-PLC), mobile controller

---

## 📂 Folder Structure

A brief overview of the most important directories:

```text
4diac_training1/
├── Ventilsteuerung/
│   ├── 4diacIDE-workspace/       # Main workspace for 4diac projects
│   │   ├── test_AX/              # Exercise series AX (with AX adapter)
│   │   ├── test_B/               # Exercise series B (without AX adapter)
│   │   ├── test_VV/              # Exercise series VV (distributed processing)
│   │   └── .lib/                 # Libraries (logiBUS®, isobus, iec61131, iec61499, OSCAT)
│   ├── ISO-DesignerProjects/     # HMI/VT designs
│   │   ├── Workspace/            # Base pool for most exercises
│   │   ├── Workspace_Joystick/   # Joystick integration
│   │   ├── Workspace_PWM/        # PWM visualization
│   │   ├── Workspace_TECU/       # Reading the tractor ECU
│   │   ├── Workspace_TC_SC/      # Task Controller / Section Control masks
│   │   ├── Workspace_Horse/      # Extended HMI exercise
│   │   ├── Workspace_Scroll/     # Scroll/list display
│   │   └── Workspace_Tester/     # I/O test masks
│   ├── TaskController-SC/        # Section Control configurations (.dvc)
│   ├── boot-files/               # FORTE .fboot startup files for the target devices
│   ├── apixon-io-client/         # Browser-based OPC UA I/O test client (Vue/TypeScript/Vite)
│   └── scripts_central/          # Python helper scripts (library/naming consistency, conversion)
├── .github/                      # CI workflows (incl. test coverage for the I/O client)
├── README.md
└── README.en.md
```

## ✅ Prerequisites

* [Eclipse 4diac IDE](https://www.eclipse.org/4diac/) (tested with `4diac-ide_3.2.0`, see `readme.txt`) incl. Java runtime environment
* Jetter / Bucher **ISO-Designer** for editing the `.jop`/`.jvi` VT pool files
* **Node.js** (for `apixon-io-client`, `npm install && npm run build`)
* **Python 3** (for the helper scripts in `scripts_central/`)
* Optional: FORTE runtime environment (PC or target device) for deploying the `.fboot` files

## 🚀 Getting Started

### 1. Get the project
You have two options for obtaining the files:

* **Option A: ZIP download (simple & fast)** You can download the current state directly as a ZIP file. This requires **no Git client**.  
    📦 [**Go to Downloads / Releases**](https://github.com/Meisterschulen-am-Ostbahnhof-Munchen/4diac_training1/releases)

* **Option B: Clone the repository (for developers)** Use this method if you want to use version control:
    ```bash
    git clone https://github.com/Meisterschulen-am-Ostbahnhof-Munchen/4diac_training1.git
    ```

### 2. Start the 4diac IDE
Select the `Ventilsteuerung/4diacIDE-workspace` folder from the downloaded package as your workspace.

### 3. Import libraries
Make sure the `isobus`, `logiBUS`, and `iec61131` libraries are correctly linked on the path.

### 4. Deploy
Use the `.launch` files, or the `.fboot` files in the `Ventilsteuerung/boot-files` folder, to load the application onto your target device (or the FORTE PC).

-----

## 📚 Documentation & Exercise Series

Detailed guides and descriptions of the individual exercise packages are available in our ReadTheDocs documentation.

| Area | Description | Documentation |
| :--- | :--- | :--- |
| **Exercises AX** | Fundamentals of valve control (series AX) | [📘 Go to documentation](https://meisterschulen-am-ostbahnhof-munchen-docs.readthedocs.io/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test_AX/Uebungen_doc/Uebungen.html) |
| **Exercises B** | Advanced exercises without the AX prefix | [📙 Go to documentation](https://meisterschulen-am-ostbahnhof-munchen-docs.readthedocs.io/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test_B/Uebungen_doc/Uebungen.html) |
| **Exercises VV** | Distributed processing & communication | [🚀 Go to documentation](https://meisterschulen-am-ostbahnhof-munchen-docs.readthedocs.io/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test_VV/Uebungen_doc/Uebungen.html) |

## 🔍 SEO & Keywords

**Subject areas:**
`Automation Engineering`, `Mobile Automation`, `Agricultural Technology`, `PLC Programming`, `Embedded Systems`

**Technologies:**
`Eclipse 4diac`, `FORTE`, `IEC 61131-3`, `IEC 61499`, `Function Block Diagram (FBD)`, `Structured Text (ST)`, `ESP32`

**Protocols & Standards:**
`ISOBUS`, `ISO 11783`, `SAE J1939`, `CAN Bus`, `Virtual Terminal (VT)`, `Task Controller (TC)`

**Specific:**
`Valve Control`, `Hydraulics`, `Master Craftsman School Project`, `Open Source PLC`

-----

**Note:** This project is primarily intended for educational purposes as part of the Meisterschulen am Ostbahnhof München (Master Craftsman Schools at Munich East Station).

<https://www.ms-muc-docs.de/>

<https://www.ms-muc.de/>
