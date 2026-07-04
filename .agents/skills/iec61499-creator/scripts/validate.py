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

def validate_xml(xml_path, schemas_dir):
    xsd_valid = False
    try:
        # Parse XML to find the root element type
        parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False, no_network=True, load_dtd=False)

        xml_doc = etree.parse(xml_path, parser)
        
        # Remove blank text/tail nodes (whitespaces) so that empty tags with spacing don't fail XSD validation
        for el in xml_doc.iter():
            if el.text is not None and not el.text.strip():
                el.text = None
            if el.tail is not None and not el.tail.strip():
                el.tail = None
                
        root_tag = xml_doc.getroot().tag
        
        # Strip namespace prefix if any
        if '}' in root_tag:
            root_tag = root_tag.split('}', 1)[1]
            
        print(f"File root tag: <{root_tag}>")
        
        schema_file = ROOT_TO_SCHEMA.get(root_tag)
        if not schema_file:
            print(f"Warning: No schema mapping found for root element <{root_tag}>. Skipping XSD validation.")
            xsd_valid = True
        else:
            schema_path = os.path.join(schemas_dir, schema_file)
            if not os.path.exists(schema_path):
                print(f"Error: Schema file not found: {schema_path}")
                sys.exit(1)
                
            print(f"Validating against: {schema_file}...")
            
            # Load and parse the schema
            schema_doc = etree.parse(schema_path)
            xml_schema = etree.XMLSchema(schema_doc)
            
            if xml_schema.validate(xml_doc):
                print("XSD Validation SUCCESS: File is valid against the schema.")
                xsd_valid = True
            else:
                print("XSD Validation FAILED:")
                for error in xml_schema.error_log:
                    print(f"  Line {error.line}: {error.message}")
                sys.exit(1)
            
    except etree.XMLSyntaxError as e:
        print(f"XML Syntax Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error during XSD validation: {e}")
        sys.exit(1)

    # Keywords validation
    if xsd_valid:
        print("Running Keyword validation...")
        keywords, allowed_contexts = load_keywords()
        violations = check_keywords_in_xml(xml_doc, keywords, allowed_contexts)
        if violations:
            print("Keyword Validation FAILED:")
            for v in violations:
                print(f"  Line {v['line']}: {v['message']}")
            sys.exit(1)
        else:
            print("Keyword Validation SUCCESS: No reserved keyword violations found.")
            sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate.py <path_to_xml_file>")
        sys.exit(1)
        
    xml_path = sys.argv[1]
    # schemas_dir is relative to this script's directory (scripts/../schemas)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    schemas_dir = os.path.abspath(os.path.join(script_dir, '..', 'schemas'))
    
    validate_xml(xml_path, schemas_dir)
