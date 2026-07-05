import sys
import os
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

from check_keywords import load_keywords, check_keywords_in_xml

class ValidationError(Exception):
    """Exception raised when XML validation fails."""
    def __init__(self, errors):
        self.errors = errors
        super().__init__("\n".join(errors))

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
        violations = check_keywords_in_xml(xml_path, keywords, allowed_contexts)
        if violations:
            semantic_errors.append("Keyword Validation FAILED:")
            for v in violations:
                semantic_errors.append(f"  Line {v['line']}: {v['message']}")
    except Exception as e:
        semantic_errors.append(f"Keyword validation loader failed: {e}")

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
