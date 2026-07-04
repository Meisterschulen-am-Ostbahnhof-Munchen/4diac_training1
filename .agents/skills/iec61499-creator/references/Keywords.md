# Reservierte Keywords in 4diac-IDE & IEC 61499

Bei der Benennung von Variablen, Funktionsbausteinen, Events, Adaptern oder Algorithmen dürfen die folgenden reservierten Schlüsselwörter (Keywords) **nicht** verwendet werden (Groß-/Kleinschreibung wird ignoriert). 

Diese Liste basiert auf [FordiacKeywords.java](https://github.com/eclipse-4diac/4diac-ide/blob/master/plugins/org.eclipse.fordiac.ide.model/src/org/eclipse/fordiac/ide/model/FordiacKeywords.java).

---

## 1. Datentypen & Datentyp-Klassen (Datatypes & Classes)

Diese Keywords dürfen nicht als Bezeichner verwendet werden, da sie vordefinierte Datentypen repräsentieren.

### Elementare Datentypen
* **Ganzzahlen (Signed):** `SINT`, `INT`, `DINT`, `LINT`
* **Ganzzahlen (Unsigned):** `USINT`, `UINT`, `UDINT`, `ULINT`
* **Gleitkommazahlen:** `REAL`, `LREAL`
* **Bit-Strings:** `BOOL`, `BYTE`, `WORD`, `DWORD`, `LWORD`
* **Zeichenketten:** `CHAR`, `WCHAR`, `STRING`, `WSTRING`
* **Zeit & Datum:** `TIME`, `LTIME`, `TIME_OF_DAY` (`TOD`), `LTIME_OF_DAY` (`LTOD`), `DATE`, `LDATE`, `DATE_AND_TIME` (`DT`, `LDATE_AND_TIME`, `LDT`)

### Generische Typklassen (ANY-Typen)
`ANY`, `ANY_DERIVED`, `ANY_ELEMENTARY`, `ANY_MAGNITUDE`, `ANY_NUM`, `ANY_SIGNED`, `ANY_UNSIGNED`, `ANY_INT`, `ANY_REAL`, `ANY_BIT`, `ANY_STRUCT`, `ANY_DATE`, `ANY_STRING`, `ANY_CHAR`, `ANY_CHARS`, `ANY_SCHARS`, `ANY_WCHARS`, `ANY_DURATION`, `ANY_TIME`

---

## 2. Zeiteinheiten (Time Units)

Diese Einheiten sind reserviert, um Zeitliterale (z. B. `T#5s`) zu definieren:
* `D` (Tag)
* `H` (Stunde)
* `M` (Minute)
* `S` (Sekunde)
* `MS` (Millisekunde)
* `US` (Mikrosekunde)
* `NS` (Nanosekunde)

---

## 3. Structured Text (ST) Keywords

Diese Schlüsselwörter bilden die Syntax der Structured Text-Programmiersprache und sind für Bezeichner strikt gesperrt.

### Kontrollstrukturen & Anweisungen
`IF`, `THEN`, `ELSIF`, `ELSE`, `END_IF`, `CASE`, `OF`, `END_CASE`, `FOR`, `TO`, `BY`, `DO`, `END_FOR`, `WHILE`, `END_WHILE`, `REPEAT`, `UNTIL`, `END_REPEAT`, `EXIT`, `CONTINUE`, `RETURN`

### Operatoren & Mathematische Funktionen
`ABS`, `ACOS`, `ADD`, `AND`, `ASIN`, `ATAN`, `ATAN2`, `COS`, `DIV`, `EQ`, `EXP`, `EXPT`, `GE`, `GT`, `LE`, `LT`, `LN`, `LOG`, `MAX`, `MID`, `MIN`, `MOD`, `MOVE`, `MUL`, `MUX`, `NE`, `NOT`, `OR`, `XOR`

### Strukturelle Deklarationen & Keywords
`VAR`, `END_VAR`, `VAR_INPUT`, `VAR_OUTPUT`, `VAR_IN_OUT`, `VAR_TEMP`, `VAR_EXTERNAL`, `VAR_GLOBAL`, `VAR_ACCESS`, `VAR_CONFIG`, `CONSTANT`, `RETAIN`, `NON_RETAIN`, `TYPE`, `END_TYPE`, `STRUCT`, `END_STRUCT`, `CLASS`, `END_CLASS`, `INTERFACE`, `END_INTERFACE`, `NAMESPACE`, `END_NAMESPACE`, `PROGRAM`, `END_PROGRAM`, `FUNCTION`, `END_FUNCTION`, `FUNCTION_BLOCK`, `END_FUNCTION_BLOCK`, `METHOD`, `END_METHOD`, `ACTION`, `END_ACTION`, `ALGORITHM`, `END_ALGORITHM`, `TRANSITION`, `END_TRANSITION`, `CONFIGURATION`, `END_CONFIGURATION`, `RESOURCE`, `END_RESOURCE`, `STEP`, `END_STEP`, `INITIAL_STEP`, `TASK`

### Weitere Keywords
`ARRAY`, `AT`, `FALSE`, `TRUE`, `FINAL`, `FIND`, `FROM`, `IMPLEMENTS`, `INSERT`, `INTERNAL`, `INTERVAL`, `LEFT`, `LEN`, `LIMIT`, `NULL`, `ON`, `OVERLAP`, `OVERRIDE`, `PRIORITY`, `PRIVATE`, `PROTECTED`, `PUBLIC`, `READ_ONLY`, `READ_WRITE`, `REF`, `REF_TO`, `REPLACE`, `RIGHT`, `SINGLE`, `SUPER`, `THIS`, `TRUNC`, `USING`, `WITH`

---

## 4. Standard-Funktionsbausteine & Trigger
`CTD`, `CTU`, `CTUD`, `F_EDGE`, `F_TRIG`, `R_EDGE`, `R_TRIG`, `RS`, `SR`, `TOF`, `TON`, `TP`
