# FIELDBUS_SIGNAL Erweiterung - Offene Punkte

## Übersicht Datentypen

| Bits | Name | Basis-Baustein | Adapter-Baustein | Status |
|------|------|----------------|-------------------|--------|
| 2 bit | QUARTER | FIELDBUS_QUARTER_TO_SIGNAL | AQ_FIELDBUS_QUARTER_TO_SIGNAL | ✅ |
| 3 bit | TRIO | FIELDBUS_TRIO_TO_SIGNAL | ATRIO_FIELDBUS_TRIO_TO_SIGNAL | ❌ OFFEN |
| 4 bit | NIBBLE | FIELDBUS_NIBBLE_TO_SIGNAL | ANIBBLE_FIELDBUS_NIBBLE_TO_SIGNAL | ❌ OFFEN |

## Offene Fragen

### 1. Konstanten für TRIO (3 bit)
- Welche Konstanten sollen verwendet werden?
- Vorschlag: `DONT_CARE_3bit`, `NOT_AVAILABLE_3Bit`
- Alternativen?

### 2. Konstanten für NIBBLE (4 bit)
- Welche Konstanten sollen verwendet werden?
- Vorschlag: `DONT_CARE_4bit`, `NOT_AVAILABLE_4Bit`
- Alternativen?

### 3. Gültigkeitsprüfung
- Bei QUARTER: `IF (IN < DONT_CARE_2bit)` (logisch: kleiner als DONT_CARE = gültig)
- Bei anderen: `IF (IN <= VALID_SIGNAL_XX)` (kleiner oder gleich = gültig)
- Wie soll die Prüfung für TRIO und NIBBLE aussehen?

## Bereits implementiert

### Basis-Bausteine (10)
- FIELDBUS_BYTE_TO_SIGNAL
- FIELDBUS_WORD_TO_SIGNAL
- FIELDBUS_DWORD_TO_SIGNAL
- FIELDBUS_UINT_TO_SIGNAL
- FIELDBUS_USINT_TO_SIGNAL
- FIELDBUS_UDINT_TO_SIGNAL
- FIELDBUS_ULINT_TO_SIGNAL
- FIELDBUS_INT_TO_SIGNAL
- FIELDBUS_LINT_TO_SIGNAL
- FIELDBUS_QUARTER_TO_SIGNAL

### Adapter-Bausteine (10)
- AB_FIELDBUS_BYTE_TO_SIGNAL
- AW_FIELDBUS_WORD_TO_SIGNAL
- AD_FIELDBUS_DWORD_TO_SIGNAL
- AUI_FIELDBUS_UINT_TO_SIGNAL
- AI_FIELDBUS_INT_TO_SIGNAL
- AUS_FIELDBUS_USINT_TO_SIGNAL
- AULI_FIELDBUS_ULINT_TO_SIGNAL
- ALI_FIELDBUS_LINT_TO_SIGNAL
- AUDI_FIELDBUS_UDINT_TO_SIGNAL
- AQ_FIELDBUS_QUARTER_TO_SIGNAL

## Adapter-Namensschema

| Prefix | Datentyp |
|--------|----------|
| AB | BYTE (8 bit) |
| AW | WORD (16 bit) |
| AD | DWORD (32 bit) |
| AI | INT (16 bit signed) |
| AUI | UINT (16 bit unsigned) |
| AUS | USINT (8 bit unsigned) |
| AULI | ULINT (64 bit unsigned) |
| ALI | LINT (64 bit signed) |
| AUDI | UDINT (32 bit unsigned) |
| AQ | BYTE (2 bit) |
| ATRIO | BYTE (3 bit) | ⬅️ OFFEN
| ANIBBLE | BYTE (4 bit) | ⬅️ OFFEN