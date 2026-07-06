---
name: iec61499-creator
description: Use this skill to create, edit, structure, and validate IEC 61499 library elements (Basic FBs, Composite FBs, Service Interface FBs, Adapters, Subapps, Devices, Resources, Systems, DataTypes) against standard schemas.
---

# IEC 61499 Library Element Creator Skill

This skill provides XSD schemas, templates, and validation scripts to create valid IEC 61499 elements.

## Directory Structure
- `schemas/`: XSD schemas defining valid IEC 61499 elements (e.g., `fbtype.xsd`, `adaptertype.xsd`, etc.)
- `templates/`: Boilerplate XML files for various library elements (e.g., `Basic.fbt`, `Composite.fbt`, `Adapter.adp`, `SubApp.sub`, etc.)
- `references/`: Reference documentation for keywords and type compatibility.
- `scripts/validate.py`: Python validation script using `lxml` to validate an XML file against its matching XSD schema.

## How to Use This Skill

### 1. Creating a New Library Element
To create a new element (e.g., a Basic Function Block, Adapter, or Subapp), start by copying the appropriate template from the `templates/` directory:
- **Basic FB**: Use `templates/Basic.fbt` or `templates/TemplateBasic.fbt`
- **Composite FB**: Use `templates/Composite.fbt`
- **Service Interface FB (SIFB)**: Use `templates/ServiceInterface.fbt`
- **Adapter**: Use `templates/Adapter.adp`
- **Subapplication**: Use `templates/SubApp.sub`
- **Data Type**: Use `templates/TemplateStruct.dtp`
- **Attribute Declaration**: Use `templates/AttributeDeclaration.atp`

Copy the template to the desired location and rename it, then update its `Name` attribute on the root tag.

### 2. Validating the XML Element
Always run the validation script to ensure that the XML you created or modified is fully compliant with the XSD schema.

#### Prerequisites
Make sure `lxml` is installed:
```bash
python -m pip install lxml
```

#### Commands
Run the validator by passing the path of the XML file:
```bash
python .agents/skills/iec61499-creator/scripts/validate.py <path_to_xml_file>
```

### 3. Key XML Schema Guidelines
- **PascalCase Attributes**: All attributes (like `Name`, `Comment`, `Type`, `Var`, `Value`) use PascalCase. Note that `Var` is capitalized (e.g. `<With Var="QI"/>`).
- **Empty Collections**: Elements like `EventInputs`, `EventOutputs`, `InputVars`, and `OutputVars` can be empty (e.g., `<InputVars/>`).
- **Self-Closing Tags**: Empty elements (e.g., `SubAppEvent`, `Identification`, `VersionInfo` with no nested tags) should be written as self-closing tags (e.g. `<Identification />`) to prevent validation failures caused by whitespace character content.

### 4. ST Code, Datatypes & Conversions Guidelines
When writing Structured Text (ST) code in Algorithms or choosing Datatypes/Conversions:
- **Avoid Reserved Keywords**: Do not use reserved IEC 61131-3 / IEC 61499 keywords (e.g., control flow, standard types, time units) as variable, block, or event names. See [Keywords.md](references/Keywords.md) for the complete list.
- **Type Compatibility**: Ensure data connections follow the rule "Target must be able to hold Source" (e.g. `SINT` -> `INT` is allowed, but `INT` -> `UINT` is not). See [Typkompatibilitaet.md](references/Typkompatibilitaet.md) for compatibility matrices.
- **Explicit Casting & Reinterpret Casts**: In ST or networks, use explicit functions (e.g., `[SOURCE]_TO_[TARGET]`). Note that converting bit-strings (like `DWORD`) directly to float/numeric types performs a `reinterpret_cast` of the raw bits. For mathematical float conversion from integer-valued DWORDs, use double casting: `UDINT_TO_REAL(DWORD_TO_UDINT(var))`.
- **Precision Limits**: Use `LREAL` instead of `REAL` for signal values or values exceeding `16,777,216` to prevent precision loss.

