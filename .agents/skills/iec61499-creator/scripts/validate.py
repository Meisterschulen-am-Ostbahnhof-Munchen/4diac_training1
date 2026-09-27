import sys
import os
import re
from lxml import etree

ROOT_TO_SCHEMA = {
    'FBType': 'fbtype.xsd',
    'AdapterType': 'adaptertype.xsd',
    'SubAppType': 'subapptype.xsd',
    'System': 'system.xsd',
    'DeviceType': 'devicetype.xsd',
    'ResourceType': 'resourcetype.xsd',
    'DataType': 'datatype.xsd',
    'AttributeDeclaration': 'attributedeclaration.xsd',
    'Function': 'function.xsd',
    'GlobalConstants': 'globalconstants.xsd'
}

# Add script directory to sys.path to allow importing sibling modules
script_dir = os.path.dirname(os.path.realpath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from check_keywords import load_keywords, check_keywords_in_xml  # noqa: E402 - must come after the sys.path patch above

class ValidationError(Exception):
    """Exception raised when XML validation fails."""
    def __init__(self, errors):
        self.errors = errors
        super().__init__("\n".join(errors))

_WORKSPACE_TYPE_CACHE = {}
_NAME_RE = re.compile(rb'<\w+Type\s+Name="([^"]+)"')
_PKG_RE = re.compile(rb'<CompilerInfo\s+packageName="([^"]+)"')

def get_workspace_type_index(xml_path):
    if not xml_path:
        return {}
    
    cur = os.path.dirname(os.path.abspath(xml_path))
    search_root = None
    while cur and cur != os.path.dirname(cur):
        if os.path.exists(os.path.join(cur, ".git")) or os.path.exists(os.path.join(cur, "4diacIDE-workspace")):
            search_root = cur
            break
        cur = os.path.dirname(cur)
        
    if not search_root:
        return {}
        
    if search_root in _WORKSPACE_TYPE_CACHE:
        return _WORKSPACE_TYPE_CACHE[search_root]
        
    workspace_types = {}
    for r, d, fs in os.walk(search_root):
        for f in fs:
            ext = os.path.splitext(f)[1].lower()
            if ext in ('.fbt', '.sub', '.adp'):
                path = os.path.join(r, f)
                try:
                    with open(path, 'rb') as fp:
                        header = fp.read(1500)
                        m_name = _NAME_RE.search(header)
                        m_pkg = _PKG_RE.search(header)
                        if m_name:
                            t_name = m_name.group(1).decode('utf-8', errors='ignore')
                            t_pkg = m_pkg.group(1).decode('utf-8', errors='ignore') if m_pkg else ''
                            fqn = f"{t_pkg}::{t_name}" if t_pkg else t_name
                            workspace_types[fqn.lower()] = (fqn, f, ext, path)
                except Exception:
                    pass
                
    _WORKSPACE_TYPE_CACHE[search_root] = workspace_types
    return workspace_types

def check_compiler_info_imports(xml_doc, xml_path):
    """
    Checks that <CompilerInfo><Import declaration="..."/></CompilerInfo> does NOT
    import Function Block Types (.fbt), SubApplication Types (.SUB/.sub), or
    Adapter Types (.adp).
    In 4diac IDE, <CompilerInfo><Import> is ONLY for:
      - Global Constants (.gcf)
      - Data Types (.dtp)
      - Functions (.fct)
    FB, SubApp, and Adapter types are resolved via the Type="..." attribute of
    <FB>, <SubApp>, <Adapter>, <Socket>, or <Plug> elements. Importing them causes
    the 4diac IDE error: "The import <declaration> does not exist (4diac IDE Import Problem)".
    """
    violations = []
    
    imports = []
    for elem in xml_doc.iter():
        if not isinstance(elem.tag, str):
            continue
        tag = elem.tag.split('}', 1)[1] if '}' in elem.tag else elem.tag
        if tag == "Import":
            decl = elem.get("declaration", "").strip()
            if decl:
                imports.append((elem.sourceline, decl))
                
    if not imports:
        return violations

    # Determine current file's package name if present
    current_pkg = ""
    for elem in xml_doc.iter():
        if not isinstance(elem.tag, str):
            continue
        tag = elem.tag.split('}', 1)[1] if '}' in elem.tag else elem.tag
        if tag == "CompilerInfo":
            current_pkg = elem.get("packageName", "").strip()
            break
        
    instantiated_types = set()
    instantiated_type_kinds = {}
    for elem in xml_doc.iter():
        if not isinstance(elem.tag, str):
            continue
        tag = elem.tag.split('}', 1)[1] if '}' in elem.tag else elem.tag
        if tag in ("FB", "SubApp", "Adapter", "Socket", "Plug"):
            t = elem.get("Type")
            if t:
                instantiated_types.add(t)
                instantiated_type_kinds[t] = tag
                if "::" not in t and current_pkg:
                    fqn = f"{current_pkg}::{t}"
                    instantiated_types.add(fqn)
                    instantiated_type_kinds[fqn] = tag

    workspace_types = get_workspace_type_index(xml_path)
    
    for line, decl in imports:
        # Check against fully qualified instantiated elements in the same file
        if decl in instantiated_types:
            kind = instantiated_type_kinds.get(decl, "network element")
            violations.append({
                "line": line,
                "message": (
                    f"Invalid import '{decl}'. {kind} types must NOT be imported in <CompilerInfo>. "
                    f"They are resolved automatically via the Type attribute on <{kind} ...> instances. "
                    f"In 4diac IDE, <CompilerInfo><Import> is ONLY for Global Constants (.gcf), DataTypes (.dtp), and Functions (.fct)."
                )
            })
            continue

        # Check against fully qualified workspace type files (.fbt, .sub/.SUB, .adp)
        decl_lower = decl.lower()
        if decl_lower in workspace_types:
            fqn, matched_file, matched_ext, _ = workspace_types[decl_lower]
            kind = "Function Block" if matched_ext == ".fbt" else ("SubApplication" if matched_ext == ".sub" else "Adapter")
            violations.append({
                "line": line,
                "message": (
                    f"Invalid import '{decl}'. Matches {kind} type '{fqn}' in '{matched_file}'. "
                    f"{kind} types must NOT be imported in <CompilerInfo>. "
                    f"In 4diac IDE, <CompilerInfo><Import> is ONLY for Global Constants (.gcf), DataTypes (.dtp), and Functions (.fct)."
                )
            })
            continue

        # Also check unqualified import if current_pkg is defined
        if "::" not in decl and current_pkg:
            unqual_fqn = f"{current_pkg}::{decl}".lower()
            if unqual_fqn in workspace_types:
                fqn, matched_file, matched_ext, _ = workspace_types[unqual_fqn]
                kind = "Function Block" if matched_ext == ".fbt" else ("SubApplication" if matched_ext == ".sub" else "Adapter")
                violations.append({
                    "line": line,
                    "message": (
                        f"Invalid import '{decl}'. Matches {kind} type '{fqn}' in '{matched_file}'. "
                        f"{kind} types must NOT be imported in <CompilerInfo>. "
                        f"In 4diac IDE, <CompilerInfo><Import> is ONLY for Global Constants (.gcf), DataTypes (.dtp), and Functions (.fct)."
                    )
                })

    return violations

def validate_xml(xml_path, schemas_dir):
    """
    Validates an XML file against its corresponding XSD schema and runs custom semantic checks.
    Raises ValidationError if any check fails.
    Returns the root_tag of the validated file.
    """
    errors = []
    
    # 1. Parse and validate against XSD
    try:
        parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False, no_network=True, load_dtd=False)
        with open(xml_path, 'rb') as f:
            xml_doc = etree.parse(f, parser)
        
        # Remove blank text/tail nodes (whitespaces) so that empty tags with spacing don't fail XSD validation
        for el in xml_doc.iter():
            if el.text is not None and not el.text.strip():
                el.text = None
            if el.tail is not None and not el.tail.strip():
                el.tail = None
                
        root_tag = xml_doc.getroot().tag
        if '}' in root_tag:
            root_tag = root_tag.split('}', 1)[1]
            
        schema_file = ROOT_TO_SCHEMA.get(root_tag)
        if schema_file:
            schema_path = os.path.join(schemas_dir, schema_file)
            if not os.path.exists(schema_path):
                raise FileNotFoundError(f"Schema file not found: {schema_path}")
                
            with open(schema_path, 'rb') as f:
                schema_doc = etree.parse(f)
            xml_schema = etree.XMLSchema(schema_doc)
            
            if not xml_schema.validate(xml_doc):
                errors.append(f"XSD Validation FAILED for {xml_path}:")
                for error in xml_schema.error_log:
                    errors.append(f"  Line {error.line}: {error.message}")
                raise ValidationError(errors)
        else:
            # No schema mapping found
            pass
            
    except etree.XMLSyntaxError as e:
        raise ValidationError([f"XML Syntax Error in {xml_path}: {e}"])
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError([f"Unexpected Error during XSD validation of {xml_path}: {e}"])

    # 2. Custom semantic validation checks (only if parse / XSD validation succeeded)
    semantic_errors = []
    
    # 2.1. OutputVars VarDeclaration name check (only the first one is allowed to be empty)
    output_var_violations = []
    for elem in xml_doc.iter():
        if not isinstance(elem.tag, str):
            continue
        tag = elem.tag.split('}', 1)[1] if '}' in elem.tag else elem.tag
        if tag == "OutputVars":
            parent = elem.getparent()
            if parent is not None and isinstance(parent.tag, str):
                parent_tag = parent.tag.split('}', 1)[1] if '}' in parent.tag else parent.tag
            else:
                parent_tag = ''
            if root_tag == "Function" and parent_tag == "InterfaceList":
                var_children = [
                    c for c in elem 
                    if isinstance(c.tag, str) and 
                    (c.tag.split('}', 1)[1] if '}' in c.tag else c.tag) == "VarDeclaration"
                ]
                for idx, var_child in enumerate(var_children):
                    name_val = var_child.get("Name", "")
                    if idx > 0 and name_val == "":
                        output_var_violations.append({
                            "line": var_child.sourceline,
                            "message": f"Only the first VarDeclaration in Function OutputVars can have an empty Name. Variable {idx + 1} must have a name."
                        })
    if output_var_violations:
        semantic_errors.append("OutputVars VarDeclaration Name Validation FAILED:")
        for v in output_var_violations:
            semantic_errors.append(f"  Line {v['line']}: {v['message']}")

    # 2.2. Keywords validation
    try:
        keywords, allowed_contexts = load_keywords()
        violations = check_keywords_in_xml(xml_doc, keywords, allowed_contexts)
        if violations:
            semantic_errors.append("Keyword Validation FAILED:")
            for v in violations:
                semantic_errors.append(f"  Line {v['line']}: {v['message']}")
    except Exception as e:
        semantic_errors.append(f"Keyword validation loader failed: {e}")

    # 2.3. CompilerInfo Import validation (SubApp, FB, and Adapter types must not be imported)
    try:
        import_violations = check_compiler_info_imports(xml_doc, xml_path)
        if import_violations:
            semantic_errors.append("CompilerInfo Import Validation FAILED:")
            for v in import_violations:
                semantic_errors.append(f"  Line {v['line']}: {v['message']}")
    except Exception as e:
        semantic_errors.append(f"CompilerInfo import validation failed: {e}")

    if semantic_errors:
        raise ValidationError(semantic_errors)
        
    return root_tag

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate.py <path_to_xml_file>")
        sys.exit(1)
        
    xml_path = sys.argv[1]
    # schemas_dir is relative to this script's directory (scripts/../schemas)
    schemas_dir = os.path.abspath(os.path.join(script_dir, '..', 'schemas'))
    
    try:
        root_tag = validate_xml(xml_path, schemas_dir)
        print(f"File root tag: <{root_tag}>")
        print("XSD Validation SUCCESS: File is valid against the schema.")
        print("OutputVars VarDeclaration Name Validation SUCCESS.")
        print("Keyword Validation SUCCESS: No reserved keyword violations found.")
        print("CompilerInfo Import Validation SUCCESS: No SubApp/FB/Adapter type imports found.")
        sys.exit(0)
    except ValidationError as ve:
        for err in ve.errors:
            print(err)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
