# Typ-Kompatibilität & Konvertierungen (Casting) in 4diac / IEC 61499

Diese Referenz beschreibt die Regeln für Datenverbindungen und Typkonvertierungen in 4diac-IDE sowie die korrekte Verwendung von Konvertierungsfunktionen.

---

## 1. Datenverbindungen (Implizite Zuweisungen)

Eine Datenverbindung im FB-Netzwerk bzw. eine implizite Zuweisung ist nur erlaubt, wenn **das Target die Source aufnehmen kann** (`targetType.isAssignableFrom(sourceType)`). Das bedeutet, der Zieltyp muss gleich groß oder allgemeiner sein als der Quelltyp.

### Integer-Typen (Ganzzahlen)
* **Signed:** `SINT` (8-Bit) $\rightarrow$ `INT` (16-Bit) $\rightarrow$ `DINT` (32-Bit) $\rightarrow$ `LINT` (64-Bit)
* **Unsigned:** `USINT` (8-Bit) $\rightarrow$ `UINT` (16-Bit) $\rightarrow$ `UDINT` (32-Bit) $\rightarrow$ `ULINT` (64-Bit)
* ⚠️ **Achtung:** Es gibt **keine** implizite Konvertierung zwischen Signed und Unsigned (z. B. `INT` $\rightarrow$ `UINT` ist verboten!).

### Gleitkommazahlen
* `REAL` (32-Bit) $\rightarrow$ `LREAL` (64-Bit)
* **Integer-Zuweisung an Reals:**
  * `REAL` akzeptiert implizit: `SINT`, `INT`, `USINT`, `UINT`
  * `LREAL` akzeptiert implizit: `SINT`, `INT`, `DINT`, `USINT`, `UINT`, `UDINT`, `REAL`

### Bit-Typen
* `BOOL` $\rightarrow$ `BYTE` $\rightarrow$ `WORD` $\rightarrow$ `DWORD` $\rightarrow$ `LWORD`
* ⚠️ **Achtung:** Dies ist eine Einbahnstraße. Bit-Typen können nicht implizit in numerische Typen (wie `INT` oder `REAL`) konvertiert werden.

### Zeichenketten & Strings
* `CHAR` $\rightarrow$ `STRING` (8-Bit ASCII)
* `WCHAR` $\rightarrow$ `WSTRING` (16-Bit Unicode/UCS-2)
* ⚠️ **Achtung:** `CHAR`/`STRING` und `WCHAR`/`WSTRING` sind untereinander nicht kompatibel.

### Zeit- & Datums-Typen
* `TIME` $\rightarrow$ `LTIME`
* `DATE` $\rightarrow$ `LDATE`
* `TOD` (Time of Day) $\rightarrow$ `LTOD`
* `DT` (Date and Time) $\rightarrow$ `LDT`

---

## 2. Veraltete Konvertierungsbausteine & F_MOVE

* **Identitäts-Konvertierungsbausteine** aus dem Ordner `convert-1.0.0` (wie `BOOL2BOOL`, `INT2INT`, `REAL2REAL`, etc.) sind **veraltet (deprecated)**.
* **Lösung:** Verwende stattdessen den generischen Baustein `F_MOVE` (`iec61131::selection::F_MOVE`).
* In XML-Netzwerkdateien muss für `F_MOVE` zwingend das Attribut `DataType` auf den gewünschten Typ gesetzt werden:
  ```xml
  <FB Name="MeinFMove" Type="iec61131::selection::F_MOVE">
      <Attribute Name="DataType" Value="BOOL"/>
  </FB>
  ```

---

## 3. Explizite Konvertierungen (Casting)

Wenn Verbindungen oder Zuweisungen nicht implizit erlaubt sind, muss explizit gecastet werden.
* **In ST:** Aufruf der Funktion `[SOURCE_TYPE]_TO_[TARGET_TYPE]` (z. B. `DINT_TO_UDINT(dint_var)`).
* **Im FB-Netzwerk:** Dazwischenschalten des entsprechenden Konvertierungsbausteins (z. B. `DINT_TO_UDINT`).

### ⚠️ Wichtig: Bit-Strings zu Numerischen Typen (reinterpret_cast)
Konvertierungen von Bit-Strings (`BYTE`, `WORD`, `DWORD`, `LWORD`) zu numerischen Typen (`REAL`, `INT`, `DINT` etc.) werden als Bit-Ebene **`reinterpret_cast`** ausgeführt (Kopieren der Roh-Bits ohne mathematische Anpassung).

#### Szenario A: Im Bit-String ist ein Zahlenwert (z.B. 123) gespeichert, der in REAL umgewandelt werden soll
* **Falsch:** `DWORD_TO_REAL(dword_var)` $\rightarrow$ interpretiert die Bits von 123 direkt als Float, was mathematisch eine extrem kleine Zahl nahe 0 ergibt.
* **Richtig (Doppel-Konvertierung):**
  * **In ST:** `UDINT_TO_REAL(DWORD_TO_UDINT(dword_var))`
  * **Im FB-Netzwerk:** `[DWORD-Ausgang]` $\rightarrow$ `[DWORD_TO_UDINT]` $\rightarrow$ `[UDINT_TO_REAL]` $\rightarrow$ `[REAL-Eingang]`

#### Szenario B: Im Bit-String ist bereits ein IEEE-754 Float-Bitmuster gespeichert (z. B. von Modbus)
* **Richtig:** `DWORD_TO_REAL(dword_var)` $\rightarrow$ interpretiert die Roh-Bits direkt als Float, was hier genau erwünscht ist.

### Nicht definierte Konvertierungen
Direkte Konvertierungen von Bit-Strings kleiner als 32-Bit in `REAL` sind in IEC 61131-3/IEC 61499 **nicht definiert**:
* `BYTE_TO_REAL` $\rightarrow$ **nicht definiert** (Korrekt: `BYTE` $\rightarrow$ `USINT` $\rightarrow$ `REAL`)
* `WORD_TO_REAL` $\rightarrow$ **nicht definiert** (Korrekt: `WORD` $\rightarrow$ `UINT` $\rightarrow$ `REAL`)
* `DWORD_TO_REAL` $\rightarrow$ Erlaubt (aber Achtung: reinterpret_cast, siehe oben! Korrekt für Zahlwert: `DWORD` $\rightarrow$ `UDINT` $\rightarrow$ `REAL`)
* `LWORD_TO_LREAL` $\rightarrow$ Erlaubt (Achtung: reinterpret_cast! Korrekt für Zahlwert: `LWORD` $\rightarrow$ `ULINT` $\rightarrow$ `LREAL`)

---

## 4. Präzisionsverlust ab 16.777.216 (REAL vs. LREAL)

`REAL` hat eine Mantisse von 24 Bit und kann nur etwa **7 Dezimalstellen** präzise darstellen. Ab dem Wert **16.777.216** ($2^{24}$) tritt bei Zuweisungen an oder Konvertierungen in `REAL` ein Rundungsfehler/Präzisionsverlust auf:
* `UDINT#16777216` $\rightarrow$ `REAL#16777216.0` (Korrekt)
* `UDINT#16777217` $\rightarrow$ `REAL#16777216.0` (Präzisionsverlust!)

**Faustregel:** Bei Werten $\ge 16.777.216$ oder für FIELDBUS Signal-Bausteine (z. B. Modbus, Profinet) immer `LREAL` anstatt `REAL` verwenden (z. B. mit `UDINT_TO_LREAL` oder `ULINT_TO_LREAL`).
