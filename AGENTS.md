# AGENTS.md - 4diac Training Project Guidelines

This document provides guidelines for AI agents working on this Eclipse 4diac™ industrial automation training repository.

## Project Overview

- **Type**: Eclipse 4diac IDE workspace for IEC 61131-3 / IEC 61499 industrial automation
- **Focus**: Valve control (Ventilsteuerung) training with ISOBUS integration
- **Workspace**: `Ventilsteuerung/4diacIDE-workspace/`
- **Documentation**: <https://www.ms-muc-docs.de/>

## Build & Deployment Commands

### 4diac IDE Operations
- **Open Workspace**: Use `Ventilsteuerung/4diacIDE-workspace` as Eclipse workspace
- **Deploy Application**: Use `.launch` files in `Launches/` folders (e.g., `Deploy_App_AX.launch`)
- **Target Runtime**: Eclipse FORTE (4diac RTE) on PC or ESP32 hardware

### Python Helper Scripts

**Lint/Check Commands:**
```bash
# Check for missing AX exercises compared to standard exercises
python script/check_missing_ax.py

# Scan for naming mismatches (instance names that match other type names)
python script/scan_bad_names.py

# Fix naming mismatches automatically
python script/fix_bad_names.py

# Comprehensive scan of project structure
python script/comprehensive_scan.py

# Check sequence naming patterns
python script/scan_sequences.py
```

**File Conversion:**
```bash
# Convert .adp files to .xml recursively
python script/adp_to_xml.py

# Convert .xml back to .adp
python script/xml_to_adp.py
```

**Generate Splits:**
```bash
python script/generate_splits.py
python script/generate_cpp_splits.py
```

### Testing Individual Exercises

To test a single exercise (SUB application):
1. Open the `.SUB` file in 4diac IDE
2. Use the Launch configuration in `Launches/` folder
3. Deploy to local FORTE or target device

## Code Style Guidelines

### File Organization

**Directory Structure:**
```
Ventilsteuerung/4diacIDE-workspace/
├── test_AX/Uebungen/          # Exercises with AX adapters
├── test_B/Uebungen/             # Standard exercises (no AX prefix)
├── test_VV/                     # Distributed processing exercises
├── .lib/                        # Library dependencies
│   ├── adapter-3.0.0/           # Unidirectional adapters
│   ├── logiBUS-3.0.0/           # logiBUS I/O library
│   ├── isobus-3.0.0/            # ISOBUS/ISO 11783 protocol
│   ├── iec61131-3-bool-3.0.0/   # IEC 61131-3 boolean functions
│   └── ...
├── Launches/                    # Deployment configurations
└── MANIFEST.MF                  # Project dependencies
```

### Naming Conventions

**Exercise Names:**
- Format: `Uebung_XXX[_suffix][_AX].SUB`
- Examples: `Uebung_001.SUB`, `Uebung_001_AX.SUB`, `Uebung_010b4_sub_AX.SUB`
- Use uppercase `.SUB` extension

**Function Block Instances:**
- Use descriptive CamelCase names: `DigitalInput_I1`, `Timer_ON`, `ValveControl`
- **NEVER** use a type name as an instance name if it's a different type
- Bad: Name="E_T_FF" Type="E_T_FF_SR" (confusing - instance name is a different type)
- Good: Name="E_T_FF_SR" Type="E_T_FF_SR" or Name="MyTimer" Type="E_T_FF_SR"

**Type References:**
- Use fully qualified names with namespace: `logiBUS::io::DI::logiBUS_IXA`
- Namespace separator: `::`
- Library version: `3.0.0` (semantic versioning)

**Adapter Naming:**
- AX: Unidirectional ANY type adapter
- A2X: Bidirectional adapter
- AB (BYTE), AI (INT), AR (REAL), etc.
- See `Unidirectional_Adapters.md` for full list

### File Formats

**XML Structure (.SUB files):**
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
    <SubAppInterfaceList>
    </SubAppInterfaceList>
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

### Import Guidelines

**Always import required types in `<CompilerInfo>`:**
```xml
<CompilerInfo packageName="Uebungen">
    <Import declaration="logiBUS::io::DI::logiBUS_IXA"/>
    <Import declaration="logiBUS::io::DQ::logiBUS_QXA"/>
    <Import declaration="iec61131-3::F_EDGE"/>
</CompilerInfo>
```

**Available Libraries:**
- `adapter-3.0.0`: Unidirectional adapters (AX, A2X, AE, etc.)
- `logiBUS-3.0.0`: logiBUS I/O blocks (Digital/Analog I/O)
- `isobus-3.0.0`: ISOBUS/ISO 11783 protocol blocks
- `iec61131-3-bool-3.0.0`: Boolean logic (AND, OR, XOR, F_EDGE, etc.)
- `events_plus-3.0.0`: Extended event handling
- `convert_plus-3.0.0`: Data conversion utilities

### Coordinates & Layout

- Position FBs using `x` and `y` attributes (grid units, typically multiples of 200)
- Connection routing uses `dx1`, `dx2` for horizontal segments
- Keep diagrams organized with consistent spacing

### Error Handling

**Safety & Error Patterns:**
- Include emergency stop (Not-Halt) routines where applicable
- Use `QI` (Quality Input) parameters set to `TRUE` for enabling blocks
- Document safety-critical logic in comments

### Comments & Documentation

- Add descriptive `Comment` attributes to SubAppType
- Include copyright notice in `<Identification>`
- Track versions in `<VersionInfo>` with Author and Date
- Use German for exercise descriptions (project language)

## Deployment & Testing

**System Configuration (`test_AX.sys`):**
- Defines resources like `FORTE_PC_AX.EMB_RES_AX`
- Launches reference this system file

**Before Committing:**
1. Run `python script/scan_bad_names.py` to check for naming issues
2. Run `python script/check_missing_ax.py` if working on AX series
3. Ensure all imports are declared in `<CompilerInfo>`
4. Verify XML is well-formed

## License

All files must include EPL 2.0 license header in `<Identification>`:
```
Copyright (c) YYYY Meisterschulen am Ostbahnhof
SPDX-License-Identifier: EPL-2.0
```
