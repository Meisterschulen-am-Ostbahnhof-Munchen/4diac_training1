import os
import sys

# Add script directory to sys.path to allow importing sibling modules
script_dir = os.path.dirname(os.path.realpath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from validate import validate_xml, ValidationError

def test_all_templates(templates_dir, schemas_dir):
    """
    Validates all templates in templates_dir against the schemas in schemas_dir.
    Returns a dict mapping filename to a list of error messages (empty list if success).
    Raises FileNotFoundError if templates_dir does not exist.
    Raises ValueError if no templates are found.
    """
    valid_ext = {'.fbt', '.adp', '.sub', '.dtp', '.atp', '.fct', '.gcf'}
    if not os.path.isdir(templates_dir):
        raise FileNotFoundError(f"Templates directory does not exist: {templates_dir}")
        
    files = sorted([
        f for f in os.listdir(templates_dir) 
        if os.path.isfile(os.path.join(templates_dir, f)) and os.path.splitext(f)[1].lower() in valid_ext
    ])
    
    if not files:
        raise ValueError(f"No templates found in {templates_dir}")
        
    results = {}
    for file in files:
        full_path = os.path.join(templates_dir, file)
        try:
            validate_xml(full_path, schemas_dir)
            results[file] = []
        except ValidationError as ve:
            results[file] = ve.errors
        except Exception as e:
            results[file] = [str(e)]
            
    return results

def main():
    templates_dir = os.path.abspath(os.path.join(script_dir, '..', 'templates'))
    schemas_dir = os.path.abspath(os.path.join(script_dir, '..', 'schemas'))
    
    try:
        results = test_all_templates(templates_dir, schemas_dir)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    all_success = True
    for file, errors in results.items():
        print(f"--- Validating {file} ---")
        if not errors:
            print("SUCCESS")
        else:
            all_success = False
            print("FAILED")
            for err in errors:
                print(err)
                
    if not all_success:
        sys.exit(1)
    print("All templates validated successfully.")
    sys.exit(0)

if __name__ == '__main__':
    main()
