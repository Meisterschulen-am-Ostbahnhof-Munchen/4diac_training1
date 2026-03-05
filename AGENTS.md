# AGENTS.md - 4diac Training Project Guidelines

This document provides guidelines for AI agents working on this Eclipse 4diac™ industrial automation training repository.

## Project Overview

- **Type**: Eclipse 4diac IDE workspace for IEC 61131-3 / IEC 61499 industrial automation
- **Focus**: Valve control (Ventilsteuerung) training with ISOBUS integration
- **Workspace**: `Ventilsteuerung/4diacIDE-workspace/`

## Build & Test Commands

### Python Helper Scripts (run from repository root)
```bash
# Check for missing AX exercises
python script/check_missing_ax.py

# Scan for naming mismatches (instance names matching other type names)
python script/scan_bad_names.py

# Auto-fix naming mismatches
python script/fix_bad_names.py

# Comprehensive project scan
python script/comprehensive_scan.py

# Check sequence naming patterns
python script/scan_sequences.py

# Check for missing AX FB variants
python script/check_missing_ax_fbs.py
```

### File Conversion
```bash
# Convert .adp to .xml
python script/adp_to_xml.py
# Convert .xml to .adp
python script/xml_to_adp.py
```

### 4diac IDE Testing
1. Open `.SUB` file in 4diac IDE
2. Use Launch configuration in `Launches/` folder
3. Deploy to FORTE (PC/ESP32)

## Directory Structure
```
Ventilsteuerung/4diacIDE-workspace/
├── test_AX/Uebungen/     # AX adapter exercises
├── test_B/Uebungen/      # Standard exercises
├── test_VV/              # Distributed processing
├── .lib/                 # Libraries (adapter, logiBUS, isobus, iec61131-3)
└── Launches/             # Deployment configs
```

## Naming Conventions

**Exercises**: `Uebung_XXX[_suffix][_AX].SUB` (e.g., `Uebung_001.SUB`, `Uebung_001_AX.SUB`)

**Function Block Instances**:
- Use descriptive CamelCase: `DigitalInput_I1`, `Timer_ON`, `ValveControl`
- **NEVER** use a type name as instance name if different type
- Bad: `Name="E_T_FF" Type="E_T_FF_SR"`
- Good: `Name="E_T_FF_SR" Type="E_T_FF_SR"` or `Name="MyTimer" Type="E_T_FF_SR"`

**Type References**: Use fully qualified names: `logiBUS::io::DI::logiBUS_IXA`
- Namespace separator: `::`
- Library version: `3.0.0`

**Adapters**: AX (unidirectional ANY), A2X (bidirectional), AB (BYTE), AI (INT), AR (REAL), etc.

## File Format (.SUB XML)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<SubAppType Name="Uebung_XXX_AX" Comment="Description">
    <Identification Standard="61499-2" Description="Copyright notice">
    </Identification>
    <VersionInfo Organization="Meisterschulen am Ostbahnhof" Version="1.0" 
                   Author="Name" Date="YYYY-MM-DD">
    </VersionInfo>
    <CompilerInfo packageName="Uebungen">
        <Import declaration="namespace::Type"/>
    </CompilerInfo>
    <SubAppInterfaceList></SubAppInterfaceList>
    <SubAppNetwork>
        <FB Name="InstanceName" Type="Namespace::Type" x="-4500" y="-800">
            <Parameter Name="QI" Value="TRUE"/>
        </FB>
        <AdapterConnections>
            <Connection Source="FB1.OUT" Destination="FB2.IN" dx1="980"/>
        </AdapterConnections>
    </SubAppNetwork>
</SubAppType>
```

## Required Imports

Always import in `<CompilerInfo>`:
```xml
<CompilerInfo packageName="Uebungen">
    <Import declaration="logiBUS::io::DI::logiBUS_IXA"/>
    <Import declaration="logiBUS::io::DQ::logiBUS_QXA"/>
    <Import declaration="iec61131-3::F_EDGE"/>
</CompilerInfo>
```

## Available Libraries
- `adapter-3.0.0`: Unidirectional adapters (AX, A2X, AE, etc.)
- `logiBUS-3.0.0`: logiBUS I/O blocks
- `isobus-3.0.0`: ISOBUS/ISO 11783 protocol
- `iec61131-3-bool-3.0.0`: Boolean logic (AND, OR, XOR, F_EDGE)
- `events_plus-3.0.0`: Extended event handling
- `convert_plus-3.0.0`: Data conversion

## Layout & Coordinates

- Position FBs using `x` and `y` (multiples of 200)
- Connection routing: `dx1`, `dx2` for horizontal segments

## Error Handling & Safety

- Include emergency stop (Not-Halt) routines where applicable
- Set `QI` (Quality Input) to `TRUE` for enabling blocks
- Document safety-critical logic

## Before Committing

1. Run `python script/scan_bad_names.py`
2. Run `python script/check_missing_ax.py` (for AX series)
3. Ensure all imports declared in `<CompilerInfo>`
4. Verify XML is well-formed

## License

All files must include EPL 2.0 header:
```
Copyright (c) YYYY Meisterschulen am Ostbahnhof
SPDX-License-Identifier: EPL-2.0
```
