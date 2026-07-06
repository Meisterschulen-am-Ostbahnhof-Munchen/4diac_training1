import os
import sys
import re
from lxml import etree

import json

def load_keywords():
    """Load keywords and allowed contexts from the local resources/keywords.json file."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.abspath(os.path.join(script_dir, '..', 'resources', 'keywords.json'))
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        keywords = set(data.get("keywords", []))
        allowed_contexts = data.get("allowed_contexts", {})
        if keywords:
            return keywords, allowed_contexts
    except Exception as e:
        print(f"Error: Failed to load local keywords.json: {e}")
        sys.exit(1)
            
    print("Error: keywords.json is empty or invalid.")
    sys.exit(1)


def check_keywords_in_xml(xml_path_or_doc, keywords, allowed_contexts):
    """Checks an XML file or parsed document for reserved keyword violations in 'Name' attributes."""
    violations = []
    try:
        if isinstance(xml_path_or_doc, (str, bytes)) or hasattr(xml_path_or_doc, '__fspath__'):
            # Securely parse the XML file using a binary stream
            parser = etree.XMLParser(
                remove_blank_text=True,
                resolve_entities=False,
                no_network=True,
                load_dtd=False,
            )
            with open(xml_path_or_doc, 'rb') as f:
                xml_doc = etree.parse(f, parser)
        else:
            # Use already parsed document directly to improve efficiency
            xml_doc = xml_path_or_doc
        
        # Traverse all elements
        for elem in xml_doc.iter():
            if not isinstance(elem.tag, str):
                continue
            name_val = elem.get("Name")
            if name_val:
                name_upper = name_val.upper()
                if name_upper in keywords:
                    # Check if it is an allowed context/tag
                    tag = elem.tag
                    if '}' in tag:
                        tag = tag.split('}', 1)[1]
                    
                    allowed_tags = allowed_contexts.get(name_upper, [])
                    tag_lower = tag.lower()
                    allowed_tags_lower = [t.lower() for t in allowed_tags]
                    if tag_lower not in allowed_tags_lower:
                        violations.append({
                            "line": elem.sourceline,
                            "tag": tag,
                            "name": name_val,
                            "message": f"Bezeichner '{name_val}' im Tag <{tag}> ist ein reserviertes Schlüsselwort."
                        })

    except etree.XMLSyntaxError as e:
        violations.append({
            "line": e.position[0],
            "tag": "XML",
            "name": "",
            "message": f"XML Syntax Fehler: {e}"
        })
    except Exception as e:
        violations.append({
            "line": 0,
            "tag": "System",
            "name": "",
            "message": f"Unerwarteter Fehler: {e}"
        })

    return violations


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_keywords.py <path_to_xml_file>")
        sys.exit(1)

    xml_path = sys.argv[1]
    keywords, allowed_contexts = load_keywords()
    
    violations = check_keywords_in_xml(xml_path, keywords, allowed_contexts)
    if violations:
        print(f"Keyword-Validierung FEHLGESCHLAGEN für {xml_path}:")
        for v in violations:
            print(f"  Zeile {v['line']}: {v['message']}")
        sys.exit(1)
    else:
        print(f"Keyword-Validierung ERFOLGREICH für {xml_path}")
        sys.exit(0)

if __name__ == "__main__":
    main()
